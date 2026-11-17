"""VIDEO 09 — 7 misterios de GTA 6 que se resuelven el jueves (sobres sellados + predicciones).
Lenguaje visual: mesa de terciopelo índigo a la luz de una vela, sobres lacrados con el sello del caimán,
medidores semicirculares de confianza, tipografía Syne + Inter. Música 'mystery' original (caja de música FM + drones).
Es el puente hacia el VIDEO 10 (post-lanzamiento), donde se abren los sobres jugando.
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL, draw_caiman, draw_badge

V1, V2 = "#1B1040", "#0A0618"; ENV = "#EADFC8"; ENV_D = "#CDBE9F"; WAX = "#9E1B32"; GOLD = "#E9C46A"; LAV = "#B8A6F0"; WHITE = "#F3EEFF"; SUN = PAL["sol"]

def velvet(c, W, H, t):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [V1, V2]))
    fl = 0.85 + 0.15 * math.sin(t * 9) * math.sin(t * 4.3)
    c.drawCircle(W * 0.82, H * 0.2, 900, rad_grad(W * 0.82, H * 0.2, 900, [hexc("#FFB65C", 0.20 * fl), hexc("#FFB65C", 0)]))
    bokeh(c, W, H, t, 18, (GOLD, LAV), seed=12, size=(6, 30), a=0.12, speed=8)

def candle(c, x, y, t, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -26, 0, 52, 170, "#EDE3CF", 1, r=6); rect(c, -26, 0, 52, 14, "#FFFFFF", 0.4, r=6)
    fl = math.sin(t * 13) * 3 + math.sin(t * 7.1) * 2
    flame = skia.Path(); flame.moveTo(0, -70 + fl); flame.cubicTo(22, -40, 16, -6, 0, -4); flame.cubicTo(-16, -6, -22, -40, 0, -70 + fl)
    c.drawCircle(0, -30, 90, rad_grad(0, -30, 90, [hexc("#FFC46B", 0.45), hexc("#FFC46B", 0)]))
    c.drawPath(flame, paint("#FFD27A", 1)); c.drawPath(flame, paint("#FFF6D6", 0.9, blur=3))
    line(c, 0, -4, 0, 4, "#2B2117", 1, 3)
    c.restore()

def envelope(c, x, y, s, num, q, t, open_p=0.0, seal=True, a=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(c, -260, -150, 520, 320, "#000000", 0.4 * a, blur=16)
    rect(c, -260, -170, 520, 320, ENV, a, r=8)
    draw_poly(c, [(-260, -170), (0, 10 - 180 * open_p), (260, -170)], ENV_D, a)
    c.drawPath(poly([(-260, -170), (0, 10 - 180 * open_p), (260, -170)]), paint("#8C7B5A", 0.6 * a, stroke=2))
    draw_poly(c, [(-260, 150), (-30, -20), (30, -20), (260, 150)], "#E2D5B9", a)
    if seal and open_p < 0.2:
        circle(c, 0, 10, 56, WAX, a); circle(c, 0, 10, 46, "#7E1427", a, stroke=4)
        arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(-18, -10, 36, 36), 180, 180); c.drawPath(arc, paint("#F2C2C8", a, stroke=4))
        line(c, -30, 8, 30, 8, "#F2C2C8", a, 3); c.drawPath(poly([(-2, 8), (2, 8), (16, 40), (-16, 40)]), paint("#F2C2C8", a, stroke=3))
    draw_text(c, f"N.º {num}", -230, 120, "syne", 30, "#6E5C3C", a)
    c.restore()

def gauge(c, x, y, r, val, t, st, col=SUN, label="CONFIANZA"):
    p = ease_out(prog(t, st, st + 1.2)); v = val * p
    arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), 180, 180); c.drawPath(arc, paint("#2A2150", 1, stroke=26, cap="butt"))
    arc2 = skia.Path(); arc2.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), 180, 180 * v); c.drawPath(arc2, paint(col, 1, stroke=26, cap="butt"))
    ang = math.pi + math.pi * v; line(c, x, y, x + math.cos(ang) * (r - 30), y + math.sin(ang) * (r - 30), WHITE, 1, 6); circle(c, x, y, 12, WHITE)
    draw_text(c, f"{int(round(v * 100))}%", x, y + 70, "syne", 64, WHITE, clamp(p * 2), align="center")
    draw_text(c, label, x, y + 110, "monob", 22, LAV, clamp(p * 2), align="center", tracking=4)

MYST = [
    dict(q="¿CUÁNDO LLEGA EL ONLINE?", known="Rockstar: “experiencia para un jugador”. Sin fecha para un online. GTA Online (GTA V) sigue activo.",
         pred="No antes de 2027", conf=0.55, cue="online"),
    dict(q="¿HABRÁ MODO A 60 FPS?", known="Objetivo oficial: 30 fps, también en PS5 Pro. El estudio no se ha comprometido con 60.",
         pred="No el día del lanzamiento", conf=0.75, cue="sesenta"),
    dict(q="¿CUÁNTOS INTERIORES?", known="No hay cifra oficial de edificios visitables.", pred="Más que en GTA 5", conf=0.6, cue="edificios"),
    dict(q="¿CUÁNTO PESA EL PERFIL CRIMINAL?", known="Rob Nelson: las acciones constantes pueden influir en el mundo y la narrativa.",
         pred="Más en el mundo que en la trama", conf=0.5, cue="Perfil Criminal"),
    dict(q="¿HURACANES DINÁMICOS?", known="Game Informer: tormentas tropicales y huracanes pueden azotar Leonida.", pred="Ambos: clima y misiones", conf=0.5, cue="huracanes"),
    dict(q="¿QUÉ ANIMAL SERÁ LEGENDARIO?", known="Hay animales raros, descubribles y legendarios. No se ha dicho cuáles.", pred="Uno emblemático de Florida", conf=0.4, cue="legendario"),
    dict(q="¿HAY MÁS DE SEIS REGIONES?", known="Seis regiones con nombre. Mapa “el doble” que el de GTA 5.", pred="Más zonas, no otra gran región", conf=0.5, cue="regiones"),
]

def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H; velvet(c, W, H, t); candle(c, 1640, 760, t, 1.1)
    for i in range(7):
        st = 0.4 + i * 0.35; p = ease_out(prog(t, st, st + 0.5))
        if p <= 0: continue
        x = 300 + (i % 4) * 340 + (170 if i >= 4 else 0); y = 380 + (i // 4) * 330 - (1 - p) * 400
        envelope(c, x, y, 0.55, i + 1, "", t, rot=[-6, 4, -3, 5, -4, 3, -5][i], a=p)
    st = info.w("El jueves"); p = ease_out_back(prog(t, st, st + 0.5))
    if p > 0:
        c.save(); c.translate(W / 2, 960); c.scale(p, p)
        rect(c, -460, -60, 920, 120, "#000000", 0.6, r=60); draw_text(c, "SE ABREN EL JUEVES", 0, 22, "syne", 64, GOLD, 1, align="center", tracking=4)
        c.restore()
    draw_text(c, "7", 160, 220, "syne", 180, GOLD, ease_out(prog(t, info.w("siete"), info.w("siete") + 0.4)))
    draw_text(c, "PREGUNTAS SIN RESPUESTA", 290, 180, "syne", 50, WHITE, ease_out(prog(t, info.w("siete"), info.w("siete") + 0.4)))

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_rules(c, t, info, ctx):
    W, H = ctx.W, ctx.H; velvet(c, W, H, t); candle(c, 1700, 780, t)
    envelope(c, 600, 520, 1.0, 0, "", t, open_p=0.0)
    items = [("PREGUNTA", "w:pregunta", WHITE), ("LO QUE SÍ SABEMOS", "w:sabemos", PAL["caiman"]), ("NUESTRA PREDICCIÓN", "w:predicción", SUN)]
    for i, (lab, cue, col) in enumerate(items):
        st = info.w(cue[2:]); p = ease_out(prog(t, st, st + 0.4)); y = 330 + i * 150
        if p <= 0: continue
        rect(c, 1040, y - 60, 600, 100, "#000000", 0.45 * p, r=14); rect(c, 1040, y - 60, 8, 100, col, p)
        draw_text(c, lab, 1080, y + 8, "syne", 44, col, p)
    gauge(c, 1340, 880, 120, 0.6, t, info.w("medidor"), SUN)
    st = info.w("no son información"); p = ease_out(prog(t, st, st + 0.4))
    if p > 0:
        rect(c, 300, 950, 760, 90, SUN, 0.15 * p, r=12); draw_text(c, "Predicción ≠ información", 680, 1010, "syne", 44, SUN, p, align="center")
        cert_tag(c, 300, 860, "DEDUCCIÓN", p, 24, t=p)

def make_myst(i):
    m = MYST[i]
    def sc(c, t, info, ctx):
        W, H = ctx.W, ctx.H; velvet(c, W, H, t); candle(c, 1780, 860, t, 0.8)
        op = ease_io(prog(t, 0.3, 1.2))
        envelope(c, 400, 560 + 40 * op, 0.9, i + 1, m["q"], t, open_p=op, seal=True)
        if op > 0.25: c.save(); c.translate(400, 560); circle(c, -90 * op, 120 + 200 * op, 18, WAX, 1 - op); circle(c, 80 * op, 140 + 190 * op, 14, WAX, 1 - op); c.restore()
        # carta que sale del sobre
        pl = ease_out(prog(t, 0.8, 1.5))
        if pl > 0:
            c.save(); c.translate(400, 480 - 220 * pl); c.rotate(-3 * pl)
            rect(c, -230, -150, 460, 300, "#FBF6EA", 1, r=4); draw_text(c, f"MISTERIO {i + 1}/7", 0, -90, "monob", 24, "#7A6A4A", 1, align="center", tracking=3)
            draw_par(c, m["q"], -200, -30, "syne", 40, 400, color="#2B1F45", lh=1.1)
            c.restore()
        draw_text(c, f"{i + 1}", 120, 220, "syne", 160, GOLD, 0.9)
        # lo que sabemos
        sk = info.w("Lo que sabemos", default=info.b(0) + 4.0); p = ease_out(prog(t, sk, sk + 0.5))
        if p > 0:
            rect(c, 820, 170, 960, 330, "#000000", 0.45 * p, r=16); rect(c, 820, 170, 8, 330, PAL["caiman"], p)
            draw_text(c, "LO QUE SÍ SABEMOS", 860, 230, "monob", 26, PAL["caiman"], p, tracking=3)
            cert_tag(c, 1750, 200, "OFICIAL" if i != 2 else "SIN CONFIRMAR", p, 20, align="right", t=p)
            draw_par(c, m["known"], 860, 300, "intersb", 34, 880, color=WHITE, a=p, lh=1.3)
        sp = info.w("Nuestra predicción", default=info.b(0) + 9.0); p2 = ease_out(prog(t, sp, sp + 0.5))
        if p2 > 0:
            rect(c, 820, 540, 960, 380, "#000000", 0.45 * p2, r=16); rect(c, 820, 540, 8, 380, SUN, p2)
            draw_text(c, "NUESTRA PREDICCIÓN", 860, 600, "monob", 26, SUN, p2, tracking=3); cert_tag(c, 1750, 570, "DEDUCCIÓN", p2, 20, align="right", t=p2)
            draw_par(c, m["pred"], 860, 690, "syne", 54, 520, color=WHITE, a=p2, lh=1.05)
            gauge(c, 1560, 790, 110, m["conf"], t, sp + 0.4, SUN)
        for k in range(7): circle(c, W / 2 - 150 + k * 50, 1030, 10, GOLD if k <= i else "#3A2F66", 1)
    return sc

def sc_close(c, t, info, ctx):
    W, H = ctx.W, ctx.H; velvet(c, W, H, t); candle(c, W / 2, 820, t, 1.2)
    for i in range(7):
        ang = math.pi + (i / 6) * math.pi; r = 620
        envelope(c, W / 2 + math.cos(ang) * r, 760 + math.sin(ang) * r * 0.75, 0.42, i + 1, "", t, rot=math.degrees(ang) + 90 - 180, a=ease_out(prog(t, i * 0.15, i * 0.15 + 0.5)))
    p = ease_out(prog(t, info.w("Siete sobres"), info.w("Siete sobres") + 0.5))
    draw_text(c, "7 SOBRES · 7 APUESTAS", W / 2, 170, "syne", 76, GOLD, p, align="center", tracking=3)
    st = info.w("comentarios"); p = ease_out(prog(t, st, st + 0.5))
    if p > 0:
        rect(c, W / 2 - 520, 930, 1040, 110, "#000000", 0.6 * p, r=55); draw_text(c, "DEJA TU PREDICCIÓN EN LOS COMENTARIOS", W / 2, 1000, "syne", 42, WHITE, p, align="center")

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "EL JUEVES ABRIMOS LOS SOBRES", "Suscríbete para ver cuántas acertamos", GOLD)

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2.5 < gt < ctx.total - 20: watermark(c, W, H, 0.45)
    if gt < 8: ai_notice(c, W, H, clamp(8 - gt), "Animación original de Sal y Asfalto · las predicciones son opinión del canal")

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Faltan horas para el lanzamiento, y todavía hay siete preguntas que Rockstar no ha respondido. Las metimos en sobres sellados. El jueves los abrimos.",
     sc_hook, section="GANCHO", energy=1, sfx=[(0.4, "paper", 0.4), (1.2, "paper", 0.4), (2.0, "paper", 0.4), ("w:El jueves", "seal", 0.6)])
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=1, trans=("flash", 0.3))
beat("Esto es Sal y Asfalto. Cada sobre lleva una pregunta, lo que sí sabemos con certeza y nuestra predicción, con un medidor de confianza. "
     "Ojo: las predicciones son nuestras, van en amarillo y no son información.",
     sc_rules, section="REGLAS", energy=1, trans=("zoom", 0.5), sfx=[("w:pregunta", "pop", 0.4), ("w:sabemos", "pop", 0.4), ("w:predicción", "pop", 0.4), ("w:no son información", "ding", 0.3)])
VO = [
    ("Sobre uno: ¿cuándo llega el online? Lo que sabemos: Rockstar describe GTA 6 como una experiencia para un jugador y no ha dado fecha para un online. GTA Online, el de GTA 5, sigue activo. "
     "Nuestra predicción: no antes de 2027. Confianza, cincuenta y cinco por ciento."),
    ("Sobre dos: ¿habrá un modo a sesenta cuadros por segundo? Lo que sabemos: el objetivo oficial es treinta, también en PS5 Pro, y el estudio no se ha comprometido con sesenta. "
     "Nuestra predicción: el día del lanzamiento, no. Confianza, setenta y cinco por ciento."),
    ("Sobre tres: ¿cuántos edificios se podrán visitar por dentro? Lo que sabemos: no hay ninguna cifra oficial. "
     "Nuestra predicción: más que en GTA 5. Confianza, sesenta por ciento."),
    ("Sobre cuatro: ¿cuánto pesa el Perfil Criminal? Lo que sabemos: Rob Nelson, de Rockstar, dijo que las acciones constantes pueden influir en cómo reacciona el mundo y en la narrativa. "
     "Nuestra predicción: va a cambiar más el mundo que la trama principal. Confianza, cincuenta por ciento."),
    ("Sobre cinco: ¿los huracanes serán dinámicos o solo de historia? Lo que sabemos: según Game Informer, tormentas tropicales y huracanes pueden azotar Leonida. "
     "Nuestra predicción: las dos cosas, clima libre y momentos de misión. Confianza, cincuenta por ciento."),
    ("Sobre seis: ¿qué animal será legendario? Lo que sabemos: habrá animales raros, descubribles y legendarios, pero nadie dijo cuáles. "
     "Nuestra predicción: un animal emblemático de Florida, como la pantera. Confianza, cuarenta por ciento."),
    ("Sobre siete: ¿hay más de seis regiones? Lo que sabemos: hay seis regiones con nombre, y el mapa es el doble que el de GTA 5. "
     "Nuestra predicción: muchas más zonas y pueblos dentro de esas regiones, pero no una séptima región grande. Confianza, cincuenta por ciento."),
]
for i, vo in enumerate(VO):
    beat(vo, make_myst(i), section=f"SOBRE {i + 1}", energy=2 if i % 3 else 1, trans=("slide_up", 0.5),
         sfx=[(0.3, "seal", 0.6), (0.9, "paper", 0.5), ("w:Lo que sabemos", "tick", 0.4), ("w:Nuestra predicción", "pop", 0.4), ("w:Confianza", "riser", 0.2)])
beat("Siete sobres, siete apuestas. El jueves los abrimos jugando, uno por uno. Si quieres ver cuántas acertamos, y cuántas fallamos, suscríbete. "
     "Y deja tu predicción en los comentarios: la más acertada se lleva el comentario fijado.",
     sc_close, section="CIERRE", energy=2, trans=("fade", 0.6), sfx=[("w:Siete sobres", "ding", 0.4)])
beat("", sc_end, dur=20, section="PANTALLA FINAL", energy=1, trans=("fade", 0.6))

VIDEO = dict(id="v09", folder="VIDEO_09", file="GTA6_7_misterios_que_se_resuelven_el_jueves",
             title="7 misterios de GTA 6 que se resuelven el jueves (y nuestras predicciones)",
             format="Largo (16:9)", music="mystery", music_seed=91, voice="host", beats=B, overlay=overlay, music_gain=0.55)

def thumbnail(c):
    W, H = 1280, 720
    velvet(c, W, H, 0.3)
    envelope(c, 420, 400, 1.05, 7, "", 0.3, open_p=0.0)
    draw_text(c, "7", 760, 300, "syne", 280, GOLD, 1)
    draw_text(c, "MISTERIOS", 760, 420, "syne", 92, WHITE, 1)
    rect(c, 760, 460, 470, 90, SUN, 1, r=12); draw_text(c, "¿ACERTAREMOS?", 995, 522, "syne", 52, "#1B1040", 1, align="center")
    draw_text(c, "GTA VI · SE ABREN EL JUEVES", 70, 680, "monob", 36, WHITE, 0.9, tracking=2)
