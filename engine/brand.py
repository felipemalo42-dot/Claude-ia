"""Identidad visual de SAL Y ASFALTO: emblema, wordmark, avatar, banner y marca de agua (arte original).

Concepto: una carretera que cruza el mar hacia el horizonte (la sal del mar y el asfalto de la calle),
estética de señalización vial: asfalto, blanco sal, amarillo de línea de carril y verde de señal de autopista.
El 'semáforo de certeza' (OFICIAL / DEDUCCIÓN / RUMOR) es literalmente un semáforo.
"""
import math, os, numpy as np, skia
from gfx import *

PAL = {
    # identidad nueva
    "asfalto": "#16181B", "asfalto2": "#25282D", "sal": "#F3F0E9", "amarillo": "#FFC72C", "mar": "#13A8A0", "mar2": "#0B5E63",
    "senal": "#0B6B45", "verde": "#22C55E", "ambar": "#FFB000", "rojo": "#FF4A3D", "cielo": "#FFE3A3",
    # alias heredados (los módulos de cada video los usan como acentos semánticos)
    "noche": "#16181B", "pantano": "#25282D", "caiman": "#22C55E", "flamenco": "#FF4A3D", "sol": "#FFB000",
    "laguna": "#13A8A0", "hueso": "#F3F0E9", "tinta": "#0D0E10",
}
BRAND = "SAL Y ASFALTO"; BRAND_TITLE = "Sal y Asfalto"; HANDLE = "@SalYAsfalto"

# Cabeza de caimán de perfil (espacio 200x100): mandíbula superior, inferior, ojo, dientes, narina
HEAD_UP = "M22 52 C24 40 32 32 44 30 C48 18 60 12 72 14 C80 16 84 22 86 30 L160 34 C166 28 176 28 182 33 C190 36 196 42 196 48 C196 52 192 54 186 54 L48 56 Z"
HEAD_LO = "M44 63 L184 62 C188 62 190 65 188 68 C184 72 174 74 160 74 L70 78 C52 78 36 74 26 66 Z"
EYE = "M66 20 C72 20 77 25 77 31 C77 37 72 41 66 41 C60 41 55 37 55 31 C55 25 60 20 66 20 Z"

def teeth_up():
    pts = []
    for i, x in enumerate(range(70, 182, 14)):
        pts.append([(x, 55.5), (x + 4, 63 if i % 2 == 0 else 61), (x + 8, 55.5)])
    return pts
def teeth_lo():
    pts = []
    for i, x in enumerate(range(77, 178, 14)):
        pts.append([(x, 62.5), (x + 4, 56.5 if i % 2 == 0 else 58), (x + 8, 62.5)])
    return pts

def draw_caiman(c, x, y, s, t=0.0, line_col="#2BFF88", eye_col="#FF4FA0", fill=None, glow=True, lw=3.2, open_=0.0, a=1.0):
    """Ilustración de cabeza de caimán (se usa como dibujo de animal en el VIDEO 08; ya NO es el logotipo). (x, y) = esquina sup. izq. del espacio 200x100 escalado por s."""
    c.save(); c.translate(x, y); c.scale(s, s)
    up = svg_path(HEAD_UP); lo = svg_path(HEAD_LO); eye = svg_path(EYE)
    # mandíbula inferior gira sobre la articulación al abrir
    c.save(); c.translate(40, 60); c.rotate(open_ * 14); c.translate(-40, -60)
    if fill: c.drawPath(lo, paint(fill, a))
    for tp in teeth_lo(): c.drawPath(poly(tp), paint("#F3EFE4", a))
    if glow: c.drawPath(lo, paint(line_col, 0.55 * a, stroke=lw * 3.2, blur=6 / s))
    c.drawPath(lo, paint(line_col, a, stroke=lw))
    c.restore()
    if fill: c.drawPath(up, paint(fill, a))
    for tp in teeth_up(): c.drawPath(poly(tp), paint("#F3EFE4", a))
    if glow: c.drawPath(up, paint(line_col, 0.55 * a, stroke=lw * 3.2, blur=6 / s))
    c.drawPath(up, paint(line_col, a, stroke=lw))
    # escamas del lomo (detalle)
    for i, xx in enumerate(range(96, 156, 12)):
        c.drawLine(xx, 37 - (i % 2), xx + 6, 37 - (i % 2), paint(line_col, 0.6 * a, stroke=lw * 0.6))
    # narina
    c.drawCircle(184, 38, 2.6, paint(line_col, a))
    # ojo flamenco con pupila rasgada y parpadeo
    blink = 0.15 if (t % 4.0) > 3.86 else 1.0
    c.save(); c.translate(66, 31); c.scale(1, blink); c.translate(-66, -31)
    if glow: c.drawPath(eye, paint(eye_col, 0.7 * a, blur=5 / s))
    c.drawPath(eye, paint(eye_col, a))
    c.drawPath(poly([(66, 22), (68.8, 31), (66, 40), (63.2, 31)]), paint("#060812", a))
    c.restore()
    c.restore()

def draw_badge(c, cx, cy, r, t=0.0, a=1.0, ring=True, speed=1.0):
    """Emblema: carretera sobre el mar hacia el sol del horizonte (inspirado en las carreteras costeras, sin marca ajena)."""
    c.save(); pth = skia.Path(); pth.addCircle(cx, cy, r); c.clipPath(pth, doAntiAlias=True)
    hy = cy - 0.12 * r
    c.drawRect(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, hy - (cy - r)), lin_grad(0, cy - r, 0, hy, [hexc("#FFF4DA", a), hexc(PAL["cielo"], a)]))
    c.drawCircle(cx, hy, 0.34 * r, paint(PAL["amarillo"], a))
    c.drawRect(skia.Rect.MakeXYWH(cx - r, hy, 2 * r, cy + r - hy), lin_grad(0, hy, 0, cy + r, [hexc(PAL["mar"], a), hexc(PAL["mar2"], a)]))
    for k in range(4):  # olas
        yy = hy + (cy + r - hy) * (0.18 + k * 0.2); amp = 0.012 * r * (1 + k)
        w = skia.Path(); w.moveTo(cx - r, yy)
        for xx in np.linspace(cx - r, cx + r, 24): w.lineTo(xx, yy + math.sin((xx - cx) / r * 9 + t * 2 + k) * amp)
        c.drawPath(w, paint(PAL["sal"], 0.35 * a, stroke=max(1, 0.018 * r)))
    # carretera en perspectiva
    road = poly([(cx - 0.02 * r, hy), (cx + 0.02 * r, hy), (cx + 0.62 * r, cy + r), (cx - 0.62 * r, cy + r)])
    c.drawPath(road, paint(PAL["asfalto2"], a))
    for sgn in (-1, 1):
        c.drawPath(poly([(cx + sgn * 0.02 * r, hy), (cx + sgn * 0.62 * r, cy + r)], False), paint(PAL["sal"], a, stroke=max(1, 0.035 * r)))
    # línea amarilla discontinua que avanza
    ph = (t * 0.9 * speed) % 1.0
    for k in range(7):
        u0 = ((k + ph) / 7) ** 1.8; u1 = ((k + ph + 0.45) / 7) ** 1.8
        y0 = hy + (cy + r - hy) * u0; y1 = hy + (cy + r - hy) * min(1, u1)
        w0 = 0.004 * r + 0.045 * r * u0; w1 = 0.004 * r + 0.045 * r * min(1, u1)
        c.drawPath(poly([(cx - w0, y0), (cx + w0, y0), (cx + w1, y1), (cx - w1, y1)]), paint(PAL["amarillo"], a))
    c.restore()
    if ring:
        circle(c, cx, cy, r, PAL["sal"], a, stroke=0.075 * r)
        circle(c, cx, cy, r + 0.06 * r, PAL["asfalto"], a, stroke=0.04 * r)

def wordmark(c, x, y, size, a=1.0, col=None, accent=None, align="left", stacked=False):
    """'SAL Y ASFALTO' en Overpass Black; la 'Y' en amarillo de carril."""
    col = col or PAL["sal"]; accent = accent or PAL["amarillo"]; f = font("ovblk", size); tr = size * 0.02
    parts = [("SAL ", col), ("Y", accent), (" ASFALTO", col)]
    w = sum(text_w(p, f, tr) for p, _ in parts) + tr * 2
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    xx = x
    for p, cl in parts: xx += draw_text(c, p, xx, y, "ovblk", size, cl, a, tracking=tr) + tr
    return w

def guide_sign(c, x, y, w, h, a=1.0, col=None, r=None):
    """Panel tipo señal de autopista (verde con borde blanco). Diseño genérico."""
    col = col or PAL["senal"]; r = r or h * 0.12
    rect(c, x + 6, y + 10, w, h, "#000000", 0.35 * a, r=r, blur=8)
    rect(c, x, y, w, h, col, a, r=r); rect(c, x + h * 0.06, y + h * 0.06, w - h * 0.12, h - h * 0.12, PAL["sal"], a, r=r * 0.7, stroke=max(2, h * 0.035))

def traffic_light(c, x, y, h, lit, a=1.0):
    """Semáforo vertical pequeño. lit: 0 verde, 1 ámbar, 2 rojo (de abajo arriba: verde, ámbar, rojo)."""
    w = h * 0.42; rect(c, x, y, w, h, "#0D0E10", a, r=w * 0.3); rect(c, x, y, w, h, PAL["sal"], 0.5 * a, r=w * 0.3, stroke=max(1, h * 0.03))
    cols = [PAL["rojo"], PAL["ambar"], PAL["verde"]]
    for i in range(3):
        on = (2 - i) == lit; cy = y + h * (0.2 + i * 0.3)
        if on: circle(c, x + w / 2, cy, w * 0.42, cols[i], 0.35 * a, blur=w * 0.25)
        circle(c, x + w / 2, cy, w * 0.3, cols[i] if on else "#2A2D31", a)

def save(surface, path):
    surface.makeImageSnapshot().save(path, skia.kPNG)

def coast_scene(c, W, H, t=0.0, hy=None, road=True, sun=True):
    """Ilustración plana: carretera costera al atardecer (para banner y cortinilla)."""
    hy = hy if hy is not None else H * 0.52
    c.drawRect(skia.Rect.MakeWH(W, hy), lin_grad(0, 0, 0, hy, ["#1B2A3A", "#4A4E69", "#C9A27E", "#FFD39A"], [0, 0.45, 0.85, 1]))
    if sun:
        c.drawCircle(W * 0.62, hy, H * 0.16, rad_grad(W * 0.62, hy, H * 0.45, [hexc(PAL["amarillo"], 0.55), hexc(PAL["amarillo"], 0)]))
        c.drawCircle(W * 0.62, hy, H * 0.11, paint(PAL["amarillo"]))
    c.drawRect(skia.Rect.MakeXYWH(0, hy, W, H - hy), lin_grad(0, hy, 0, H, [PAL["mar"], PAL["mar2"], "#06292C"]))
    for k in range(14):
        yy = hy + (H - hy) * (k / 14) ** 1.6; amp = 2 + k * 1.4
        w = skia.Path(); w.moveTo(0, yy)
        for xx in range(0, W + 40, 40): w.lineTo(xx, yy + math.sin(xx * 0.01 + t * 1.5 + k) * amp)
        c.drawPath(w, paint(PAL["sal"], 0.10 + 0.01 * k, stroke=1.5 + k * 0.15))
    c.drawRect(skia.Rect.MakeXYWH(0, hy - 2, W, 4), paint(PAL["sal"], 0.6))
    if road:
        vx = W * 0.62; L = W * 0.08; Rr = W * 0.98
        c.drawPath(poly([(vx - 4, hy), (vx + 4, hy), (Rr, H), (L, H)]), paint(PAL["asfalto2"]))
        for xb in (vx - 4, vx + 4):
            c.drawPath(poly([(xb, hy), (L if xb < vx else Rr, H)], False), paint(PAL["sal"], 0.9, stroke=6))
        ph = (t * 1.2) % 1.0
        for k in range(10):
            u0 = ((k + ph) / 10) ** 2; u1 = ((k + ph + 0.45) / 10) ** 2
            y0 = hy + (H - hy) * u0; y1 = hy + (H - hy) * min(1, u1)
            x0 = vx + ((L + Rr) / 2 - vx) * u0; x1 = vx + ((L + Rr) / 2 - vx) * min(1, u1)
            w0 = 1 + 18 * u0; w1 = 1 + 18 * min(1, u1)
            c.drawPath(poly([(x0 - w0, y0), (x0 + w0, y0), (x1 + w1, y1), (x1 - w1, y1)]), paint(PAL["amarillo"]))
        # postes de baranda
        for k in range(16):
            u = (k / 16) ** 2; yy = hy + (H - hy) * u; xx = vx + (L - vx) * u - 10 - 30 * u
            rect(c, xx, yy - 30 * u - 4, 2 + 6 * u, 30 * u + 4, "#D9D4C7", 0.8)

def make_all(out):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".png"): os.remove(os.path.join(out, f))
    # 1) Logotipo horizontal (transparente y sobre fondo)
    for name, bg in (("logo_horizontal_transparente.png", False), ("logo_horizontal_fondo.png", True)):
        W, H = 2600, 640; s = new_surface(W, H); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        if bg: c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [PAL["asfalto"], PAL["asfalto2"]]))
        draw_badge(c, 330, 320, 250)
        wordmark(c, 660, 380, 230, col=PAL["sal"] if bg else PAL["asfalto"])
        draw_text(c, "GTA VI EN ESPAÑOL · LO OFICIAL, LO DEDUCIDO Y EL RUMOR, SEPARADOS", 668, 490, "ovmono", 40, PAL["sal"] if bg else PAL["asfalto"], 0.85, tracking=1)
        rect(c, 668, 525, 1700, 10, PAL["amarillo"], 1)
        save(s, f"{out}/{name}")
    # 2) Avatar
    s = new_surface(800, 800); c = s.getCanvas(); c.clear(hexc(PAL["asfalto"]))
    draw_badge(c, 400, 400, 330)
    save(s, f"{out}/avatar_800x800.png")
    # 3) Banner 2560x1440 (zona segura 1546x423 centrada)
    W, H = 2560, 1440; s = new_surface(W, H); c = s.getCanvas(); coast_scene(c, W, H, 0.0, hy=H * 0.5)
    rect(c, 0, 0, W, H, "#000000", 0.18)
    sx, sy, sw, sh = (W - 1546) / 2, (H - 423) / 2, 1546, 423
    guide_sign(c, sx, sy + 20, sw, 300)
    draw_badge(c, sx + 150, sy + 170, 105)
    wordmark(c, sx + 290, sy + 215, 120)
    draw_text(c, "GTA VI EN ESPAÑOL · GUÍAS · MAPAS · ANÁLISIS", sx + 296, sy + 280, "ovmono", 34, PAL["sal"], 0.95, tracking=1)
    xx = sx + 300
    for lit, lab in ((0, "OFICIAL"), (1, "DEDUCCIÓN"), (2, "RUMOR")):
        traffic_light(c, xx, sy + 340, 80, lit); draw_text(c, lab, xx + 50, sy + 395, "ovb", 36, PAL["sal"], 1, stroke=6, stroke_color="#000000"); xx += 330
    rect(c, W - sx - 600, sy - 72, 600, 62, PAL["amarillo"], 1, r=8)
    draw_text(c, "NUEVOS VIDEOS · MAR · JUE · SÁB", W - sx - 300, sy - 30, "ovb", 30, PAL["asfalto"], 1, align="center")
    save(s, f"{out}/banner_2560x1440.png")
    # 4) Marca de agua
    s = new_surface(150, 150); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT); draw_badge(c, 75, 75, 66); save(s, f"{out}/marca_de_agua_150x150.png")
    # 5) Paleta
    W, H = 2200, 900; s = new_surface(W, H); c = s.getCanvas(); c.clear(hexc(PAL["asfalto"]))
    draw_text(c, "PALETA SAL Y ASFALTO", 80, 120, "ovblk", 80, PAL["sal"])
    names = [("Asfalto", "asfalto"), ("Asfalto 2", "asfalto2"), ("Sal", "sal"), ("Amarillo carril", "amarillo"), ("Mar", "mar"), ("Señal", "senal"), ("Verde", "verde"), ("Ámbar", "ambar"), ("Rojo", "rojo")]
    for i, (lab, k) in enumerate(names):
        x = 80 + i * 228; rect(c, x, 190, 205, 420, PAL[k], 1, r=14); rect(c, x, 190, 205, 420, "#ffffff", 0.2, r=14, stroke=2)
        draw_text(c, lab.upper(), x, 670, "ovb", 30, PAL["sal"]); draw_text(c, PAL[k], x, 715, "ovmonomd", 28, PAL["sal"], 0.8)
    draw_text(c, "Semáforo de certeza: verde = OFICIAL · ámbar = DEDUCCIÓN · rojo = RUMOR", 80, 820, "ovsb", 36, PAL["sal"], 0.9)
    save(s, f"{out}/paleta.png")
    # 6) Tipografía
    W, H = 2000, 900; s = new_surface(W, H); c = s.getCanvas(); c.clear(hexc(PAL["asfalto"]))
    draw_text(c, "Overpass Black — titulares y miniaturas", 80, 140, "ovblk", 76, PAL["sal"])
    draw_text(c, "Inter — texto y subtítulos", 80, 270, "interb", 64, PAL["sal"])
    draw_text(c, "OVERPASS MONO — DATOS, ETIQUETAS, FUENTES", 80, 390, "ovmono", 56, PAL["amarillo"])
    draw_text(c, "Overpass deriva de la tipografía de señalización vial de EE. UU. (licencia SIL OFL).", 80, 500, "ovsb", 38, PAL["sal"], 0.85)
    draw_text(c, "Cada formato conserva su tipografía de acento (ver GUIA_DE_MARCA.md).", 80, 570, "ovsb", 38, PAL["sal"], 0.85)
    save(s, f"{out}/tipografia.png")

if __name__ == "__main__":
    import sys
    make_all(sys.argv[1] if len(sys.argv) > 1 else "../CANAL_IDENTIDAD")
