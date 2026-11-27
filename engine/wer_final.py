"""Verificación final guion ↔ narración sobre el audio DEFINITIVO (no sobre las tomas sueltas).

Uso: python wer_final.py gx      (o el id del Short)

1. Frase a frase: se recorta cada frase de la narración final (con 0,2 s antes y 0,35 s después, sin invadir la
   frase vecina) y se transcribe con DOS reconocedores independientes (Parakeet TDT v3 y Whisper small).
2. WER = (sustituciones + omisiones + inserciones) / palabras del guion, con la normalización de voice_qa.wer
   (minúsculas, sin puntuación ni tildes, cifras en palabras, grafías alternativas de nombres propios, homófonos del
   seseo y fusión de palabras en el habla encadenada). Una palabra cuenta como error solo si la fallan los DOS
   reconocedores (voice_qa.wer_combined); también se dan los totales de cada reconocedor por separado.
   Frases de 3 palabras o menos que fallan solas: se repiten con la frase anterior delante (un recorte de 1-2 s sin
   contexto confunde a los dos reconocedores) y cuentan solo los errores que añade esa frase.
3. Comprobación en bloques de ~20 s (varias frases seguidas): detecta problemas en las uniones entre tomas.
4. Términos clave (nombres propios, cifras, términos de GTA): uno a uno, ¿lo reconoce al menos un reconocedor?
5. Uniones: ninguna toma se solapa con la siguiente; ninguna termina de golpe con voz (energía en los últimos 30 ms).
6. Música y efectos frente a voz (pistas separadas): relación en dB mientras hay voz.
Resultado: PROYECTO_DE_EDICION/CONTROL_VOZ_WER.md y control_voz_wer.csv
"""
import re, csv, importlib, json, os, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import Aligner, canon
import voice_qa as Q
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEY = {"gta", "vice", "city", "jason", "lucia", "rockstar", "focus", "psicopata", "irredimible", "profesional", "curtido", "violento",
       "estrellas", "estrella", "policia", "perfil", "criminal", "uno", "dos", "tres", "cuatro", "cinco", "seis", "diez", "trescientos",
       "veintiuno", "cuatrocientos", "sesenta", "noventa", "ocho", "helicoptero", "avion", "tanque", "tanques", "aeropuerto", "militar"}

def main(vid):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos"))
    V = importlib.import_module(f"videos.{vid}").VIDEO
    # BUILD_OUT: comprobar un audio reconstruido aparte antes de instalarlo en la carpeta de entrega
    out = os.environ.get("BUILD_OUT") or os.path.join(ROOT, V["folder"]); res = os.path.join(out, V.get("res_dir", "recursos"))
    tl = json.load(open(os.path.join(res, "timeline.json")))
    narr = os.path.join(out, V.get("names", {}).get("narr_wav", "narracion.wav"))
    x, sr = sf.read(narr, dtype="float32")
    if x.ndim > 1: x = x.mean(axis=1)
    A = Aligner(); Wh = Q.Whisper()
    sents = [s for b in tl["beats"] for s in b["sents"]]
    only = os.environ.get("WER_ONLY")   # comprobación parcial: solo las frases que coinciden con esta expresión (p. ej. tras cambiar unas pocas)
    if only:
        n = e = 0
        for i, s in enumerate(sents):
            if not re.search(only, s["text"]): continue
            a = s["start"] - 0.15; b = s["end"] + 0.25
            if i > 0: a = max(a, sents[i - 1]["end"] + 0.02)
            if i + 1 < len(sents): b = min(b, sents[i + 1]["start"] - 0.12)
            seg = x[max(0, int(a * sr)): int(b * sr)]
            hp, _ = A.transcribe(seg, sr); hw = Wh.transcribe(seg, sr); best = Q.wer_combined(s["text"], hp, hw)
            n += best["n"] if "n" in best else len(s["text"].split()); e += best["err"]
            print(f"  {s['start']:7.2f} s · errores {best['err']} · «{s['text']}»\n     P: {hp}\n     W: {hw}", flush=True)
        print(f"  parcial: {e} errores en {n} palabras"); return
    rows = []; tot = dict(n=0, comb=0, par=0, whi=0); key_miss = []
    for i, s in enumerate(sents):
        a = s["start"] - 0.15; b = s["end"] + 0.25
        if i > 0: a = max(a, sents[i - 1]["end"] + 0.02)
        if i + 1 < len(sents): b = min(b, sents[i + 1]["start"] - 0.12)   # sin el comienzo de la frase siguiente
        seg = x[max(0, int(a * sr)): int(b * sr)]
        hp, _ = A.transcribe(seg, sr); hw = Wh.transcribe(seg, sr)
        rp = Q.wer(s["text"], hp); rw = Q.wer(s["text"], hw)
        best = Q.wer_combined(s["text"], hp, hw)   # error solo si fallan los dos reconocedores
        if best["err"] and i > 0 and len(s["text"].split()) <= 3 and rows:
            # frase muy corta («Se acabó.»): los reconocedores fallan con un recorte de 1-2 s sin contexto; se repite con la
            # frase anterior delante y se cuentan solo los errores que añade esta frase
            pv = sents[i - 1]; a2 = max(0, pv["start"] - 0.15)
            seg2 = x[int(a2 * sr): int(b * sr)]; hp2, _ = A.transcribe(seg2, sr); hw2 = Wh.transcribe(seg2, sr)
            b2 = Q.wer_combined(pv["text"] + " " + s["text"], hp2, hw2)
            if max(0, b2["err"] - rows[-1]["err"]) < best["err"]:
                best = dict(b2, err=max(0, b2["err"] - rows[-1]["err"])); hp = f"{hp} (con la frase anterior: {hp2})"; hw = f"{hw} (con la frase anterior: {hw2})"
        tot["n"] += rp["n"]; tot["comb"] += best["err"]; tot["par"] += rp["err"]; tot["whi"] += rw["err"]
        E = Q.wer_tokens(s["text"]); Hp = set(Q.wer_tokens(hp, True)); Hw = set(Q.wer_tokens(hw, True))
        # un término unido a la palabra vecina en la transcripción («en curtido» → «encurtido») está reconocido: la unión no se oye
        unidos = {t for r_ in (best, rp, rw) for e_, h_ in r_["uniones"] for t in e_.split()}
        for w in E:
            if w in KEY and w not in Hp and w not in Hw and w not in unidos: key_miss.append((round(s["start"], 2), w, s["text"]))
        rows.append(dict(i=i + 1, t=round(s["start"], 2), guion=s["text"], parakeet=hp, whisper=hw, err_parakeet=rp["err"], err_whisper=rw["err"],
                         err=best["err"], palabras=rp["n"], detalle=" | ".join(f"{k}: «{e}» → «{h}»" for k, e, h in best["diff"]),
                         homofonos=" | ".join(f"«{e}» = «{h}»" for e, h in best["homof"]), uniones=" | ".join(f"«{e}» = «{h}»" for e, h in best["uniones"])))
        print(f"  [{i + 1}/{len(sents)}] {s['start']:7.2f} s · errores {best['err']} (P {rp['err']} · W {rw['err']})", flush=True)
    # bloques de ~20 s
    blocks = []; cur = []
    for s in sents:
        if cur and s["end"] - cur[0]["start"] > 20: blocks.append(cur); cur = []
        cur.append(s)
    if cur: blocks.append(cur)
    brows = []; bt = dict(n=0, err=0)
    for bl in blocks:
        a = max(0, bl[0]["start"] - 0.2); b = bl[-1]["end"] + 0.35
        seg = x[int(a * sr): int(b * sr)]; exp = " ".join(s["text"] for s in bl)
        hp, _ = A.transcribe(seg, sr); hw = Wh.transcribe(seg, sr)
        rp = Q.wer(exp, hp); rw = Q.wer(exp, hw); best = Q.wer_combined(exp, hp, hw)
        bt["n"] += rp["n"]; bt["err"] += best["err"]
        brows.append((round(a, 2), round(b, 2), rp["n"], rp["err"], rw["err"], best["err"], " | ".join(f"{k}: «{e}» → «{h}»" for k, e, h in best["diff"])))
    # uniones entre tomas
    takes = tl.get("takes", []); overl = []; abrupt = []
    for k in range(len(takes) - 1):
        if takes[k + 1][0] < takes[k][1] - 1e-3: overl.append((takes[k], takes[k + 1]))
    for st, en in takes:
        y = x[int(st * sr): int(en * sr)]
        if len(y) < sr * 0.2: continue
        ref = np.percentile(np.abs(y), 99) + 1e-9; tail = np.sqrt(np.mean(y[-int(0.03 * sr):] ** 2)) / ref
        if 20 * np.log10(tail + 1e-9) > -26: abrupt.append((st, en, round(20 * np.log10(tail + 1e-9), 1)))
    # voz frente a música y efectos
    mask_txt = "sin pistas separadas"
    sd = os.path.join(out, V.get("stems", "")) if V.get("stems") else None
    if sd and os.path.exists(os.path.join(sd, "voz.wav")):
        vz, srs = sf.read(os.path.join(sd, "voz.wav"), dtype="float32"); mu, _ = sf.read(os.path.join(sd, "musica.wav"), dtype="float32"); fx, _ = sf.read(os.path.join(sd, "efectos.wav"), dtype="float32")
        vz = vz.mean(axis=1) if vz.ndim > 1 else vz; bg = (mu.mean(axis=1) if mu.ndim > 1 else mu) + (fx.mean(axis=1) if fx.ndim > 1 else fx)
        hop = int(0.5 * srs); n = min(len(vz), len(bg)) // hop
        rv = np.sqrt(np.mean(vz[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12); rb = np.sqrt(np.mean(bg[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
        act = rv > np.percentile(rv, 95) * 10 ** (-20 / 20); ratio = 20 * np.log10(rv[act] / rb[act])
        mask_txt = f"voz por encima de música + efectos mientras hay voz: mediana {np.median(ratio):.1f} dB · percentil 5 {np.percentile(ratio, 5):.1f} dB · mínimo {ratio.min():.1f} dB ({act.sum()} ventanas de 0,5 s)"
    # informe
    # informe en el proyecto de edición (vídeo largo) o en la carpeta de trabajo (Short): la carpeta de entrega queda limpia
    N = tot["n"]; pd = os.path.join(out, "PROYECTO_DE_EDICION") if os.path.isdir(os.path.join(out, "PROYECTO_DE_EDICION")) else res
    with open(os.path.join(pd, "control_voz_wer.csv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";"); wr.writeheader(); wr.writerows(rows)
    L = [f"# Control de la voz: guion frente a narración final (WER) — {V['title']}", "",
         f"Audio comprobado: `{os.path.relpath(narr, out)}` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.", "",
         "| Medida | Resultado |", "|---|---|",
         f"| Palabras del guion | {N} |",
         f"| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | {tot['comb']} |",
         f"| **WER final** | **{tot['comb'] / N:.3%}** (coincidencia {1 - tot['comb'] / N:.3%}) |",
         f"| WER solo con Parakeet TDT v3 | {tot['par'] / N:.3%} ({tot['par']} errores) |",
         f"| WER solo con Whisper small | {tot['whi'] / N:.3%} ({tot['whi']} errores) |",
         f"| WER en bloques de ~20 s (uniones entre tomas) | {bt['err'] / max(1, bt['n']):.3%} ({bt['err']} errores en {bt['n']} palabras, {len(brows)} bloques) |",
         f"| Términos clave no reconocidos por ningún reconocedor | {len(key_miss)} |",
         f"| Tomas solapadas | {len(overl)} |", f"| Tomas que terminan de golpe con voz | {len(abrupt)} |",
         f"| Voz frente a música y efectos | {mask_txt} |", "",
         f"Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **{'CUMPLE' if tot['comb'] / N <= 0.002 else 'NO CUMPLE'}**.", ""]
    dif = [r for r in rows if r["err"]]
    L += ["## Diferencias que quedan (frase a frase)", ""]
    if not dif: L.append("Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.")
    for r in dif: L.append(f"- {r['t']} s · «{r['guion']}» → Parakeet: «{r['parakeet']}» · Whisper: «{r['whisper']}» · {r['detalle']}")
    hom = [(r["t"], r["homofonos"]) for r in rows if r["homofonos"]]; uni = [(r["t"], r["uniones"]) for r in rows if r["uniones"]]
    L += ["", "## Igualdades que no cuentan como error", "",
          "Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):" + ("" if hom else " ninguno.")]
    L += [f"- {t} s · {h}" for t, h in hom]
    L += ["", "Uniones o separaciones de palabras (la separación entre palabras no se oye):" + ("" if uni else " ninguna.")]
    L += [f"- {t} s · {u}" for t, u in uni]
    L += ["", "## Términos clave", ""]
    L.append("Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor." if not key_miss else "")
    for t, w, txt in key_miss: L.append(f"- {t} s · «{w}» en «{txt}»")
    L += ["", "## Bloques de ~20 s", "", "| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |", "|---|---|---|---|---|---|---|"]
    for r in brows: L.append("| " + " | ".join(str(v) for v in r) + " |")
    open(os.path.join(pd, "CONTROL_VOZ_WER.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"WER final {tot['comb'] / N:.3%} · Parakeet {tot['par'] / N:.3%} · Whisper {tot['whi'] / N:.3%} · bloques {bt['err'] / max(1, bt['n']):.3%} · términos sin reconocer {len(key_miss)} · solapes {len(overl)} · finales bruscos {len(abrupt)}")
    print(mask_txt)

if __name__ == "__main__":
    main(sys.argv[1])
