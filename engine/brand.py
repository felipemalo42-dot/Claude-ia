"""Identidad visual de Caimán Neón: logotipo, avatar, banner y marca de agua (arte original)."""
import math, os, numpy as np, skia
from gfx import *

PAL = {"noche": "#0B0F1E", "pantano": "#10302A", "caiman": "#2BFF88", "flamenco": "#FF4FA0",
       "sol": "#FFC83D", "laguna": "#27D7F2", "hueso": "#F3EFE4", "tinta": "#060812"}

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

def draw_caiman(c, x, y, s, t=0.0, line_col=PAL["caiman"], eye_col=PAL["flamenco"], fill=None, glow=True, lw=3.2, open_=0.0, a=1.0):
    """Dibuja el caimán neón. (x, y) = esquina sup. izq. del espacio 200x100 escalado por s."""
    c.save(); c.translate(x, y); c.scale(s, s)
    up = svg_path(HEAD_UP); lo = svg_path(HEAD_LO); eye = svg_path(EYE)
    # mandíbula inferior gira sobre la articulación al abrir
    c.save(); c.translate(40, 60); c.rotate(open_ * 14); c.translate(-40, -60)
    if fill: c.drawPath(lo, paint(fill, a))
    for tp in teeth_lo(): c.drawPath(poly(tp), paint(PAL["hueso"], a))
    if glow: c.drawPath(lo, paint(line_col, 0.55 * a, stroke=lw * 3.2, blur=6 / s))
    c.drawPath(lo, paint(line_col, a, stroke=lw))
    c.restore()
    if fill: c.drawPath(up, paint(fill, a))
    for tp in teeth_up(): c.drawPath(poly(tp), paint(PAL["hueso"], a))
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
    c.drawPath(poly([(66, 22), (68.8, 31), (66, 40), (63.2, 31)]), paint(PAL["tinta"], a))
    c.restore()
    c.restore()

def wordmark(c, x, y, size, a=1.0, glow=True, col=PAL["hueso"], accent=PAL["caiman"]):
    """'CAIMÁN NEÓN' con NEÓN en tubo de neón."""
    w1 = draw_text(c, "CAIMÁN", x, y, "anton", size, col, a, tracking=size * 0.02)
    gx = x + w1 + size * 0.22
    if glow: draw_text(c, "NEÓN", gx, y, "anton", size, accent, a * 0.9, tracking=size * 0.02, p=paint(accent, a * 0.7, blur=size * 0.08))
    draw_text(c, "NEÓN", gx, y, "anton", size, accent, a, tracking=size * 0.02)
    return gx + text_w("NEÓN", font("anton", size), size * 0.02) - x

def save(surface, path):
    img = surface.makeImageSnapshot(); img.save(path, skia.kPNG)

def bg_swamp(c, w, h, seed=2):
    c.drawRect(skia.Rect.MakeWH(w, h), lin_grad(0, 0, 0, h, [PAL["noche"], "#0C1A24", PAL["pantano"]], [0, 0.6, 1]))
    rng = np.random.default_rng(seed)
    # olas/ondas del pantano (líneas horizontales finas)
    for i in range(26):
        yy = h * 0.62 + i * (h * 0.38 / 26); amp = 3 + i * 0.6
        pth = skia.Path(); pth.moveTo(0, yy)
        for xx in range(0, w + 40, 40): pth.lineTo(xx, yy + math.sin(xx * 0.01 + i) * amp)
        c.drawPath(pth, paint(PAL["laguna"], 0.05 + 0.004 * i, stroke=1.2))
    c.drawCircle(w * 0.78, h * 0.3, h * 0.55, rad_grad(w * 0.78, h * 0.3, h * 0.55, [hexc(PAL["flamenco"], 0.22), hexc(PAL["flamenco"], 0)]))
    c.drawCircle(w * 0.2, h * 0.75, h * 0.6, rad_grad(w * 0.2, h * 0.75, h * 0.6, [hexc(PAL["caiman"], 0.12), hexc(PAL["caiman"], 0)]))

def make_all(out):
    os.makedirs(out, exist_ok=True)
    # 1) Logotipo horizontal transparente
    W, H = 2600, 640; s = new_surface(W, H); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    draw_caiman(c, 40, 90, 4.4, lw=3.0)
    wordmark(c, 980, 390, 270)
    draw_text(c, "GTA VI EN ESPAÑOL · LO OFICIAL, LO DEDUCIDO Y EL RUMOR, SEPARADOS", 990, 520, "monob", 38, PAL["hueso"], 0.85, tracking=2)
    save(s, f"{out}/logo_horizontal_transparente.png")
    # 1b) versión sobre fondo oscuro
    s = new_surface(W, H); c = s.getCanvas(); bg_swamp(c, W, H)
    draw_caiman(c, 40, 90, 4.4, lw=3.0); wordmark(c, 980, 390, 270)
    draw_text(c, "GTA VI EN ESPAÑOL · LO OFICIAL, LO DEDUCIDO Y EL RUMOR, SEPARADOS", 990, 520, "monob", 38, PAL["hueso"], 0.85, tracking=2)
    save(s, f"{out}/logo_horizontal_fondo.png")
    # 2) Avatar 800x800
    s = new_surface(800, 800); c = s.getCanvas()
    c.drawRect(skia.Rect.MakeWH(800, 800), rad_grad(400, 360, 560, [hexc("#173A33"), hexc(PAL["noche"])]))
    c.drawCircle(400, 400, 360, paint(PAL["caiman"], 0.25, stroke=6))
    c.drawCircle(400, 400, 300, rad_grad(400, 400, 300, [hexc(PAL["flamenco"], 0.16), hexc(PAL["flamenco"], 0)]))
    draw_caiman(c, 22, 215, 3.78, lw=3.6)
    save(s, f"{out}/avatar_800x800.png")
    # 3) Banner 2560x1440 (zona segura central 1546x423)
    W, H = 2560, 1440; s = new_surface(W, H); c = s.getCanvas(); bg_swamp(c, W, H, 5)
    grid(c, W, H, 64, PAL["laguna"], 0.035)
    sx, sy, sw, sh = (W - 1546) / 2, (H - 423) / 2, 1546, 423
    draw_caiman(c, sx - 10, sy + 40, 2.9, lw=3.2)
    wordmark(c, sx + 600, sy + 220, 170)
    draw_text(c, "GUÍAS · MAPAS · ANÁLISIS · MISTERIOS", sx + 606, sy + 300, "monob", 34, PAL["hueso"], 0.9, tracking=3)
    # semáforo de certeza (seña de identidad)
    xx = sx + 606
    for lab, col in (("OFICIAL", PAL["caiman"]), ("DEDUCCIÓN", PAL["sol"]), ("RUMOR", PAL["flamenco"])):
        wlab = text_w(lab, font("monob", 26), 2) + 36
        rect(c, xx, sy + 330, wlab, 46, col, 0.16, r=23); rect(c, xx, sy + 330, wlab, 46, col, 1, r=23, stroke=2.5)
        draw_text(c, lab, xx + 18, sy + 362, "monob", 26, col, 1, tracking=2); xx += wlab + 18
    draw_text(c, "NUEVOS VIDEOS · MAR · JUE · SÁB", W - sx, sy - 30, "monob", 28, PAL["sol"], 0.9, align="right", tracking=3)
    save(s, f"{out}/banner_2560x1440.png")
    # 4) Marca de agua 150x150 (transparente)
    s = new_surface(150, 150); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    c.drawCircle(75, 75, 72, paint(PAL["noche"], 0.85)); c.drawCircle(75, 75, 70, paint(PAL["caiman"], 0.9, stroke=3))
    draw_caiman(c, 8, 38, 0.67, lw=4.5, glow=False)
    save(s, f"{out}/marca_de_agua_150x150.png")
    # 5) Paleta
    W, H = 2000, 900; s = new_surface(W, H); c = s.getCanvas(); c.clear(hexc(PAL["tinta"]))
    draw_text(c, "PALETA CAIMÁN NEÓN", 80, 120, "anton", 80, PAL["hueso"])
    names = [("Noche", "noche"), ("Pantano", "pantano"), ("Caimán", "caiman"), ("Flamenco", "flamenco"), ("Sol", "sol"), ("Laguna", "laguna"), ("Hueso", "hueso")]
    for i, (lab, k) in enumerate(names):
        x = 80 + i * 266; rect(c, x, 190, 240, 420, PAL[k], 1, r=18); rect(c, x, 190, 240, 420, "#ffffff", 0.15, r=18, stroke=2)
        draw_text(c, lab.upper(), x, 670, "anton", 46, PAL["hueso"]); draw_text(c, PAL[k], x, 720, "mono", 30, PAL["hueso"], 0.8)
    draw_text(c, "Semáforo de certeza: Caimán = OFICIAL · Sol = DEDUCCIÓN · Flamenco = RUMOR", 80, 820, "intersb", 34, PAL["hueso"], 0.9)
    save(s, f"{out}/paleta.png")
    # 6) Tipografía
    W, H = 2000, 1000; s = new_surface(W, H); c = s.getCanvas(); c.clear(hexc(PAL["noche"]))
    draw_text(c, "Anton — Titulares y miniaturas", 80, 140, "anton", 90, PAL["hueso"])
    draw_text(c, "Inter — Texto, subtítulos y rótulos de apoyo", 80, 290, "interb", 64, PAL["hueso"])
    draw_text(c, "JetBrains Mono — DATOS, ETIQUETAS, FUENTES", 80, 420, "monob", 58, PAL["caiman"])
    draw_text(c, "Tipografías por formato (todas con licencia OFL/Apache 2.0):", 80, 560, "intersb", 40, PAL["sol"])
    y = 640
    for nm, f in (("Barlow Condensed (Kit de lanzamiento)", "barlowblk"), ("Share Tech Mono (Investigación)", "techmono"),
                  ("DM Serif Display (Mapas)", "dmserif"), ("Special Elite (Expedientes)", "elite"), ("Bungee (Shorts juego)", "bungee"),
                  ("Abril Fatface (Guía de campo)", "abril"), ("Syne (Misterios)", "syne")):
        draw_text(c, nm, 80 + (0 if y < 900 else 960), y if y < 900 else y - 300, f, 40, PAL["hueso"]); y += 50
    save(s, f"{out}/tipografia.png")

if __name__ == "__main__":
    import sys
    make_all(sys.argv[1] if len(sys.argv) > 1 else "../CANAL_IDENTIDAD")
