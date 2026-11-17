"""VIDEO 07 — SHORT: GTA 6 pesa 210 GB, ¿te cabe en tu consola?
Lenguaje visual: concurso de TV / videojuego arcade: tanques de almacenamiento verticales, bloque de 210 GB que cae
como pieza de puzle, sellos '¡CABE!', confeti. Paleta violeta/amarillo/cian, tipografía Bungee. Música chiptune original.
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL, draw_caiman, draw_badge

W, H = 1080, 1920
VIO1, VIO2 = "#2A0F5E", "#140632"; YEL = "#FFD23F"; CY = "#3EE6FF"; PINK = "#FF4FA0"; GRN = PAL["caiman"]; RED = "#FF4A3D"; WH = "#FFFFFF"

CONSOLES = [("PS5", "825 GB", 667, "PS5 original"), ("SERIES S", "512 GB", 364, "Series S"), ("SERIES X", "1 TB", 802, "Series X"), ("PS5 SLIM", "1 TB", 840, "Slim")]

def bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [VIO1, VIO2]))
    for i in range(12):  # rayos de concurso
        ang = t * 0.15 + i * math.pi / 6
        pth = poly([(W / 2, 700), (W / 2 + math.cos(ang) * 1600, 700 + math.sin(ang) * 1600), (W / 2 + math.cos(ang + 0.18) * 1600, 700 + math.sin(ang + 0.18) * 1600)])
        c.drawPath(pth, paint("#FFFFFF", 0.035))
    for i in range(0, W, 60):
        for j in range(0, H, 60): circle(c, i + 30, j + 30, 2, "#FFFFFF", 0.06)

def tank(c, x, y, w, h, cap, used, label, sub, t, st, verdict):
    p = ease_out_back(prog(t, st, st + 0.4))
    if p <= 0: return
    c.save(); c.translate(x + w / 2, y + h); c.scale(p, p); c.translate(-(x + w / 2), -(y + h))
    rect(c, x + 10, y + 14, w, h, "#000000", 0.4, r=26)
    rect(c, x, y, w, h, "#0E0828", 1, r=26); rect(c, x, y, w, h, WH, 1, r=26, stroke=6)
    # bloque que cae
    drop = ease_out(prog(t, st + 0.5, st + 1.1)); bh = (h - 20) * used / cap
    by = lerp(y - 700, y + h - 10 - bh, drop)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x - 40, 0, w + 80, y + h));
    col = RED if used / cap > 0.5 else GRN
    rect(c, x + 10, by, w - 20, bh, col, 1, r=16); rect(c, x + 10, by, w - 20, 16, "#FFFFFF", 0.35, r=8)
    draw_text(c, "GTA VI", x + w / 2, by + bh / 2 + 16, "bungee", 46, "#000000", 1, align="center")
    c.restore()
    draw_text(c, label, x + w / 2, y - 70, "bungee", 58, YEL, 1, align="center", stroke=8, stroke_color="#000000")
    draw_text(c, f"{sub} · {cap} libres", x + w / 2, y - 22, "monob", 30, WH, 0.9, align="center")
    if drop >= 1:
        pct = int(round(100 * used / cap)); pv = ease_out_back(prog(t, st + 1.1, st + 1.4))
        draw_text(c, f"{pct}%", x + w / 2, y + 105, "bungee", 96 * pv, WH, 1, align="center", stroke=10, stroke_color="#000000")
        if verdict:
            c.save(); c.translate(x + w / 2, y + h + 95); c.rotate(-4); c.scale(pv, pv)
            vcol = GRN if "SOBRA" in verdict or "DRAMA" in verdict or "HOLGADO" in verdict else (YEL if "JUSTO" in verdict else RED)
            rect(c, -330, -60, 660, 120, vcol, 1, r=24); draw_text(c, verdict, 0, 26, "bungee", 62, "#000000", 1, align="center")
            c.restore()
    c.restore()

def confetti(c, t, t0, seed=1):
    if t < t0 or t > t0 + 2.5: return
    rng = np.random.default_rng(seed); dt = t - t0
    for i in range(60):
        x = W / 2 + rng.normal(0, 1) * 300 + rng.normal(0, 1) * 200 * dt; y = 500 - 700 * dt * rng.random() + 900 * dt * dt
        col = [YEL, CY, PINK, GRN][i % 4]; c.save(); c.translate(x, y); c.rotate(dt * 400 * rng.random()); rect(c, -10, -5, 20, 10, col, clamp(2.5 - dt)); c.restore()

def sc_main(c, t, info, ctx):
    bg(c, t)
    # título
    p = ease_out_back(prog(t, 0, 0.5))
    c.save(); c.translate(W / 2, 270); c.scale(p, p)
    draw_text(c, "210 GB", 0, 0, "bungee", 170, YEL, 1, align="center", stroke=14, stroke_color="#000000")
    draw_text(c, "¿TE CABE?", 0, 130, "bungee", 110, WH, 1, align="center", stroke=12, stroke_color="#000000")
    c.restore()
    cues = [info.w("PS5 original"), info.w("Series S"), info.w("Series X"), info.w("Slim")]
    verdicts = ["TE SOBRA", "JUSTO: 58%", "SIN DRAMA", "HOLGADO"]
    # mostrar de a una consola, grande
    cur = None
    for i, cu in enumerate(cues):
        if t >= cu - 0.2: cur = i
    if cur is not None and t < info.w("truco") - 0.2:
        name, sub, cap, _ = CONSOLES[cur]
        tank(c, W / 2 - 200, 690, 400, 500, cap, 210, name, sub, t, cues[cur] - 0.2, verdicts[cur])
        # miniaturas de las ya vistas
        for j in range(cur):
            nm = CONSOLES[j][0]; rect(c, 75 + j * 240, 440, 210, 64, "#000000", 0.5, r=32)
            draw_text(c, nm, 180 + j * 240, 483, "bungee", 26, GRN if j != 1 else YEL, 1, align="center")
    st = info.w("truco")
    if t >= st - 0.2 and t < info.w("PS4") - 0.2:
        pp = ease_out_back(prog(t, st - 0.2, st + 0.3))
        c.save(); c.translate(W / 2, 880); c.scale(pp, pp)
        rect(c, -460, -260, 920, 520, "#0E0828", 1, r=30); rect(c, -460, -260, 920, 520, CY, 1, r=30, stroke=6)
        icon(c, "disk", 0, -120, 160, CY)
        draw_par(c, "Revisa tu espacio libre HOY", -400, 40, "bungee", 64, 800, color=WH, lh=1.05)
        draw_text(c, "(lo que ya tienes instalado cuenta)", 0, 210, "monob", 30, CY, 1, align="center")
        c.restore()
    st = info.w("PS4")
    if t >= st - 0.2:
        pp = ease_out_back(prog(t, st - 0.2, st + 0.3))
        c.save(); c.translate(W / 2, 880); c.scale(pp, pp)
        rect(c, -460, -260, 920, 520, "#2A0610", 1, r=30); rect(c, -460, -260, 920, 520, RED, 1, r=30, stroke=6)
        draw_text(c, "PS4 / XBOX ONE", 0, -110, "bungee", 70, WH, 1, align="center")
        icon(c, "cross", 0, 40, 170, RED)
        draw_text(c, "GTA VI NO EXISTE AHÍ", 0, 200, "bungee", 56, RED, 1, align="center")
        c.restore()
    confetti(c, t, cues[0] + 1.1, 1); confetti(c, t, cues[2] + 1.1, 2)

def overlay(c, gt, ctx):
    short_captions(c, gt, ctx, y=1470, size=70, hl=YEL, fontname="bungee", maxw=980)
    draw_badge(c, W / 2 - 150, 46, 24)
    draw_text(c, "SAL Y ASFALTO", W / 2 - 112, 56, "ovblk", 28, WH, 0.9, tracking=2)

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("GTA 6 pesa unos doscientos diez gigas. ¿Te cabe? Vamos consola por consola. "
     "PS5 original: de sus ochocientos veinticinco gigas, te quedan libres unos seiscientos sesenta y siete. Cabe, y te sobra. "
     "Series S de quinientos doce: unos trescientos sesenta y cuatro libres. Cabe, pero se come casi el sesenta por ciento. "
     "Series X de un tera: unos ochocientos dos libres. Sin drama. "
     "PS5 Slim de un tera: alrededor de ochocientos cuarenta. Holgado. "
     "El truco: tu espacio real depende de lo que ya tengas instalado. Revísalo hoy, no a las once y cincuenta y nueve. "
     "Y si estás en PS4 o Xbox One... no te cabe ni aunque borres todo: GTA 6 no existe ahí. "
     "¿Cuánto espacio te queda a ti?",
     sc_main, energy=3, speed=1.1, pause_mul=0.65,
     sfx=[(0.0, "coin", 0.5), ("w:PS5 original", "pop", 0.5), ("w:Cabe, y", "coin", 0.6), ("w:Series S", "pop", 0.5), ("w:Cabe, pero", "buzz", 0.4),
          ("w:Series X", "pop", 0.5), ("w:Sin drama", "coin", 0.6), ("w:Slim", "pop", 0.5), ("w:Holgado", "coin", 0.6), ("w:truco", "ding", 0.4), ("w:PS4", "buzz", 0.6)])

VIDEO = dict(id="v07", folder="VIDEO_07", file="GTA6_210GB_te_cabe_SHORT", size=(W, H),
             title="GTA 6 pesa 210 GB: ¿te cabe en tu consola? #shorts", format="Short vertical (9:16)",
             music="chip", music_seed=71, voice="host", beats=B, overlay=overlay, lead_in=0.15, tail=1.0, music_gain=0.4)

THUMB_MARK = (1232, 52, 30)

def thumbnail(c):
    Wt, Ht = 1280, 720
    c.drawRect(skia.Rect.MakeWH(Wt, Ht), lin_grad(0, 0, 0, Ht, [VIO1, VIO2]))
    for i in range(0, Wt, 50):
        for j in range(0, Ht, 50): circle(c, i + 25, j + 25, 2, "#FFFFFF", 0.07)
    draw_text(c, "210 GB", 60, 260, "bungee", 190, YEL, 1, stroke=14, stroke_color="#000000")
    draw_text(c, "¿TE CABE?", 60, 420, "bungee", 120, WH, 1, stroke=12, stroke_color="#000000")
    for i, (nm, cap, col) in enumerate((("PS5", 667, GRN), ("SERIES S", 364, RED))):
        x = 820 + i * 220; y = 110; h = 480
        rect(c, x, y, 180, h, "#0E0828", 1, r=20); rect(c, x, y, 180, h, WH, 1, r=20, stroke=5)
        bh = (h - 16) * 210 / cap; rect(c, x + 8, y + h - 8 - bh, 164, bh, col, 1, r=12)
        draw_text(c, nm, x + 90, y + h + 60, "bungee", 34, WH, 1, align="center")
        draw_text(c, f"{int(round(100 * 210 / cap))}%", x + 90, y + h - bh / 2 + 20, "bungee", 50, "#000000", 1, align="center")
    draw_text(c, "GTA VI · PS5 · XBOX SERIES", 60, 560, "monob", 40, WH, 0.9, tracking=2)
