"""Pipeline de producción: guion → voz → tiempos → música/SFX → animación → MP4 + SRT.

Uso:  python build.py v01 [--stage all|audio|video|thumb] [--master] [--preview SEG]
"""
import argparse, importlib, json, math, os, re, subprocess, sys, time
import numpy as np, soundfile as sf, skia
sys.path.insert(0, os.path.dirname(__file__))
import audio, gfx
from tts import Kokoro, split_markup, spoken, pause_after, SR as TSR

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FPS = 30

# ---------------------------------------------------------------- texto → frases (respetando {sub|habla})
def split_sentences(text):
    prot = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(".", "\x00").replace("?", "\x01").replace("!", "\x02").replace(":", "\x03"), text.strip())
    parts = re.split(r"(?<=[\.\?\!…:])\s+(?=[¿¡A-ZÁÉÍÓÚÑ0-9\"«({])", prot)
    return [p.replace("\x00", ".").replace("\x01", "?").replace("\x02", "!").replace("\x03", ":").strip() for p in parts if p.strip()]

# ---------------------------------------------------------------- etapa de audio
def build_audio(V, outdir, k=None):
    k = k or Kokoro()
    t = V.get("lead_in", 0.25); beats = []; chunks = []
    for bi, b in enumerate(V["beats"]):
        bstart = t + b.get("pre", 0.0); cur = bstart; sents = []
        vo = b.get("vo", "")
        human = f"{outdir}/voz_humana/beat_{bi:02d}.wav"
        if vo and os.path.exists(human):
            # Locución humana: un archivo por bloque; los tiempos de frase se reparten por nº de caracteres
            from scipy import signal as _sg
            from tts import trim as _trim
            ha, hsr = sf.read(human, dtype="float32")
            if ha.ndim > 1: ha = ha.mean(axis=1)
            if hsr != TSR: ha = _sg.resample_poly(ha, TSR, hsr).astype(np.float32)
            ha = _trim(ha); chunks.append((cur, ha)); subs = [split_markup(x)[0] for x in split_sentences(vo)]
            tot = sum(len(x) for x in subs); dur = len(ha) / TSR; acc = 0
            for x in subs:
                st = cur + dur * acc / tot; acc += len(x)
                sents.append(dict(text=x, start=round(st, 3), end=round(cur + dur * acc / tot, 3), voice="humana"))
            cur += dur + 0.3
        for s in (split_sentences(vo) if vo and not os.path.exists(human) else []):
            sub, spk = split_markup(s)
            a = k.synth(spoken(spk), b.get("voice", V.get("voice", "host")), b.get("speed", V.get("speed", 1.0)))
            chunks.append((cur, a))
            sents.append(dict(text=sub, start=round(cur, 3), end=round(cur + len(a) / TSR, 3), voice=b.get("voice", V.get("voice", "host"))))
            cur += len(a) / TSR + pause_after(sub) * b.get("pause_mul", V.get("pause_mul", 1.0))
        if not sents: cur = bstart + b.get("dur", 2.0)
        bend = max(cur + b.get("hold", 0.0), bstart + b.get("min", 0.0))
        beats.append(dict(i=bi, start=round(bstart, 3), end=round(bend, 3), sents=sents, id=b.get("id", f"b{bi}")))
        t = bend
    total = t + V.get("tail", 0.4)
    # pista de narración (24 kHz mono, sin procesar)
    nar = np.zeros(int(total * TSR) + TSR, np.float32)
    for st, a in chunks:
        s = int(st * TSR); nar[s:s + len(a)] += a
    nar = nar[: int(total * TSR)]
    sf.write(f"{outdir}/narracion.wav", nar, TSR, subtype="PCM_16")
    # voz procesada 48 kHz
    vox = audio.voice_chain(nar, TSR); n = int(total * audio.SR); vox = np.pad(vox, ((0, max(0, n - len(vox))), (0, 0)))[:n]
    # música
    energy = []
    for b, bd in zip(V["beats"], beats):
        if "energy" in b: energy.append((bd["start"], b["energy"]))
    energy = energy or [(0, 2)]
    mus = audio.compose(V["music"], total, energy=energy, seed=V.get("music_seed", 1), key_shift=V.get("key_shift", 0))
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
                    if i >= 0: ref = st["start"] + (st["end"] - st["start"]) * i / max(1, len(st["text"])); break
                if ref is None: print(f"   [aviso] sfx: marca '{frag}' no encontrada"); continue
                off = 0
            y = audio.to_stereo(audio.sfx(name)) * g
            audio.place(fx, y, max(0, ref + off))
    mix = vox * V.get("voice_gain", 1.0) + mus + fx * V.get("sfx_gain", 0.8)
    mix = mix * np.minimum(1, np.minimum(np.arange(n) / (0.02 * audio.SR), 1))[:, None]
    mix, lufs = audio.master(mix, -14.0)
    sf.write(f"{outdir}/recursos/mezcla_final.wav", mix.astype(np.float32), audio.SR, subtype="PCM_16")
    sf.write(f"{outdir}/recursos/musica_original.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.8).astype(np.float32), audio.SR, subtype="PCM_16")
    # mp3 de la narración procesada
    sf.write(f"{outdir}/recursos/_vox.wav", (vox / (np.abs(vox).max() + 1e-9) * 0.9).astype(np.float32), audio.SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{outdir}/recursos/_vox.wav", "-c:a", "libmp3lame", "-b:a", "160k", f"{outdir}/narracion.mp3"], check=True)
    os.remove(f"{outdir}/recursos/_vox.wav")
    tl = dict(total=round(total, 3), beats=beats, lufs_in=round(lufs, 2))
    json.dump(tl, open(f"{outdir}/recursos/timeline.json", "w"), ensure_ascii=False, indent=1)
    write_srt(tl, f"{outdir}/subtitulos.srt", V)
    write_script(V, tl, f"{outdir}/guion.txt")
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
    out = []; n = 1
    for b in tl["beats"]:
        for s in b["sents"]:
            groups = srt_chunks(s["text"]); total_chars = sum(len(" ".join(g)) for g in groups); t0 = s["start"]
            for g in groups:
                dur = (s["end"] - s["start"]) * len(" ".join(g)) / max(1, total_chars)
                out.append(f"{n}\n{fmt_ts(t0)} --> {fmt_ts(t0 + dur)}\n" + "\n".join(g) + "\n"); n += 1; t0 += dur
    open(path, "w", encoding="utf-8").write("\n".join(out))

def write_script(V, tl, path):
    L = [f"GUION — {V['title']}", f"Formato: {V['format']} · Duración: {fmt_ts(tl['total'], False)[:-4]} · Voz: Kokoro (Apache-2.0), español latinoamericano", "=" * 78, ""]
    names = {"host": "NARRADOR", "analista": "ANALISTA"}
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
    elif kind == "slide_up":
        c.save(); c.translate(0, -H * e); c.drawImage(imgA, 0, 0); c.restore(); c.save(); c.translate(0, H * (1 - e)); c.drawImage(imgB, 0, 0); c.restore()
    else:
        c.drawImage(imgB, 0, 0)

def render_video(V, tl, outdir, master=False, preview=None, frames_dir=None):
    W, H = V.get("size", (1920, 1080)); ctx = Ctx(V, tl, W, H)
    groups = group_scenes(V, tl); infos = [SceneInfo(g) for g in groups]
    total = tl["total"]; nfr = int(math.ceil(total * FPS))
    f0, f1 = 0, nfr
    if preview: a, b = preview; f0, f1 = int(a * FPS), min(nfr, int(b * FPS))
    mp4 = f"{outdir}/{V['file']}.mp4" if not preview else f"{outdir}/recursos/preview_{int(f0 / FPS)}.mp4"
    dur = (f1 - f0) / FPS
    if master: vargs = ["-crf", "17", "-maxrate", "12M", "-bufsize", "24M"]
    else:
        cap = int(min(8000, 92 * 8 * 1000 / max(1, total) - 192)); vargs = ["-crf", "19", "-maxrate", f"{cap}k", "-bufsize", f"{cap * 2}k"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-ss", f"{f0 / FPS:.3f}", "-t", f"{dur:.3f}", "-i", f"{outdir}/recursos/mezcla_final.wav",
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-tune", "animation", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-g", "60", *vargs, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", mp4]
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

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vid"); ap.add_argument("--stage", default="all")
    ap.add_argument("--master", action="store_true"); ap.add_argument("--preview", type=float, nargs=2)
    a = ap.parse_args()
    mod = importlib.import_module(f"videos.{a.vid}"); V = mod.VIDEO
    outdir = os.path.join(ROOT, V["folder"]); os.makedirs(f"{outdir}/recursos", exist_ok=True)
    t0 = time.time()
    if a.stage in ("all", "audio"):
        tl = build_audio(V, outdir); print(f"{V['id']}: audio listo, {tl['total']:.1f} s ({time.time() - t0:.0f} s)")
    tl = json.load(open(f"{outdir}/recursos/timeline.json"))
    if a.stage in ("all", "thumb") and hasattr(mod, "thumbnail"):
        s = gfx.new_surface(1280, 720); mod.thumbnail(s.getCanvas())
        mk = getattr(mod, "THUMB_MARK", (1215, 655, 34))
        if mk:
            import components; components.thumb_mark(s.getCanvas(), *mk)
        s.makeImageSnapshot().save(f"{outdir}/miniatura.png", skia.kPNG); print("miniatura lista")
    if a.stage in ("all", "video"):
        fd = f"{outdir}/recursos/fotogramas"; os.makedirs(fd, exist_ok=True)
        out = render_video(V, tl, outdir, a.master, a.preview, None if a.preview else fd)
        print(f"{V['id']}: vídeo listo {out} ({(time.time() - t0) / 60:.1f} min)")

if __name__ == "__main__":
    main()
