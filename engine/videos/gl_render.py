"""Montaje de GTA6_VIDEO_LANZAMIENTO con material oficial de Rockstar Games.

- Cada plano empieza en la palabra exacta del guion que lo menciona (tiempos de palabra del reconocedor de voz).
- Fotos: encuadre de cobertura + movimiento lento (Ken Burns). Si un plano supera ~4,5 s se renueva el encuadre.
- Vídeo: se decodifica con ffmpeg (sin audio: el audio oficial va silenciado) y se dibuja fotograma a fotograma.
  Tramos del Extended Look con misiones o escenas de historia: prohibidos (BAD); si un plano llegara a ellos, vuelve a su inicio.
- Rótulos: fuente de cada plano, semáforo (oficial / interpretación / exclusivo Ultimate / bono de reserva),
  capítulo, nombres, citas oficiales y subtítulos dinámicos palabra a palabra.
"""
import bisect, glob, json, math, os, subprocess, numpy as np, skia
from gfx import *
from brand import PAL, draw_badge, wordmark
import components as K

SCR = "/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad"
RM = os.environ.get("GL_MEDIA", f"{SCR}/rmedia"); EL = os.environ.get("GL_EL", f"{SCR}/el1080")
W, H, FPS = 1920, 1080, 30
LEAD = 0.06        # el corte llega 2 fotogramas antes de que empiece la palabra (sincronía percibida)
MAXD = 4.6         # renovación del encuadre en planos largos
YEL, GRN, MAG, CYA = "#FFC72C", "#22C55E", "#FF4FD8", "#36E3FF"

# ---------------------------------------------------------------- catálogo de material oficial
EL_RANGES = {"r1": (360.0, 688.0), "r3": (994.0, 1164.0), "r2": (750.0, 790.0), "r4": (1208.0, 1238.0), "r5": (1540.0, 1582.0)}
# tramos del Extended Look que NO se muestran (misiones, escenas de historia, violencia, rótulos de cierre)
BAD = [(360.0, 364.9), (372.0, 379.9), (386.5, 421.8), (481.9, 483.9), (538.6, 544.4), (546.6, 554.4), (560.9, 564.9), (568.9, 570.9), (574.9, 690.0),
       (1000.0, 1026.4), (1046.9, 1048.9), (1051.4, 1061.0), (1067.9, 1069.4), (1079.6, 1083.6), (1112.0, 1115.6), (1125.6, 1127.9),
       (1138.4, 1139.5), (1140.9, 1141.9), (1143.4, 1143.9), (1146.6, 1170.0), (1216.0, 1217.8), (1229.0, 1240.0),
       (1540.0, 1545.9), (1550.95, 1565.9), (1568.4, 1569.9), (1572.6, 1600.0)]
_IDX = {}
def _index():
    if _IDX: return _IDX
    for p in glob.glob(f"{RM}/**/*.jpg", recursive=True): _IDX[os.path.splitext(os.path.basename(p))[0]] = p
    return _IDX

def asset_path(src):
    k, v = src.split(":", 1)
    if k in ("s", "u", "v", "a"): return _index()[v]
    if k == "l": return f"{RM}/GTAVI_Launch_Trailer.mp4"
    if k == "p": return f"{RM}/GTAVI_Pre-Load_Now.mp4"
    if k == "c": return f"{RM}/GTAVI_Videos/{v}_Video_Clip.mp4"
    if k == "k": return f"{RM}/GTAVI_Videos/GTAVI_Official_Cover_Art_Landscape.mp4"
    if k == "e":
        T = float(v)
        for r, (a, b) in EL_RANGES.items():
            if a <= T < b: return f"{EL}/{r}.mp4"
        raise ValueError(f"segundo {T} fuera de los tramos extraídos")
    if k == "x": return x_path(v.split("@")[0])
    return None

# ---------------------------------------------------------------- gameplay de terceros (clips externos con licencia y crédito)
# Fuente "x:ID@segundo": vídeo ID del catálogo videos/gp_clips.json, guardado en XDIR/ID.<ext>. Cada plano muestra su autor.
XDIR = os.environ.get("GL_X", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "GTA6_VIDEO_LANZAMIENTO", "clips_externos"))
XCAT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gp_clips.json"), encoding="utf-8"))
XBAD = {}   # ID → [(a, b)] tramos que no se muestran (sangre, rótulos del autor, cámara del streamer, menús)
def x_path(vid):
    for ext in ("mp4", "mkv", "webm", "mov"):
        p = f"{XDIR}/{vid}.{ext}"
        if os.path.exists(p): return p
    raise FileNotFoundError(f"falta el clip externo {vid} en {XDIR}")
def x_credit(vid, short=False):
    m = XCAT[vid]
    return f"{m['autor']} · {m['plataforma']}" if short else f"{m['autor']} · {m['plataforma']} «{m['titulo'][:46]}» · {m['licencia']}"

def _mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
def source_label(src):
    k, v = src.split(":", 1)
    if k == "s": return f"Rockstar Games · captura oficial «{v}»"
    if k == "u": return f"Rockstar Games · edición Ultimate «{v.replace('ULTIMATE_EDITION_', '')}»"
    if k == "v": return f"Rockstar Games · paquete Vintage Vice City «{v.replace('VINTAGE_VICE_CITY_', '')}»"
    if k == "a": return f"Rockstar Games · ilustración oficial «{v.replace('_landscape', '')}»"
    if k == "e": return f"Rockstar Games · An Extended Look · {_mmss(float(v))}"
    if k == "l": return f"Rockstar Games · tráiler de lanzamiento · {_mmss(float(v))}"
    if k == "p": return f"Rockstar Games · vídeo «Pre-Load Now» · {_mmss(float(v))}"
    if k == "c": return f"Rockstar Games · vídeo oficial de personaje «{v.replace('_', ' ')}»"
    if k == "k": return "Rockstar Games · portada oficial animada"
    if k == "x": vid, s = v.split("@"); return f"Gameplay: {x_credit(vid)} · {_mmss(float(s))}"
    return None
GFX_SRC = {"mosaic": "Gráfico: Sal y Asfalto con las 138 capturas oficiales de Rockstar Games", "map": "Representación aproximada sobre el mapa real de Florida (Natural Earth). Rockstar no ha publicado el mapa",
           "postcards": "Gráfico: Sal y Asfalto con las postales oficiales de Rockstar Games", "cast": "Gráfico: Sal y Asfalto con ilustraciones oficiales de Rockstar Games",
           "swap": "Montaje: Sal y Asfalto con dos capturas oficiales de Rockstar Games", "poll": "Gráfico: Sal y Asfalto con ilustraciones oficiales de Rockstar Games",
           "media": "Rockstar Games · rockstargames.com/VI/downloads", "timeline": "Gráfico: Sal y Asfalto · fuentes en la descripción",
           "claim": "Rob Nelson (Rockstar North) a Kinda Funny, recogido por Push Square y TweakTown (08/2026)",
           "el_card": "Rockstar Games · An Extended Look · estreno en Netflix el 27/08/2026", "profile": "Representación gráfica: no es una imagen del juego",
           "editions": "Rockstar Games · página de la edición Ultimate", "unknown": "Rob Nelson a Kinda Funny (08/2026) · plataformas anunciadas por Rockstar",
           "date": "Rockstar Games · rockstargames.com/VI", "platforms": "Rockstar Games · rockstargames.com/VI", "lang": "Ficha de PlayStation Store y Xbox Store",
           "trailers": "Rockstar Games · tráileres oficiales"}

# ---------------------------------------------------------------- imágenes fijas (caché)
_IMG = {}; _IMG_ORDER = []
def load_img(path, maxw=2400):
    if path in _IMG: return _IMG[path]
    im = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(path))
    if im.width() > maxw:
        s = maxw / im.width(); w2, h2 = int(im.width() * s), int(im.height() * s)
        surf = skia.Surface(w2, h2); surf.getCanvas().drawImageRect(im, skia.Rect.MakeWH(w2, h2), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
        im = surf.makeImageSnapshot()
    _IMG[path] = im; _IMG_ORDER.append(path)
    if len(_IMG_ORDER) > 60: _IMG.pop(_IMG_ORDER.pop(0), None)
    return im

def thumb(name, w=480):
    key = ("thumb", name, w)
    if key in _IMG: return _IMG[key]
    im = load_img(_index()[name], maxw=w * 2)
    s = w / im.width(); w2, h2 = int(im.width() * s), int(im.height() * s)
    surf = skia.Surface(w2, h2); surf.getCanvas().drawImageRect(im, skia.Rect.MakeWH(w2, h2), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    _IMG[key] = surf.makeImageSnapshot(); return _IMG[key]

# ---------------------------------------------------------------- vídeo (ffmpeg → RGBA)
class Clip:
    """Lector secuencial de un tramo de vídeo. get(i) devuelve el fotograma i (desde t0) como skia.Image."""
    def __init__(self, path, t0, dur, size):
        self.path, self.t0, self.dur, self.size = path, max(0.0, t0), dur + 1.0, size
        self.p = None; self.i = -1; self.img = None; self._open()
    def _open(self):
        w, h = self.size
        vf = f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=bicubic,crop={w}:{h},fps={FPS},format=rgba"
        self.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "fatal", "-ss", f"{self.t0:.3f}", "-i", self.path, "-t", f"{self.dur:.3f}", "-an",
                                   "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE, bufsize=w * h * 4 * 2)
        self.i = -1; self.eof = False
    def get(self, i):
        w, h = self.size
        if i < self.i: self.close(); self._open()
        while self.i < i and not self.eof:
            buf = self.p.stdout.read(w * h * 4)
            if len(buf) < w * h * 4: self.eof = True; break
            self.i += 1
            if self.i >= i:
                arr = np.frombuffer(buf, np.uint8).reshape(h, w, 4)
                self.img = skia.Image.fromarray(arr, colorType=skia.ColorType.kRGBA_8888_ColorType)
        return self.img
    def close(self):
        if self.p:
            try: self.p.stdout.close(); self.p.kill(); self.p.wait(timeout=2)
            except Exception: pass
        self.p = None

# ---------------------------------------------------------------- tabla de planos (tiempos globales)
_T = {}
def _word_time(sents, frag, after):
    """Inicio (absoluto) de la palabra donde empieza `frag`, buscando a partir del instante `after`."""
    for s in sents:
        i = s["text"].find(frag)
        while i >= 0:
            ws = s.get("words")
            k = min(len(ws) - 1, s["text"][:i].count(" ")) if ws else None
            t = ws[k][1] if ws else s["start"]
            if t >= after - 1e-6: return t, (ws[k][0] if ws else frag)
            i = s["text"].find(frag, i + 1)
    return None, None

def table(ctx):
    if "shots" in _T: return _T
    V, tl = ctx.V, ctx.tl; shots = []; beats = []; chapters = []
    for bi, (b, bd) in enumerate(zip(V["beats"], tl["beats"])):
        beats.append(dict(b=b, bd=bd))
        if b.get("chapter"): chapters.append((bd["start"] + 0.05, b["chapter"]))
        last = bd["start"]
        for j, sh in enumerate(b.get("shots", [])):
            if sh["anchor"] is None: t0 = bd["start"]; wt = None; word = None
            else:
                wt, word = _word_time(bd["sents"], sh["anchor"], last)
                if wt is None: raise ValueError(f"ancla «{sh['anchor']}» no encontrada en el beat {bi}")
                t0 = wt - LEAD
            shots.append(dict(sh, t0=t0, beat=bi, word_t=wt, word=word, k=len(shots)))
            last = wt + 0.01 if wt is not None else bd["start"]
    shots.sort(key=lambda s: s["t0"])
    for i, s in enumerate(shots): s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else tl["total"]
    _T.update(shots=shots, starts=[s["t0"] for s in shots], beats=beats, chapters=chapters,
              bstarts=[x["bd"]["start"] for x in beats], words=[w for x in beats for s in x["bd"]["sents"] for w in s.get("words", [])])
    return _T

def sync_report(ctx):
    """Control de sincronía imagen ↔ palabra: desfase entre cada corte y el inicio de la palabra que lo motiva."""
    T = table(ctx); rows = []
    for s in T["shots"]:
        if s["word_t"] is None: continue
        rows.append(dict(t=round(s["t0"], 3), palabra=s["word"], ancla=s["anchor"], fuente=s["src"], desfase=round(s["t0"] - s["word_t"], 3)))
    return rows

# ---------------------------------------------------------------- dibujo de un plano
def _cover(c, img, z, fx, fy, a=1.0, cf=None):
    iw, ih = img.width(), img.height(); s = max(W / iw, H / ih) * z
    dw, dh = iw * s, ih * s
    # el punto (fx, fy) de la imagen queda en (fx, fy) del cuadro, sin dejar bordes vacíos
    x = min(0, max(W - dw, W * fx - dw * fx)); y = min(0, max(H - dh, H * fy - dh * fy))
    p = skia.Paint(); p.setAlphaf(a)
    if cf is not None: p.setColorFilter(cf)
    c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, dw, dh), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), p)

_CL = {}
def _bad(T):
    for a, b in BAD:
        if a <= T < b: return True
    return False

_CUTS = {}
# cortes que la detección automática no ve (fundidos, rótulos que aparecen sin corte), medidos a mano
MANUAL_CUTS = {"GTAVI_Launch_Trailer": [22.35, 22.95, 25.0, 26.35, 47.45, 50.9], "GTAVI_Official_Cover_Art_Landscape": [7.0, 15.4, 21.2], "GTAVI_Pre-Load_Now": [15.45, 17.55, 18.6, 19.75]}
def cuts_for(path):
    """Cortes de escena del material (dos pasadas de detección, umbral 0,22 y 0,10, más los cortes medidos a mano)."""
    if path not in _CUTS:
        b = os.path.splitext(os.path.basename(path))[0]; cs = set(MANUAL_CUTS.get(b, []))
        for d in ("cuts", "cuts2"):
            f = f"{SCR}/{d}/{b}.txt"
            if os.path.exists(f): cs |= {float(x) for x in open(f).read().split()}
        _CUTS[path] = sorted(cs)
    return _CUTS[path]

def src_window(sh):
    """(archivo, inicio local, duración útil) del plano de vídeo: termina en el siguiente corte de escena del
    material, en un tramo prohibido o al final del tramo extraído. Si el inicio cae justo antes de un corte, salta a él."""
    if "_win" in sh: return sh["_win"]
    k, v = sh["src"].split(":", 1); path = asset_path(sh["src"])
    T0 = float(v) if k in ("e", "l", "p") else float(sh.get("st", 0.0)) if k == "k" else float(v.split("@")[1]) if k == "x" else 0.0
    off = 0.0; limit = _clip_meta(path)["dur"] - 0.1
    if k == "x":
        xb = XBAD.get(v.split("@")[0], [])
        for a, b in xb:
            if a <= T0 < b: T0 = b + 0.05
        for a, b in xb:
            if a > T0: limit = min(limit, a - 0.05)
    if k == "e":
        r = next(r for r, (a, b) in EL_RANGES.items() if a <= T0 < b); ra, rb = EL_RANGES[r]; off = ra; limit = rb - ra - 0.1
        for a, b in BAD:
            if a <= T0 < b: T0 = b + 0.05          # el inicio caía en un tramo prohibido
        for a, b in BAD:
            if a > T0: limit = min(limit, a - ra - 0.05)
    loc = T0 - off; cs = cuts_for(path)
    for _ in range(3):
        nxt = next((x for x in cs if x > loc + 0.02), limit + 0.1)
        end = min(nxt - 0.04, limit)
        if end - loc >= 0.8 or nxt > limit: break
        loc = nxt + 0.02     # el inicio estaba pegado a un corte: empezar en el plano siguiente
    sh["_win"] = (path, loc, max(0.4, end - loc)); return sh["_win"]

_FR = {}
def clip_frames(path, size):
    """Vídeos de personaje (1-1,5 s, pensados para repetirse en bucle): todos los fotogramas en memoria."""
    key = (path, size)
    if key not in _FR:
        cl = Clip(path, 0.0, 5.0, size); frames = []
        while True:
            im = cl.get(len(frames))
            if im is None or cl.eof: break
            frames.append(im)
        cl.close(); _FR.clear(); _FR[key] = frames
    return _FR[key]

def footage(c, sh, tau, d, slot="main"):
    """Dibuja el material de un plano a tau segundos de su inicio (d = duración del plano)."""
    src = sh["src"]; k, v = src.split(":", 1)
    if k == "g": return
    # renovación del encuadre en planos largos: segmentos de ≤ MAXD con otro encuadre
    nseg = max(1, int(math.ceil(d / MAXD))); seg = min(nseg - 1, int(tau / (d / nseg))) if nseg > 1 else 0
    tl_ = (tau - seg * d / nseg) / (d / nseg)
    z0, z1 = sh.get("z", (1.0, 1.06) if k in ("s", "u", "v", "a") else (1.0, 1.03))
    fx, fy = sh.get("f", (0.5, 0.5))
    if seg % 2 == 1:   # encuadre alternativo: más cerrado y desplazado
        z0, z1 = z1 * 1.12, z1 * 1.2; fx, fy = (0.5 + (0.18 if (sh["k"] + seg) % 2 else -0.18), 0.45)
    elif seg >= 2: z0, z1 = z1, z1 * 1.08
    z = lerp(z0, z1, ease_io(clamp(tl_)) if nseg > 1 else clamp(tau / max(d, 0.1)))
    if k in ("s", "u", "v", "a"):
        _cover(c, load_img(asset_path(src)), z, fx, fy); return
    path = asset_path(src)
    if k == "c":
        info = _clip_meta(path); sq = info["w"] == info["h"]
        frames = clip_frames(path, (1080, 1080) if sq else (W, H))
        if not frames: return
        img = frames[int(tau * sh.get("speed", 0.75) * FPS) % len(frames)]
        if sq:
            bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(40, 40))
            c.drawImageRect(img, skia.Rect.MakeXYWH(-120, -560, W + 240, W + 240), skia.SamplingOptions(skia.FilterMode.kLinear), bg)
            rect(c, 0, 0, W, H, "#0A0A12", 0.45)
            s2 = 1.0 + 0.04 * clamp(tau / max(d, 0.1)); side = 1000 * s2; x = W - side - 70; y = (H - side) / 2
            rect(c, x + 14, y + 18, side, side, "#000000", 0.45, r=26, blur=18)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, side, side), 26, 26), True)
            c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, side, side), skia.SamplingOptions(skia.FilterMode.kLinear)); c.restore()
        else:
            _cover(c, img, z, fx, fy)
        return
    # e / l / p / k / x: vídeo 16:9 dentro de su plano de origen (sin cruzar cortes de escena ni tramos prohibidos)
    path, loc, Ls = src_window(sh)
    sp = sh.get("speed") or max(0.5, min(1.0, Ls / max(d, 0.1)))
    tt = (tau * sp) % Ls
    clip = _CL.get(slot)
    if clip is None or clip.path != path or abs(clip.t0 - loc) > 1e-3:
        if clip: clip.close()
        clip = Clip(path, loc, Ls + 0.2, (W, H)); _CL[slot] = clip
    img = clip.get(int(tt * FPS))
    if img is not None: _cover(c, img, z, fx, fy)

_META = {}
def _clip_meta(path):
    if path not in _META:
        o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,duration", "-of", "json", path], capture_output=True, text=True)
        st = json.loads(o.stdout)["streams"][0]; _META[path] = dict(w=int(st["width"]), h=int(st["height"]), dur=float(st.get("duration", 1.0)))
    return _META[path]

# ---------------------------------------------------------------- rótulos
def chip(c, x, y, txt, a=1.0, size=21, col=YEL):
    if a <= 0 or not txt: return 0
    f = font("ovmonomd", size); w = text_w(txt, f, 0.5) + size * 1.6; h = size * 1.75
    rect(c, x, y, w, h, "#000000", 0.62 * a, r=5); rect(c, x, y, 5, h, col, a)
    draw_text(c, txt, x + size * 0.85, y + h * 0.69, "ovmonomd", size, "#F3F0E9", 0.95 * a, tracking=0.5)
    return w

TAGS = {"OFICIAL": (GRN, "DATO OFICIAL"), "INTERPRETACIÓN": (YEL, "NUESTRA INTERPRETACIÓN"), "ULTIMATE": ("#B57CFF", "EXCLUSIVO EDICIÓN ULTIMATE"),
        "RESERVA": ("#36E3FF", "BONO POR RESERVAR")}
def tag(c, x, y, kind, a=1.0, size=26):
    if a <= 0 or kind not in TAGS: return
    col, txt = TAGS[kind]; f = font("ovmono", size); w = text_w(txt, f, 1) + size * 2.2; h = size * 1.7
    x -= w
    rect(c, x, y, w, h, "#0B0C10", 0.82 * a, r=h / 2); rect(c, x, y, w, h, col, a, r=h / 2, stroke=3)
    circle(c, x + size * 0.95, y + h / 2, size * 0.32, col, a)
    draw_text(c, txt, x + size * 1.55, y + h / 2 + size * 0.36, "ovmono", size, col, a, tracking=1)

def lower_third(c, name, role, p, x=90, y=690):
    if p <= 0: return
    e = ease_out(p); f1 = font("anton", 92); w = max(text_w(name, f1) + 70, text_w(role, font("intersb", 34)) + 70)
    c.save(); c.translate(-(1 - e) * 120, 0)
    rect(c, x, y, w, 118, "#0B0C10", 0.86 * e, r=10); rect(c, x, y, 10, 186, YEL, e)
    draw_text(c, name, x + 34, y + 98, "anton", 92, "#FFFFFF", e)
    rect(c, x, y + 124, w * 0.8, 62, YEL, e, r=8); draw_text(c, role, x + 34, y + 167, "intersb", 34, "#16181B", e)
    c.restore()

def quote_box(c, txt, p, src="Ficha oficial · rockstargames.com/VI"):
    if p <= 0: return
    e = ease_out(p); maxw = 1180; lines = wrap(txt, "dmserif", 66, maxw)
    h = 70 * len(lines) + 120; x = 90; y = 470 - h / 2
    c.save(); c.translate(0, (1 - e) * 40)
    rect(c, x, y, maxw + 90, h, "#0B0C10", 0.80 * e, r=14); rect(c, x, y, 8, h, YEL, e)
    for i, ln in enumerate(lines): draw_text(c, ln, x + 46, y + 92 + i * 70, "dmserif", 66, "#FFFFFF", e)
    draw_text(c, src, x + 48, y + h - 26, "ovmonomd", 22, YEL, 0.9 * e, tracking=1)
    c.restore()

def big_label(c, txt, p, y=170, col="#FFFFFF", size=120):
    if p <= 0: return
    e = ease_out_back(p); f = font("anton", size); w = text_w(txt, f, 2)
    c.save(); c.translate(90, y); c.scale(e, e)
    draw_text(c, txt, 6, 6, "anton", size, "#000000", 0.5 * clamp(p * 2), tracking=2)
    draw_text(c, txt, 0, 0, "anton", size, col, clamp(p * 2), tracking=2)
    c.restore()

def act_label(c, txt, p):
    if p <= 0: return
    e = ease_out_back(p); f = font("anton", 64); w = text_w(txt, f, 3) + 60
    c.save(); c.translate(90 + w / 2, 222); c.scale(e, e); c.translate(-(90 + w / 2), -222)
    rect(c, 90, 180, w, 84, YEL, clamp(p * 2), r=6); draw_text(c, txt, 120, 249, "anton", 64, "#16181B", clamp(p * 2), tracking=3)
    c.restore()

def stamp_label(c, txt, p):
    if p <= 0: return
    e = ease_out_back(p, 2.2); c.save(); c.translate(W / 2, H * 0.42); c.rotate(-6); c.scale(2.2 - 1.2 * e, 2.2 - 1.2 * e)
    f = font("ovblk", 70); w = text_w(txt, f, 3) + 80
    rect(c, -w / 2, -70, w, 120, "#FF4A3D", clamp(p * 3), r=10, stroke=8); draw_text(c, txt, 0, 18, "ovblk", 70, "#FF4A3D", clamp(p * 3), align="center", tracking=3)
    c.restore()

# ---------------------------------------------------------------- subtítulos dinámicos
_SUB = {}
def _sub_chunks(ctx):
    if "c" in _SUB: return _SUB["c"]
    out = []
    for b in ctx.tl["beats"]:
        for s in b["sents"]:
            ws = s.get("words") or []
            cur = []; n = 0
            for w in ws:
                if cur and n + len(w[0]) + 1 > 44: out.append(cur); cur = []; n = 0
                cur.append(w); n += len(w[0]) + 1
            if cur: out.append(cur)
    _SUB["c"] = out; _SUB["st"] = [ch[0][1] for ch in out]; return out

def subtitles(c, gt, ctx):
    ch = _sub_chunks(ctx); st = _SUB["st"]; i = bisect.bisect_right(st, gt + 0.02) - 1
    if i < 0: return
    words = ch[i]; end = words[-1][2]; nxt = st[i + 1] if i + 1 < len(st) else end + 1
    if gt > max(end + 0.35, min(nxt - 0.05, end + 0.8)): return
    txt = " ".join(w[0] for w in words); f = font("interb", 46); tw = text_w(txt, f)
    x = W / 2 - tw / 2; y = H - 96
    rect(c, x - 26, y - 50, tw + 52, 70, "#000000", 0.62, r=12)
    xx = x
    for w in words:
        wd = text_w(w[0] + " ", f); on = w[1] - 0.03 <= gt
        draw_text(c, w[0], xx, y, "interb", 46, YEL if (on and gt < w[2] + 0.12) else "#FFFFFF", 1.0 if on else 0.82)
        xx += wd

# ---------------------------------------------------------------- gráficos propios (g:)
def _panel_bg(c, name="Vice_City_27", dark=0.62):
    _cover(c, load_img(_index()[name]), 1.08, 0.5, 0.5)
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(22, 22)); c.saveLayer(skia.Rect.MakeWH(W, H), p); c.restore()
    rect(c, 0, 0, W, H, "#07080C", dark)

def _img_card(c, img, x, y, w, h, a=1.0, r=14, border=None):
    if a <= 0: return
    rect(c, x + 10, y + 14, w, h, "#000000", 0.4 * a, r=r, blur=14)
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), True)
    iw, ih = img.width(), img.height(); s = max(w / iw, h / ih)
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(img, skia.Rect.MakeXYWH(x + (w - iw * s) / 2, y + (h - ih * s) / 2, iw * s, ih * s), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), p)
    c.restore()
    if border: rect(c, x, y, w, h, border, a, r=r, stroke=4)

def g_trailers(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_14")
    items = [("TRÁILER 1", "DICIEMBRE 2023", None), ("TRÁILER 2", "MAYO 2025", None), ("TRÁILER DE LANZAMIENTO", "OCTUBRE 2026", "l")]
    for i, (a, b, kind) in enumerate(items):
        p = ease_out_back(prog(t, 0.08 * i, 0.08 * i + 0.4)); x = 140 + i * 560; y = 300
        c.save(); c.translate(x + 250, y + 200); c.scale(p, p); c.translate(-(x + 250), -(y + 200))
        rect(c, x, y, 500, 300, "#11131A", 0.95, r=16); rect(c, x, y, 500, 300, YEL if kind else "#FFFFFF", 0.9, r=16, stroke=4)
        if kind:
            fr = _still_from_video(f"{RM}/GTAVI_Launch_Trailer.mp4", 25.2); _img_card(c, fr, x + 12, y + 12, 476, 276, 1, r=10)
            rect(c, x + 12, y + 12, 476, 276, "#000000", 0.35, r=10)
        else:
            icon(c, "film", x + 250, y + 140, 80, "#FFFFFF", 0.85)
        draw_text(c, a, x + 250, y + 370, "anton", 46, "#FFFFFF", 1, align="center", tracking=1)
        draw_text(c, b, x + 250, y + 420, "ovmono", 30, YEL, 1, align="center", tracking=2)
        c.restore()
    big_label(c, "3 TRÁILERES", prog(t, 0.2, 0.6), y=200, size=110)

_VS = {}
def _still_from_video(path, t, size=(960, 540)):
    key = (path, t)
    if key not in _VS:
        cl = Clip(path, t, 0.2, size); img = cl.get(0); cl.close(); _VS[key] = img
    return _VS[key]

_MOS = {}
def g_mosaic(c, t, d, sh, ctx):
    if "img" not in _MOS:
        names = sorted(n for n, p in _index().items() if "/GTAVI_Screenshots/" in p)
        cols, rows = 23, 6; tw, th = W / cols, (W / cols) * 9 / 16
        surf = skia.Surface(W, int(th * rows)); cc = surf.getCanvas(); cc.clear(skia.ColorBLACK)
        for i, n in enumerate(names[:cols * rows]):
            im = thumb(n, 160); x, y = (i % cols) * tw, (i // cols) * th
            cc.drawImageRect(im, skia.Rect.MakeXYWH(x + 1, y + 1, tw - 2, th - 2), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
        _MOS["img"] = surf.makeImageSnapshot(); _MOS["n"] = len(names); _MOS["th"] = th
    img = _MOS["img"]; s = 1.0 + 0.06 * clamp(t / max(d, 0.1)); oy = (H - img.height()) / 2
    c.save(); c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
    n_vis = int(_MOS["n"] * ease_out(prog(t, 0, 0.9)))
    cols = 23; th = _MOS["th"]; tw = W / cols
    for i in range(n_vis):
        x, y = (i % cols) * tw, (i // cols) * th
        c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, tw, th), skia.Rect.MakeXYWH(x, y + oy, tw, th), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint())
    c.restore()
    rect(c, 0, 0, W, H, "#000000", 0.35)
    n = int(138 * ease_out(prog(t, 0, 0.9)))
    draw_text(c, f"{n}", W / 2, H / 2 + 80, "anton", 260, YEL, 1, align="center")
    draw_text(c, "CAPTURAS OFICIALES", W / 2, H / 2 + 170, "ovblk", 54, "#FFFFFF", 1, align="center", tracking=4)

def g_nospoil(c, t, d, sh, ctx):
    _panel_bg(c, "Jason_and_Lucia_16", 0.5)
    for i, txt in enumerate(["0 MISIONES", "0 FINALES", "0 FILTRACIONES"]):
        p = ease_out_back(prog(t, 0.12 * i, 0.12 * i + 0.35), 2.0)
        c.save(); c.translate(W / 2, 330 + i * 170); c.rotate(-4 + 4 * i); c.scale(1.6 - 0.6 * p, 1.6 - 0.6 * p)
        f = font("ovblk", 92); w = text_w(txt, f, 4) + 90
        rect(c, -w / 2, -88, w, 130, "#FF4A3D", clamp(p * 2), r=12, stroke=9)
        draw_text(c, txt, 0, 12, "ovblk", 92, "#FF4A3D", clamp(p * 2), align="center", tracking=4); c.restore()

def g_sting(c, t, d, sh, ctx):
    class I: pass
    K.brand_sting(c, t, I(), ctx)

def g_title(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_14", 0.55)
    p = ease_out(prog(t, 0, 0.5))
    draw_text(c, "GTA 6", W / 2, 360, "anton", 170, YEL, p, align="center", tracking=4)
    draw_text(c, "TODO LO QUE ROCKSTAR HA ENSEÑADO", W / 2, 470, "anton", 92, "#FFFFFF", p, align="center", tracking=2)
    q = ease_out_back(prog(t, 0.35, 0.8))
    rect(c, W / 2 - 300, 540, 600, 80, "#FF4A3D", q, r=40); draw_text(c, "SIN SPOILERS", W / 2, 597, "ovblk", 48, "#FFFFFF", q, align="center", tracking=4)
    draw_text(c, "una guía de Sal y Asfalto · solo material oficial", W / 2, 690, "intersb", 34, "#FFFFFF", 0.85 * p, align="center")

def g_media(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_11", 0.66)
    draw_text(c, "MATERIAL OFICIAL PARA DESCARGAR Y COMPARTIR", W / 2, 150, "anton", 64, "#FFFFFF", ease_out(prog(t, 0, 0.4)), align="center", tracking=2)
    draw_text(c, "rockstargames.com/VI/downloads", W / 2, 205, "ovmono", 30, YEL, ease_out(prog(t, 0.1, 0.5)), align="center")
    items = [("e", 1136.4, "AN EXTENDED LOOK", "26 min de juego"), ("l", 25.2, "TRÁILER DE LANZAMIENTO", "1:29"), ("p", 19.0, "VÍDEO DE PRECARGA", "0:29"),
             ("s", "Vice_City_05", "138 CAPTURAS", "personas y lugares"), ("a", "Vice_City_Postcard_landscape", "142 ILUSTRACIONES", "fondos y postales"),
             ("u", "ULTIMATE_EDITION_GROTTI_CHEETAH_01", "63 IMÁGENES", "Ultimate y reserva")]
    for i, (k, v, a, b) in enumerate(items):
        p = ease_out_back(prog(t, 0.15 + 0.07 * i, 0.5 + 0.07 * i)); x = 150 + (i % 3) * 560; y = 270 + (i // 3) * 370
        c.save(); c.translate(x + 250, y + 150); c.scale(p, p); c.translate(-(x + 250), -(y + 150))
        if k in ("l", "p"): img = _still_from_video(f"{RM}/GTAVI_Launch_Trailer.mp4" if k == "l" else f"{RM}/GTAVI_Pre-Load_Now.mp4", v)
        elif k == "e": img = _still_from_video(f"{EL}/r3.mp4", v - 994.0)
        else: img = thumb(v, 520)
        _img_card(c, img, x, y, 500, 260, 1, border="#FFFFFF")
        draw_text(c, a, x, y + 305, "anton", 40, "#FFFFFF", 1, tracking=1); draw_text(c, b, x, y + 345, "intersb", 28, YEL, 1)
        c.restore()

def g_legend(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_27", 0.6); st = sh.get("step", 0)
    for i, (kind, txt) in enumerate([("OFICIAL", "Lo dice Rockstar o se ve en su material"), ("INTERPRETACIÓN", "Opinión o lectura de Sal y Asfalto")]):
        if i > st: continue
        p = ease_out_back(prog(t, 0, 0.35)) if i == st else 1.0
        y = 380 + i * 220; c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        tag(c, W / 2 + 420, y - 60, kind, 1, 44)
        draw_text(c, txt, W / 2, y + 90, "intersb", 46, "#FFFFFF", 1, align="center"); c.restore()

CHAPS = ["Lo esencial", "Jason y Lucía", "El reparto", "Leonida", "Un día en Vice City", "Qué puedes hacer", "Cómo se juega", "Vehículos y fauna", "Ediciones", "La música"]
def g_chapters(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_15", 0.7)
    draw_text(c, "10 CAPÍTULOS", 140, 190, "anton", 96, YEL, ease_out(prog(t, 0, 0.3)), tracking=2)
    for i, ch in enumerate(CHAPS):
        p = ease_out(prog(t, 0.05 * i, 0.05 * i + 0.3)); x = 140 + (i // 5) * 820; y = 320 + (i % 5) * 140
        c.save(); c.translate(-(1 - p) * 60, 0)
        rect(c, x, y - 62, 92, 92, YEL, p, r=10); draw_text(c, f"{i + 1}", x + 46, y + 6, "anton", 60, "#16181B", p, align="center")
        draw_text(c, ch.upper(), x + 120, y + 4, "anton", 56, "#FFFFFF", p, tracking=1); c.restore()

def g_date(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_27", 0.5)
    p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, 470); c.scale(p, p)
    rect(c, -520, -250, 1040, 470, "#F3F0E9", 1, r=24); rect(c, -520, -250, 1040, 110, "#FF4A3D", 1, r=24); rect(c, -520, -170, 1040, 30, "#FF4A3D", 1)
    draw_text(c, "JUEVES · NOVIEMBRE 2026", 0, -178, "ovblk", 46, "#FFFFFF", 1, align="center", tracking=3)
    draw_text(c, "19", 0, 120, "anton", 300, "#16181B", 1, align="center"); c.restore()
    q = ease_out(prog(t, 0.4, 0.8))
    draw_text(c, "00:00 · HORA LOCAL DE CADA PAÍS", W / 2, 840, "anton", 70, YEL, q, align="center", tracking=2)

def g_platforms(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_10", 0.55)
    for i, (a, b) in enumerate([("PlayStation 5", "PS5 · PS5 Pro"), ("Xbox Series X|S", "Series X · Series S")]):
        p = ease_out_back(prog(t, 0.12 * i, 0.12 * i + 0.4)); x = W / 2 - 780 + i * 820
        c.save(); c.translate(x + 370, 520); c.scale(p, p); c.translate(-(x + 370), -520)
        rect(c, x, 360, 740, 320, "#0B0C10", 0.88, r=20); rect(c, x, 360, 740, 320, "#FFFFFF", 0.9, r=20, stroke=4)
        draw_text(c, a, x + 370, 520, "anton", 86, "#FFFFFF", 1, align="center"); draw_text(c, b, x + 370, 590, "ovmono", 30, YEL, 1, align="center")
        c.restore()
    draw_text(c, "SOLO EN CONSOLAS DE ESTA GENERACIÓN", W / 2, 820, "anton", 56, "#FFFFFF", ease_out(prog(t, 0.4, 0.8)), align="center", tracking=2)

def g_lang(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_09", 0.55)
    for i, (a, b) in enumerate([("VOCES", "INGLÉS"), ("TEXTOS Y SUBTÍTULOS", "ESPAÑOL")]):
        p = ease_out_back(prog(t, 0.1 * i, 0.1 * i + 0.4)); y = 340 + i * 240
        c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        draw_text(c, a, W / 2, y, "ovmono", 40, "#FFFFFF", 0.9, align="center", tracking=4)
        draw_text(c, b, W / 2, y + 120, "anton", 120, YEL, 1, align="center", tracking=3); c.restore()

def g_claim(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_26", 0.55); st = sh.get("step", 0)
    rows = [("SIN MICROPAGOS", "con dinero real, en el lanzamiento (modo historia)"), ("SIN IA GENERATIVA", "en su desarrollo, según Rockstar North")]
    for i, (a, b) in enumerate(rows):
        if i > st: continue
        p = ease_out_back(prog(t, 0, 0.35)) if i == st else 1.0; y = 400 + i * 250
        c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        rect(c, W / 2 - 720, y - 120, 1440, 210, "#0B0C10", 0.86, r=18); rect(c, W / 2 - 720, y - 120, 14, 210, GRN, 1)
        icon(c, "check", W / 2 - 630, y - 32, 64, GRN, 1); draw_text(c, a, W / 2 - 570, y + 2, "anton", 96, "#FFFFFF", 1, tracking=1)
        draw_text(c, b, W / 2 - 656, y + 62, "intersb", 36, YEL, 1); c.restore()

TL_NODES = [("DIC 2023", "Tráiler 1", "Récords en YouTube"), ("MAY 2025", "Tráiler 2", "70 capturas · 475 M de vistas en 24 h"),
            ("MAY 2025", "Tráiler 2", "475 millones de visualizaciones en 24 h"), ("JUN 2026", "Portada y ediciones", ""),
            ("AGO 2026", "Extended Look", "Estreno en Netflix"), ("OCT 2026", "Tráiler de lanzamiento", ""), ("10 NOV 2026", "Precarga", "")]
def g_timeline(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_27", 0.62); st = sh.get("step", -1)
    pts = ["DIC 2023", "MAY 2025", "JUN 2026", "AGO 2026", "OCT 2026", "10 NOV", "19 NOV"]
    x0, x1, y = 160, W - 160, 300; pr = ease_out(prog(t, 0, 0.5)) if st == -1 else 1.0
    line(c, x0, y, x0 + (x1 - x0) * pr, y, "#FFFFFF", 0.6, 6)
    act = {-1: -1, 0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}[st]
    for i, lab in enumerate(pts):
        x = x0 + (x1 - x0) * i / (len(pts) - 1); on = i <= act; cur = i == act
        r = 26 if cur else 16
        if cur: circle(c, x, y, r + 14 + 6 * pulse(t, 1.0), YEL, 0.3)
        circle(c, x, y, r, YEL if on else ("#FF4A3D" if i == 6 else "#555A66"), 1)
        draw_text(c, lab, x, y - 50, "ovmono", 28 if cur else 24, YEL if cur else "#FFFFFF", 1 if on or i == 6 else 0.6, align="center")
    if st >= 0:
        lab, title, sub = TL_NODES[st]; p = ease_out(prog(t, 0, 0.35))
        img = None
        if st == 3: img = thumb("Official_Cover_Art_landscape", 900)
        elif st == 4: img = _still_from_video(f"{EL}/r3.mp4", 1130.4 - 994.0)
        elif st == 5: img = _still_from_video(f"{RM}/GTAVI_Launch_Trailer.mp4", 25.2)
        elif st == 6: img = _still_from_video(f"{RM}/GTAVI_Pre-Load_Now.mp4", 19.0)
        c.save(); c.translate(0, (1 - p) * 40)
        if img is not None:
            _img_card(c, img, 1000, 420, 760, 428, p, border="#FFFFFF")
            draw_text(c, title.upper(), 160, 560, "anton", 96, "#FFFFFF", p, tracking=1); draw_text(c, sub, 160, 630, "intersb", 40, YEL, p)
        else:
            draw_text(c, title.upper(), W / 2, 600, "anton", 140, "#FFFFFF", p, align="center", tracking=2)
            draw_text(c, sub, W / 2, 690, "intersb", 46, YEL, p, align="center")
            if st == 2: draw_text(c, "475.000.000", W / 2, 840, "anton", 130, YEL, ease_out(prog(t, 0.1, 0.6)), align="center", tracking=3)
        c.restore()

def g_swap(c, t, d, sh, ctx):
    a = load_img(_index()["Jason_Duval_19"]); b = load_img(_index()["Lucia_Caminos_12"])
    k = 0.5 + 0.5 * math.tanh((t - d * 0.5) * 3) ; side = 0 if t < d * 0.5 else 1
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, W / 2, H)); _cover(c, a, 1.08 + 0.04 * clamp(t / d), 0.6, 0.5); c.restore()
    c.save(); c.clipRect(skia.Rect.MakeXYWH(W / 2, 0, W / 2, H)); _cover(c, b, 1.08 + 0.04 * clamp(t / d), 0.4, 0.5); c.restore()
    rect(c, 0 if side else W / 2, 0, W / 2, H, "#000000", 0.55)
    line(c, W / 2, 0, W / 2, H, "#FFFFFF", 0.9, 6)
    circle(c, W / 2, H / 2, 86, YEL, 1)
    for sg in (1, -1):   # flechas de intercambio
        yy = H / 2 - 18 * sg; line(c, W / 2 - 42, yy, W / 2 + 42, yy, "#16181B", 1, 9)
        tip = W / 2 + 42 * sg; draw_poly(c, [(tip + 14 * sg, yy), (tip - 8 * sg, yy - 16), (tip - 8 * sg, yy + 16)], "#16181B", 1)
    draw_text(c, "JASON", W / 4, 160, "anton", 110, "#FFFFFF", 1 if side == 0 else 0.5, align="center", tracking=3)
    draw_text(c, "LUCÍA", W * 3 / 4, 160, "anton", 110, "#FFFFFF", 1 if side == 1 else 0.5, align="center", tracking=3)

def g_poll(c, t, d, sh, ctx):
    a = thumb("Jason_and_Lucia_Beach_landscape", 1600)
    _cover(c, a, 1.05 + 0.04 * clamp(t / d), 0.5, 0.45); rect(c, 0, 0, W, H, "#000000", 0.35)
    p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, 200); c.scale(p, p)
    rect(c, -560, -80, 1120, 130, YEL, 1, r=16); draw_text(c, "PAUSA RÁPIDA", 0, 25, "anton", 96, "#16181B", 1, align="center", tracking=4); c.restore()
    for i, n in enumerate(["JASON", "LUCÍA"]):
        q = ease_out_back(prog(t, 0.3 + 0.15 * i, 0.7 + 0.15 * i)); x = W / 2 - 520 + i * 640
        c.save(); c.translate(x + 200, 850); c.scale(q, q); c.translate(-(x + 200), -850)
        rect(c, x, 780, 400, 130, "#0B0C10", 0.88, r=65); rect(c, x, 780, 400, 130, "#FFFFFF", 1, r=65, stroke=5)
        draw_text(c, n, x + 200, 872, "anton", 84, "#FFFFFF", 1, align="center", tracking=3); c.restore()
    draw_text(c, "¿A QUIÉN ELIGES?", W / 2, 1000, "ovblk", 44, "#FFFFFF", ease_out(prog(t, 0.6, 1.0)), align="center", tracking=3)

CAST = [("Cal_Hampton_landscape", "CAL HAMPTON"), ("Boobie_Ike_landscape", "BOOBIE IKE"), ("DreQuan_Priest_landscape", "DRE'QUAN PRIEST"),
        ("Real_Dimez_landscape", "REAL DIMEZ"), ("Raul_Bautista_landscape", "RAÚL BAUTISTA"), ("Brian_Heder_landscape", "BRIAN HEDER")]
def g_cast(c, t, d, sh, ctx):
    rect(c, 0, 0, W, H, "#0B0C10", 1)
    for i, (n, lab) in enumerate(CAST):
        p = ease_out_back(prog(t, 0.08 * i, 0.08 * i + 0.4)); x = 60 + (i % 3) * 610; y = 140 + (i // 3) * 450
        c.save(); c.translate(x + 290, y + 170); c.scale(p, p); c.translate(-(x + 290), -(y + 170))
        _img_card(c, thumb(n, 700), x, y, 580, 326, 1, border="#FFFFFF")
        draw_text(c, lab, x, y + 385, "anton", 52, "#FFFFFF", 1, tracking=1); c.restore()
    draw_text(c, "EL REPARTO OFICIAL", W / 2, 90, "anton", 64, YEL, ease_out(prog(t, 0, 0.3)), align="center", tracking=3)

# mapa oficial de Leonida (descarga gratuita de Rockstar el día del lanzamiento): si está en RM/mapa_oficial/, sustituye a la representación sobre Florida
MAP_OFICIAL = next(iter(sorted(glob.glob(f"{RM}/mapa_oficial/*.jpg") + glob.glob(f"{RM}/mapa_oficial/*.png"))), None)
if MAP_OFICIAL: GFX_SRC["map"] = "Rockstar Games · mapa oficial de Leonida (descarga gratuita, rockstargames.com/VI)"
def g_map(c, t, d, sh, ctx):
    if MAP_OFICIAL:
        img = load_img(MAP_OFICIAL, maxw=3200); p = ease_io(prog(t, 0, d))
        rect(c, 0, 0, W, H, "#0B0C10", 1)
        # el mapa entero a la vista (sin recortar) y acercamiento lento hacia Vice City (sureste)
        iw, ih = img.width(), img.height(); s0 = min(W / iw, (H - 40) / ih); s = s0 * lerp(1.0, 1.35, p)
        fx, fy = sh.get("f", (0.72, 0.78)); dw, dh = iw * s, ih * s
        x = W / 2 - dw * lerp(0.5, fx, p) + lerp(0, W * (fx - 0.5) * 0.5, p); y = H / 2 - dh * lerp(0.5, fy, p) + lerp(0, H * (fy - 0.5) * 0.5, p)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, dw, dh), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
        rect(c, 0, 140, W, 120, "#000000", 0.55)
        draw_text(c, "EL MAPA OFICIAL DE LEONIDA", 90, 225, "anton", 76, "#FFFFFF", 1, tracking=2)
        return
    from videos import v04
    p = ease_io(prog(t, 0, d)); v04.draw_map(c, W, H, (-82.4, 27.4, 1500 - 160 * p, 66, 0), t, visited=[s["key"] for s in v04.STOPS], labels=True)
    rect(c, 0, 90, W, 120, "#000000", 0.5)
    draw_text(c, "LEONIDA SE INSPIRA EN FLORIDA", 90, 175, "anton", 76, "#FFFFFF", 1, tracking=2)
    rect(c, 90, H - 190, 1080, 58, "#FFB000", 1, r=8)
    draw_text(c, "REPRESENTACIÓN APROXIMADA · NO ES EL MAPA DEL JUEGO", 115, H - 150, "ovmono", 28, "#16181B", 1, tracking=1)

PCS = ["Vice_City_Postcard_landscape", "Leonida_Keys_Postcard_landscape", "Grassrivers_Postcard_landscape", "Port_Gellhorn_Postcard_landscape",
       "Ambrosia_Postcard_landscape", "Mount_Kalaga_National_Park_Postcard_landscape"]
def g_postcards(c, t, d, sh, ctx):
    rect(c, 0, 0, W, H, "#1A1530", 1)
    for i, n in enumerate(PCS):
        p = ease_out_back(prog(t, 0.08 * i, 0.08 * i + 0.45)); x = 70 + (i % 3) * 600; y = 120 + (i // 3) * 450
        rot = (-3, 2, -2, 3, -1, 2)[i]
        c.save(); c.translate(x + 280, y + 180); c.rotate(rot * p); c.scale(p, p); c.translate(-(x + 280), -(y + 180))
        _img_card(c, thumb(n, 720), x, y, 560, 360, 1, r=6); c.restore()
    if sh.get("step", 0) == 1:
        q = ease_out_back(prog(t, 0.3, 0.7)); c.save(); c.translate(W / 2, H / 2); c.scale(q, q)
        rect(c, -520, -90, 1040, 160, "#0B0C10", 0.9, r=16); draw_text(c, "UN ESTADO ENTERO", 0, 30, "anton", 110, YEL, 1, align="center", tracking=3); c.restore()

def g_el_card(c, t, d, sh, ctx):
    img = _still_from_video(f"{EL}/r3.mp4", 1131.0 - 994.0, (1920, 1080)); _cover(c, img, 1.04 + 0.03 * clamp(t / d), 0.5, 0.5)
    rect(c, 0, 0, W, H, "#000000", 0.6); st = sh.get("step", 0); p = ease_out(prog(t, 0, 0.4))
    if st == 0:
        draw_text(c, "AN EXTENDED LOOK", W / 2, 470, "anton", 150, "#FFFFFF", p, align="center", tracking=4)
        draw_text(c, "26 MINUTOS · 27/08/2026 · ESTRENO EN NETFLIX, LUEGO YOUTUBE Y WEB", W / 2, 560, "ovmono", 34, YEL, p, align="center", tracking=1)
    else:
        draw_text(c, "DÍA DEL ESTRENO", W / 2, 420, "ovmono", 40, YEL, p, align="center", tracking=4)
        draw_text(c, "NETFLIX Y TWITCH,", W / 2, 540, "anton", 120, "#FFFFFF", p, align="center", tracking=2)
        draw_text(c, "CON PROBLEMAS TÉCNICOS", W / 2, 670, "anton", 120, "#FFFFFF", p, align="center", tracking=2)
        chip(c, W / 2 - 330, 760, "The Independent y PC Gamer, 27/08/2026", p, 26)

def g_profile(c, t, d, sh, ctx):
    _panel_bg(c, "Jason_and_Lucia_06", 0.62); st = sh.get("step", 0)
    draw_text(c, "PERFIL CRIMINAL", W / 2, 260, "anton", 120, "#FFFFFF", 1, align="center", tracking=4)
    x0, x1, y = 360, W - 360, 520; line(c, x0, y, x1, y, "#FFFFFF", 0.5, 10)
    rr = skia.Paint(); rr.setShader(skia.GradientShader.MakeLinear([(x0, y), (x1, y)], [hexc(GRN), hexc(YEL), hexc("#FF4A3D")])); rr.setStrokeWidth(10); rr.setStyle(skia.Paint.kStroke_Style); rr.setAntiAlias(True)
    c.drawLine(x0, y, x1, y, rr)
    k = 0.15 if st == 0 else lerp(0.15, 0.88, ease_io(prog(t, 0, 1.0)))
    circle(c, lerp(x0, x1, k), y, 30, "#FFFFFF", 1)
    draw_text(c, "¿PROFESIONAL?", x0, y + 100, "anton", 60, GRN, 1); draw_text(c, "¿DEMASIADO VIOLENTO?", x1, y + 100, "anton", 60, "#FF4A3D", 1, align="right")
    rect(c, W / 2 - 520, 800, 1040, 58, "#FFB000", 1, r=8)
    draw_text(c, "REPRESENTACIÓN GRÁFICA · NO ES UNA IMAGEN DEL JUEGO", W / 2, 840, "ovmono", 28, "#16181B", 1, align="center")

def g_editions(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_26", 0.62); st = sh.get("step", 0)
    if st == 0:
        cols = [("ESTÁNDAR", "El juego", "#FFFFFF"), ("ULTIMATE", "El juego + contenido exclusivo", "#B57CFF")]
        for i, (a, b, col) in enumerate(cols):
            p = ease_out_back(prog(t, 0.1 * i, 0.1 * i + 0.4)); x = W / 2 - 800 + i * 820
            c.save(); c.translate(x + 390, 520); c.scale(p, p); c.translate(-(x + 390), -520)
            rect(c, x, 330, 780, 380, "#0B0C10", 0.88, r=20); rect(c, x, 330, 780, 380, col, 1, r=20, stroke=5)
            draw_text(c, a, x + 390, 480, "anton", 110, col, 1, align="center", tracking=3); draw_text(c, b, x + 390, 580, "intersb", 40, "#FFFFFF", 1, align="center")
            c.restore()
        draw_text(c, "TATUAJES · PELUQUERÍA · TIENDA · COCHES · LANCHA → SOLO ULTIMATE", W / 2, 840, "ovmono", 30, YEL, ease_out(prog(t, 0.5, 0.9)), align="center")
    else:
        p = ease_out_back(prog(t, 0, 0.4)); c.save(); c.translate(W / 2, H / 2); c.scale(p, p)
        draw_text(c, "COMPRUÉBALO", 0, -40, "anton", 150, "#FFFFFF", 1, align="center", tracking=3)
        draw_text(c, "ANTES DE PAGAR", 0, 120, "anton", 150, YEL, 1, align="center", tracking=3); c.restore()

def g_mute(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_13", 0.62)
    p = ease_out_back(prog(t, 0, 0.4)); c.save(); c.translate(W / 2, 400); c.scale(p, p)
    circle(c, 0, 0, 150, "#0B0C10", 0.9); circle(c, 0, 0, 150, "#FFFFFF", 1, stroke=6)
    draw_poly(c, [(-70, -30), (-30, -30), (20, -80), (20, 80), (-30, 30), (-70, 30)], "#FFFFFF", 1)
    line(c, 50, -50, 110, 50, "#FF4A3D", 1, 14); line(c, 110, -50, 50, 50, "#FF4A3D", 1, 14); c.restore()
    draw_text(c, "AUDIO OFICIAL SILENCIADO", W / 2, 680, "anton", 92, "#FFFFFF", ease_out(prog(t, 0.2, 0.6)), align="center", tracking=2)
    draw_text(c, "Toda la música de este vídeo es original de Sal y Asfalto", W / 2, 760, "intersb", 42, YEL, ease_out(prog(t, 0.4, 0.8)), align="center")

def g_unknown(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_08", 0.6); st = sh.get("step", 0)
    rows = [("MODO ONLINE", "Rockstar prefirió no hablar de él"), ("VERSIÓN PARA PC", "Sin anunciar por ahora")]
    for i, (a, b) in enumerate(rows):
        if i > st: continue
        p = ease_out_back(prog(t, 0, 0.35)) if i == st else 1.0; y = 400 + i * 250
        c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        rect(c, W / 2 - 720, y - 120, 1440, 210, "#0B0C10", 0.86, r=18); rect(c, W / 2 - 720, y - 120, 14, 210, "#FFB000", 1)
        draw_text(c, "? " + a, W / 2 - 660, y + 2, "anton", 96, "#FFFFFF", 1, tracking=1)
        draw_text(c, b, W / 2 - 656, y + 62, "intersb", 36, YEL, 1); c.restore()

def g_subscribe(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_27", 0.5)
    p = ease_out_back(prog(t, 0, 0.45)); c.save(); c.translate(W / 2, 430); c.scale(p, p); draw_badge(c, 0, 0, 150, t=t); c.restore()
    q = ease_out_back(prog(t, 0.25, 0.7)); c.save(); c.translate(W / 2, 720); c.scale(q, q)
    rect(c, -420, -70, 840, 130, "#FF4A3D", 1, r=65); draw_text(c, "SUSCRÍBETE", 0, 28, "anton", 96, "#FFFFFF", 1, align="center", tracking=4); c.restore()
    draw_text(c, "Guías de GTA 6 sin spoilers, toda la semana", W / 2, 860, "intersb", 42, "#FFFFFF", ease_out(prog(t, 0.5, 0.9)), align="center")

def g_end(c, t, d, sh, ctx):
    class I: pass
    K.end_screen(c, t, I(), ctx, title="SIGUIENTE SALIDA", sub="Más guías de GTA 6, sin spoilers")

GFX = {k[2:]: v for k, v in globals().items() if k.startswith("g_")}

# ---------------------------------------------------------------- escena única (todo el vídeo)
_PREV = {}
def scene(c, t, info, ctx):
    gt = info.start + t; T = table(ctx)
    i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    tau = gt - sh["t0"]; d = max(0.05, sh["t1"] - sh["t0"])
    draw_shot(c, sh, tau, d, ctx)
    # fundido corto (4 fotogramas) solo hacia/desde gráficos; entre planos de material, corte seco en la palabra
    if i > 0 and tau < 0.13 and (sh["src"].startswith("g:") or T["shots"][i - 1]["src"].startswith("g:")):
        pv = T["shots"][i - 1]; a = 1 - tau / 0.13
        c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * a)); draw_shot(c, pv, gt - pv["t0"], max(0.05, pv["t1"] - pv["t0"]), ctx, slot="prev"); c.restore()

def draw_shot(c, sh, tau, d, ctx, slot="main"):
    k, v = sh["src"].split(":", 1)
    if k == "g": GFX[v](c, tau, d, sh, ctx)
    else: footage(c, sh, tau, d, slot)
    # rótulos ligados al plano
    if sh.get("card"): lower_third(c, sh["card"][0], sh["card"][1], prog(tau, 0.15, 0.6) * (1 - prog(tau, d - 0.3, d)))
    if sh.get("quote"): quote_box(c, sh["quote"], prog(tau, 0.1, 0.5))
    if sh.get("region"): big_label(c, sh["region"], prog(tau, 0.1, 0.45) * (1 - prog(tau, d - 0.25, d)), y=300, size=130)
    if sh.get("label"): act_label(c, sh["label"], prog(tau, 0.05, 0.35) * (1 - prog(tau, d - 0.2, d)))
    if sh.get("stamp"): stamp_label(c, sh["stamp"], prog(tau, 0.5, 0.8))
    if sh.get("ring"):
        rx, ry, rr = sh["ring"]; p = ease_out_back(prog(tau, 0.2, 0.6))
        circle(c, rx * W, ry * H, rr * W * p + 6 * pulse(tau, 0.8), YEL, 1, stroke=8)
        draw_text(c, "MINIMAPA", rx * W + rr * W + 30, ry * H - 30, "anton", 64, YEL, clamp(p * 2), tracking=2)
    if sh.get("point_chip"):
        p = ease_out(prog(tau, 0.3, 0.8)); y = 200 + 20 * pulse(tau, 0.7)
        draw_text(c, "AQUÍ ARRIBA VA SIEMPRE LA FUENTE", 60, y, "anton", 58, YEL, p, tracking=2)

def overlay(c, gt, ctx):
    T = table(ctx)
    i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    bi = max(0, bisect.bisect_right(T["bstarts"], gt) - 1); b = T["beats"][bi]["b"]
    end_zone = gt > ctx.total - 20.3; sting = sh["src"] == "g:sting"
    if end_zone or sting: return
    # capítulo (rótulo de entrada + etiqueta persistente)
    ch = None
    for st, cc in T["chapters"]:
        if gt >= st: ch = (st, cc)
    if ch and gt < ctx.total - 60:
        st, (n, name) = ch; tt = gt - st
        if tt < 2.6 and not sh["src"].startswith("g:spoiler"):
            p = ease_out(prog(tt, 0, 0.35)) * (1 - prog(tt, 2.2, 2.6))
            rect(c, 0, H / 2 - 120, W * ease_out(prog(tt, 0, 0.35)), 240, "#0B0C10", 0.82 * p)
            draw_text(c, f"{n:02d}", 120, H / 2 + 62, "anton", 200, YEL, p)
            draw_text(c, name, 380, H / 2 + 50, "anton", 130, "#FFFFFF", p, tracking=3)
        else:
            chip(c, 40, 34, f"{n:02d} · {name}", 1, 24, YEL)
    if b.get("spoiler") and sh["src"] != "g:spoiler":
        rect(c, W / 2 - 330, 30, 660, 62, "#FF4A3D", 0.95, r=31); icon(c, "warn", W / 2 - 290, 61, 34, "#FFFFFF", 1)
        draw_text(c, "SPOILER · ESCENAS DE MISIONES", W / 2 + 20, 74, "ovblk", 30, "#FFFFFF", 1, align="center", tracking=2)
    # semáforo del dato
    cert = b.get("cert")
    if cert: tag(c, W - 40, 34, cert, 1, 26)
    # fuente del plano
    k, v = sh["src"].split(":", 1)
    src = source_label(sh["src"]) if k != "g" else GFX_SRC.get(v)
    ytop = 86 if ch else 34
    if src: chip(c, 40, ytop, src, 0.95, 21, YEL if k != "g" else "#9AA0AA")
    if b.get("src_note") and k != "g": chip(c, 40, ytop + 46, "Dato: " + b["src_note"], 0.95, 21, GRN)
    subtitles(c, gt, ctx)
    if gt > 3: K.watermark(c, W, H, 0.5, size=58)

# ---------------------------------------------------------------- miniatura (sin spoilers)
def thumbnail(c):
    Wt, Ht = 1280, 720
    img = load_img(_index()["Jason_and_Lucia_01_landscape"])
    iw, ih = img.width(), img.height(); s = Ht / ih * 1.12; dw = iw * s
    c.drawImageRect(img, skia.Rect.MakeXYWH(Wt - dw + 140, -40, dw, ih * s), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (760, 0)], [skia.Color(10, 8, 20, 245), skia.Color(10, 8, 20, 200), skia.Color(10, 8, 20, 0)], [0, 0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(820, Ht), g)
    draw_text(c, "GTA 6", 48, 170, "anton", 170, YEL, 1, tracking=3)
    draw_text(c, "TODO LO QUE", 50, 290, "anton", 104, "#FFFFFF", 1, tracking=2)
    draw_text(c, "YA SABEMOS", 50, 400, "anton", 104, "#FFFFFF", 1, tracking=2)
    rect(c, 50, 445, 420, 92, "#FF4A3D", 1, r=46); draw_text(c, "SIN SPOILERS", 260, 507, "ovblk", 46, "#FFFFFF", 1, align="center", tracking=3)
    draw_text(c, "SOLO IMÁGENES OFICIALES", 54, 610, "ovmono", 30, "#FFFFFF", 0.9, tracking=2)
    draw_badge(c, 1200, 640, 52)


# ================================================================ gráficos del vídeo post lanzamiento (gp.py)
def _card(c, x, y, w, h, col="#FFFFFF", a=1.0, fill="#0B0C10", fa=0.88):
    rect(c, x, y, w, h, fill, fa * a, r=18); rect(c, x, y, w, h, col, a, r=18, stroke=4)

def _rows(c, t, rows, st, x=W / 2 - 760, y0=330, dy=170, col=YEL):
    """Filas que se acumulan: rows[i] = (título, subtítulo); st = índice de la última visible."""
    for i, (a_, b_) in enumerate(rows):
        if i > st: continue
        p = ease_out_back(prog(t, 0, 0.35)) if i == st else 1.0; y = y0 + i * dy
        c.save(); c.translate(x + 760, y); c.scale(p, p); c.translate(-(x + 760), -y)
        rect(c, x, y - 80, 1520, 145, "#0B0C10", 0.86, r=16); rect(c, x, y - 80, 12, 145, col, 1)
        draw_text(c, a_, x + 50, y + 10, "anton", 74, "#FFFFFF", 1, tracking=1)
        if b_: draw_text(c, b_, x + 52, y + 52, "intersb", 32, col, 1)
        c.restore()

def g_title2(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_14", 0.55); p = ease_out(prog(t, 0, 0.5))
    draw_text(c, "GTA 6 YA SE JUEGA", W / 2, 380, "anton", 150, YEL, p, align="center", tracking=4)
    draw_text(c, "QUÉ DICEN DE SU JUGABILIDAD QUIENES YA LO HAN JUGADO", W / 2, 470, "anton", 62, "#FFFFFF", p, align="center", tracking=2)
    q = ease_out_back(prog(t, 0.35, 0.8))
    rect(c, W / 2 - 420, 540, 840, 80, "#FF4A3D", q, r=40); draw_text(c, "CON AVISO ANTES DE CADA SPOILER", W / 2, 595, "ovblk", 34, "#FFFFFF", q, align="center", tracking=2)

def g_meta(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_10", 0.62); st = sh.get("step", 0)
    p = ease_out_back(prog(t, 0, 0.45)) if st == 0 else 1.0
    c.save(); c.translate(420, H / 2); c.scale(p, p)
    circle(c, 0, 0, 230, "#16A34A", 1); circle(c, 0, 0, 230, "#FFFFFF", 1, stroke=10)
    n = int(99 * ease_out(prog(t, 0, 0.9))) if st == 0 else 99
    draw_text(c, f"{n}", 0, 95, "anton", 280, "#FFFFFF", 1, align="center"); c.restore()
    draw_text(c, "METACRITIC · 18/11/2026", 420, H / 2 + 300, "ovmono", 30, "#FFFFFF", p, align="center", tracking=2)
    rows = [("99 SOBRE 100", "Nota media de la crítica"), ("+140 RESEÑAS", "0 mixtas · 0 negativas"), ("RÉCORD HISTÓRICO", "Empata con Ocarina of Time (1998)"),
            ("OPENCRITIC: 98-99", "El 100 % de la crítica lo recomienda"), ("16 DE 18 RESEÑAS", "hablan de Jason y Lucía (resumen de Output Lag)")]
    if st >= 1:
        k = st - 1
        for i, (a_, b_) in enumerate(rows[:k + 1]):
            q = ease_out(prog(t, 0, 0.35)) if i == k else 1.0; y = 240 + i * 150
            c.save(); c.translate((1 - q) * 80, 0)
            draw_text(c, a_, 760, y, "anton", 76, YEL if i == k else "#FFFFFF", q, tracking=1); draw_text(c, b_, 762, y + 46, "intersb", 32, "#FFFFFF", 0.85 * q)
            c.restore()

QUOTES = [("IGN", "10/10", "«El videojuego más impresionante que he jugado nunca»"),
          ("GAMESPOT", "10/10", "«Apuesto a que no lo superará nadie hasta GTA 7»"),
          ("EUROGAMER", "5/5", "«Rockstar vuelve a ampliar el horizonte de los videojuegos»"),
          ("GAMESRADAR+", "", "«El sandbox de mayor fidelidad de esta generación»")]
def g_quote(c, t, d, sh, ctx):
    bgs = ["Vice_City_15", "Vice_City_10", "Vice_City_26", "Vice_City_11"]; q = sh.get("q", 0); src, score, txt = QUOTES[q]
    _panel_bg(c, bgs[q], 0.6); p = ease_out(prog(t, 0, 0.4))
    c.save(); c.translate(0, (1 - p) * 40)
    draw_text(c, src, 160, 330, "anton", 110, YEL, p, tracking=3)
    if score:
        f = font("anton", 110); xs = 160 + text_w(src, f, 3) + 50
        rect(c, xs, 228, 300, 130, "#16A34A", p, r=16); draw_text(c, score, xs + 150, 330, "anton", 100, "#FFFFFF", p, align="center")
    lines = wrap(txt, "dmserif", 84, 1500)
    for i, ln in enumerate(lines): draw_text(c, ln, 160, 500 + i * 100, "dmserif", 84, "#FFFFFF", p)
    draw_text(c, "Reseña del 18/11/2026 · traducción de Sal y Asfalto", 162, 520 + len(lines) * 100, "ovmono", 28, "#FFFFFF", 0.75 * p)
    c.restore()

OUTLETS = [("IGN", "10"), ("GAMESPOT", "10"), ("EUROGAMER", "5/5"), ("DESTRUCTOID", "10"), ("WORTHPLAYING", "9,5"), ("WINDOWS CENTRAL", ""),
           ("GAMESRADAR+", ""), ("FORBES", ""), ("VICE", ""), ("THE GUARDIAN", ""), ("DIGITAL FOUNDRY", "análisis técnico"), ("PRENSA DE N. ZELANDA", "primeros jugadores")]
def g_outlets(c, t, d, sh, ctx):
    rect(c, 0, 0, W, H, "#0B0C10", 1)
    draw_text(c, "DE DÓNDE SALEN LAS OPINIONES", W / 2, 130, "anton", 70, YEL, ease_out(prog(t, 0, 0.3)), align="center", tracking=2)
    for i, (n, sc) in enumerate(OUTLETS):
        p = ease_out_back(prog(t, 0.04 * i, 0.04 * i + 0.35)); x = 110 + (i % 4) * 430; y = 220 + (i // 4) * 250
        c.save(); c.translate(x + 200, y + 100); c.scale(p, p); c.translate(-(x + 200), -(y + 100))
        _card(c, x, y, 400, 200, "#FFFFFF", 1)
        draw_text(c, n, x + 200, y + 95, "anton", 44 if len(n) < 14 else 36, "#FFFFFF", 1, align="center", tracking=1)
        if sc: draw_text(c, sc, x + 200, y + 160, "anton" if len(sc) < 5 else "intersb", 52 if len(sc) < 5 else 28, YEL, 1, align="center")
        c.restore()
    draw_text(c, "Reseñas publicadas el 18/11/2026 tras jugar la versión final · fuentes en la descripción", W / 2, H - 60, "intersb", 30, "#FFFFFF", 0.8, align="center")

def _spoiler_jump(ctx):
    T = table(ctx)
    for st, (n, name) in T["chapters"]:
        if "CONDUCCIÓN" in name: return f"{int(st // 60)}:{int(st % 60):02d}"
    return ""

def g_spoiler(c, t, d, sh, ctx):
    st = sh.get("step", 0)
    rect(c, 0, 0, W, H, "#1A0606" if st else "#0B0C10", 1)
    for k in range(-2, 24):   # bandas de advertencia
        x = k * 120 - (t * 60) % 120
        draw_poly(c, [(x, 0), (x + 60, 0), (x - 140, 90), (x - 200, 90)], "#FFC72C", 0.9)
        draw_poly(c, [(x, H - 90), (x + 60, H - 90), (x - 140, H), (x - 200, H)], "#FFC72C", 0.9)
    p = ease_out_back(prog(t, 0, 0.45), 2.0)
    c.save(); c.translate(W / 2, H / 2 - 40); c.scale(p, p)
    icon(c, "warn", 0, -200, 150, "#FF4A3D", 1)
    draw_text(c, "AVISO DE SPOILER", 0, 30, "anton", 160, "#FFFFFF", 1, align="center", tracking=4)
    sub = "ESCENAS DE MISIONES DEL EXTENDED LOOK (OFICIAL)" if st else "EN EL CAPÍTULO 4 HAY ESCENAS DE MISIONES"
    draw_text(c, sub, 0, 120, "ovblk", 44, YEL, 1, align="center", tracking=2)
    if st:
        j = _spoiler_jump(ctx)
        if j: draw_text(c, f"PARA SALTARLAS, VE AL MINUTO {j}", 0, 200, "anton", 64 if st == 1 else 96, YEL if st == 2 else "#FFFFFF", 1, align="center", tracking=2)
    c.restore()

def g_spoiler_end(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_05", 0.5); p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, H / 2); c.scale(p, p)
    rect(c, -560, -110, 1120, 200, "#16A34A", 1, r=20); draw_text(c, "FIN DE LOS SPOILERS", 0, 35, "anton", 120, "#FFFFFF", 1, align="center", tracking=3); c.restore()

UNLOCK = [("NUEVA ZELANDA", "11:00 UTC · 18/11"), ("AUSTRALIA (SÍDNEY)", "13:00 UTC · 18/11"), ("JAPÓN", "15:00 UTC · 18/11"), ("ESPAÑA", "23:00 UTC · 18/11"),
          ("MÉXICO (CDMX)", "06:00 UTC · 19/11")]
def g_nz(c, t, d, sh, ctx):
    _panel_bg(c, "Leonida_Keys_01", 0.62); st = sh.get("step", 0)
    if st == 2:
        p = ease_out_back(prog(t, 0, 0.4)); c.save(); c.translate(W / 2, H / 2); c.scale(p, p)
        _card(c, -760, -220, 1520, 420, YEL, 1)
        draw_text(c, "EL «TRUCO DE NUEVA ZELANDA»", 0, -110, "anton", 92, YEL, 1, align="center", tracking=2)
        draw_text(c, "Cambiar la región de la consola para jugar antes", 0, -20, "intersb", 46, "#FFFFFF", 1, align="center")
        draw_text(c, "Algunos medios advierten de posibles sanciones en las cuentas", 0, 80, "intersb", 40, "#FF8A80", 1, align="center")
        c.restore(); return
    draw_text(c, "DESBLOQUEO A MEDIANOCHE LOCAL", W / 2, 235, "anton", 80, "#FFFFFF", ease_out(prog(t, 0, 0.3)), align="center", tracking=2)
    n = 1 if st == 0 else len(UNLOCK)
    for i, (a_, b_) in enumerate(UNLOCK[:n]):
        q = ease_out(prog(t, 0.08 * i, 0.08 * i + 0.35)); y = 360 + i * 125
        c.save(); c.translate((1 - q) * 80, 0)
        rect(c, W / 2 - 640, y - 70, 1280, 115, "#0B0C10", 0.85 * q, r=14); rect(c, W / 2 - 640, y - 70, 12, 115, YEL if i == 0 else "#FFFFFF", q)
        draw_text(c, a_, W / 2 - 590, y + 12, "anton", 64, YEL if i == 0 else "#FFFFFF", q, tracking=1)
        draw_text(c, b_, W / 2 + 590, y + 12, "ovmono", 44, "#FFFFFF", q, align="right")
        c.restore()
    if st == 0: draw_text(c, "PRIMER PAÍS DEL MUNDO EN JUGARLO", W / 2, 560, "anton", 70, YEL, ease_out(prog(t, 0.3, 0.7)), align="center", tracking=2)

def g_warn(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_22", 0.6); p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, H / 2); c.scale(p, p); icon(c, "warn", 0, -170, 160, "#FF4A3D", 1)
    draw_text(c, "RIESGO DE SANCIÓN", 0, 40, "anton", 130, "#FFFFFF", 1, align="center", tracking=3)
    draw_text(c, "Saltarse la hora de desbloqueo puede costar la cuenta", 0, 120, "intersb", 44, YEL, 1, align="center"); c.restore()

def g_realism(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_09", 0.6)
    _rows(c, t, [("COCHES FRÁGILES", "Se rompen antes que en GTA 5"), ("FACTURAS DE REPARACIÓN", "Arreglarlos cuesta dinero"), ("TAREAS COTIDIANAS", "Comer, dormir, entrenar")],
          sh.get("step", 0) + (1 if sh.get("step", 0) == 1 else 0), y0=420)
    draw_text(c, "6 RESEÑAS LO AVISAN", W / 2, 250, "anton", 80, YEL, 1, align="center", tracking=2)

def g_fps(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_27", 0.62); st = sh.get("step", 0)
    p = ease_out_back(prog(t, 0, 0.4)) if st == 0 else 1.0
    c.save(); c.translate(430, H / 2 - 30); c.scale(p, p)
    draw_text(c, "30", 0, 120, "anton", 380, YEL, 1, align="center"); draw_text(c, "FPS", 0, 220, "anton", 110, "#FFFFFF", 1, align="center"); c.restore()
    rows = [("TODAS LAS CONSOLAS", "PS5, PS5 Pro, Xbox Series X y S"), ("SIN MODO A 60", "No hay opción de rendimiento"), ("9 RESEÑAS", "notaron caídas por debajo de 30")]
    for i, (a_, b_) in enumerate(rows[:st + 1]):
        q = ease_out(prog(t, 0, 0.35)) if i == st else 1.0; y = 300 + i * 190
        c.save(); c.translate((1 - q) * 80, 0)
        draw_text(c, a_, 820, y, "anton", 84, YEL if i == st else "#FFFFFF", q, tracking=1); draw_text(c, b_, 822, y + 52, "intersb", 36, "#FFFFFF", 0.85 * q)
        c.restore()

def g_df(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_17", 0.64); st = sh.get("step", 0)
    draw_text(c, "DIGITAL FOUNDRY", W / 2, 250, "anton", 90, YEL, 1, align="center", tracking=3)
    _rows(c, t, [("XBOX SERIES X", "1440p internos · objetivo 30 fps · bajadas en escenas cargadas"),
                 ("XBOX SERIES S", "720p internos, reescalados a 1080p · a menudo por debajo de 30"),
                 ("SU RECOMENDACIÓN", "Jugar en PS5 o en Xbox Series X")], st, y0=420, dy=180)

def g_police(c, t, d, sh, ctx):
    _panel_bg(c, "Lucia_Caminos_14", 0.62)
    draw_text(c, "LA POLICÍA, SEGÚN WINDOWS CENTRAL", W / 2, 250, "anton", 70, YEL, 1, align="center", tracking=2)
    _rows(c, t, [("CORTA ALARMAS Y CÁMARAS", "La policía pierde eficacia"), ("ESCÓNDETE EN EL COCHE", "Los agentes pasan a modo de búsqueda")], sh.get("step", 0), y0=380, dy=210)

def g_drone(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_03", 0.6); p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, H / 2); c.scale(p, p)
    draw_text(c, "CARRERAS DE DRONES", 0, 20, "anton", 140, "#FFFFFF", 1, align="center", tracking=3); c.restore()
    rect(c, W / 2 - 470, 700, 940, 58, "#FFB000", 1, r=8)
    draw_text(c, "SIN IMAGEN OFICIAL · LO CITAN LAS RESEÑAS", W / 2, 740, "ovmono", 30, "#16181B", 1, align="center")

def _poll(c, t, title, opts):
    _cover(c, thumb("Jason_and_Lucia_Beach_landscape", 1600), 1.05 + 0.04 * clamp(t / 4), 0.5, 0.45); rect(c, 0, 0, W, H, "#000000", 0.45)
    p = ease_out_back(prog(t, 0, 0.4)); c.save(); c.translate(W / 2, 220); c.scale(p, p)
    f = font("anton", 90); w = text_w(title, f, 3) + 120
    rect(c, -w / 2, -80, w, 130, YEL, 1, r=16); draw_text(c, title, 0, 25, "anton", 90, "#16181B", 1, align="center", tracking=3); c.restore()
    for i, n in enumerate(opts):
        q = ease_out_back(prog(t, 0.3 + 0.15 * i, 0.7 + 0.15 * i)); x = W / 2 - 700 + i * 760
        c.save(); c.translate(x + 320, 820); c.scale(q, q); c.translate(-(x + 320), -820)
        rect(c, x, 750, 640, 140, "#0B0C10", 0.88, r=70); rect(c, x, 750, 640, 140, "#FFFFFF", 1, r=70, stroke=5)
        draw_text(c, n, x + 320, 845, "anton", 70, "#FFFFFF", 1, align="center", tracking=2); c.restore()

def g_poll2(c, t, d, sh, ctx): _poll(c, t, "¿INMERSIÓN O MOLESTIA?", ["INMERSIÓN", "MOLESTIA"])
def g_poll3(c, t, d, sh, ctx): _poll(c, t, "PAUSA RÁPIDA", ["YA LO JUEGO", "TODAVÍA NO"])

def g_hours(c, t, d, sh, ctx):
    _panel_bg(c, "Jason_and_Lucia_13", 0.6); p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, H / 2 - 40); c.scale(p, p)
    draw_text(c, "≈80 HORAS", 0, 40, "anton", 220, YEL, 1, align="center", tracking=3)
    draw_text(c, "HISTORIA PRINCIPAL · ESTIMACIÓN DE ROCKSTAR ANTES DEL LANZAMIENTO", 0, 130, "ovblk", 34, "#FFFFFF", 1, align="center", tracking=1); c.restore()

def g_houser(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_15", 0.62)
    quote_box(c, "«Estamos increíblemente agradecidos y esperamos compartir estas experiencias con ustedes muchos años más»", prog(t, 0.05, 0.45),
              src="Sam Houser, cofundador de Rockstar · vía GamesRadar+ (traducción)")

def g_stock(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_10", 0.62)
    _rows(c, t, [("TAKE-TWO +6 % EN BOLSA", "El día de las reseñas (Forbes, 18/11/2026)"), ("+1.500 M$ EN RESERVAS", "Estimación citada por Forbes")], sh.get("step", 0), y0=420, dy=220, col=GRN)

def g_nospoil2(c, t, d, sh, ctx):
    _panel_bg(c, "Jason_and_Lucia_16", 0.5); p = ease_out_back(prog(t, 0, 0.4), 2.0)
    c.save(); c.translate(W / 2, H / 2); c.rotate(-4); c.scale(1.6 - 0.6 * p, 1.6 - 0.6 * p)
    f = font("ovblk", 80); txt = "SIN SPOILERS EN LOS COMENTARIOS"; w = text_w(txt, f, 3) + 90
    rect(c, -w / 2, -80, w, 130, "#FF4A3D", clamp(p * 2), r=12, stroke=9)
    draw_text(c, txt, 0, 20, "ovblk", 80, "#FF4A3D", clamp(p * 2), align="center", tracking=3); c.restore()

GFX.update({k[2:]: v for k, v in list(globals().items()) if k.startswith("g_") and k[2:] not in GFX})
GFX_SRC.update({"meta": "Metacritic y OpenCritic (18/11/2026), vía Bloomberg, Vice, Dot Esports y Output Lag", "quote": "Reseñas del 18/11/2026 · traducción de Sal y Asfalto",
                "outlets": "Gráfico: Sal y Asfalto · fuentes en la descripción", "title2": None, "spoiler": "Aviso de Sal y Asfalto", "spoiler_end": None,
                "nz": "Hora de desbloqueo: medianoche local (MP1st, Stevivor) · prensa de Nueva Zelanda: Stuff y NZ Herald",
                "warn": "Notebookcheck, Newsweek y NME (11/2026)", "realism": "Resumen de reseñas de The National (18/11/2026)",
                "fps": "Resúmenes de reseñas de The National y Output Lag (18/11/2026)", "df": "Digital Foundry vía VGC y LevelUp · Rockstar a Wccftech (11/2026)",
                "police": "Windows Central, reseña del 18/11/2026", "drone": "Output Lag (resumen de reseñas, 18/11/2026)", "poll2": "Gráfico con ilustración oficial de Rockstar Games",
                "poll3": "Gráfico con ilustración oficial de Rockstar Games", "hours": "Rob Nelson (Rockstar North) a Variety, 11/2026",
                "houser": "GamesRadar+ (18/11/2026)", "stock": "Forbes (18/11/2026)", "nospoil2": None})

def thumbnail2(c):
    """Miniatura del vídeo post lanzamiento: captura oficial, sin spoilers."""
    Wt, Ht = 1280, 720
    img = load_img(_index()["Jason_and_Lucia_09"])
    iw, ih = img.width(), img.height(); s = Ht / ih * 1.08; dw = iw * s
    c.drawImageRect(img, skia.Rect.MakeXYWH(Wt - dw + 200, -20, dw, ih * s), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (760, 0)], [skia.Color(10, 8, 20, 245), skia.Color(10, 8, 20, 205), skia.Color(10, 8, 20, 0)], [0, 0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(820, Ht), g)
    draw_text(c, "GTA 6", 48, 165, "anton", 160, YEL, 1, tracking=3)
    draw_text(c, "¿CÓMO SE", 50, 280, "anton", 104, "#FFFFFF", 1, tracking=2)
    draw_text(c, "JUEGA?", 50, 390, "anton", 104, "#FFFFFF", 1, tracking=2)
    circle(c, 640, 250, 92, "#16A34A", 1); circle(c, 640, 250, 92, "#FFFFFF", 1, stroke=6)
    draw_text(c, "99", 640, 285, "anton", 100, "#FFFFFF", 1, align="center"); draw_text(c, "METACRITIC", 640, 375, "ovblk", 26, "#FFFFFF", 1, align="center", tracking=2)
    rect(c, 50, 440, 560, 90, "#FF4A3D", 1, r=45); draw_text(c, "LO BUENO Y LO MALO", 330, 501, "ovblk", 44, "#FFFFFF", 1, align="center", tracking=2)
    draw_text(c, "LO QUE DICE QUIEN YA LO JUGÓ", 54, 610, "ovmono", 30, "#FFFFFF", 0.92, tracking=2)
    draw_badge(c, 1200, 640, 52)

def g_dfps(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_22", 0.64); st = sh.get("step", 0)
    draw_text(c, "DIGITAL FOUNDRY · PLAYSTATION", W / 2, 250, "anton", 80, YEL, 1, align="center", tracking=3)
    _rows(c, t, [("PS5 Y PS5 PRO", "≈1440p internos · objetivo 30 fps · sin modo a 60"),
                 ("PS5 PRO", "PSSR → imagen casi 4K · sombras con trazado de rayos · 30 casi estables"),
                 ("PS5 NORMAL", "Más caídas por debajo de 30 en la acción intensa"),
                 ("VEREDICTO", "«Aceptable, pero algo decepcionante»")], st, y0=400, dy=160)

def g_stream(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_13", 0.62); st = sh.get("step", 0)
    draw_text(c, "RÉCORD DE AUDIENCIA EN DIRECTO", W / 2, 250, "anton", 80, YEL, 1, align="center", tracking=2)
    _rows(c, t, [("+6 MILLONES A LA VEZ", "Twitch + YouTube + Kick (Streams Charts; otras mediciones, hasta 7,8 M)"),
                 ("+3 MILLONES EN TWITCH", "Pico de espectadores simultáneos"),
                 ("RÉCORD HISTÓRICO", "El mayor lanzamiento de un videojuego en streaming")], st, y0=420, dy=190, col=GRN)

def g_bugs(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_16", 0.66); st = sh.get("step", 0)
    draw_text(c, "PRIMERAS QUEJAS DE JUGADORES", W / 2, 250, "anton", 80, "#FF8A80", 1, align="center", tracking=2)
    _rows(c, t, [("ATRAVESAR OBJETOS", "Personajes que atraviesan muebles o el suelo"), ("FÍSICAS RARAS", "Reacciones extrañas de objetos y vehículos"),
                 ("CIERRES EN CONSOLA", "Algunos jugadores reportan cuelgues")], 2 if st >= 1 or sh.get("row") else min(2, int(t / 1.2)), y0=470, dy=165, col="#FF8A80")
    if st >= 1:
        p = ease_out_back(prog(t, 0, 0.4)); c.save(); c.translate(W / 2, 345); c.scale(p, p)
        rect(c, -560, -50, 1120, 80, "#FFB000", 1, r=10); draw_text(c, "SIN CONFIRMAR POR ROCKSTAR · OTROS NO REPORTAN FALLOS", 0, 6, "ovmono", 30, "#16181B", 1, align="center")
        c.restore()

def g_psn(c, t, d, sh, ctx):
    _panel_bg(c, "Vice_City_27", 0.62); p = ease_out_back(prog(t, 0, 0.4))
    c.save(); c.translate(W / 2, H / 2 - 20); c.scale(p, p)
    draw_text(c, "CAÍDA DE PLAYSTATION NETWORK", 0, 0, "anton", 96, "#FFFFFF", 1, align="center", tracking=2)
    draw_text(c, "Horas antes del lanzamiento · reconocida por PlayStation", 0, 80, "intersb", 44, YEL, 1, align="center"); c.restore()

GFX.update({"dfps": g_dfps, "stream": g_stream, "bugs": g_bugs, "psn": g_psn})
GFX_SRC.update({"dfps": "Digital Foundry (18/11/2026), vía TweakTown y Twisted Voxel", "stream": "Streams Charts, TalkEsport y Win.gg (19/11/2026)",
                "bugs": "Reportes de jugadores recogidos por Sportskeeda y Brit Brief · sin confirmar", "psn": "Newsweek (18/11/2026)"})
