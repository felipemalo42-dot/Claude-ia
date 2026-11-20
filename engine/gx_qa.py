"""Control de calidad del vídeo final (VIDEO_LARGO_GTA6 o el Short): formato, fluidez, orden de reproducción, congelados,
negros, sonoridad, subtítulos y sincronía. Escribe CONTROL_DE_CALIDAD.md en PROYECTO_DE_EDICION (o en la carpeta de trabajo del Short).

Uso: python gx_qa.py gx|gs
Fluidez: el montaje reproduce cada plano de gameplay fotograma a fotograma (fotograma k del plano = fotograma k del tramo
original). Se compara el cambio entre fotogramas consecutivos del vídeo final con el del original en el mismo instante:
si el original se mueve y el vídeo final no, hay un fotograma repetido o congelado introducido por el montaje.
"""
import importlib, json, math, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

SW, SH = 160, 90
def diffs(path, ss=None, n=None, size=(SW, SH), crop=None):
    """Diferencia media entre fotogramas consecutivos (escala de grises reducida)."""
    w, h = size
    vf = (f"{crop}," if crop else "") + f"scale={w}:{h},format=gray"
    cmd = ["ffmpeg", "-nostdin", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + ["-i", path] + (["-frames:v", str(n)] if n else []) + \
          ["-vf", vf, "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.int16)
    return np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)), len(fr)

def player_order(mp4):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.split()
    ts = [int(x.split(",")[0]) for x in o if x.split(",")[0].lstrip("-").isdigit()]
    order = sorted(range(len(ts)), key=ts.__getitem__)
    durs = np.diff(sorted(ts))
    return sum(1 for a, b in zip(order, order[1:]) if b < a), len(ts), (len(set(durs.tolist())) if len(durs) else 0)

def main(vid):
    mod = importlib.import_module(f"videos.{vid}"); V = mod.VIDEO; R = sys.modules[mod.__name__.replace(vid, vid + "_render")] if False else None
    R = importlib.import_module(f"videos.{vid}_render")
    out = os.path.join(build.ROOT, V["folder"]); res = os.path.join(out, V["res_dir"]); mp4 = os.path.join(out, V["file"] + ".mp4")
    rep_dir = os.path.join(out, "PROYECTO_DE_EDICION") if vid == "gx" else res
    Wv, Hv = V.get("size", (1920, 1080))
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate:stream=codec_name,profile,width,height,r_frame_rate,avg_frame_rate,pix_fmt,sample_rate,channels,nb_frames,duration",
                                    "-of", "json", mp4], capture_output=True, text=True).stdout)
    fmt = pr["format"]; vs = [s for s in pr["streams"] if s.get("width")][0]; aus = [s for s in pr["streams"] if s.get("sample_rate")][0]
    dur = float(fmt["duration"]); nfr = int(vs.get("nb_frames") or 0)
    back, nts, ndur = player_order(mp4)
    lu = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", lu); lufs = float(m[-1]) if m else float("nan")
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lu); tpk = float(tp[-1]) if tp else float("nan")
    bd = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-vf", "blackdetect=d=0.25:pix_th=0.06", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bd)
    # fluidez: vídeo final frente al original, plano a plano
    tl = json.load(open(os.path.join(res, "timeline.json")))
    ctx = build.Ctx(V, tl, Wv, Hv); R._T.clear(); T = R.table(ctx)
    bad = R.validate(ctx, verbose=False)
    # zona de imagen sin rótulos ni subtítulos
    crop = "crop=iw:ih*0.62:0:ih*0.16" if vid == "gx" else "crop=iw:ih*0.45:0:ih*0.17"
    dout, nout = diffs(mp4, crop=crop)
    shots = [s for s in T["shots"] if not s["src"].startswith("g:")]
    froz = 0; rep = 0; checked = 0; worst = []; src_rep = 0
    for s in shots:
        f0 = int(np.ceil(s["t0"] * 30)) + 2; f1 = int(np.floor(s["t1"] * 30)) - 2
        if f1 - f0 < 6: continue
        if vid == "gx":
            path, loc, avail, vert = R.x_window(s)
            if vert: continue          # tarjeta vertical: imagen pequeña sobre fondo desenfocado
            if s.get("zoom"): continue  # el zoom animado cambia la imagen aunque el original esté quieto
        else:
            path, loc, avail, kind = R.window(s)
            if kind == "c": continue
        # misma correspondencia que el montaje: el fotograma f del vídeo es el fotograma k = ⌊(f/30 − t0)·30⌋ del tramo leído
        # desde «loc» (se lee igual que lo lee el montaje, desde loc, y se descartan los k0 primeros)
        k0 = int(math.floor((f0 / 30 - s["t0"]) * 30 + 1e-6))
        dsrc, _ = diffs(path, ss=loc, n=k0 + (f1 - f0) + 1, crop=crop); dsrc = dsrc[k0:]
        do = dout[f0:f1]; k = min(len(do), len(dsrc))
        if k < 4: continue
        checked += k
        moving = dsrc[:k] > 1.0
        z = (do[:k] < 0.25) & moving
        froz += int(z.sum())
        if z.sum(): worst.append((round(s["t0"], 2), s["src"], int(z.sum())))
        # repeticiones que ya trae la grabación original (la imagen se mueve antes y después, pero ese fotograma repite)
        ds = dsrc[:k]; rs = [i for i in range(1, k - 1) if ds[i] < 0.25 and ds[i - 1] > 1.0 and ds[i + 1] > 1.0]
        src_rep += len(rs)
    # subtítulos frente al guion
    srt = open(os.path.join(out, V["names"]["srt"]), encoding="utf-8").read()
    blocks = [b for b in srt.strip().split("\n\n") if b.strip()]
    sub_txt = " ".join(" ".join(b.split("\n")[2:]) for b in blocks)
    import voice_qa as Q
    script_txt = " ".join(s["text"] for b in tl["beats"] for s in b["sents"])
    sw = Q.wer(script_txt, sub_txt)
    times = []
    for b in blocks:
        mm = re.findall(r"(\d+):(\d+):(\d+),(\d+)", b.split("\n")[1])
        if len(mm) == 2: times.append([int(h) * 3600 + int(m_) * 60 + int(s_) + int(ms) / 1000 for h, m_, s_, ms in mm])
    overl = sum(1 for a, b in zip(times, times[1:]) if b[0] < a[1] - 1e-3)
    # sincronía corte ↔ palabra
    offs = [s["t0"] - s["word_t"] for s in T["shots"] if s.get("word_t")]
    L = [f"# Control de calidad — {V['folder']}/{V['file']}.mp4", "",
         "| Medida | Resultado | Objetivo |", "|---|---|---|",
         f"| Duración | {dur:.1f} s ({int(dur // 60)}:{int(dur % 60):02d}) | {'≥ 10 min' if vid == 'gx' else '35-60 s'} |",
         f"| Vídeo | {vs['codec_name'].upper()} {vs.get('profile', '')} · {vs['width']}×{vs['height']} · {vs['pix_fmt']} | {'1920×1080' if vid == 'gx' else '1080×1920'} |",
         f"| Fotogramas por segundo | {vs['r_frame_rate']} (media {vs['avg_frame_rate']}) · {ndur} duración(es) de fotograma distinta(s) | 30 constantes |",
         f"| Fotogramas | {nfr} (esperados por la duración de la pista de vídeo: {round(float(vs.get('duration') or dur) * 30)}) | iguales |",
         f"| Tasa de bits | {int(fmt['bit_rate']) / 1e6:.1f} Mbit/s · {int(fmt['size']) / 1e6:.0f} MB | H.264 de alta calidad |",
         f"| Audio | {aus['codec_name'].upper()} {aus['sample_rate']} Hz · {aus['channels']} canales · {lufs:.1f} LUFS · pico {tpk:.1f} dBFS | −14 LUFS |",
         f"| Orden de reproducción (saltos atrás según las marcas de tiempo) | {back} de {nts} | 0 |",
         f"| Planos de gameplay con material continuo suficiente (sin bucles ni congelados) | {len(shots) - len(bad)} de {len(shots)} | todos |",
         f"| Fotogramas repetidos o congelados por el montaje (el original se mueve y el vídeo no) | {froz} de {checked} comprobados | 0 |",
         f"| Fotogramas que ya vienen repetidos en la grabación original (tirones del propio juego o de la captura) | {src_rep} de {checked} | informativo |",
         f"| Tramos en negro (≥ 0,25 s) | {len(blacks)} {'(' + ', '.join(f'{float(a):.1f}-{float(b):.1f} s' for a, b in blacks) + ')' if blacks else ''} | solo fundidos intencionados |",
         f"| Subtítulos frente al guion | {len(blocks)} subtítulos · diferencias de palabras {sw['err']} de {sw['n']} · solapes {overl} | 0 |",
         (f"| Sincronía corte ↔ palabra | {len(offs)} cortes anclados · desfase medio {np.mean(offs):+.3f} s · máximo {max(abs(o) for o in offs):.3f} s | −0,06 s (2 fotogramas antes) |" if offs else "| Sincronía corte ↔ palabra | sin cortes anclados | |"), ""]
    if worst: L += ["Planos con fotogramas repetidos:", ""] + [f"- {t} s · {src} · {n}" for t, src, n in worst]
    open(os.path.join(rep_dir, "CONTROL_DE_CALIDAD.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main(sys.argv[1])
