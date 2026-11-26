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
DEC = {"gJyMGHxCKHU": DECIMATE2, "cEDUO1zjB5c": DECIMATE2, "-UuHA1h-Cf8": DECIMATE2, "gvlY1gVmSKM": DECIMATE2, "NwQKirh2dxE": DECIMATE2}

# fuente → (fps del archivo, ¿HDR?)
SRC = {"Om4W6tYMF-0": (29.97, False), "gJyMGHxCKHU": (59.94, False), "ey0qks0aQ-c": (59.94, True),
       # vídeos 2 y 3 (Planeta Vice City, GTA 6 a juicio): 30 o 60 fps exactos (juego a 30 grabado a 60 → decimate)
       "cEDUO1zjB5c": (60.0, False), "-UuHA1h-Cf8": (60.0, False), "3UiRmXUIE9k": (30.0, False), "xnNu7YybiCM": (30.0, False),
       "jZka1Ay1-gI": (29.97, False), "gvlY1gVmSKM": (59.94, False), "NwQKirh2dxE": (60.0, False), "4HCd052lpnA": (30.0, False), "gN5qaT7u-uM": (29.97, False), "R9r9ew12GcA": (30.0, False),
       "qbhJRtgCx30": (59.94, False), "eD5ndr0OMM0": (30.0, False),
       "JHRVSzM2O2M": (59.94, False), "uMYUjOLOOVQ": (59.94, False)}   # estos dos: vídeos verticales de 1080×1920
VERTICAL = {"JHRVSzM2O2M", "uMYUjOLOOVQ", "R9r9ew12GcA"}
# fuentes que no son copias de YouTube: URL directa y recorte de la imagen de juego (sin los rótulos del montaje original)
# vídeo 4 (GTA 5 vs GTA 6): GTA 5 de Kotaku y The Escapist (2013), GTA 5 Enhanced de LOCAL GAMING (4K60) y la base de GTA 6 de Sirloin
SRC.update({"igPenta": (30.0, False), "igFP": (30.0, False), "igRocket": (30.0, False), "igPlaneV": (30.0, False),
            "NKq2GOBaJV8": (29.97, False), "QBMZ1ZXlflk": (60.0, False), "HAIx2b9ThL8": (59.94, False)})
# Shorts 10-14 (guías IGN 4K y la misión del huracán de Lootward)
SRC.update({"B0b5JhrGUJQ": (30.0, False)})
SRC.update({"rK6MXJpcaIA": (59.94, False)}); DEC["rK6MXJpcaIA"] = DECIMATE2   # vídeo largo de la policía (Cynic, 4K a 59,94)
SRC.update({"GByO53W1-fI": (60.0, False), "IqKb-yJGroE": (30.0, False), "gNMTCbS8Ytg": (60.0, False), "mMBdAMjCEnE": (60.0, False), "JPnJPuH4N6Q": (30.0, False)})   # Shorts rt/gr/fp/am (IGN; tiras limpias de los verticales ya recortadas en xmez)
SRC.update({"vpWestern": (30.0, False), "vpWaffles": (30.0, False), "vpWeazel": (30.0, False), "vpBurger": (30.0, False), "vpBradlaw": (30.0, False),
            "vpDive": (30.0, False), "vpGame": (30.0, False), "P-BbiYUPD-o": (30.0, False)})   # Shorts zp/jg/tb (Video Pump, CC BY 4.0; tiras limpias ya recortadas en xmez) e IGN
SRC.update({"IG2hfrBVjh4": (29.97, False), "Q5XgKNEnbP4": (30.0, False), "V99Ng_VTBUs": (59.94, False), "nqmpDCbz3lA": (30.0, False)})
DEC["V99Ng_VTBUs"] = "fps=30000/1001"   # GTA 5 en PC a 60 imágenes distintas por segundo: se toma una de cada dos (sin mpdecimate)
SRC["vpHospital1"] = (30.0, False)
SRC_URL = {"vpHospital1": "https://archive.org/download/videopump-2026-11-20-hospital-bill/24-hospital-bill-1191.mp4"}
SRC_CROP = {"vpHospital1": "crop=1080:608:0:656"}   # franja 16:9 con la partida dentro del vertical de Video Pump
# vídeo largo de los finales: recopilación con rótulos arriba, marcas de agua y subtítulos abajo → recorte 16:9 central (76 %)
SRC_CROP["B0b5JhrGUJQ"] = "crop=1938:1090:70:60"
def rate(vid):
    """Segundos del original por segundo del tramo: 1,001 si el original va a 29,97/59,94 fps; 1 si va a 30/60 fps exactos."""
    return 1.0 if abs(SRC[vid][0] - round(SRC[vid][0])) < 1e-3 else 1.001
# tramos (segundos del original) que usa el montaje; se amplían 1 s por cada lado para poder ajustar los planos
_VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
WINDOWS = {}
for _f in ("gx_windows.json", "pv_windows.json", "jz_windows.json", "cv_windows.json", "shx_windows.json", "sh2_windows.json", "fn_windows.json", "pl_windows.json"):   # un archivo por vídeo; se suman las ventanas de cada fuente
    if os.path.exists(os.path.join(_VD, _f)):
        for _k, _v in json.load(open(os.path.join(_VD, _f), encoding="utf-8")).items(): WINDOWS.setdefault(_k, []).extend(_v)

def source(vid):
    """Copia local completa del original si existe (descargada con reanudación: la red corta las lecturas largas);
    si no, la URL de Internet Archive. → (lista de argumentos de entrada de ffmpeg sin -ss)"""
    loc = f"{OUT}/_src/{vid}.webm"
    if os.path.exists(loc): return [loc]
    return [*PROXY, SRC_URL.get(vid) or f"https://archive.org/download/youtube-{vid}/{vid}.webm"]

def complete(path, expected):
    """¿El tramo tiene toda su duración? Si la conexión se corta a mitad de descarga, ffmpeg termina «bien» con un
    archivo más corto: eso no puede pasar por bueno (los planos leerían más allá del final)."""
    try: d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))
    except Exception: return False
    if d < expected - 0.4: print(f"  incompleto: {os.path.basename(path)} dura {d:.2f} s de {expected:.2f}", flush=True); return False
    return True

def name(vid, a, b): return f"{OUT}/{vid}_{a:07.2f}_{b:07.2f}.mp4"

def build(vid, a, b):
    out = name(vid, a, b)
    if os.path.exists(out): return out
    fps, hdr = SRC[vid]
    vf = ([SRC_CROP[vid]] if vid in SRC_CROP else []) + [TONEMAP if hdr else (SCALE.replace("1920:1080", "1080:1920") if vid in VERTICAL else SCALE)]
    if fps > 50: vf.append(DEC.get(vid, DECIMATE))
    vf.append("setpts=N/(30*TB)")
    inp = source(vid)
    tmp = out + ".part.mp4"; t0 = time.time()
    cmd = ["nice", "-n", os.environ.get("MEZ_NICE", "8"), "ffmpeg", "-nostdin", "-v", "error", "-y", *inp[:-1], "-ss", f"{a:.3f}", "-i", inp[-1], "-t", f"{b - a:.3f}", "-an",
           "-vf", ",".join(vf), "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", os.environ.get("MEZ_PRESET", "slow"), "-crf", os.environ.get("MEZ_CRF", "14"), "-pix_fmt", "yuv420p",
           "-g", "30", "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", tmp]
    for k in range(4):
        r = subprocess.run(cmd)
        if r.returncode == 0 and complete(tmp, (b - a) / rate(vid)): break
        print(f"  reintento {k + 1} de {vid} {a}-{b}", flush=True); time.sleep(5 * (k + 1))
    else: raise RuntimeError(f"no se pudo extraer {vid} {a}-{b}")
    os.replace(tmp, out); print(f"  {os.path.basename(out)} · {time.time() - t0:.0f} s", flush=True)
    return out

def windows_for(vid): return [(float(w[0]), float(w[1])) for w in WINDOWS.get(vid, [])]

# ---------------------------------------------------------------- recortes verticales 9:16 para el Short (desde la copia 4K)
VWIN = {}
for _f in ("gs_windows.json", "ps_windows.json", "js_windows.json", "zp_windows.json"):
    if os.path.exists(os.path.join(_VD, _f)):
        for _k, _v in json.load(open(os.path.join(_VD, _f), encoding="utf-8")).items(): VWIN.setdefault(_k, []).extend(_v)
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
    inp = source(vid); tmp = out + ".part.mp4"; t0 = time.time()
    cmd = ["nice", "-n", os.environ.get("MEZ_NICE", "8"), "ffmpeg", "-nostdin", "-v", "error", "-y", *inp[:-1], "-ss", f"{a:.3f}", "-i", inp[-1], "-t", f"{b - a:.3f}", "-an",
           "-vf", ",".join(vf), "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", os.environ.get("MEZ_PRESET", "slow"), "-crf", os.environ.get("MEZ_CRF", "14"), "-pix_fmt", "yuv420p",
           "-g", "30", "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", tmp]
    for k in range(4):
        if subprocess.run(cmd).returncode == 0 and complete(tmp, (b - a) / rate(vid)): break
        print(f"  reintento {k + 1} de {vid} {a}-{b} (vertical)", flush=True); time.sleep(5 * (k + 1))
    else: raise RuntimeError(f"no se pudo extraer {vid} {a}-{b} (vertical)")
    os.replace(tmp, out); print(f"  {os.path.basename(out)} · {time.time() - t0:.0f} s", flush=True); return out

def locate_v(vid, T, cx=None):
    for w in VWIN.get(vid, []):
        a, b, c_ = float(w[0]), float(w[1]), float(w[2])
        if a <= T < b and (cx is None or abs(c_ - cx) < 1e-3):
            p = vname(vid, a, b, c_)
            if os.path.exists(p): return p, (T - a) / rate(vid), (b - T) / rate(vid) - 0.12
    return None

def locate(vid, T):
    """Segundo T del original → (archivo del tramo, segundo dentro del tramo) o None si no hay tramo."""
    for a, b in windows_for(vid):
        if a <= T < b:
            p = name(vid, a, b)
            if os.path.exists(p): return p, (T - a) / rate(vid)
    return None

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[1:2] == ["--short"]:
        for vid, ws in VWIN.items():
            if sys.argv[2:] and vid not in sys.argv[2:]: continue   # python mezzanine.py --short [ID ...]
            for w in ws: build_v(vid, float(w[0]), float(w[1]), float(w[2]))
        print("FIN", flush=True); sys.exit(0)
    if os.environ.get("MEZ_ONLY"):   # p. ej. MEZ_ONLY=cv: solo los tramos de ese vídeo (las fuentes se comparten entre vídeos)
        WINDOWS = {k: v for k, v in json.load(open(os.path.join(_VD, os.environ["MEZ_ONLY"] + "_windows.json"), encoding="utf-8")).items()}
    ids = sys.argv[1:] or list(WINDOWS)
    for vid in ids:
        for a, b in windows_for(vid): build(vid, a, b)
    print("FIN", flush=True)
