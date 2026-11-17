"""Motor gráfico vectorial (skia) para motion graphics originales."""
import math, os, re, numpy as np, skia

FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
_TF = {}
FONTS = {
    "anton": "Anton-Regular.ttf", "bebas": "BebasNeue-Regular.ttf", "archivo": "ArchivoBlack-Regular.ttf",
    "space": "SpaceGrotesk[wght].ttf", "elite": "SpecialElite-Regular.ttf", "courier": "CourierPrime-Regular.ttf",
    "courierb": "CourierPrime-Bold.ttf", "marker": "PermanentMarker-Regular.ttf", "monoton": "Monoton-Regular.ttf",
    "bungee": "Bungee-Regular.ttf", "techmono": "ShareTechMono-Regular.ttf", "dmserif": "DMSerifDisplay-Regular.ttf",
    "dmserifi": "DMSerifDisplay-Italic.ttf", "pacifico": "Pacifico-Regular.ttf", "rubikmono": "RubikMonoOne-Regular.ttf",
    "barlow": "BarlowCondensed-Bold.ttf", "barlowblk": "BarlowCondensed-Black.ttf", "barlowmd": "BarlowCondensed-Medium.ttf",
    "shoulders": "BigShouldersDisplay[wght].ttf", "vt323": "VT323-Regular.ttf", "caveat": "Caveat[wght].ttf",
    "abril": "AbrilFatface-Regular.ttf", "syne": "Syne[wght].ttf", "inter": "Inter-Regular.otf", "intermd": "Inter-Medium.otf",
    "intersb": "Inter-SemiBold.otf", "interb": "Inter-Bold.otf", "interxb": "Inter-ExtraBold.otf", "interblk": "Inter-Black.otf",
    "interdisp": "InterDisplay-Black.otf", "mono": "JetBrainsMono-Regular.ttf", "monob": "JetBrainsMono-Bold.ttf",
}

def typeface(name):
    if name not in _TF:
        _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, FONTS[name]))
    return _TF[name]

_FC = {}
def font(name, size):
    k = (name, round(size, 1))
    if k not in _FC:
        f = skia.Font(typeface(name), size); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kAntiAlias)
        if len(_FC) > 4000: _FC.clear()
        _FC[k] = f
    return _FC[k]

# ---------------------------------------------------------------- color
def hexc(h, a=1.0):
    h = h.lstrip("#"); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return skia.Color(r, g, b, int(max(0, min(1, a)) * 255))

def mixc(h1, h2, t, a=1.0):
    h1 = h1.lstrip("#"); h2 = h2.lstrip("#")
    c = [int(int(h1[i:i + 2], 16) * (1 - t) + int(h2[i:i + 2], 16) * t) for i in (0, 2, 4)]
    return skia.Color(c[0], c[1], c[2], int(a * 255))

def paint(color="#ffffff", a=1.0, stroke=None, aa=True, blur=0, cap="round", join="round"):
    p = skia.Paint(AntiAlias=aa)
    p.setColor(hexc(color, a) if isinstance(color, str) else color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap({"round": skia.Paint.kRound_Cap, "butt": skia.Paint.kButt_Cap, "square": skia.Paint.kSquare_Cap}[cap])
        p.setStrokeJoin({"round": skia.Paint.kRound_Join, "miter": skia.Paint.kMiter_Join, "bevel": skia.Paint.kBevel_Join}[join])
    if blur > 0: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

def lin_grad(x0, y0, x1, y1, colors, pos=None, a=1.0):
    p = skia.Paint(AntiAlias=True)
    cols = [hexc(c, a) if isinstance(c, str) else c for c in colors]
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], cols, pos))
    return p

def rad_grad(cx, cy, r, colors, pos=None, a=1.0):
    p = skia.Paint(AntiAlias=True)
    cols = [hexc(c, a) if isinstance(c, str) else c for c in colors]
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), max(1, r), cols, pos))
    return p

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)
def lerp(a, b, t): return a + (b - a) * t
def ease_out(t): return 1 - (1 - t) ** 3
def ease_in(t): return t ** 3
def ease_io(t): return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
def ease_out_back(t, s=1.7): t -= 1; return t * t * ((s + 1) * t + s) + 1
def ease_out_expo(t): return 1 if t >= 1 else 1 - 2 ** (-10 * t)
def spring(t, f=4.5, d=5.0): return 1 - math.exp(-d * t) * math.cos(f * math.pi * t) if t > 0 else 0.0
def pulse(t, period=1.0): return 0.5 + 0.5 * math.sin(2 * math.pi * t / period)
def inout(t, d, fin=0.4, fout=0.35):
    """Opacidad de entrada/salida de una escena."""
    return clamp(min(t / fin if fin > 0 else 1, (d - t) / fout if fout > 0 else 1))

# ---------------------------------------------------------------- texto
def text_w(s, f, tracking=0.0):
    w = f.measureText(s)
    return w + tracking * max(0, len(s) - 1)

def draw_text(c, s, x, y, fname, size, color="#ffffff", a=1.0, align="left", tracking=0.0, p=None,
              shadow=None, glow=None, stroke=None, stroke_color="#000000"):
    """Dibuja texto en la línea base y. align: left|center|right. tracking en px."""
    if not s or a <= 0.003: return 0
    f = font(fname, size); w = text_w(s, f, tracking)
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    pnt = p or paint(color, a)
    def _draw(px, py, pp):
        if tracking == 0:
            c.drawString(s, px, py, f, pp)
        else:
            cx = px
            for ch in s:
                c.drawString(ch, cx, py, f, pp); cx += f.measureText(ch) + tracking
    if glow:
        gcol, gr = glow; _draw(x, y, paint(gcol, a * 0.85, blur=gr))
    if shadow:
        dx, dy, sb, sc, sa = shadow; _draw(x + dx, y + dy, paint(sc, a * sa, blur=sb))
    if stroke:
        _draw(x, y, paint(stroke_color, a, stroke=stroke))
    _draw(x, y, pnt)
    return w

def wrap(s, fname, size, maxw, tracking=0):
    f = font(fname, size); words = s.split(); lines = []; cur = ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(trial, f, tracking) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

def draw_par(c, s, x, y, fname, size, maxw, lh=1.25, **kw):
    lines = wrap(s, fname, size, maxw, kw.get("tracking", 0))
    for i, L in enumerate(lines): draw_text(c, L, x, y + i * size * lh, fname, size, **kw)
    return len(lines) * size * lh

def typewriter(s, t, cps=28):
    n = int(max(0, t) * cps); return s[:n]

# ---------------------------------------------------------------- formas
def rect(c, x, y, w, h, color="#ffffff", a=1.0, r=0, p=None, stroke=None, blur=0):
    pp = p or paint(color, a, stroke=stroke, blur=blur)
    rr = skia.Rect.MakeXYWH(x, y, w, h)
    if r: c.drawRoundRect(rr, r, r, pp)
    else: c.drawRect(rr, pp)

def circle(c, x, y, r, color="#ffffff", a=1.0, p=None, stroke=None, blur=0):
    c.drawCircle(x, y, max(0.1, r), p or paint(color, a, stroke=stroke, blur=blur))

def line(c, x0, y0, x1, y1, color="#ffffff", a=1.0, w=2, cap="round", dash=None):
    pp = paint(color, a, stroke=w, cap=cap)
    if dash: pp.setPathEffect(skia.DashPathEffect.Make(dash, 0))
    c.drawLine(x0, y0, x1, y1, pp)

def poly(pts, close=True):
    p = skia.Path()
    if not pts: return p
    p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p

def draw_poly(c, pts, color="#ffffff", a=1.0, close=True, stroke=None, p=None, blur=0):
    c.drawPath(poly(pts, close), p or paint(color, a, stroke=stroke, blur=blur))

def partial_path(path, frac):
    """Devuelve el segmento inicial [0, frac] de un path (para animar trazos)."""
    if frac >= 1: return path
    meas = skia.PathMeasure(path, False); out = skia.Path(); total = 0; lens = []
    while True:
        L = meas.getLength(); lens.append(L); total += L
        if not meas.nextContour(): break
    meas = skia.PathMeasure(path, False); target = total * frac; acc = 0
    for L in lens:
        if acc + L >= target:
            meas.getSegment(0, target - acc, out, True); break
        meas.getSegment(0, L, out, True); acc += L; meas.nextContour()
    return out

_NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?")
def svg_path(d, scale=1.0, ox=0.0, oy=0.0):
    """Parser mínimo de rutas SVG (M L H V C S Q T Z, absolutas y relativas)."""
    toks = re.findall(r"[MmLlHhVvCcSsQqTtZzAa]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", d)
    p = skia.Path(); i = 0; cx = cy = 0.0; sx = sy = 0.0; cmd = None; lastc = None
    def num():
        nonlocal i; v = float(toks[i]); i += 1; return v
    T = lambda x, y: (ox + x * scale, oy + y * scale)
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]): cmd = toks[i]; i += 1
        rel = cmd.islower(); C = cmd.upper()
        if C == "Z": p.close(); cx, cy = sx, sy; continue
        if C == "M":
            x, y = num(), num(); x, y = (cx + x, cy + y) if rel else (x, y); p.moveTo(*T(x, y)); cx, cy = sx, sy = x, y
            cmd = "l" if rel else "L"
        elif C == "L":
            x, y = num(), num(); x, y = (cx + x, cy + y) if rel else (x, y); p.lineTo(*T(x, y)); cx, cy = x, y
        elif C == "H":
            x = num(); x = cx + x if rel else x; p.lineTo(*T(x, cy)); cx = x
        elif C == "V":
            y = num(); y = cy + y if rel else y; p.lineTo(*T(cx, y)); cy = y
        elif C == "C":
            a = [num() for _ in range(6)]
            if rel: a = [a[0] + cx, a[1] + cy, a[2] + cx, a[3] + cy, a[4] + cx, a[5] + cy]
            p.cubicTo(*T(a[0], a[1]), *T(a[2], a[3]), *T(a[4], a[5])); lastc = (a[2], a[3]); cx, cy = a[4], a[5]
        elif C == "S":
            a = [num() for _ in range(4)]
            if rel: a = [a[0] + cx, a[1] + cy, a[2] + cx, a[3] + cy]
            r1 = (2 * cx - lastc[0], 2 * cy - lastc[1]) if lastc else (cx, cy)
            p.cubicTo(*T(*r1), *T(a[0], a[1]), *T(a[2], a[3])); lastc = (a[0], a[1]); cx, cy = a[2], a[3]
        elif C == "Q":
            a = [num() for _ in range(4)]
            if rel: a = [a[0] + cx, a[1] + cy, a[2] + cx, a[3] + cy]
            p.quadTo(*T(a[0], a[1]), *T(a[2], a[3])); cx, cy = a[2], a[3]
        elif C == "A":  # aproximación: línea recta al punto final
            a = [num() for _ in range(7)]; x, y = (cx + a[5], cy + a[6]) if rel else (a[5], a[6]); p.lineTo(*T(x, y)); cx, cy = x, y
        else: i += 1
    return p

# ---------------------------------------------------------------- iconos (rutas propias, 100x100)
ICONS = {
    "clock": "M50 8 C73 8 92 27 92 50 C92 73 73 92 50 92 C27 92 8 73 8 50 C8 27 27 8 50 8 Z M50 18 C32 18 18 32 18 50 C18 68 32 82 50 82 C68 82 82 68 82 50 C82 32 68 18 50 18 Z M46 28 L54 28 L54 48 L68 58 L63 65 L46 53 Z",
    "download": "M42 10 L58 10 L58 50 L74 50 L50 76 L26 50 L42 50 Z M14 80 L86 80 L86 92 L14 92 Z",
    "disk": "M10 30 L90 30 L90 74 L10 74 Z M18 38 L18 66 L82 66 L82 38 Z M24 44 L60 44 L60 60 L24 60 Z M68 50 C71 50 74 53 74 56 C74 59 71 62 68 62 C65 62 62 59 62 56 C62 53 65 50 68 50 Z",
    "tag": "M10 14 L52 14 L90 52 L52 90 L10 52 Z M28 26 C32 26 36 30 36 34 C36 38 32 42 28 42 C24 42 20 38 20 34 C20 30 24 26 28 26 Z",
    "chat": "M12 16 L88 16 L88 66 L46 66 L26 84 L28 66 L12 66 Z",
    "globe": "M50 8 C73 8 92 27 92 50 C92 73 73 92 50 92 C27 92 8 73 8 50 C8 27 27 8 50 8 Z M50 16 C44 24 40 36 40 50 C40 64 44 76 50 84 C56 76 60 64 60 50 C60 36 56 24 50 16 Z M16 46 L84 46 L84 54 L16 54 Z",
    "shield": "M50 6 L88 20 L88 48 C88 70 72 86 50 94 C28 86 12 70 12 48 L12 20 Z M50 18 L22 28 L22 48 C22 64 34 77 50 83 Z",
    "warn": "M50 6 L96 88 L4 88 Z M45 34 L55 34 L53 64 L47 64 Z M50 70 C54 70 56 72 56 76 C56 80 54 82 50 82 C46 82 44 80 44 76 C44 72 46 70 50 70 Z",
    "lock": "M26 44 L26 32 C26 18 37 8 50 8 C63 8 74 18 74 32 L74 44 L84 44 L84 92 L16 92 L16 44 Z M36 44 L64 44 L64 32 C64 24 58 18 50 18 C42 18 36 24 36 32 Z",
    "pin": "M50 6 C68 6 82 20 82 38 C82 62 50 94 50 94 C50 94 18 62 18 38 C18 20 32 6 50 6 Z M50 26 C43 26 38 31 38 38 C38 45 43 50 50 50 C57 50 62 45 62 38 C62 31 57 26 50 26 Z",
    "star": "M50 4 L62 36 L96 38 L70 60 L79 94 L50 76 L21 94 L30 60 L4 38 L38 36 Z",
    "check": "M8 52 L22 38 L40 56 L78 18 L92 32 L40 84 Z",
    "cross": "M20 8 L50 38 L80 8 L92 20 L62 50 L92 80 L80 92 L50 62 L20 92 L8 80 L38 50 L8 20 Z",
    "eye": "M4 50 C20 24 36 14 50 14 C64 14 80 24 96 50 C80 76 64 86 50 86 C36 86 20 76 4 50 Z M50 30 C39 30 30 39 30 50 C30 61 39 70 50 70 C61 70 70 61 70 50 C70 39 61 30 50 30 Z",
    "pad": "M22 30 L78 30 C90 30 96 44 96 58 C96 72 90 80 82 80 C74 80 70 70 64 64 L36 64 C30 70 26 80 18 80 C10 80 4 72 4 58 C4 44 10 30 22 30 Z M26 42 L30 42 L30 46 L34 46 L34 50 L30 50 L30 54 L26 54 L26 50 L22 50 L22 46 L26 46 Z M70 42 C72 42 74 44 74 46 C74 48 72 50 70 50 C68 50 66 48 66 46 C66 44 68 42 70 42 Z M78 50 C80 50 82 52 82 54 C82 56 80 58 78 58 C76 58 74 56 74 54 C74 52 76 50 78 50 Z",
    "skull": "M50 6 C74 6 90 22 90 44 C90 58 84 66 76 70 L76 84 L64 84 L64 94 L36 94 L36 84 L24 84 L24 70 C16 66 10 58 10 44 C10 22 26 6 50 6 Z M34 40 C28 40 24 44 24 50 C24 56 28 60 34 60 C40 60 44 56 44 50 C44 44 40 40 34 40 Z M66 40 C60 40 56 44 56 50 C56 56 60 60 66 60 C72 60 76 56 76 50 C76 44 72 40 66 40 Z M50 62 L56 72 L44 72 Z",
    "wifi": "M50 74 C55 74 58 78 58 82 C58 86 55 90 50 90 C45 90 42 86 42 82 C42 78 45 74 50 74 Z M24 56 C38 42 62 42 76 56 L68 64 C58 54 42 54 32 64 Z M8 40 C30 18 70 18 92 40 L84 48 C66 30 34 30 16 48 Z",
    "palm": "M48 40 C40 30 26 26 12 30 C24 22 40 22 50 32 C52 20 62 10 78 10 C66 16 58 24 56 34 C66 28 82 30 92 40 C78 36 64 38 56 44 L60 92 L48 92 Z",
    "car": "M10 60 L18 38 C20 32 26 28 32 28 L68 28 C74 28 80 32 82 38 L90 60 L90 76 L80 76 C80 82 76 86 70 86 C64 86 60 82 60 76 L40 76 C40 82 36 86 30 86 C24 86 20 82 20 76 L10 76 Z M26 40 L22 54 L78 54 L74 40 Z",
    "money": "M8 26 L92 26 L92 74 L8 74 Z M50 36 C42 36 36 42 36 50 C36 58 42 64 50 64 C58 64 64 58 64 50 C64 42 58 36 50 36 Z",
    "film": "M10 20 L90 20 L90 80 L10 80 Z M16 26 L16 34 L24 34 L24 26 Z M16 66 L16 74 L24 74 L24 66 Z M76 26 L76 34 L84 34 L84 26 Z M76 66 L76 74 L84 74 L84 66 Z M30 30 L70 30 L70 70 L30 70 Z",
    "envelope": "M8 24 L92 24 L92 80 L8 80 Z M14 30 L50 56 L86 30 L86 34 L50 62 L14 34 Z",
    "magnify": "M42 8 C61 8 76 23 76 42 C76 50 73 57 69 62 L92 85 L85 92 L62 69 C57 73 50 76 42 76 C23 76 8 61 8 42 C8 23 23 8 42 8 Z M42 18 C29 18 18 29 18 42 C18 55 29 66 42 66 C55 66 66 55 66 42 C66 29 55 18 42 18 Z",
    "user": "M50 8 C61 8 70 17 70 30 C70 43 61 52 50 52 C39 52 30 43 30 30 C30 17 39 8 50 8 Z M14 92 C14 72 30 58 50 58 C70 58 86 72 86 92 Z",
    "phone": "M30 4 L70 4 C75 4 78 7 78 12 L78 88 C78 93 75 96 70 96 L30 96 C25 96 22 93 22 88 L22 12 C22 7 25 4 30 4 Z M30 14 L30 82 L70 82 L70 14 Z",
    "monitor": "M6 14 L94 14 L94 70 L58 70 L62 84 L74 84 L74 92 L26 92 L26 84 L38 84 L42 70 L6 70 Z M14 22 L14 62 L86 62 L86 22 Z",
    "console": "M14 10 L44 10 L44 92 L14 92 Z M20 18 L20 22 L38 22 L38 18 Z M52 34 L92 34 L92 92 L52 92 Z M66 50 C70 50 74 54 74 58 C74 62 70 66 66 66 C62 66 58 62 58 58 C58 54 62 50 66 50 Z",
    "bolt": "M58 4 L18 56 L46 56 L38 96 L82 40 L54 40 Z",
    "storm": "M28 60 C14 60 6 50 6 40 C6 28 16 20 28 22 C32 12 42 6 54 6 C70 6 82 18 82 32 C92 34 96 42 96 48 C96 56 90 60 82 60 Z M48 62 L36 82 L48 82 L42 96 L62 72 L50 72 L56 62 Z",
}

def icon(c, name, x, y, size, color="#ffffff", a=1.0, glow=None):
    pth = svg_path(ICONS[name], size / 100.0, x - size / 2, y - size / 2)
    pth.setFillType(skia.PathFillType.kEvenOdd)
    if glow: c.drawPath(pth, paint(glow[0], a * 0.8, blur=glow[1]))
    c.drawPath(pth, paint(color, a))

# ---------------------------------------------------------------- fondos y texturas
class Grain:
    """Textura de grano estática (no cambia por frame → comprime bien)."""
    def __init__(self, w, h, amount=10, seed=3):
        rng = np.random.default_rng(seed); n = rng.integers(0, 256, (h // 2, w // 2), dtype=np.uint8)
        arr = np.zeros((h // 2, w // 2, 4), np.uint8); arr[..., 0:3] = n[..., None]; arr[..., 3] = amount
        self.img = skia.Image.fromarray(arr, colorType=skia.ColorType.kRGBA_8888_ColorType)
        self.w, self.h = w, h
    def draw(self, c, a=1.0):
        p = skia.Paint(); p.setAlphaf(a); p.setBlendMode(skia.BlendMode.kOverlay)
        c.drawImageRect(self.img, skia.Rect.MakeWH(self.w, self.h), skia.SamplingOptions(), p)

def vignette(c, w, h, strength=0.55, color="#000000"):
    c.drawRect(skia.Rect.MakeWH(w, h), rad_grad(w / 2, h / 2, math.hypot(w, h) / 2, [hexc(color, 0), hexc(color, 0), hexc(color, strength)], [0, 0.55, 1]))

def bokeh(c, w, h, t, n=24, colors=("#ffffff",), seed=1, size=(20, 90), a=0.10, speed=12):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = rng.random() * w; y = rng.random() * h; r = rng.uniform(*size); ph = rng.random() * 6.28
        col = colors[i % len(colors)]; yy = (y - t * speed * (0.5 + rng.random())) % (h + 200) - 100
        xx = x + math.sin(t * 0.3 + ph) * 30
        c.drawCircle(xx, yy, r, rad_grad(xx, yy, r, [hexc(col, a * (0.6 + 0.4 * math.sin(t + ph))), hexc(col, 0)]))

def grid(c, w, h, step=80, color="#ffffff", a=0.05, ox=0, oy=0, wline=1):
    p = paint(color, a, stroke=wline)
    x = ox % step
    while x < w: c.drawLine(x, 0, x, h, p); x += step
    y = oy % step
    while y < h: c.drawLine(0, y, w, y, p); y += step

# ---------------------------------------------------------------- 3D sencillo
class Cam3D:
    """Cámara en perspectiva: mundo (x, y, z) con z hacia arriba."""
    def __init__(self, w, h, fov=50):
        self.w, self.h = w, h; self.f = (h / 2) / math.tan(math.radians(fov) / 2)
        self.pos = np.array([0, -10, 10.0]); self.target = np.array([0, 0, 0.0])
    def look(self, pos, target):
        self.pos = np.array(pos, float); self.target = np.array(target, float)
        fwd = self.target - self.pos; fwd /= np.linalg.norm(fwd)
        right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right)
        up = np.cross(right, fwd); self.R = np.stack([right, up, fwd])
    def proj(self, pts):
        """pts: (N,3) → (N,2) pantalla y profundidad."""
        p = (np.asarray(pts, float) - self.pos) @ self.R.T
        z = np.maximum(p[:, 2], 1e-3)
        sx = self.w / 2 + self.f * p[:, 0] / z; sy = self.h / 2 - self.f * p[:, 1] / z
        return np.stack([sx, sy], 1), p[:, 2]

def new_surface(w, h):
    info = skia.ImageInfo.Make(w, h, skia.ColorType.kRGBA_8888_ColorType, skia.AlphaType.kPremul_AlphaType)
    return skia.Surface.MakeRaster(info)
