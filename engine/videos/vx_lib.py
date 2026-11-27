"""Biblioteca visual de VIDEO_EXTRA («¿Por qué Vice City es rosa?»).

Todo se dibuja por código (Skia): fachadas art déco genéricas, calles, mapas esquemáticos, tormentas,
documentos y aparatos. Ninguna ilustración copia material de Rockstar ni edificios concretos:
los hoteles son inventados (MAREA, CORAL, BRISA, SOL) y reúnen rasgos comunes del art déco tropical.
"""
import math, zlib, numpy as np, skia
from gfx import *
from brand import PAL

W, H = 1920, 1080

# ---------------------------------------------------------------- paletas por época
PASTEL = dict(rosa="#F7B7C8", menta="#A8E6C9", pervinca="#AFC3F0", crema="#F6E3A8", durazno="#F9C9A8", lavanda="#C9B3E6",
              aqua="#9FE3E0", arena="#E8CF9A", espuma="#B8EBD2", caribe="#4FB8D9", naranja="#F6A26B")
WHITE30 = dict(body="#F2EFE6", body2="#ECE6D8", jade="#4E9C7A", ocre="#C9973B", coral="#E0705A")
NEON = dict(rosa="#FF4FA3", cian="#3FF5FF", menta="#7CFFC4", ambar="#FFC14D", lila="#C77DFF")
SEPIA = dict(papel="#E9DCC2", papel2="#D9C7A4", tinta="#4A3826", tinta2="#6E5638")
BLUE = dict(fondo="#0E2A47", fondo2="#143A60", linea="#CFE6FF")
INK = "#0D0E10"

def night_tint(h, k=0.55, tint="#1B1636"):
    return mixc(h, tint, k)

# ---------------------------------------------------------------- hoteles (rasgos art déco genéricos)
HOTELS = [
    dict(name="MAREA", w=400, h=470, floors=3, top="tower", sign="left", eyebrows=True, fins=True, port=0, glass=False, corner=None, stripes=False),
    dict(name="CORAL", w=380, h=400, floors=3, top="step", sign="center", eyebrows=True, fins=False, port=0, glass=False, corner="right", stripes=True),
    dict(name="BRISA", w=420, h=520, floors=4, top="tower_r", sign="right", eyebrows=True, fins=False, port=3, glass=True, corner=None, stripes=False),
    dict(name="SOL", w=360, h=420, floors=3, top="flat", sign="canopy", eyebrows=True, fins=True, port=0, glass=False, corner="left", stripes=True),
]

def hotel_colors(mode, i):
    """Colores de la fachada i según la época. En 'pastel' el color del cuerpo de un hotel pasa a los detalles del siguiente
    (el truco de continuidad de Leonard Horowitz)."""
    bodies = [PASTEL["rosa"], PASTEL["menta"], PASTEL["lavanda"], PASTEL["crema"]]
    if mode == "pastel":
        return dict(body=bodies[i % 4], trim=bodies[(i - 1) % 4], accent=mixc(bodies[(i - 1) % 4], "#000000", 0.25), win="#3B4E66", sign=NEON["rosa"], shade=0.18)
    if mode == "white":
        acc = [WHITE30["jade"], WHITE30["ocre"], WHITE30["coral"], WHITE30["jade"]][i % 4]
        return dict(body=WHITE30["body"] if i % 2 == 0 else WHITE30["body2"], trim=WHITE30["body"], accent=acc, win="#47505A", sign=acc, shade=0.14)
    if mode == "faded":
        b = ["#B9B3A8", "#A9A59C", "#C2BBAE", "#9E9A91"][i % 4]
        return dict(body=b, trim=mixc(b, "#000000", 0.12), accent=mixc(b, "#000000", 0.25), win="#4A4C4E", sign="#8C877E", shade=0.22)
    if mode == "night":
        neons = [NEON["rosa"], NEON["cian"], NEON["menta"], NEON["ambar"]]
        return dict(body=night_tint(bodies[i % 4], 0.5), trim=night_tint(bodies[(i - 1) % 4], 0.35), accent=neons[(i + 1) % 4],
                    win="#FFD9A0", sign=neons[i % 4], shade=0.35)
    if mode == "pixel":
        neons = [NEON["rosa"], NEON["cian"], NEON["menta"], NEON["ambar"]]
        return dict(body=night_tint(bodies[i % 4], 0.35), trim=night_tint(bodies[(i - 1) % 4], 0.2), accent=neons[(i + 1) % 4], win="#FFE08A", sign=neons[i % 4], shade=0.3)
    raise KeyError(mode)

def _c(x):  # color hex o skia → skia
    return hexc(x) if isinstance(x, str) else x

def _p(col, a=1.0, **k):
    if isinstance(col, str): return paint(col, a, **k)
    p = paint("#ffffff", a, **k); p.setColor(col); p.setAlphaf(a * (skia.ColorGetA(col) / 255.0)); return p

def _rect(c, x, y, w, h, col, a=1.0, r=0, blur=0, stroke=None):
    pp = _p(col, a, blur=blur, stroke=stroke); rr = skia.Rect.MakeXYWH(x, y, w, h)
    c.drawRoundRect(rr, r, r, pp) if r else c.drawRect(rr, pp)

def facade(c, x, yb, spec, col, t=0.0, mode="pastel", neon=0.0, lights=0.0, s=1.0, outline=None, draw_p=1.0, flicker=0.0):
    """Dibuja un hotel con base en (x, yb). outline=color → solo trazos (plano azul), draw_p = fracción dibujada."""
    w, h = spec["w"] * s, spec["h"] * s
    y0 = yb - h
    if outline:
        _facade_lines(c, x, yb, spec, s, outline, draw_p); return
    body = col["body"]; trim = col["trim"]; acc = col["accent"]
    # torre / escalonado por encima de la cornisa
    top = spec["top"]
    if top in ("tower", "tower_r"):
        tw = w * 0.26; tx = x + (w - tw) / 2 if top == "tower" else x + w * 0.66; th = h * 0.22
        _rect(c, tx, y0 - th, tw, th + 2, body); _rect(c, tx, y0 - th, tw, th, "#000000", col["shade"] * 0.5)
        _rect(c, tx - 6 * s, y0 - th - 10 * s, tw + 12 * s, 12 * s, trim)
        line(c, tx + tw / 2, y0 - th - 10 * s, tx + tw / 2, y0 - th - 70 * s, mixc(trim, "#000000", 0.2) if isinstance(trim, str) else trim, 1, 4 * s)
        circle(c, tx + tw / 2, y0 - th - 74 * s, 7 * s, acc if isinstance(acc, str) else "#ffffff")
        if spec.get("fins") or top == "tower":
            for k in range(3):  # regla de tres: tres aletas verticales
                fx = tx + tw * (0.3 + 0.2 * k); _rect(c, fx - 4 * s, y0 - th + 14 * s, 8 * s, th + h * 0.35, acc, 0.95)
        if spec.get("port"):
            for k in range(spec["port"]):
                py = y0 - th * 0.45 + k * 62 * s; circle(c, tx + tw / 2, py, 19 * s, trim); circle(c, tx + tw / 2, py, 13 * s, col["win"], 0.9 if mode != "night" else 0.5 + 0.5 * lights)
    elif top == "step":
        for k in range(3):
            sw = w * (0.62 - 0.17 * k); _rect(c, x + (w - sw) / 2, y0 - (k + 1) * 22 * s, sw, 24 * s, body)
            _rect(c, x + (w - sw) / 2, y0 - (k + 1) * 22 * s, sw, 5 * s, trim)
    # cuerpo
    _rect(c, x, y0, w, h, body)
    c.drawRect(skia.Rect.MakeXYWH(x, y0, w, h), lin_grad(0, y0, 0, yb, [hexc("#000000", 0.0), hexc("#000000", col["shade"] * 0.8)]))
    if spec.get("corner"):  # esquina redondeada (streamline): banda con degradado
        cw = w * 0.13; cx0 = x if spec["corner"] == "left" else x + w - cw
        cols = [hexc("#ffffff", 0.18), hexc("#000000", 0.18)] if spec["corner"] == "left" else [hexc("#000000", 0.05), hexc("#000000", 0.3)]
        c.drawRect(skia.Rect.MakeXYWH(cx0, y0, cw, h), lin_grad(cx0, 0, cx0 + cw, 0, cols))
    # cornisa y franjas
    _rect(c, x - 6 * s, y0 - 4 * s, w + 12 * s, 14 * s, trim)
    if spec.get("stripes"):  # tres líneas de velocidad
        sx = x + (w * 0.05 if spec.get("corner") == "left" else w * 0.62)
        for k in range(3): _rect(c, sx, y0 + 30 * s + k * 14 * s, w * 0.33, 6 * s, acc, 0.95)
    # pisos y ventanas
    nf = spec["floors"]; gh = h * 0.2; fh = (h - gh - 40 * s) / nf
    nwin = 4 if w / s > 380 else 3
    for f in range(nf):
        fy = y0 + 40 * s + f * fh
        for k in range(nwin):
            ww = w * 0.12; gap = (w - nwin * ww) / (nwin + 1); wx = x + gap + k * (ww + gap)
            if spec.get("glass") and k == nwin - 1:  # columna de bloques de vidrio
                for gy in range(5):
                    for gx in range(2):
                        _rect(c, wx + gx * ww / 2 + 2, fy + 12 * s + gy * fh * 0.13, ww / 2 - 4, fh * 0.11, "#DDEFF2" if mode != "night" else "#9FD8E8", 0.85)
                continue
            lit = 0.0
            if mode in ("night", "pixel"):
                rng_ = (zlib.crc32(f"{spec['name']}{f}{k}".encode()) % 100) / 100.0; lit = lights * (1.0 if rng_ > 0.35 else 0.15)
            winc = col["win"] if mode not in ("night", "pixel") else mixc("#1E2238", col["win"], lit)
            _rect(c, wx, fy + 14 * s, ww, fh * 0.56, winc)
            line(c, wx + ww / 2, fy + 14 * s, wx + ww / 2, fy + 14 * s + fh * 0.56, body, 0.6, 2 * s)
            if spec.get("eyebrows"):  # cejas: viseras de concreto que dan sombra
                _rect(c, wx - 10 * s, fy + 4 * s, ww + 20 * s, 8 * s, trim)
                _rect(c, wx - 6 * s, fy + 12 * s, ww + 12 * s, 7 * s, "#000000", 0.22)
    # planta baja: marquesina y puerta
    gy = yb - gh
    _rect(c, x + w * 0.2, gy + gh * 0.25, w * 0.6, gh * 0.75, mixc(body, "#000000", 0.35) if isinstance(body, str) else body)
    _rect(c, x + w * 0.12, gy, w * 0.76, gh * 0.22, trim, r=6 * s)
    if spec.get("sign") == "canopy":
        tc = col["sign"] if mode in ("night", "pixel") else acc
        draw_text(c, spec["name"], x + w / 2, gy + gh * 0.17, "abril", 30 * s, tc if isinstance(tc, str) else "#ffffff", 1, align="center", glow=(tc, 12 * s) if mode == "night" and neon > 0 else None)
    # letrero vertical de neón
    if spec.get("sign") in ("left", "right", "center"):
        sw = 54 * s; sh = min(h * 0.62, len(spec["name"]) * 62 * s + 30 * s)
        sx = {"left": x + w * 0.08, "right": x + w * 0.8, "center": x + w / 2 - sw / 2}[spec["sign"]]; sy = y0 + 40 * s
        _rect(c, sx, sy, sw, sh, mixc(trim, "#000000", 0.15) if isinstance(trim, str) else trim, r=8 * s)
        on = neon * (1.0 - flicker)
        sc = col["sign"]
        for i, ch in enumerate(spec["name"]):
            cy = sy + 50 * s + i * 60 * s
            if mode in ("night", "pixel") and on > 0:
                draw_text(c, ch, sx + sw / 2, cy, "monoton", 44 * s, sc, on, align="center", glow=(sc, 16 * s))
            else:
                draw_text(c, ch, sx + sw / 2, cy, "monoton", 44 * s, acc if isinstance(acc, str) else "#ffffff", 0.9, align="center")
        if mode in ("night", "pixel") and on > 0:
            c.drawRect(skia.Rect.MakeXYWH(sx - 40 * s, sy - 30 * s, sw + 80 * s, sh + 60 * s), rad_grad(sx + sw / 2, sy + sh / 2, sh * 0.8, [hexc(sc, 0.22 * on), hexc(sc, 0)]))
    # luz de neón rasante sobre la fachada (de noche)
    if mode == "night" and neon > 0:
        c.drawRect(skia.Rect.MakeXYWH(x, y0, w, h), lin_grad(0, yb, 0, y0, [hexc(col["accent"], 0.20 * neon), hexc(col["accent"], 0.0)]))
        _rect(c, x - 6 * s, y0 - 4 * s, w + 12 * s, 4 * s, col["accent"], 0.9 * neon, blur=0)
        _rect(c, x - 6 * s, y0 - 6 * s, w + 12 * s, 8 * s, col["accent"], 0.6 * neon, blur=8 * s)

def _facade_lines(c, x, yb, spec, s, col, p):
    """Versión de plano: el mismo edificio en trazos, dibujado progresivamente."""
    w, h = spec["w"] * s, spec["h"] * s; y0 = yb - h
    paths = []
    def R(xx, yy, ww, hh):
        pth = skia.Path(); pth.addRect(skia.Rect.MakeXYWH(xx, yy, ww, hh)); paths.append(pth)
    def C(cx, cy, r):
        pth = skia.Path(); pth.addCircle(cx, cy, r); paths.append(pth)
    R(x, y0, w, h); R(x - 6 * s, y0 - 4 * s, w + 12 * s, 14 * s)
    top = spec["top"]
    if top in ("tower", "tower_r"):
        tw = w * 0.26; tx = x + (w - tw) / 2 if top == "tower" else x + w * 0.66; th = h * 0.22
        R(tx, y0 - th, tw, th); pth = skia.Path(); pth.moveTo(tx + tw / 2, y0 - th - 10 * s); pth.lineTo(tx + tw / 2, y0 - th - 70 * s); paths.append(pth)
        for k in range(3):
            fx = tx + tw * (0.3 + 0.2 * k); R(fx - 4 * s, y0 - th + 14 * s, 8 * s, th + h * 0.35)
        for k in range(spec.get("port", 0)): C(tx + tw / 2, y0 - th * 0.45 + k * 62 * s, 16 * s)
    elif top == "step":
        for k in range(3):
            sw = w * (0.62 - 0.17 * k); R(x + (w - sw) / 2, y0 - (k + 1) * 22 * s, sw, 22 * s)
    nf = spec["floors"]; gh = h * 0.2; fh = (h - gh - 40 * s) / nf; nwin = 4 if w / s > 380 else 3
    for f in range(nf):
        fy = y0 + 40 * s + f * fh
        for k in range(nwin):
            ww = w * 0.12; gap = (w - nwin * ww) / (nwin + 1); wx = x + gap + k * (ww + gap)
            R(wx, fy + 14 * s, ww, fh * 0.56)
            if spec.get("eyebrows"): R(wx - 10 * s, fy + 4 * s, ww + 20 * s, 8 * s)
    gy = yb - gh; R(x + w * 0.12, gy, w * 0.76, gh * 0.22); R(x + w * 0.2, gy + gh * 0.25, w * 0.6, gh * 0.75)
    if spec.get("stripes"):
        sx = x + (w * 0.05 if spec.get("corner") == "left" else w * 0.62)
        for k in range(3): R(sx, y0 + 30 * s + k * 14 * s, w * 0.33, 6 * s)
    n = len(paths); pp = paint(col, 0.95, stroke=2.2)
    for i, pth in enumerate(paths):
        q = clamp(p * n - i)
        if q <= 0: break
        c.drawPath(partial_path(pth, q), pp)

def hotel_row(c, t, mode, yb=700, x0=70, s=1.0, neon=0.0, lights=0.0, gap=24, outline=None, draw_p=1.0, flick=None, only=None):
    x = x0; xs = []
    for i, sp in enumerate(HOTELS):
        if only is None or i in only:
            fl = 0.0
            if flick is not None and flick[i] > 0: fl = flick[i]
            facade(c, x, yb, sp, hotel_colors(mode, i) if not outline else None, t, mode, neon, lights, s, outline=outline,
                   draw_p=clamp(draw_p * len(HOTELS) - i) if outline else 1.0, flicker=fl)
        xs.append(x); x += sp["w"] * s + gap
    return xs

# ---------------------------------------------------------------- cielo, calle, mar, palmeras, autos
def sky(c, mode, t=0.0, hy=700):
    if mode == "night":
        c.drawRect(skia.Rect.MakeWH(W, hy), lin_grad(0, 0, 0, hy, ["#07061A", "#1C1240", "#3A1A55"]))
        rng = np.random.default_rng(5)
        for i in range(90):
            sx, sy = rng.random() * W, rng.random() * hy * 0.6; tw = 0.5 + 0.5 * math.sin(t * (1 + rng.random() * 2) + i)
            circle(c, sx, sy, 1.2 + rng.random() * 1.2, "#FFFFFF", 0.25 + 0.5 * tw)
        circle(c, 1640, 150, 46, "#FFF3D6", 0.9); circle(c, 1640, 150, 120, "#FFF3D6", 0.10, blur=40)
    elif mode == "dusk":
        c.drawRect(skia.Rect.MakeWH(W, hy), lin_grad(0, 0, 0, hy, ["#2B2A6B", "#C2577E", "#FFB17A"]))
        circle(c, 1500, hy - 60, 110, "#FFE3A3", 0.95); circle(c, 1500, hy - 60, 260, "#FFC46B", 0.25, blur=60)
    elif mode == "day":
        c.drawRect(skia.Rect.MakeWH(W, hy), lin_grad(0, 0, 0, hy, ["#7EC8F2", "#BFE6FA", "#F4F7F2"]))
        for k, (cx, cy) in enumerate(((300, 160), (980, 110), (1500, 200))):
            for j in range(4): circle(c, cx + j * 50 + (t * 6) % 2000 * 0, cy + (j % 2) * 12, 46 - j * 4, "#FFFFFF", 0.85)
    elif mode == "faded":
        c.drawRect(skia.Rect.MakeWH(W, hy), lin_grad(0, 0, 0, hy, ["#9FB4BF", "#C9CFC7", "#E3DCCB"]))
    elif mode == "white":
        c.drawRect(skia.Rect.MakeWH(W, hy), lin_grad(0, 0, 0, hy, ["#C9D6DC", "#E7ECEA", "#F6F4EE"]))

def palm(c, x, yb, h, col="#0B0A14", sway=0.0, a=1.0):
    tr = skia.Path(); tr.moveTo(x - 9, yb); tr.cubicTo(x - 6, yb - h * 0.4, x + 20 + sway * 10, yb - h * 0.75, x + 14 + sway * 30, yb - h)
    tr.lineTo(x + 24 + sway * 30, yb - h); tr.cubicTo(x + 30 + sway * 10, yb - h * 0.75, x + 8, yb - h * 0.4, x + 11, yb); tr.close()
    c.drawPath(tr, paint(col, a))
    cx, cy = x + 19 + sway * 30, yb - h
    for k in range(7):
        ang = -math.pi / 2 + (k - 3) * 0.5 + sway * 0.15; L = h * (0.42 + 0.06 * (k % 2))
        ex, ey = cx + math.cos(ang) * L, cy + math.sin(ang) * L + L * 0.45
        fr = skia.Path(); fr.moveTo(cx, cy)
        mx, my = cx + math.cos(ang) * L * 0.5, cy + math.sin(ang) * L * 0.5 - 20
        fr.quadTo(mx, my - 12, ex, ey); fr.quadTo(mx + 8, my + 10, cx, cy + 6); fr.close()
        c.drawPath(fr, paint(col, a))

def car(c, x, yb, s=1.0, col="#E0E0E0", era=2026, lights=0.0, dirn=1):
    c.save(); c.translate(x, yb); c.scale(s * dirn, s)
    if era < 1950:
        body = skia.Path(); body.moveTo(-90, 0); body.lineTo(-90, -26); body.cubicTo(-70, -34, -50, -36, -40, -38)
        body.cubicTo(-30, -66, 20, -66, 30, -40); body.cubicTo(60, -40, 88, -34, 92, -18); body.lineTo(92, 0); body.close()
    elif era < 2000:
        body = skia.Path(); body.moveTo(-100, 0); body.lineTo(-100, -28); body.lineTo(-60, -34); body.lineTo(-38, -60); body.lineTo(34, -60)
        body.lineTo(58, -34); body.lineTo(100, -30); body.lineTo(100, 0); body.close()
    else:
        body = skia.Path(); body.moveTo(-100, 0); body.lineTo(-100, -24); body.cubicTo(-80, -34, -50, -36, -36, -38); body.cubicTo(-20, -62, 30, -62, 46, -40)
        body.cubicTo(80, -38, 100, -30, 100, -14); body.lineTo(100, 0); body.close()
    c.drawPath(body, paint(col))
    for wx in (-58, 58): circle(c, wx, 0, 17, "#111111"); circle(c, wx, 0, 8, "#777777")
    if lights > 0:
        circle(c, 96, -16, 6, "#FFF6C8", lights)
        c.drawPath(poly([(98, -18), (330, -40), (330, 10), (98, -12)]), paint("#FFF6C8", 0.10 * lights, blur=6))
        circle(c, -97, -16, 5, "#FF3A3A", lights)
    c.restore()

def street(c, t, mode="night", cam=0.0, neon=1.0, lights=1.0, cars=True, flick=None, sky_mode=None, people=None):
    """Calle frente al mar con hoteles art déco (vista desde el parque). mode: night|pastel|white|faded."""
    smode = sky_mode or {"night": "night", "pastel": "day", "white": "white", "faded": "faded", "pixel": "night"}[mode]
    sky(c, smode, t, hy=710)
    c.save(); c.translate(-cam, 0)
    hotel_row(c, t, "night" if mode == "pixel" else mode, yb=700, x0=70, s=1.0, neon=neon, lights=lights, flick=flick)
    c.restore()
    # acera de cemento rojizo, calzada y césped del parque
    side = {"night": "#5B2E3A", "pastel": "#C97B6E", "white": "#BDB7AA", "faded": "#9C8F84", "pixel": "#5B2E3A"}[mode]
    rect(c, 0, 700, W, 22, side)
    rect(c, 0, 722, W, 90, {"night": "#121119", "pastel": "#4A4B52", "white": "#6B6A66", "faded": "#5E5C58", "pixel": "#121119"}[mode])
    for k in range(12):
        line(c, ((k * 190 - t * 60) % (W + 200)) - 100, 768, ((k * 190 - t * 60) % (W + 200)) - 30, 768, "#E8E3D3", 0.55 if mode != "night" else 0.35, 4)
    if cars:
        era = {"night": 2026, "pastel": 1985, "white": 1938, "faded": 1975, "pixel": 1986}[mode]
        ccol = {"night": ["#E8E8F0", "#FF6FB5", "#5BE3FF"], "pastel": ["#FFFFFF", "#F7B7C8", "#2A2A2A"], "white": ["#2B2B2B", "#4A4A4A", "#1E1E1E"],
                "faded": ["#8A7F6E", "#6F6A60", "#A39A88"], "pixel": ["#FF6FB5", "#FFFFFF", "#5BE3FF"]}[mode]
        for k in range(3):
            xx = ((k * 760 + t * (150 + 25 * k)) % (W + 700)) - 300
            car(c, xx, 800, 0.9, ccol[k % 3], era, lights=1.0 if mode in ("night", "pixel") else 0.0)
    rect(c, 0, 812, W, 70, {"night": "#0E2A22", "pastel": "#7BC59A", "white": "#9DB59C", "faded": "#9CA58A", "pixel": "#0E2A22"}[mode])
    sand = {"night": "#2A2236", "pastel": "#F3E2C0", "white": "#ECE3D0", "faded": "#D9CDB4", "pixel": "#2A2236"}[mode]
    c.drawRect(skia.Rect.MakeXYWH(0, 880, W, 200), lin_grad(0, 880, 0, H, [sand, mixc(sand, "#000000", 0.25)]))
    pcol = {"night": "#06050C", "pastel": "#2F5D3A", "white": "#3C4A3E", "faded": "#4F5546", "pixel": "#06050C"}[mode]
    for k, (px, ph) in enumerate(((140, 560), (600, 470), (1180, 520), (1760, 600))):
        palm(c, px - cam * 1.6, 900, ph, pcol, math.sin(t * 0.8 + k) * 0.6)
    if people:
        people(c, t)

# ---------------------------------------------------------------- dispositivos editoriales
LAYERS = [("1912", "ARENA", "#E8D3A2"), ("1930s", "BLANCO", "#F2EFE6"), ("1979", "PROTECCIÓN", "#C9D9C2"), ("1980", "PASTEL", PASTEL["rosa"]),
          ("1984", "TELEVISIÓN", PASTEL["aqua"]), ("2002", "VIDEOJUEGO", "#8E7CFF"), ("2026", "PANTALLAS", NEON["rosa"])]

def cross_section(c, x, y, w, h, n, t=0.0, hl=None, labels=True, a=1.0, scale_txt=1.0):
    """Corte de pintura: n capas visibles (de abajo hacia arriba). hl = índice resaltado."""
    lh = h / len(LAYERS)
    rect(c, x - 10, y - 10, w + 20, h + 20, "#000000", 0.35 * a, r=10)
    for i, (yr, name, col) in enumerate(LAYERS):
        yy = y + h - (i + 1) * lh
        if i < n:
            p = ease_out(clamp(n - i)) if n - i < 1 else 1.0
            rect(c, x, yy + lh * (1 - p), w, lh * p - 2, col, a)
            # borde irregular de capa de pintura
            pth = skia.Path(); pth.moveTo(x, yy + lh * (1 - p))
            for k in range(13): pth.lineTo(x + w * k / 12, yy + lh * (1 - p) + math.sin(k * 1.7 + i) * 2.5)
            c.drawPath(pth, paint("#000000", 0.25 * a, stroke=1.5))
            if labels:
                tc = INK if i not in (5,) else "#FFFFFF"
                draw_text(c, yr, x + 14, yy + lh * 0.64, "ovmono", 17 * scale_txt, tc, 0.85 * a * p)
                draw_text(c, name, x + w - 12, yy + lh * 0.64, "ovmono", 17 * scale_txt, tc, 0.85 * a * p, align="right")
        else:
            rect(c, x, yy, w, lh - 2, "#FFFFFF", 0.10 * a, stroke=1.5)
        if hl == i:
            rect(c, x - 6, yy - 3, w + 12, lh + 2, PAL["amarillo"], a * (0.7 + 0.3 * math.sin(t * 5)), stroke=4, r=4)

def chapter_header(c, t, num, years, title, col="#FFFFFF", d=99.0, n_layers=None, dark=True):
    """Rótulo de capítulo: grande al inicio (≈2,6 s) y luego pequeño en la esquina."""
    p_in = ease_out(prog(t, 0.0, 0.6)); p_small = ease_io(prog(t, 2.4, 3.1))
    a = clamp(min(1, (d - t) / 0.4))
    if p_small < 1:
        k = 1 - p_small
        rect(c, 0, 0, W, H, "#000000", 0.55 * k * p_in if dark else 0)
        cx = W / 2; cy = H * 0.46
        draw_text(c, f"CAPA {num}", cx, cy - 120, "ovmono", 34, col, k * p_in * a, align="center", tracking=8)
        draw_text(c, years, cx, cy + 40 * (1 - p_in) + 30, "monoton", 150, col, k * p_in * a, align="center", glow=(col, 18))
        draw_text(c, title, cx, cy + 140, "abril", 70, col, k * p_in * a, align="center")
    if p_small > 0:
        left = f"CAPA {num} · {years}"; wl = text_w(left, font("ovmono", 26), 2); wt = text_w(title, font("ovsb", 24))
        rect(c, 40, 34, wl + wt + 70, 64, "#000000", 0.5 * p_small * a, r=10)
        draw_text(c, left, 62, 76, "ovmono", 26, col, p_small * a, tracking=2)
        draw_text(c, title, 62 + wl + 26, 76, "ovsb", 24, col, 0.8 * p_small * a)

def quote_card(c, x, y, w, text, sub=None, src=None, t=1.0, col="#FFFFFF", bg="#000000", size=46, font_="dmserif", a=1.0):
    p = ease_out(clamp(t)); a = a * p
    lines = wrap(text, font_, size, w - 80); h = len(lines) * size * 1.22 + 70 + (40 if sub else 0) + (50 if src else 0)
    rect(c, x, y + (1 - p) * 30, w, h, bg, 0.62 * a, r=14)
    draw_text(c, "“", x + 26, y + (1 - p) * 30 + 92, "abril", 120, PAL["amarillo"], a)
    yy = y + (1 - p) * 30 + 40 + size
    for L in lines: draw_text(c, L, x + 70, yy, font_, size, col, a); yy += size * 1.22
    if sub: draw_text(c, sub, x + 70, yy + 6, "inter", 24, col, 0.7 * a); yy += 40
    if src: draw_text(c, src, x + 70, yy + 20, "ovmonomd", 20, PAL["amarillo"], 0.85 * a, tracking=1)
    return h

def name_card(c, x, y, name, role, t, col=PAL["amarillo"], a=1.0, w=None):
    p = ease_out(prog(t, 0, 0.6)); a = a * p
    w = w or max(text_w(name, font("abril", 54)), text_w(role, font("inter", 26))) + 90
    rect(c, x, y, w * p, 130, "#000000", 0.6 * a, r=10); rect(c, x, y, 10, 130, col, a)
    draw_text(c, name, x + 36, y + 64, "abril", 54, "#FFFFFF", a)
    draw_text(c, role, x + 38, y + 106, "inter", 26, "#FFFFFF", 0.78 * a)

def stamp(c, x, y, lines_, t, col="#C8102E", rot=-8, size=44, a=1.0):
    p = prog(t, 0, 0.25)
    if p <= 0: return
    s = 1.6 - 0.6 * ease_out(p); c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    f = font("ovblk", size); wmax = max(text_w(L, f) for L in lines_) + 60; hh = len(lines_) * size * 1.15 + 34
    rect(c, -wmax / 2, -hh / 2, wmax, hh, col, 0.9 * a * p, r=8, stroke=6)
    for i, L in enumerate(lines_):
        draw_text(c, L, 0, -hh / 2 + 20 + (i + 0.82) * size * 1.15 - size * 0.2, "ovblk", size, col, 0.9 * a * p, align="center")
    c.restore()

def paper(c, x, y, w, h, lines_, t, cps=40, size=30, rot=0, a=1.0, title=None):
    c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(rot); c.translate(-w / 2, -h / 2)
    rect(c, 8, 10, w, h, "#000000", 0.35 * a, blur=10)
    rect(c, 0, 0, w, h, "#F4ECD9", a); rect(c, 0, 0, w, h, "#C9B98F", a * 0.6, stroke=2)
    yy = 70
    if title: draw_text(c, title, 40, yy, "elite", size * 1.15, INK, a); yy += size * 1.8
    n = int(max(0, t) * cps); k = 0
    for L in lines_:
        vis = L[:max(0, n - k)]; k += len(L)
        draw_text(c, vis, 40, yy, "elite", size, "#2B2620", a); yy += size * 1.45
    c.restore()

def phone_frame(c, x, y, w, h, t, a=1.0, content=None, rec=True):
    rect(c, x - 10, y - 10, w + 20, h + 20, "#0A0A0F", 0.92 * a, r=36)
    c.save(); pth = skia.Path(); pth.addRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 26, 26); c.clipPath(pth, doAntiAlias=True)
    if content: content(c, x, y, w, h, t)
    c.restore()
    rect(c, x, y, w, h, "#FFFFFF", 0.25 * a, r=26, stroke=2)
    if rec:
        circle(c, x + 30, y + 34, 9, "#FF3A3A", a * (0.5 + 0.5 * (math.sin(t * 6) > 0)))
        draw_text(c, f"REC 00:{int(t) % 60:02d}", x + 48, y + 41, "ovmono", 18, "#FFFFFF", a)
    rect(c, x + w / 2 - 40, y + 10, 80, 8, "#000000", 0.6 * a, r=4)

def crt(c, x, y, w, h, t, content, a=1.0, on=1.0):
    rect(c, x - 40, y - 40, w + 80, h + 120, "#3B2F2A", a, r=40); rect(c, x - 40, y - 40, w + 80, h + 120, "#000000", 0.25 * a, r=40, stroke=6)
    c.save(); pth = skia.Path(); pth.addRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 36, 36); c.clipPath(pth, doAntiAlias=True)
    rect(c, x, y, w, h, "#050505", a)
    if on > 0:
        c.save(); sy = ease_out(clamp(on)); c.translate(x + w / 2, y + h / 2); c.scale(1, max(0.01, sy)); c.translate(-(x + w / 2), -(y + h / 2))
        content(c, x, y, w, h, t); c.restore()
        for yy in range(int(y), int(y + h), 4): line(c, x, yy, x + w, yy, "#000000", 0.13, 1.5, cap="butt")
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), rad_grad(x + w / 2, y + h / 2, w * 0.7, [hexc("#000000", 0), hexc("#000000", 0.0), hexc("#000000", 0.55)], [0, 0.6, 1]))
    c.restore()
    for k in range(2): circle(c, x + w + 0 - 40 + 0 * k, y + h + 40, 12, "#1E1916", a)
    rect(c, x + 30, y + h + 30, 160, 20, "#1E1916", a, r=6)

_PIX = {}
def pixelated(c, draw_fn, factor=4, x=0, y=0, w=W, h=H, t=0.0):
    """Dibuja draw_fn a baja resolución y lo amplía sin suavizado (estética de consola de 2002)."""
    sw, sh = int(w / factor), int(h / factor); key = (sw, sh)
    if key not in _PIX: _PIX[key] = new_surface(sw, sh)
    s = _PIX[key]; cc = s.getCanvas(); cc.clear(skia.ColorBLACK); cc.save(); cc.scale(1 / factor, 1 / factor); draw_fn(cc, t); cc.restore()
    c.drawImageRect(s.makeImageSnapshot(), skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kNearest))

def deco_icon(c, kind, x, y, s, col="#FFFFFF", a=1.0):
    """Iconos de la guía de campo (dibujos propios)."""
    pc = paint(col, a, stroke=5 * s / 60)
    if kind == "cejas":
        for k in range(2):
            rect(c, x - 40 * s / 60, y - 30 * s / 60 + k * 40 * s / 60, 80 * s / 60, 8 * s / 60, col, a)
            rect(c, x - 26 * s / 60, y - 18 * s / 60 + k * 40 * s / 60, 52 * s / 60, 22 * s / 60, col, a * 0.35)
    elif kind == "ojo":
        circle(c, x, y, 34 * s / 60, col, a, stroke=7 * s / 60); circle(c, x, y, 20 * s / 60, col, a * 0.35)
    elif kind == "tres":
        for k in range(3): rect(c, x - 30 * s / 60 + k * 24 * s / 60, y - 40 * s / 60, 10 * s / 60, 80 * s / 60, col, a)
    elif kind == "vidrio":
        for gy in range(3):
            for gx in range(3): rect(c, x - 33 * s / 60 + gx * 23 * s / 60, y - 33 * s / 60 + gy * 23 * s / 60, 19 * s / 60, 19 * s / 60, col, a * 0.8, r=3)
    elif kind == "esquina":
        pth = skia.Path(); pth.moveTo(x - 40 * s / 60, y + 40 * s / 60); pth.lineTo(x - 40 * s / 60, y - 10 * s / 60)
        pth.quadTo(x - 40 * s / 60, y - 40 * s / 60, x - 10 * s / 60, y - 40 * s / 60); pth.lineTo(x + 40 * s / 60, y - 40 * s / 60); c.drawPath(pth, pc)
        for k in range(3): line(c, x - 22 * s / 60, y - 6 * s / 60 + k * 14 * s / 60, x + 34 * s / 60, y - 6 * s / 60 + k * 14 * s / 60, col, a, 4 * s / 60)
    elif kind == "neon":
        rect(c, x - 16 * s / 60, y - 44 * s / 60, 32 * s / 60, 88 * s / 60, col, a, r=6, stroke=5 * s / 60)
        for k, ch in enumerate("ABC"): draw_text(c, ch, x, y - 18 * s / 60 + k * 26 * s / 60, "monoton", 22 * s / 60, col, a, align="center")

def check_box(c, x, y, s, p, col=PAL["verde"], a=1.0):
    rect(c, x, y, s, s, "#FFFFFF", 0.9 * a, r=6, stroke=3)
    if p > 0:
        pth = skia.Path(); pth.moveTo(x + s * 0.2, y + s * 0.55); pth.lineTo(x + s * 0.42, y + s * 0.78); pth.lineTo(x + s * 0.85, y + s * 0.22)
        c.drawPath(partial_path(pth, clamp(p)), paint(col, a, stroke=s * 0.16))
