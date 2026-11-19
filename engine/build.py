"""Pipeline de producción: guion → voz → tiempos → música/SFX → animación → MP4 + SRT.

Uso:  python build.py v01 [--stage all|audio|video|thumb] [--master] [--preview SEG]
"""
import argparse, importlib, json, math, os, re, shutil, subprocess, sys, time
import numpy as np, soundfile as sf, skia
sys.path.insert(0, os.path.dirname(__file__))
import audio, gfx
from tts import Supertonic, Aligner, split_markup, spoken, pause_after, trim, level, take_seed, SR as TSR

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FPS = 30

# ---------------------------------------------------------------- texto → frases (respetando {sub|habla})
def split_sentences(text):
    prot = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(".", "\x00").replace("?", "\x01").replace("!", "\x02").replace(":", "\x03"), text.strip())
    parts = re.split(r"(?<=[\.\?\!…:])\s+(?=[¿¡A-ZÁÉÍÓÚÑ0-9\"«({])", prot)
    return [p.replace("\x00", ".").replace("\x01", "?").replace("\x02", "!").replace("\x03", ":").strip() for p in parts if p.strip()]

# ---------------------------------------------------------------- etapa de audio
QA_THR = 0.90     # coincidencia mínima entre el guion y la voz reconocida para aceptar una toma
MAX_TRIES = 5     # tomas alternativas (otra semilla) si la verificación falla

def word_at(sent, char_i):
    """Tiempo (absoluto) de la palabra que contiene el carácter `char_i` del texto de la frase."""
    ws = sent.get("words")
    if not ws: return sent["start"] + (sent["end"] - sent["start"]) * char_i / max(1, len(sent["text"]))
    k = min(len(ws) - 1, sent["text"][:char_i].count(" "))
    return ws[k][1]

def group_takes(items, max_chars=250, max_sents=3):
    """Agrupa frases consecutivas en tomas (párrafos cortos) para que el ritmo entre frases sea natural."""
    groups = []; cur = []; n = 0
    for it in items:
        L = len(it["spk"])
        if cur and (n + L > max_chars or len(cur) >= max_sents): groups.append(cur); cur = []; n = 0
        cur.append(it); n += L + 1
    if cur:
        # una frase muy corta sola suena peor: se une a la toma anterior si cabe
        if groups and sum(len(it["spk"]) for it in cur) < 45 and sum(len(it["spk"]) for it in groups[-1] + cur) <= max_chars + 90:
            groups[-1] += cur
        else: groups.append(cur)
    return groups

VOICE_ENGINE = os.environ.get("VOICE_ENGINE", "chatterbox")
_SCR = "/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad"
CB = dict(python=os.environ.get("CHATTERBOX_PY", f"{_SCR}/cbenv/bin/python"), dir=os.environ.get("CHATTERBOX_DIR", f"{_SCR}/cbmodel"),
          cache=os.environ.get("VOICE_CACHE", f"{_SCR}/voice_cache"), shards=int(os.environ.get("CB_SHARDS", "2")))
# Referencias de voz (≈12 s de audio limpio cada una). Ver engine/voces/README.md
CB_VOICES = {"host": dict(ref=os.path.join(os.path.dirname(__file__), "voces", "narradora_ref.wav"), exaggeration=0.6, cfg=0.4),
             "copiloto": dict(ref=os.path.join(os.path.dirname(__file__), "voces", "copiloto_ref.wav"), exaggeration=0.5, cfg=0.45)}

def cb_batch(jobs):
    """Genera en paralelo (varios procesos) las tomas que no están en caché."""
    import hashlib
    todo = [j for j in jobs if not os.path.exists(j["out"])]
    if not todo: return
    os.makedirs(CB["cache"], exist_ok=True); n = max(1, min(CB["shards"], len(todo))); procs = []
    thr = max(1, (os.cpu_count() or 4) // n)
    for k in range(n):
        part = todo[k::n]; jf = os.path.join(CB["cache"], f"lote_{os.getpid()}_{k}.json")
        json.dump(part, open(jf, "w", encoding="utf-8"), ensure_ascii=False)
        env = dict(os.environ, CHATTERBOX_DIR=CB["dir"])
        procs.append(subprocess.Popen([CB["python"], os.path.join(os.path.dirname(__file__), "tts_chatterbox.py"), jf, "--threads", str(thr)], env=env,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True))
    # leer la salida de todos los procesos a la vez: si no, el que no se lee se bloquea al llenarse su tubería
    import threading
    def drain(p, k):
        for line in p.stdout:
            if line.startswith("[") or "Error" in line or "Traceback" in line: print(f"    [proceso {k}]", line.rstrip(), flush=True)
    ths = [threading.Thread(target=drain, args=(p, k), daemon=True) for k, p in enumerate(procs)]
    for th in ths: th.start()
    for p in procs: p.wait()
    for th in ths: th.join(timeout=5)
    if any(p.returncode for p in procs): raise RuntimeError("Falló la síntesis con Chatterbox")

def cb_job(text, voice, seed, exag=None, cfg=None):
    import hashlib
    v = dict(CB_VOICES.get(voice, CB_VOICES["host"]))
    if exag is not None: v["exaggeration"] = exag
    if cfg is not None: v["cfg"] = cfg
    key = hashlib.sha1(f"{text}|{voice}|{seed}|{v['exaggeration']}|{v['cfg']}|{os.path.getsize(v['ref'])}".encode()).hexdigest()[:20]
    return dict(text=text, seed=int(seed), ref=v["ref"], exaggeration=v["exaggeration"], cfg=v["cfg"], temperature=0.8,
                out=os.path.join(CB["cache"], f"{key}.wav"))

def load_take(path):
    from scipy import signal as _sg
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1: x = x.mean(axis=1)
    if sr != TSR:
        from math import gcd
        g = gcd(TSR, sr); x = _sg.resample_poly(x, TSR // g, sr // g).astype(np.float32)
    return level(trim(x))

NAMES = dict(narr_wav="narracion.wav", narr_mp3="narracion.mp3", srt="subtitulos.srt", script="guion.txt", thumb="miniatura.png")
def out_name(V, key): return V.get("names", {}).get(key, NAMES[key])

def build_audio(V, outdir, narr=None, aligner=None):
    aligner = aligner or Aligner()
    # 1) planificar tomas
    plan = []
    for bi, b in enumerate(V["beats"]):
        vo = b.get("vo", ""); voice = b.get("voice", V.get("voice", "host"))
        speed = b.get("speed", V.get("speed", 1.0))
        items = []
        for sx in (split_sentences(vo) if vo else []):
            sub, spk = split_markup(sx); items.append(dict(sub=sub, plain=spk, spk=spoken(spk)))
        human = f"{outdir}/voz_humana/beat_{bi:02d}.wav"
        if items and os.path.exists(human):
            plan.append([dict(bi=bi, take=items, voice="humana", speed=None, human=human)])
        else:
            plan.append([dict(bi=bi, take=tk, voice=voice, speed=speed, exag=b.get("exag"), cfg=b.get("cfg")) for tk in group_takes(items)])
    takes = [tk for bt in plan for tk in bt]
    for tk in takes:
        tk["text"] = " ".join(it["spk"] for it in tk["take"]); tk["flat"] = [w for it in tk["take"] for w in it["sub"].split()]
        tk["exp"] = " ".join(it["plain"] for it in tk["take"]); tk["best"] = None; tk["tries"] = 0
    # 2) sintetizar + verificar (rondas con otra semilla para las tomas que no pasan el control)
    thr = V.get("qa_thr", QA_THR); metric = V.get("qa_metric", "tokens"); W2 = {}
    def evaluate(tk, x):
        """→ (tiempos por palabra, coincidencia, texto reconocido, detalle). Métrica «fonetica»: ver voice_qa.py."""
        times, score, hyp = aligner.align(x, TSR, tk["flat"], tk["exp"])
        if metric != "fonetica": return times, score, hyp, dict(d=None, n=None, src="parakeet")
        import voice_qa
        sc, d, e, h = voice_qa.score(tk["exp"], hyp); src = "parakeet"; n = len(e)
        if sc < thr:  # segunda opinión: un error del reconocedor no debe contar como error de la voz
            if "w" not in W2: W2["w"] = voice_qa.Whisper()
            hw = W2["w"].transcribe(x, TSR); sc2, d2, _, _ = voice_qa.score(tk["exp"], hw)
            if sc2 > sc: sc, d, hyp, src = sc2, d2, hw, "whisper"
        return times, sc, hyp, dict(d=d, n=n, src=src)
    for tk in takes:
        if tk["voice"] == "humana":
            from scipy import signal as _sg
            ha, hsr = sf.read(tk["human"], dtype="float32")
            if ha.ndim > 1: ha = ha.mean(axis=1)
            if hsr != TSR: ha = _sg.resample_poly(ha, TSR, hsr).astype(np.float32)
            x = level(trim(ha)); times, score, hyp, det = evaluate(tk, x); tk["best"] = (score, x, times, hyp, det); tk["tries"] = 1
    synth = [tk for tk in takes if tk["voice"] != "humana"]
    if VOICE_ENGINE == "supertonic":
        narr = narr or Supertonic()
    for k in range(V.get("max_tries", MAX_TRIES)):
        pend = [tk for tk in synth if tk["best"] is None or tk["best"][0] < thr]
        if not pend: break
        if k: print(f"  ronda {k + 1}: repitiendo {len(pend)} tomas con otra semilla")
        if VOICE_ENGINE == "chatterbox":
            for tk in pend: tk["job"] = cb_job(tk["text"], tk["voice"], take_seed(tk["text"], tk["voice"]) + k, tk.get("exag"), tk.get("cfg"))
            cb_batch([tk["job"] for tk in pend])
        for tk in pend:
            x = load_take(tk["job"]["out"]) if VOICE_ENGINE == "chatterbox" else level(trim(narr.synth(tk["text"], tk["voice"], tk["speed"], take_seed(tk["text"], tk["voice"]) + k)))
            times, score, hyp, det = evaluate(tk, x); tk["tries"] = k + 1
            if tk["best"] is None or score > tk["best"][0]: tk["best"] = (score, x, times, hyp, det)
    # 3) montar la línea de tiempo
    t = V.get("lead_in", 0.25); beats = []; chunks = []; qa = []
    for bi, b in enumerate(V["beats"]):
        bstart = t + b.get("pre", 0.0); cur = bstart; sents = []; pmul = b.get("pause_mul", V.get("pause_mul", 1.0))
        for tk in plan[bi]:
            score, x, times, hyp, det = tk["best"]
            tt_ = V.get("trim_tail"); tthr = tt_ if isinstance(tt_, float) else 0.6
            if tt_ and times and len(x) / TSR - times[-1][1] > tthr:
                # la síntesis a veces añade balbuceo tras la última palabra: se corta poco después, con un fundido corto
                cut = int((times[-1][1] + min(0.25, tthr)) * TSR); x = x[:cut].copy(); fo = int(0.04 * TSR); x[-fo:] *= np.linspace(1, 0, fo)
            qa.append(dict(t=round(cur, 2), score=round(score, 4), tries=tk["tries"], guion=tk["exp"], reconocido=hyp, voz=tk["voice"], **det))
            chunks.append((cur, x)); i0 = 0
            for it in tk["take"]:
                ws = it["sub"].split(); wt = times[i0:i0 + len(ws)]; i0 += len(ws)
                sents.append(dict(text=it["sub"], start=round(cur + wt[0][0], 3), end=round(cur + wt[-1][1], 3), voice=tk["voice"],
                                  words=[[w, round(cur + ws_, 3), round(cur + we_, 3)] for w, (ws_, we_) in zip(ws, wt)]))
            cur += len(x) / TSR + pause_after(tk["take"][-1]["sub"]) * pmul
        if not sents: cur = bstart + b.get("dur", 2.0)
        bend = max(cur + b.get("hold", 0.0), bstart + b.get("min", 0.0))
        beats.append(dict(i=bi, start=round(bstart, 3), end=round(bend, 3), sents=sents, id=b.get("id", f"b{bi}")))
        t = bend
    total = t + V.get("tail", 0.4)
    # control de calidad de la voz: guion frente a lo que entiende el reconocedor
    import csv as _csv
    with open(f"{outdir}/recursos/control_de_voz.csv", "w", encoding="utf-8", newline="") as f:
        wr = _csv.writer(f, delimiter=";")
        wr.writerow(["inicio_s", "coincidencia", "tomas", "voz", "diferencias", "sonidos", "reconocedor", "guion", "reconocido"])
        for q in qa: wr.writerow([q["t"], q["score"], q["tries"], q["voz"], q.get("d"), q.get("n"), q.get("src"), q["guion"], q["reconocido"]])
    low = [q for q in qa if q["score"] < thr]
    print(f"  voz: {len(qa)} tomas · coincidencia media {np.mean([q['score'] for q in qa]):.4f} · mínima {min(q['score'] for q in qa):.4f} · repetidas {sum(q['tries'] > 1 for q in qa)} · bajo umbral {len(low)}")
    if metric == "fonetica":
        D = sum(q["d"] for q in qa); N = sum(q["n"] for q in qa)
        print(f"  coincidencia fonética global guion↔voz: {1 - D / N:.4%} ({D} diferencias en {N} sonidos)")
    for q in low: print(f"   [revisar {q['score']:.2f}] {q['guion']}\n        → {q['reconocido']}")
    # pista de narración (44,1 kHz mono, sin procesar)
    nar = np.zeros(int(total * TSR) + TSR, np.float32)
    for st, a in chunks:
        s = int(st * TSR); nar[s:s + len(a)] += a
    nar = nar[: int(total * TSR)]
    sf.write(f"{outdir}/{out_name(V, 'narr_wav')}", nar, TSR, subtype="PCM_16")
    # voz procesada 48 kHz
    vox = audio.voice_chain(nar, TSR); n = int(total * audio.SR); vox = np.pad(vox, ((0, max(0, n - len(vox))), (0, 0)))[:n]
    # música
    energy = []
    for b, bd in zip(V["beats"], beats):
        if "energy" in b: energy.append((bd["start"], b["energy"]))
    energy = energy or [(0, 2)]
    if V.get("music_fn"): mus = V["music_fn"](total, beats)
    else: mus = audio.compose(V["music"], total, energy=energy, seed=V.get("music_seed", 1), key_shift=V.get("key_shift", 0))
    mus = mus[:n] if len(mus) >= n else np.pad(mus, ((0, n - len(mus)), (0, 0)))
    duck = audio.duck_envelope(vox, depth=V.get("duck", 0.30))
    # silencios dramáticos de música
    gate = np.ones(n)
    for b, bd in zip(V["beats"], beats):
        if b.get("music_stop"):
            s = int(bd["start"] * audio.SR); e = int(min(bd["end"], bd["start"] + b["music_stop"]) * audio.SR)
            gate[s:e] = 0.08
    gate = np.convolve(gate, np.ones(4800) / 4800, "same")
    mus = mus * (duck * gate)[:, None] * V.get("music_gain", 0.55)
    # efectos
    fx = np.zeros((n, 2))
    for b, bd in zip(V["beats"], beats):
        for cue in b.get("sfx", []):
            off, name = cue[0], cue[1]; g = cue[2] if len(cue) > 2 else 0.6
            ref = bd["start"]
            if isinstance(off, str) and off.startswith("s"):  # 's2' = inicio de la frase 2 del beat
                idx = int(off[1:]); ref = bd["sents"][min(idx, len(bd["sents"]) - 1)]["start"] if bd["sents"] else bd["start"]; off = 0
            elif isinstance(off, str) and off == "end": ref = bd["end"]; off = -0.25
            elif isinstance(off, str) and off.startswith("w:"):
                frag = off[2:]; ref = None
                for st in bd["sents"]:
                    i = st["text"].find(frag)
                    if i >= 0: ref = word_at(st, i); break
                if ref is None: print(f"   [aviso] sfx: marca '{frag}' no encontrada"); continue
                off = 0
            y = audio.to_stereo(audio.sfx(name)) * g
            audio.place(fx, y, max(0, ref + off))
    mix = vox * V.get("voice_gain", 1.0) + mus + fx * V.get("sfx_gain", 0.8)
    mix = mix * np.minimum(1, np.minimum(np.arange(n) / (0.02 * audio.SR), 1))[:, None]
    mix, lufs = audio.master(mix, -14.0)
    gr = audio.master.last_gr; print(f"  mezcla: limitador máx. {gr['max_db']:.1f} dB · {gr['pct_over_1db']:.2f} % del tiempo por encima de 1 dB")
    sf.write(f"{outdir}/recursos/mezcla_final.wav", mix.astype(np.float32), audio.SR, subtype="PCM_16")
    sf.write(f"{outdir}/recursos/musica_original.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.8).astype(np.float32), audio.SR, subtype="PCM_16")
    # mp3 de la narración procesada
    sf.write(f"{outdir}/recursos/_vox.wav", (vox / (np.abs(vox).max() + 1e-9) * 0.9).astype(np.float32), audio.SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{outdir}/recursos/_vox.wav", "-c:a", "libmp3lame", "-b:a", "160k", f"{outdir}/{out_name(V, 'narr_mp3')}"], check=True)
    os.remove(f"{outdir}/recursos/_vox.wav")
    tl = dict(total=round(total, 3), beats=beats, lufs_in=round(lufs, 2))
    json.dump(tl, open(f"{outdir}/recursos/timeline.json", "w"), ensure_ascii=False, indent=1)
    write_srt(tl, f"{outdir}/{out_name(V, 'srt')}", V)
    write_script(V, tl, f"{outdir}/{out_name(V, 'script')}")
    return tl

# ---------------------------------------------------------------- SRT y guion
def fmt_ts(t, comma=True):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d}{',' if comma else '.'}{int(round((s - int(s)) * 1000)) % 1000:03d}"

def srt_chunks(text, maxc=42, maxl=2):
    words = text.split(); lines = []; cur = ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return [lines[i:i + maxl] for i in range(0, len(lines), maxl)]

def write_srt(tl, path, V):
    caps = []
    for b in tl["beats"]:
        for s in b["sents"]:
            groups = srt_chunks(s["text"]); ws = s.get("words"); i0 = 0
            total_chars = sum(len(" ".join(g)) for g in groups); t0 = s["start"]
            for g in groups:
                nw = sum(len(line.split()) for line in g)
                if ws and i0 + nw <= len(ws):
                    st, en = ws[i0][1], ws[i0 + nw - 1][2]; i0 += nw
                else:
                    dur = (s["end"] - s["start"]) * len(" ".join(g)) / max(1, total_chars); st, en = t0, t0 + dur; t0 += dur
                caps.append([st, en, "\n".join(g)])
    # legibilidad: cada subtítulo dura al menos ~1 s y se mantiene hasta el siguiente si la pausa es corta
    for i, c in enumerate(caps):
        nxt = caps[i + 1][0] if i + 1 < len(caps) else c[1] + 1.0
        c[1] = min(max(c[1] + 0.25, c[0] + 1.0), nxt - 0.04) if nxt - c[0] > 0.3 else c[1]
        if nxt - c[1] < 0.5: c[1] = nxt - 0.04
    out = [f"{i + 1}\n{fmt_ts(c[0])} --> {fmt_ts(c[1])}\n{c[2]}\n" for i, c in enumerate(caps)]
    open(path, "w", encoding="utf-8").write("\n".join(out))

def write_script(V, tl, path):
    L = [f"GUION — {V['title']}", f"Formato: {V['format']} · Duración: {fmt_ts(tl['total'], False)[:-4]} · Voz: narradora (Chatterbox Multilingual), español", "=" * 78, ""]
    names = {"host": "NARRADORA", "copiloto": "COPILOTO", "humana": "VOZ HUMANA"}
    for b, bd in zip(V["beats"], tl["beats"]):
        if b.get("section"): L += ["", f"## {b['section']}", ""]
        if b.get("note"): L.append(f"   [VISUAL] {b['note']}")
        for s in bd["sents"]:
            L.append(f"[{fmt_ts(s['start'], False)[3:-1]}] {names.get(s['voice'], s['voice'])}: {s['text']}")
        if not bd["sents"]: L.append(f"[{fmt_ts(bd['start'], False)[3:-1]}] (sin narración · {round(bd['end'] - bd['start'], 1)} s)")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")

# ---------------------------------------------------------------- etapa de vídeo
class Ctx:
    def __init__(self, V, tl, W, H):
        self.V, self.tl, self.W, self.H = V, tl, W, H
        self.total = tl["total"]

def group_scenes(V, tl):
    groups = []
    for b, bd in zip(V["beats"], tl["beats"]):
        if b.get("scene") is None and groups:
            groups[-1]["end"] = bd["end"]; groups[-1]["beats"].append(bd)
        else:
            groups.append(dict(fn=b.get("scene"), start=bd["start"], end=bd["end"], beats=[bd], trans=b.get("trans", V.get("trans", ("fade", 0.4)))))
    groups[-1]["end"] = tl["total"]
    return groups

class SceneInfo:
    """Información de tiempos que recibe cada escena (tiempos relativos al inicio de la escena)."""
    def __init__(self, g):
        self.start = g["start"]; self.d = g["end"] - g["start"]
        self.sents = [dict(s, start=s["start"] - g["start"], end=s["end"] - g["start"]) for b in g["beats"] for s in b["sents"]]
        self.beats = [(b["start"] - g["start"], b["end"] - g["start"]) for b in g["beats"]]
    def s(self, i):  # inicio de la frase i (relativo)
        return self.sents[min(i, len(self.sents) - 1)]["start"] if self.sents else 0
    def b(self, i): return self.beats[min(i, len(self.beats) - 1)][0]
    def w(self, frag, n=0, default=None):
        """Momento estimado (relativo) en que el narrador dice `frag` (n-ésima aparición)."""
        k = 0
        for s in self.sents:
            i = s["text"].find(frag)
            while i >= 0:
                if k == n:
                    if s.get("words"): return word_at(s, i) - self.start
                    return s["start"] + (s["end"] - s["start"]) * i / max(1, len(s["text"]))
                k += 1; i = s["text"].find(frag, i + 1)
        if default is None: print(f"   [aviso] marca '{frag}' no encontrada en la escena")
        return 999.0 if default is None else default

def blend_transition(c, imgA, imgB, kind, p, W, H):
    e = gfx.ease_io(p); full = skia.Rect.MakeWH(W, H); so = skia.SamplingOptions(skia.FilterMode.kLinear)
    if kind == "fade" or kind == "cut":
        c.drawImage(imgA, 0, 0); pp = skia.Paint(); pp.setAlphaf(e if kind == "fade" else (1 if p > 0.5 else 0)); c.drawImage(imgB, 0, 0, so, pp)
    elif kind in ("whip", "whip_left"):
        sgn = 1 if kind == "whip" else -1
        c.save(); c.translate(-sgn * W * e, 0); c.drawImage(imgA, 0, 0); c.restore()
        c.save(); c.translate(sgn * W * (1 - e), 0); c.drawImage(imgB, 0, 0); c.restore()
        if 0.15 < p < 0.85:  # desenfoque de movimiento simulado
            pp = skia.Paint(); pp.setImageFilter(skia.ImageFilters.Blur(28 * math.sin(p * math.pi), 0)); pp.setAlphaf(0.6)
            c.saveLayer(full, pp); c.restore()
    elif kind == "wipe":
        c.drawImage(imgA, 0, 0); c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, W * e, H)); c.drawImage(imgB, 0, 0); c.restore()
        gfx.rect(c, W * e - 6, 0, 12, H, "#ffffff", 0.9 * math.sin(p * math.pi))
    elif kind == "vwipe":
        c.drawImage(imgA, 0, 0); c.save(); c.clipRect(skia.Rect.MakeXYWH(0, H * (1 - e), W, H * e)); c.drawImage(imgB, 0, 0); c.restore()
    elif kind == "iris":
        c.drawImage(imgA, 0, 0); c.save(); pth = skia.Path(); pth.addCircle(W / 2, H / 2, math.hypot(W, H) / 2 * e); c.clipPath(pth, doAntiAlias=True); c.drawImage(imgB, 0, 0); c.restore()
    elif kind == "zoom":
        c.save(); s = 1 + 0.25 * e; c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
        pa = skia.Paint(); pa.setAlphaf(1 - e); c.drawImage(imgA, 0, 0, so, pa); c.restore()
        c.save(); s = 0.85 + 0.15 * e; c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
        pb = skia.Paint(); pb.setAlphaf(e); c.drawImage(imgB, 0, 0, so, pb); c.restore()
    elif kind == "glitch":
        src = imgA if p < 0.5 else imgB; c.drawImage(src, 0, 0)
        rng = np.random.default_rng(int(p * 997))
        for _ in range(9):
            y = rng.integers(0, H); h = rng.integers(8, 90); dx = rng.integers(-120, 120) * math.sin(p * math.pi)
            c.save(); c.clipRect(skia.Rect.MakeXYWH(0, y, W, h)); c.drawImage(imgB if rng.random() < p else imgA, dx, 0); c.restore()
        gfx.rect(c, 0, 0, W, H, "#ff2bd6", 0.10 * math.sin(p * math.pi))
    elif kind == "flash":
        c.drawImage(imgA if p < 0.5 else imgB, 0, 0); gfx.rect(c, 0, 0, W, H, "#ffffff", math.sin(p * math.pi) ** 2 * 0.9)
    elif kind == "paint":  # rodillo de pintura: borde ondulado que avanza
        c.drawImage(imgA, 0, 0); xe = W * 1.2 * e - W * 0.1
        pth = skia.Path(); pth.moveTo(-10, -10)
        for k in range(41):
            yy = H * k / 40; xx = xe + 26 * math.sin(k * 1.3 + p * 7) + 12 * math.sin(k * 3.1 + 1)
            pth.lineTo(xx, yy) if k else pth.lineTo(xx, -10)
        pth.lineTo(-10, H + 10); pth.close()
        c.save(); c.clipPath(pth, doAntiAlias=True); c.drawImage(imgB, 0, 0); c.restore()
        edge = skia.Path()
        for k in range(41):
            yy = H * k / 40; xx = xe + 26 * math.sin(k * 1.3 + p * 7) + 12 * math.sin(k * 3.1 + 1)
            edge.lineTo(xx, yy) if k else edge.moveTo(xx, yy)
        c.drawPath(edge, gfx.paint("#ffffff", 0.35 * math.sin(p * math.pi), stroke=8))
    elif kind == "slide_up":
        c.save(); c.translate(0, -H * e); c.drawImage(imgA, 0, 0); c.restore(); c.save(); c.translate(0, H * (1 - e)); c.drawImage(imgB, 0, 0); c.restore()
    else:
        c.drawImage(imgB, 0, 0)

def render_video(V, tl, outdir, master=False, preview=None, frames_dir=None, segment=None):
    """segment=(k, n): renderiza solo la parte k de n (sin audio) para montarla después en paralelo."""
    W, H = V.get("size", (1920, 1080)); ctx = Ctx(V, tl, W, H)
    groups = group_scenes(V, tl); infos = [SceneInfo(g) for g in groups]
    total = tl["total"]; nfr = int(math.ceil(total * FPS))
    f0, f1 = 0, nfr
    if preview: a, b = preview; f0, f1 = int(a * FPS), min(nfr, int(b * FPS))
    if segment: k, n = segment; f0, f1 = nfr * k // n, nfr * (k + 1) // n
    mp4 = f"{outdir}/{V['file']}.mp4" if not preview else f"{outdir}/recursos/preview_{int(f0 / FPS)}.mp4"
    if segment: mp4 = f"{outdir}/recursos/_seg_{segment[0]:02d}.h264"   # H.264 en bruto: se une con cat sin perder fotogramas
    dur = (f1 - f0) / FPS
    if master: vargs = ["-crf", "17", "-maxrate", "12M", "-bufsize", "24M"]
    elif segment: vargs = ["-crf", "17" if V.get("final_codec") else "15"]   # intermedio de alta calidad; la compresión final va aparte
    else:
        cap = int(min(8000, 92 * 8 * 1000 / max(1, total) - 192)); vargs = ["-crf", "19", "-maxrate", f"{cap}k", "-bufsize", f"{cap * 2}k"]
    aud_in = [] if segment else ["-ss", f"{f0 / FPS:.3f}", "-t", f"{dur:.3f}", "-i", f"{outdir}/recursos/mezcla_final.wav"]
    aud_out = [] if segment else ["-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *aud_in,
           "-map", "0:v", *aud_out, "-c:v", "libx264", "-preset", "medium", "-tune", "animation", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-g", "60", *vargs, *(["-f", "h264"] if segment else ["-movflags", "+faststart"]),
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", mp4]
    if segment: cmd[cmd.index("-preset") + 1] = "veryfast"
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = gfx.new_surface(W, H); sA = gfx.new_surface(W, H); sB = gfx.new_surface(W, H)
    buf = np.zeros((H, W, 4), np.uint8)
    overlay = V.get("overlay"); grade = V.get("grade")
    t_start = time.time(); gi = 0
    for fi in range(f0, f1):
        gt = fi / FPS
        while gi < len(groups) - 1 and gt >= groups[gi + 1]["start"]: gi += 1
        g = groups[gi]; info = infos[gi]; c = surf.getCanvas()
        # ¿estamos dentro de una transición hacia la escena gi o hacia la siguiente?
        kind, td = g["trans"]; nxt = groups[gi + 1] if gi + 1 < len(groups) else None
        in_tr = None
        if gi > 0 and kind != "cut" and gt < g["start"] + td / 2: in_tr = (gi - 1, gi, (gt - (g["start"] - td / 2)) / td)
        elif nxt and nxt["trans"][0] != "cut" and gt >= nxt["start"] - nxt["trans"][1] / 2: in_tr = (gi, gi + 1, (gt - (nxt["start"] - nxt["trans"][1] / 2)) / nxt["trans"][1])
        if in_tr:
            ia, ib, p = in_tr; ga, gb = groups[ia], groups[ib]
            ca = sA.getCanvas(); ca.clear(skia.ColorBLACK); ga["fn"](ca, min(gt - ga["start"], ga["end"] - ga["start"] + 0.5), infos[ia], ctx)
            cb = sB.getCanvas(); cb.clear(skia.ColorBLACK); gb["fn"](cb, max(0.0, gt - gb["start"]), infos[ib], ctx)
            c.clear(skia.ColorBLACK); blend_transition(c, sA.makeImageSnapshot(), sB.makeImageSnapshot(), (gb["trans"][0]), gfx.clamp(p), W, H)
        else:
            c.clear(skia.ColorBLACK); g["fn"](c, gt - g["start"], info, ctx)
        if overlay: overlay(c, gt, ctx)
        if grade: grade(c, gt, ctx)
        surf.readPixels(skia.ImageInfo.Make(W, H, skia.ColorType.kRGBA_8888_ColorType, skia.AlphaType.kPremul_AlphaType), buf, W * 4, 0, 0)
        proc.stdin.write(buf.tobytes())
        if frames_dir and fi % int(FPS * 5) == 0:
            surf.makeImageSnapshot().save(f"{frames_dir}/f_{fi // FPS:05d}.png", skia.kPNG)
        if fi % 300 == 0:
            el = time.time() - t_start; rate = (fi - f0 + 1) / max(el, 1e-6)
            print(f"  {V['id']} frame {fi}/{f1} ({rate:.1f} fps, ETA {(f1 - fi) / max(rate, 1e-6) / 60:.1f} min)", flush=True)
    proc.stdin.close(); proc.wait()
    return mp4

def render_parallel(V, tl, outdir, vid, jobs, master=False):
    """Renderiza en `jobs` procesos (cada uno una parte del vídeo) y une las partes con el audio final."""
    procs = []
    for k in range(jobs):
        cmd = [sys.executable, os.path.abspath(__file__), vid, "--stage", "video", "--segment", str(k), str(jobs)] + (["--master"] if master else [])
        procs.append(subprocess.Popen(cmd))
    codes = [p.wait() for p in procs]
    if any(codes): raise RuntimeError(f"falló algún segmento: {codes}")
    # unir los segmentos H.264 en bruto (cat) conserva todos los fotogramas; el contenedor se genera al final
    allv = f"{outdir}/recursos/_video.h264"
    with open(allv, "wb") as fo:
        for k in range(jobs):
            with open(f"{outdir}/recursos/_seg_{k:02d}.h264", "rb") as fi: shutil.copyfileobj(fi, fo, 1 << 24)
            os.remove(f"{outdir}/recursos/_seg_{k:02d}.h264")
    mp4 = f"{outdir}/{V['file']}.mp4"; wav = f"{outdir}/recursos/mezcla_final.wav"
    if V.get("final_codec") == "av1":
        # tamaño objetivo (GitHub admite archivos de hasta 100 MB): AV1 de 10 bits conserva mucho más detalle que H.264 a la misma tasa
        abr = 128; kbps = int(V.get("target_mb", 94) * 8 * 1024 / tl["total"] - abr)
        venc = ["-c:v", "libsvtav1", "-preset", str(V.get("av1_preset", 6)), "-b:v", f"{kbps}k", "-g", "240", "-pix_fmt", "yuv420p10le",
                "-svtav1-params", "tune=0:enable-overlays=1:scd=1"]
    else:
        # Antes se copiaba el H.264 en bruto al MP4 («-c:v copy»): el contenedor quedaba sin el orden de presentación de los
        # fotogramas B (marcas de tiempo de decodificación = de presentación) y los móviles y navegadores mostraban las
        # imágenes desordenadas (avanzan y retroceden). Ahora se vuelve a codificar desde un intermedio de alta calidad.
        abr = 192; cap = int(min(8000, 92 * 8 * 1000 / max(1, tl["total"]) - abr))
        venc = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", f"{cap}k", "-bufsize", f"{cap * 2}k",
                "-profile:v", "high", "-pix_fmt", "yuv420p", "-g", "60", "-video_track_timescale", "15360"]
    # marcas de tiempo nuevas y correlativas, en el orden en que el decodificador entrega las imágenes (orden de presentación)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", allv, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-vf", f"setpts=N/({FPS}*TB)", "-fps_mode", "passthrough", *venc,
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-c:a", "aac", "-b:a", f"{abr}k", "-ar", "48000", "-shortest", "-movflags", "+faststart", mp4], check=True)
    if V.get("keep_master"): os.replace(allv, f"{outdir}/recursos/master_h264_crf17.h264")
    else: os.remove(allv)
    return mp4

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vid"); ap.add_argument("--stage", default="all")
    ap.add_argument("--master", action="store_true"); ap.add_argument("--preview", type=float, nargs=2)
    ap.add_argument("--jobs", type=int, default=1); ap.add_argument("--segment", type=int, nargs=2)
    a = ap.parse_args()
    mod = importlib.import_module(f"videos.{a.vid}"); V = mod.VIDEO
    outdir = os.environ.get("BUILD_OUT") or os.path.join(ROOT, V["folder"]); os.makedirs(f"{outdir}/recursos", exist_ok=True)   # BUILD_OUT: pruebas sin tocar la entrega
    t0 = time.time()
    if a.stage in ("all", "audio"):
        tl = build_audio(V, outdir); print(f"{V['id']}: audio listo, {tl['total']:.1f} s ({time.time() - t0:.0f} s)")
    tl = json.load(open(f"{outdir}/recursos/timeline.json"))
    if a.stage in ("all", "thumb") and hasattr(mod, "thumbnail"):
        tw, th = V.get("thumb_size", (1280, 720)); s = gfx.new_surface(tw, th); mod.thumbnail(s.getCanvas())
        mk = getattr(mod, "THUMB_MARK", (1215, 655, 34))
        if mk:
            import components; components.thumb_mark(s.getCanvas(), *mk)
        s.makeImageSnapshot().save(f"{outdir}/{out_name(V, 'thumb')}", skia.kPNG); print("miniatura lista")
    if a.stage in ("all", "video"):
        fd = f"{outdir}/recursos/fotogramas"; os.makedirs(fd, exist_ok=True)
        if a.segment:
            render_video(V, tl, outdir, a.master, None, fd, segment=tuple(a.segment)); return
        if a.jobs > 1 and not a.preview: out = render_parallel(V, tl, outdir, a.vid, a.jobs, a.master)
        else: out = render_video(V, tl, outdir, a.master, a.preview, None if a.preview else fd)
        print(f"{V['id']}: vídeo listo {out} ({(time.time() - t0) / 60:.1f} min)")

if __name__ == "__main__":
    main()
