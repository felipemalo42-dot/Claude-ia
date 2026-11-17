"""VIDEO 08 — SHORT: Fauna de Leonida — los 4 animales que Rockstar ya nombró (guía de campo).
Lenguaje visual: cuaderno de naturalista: papel crema, ilustraciones vectoriales originales a tinta y acuarela plana,
Abril Fatface + Caveat, anotaciones a mano, fichas que se pasan como páginas. Voz: analista (documental). Música: 'nature' original.
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL, draw_caiman

W, H = 1080, 1920
PAPER = "#F3EBD8"; PAPER2 = "#E9DEC4"; INK = "#22301F"; SAGE = "#7FA37A"; FLAM = "#F27BA0"; TEAL = "#3C8C8A"; OCHRE = "#C98B2E"; GREY = "#8A8F98"

def paper(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [PAPER, PAPER2]))
    rng = np.random.default_rng(8)
    for _ in range(260): circle(c, rng.random() * W, rng.random() * H, rng.random() * 2.5, "#B9A985", 0.25)
    for k in range(40): rect(c, 0, 120 + k * 46, W, 1, "#9DB4C8", 0.18)
    rect(c, 110, 0, 2, H, "#D98C8C", 0.4)

def wash(c, x, y, rx, ry, col, a=0.35, seed=1):
    rng = np.random.default_rng(seed)
    for k in range(4):
        c.drawOval(skia.Rect.MakeXYWH(x - rx + rng.normal(0, 10), y - ry + rng.normal(0, 8), 2 * rx * (0.9 + 0.2 * rng.random()), 2 * ry * (0.9 + 0.2 * rng.random())), paint(col, a * 0.5, blur=12))

def ink(c, pth, fill, a=1.0, w=5):
    c.drawPath(pth, paint(fill, a)); c.drawPath(pth, paint(INK, a, stroke=w))

# ---------------------------------------------------------------- ilustraciones originales
def gator(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    wash(c, 0, 40, 420, 70, TEAL, 0.5, 2)
    sway = math.sin(t * 1.5) * 12
    body = skia.Path(); body.moveTo(-120, -10); body.cubicTo(-60, -45, 120, -45, 170, -15); body.cubicTo(200, 0, 200, 20, 170, 30)
    body.cubicTo(120, 45, -60, 45, -120, 20); body.cubicTo(-220, 10 + sway * 0.3, -330, 10 + sway, -420, 20 + sway); body.cubicTo(-330, 0 + sway, -220, -10, -120, -10); body.close()
    ink(c, body, "#5E7F4E", a)
    for i in range(9): line(c, -100 + i * 28, -32, -88 + i * 28, -32, INK, 0.6 * a, 3)
    for lx, d in ((-80, 1), (-40, -1), (110, 1), (140, -1)):
        leg = poly([(lx, 25), (lx + 18 * d, 70), (lx + 40 * d, 74), (lx + 22, 30)]); ink(c, leg, "#4E6B40", a, 4)
    c.restore()
    draw_caiman(c, x + 130 * s, y - 52 * s, 0.95 * s, t=t, line_col=INK, eye_col=OCHRE, fill="#5E7F4E", glow=False, lw=5 / max(0.5, s), a=a)

def flamingo(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    wash(c, 0, 0, 160, 260, FLAM, 0.45, 3)
    bob = math.sin(t * 2.0) * 8
    line(c, -5, 60, -5, 330, INK, a, 6); line(c, 25, 60, 25, 170, INK, a, 6); line(c, 25, 170, -20, 220, INK, a, 6)
    body = skia.Path(); body.addOval(skia.Rect.MakeXYWH(-110, -40, 210, 120)); ink(c, body, FLAM, a)
    wing = skia.Path(); wing.moveTo(-60, -10); wing.cubicTo(-10, -40, 60, -20, 80, 30); wing.cubicTo(20, 40, -40, 30, -60, -10); ink(c, wing, "#E0628A", a, 4)
    neck = skia.Path(); neck.moveTo(70, 0); neck.cubicTo(150, -40, 40, -140, 90, -230 + bob); c.drawPath(neck, paint(INK, a, stroke=30)); c.drawPath(neck, paint(FLAM, a, stroke=22))
    head = skia.Path(); head.addCircle(95, -240 + bob, 26); ink(c, head, FLAM, a, 4)
    beak = poly([(110, -250 + bob), (165, -230 + bob), (150, -200 + bob), (118, -225 + bob)]); ink(c, beak, "#2B2B2B", a, 3)
    circle(c, 92, -246 + bob, 5, INK, a)
    c.restore()

def pelican(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    wash(c, 0, 20, 260, 170, "#8FB3C9", 0.45, 4)
    flap = math.sin(t * 2.5) * 8
    post = skia.Path(); post.addRect(skia.Rect.MakeXYWH(-40, 110, 80, 150)); ink(c, post, "#8B6A44", a, 4)
    body = skia.Path(); body.moveTo(-170, 40); body.cubicTo(-160, -60, 60, -80, 110, -10); body.cubicTo(120, 60, 20, 120, -60, 120); body.cubicTo(-120, 110, -170, 90, -170, 40); body.close(); ink(c, body, "#B7B9B4", a)
    wing = skia.Path(); wing.moveTo(-140, 20 + flap); wing.cubicTo(-80, -40, 40, -30, 70, 30 + flap); wing.cubicTo(0, 60, -90, 70, -140, 20 + flap); ink(c, wing, "#6F7470", a, 4)
    neck = skia.Path(); neck.moveTo(70, -10); neck.cubicTo(120, -60, 60, -140, 110, -170); c.drawPath(neck, paint(INK, a, stroke=34)); c.drawPath(neck, paint("#D9D6CB", a, stroke=26))
    head = skia.Path(); head.addCircle(118, -175, 30); ink(c, head, "#EDE7D3", a, 4)
    beak = poly([(140, -185), (320, -150), (300, -130), (150, -150)]); ink(c, beak, OCHRE, a, 4)
    pouch = skia.Path(); pouch.moveTo(150, -150); pouch.cubicTo(200, -90, 280, -110, 300, -132); pouch.close(); ink(c, pouch, "#D7A35A", a, 3)
    circle(c, 115, -182, 5, INK, a)
    c.restore()

def manatee(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y + math.sin(t * 1.2) * 10); c.scale(s, s)
    wash(c, 0, 0, 380, 160, TEAL, 0.55, 5)
    for k in range(6):
        yy = -150 + k * 60; pth = skia.Path(); pth.moveTo(-420, yy)
        for xx in range(-420, 440, 40): pth.lineTo(xx, yy + math.sin(xx * 0.03 + t * 2 + k) * 6)
        c.drawPath(pth, paint("#6FA9A8", 0.35 * a, stroke=3))
    body = skia.Path(); body.moveTo(-250, 0); body.cubicTo(-240, -110, 150, -120, 230, -40); body.cubicTo(280, 0, 260, 60, 220, 80)
    body.cubicTo(120, 110, -200, 100, -250, 0); body.close(); ink(c, body, "#8E9AA0", a)
    tail = skia.Path(); tail.addOval(skia.Rect.MakeXYWH(-370, -55, 140, 110)); ink(c, tail, "#808C92", a)
    fl = poly([(120, 60), (90, 120), (150, 115)]); ink(c, fl, "#7C878D", a, 4)
    snout = skia.Path(); snout.addOval(skia.Rect.MakeXYWH(200, -40, 90, 80)); ink(c, snout, "#9AA6AB", a, 4)
    circle(c, 215, -30, 5, INK, a)
    for k in range(4): line(c, -120 + k * 70, -60, -110 + k * 70, 40, INK, 0.25 * a, 3)
    c.restore()

ANIMALS = [("ALIGÁTOR AMERICANO", "el que todos llamamos “caimán”", gator, "aligátor", "Grassrivers · pantanos"),
           ("FLAMENCO", "el rosado más famoso de Florida", flamingo, "flamenco", "costas y lagunas"),
           ("PELÍCANO", "patrulla muelles y playas", pelican, "pelícano", "muelles · costa"),
           ("MANATÍ", "la “vaca marina”", manatee, "manatí", "aguas tranquilas")]

def sc_main(c, t, info, ctx):
    paper(c, t)
    # cabecera
    p = ease_out(prog(t, 0, 0.6))
    draw_text(c, "GUÍA DE CAMPO", W / 2, 230, "abril", 92, INK, p, align="center")
    draw_text(c, "fauna de Leonida · edición previa al lanzamiento", W / 2, 290, "caveat", 46, TEAL, p, align="center")
    st = info.w("ciento setenta"); pp = ease_out_back(prog(t, st, st + 0.5))
    if pp > 0 and t < info.w("aligátor") - 0.3:
        c.save(); c.translate(W / 2, 760); c.scale(pp, pp)
        draw_text(c, "170+", 0, 0, "abril", 300, INK, 1, align="center"); draw_text(c, "especies", 0, 100, "caveat", 90, TEAL, 1, align="center")
        c.restore()
        draw_text(c, "según Game Informer (n.º 382)", W / 2, 960, "caveat", 46, INK, 0.8 * pp, align="center")
    st4 = info.w("Rockstar ya nombró")
    if t > st4 and t < info.w("aligátor") - 0.3:
        draw_text(c, "Rockstar ya nombró a 4 →", W / 2, 1100, "caveat", 64, OCHRE, ease_out(prog(t, st4, st4 + 0.4)), align="center")
    # fichas
    cues = [info.w(a[3]) for a in ANIMALS]
    cur = None
    for i, cu in enumerate(cues):
        if t >= cu - 0.3: cur = i
    end_cards = info.w("rastrear")
    if cur is not None and t < end_cards - 0.3:
        name, sub, fn, _, hab = ANIMALS[cur]; st = cues[cur] - 0.3; e = ease_out(prog(t, st, st + 0.5))
        c.save(); c.translate((1 - e) * W, 0)
        fn(c, W / 2 + (70 if cur == 0 else 0), [820, 800, 760, 800][cur], [1.12, 1.1, 1.0, 1.0][cur], t, 1)
        draw_text(c, f"N.º {cur + 1:02d}", 160, 420, "caveat", 60, OCHRE, 1)
        draw_par(c, name, 160, 1180, "abril", 84 if len(name) < 12 else 66, 820, color=INK, lh=1.0)
        draw_text(c, sub, 160, 1300 if len(name) < 12 else 1330, "caveat", 54, TEAL, 1)
        draw_text(c, "hábitat: " + hab, 160, 1370 if len(name) < 12 else 1400, "caveat", 46, INK, 0.75)
        c.restore()
        cert_tag(c, W - 140, 400, "OFICIAL", 1, 26, align="right", t=prog(t, st + 0.3, st + 0.7))
    # rareza
    if t >= end_cards - 0.3:
        e = ease_out(prog(t, end_cards - 0.3, end_cards + 0.3))
        labs = [("RAROS", SAGE), ("DESCUBRIBLES", TEAL), ("LEGENDARIOS", OCHRE)]
        for i, (lab, col) in enumerate(labs):
            pp = ease_out_back(prog(t, end_cards + i * 0.5, end_cards + i * 0.5 + 0.4)); y = 520 + i * 230
            if pp <= 0: continue
            c.save(); c.translate(W / 2, y); c.scale(pp, pp); c.rotate([-2, 1.5, -1][i])
            rect(c, -400, -90, 800, 180, "#FFFFFF", 0.7, r=10); rect(c, -400, -90, 800, 180, col, 1, r=10, stroke=6)
            for k in range(i + 1): draw_text(c, "★", -330 + k * 60, 25, "inter", 60, col, 1)
            draw_text(c, lab, 60, 30, "abril", 70, INK, 1, align="center")
            c.restore()
        sq = info.w("¿Cuáles"); pq = ease_out(prog(t, sq, sq + 0.4))
        if pq > 0: draw_text(c, "¿cuáles serán legendarios? → nadie lo sabe aún", W / 2, 1270, "caveat", 54, OCHRE, pq, align="center")

def overlay(c, gt, ctx):
    short_captions(c, gt, ctx, y=1520, size=68, hl=OCHRE, fontname="abril", maxw=960, box=False)
    draw_caiman(c, W / 2 - 150, 22, 0.36, lw=6, glow=False, line_col=INK, eye_col=FLAM, a=0.9)
    draw_text(c, "CAIMÁN NEÓN", W / 2 - 66, 52, "monob", 24, INK, 0.8, tracking=3)
    draw_text(c, "Ilustraciones originales · no son imágenes del juego", W / 2, 1640, "mono", 20, INK, 0.55, align="center")

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Más de ciento setenta especies. Eso es lo que, según Game Informer, vive en Leonida. Y Rockstar ya nombró a cuatro. "
     "El aligátor americano, al que casi todos llamamos caimán: el rey de los pantanos, visto desde el primer tráiler. "
     "El flamenco, el rosado más famoso de Florida. "
     "El pelícano, patrullando muelles y playas. "
     "Y el manatí, la vaca marina: lenta, enorme y pacífica. "
     "Además, algunos animales se podrán rastrear por rareza: raros, descubribles y legendarios. "
     "¿Cuáles serán legendarios? Todavía nadie lo sabe. Guarda este video: después del lanzamiento armamos la guía de campo completa.",
     sc_main, voice="analista", energy=2, speed=1.04, pause_mul=0.8,
     sfx=[(0.2, "paper", 0.5), ("w:ciento setenta", "pop", 0.4), ("w:aligátor", "paper", 0.6), ("w:flamenco", "paper", 0.6), ("w:pelícano", "paper", 0.6),
          ("w:manatí", "paper", 0.6), ("w:rastrear", "ding", 0.4), (1.5, "bird", 0.4), (9.0, "bird", 0.35), (20.0, "water", 0.4)])

VIDEO = dict(id="v08", folder="VIDEO_08", file="GTA6_fauna_Leonida_guia_de_campo_SHORT", size=(W, H),
             title="Los 4 animales de GTA 6 que Rockstar ya confirmó (y 170 especies más) #shorts", format="Short vertical (9:16)",
             music="nature", music_seed=81, voice="analista", beats=B, overlay=overlay, lead_in=0.2, tail=1.2, music_gain=0.5)

def thumbnail(c):
    Wt, Ht = 1280, 720
    c.drawRect(skia.Rect.MakeWH(Wt, Ht), lin_grad(0, 0, 0, Ht, [PAPER, PAPER2]))
    for k in range(16): rect(c, 0, 40 + k * 46, Wt, 1, "#9DB4C8", 0.2)
    flamingo(c, 1040, 330, 0.95, 0.4)
    gator(c, 560, 600, 0.75, 0.0)
    draw_text(c, "170+", 60, 220, "abril", 210, INK, 1)
    draw_text(c, "especies en Leonida", 70, 300, "caveat", 70, TEAL, 1)
    rect(c, 60, 340, 520, 90, OCHRE, 1, r=10); draw_text(c, "GUÍA DE CAMPO GTA VI", 320, 402, "abril", 44, "#FFFFFF", 1, align="center")
