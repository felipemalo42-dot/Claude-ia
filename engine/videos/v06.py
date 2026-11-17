"""VIDEO 06 — GTA 6 vs GTA 5: 10 cambios confirmados, 1 que no cambió y 3 rumores.
Lenguaje visual: transmisión deportiva 'versus': pantalla dividida en diagonal (GTA V cian / GTA VI verde caimán),
marcador de rondas, cifras gigantes (Anton), visualizaciones distintas por ronda. Música: dembow original.
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL

L1, L2 = "#0D1A3A", "#081026"; R1, R2 = "#0A2C24", "#06170F"; CY = "#3EC8FF"; GR = PAL["caiman"]; WHITE = "#F4F6F8"; PINK = PAL["flamenco"]; SUN = PAL["sol"]

def split_bg(c, W, H, t, slant=120):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [L1, L2]))
    mid = W / 2 + 20 * math.sin(t * 0.5)
    c.drawPath(poly([(mid + slant, 0), (W, 0), (W, H), (mid - slant, H)]), lin_grad(0, 0, 0, H, [R1, R2]))
    for i in range(14):  # rayas de velocidad
        y = (i * 97 + t * 160) % (H + 100) - 50
        rect(c, 0, y, W * 0.18, 2, CY, 0.08); rect(c, W * 0.82, H - y, W * 0.18, 2, GR, 0.08)
    c.drawPath(poly([(mid + slant - 4, 0), (mid + slant + 4, 0), (mid - slant + 4, H), (mid - slant - 4, H)]), paint("#FFFFFF", 0.85))
    return mid

def vs_badge(c, x, y, t, s=1.0):
    p = ease_out_back(clamp(t / 0.4)); c.save(); c.translate(x, y); c.scale(p * s, p * s); c.rotate(-8)
    rect(c, -70, -50, 140, 100, "#000000", 1, r=10); rect(c, -70, -50, 140, 100, SUN, 1, r=10, stroke=4)
    draw_text(c, "VS", 0, 32, "anton", 86, SUN, 1, align="center"); c.restore()

def round_header(c, W, n, title, t):
    p = ease_out(prog(t, 0, 0.35))
    rect(c, W / 2 - 360, 40 - (1 - p) * 80, 720, 96, "#000000", 0.85, r=12)
    draw_text(c, f"RONDA {n:02d}" if isinstance(n, int) else n, W / 2, 78 - (1 - p) * 80, "monob", 26, SUN, 1, align="center", tracking=6)
    draw_text(c, title, W / 2, 124 - (1 - p) * 80, "anton", 44, WHITE, 1, align="center", tracking=3)

def side_label(c, W, H):
    draw_text(c, "GTA V · 2013", 80, H - 60, "anton", 44, CY, 0.9, tracking=2)
    draw_text(c, "GTA VI · 2026", W - 80, H - 60, "anton", 44, GR, 0.9, align="right", tracking=2)

def big_value(c, x, y, txt, sub, col, p, size=200):
    if p <= 0: return
    s = ease_out_back(p); c.save(); c.translate(x, y); c.scale(s, s)
    draw_text(c, txt, 0, 0, "anton", size, col, 1, align="center", glow=(col, 16))
    if sub: draw_text(c, sub, 0, 70, "intersb", 34, WHITE, 0.9, align="center")
    c.restore()

def star(c, x, y, r, col, a=1.0, fill=True):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    draw_poly(c, pts, col, a, stroke=None if fill else 4)

# ---------------------------------------------------------------- escenas
def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H; mid = split_bg(c, W, H, t)
    p = ease_out(prog(t, 0, 1.2)); yrs = int(lerp(2013, 2026, p))
    draw_text(c, "2013", W * 0.25, 560, "anton", 260, CY, ease_out(prog(t, 0.0, 0.4)), align="center", glow=(CY, 16))
    draw_text(c, str(yrs), W * 0.75, 560, "anton", 260, GR, ease_out(prog(t, 0.3, 0.7)), align="center", glow=(GR, 16))
    st = info.w("Trece"); big_value(c, W / 2, 820, "13 AÑOS", None, WHITE, prog(t, st, st + 0.4), 110)
    st = info.w("intacta"); p = ease_out(prog(t, st, st + 0.4))
    if p > 0:
        rect(c, W / 2 - 520, 880, 1040, 120, "#000000", 0.85 * p, r=14)
        draw_text(c, "…Y UNA COSA QUE NO CAMBIÓ", W / 2, 960, "anton", 64, SUN, p, align="center", tracking=2)
    vs_badge(c, W / 2, 300, t - 0.5)

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_intro(c, t, info, ctx):
    W, H = ctx.W, ctx.H; split_bg(c, W, H, t); vs_badge(c, W / 2, H / 2, t - 0.2, 1.4)
    items = [("10", "CAMBIOS CONFIRMADOS", GR, "diez"), ("1", "QUE NO CAMBIÓ", SUN, "uno que"), ("3", "RUMORES SEÑALADOS", PINK, "tres rumores")]
    for i, (n, lab, col, cue) in enumerate(items):
        st = info.w(cue); p = ease_out_back(prog(t, st, st + 0.4)); y = 250 + i * 250
        if p <= 0: continue
        c.save(); c.translate(W / 2 + 480, y); c.scale(p, p)
        draw_text(c, n, -260, 50, "anton", 180, col, 1, align="center"); draw_text(c, lab, -160, 30, "anton", 52, WHITE, 1)
        c.restore()
    p1 = ease_out(prog(t, info.w("izquierda"), info.w("izquierda") + 0.4)); p2 = ease_out(prog(t, info.w("derecha"), info.w("derecha") + 0.4))
    draw_text(c, "← GTA V", 120, 560, "anton", 100, CY, p1); draw_text(c, "GTA VI →", 120, 700, "anton", 100, GR, p2)

def make_round(n, title, viz, src=None, cert="OFICIAL"):
    def sc(c, t, info, ctx):
        W, H = ctx.W, ctx.H; split_bg(c, W, H, t); round_header(c, W, n, title, t); side_label(c, W, H)
        viz(c, t, info, ctx)
        if src: source_chip(c, W / 2 - 300, H - 150, src, ease_out(prog(t, 0.6, 1.0)))
        cert_tag(c, W - 70, 170, cert, 1, 24, align="right", t=prog(t, 0.5, 0.9))
        # marcador de cambios
        for i in range(10):
            on = (i < n) if isinstance(n, int) else True
            rect(c, W / 2 - 250 + i * 50, H - 70, 40, 12, GR if on else "#33405A", 1, r=6)
    return sc

def viz_map(c, t, info, ctx):
    W, H = ctx.W, ctx.H; p1 = prog(t, info.w("California") - 0.3, info.w("California") + 0.3); p2 = prog(t, info.w("Leonida") - 0.2, info.w("Leonida") + 0.4)
    big_value(c, W * 0.25, 470, "LOS SANTOS", "sur de California", CY, p1, 110)
    big_value(c, W * 0.75, 470, "LEONIDA", "parodia de Florida", GR, p2, 120)
    st = info.w("doble"); p3 = ease_out_back(prog(t, st, st + 0.4))
    if p3 > 0:
        s = 140; rect(c, W * 0.25 - s / 2, 620, s, s, CY, 0.25 * p3); rect(c, W * 0.25 - s / 2, 620, s, s, CY, p3, stroke=3)
        s2 = s * math.sqrt(2) * p3; rect(c, W * 0.75 - s2 / 2, 620, s2, s2, GR, 0.25); rect(c, W * 0.75 - s2 / 2, 620, s2, s2, GR, 1, stroke=3)
        draw_text(c, "×2", W * 0.75, 620 + s2 / 2 + 30, "anton", 80, WHITE, p3, align="center")

def viz_heroes(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    for i in range(3):
        p = ease_out_back(prog(t, info.w("tres") + i * 0.25, info.w("tres") + i * 0.25 + 0.4))
        if p > 0: c.save(); c.translate(W * 0.25 + (i - 1) * 170, 520); c.scale(p, p); icon(c, "user", 0, 0, 170, CY); c.restore()
    big_value(c, W * 0.25, 760, "3", "Michael · Franklin · Trevor", CY, prog(t, info.w("Michael"), info.w("Michael") + 0.4), 120)
    for i in range(2):
        p = ease_out_back(prog(t, info.w("dos,") + i * 0.25, info.w("dos,") + i * 0.25 + 0.4))
        col = PINK if i == 0 else CY
        if p > 0: c.save(); c.translate(W * 0.75 + (i - 0.5) * 200, 520); c.scale(p, p); icon(c, "user", 0, 0, 190, GR); c.restore()
    big_value(c, W * 0.75, 760, "2", "Jason · Lucía", GR, prog(t, info.w("Jason"), info.w("Jason") + 0.4), 120)
    st = info.w("sin pantalla"); p = ease_out(prog(t, st, st + 0.4))
    if p > 0:
        rect(c, W * 0.75 - 330, 850, 660, 70, "#000000", 0.8 * p, r=35); draw_text(c, "CAMBIO SIN PANTALLA DE CARGA", W * 0.75, 897, "anton", 40, SUN, p, align="center")

def viz_stars(c, t, info, ctx):
    W, H = ctx.W, ctx.H; st5 = info.w("cinco"); st6 = info.w("seis")
    for i in range(5):
        p = ease_out_back(prog(t, st5 + i * 0.12, st5 + i * 0.12 + 0.3))
        if p > 0: star(c, W * 0.25 - 280 + i * 140, 520, 60 * p, CY)
    big_value(c, W * 0.25, 760, "5", "estrellas", CY, prog(t, st5, st5 + 0.4), 150)
    for i in range(6):
        p = ease_out_back(prog(t, st6 + i * 0.12, st6 + i * 0.12 + 0.3))
        if p > 0: star(c, W * 0.75 - 330 + i * 132, 520, 60 * p * (1.25 if i == 5 else 1), GR if i < 5 else SUN)
    big_value(c, W * 0.75, 760, "6", "estrellas", GR, prog(t, st6, st6 + 0.4), 150)

def viz_profile(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    big_value(c, W * 0.25, 560, "—", "no existía", CY, prog(t, 0.3, 0.7), 200)
    st = info.w("Perfil"); p = ease_out(prog(t, st, st + 0.5))
    if p > 0:
        x0, y0 = W * 0.75 - 330, 330
        rect(c, x0, y0, 660, 470, "#000000", 0.6 * p, r=16); rect(c, x0, y0, 660, 470, GR, p, r=16, stroke=3)
        draw_text(c, "PERFIL CRIMINAL", x0 + 330, y0 + 70, "anton", 54, GR, p, align="center")
        for i, lab in enumerate(("CONDUCCIÓN", "VIOLENCIA", "SIGILO", "REPUTACIÓN")):
            v = 0.3 + 0.6 * abs(math.sin(t * 0.7 + i * 1.7)); y = y0 + 140 + i * 78
            draw_text(c, lab, x0 + 40, y + 28, "monob", 26, WHITE, p); rect(c, x0 + 290, y + 6, 330, 28, "#1A2A26", p, r=14); rect(c, x0 + 290, y + 6, 330 * v * p, 28, GR, p, r=14)
        draw_text(c, "Barras ilustrativas: no es la interfaz del juego", x0 + 330, y0 + 455, "mono", 18, WHITE, 0.6 * p, align="center")
    st = info.w("Rob Nelson"); p = ease_out(prog(t, st, st + 0.4))
    if p > 0: draw_par(c, "“Las acciones constantes pueden influir en cómo reacciona el mundo” — Rob Nelson", W * 0.75 - 330, 870, "dmserifi", 32, 680, color=WHITE, a=p)

def viz_focus(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    big_value(c, W * 0.25, 560, "—", "sin sistema de foco", CY, prog(t, 0.3, 0.7), 200)
    cx, cy = W * 0.75, 540; p = ease_out(prog(t, info.w("fijar") - 0.3, info.w("fijar") + 0.3))
    if p > 0:
        r = 170 - 40 * p
        for k in range(4):
            ang = k * math.pi / 2 + t * 0.8
            line(c, cx + math.cos(ang) * r, cy + math.sin(ang) * r, cx + math.cos(ang) * (r + 50), cy + math.sin(ang) * (r + 50), GR, p, 8)
        circle(c, cx, cy, r, GR, 0.8 * p, stroke=4); icon(c, "user", cx, cy, 160, WHITE, p)
    st = info.w("ralentiza"); p2 = ease_out(prog(t, st, st + 0.4))
    if p2 > 0:
        for k in range(3): circle(c, cx + [-40, 30, 0][k], cy + [-50, 0, 60][k], 14, PINK, p2); circle(c, cx + [-40, 30, 0][k], cy + [-50, 0, 60][k], 24 + 6 * pulse(t, 0.8), PINK, 0.5 * p2, stroke=3)
        draw_text(c, "CÁMARA LENTA + PUNTOS DÉBILES", cx, 820, "anton", 46, SUN, p2, align="center")
    draw_text(c, "INSPIRADO EN RED DEAD REDEMPTION 2", cx, 300, "monob", 26, WHITE, 0.8 * p, align="center", tracking=2)

def viz_weather(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    p1 = ease_out(prog(t, info.w("lluvia") - 0.3, info.w("lluvia") + 0.3))
    if p1 > 0:
        icon(c, "storm", W * 0.25, 500, 220, CY, p1)
        for k in range(30):
            x = W * 0.25 - 200 + (k * 53) % 400; y = 600 + ((t * 600 + k * 77) % 250); line(c, x, y, x - 8, y + 30, CY, 0.5 * p1, 3)
        draw_text(c, "LLUVIA Y TORMENTAS", W * 0.25, 900, "anton", 50, WHITE, p1, align="center")
    st = info.w("huracanes"); p2 = ease_out(prog(t, st - 0.3, st + 0.3))
    if p2 > 0:
        cx, cy = W * 0.75, 540
        for k in range(5):
            r = 60 + k * 45; a0 = t * (2.5 - k * 0.3)
            arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), math.degrees(a0), 250)
            c.drawPath(arc, paint(GR, p2 * (1 - k * 0.15), stroke=10 - k))
        circle(c, cx, cy, 30, WHITE, p2)
        draw_text(c, "TORMENTAS TROPICALES", cx, 860, "anton", 50, WHITE, p2, align="center"); draw_text(c, "Y HURACANES", cx, 920, "anton", 50, GR, p2, align="center")

def viz_fauna(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    big_value(c, W * 0.25, 560, "SÍ", "había animales", CY, prog(t, 0.4, 0.8), 160)
    st = info.w("ciento setenta"); p = prog(t, st - 0.2, st + 1.6)
    n = int(170 * ease_out(p))
    for i in range(n):
        col, row = i % 17, i // 17; x = W * 0.75 - 340 + col * 42; y = 300 + row * 42
        colr = SUN if i in (7, 63, 121) else (PINK if i % 23 == 0 else GR)
        circle(c, x, y, 14, colr, 0.95)
    if p > 0: draw_text(c, f"{n}+", W * 0.75, 790, "anton", 120, WHITE, 1, align="center")
    st = info.w("raras"); pp = ease_out(prog(t, st, st + 0.4))
    if pp > 0:
        for i, (lab, col) in enumerate((("RARAS", GR), ("DESCUBRIBLES", PINK), ("LEGENDARIAS", SUN))):
            draw_text(c, "● " + lab, W * 0.75 - 330 + i * 230, 880, "monob", 26, col, pp)

def viz_price(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    big_value(c, W * 0.25, 600, "US$59,99", "2013", CY, prog(t, info.w("59,99") - 0.3, info.w("59,99") + 0.2), 150)
    big_value(c, W * 0.75, 600, "US$79,99", "edición estándar", GR, prog(t, info.w("79,99") - 0.3, info.w("79,99") + 0.2), 150)
    st = info.w("79,99") + 1.0; p = ease_out_back(prog(t, st, st + 0.4))
    if p > 0:
        c.save(); c.translate(W / 2, 820); c.scale(p, p); rect(c, -200, -50, 400, 100, SUN, 1, r=50); draw_text(c, "+20 USD", 0, 30, "anton", 70, "#000000", 1, align="center"); c.restore()

def viz_online(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    big_value(c, W * 0.25, 560, "2 SEMANAS", "después del juego", CY, prog(t, info.w("dos semanas") - 0.3, info.w("dos semanas") + 0.2), 120)
    big_value(c, W * 0.75, 560, "SIN FECHA", "“experiencia para un jugador”", GR, prog(t, info.w("un jugador") - 0.3, info.w("un jugador") + 0.2), 120)

def viz_platforms(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    rowsL = [("PS3 · X360", "2013"), ("PC", "+19 MESES"), ("PS4 · XB1 · PS5 · SERIES", "después")]
    for i, (a, b) in enumerate(rowsL):
        st = info.w("PS3") + i * 0.9; p = ease_out(prog(t, st, st + 0.4)); y = 380 + i * 150
        if p <= 0: continue
        rect(c, W * 0.25 - 330, y, 660, 110, "#000000", 0.5 * p, r=12); draw_text(c, a, W * 0.25 - 300, y + 70, "anton", 46, CY, p); draw_text(c, b, W * 0.25 + 300, y + 70, "monob", 26, WHITE, p, align="right")
    rowsR = [("PS5 · XBOX SERIES", "19 NOV 2026", GR), ("PC", "SIN FECHA", PINK)]
    for i, (a, b, col) in enumerate(rowsR):
        st = info.w("PS5") + i * 1.2; p = ease_out(prog(t, st, st + 0.4)); y = 380 + i * 150
        if p <= 0: continue
        rect(c, W * 0.75 - 330, y, 660, 110, "#000000", 0.5 * p, r=12); draw_text(c, a, W * 0.75 - 300, y + 70, "anton", 46, col, p); draw_text(c, b, W * 0.75 + 300, y + 70, "monob", 26, WHITE, p, align="right")

def viz_same(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    for x, col in ((W * 0.25, CY), (W * 0.75, GR)):
        p = ease_out(prog(t, 0.3, 0.8))
        rect(c, x - 300, 330, 600, 420, "#000000", 0.55 * p, r=18)
        draw_text(c, "VOCES", x, 420, "monob", 30, WHITE, p, align="center", tracking=4); draw_text(c, "INGLÉS", x, 520, "anton", 110, col, p, align="center")
        draw_text(c, "TEXTOS", x, 610, "monob", 30, WHITE, p, align="center", tracking=4); draw_text(c, "ESPAÑOL", x, 700, "anton", 90, col, p, align="center")
    st = info.w("Algunos"); p = ease_out_back(prog(t, st, st + 0.4))
    if p > 0: c.save(); c.translate(W / 2, 860); c.scale(p, p); rect(c, -330, -50, 660, 100, SUN, 1, r=50); draw_text(c, "= IGUAL QUE EN 2013", 0, 30, "anton", 60, "#000000", 1, align="center"); c.restore()

def sc_rumors(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, ["#2A0C1E", "#12060E"])); grid(c, W, H, 70, PINK, 0.06)
    round_header(c, W, "ZONA DE RUMORES", "3 COSAS QUE NADIE HA CONFIRMADO", t)
    items = [("MODO A 60 FPS", "Objetivo oficial: 30 fps. 60 no está confirmado.", "sesenta cuadros"),
             ("ONLINE EN POCAS SEMANAS", "Lo dice un filtrador, no Rockstar.", "filtrador"),
             ("PC EN 2027", "Expectativa de analistas. Nadie lo ha anunciado.", "PC en"),]
    for i, (a, b, cue) in enumerate(items):
        st = info.w(cue); p = ease_out(prog(t, st - 0.3, st + 0.2)); y = 250 + i * 230
        if p <= 0: continue
        c.save(); c.translate((1 - p) * 200, 0)
        rect(c, 200, y, 1520, 190, "#000000", 0.6, r=16); rect(c, 200, y, 1520, 190, PINK, 1, r=16, stroke=3)
        draw_text(c, a, 260, y + 85, "anton", 64, WHITE, 1); draw_text(c, b, 260, y + 145, "intersb", 34, "#F6C7DA", 1)
        cert_tag(c, 1680, y + 30, "RUMOR", 1, 26, align="right", t=1)
        c.restore()

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "¿CUÁL ES EL CAMBIO MÁS IMPORTANTE?", "Comparación jugando, con pruebas reales, después del jueves", GR)

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2.5 < gt < ctx.total - 20: watermark(c, W, H, 0.45, corner="tr")
    if gt < 8: ai_notice(c, W, H, clamp(8 - gt), "Infografías originales de Sal y Asfalto · sin imágenes de GTA V ni de GTA VI")

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Trece años separan a GTA 5 de GTA 6. Y en ese tiempo, Rockstar cambió más cosas de las que parece... y dejó intacta una que muchos esperaban.",
     sc_hook, section="GANCHO", energy=2, sfx=[(0.0, "riser", 0.4), ("w:Trece", "hit", 0.6), ("w:intacta", "hit", 0.5)])
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=2, trans=("flash", 0.3))
beat("Estás en Sal y Asfalto. Hoy: diez cambios confirmados entre GTA 5 y GTA 6, uno que no cambió, y tres rumores que te vamos a señalar con el dedo. "
     "A la izquierda, GTA 5, y a la derecha, GTA 6.",
     sc_intro, section="INTRODUCCIÓN", energy=3, trans=("zoom", 0.5), sfx=[("w:diez", "hit", 0.5), ("w:uno que", "hit", 0.5), ("w:tres rumores", "hit", 0.5)])
R = []
def rnd(n, title, viz, vo, src=None, cert="OFICIAL", sfx=()):
    beat(vo, make_round(n, title, viz, src, cert), section=f"RONDA {n} · {title}", energy=3, trans=("whip" if n % 2 else "whip_left", 0.4), sfx=[(0.0, "whoosh", 0.5), *sfx])
rnd(1, "EL MUNDO", viz_map, "Uno: el mundo. GTA 5 recreaba el sur de California con Los Santos. GTA 6 se muda a Leonida, la parodia de Florida. Y según Aaron Garbut, de Rockstar, el mapa es el doble de grande.",
    "Aaron Garbut en Game Informer", sfx=[("w:doble", "hit", 0.5)])
rnd(2, "PROTAGONISTAS", viz_heroes, "Dos: los protagonistas. GTA 5 tenía tres: Michael, Franklin y Trevor. GTA 6 tiene dos, Jason y Lucía, y en el Extended Look se vio que puedes cambiar entre ellos en plena acción, sin pantalla de carga.",
    "Extended Look (Rockstar), vía TechRadar", sfx=[("w:tres", "pop", 0.4), ("w:dos,", "pop", 0.4), ("w:sin pantalla", "hit", 0.4)])
rnd(3, "ESTRELLAS DE BÚSQUEDA", viz_stars, "Tres: las estrellas de búsqueda. GTA 5 llegaba a cinco. GTA 6 llega a seis.",
    "Extended Look (Rockstar)", sfx=[("w:cinco", "coin", 0.4), ("w:seis", "hit", 0.6)])
rnd(4, "PERFIL CRIMINAL", viz_profile, "Cuatro: algo que GTA 5 no tenía. El Perfil Criminal, un sistema que registra cómo te comportas. Rob Nelson, de Rockstar, dijo que las acciones constantes pueden influir en cómo reacciona el mundo.",
    "Rob Nelson (Rockstar), vía prensa", sfx=[("w:Perfil", "ding", 0.4)])
rnd(5, "SISTEMA DE FOCO", viz_focus, "Cinco: el sistema de foco. Como en Red Dead Redemption 2, puedes fijar la atención en personas y animales para interactuar con ellos. Y al apuntar, el tiempo se ralentiza y se marcan los puntos débiles del enemigo.",
    "Extended Look (Rockstar), vía Red Bull / TechRadar", sfx=[("w:fijar", "tick", 0.5), ("w:ralentiza", "whoosh", 0.4)])
rnd(6, "CLIMA", viz_weather, "Seis: el clima. GTA 5 tenía lluvia y tormentas. GTA 6 suma tormentas tropicales y huracanes, con un sistema rehecho a partir del de Red Dead Redemption 2, según Game Informer.",
    "Game Informer, n.º 382", sfx=[("w:huracanes", "riser", 0.4)])
rnd(7, "FAUNA", viz_fauna, "Siete: la fauna. GTA 5 tenía animales, sí. Pero GTA 6, según Game Informer, tiene más de ciento setenta especies. Y algunas se pueden rastrear por rareza: raras, descubribles y legendarias.",
    "Game Informer, vía Insider Gaming", sfx=[("w:ciento setenta", "riser", 0.3), ("w:raras", "pop", 0.4)])
rnd(8, "PRECIO", viz_price, "Ocho: el precio. GTA 5 salió en 2013 a {59,99|cincuenta y nueve con noventa y nueve} dólares. GTA 6 cuesta {79,99|setenta y nueve con noventa y nueve} en su edición estándar.",
    "Hollywood Reporter", sfx=[("w:59,99", "coin", 0.4), ("w:79,99", "coin", 0.5)])
rnd(9, "ONLINE", viz_online, "Nueve: el online. GTA Online llegó apenas dos semanas después de GTA 5. Para GTA 6, Rockstar habla de una experiencia para un jugador, sin fecha para un online.",
    "FAQ de PlayStation · Take-Two", sfx=[("w:un jugador", "hit", 0.4)])
rnd(10, "PLATAFORMAS", viz_platforms, "Diez: las plataformas. GTA 5 salió en PS3 y Xbox 360, y a PC llegó diecinueve meses después. GTA 6 sale solo en PS5 y Xbox Series, y la versión de PC no tiene fecha.",
    "Take-Two · historial de lanzamientos de GTA V", sfx=[("w:PS3", "pop", 0.4), ("w:PS5", "pop", 0.4)])
beat("¿Y lo que no cambió? El idioma. GTA 5 no tenía doblaje al español y GTA 6 tampoco: voces en inglés y textos en español. Algunos lo celebran por las actuaciones originales; otros, no tanto.",
     make_round("LO QUE NO CAMBIA", "EL IDIOMA", viz_same, "Vandal · Microsoft Store"), section="LO QUE NO CAMBIA", energy=2, trans=("flash", 0.3), sfx=[("w:Algunos", "stamp", 0.5)])
beat("Y ahora, tres rumores, con etiqueta roja. Uno: un modo a sesenta cuadros por segundo. Rockstar dijo que el objetivo es treinta, y no ha confirmado sesenta. "
     "Dos: un online para Leonida en pocas semanas. Lo dice un filtrador, no Rockstar. "
     "Tres: la versión de PC en 2027. Es lo que esperan muchos analistas mirando lo que pasó con GTA 5, pero nadie lo ha anunciado.",
     sc_rumors, section="RUMORES", energy=2, trans=("glitch", 0.4), sfx=[("w:sesenta cuadros", "buzz", 0.4), ("w:filtrador", "buzz", 0.4), ("w:PC en", "buzz", 0.4)])
beat("Diez cambios, una tradición y tres incógnitas. ¿Cuál de estos cambios te parece el más importante? Te leo en los comentarios. "
     "Y si quieres la comparación jugando, con pruebas reales, suscríbete: llega después del jueves.",
     sc_end, section="LLAMADA A LA ACCIÓN", energy=2, hold=4.0, min=20, trans=("fade", 0.6))

VIDEO = dict(id="v06", folder="VIDEO_06", file="GTA6_vs_GTA5_10_cambios_confirmados",
             title="GTA 6 vs GTA 5: 10 cambios confirmados, 1 que no cambió y 3 rumores",
             format="Largo (16:9)", music="dembow", music_seed=61, voice="host", speed=1.04, beats=B, overlay=overlay, music_gain=0.48)

THUMB_MARK = (1236, 676, 30)

def thumbnail(c):
    W, H = 1280, 720
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [L1, L2]))
    c.drawPath(poly([(700, 0), (W, 0), (W, H), (580, H)]), lin_grad(0, 0, 0, H, [R1, R2]))
    c.drawPath(poly([(694, 0), (706, 0), (586, H), (574, H)]), paint("#FFFFFF"))
    draw_text(c, "V", 300, 470, "ovblk", 400, CY, 1, align="center")
    draw_text(c, "VI", 960, 470, "ovblk", 400, GR, 1, align="center")
    for i in range(5): star(c, 130 + i * 85, 600, 34, CY)
    for i in range(6): star(c, 760 + i * 80, 600, 34, GR if i < 5 else SUN)
    c.save(); c.translate(640, 330); c.rotate(-8); rect(c, -95, -65, 190, 130, "#000000", 1, r=12); rect(c, -95, -65, 190, 130, SUN, 1, r=12, stroke=5)
    draw_text(c, "VS", 0, 42, "anton", 110, SUN, 1, align="center"); c.restore()
    sign_text(c, W / 2, 14, "10 CAMBIOS CONFIRMADOS", 60, align="center")
