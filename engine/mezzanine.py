"""Tramos de gameplay en calidad de entrega («mezzanine») para VIDEO_LARGO_GTA6 y su Short.

Cada tramo se lee directamente de la copia pública de mayor resolución (Internet Archive, AV1 4K/1080p) y se guarda en
1920×1080, 30 fps constantes, H.264 CRF 14 (prácticamente sin pérdidas), sin audio. Reglas:
- Grabaciones a 59,94 fps de un juego que funciona a 30 fps (cada imagen repetida dos veces): se eliminan las repeticiones
  (mpdecimate) y se conserva el ritmo original de imágenes únicas (fps=30000/1001). No se inventan fotogramas
  (sin interpolación) y no se cambia la velocidad: 29,97 → 30 fps es un 0,1 % más rápido, imperceptible.
- Grabación HDR10 (PQ, BT.2020): conversión a SDR BT.709 con el operador Hable, sin desaturar.
- Grabaciones a 29,97/30 fps: se conservan todos los fotogramas.
Correspondencia de tiempos: segundo T del original = inicio del tramo + t × 1,001 (t = segundo dentro del tramo).

Uso: python mezzanine.py [ID ...]   (sin argumentos: todos los tramos de WINDOWS que falten)
"""
import json, os, subprocess, sys, time

SCR = "/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad"
OUT = os.environ.get("MEZ_DIR", f"{SCR}/xmez")
PROXY = ["-http_proxy", os.environ.get("HTTPS_PROXY", ""), "-ca_file", "/root/.ccr/ca-bundle.crt", "-tls_verify", "1"]
TONEMAP = ("zscale=w=1920:h=1080:filter=lanczos:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
SCALE = "scale=1920:1080:flags=lanczos,format=yuv420p"
DECIMATE = "mpdecimate=hi=64*12:lo=64*5:frac=0.33,fps=30000/1001"
# 59,94 → 29,97 quitando en cada pareja de fotogramas la imagen repetida (decimate, ciclo 2): conserva el ritmo real del juego.
# Con GTAsatara, mpdecimate (umbrales amplios) descartaba también imágenes distintas pero muy parecidas en escenas lentas y
# el vídeo repetía fotogramas que el original no repite (comprobado contra el original: 34 de 35 repeticiones).
DECIMATE2 = "decimate=cycle=2"
DEC = {"gJyMGHxCKHU": DECIMATE2}

# fuente → (fps del archivo, ¿HDR?)
SRC = {"Om4W6tYMF-0": (29.97, False), "gJyMGHxCKHU": (59.94, False), "ey0qks0aQ-c": (59.94, True),
       "qbhJRtgCx30": (59.94, False), "eD5ndr0OMM0": (30.0, False),
       "JHRVSzM2O2M": (59.94, False), "uMYUjOLOOVQ": (59.94, False)}   # estos dos: vídeos verticales de 1080×1920
VERTICAL = {"JHRVSzM2O2M", "uMYUjOLOOVQ"}
# tramos (segundos del original) que usa el montaje; se amplían 1 s por cada lado para poder ajustar los planos
WINDOWS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos", "gx_windows.json"), encoding="utf-8"))

def name(vid, a, b): return f"{OUT}/{vid}_{a:07.2f}_{b:07.2f}.mp4"

def build(vid, a, b):
    out = name(vid, a, b)
    if os.path.exists(out): return out
    fps, hdr = SRC[vid]
    vf = [TONEMAP if hdr else (SCALE.replace("1920:1080", "1080:1920") if vid in VERTICAL else SCALE)]
    if fps > 50: vf.append(DEC.get(vid, DECIMATE))
    vf.append("setpts=N/(30*TB)")
    url = f"https://archive.org/download/youtube-{vid}/{vid}.webm"
    tmp = out + ".part.mp4"; t0 = time.time()
    cmd = ["nice", "-n", "8", "ffmpeg", "-nostdin", "-v", "error", "-y", *PROXY, "-ss", f"{a:.3f}", "-i", url, "-t", f"{b - a:.3f}", "-an",
           "-vf", ",".join(vf), "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
           "-g", "30", "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", tmp]
    for k in range(3):
        r = subprocess.run(cmd)
        if r.returncode == 0: break
        print(f"  reintento {k + 1} de {vid} {a}-{b}", flush=True); time.sleep(5 * (k + 1))
    else: raise RuntimeError(f"no se pudo extraer {vid} {a}-{b}")
    os.replace(tmp, out); print(f"  {os.path.basename(out)} · {time.time() - t0:.0f} s", flush=True)
    return out

def windows_for(vid): return [(float(w[0]), float(w[1])) for w in WINDOWS.get(vid, [])]

# ---------------------------------------------------------------- recortes verticales 9:16 para el Short (desde la copia 4K)
VWIN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos", "gs_windows.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos", "gs_windows.json")) else {}
def vname(vid, a, b, cx): return f"{OUT}/{vid}_{a:07.2f}_{b:07.2f}_v{cx:.2f}.mp4"

def build_v(vid, a, b, cx):
    """Recorte vertical (9:16) centrado en cx (0-1) de la copia de mayor resolución → 1080×1920, 30 fps, solo imágenes únicas."""
    out = vname(vid, a, b, cx)
    if os.path.exists(out): return out
    fps, hdr = SRC[vid]
    crop = f"crop=ih*9/16:ih:max(0\\,min(iw-ih*9/16\\,iw*{cx:.4f}-ih*9/32)):0"
    vf = [crop, (TONEMAP.replace("w=1920:h=1080", "w=1080:h=1920") if hdr else "scale=1080:1920:flags=lanczos,format=yuv420p")]
    if fps > 50: vf.append(DEC.get(vid, DECIMATE))
    vf.append("setpts=N/(30*TB)")
    url = f"https://archive.org/download/youtube-{vid}/{vid}.webm"; tmp = out + ".part.mp4"; t0 = time.time()
    cmd = ["nice", "-n", "8", "ffmpeg", "-nostdin", "-v", "error", "-y", *PROXY, "-ss", f"{a:.3f}", "-i", url, "-t", f"{b - a:.3f}", "-an",
           "-vf", ",".join(vf), "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
           "-g", "30", "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", tmp]
    for k in range(3):
        if subprocess.run(cmd).returncode == 0: break
        time.sleep(5 * (k + 1))
    else: raise RuntimeError(f"no se pudo extraer {vid} {a}-{b} (vertical)")
    os.replace(tmp, out); print(f"  {os.path.basename(out)} · {time.time() - t0:.0f} s", flush=True); return out

def locate_v(vid, T, cx=None):
    for w in VWIN.get(vid, []):
        a, b, c_ = float(w[0]), float(w[1]), float(w[2])
        if a <= T < b and (cx is None or abs(c_ - cx) < 1e-3):
            p = vname(vid, a, b, c_)
            if os.path.exists(p): return p, (T - a) / 1.001, (b - T) / 1.001 - 0.12
    return None

def locate(vid, T):
    """Segundo T del original → (archivo del tramo, segundo dentro del tramo) o None si no hay tramo."""
    for a, b in windows_for(vid):
        if a <= T < b:
            p = name(vid, a, b)
            if os.path.exists(p): return p, (T - a) / 1.001
    return None

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[1:2] == ["--short"]:
        for vid, ws in VWIN.items():
            for w in ws: build_v(vid, float(w[0]), float(w[1]), float(w[2]))
        print("FIN", flush=True); sys.exit(0)
    ids = sys.argv[1:] or list(WINDOWS)
    for vid in ids:
        for a, b in windows_for(vid): build(vid, a, b)
    print("FIN", flush=True)
