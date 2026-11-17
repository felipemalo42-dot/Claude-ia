"""VIDEO 05 — Expediente Jason y Lucía: lo que Rockstar ya contó (sin spoilers).
Lenguaje visual: expediente policial sobre escritorio, máquina de escribir (Special Elite / Courier Prime),
sellos de tinta, tablero de evidencias con hilo rojo, polaroids con SILUETAS GENÉRICAS (sin parecido con los personajes).
Dos voces: narrador + analista (lee los expedientes). Música: noir original (piano eléctrico FM + batería con swing).
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL

DESK1, DESK2 = "#22170F", "#0F0A07"; MANILA = "#D8B97E"; MANILA_D = "#B9965A"; PAPER = "#F1EADB"; INK = "#1D1B18"
STAMP = "#B3261E"; CORK = "#7D5E3C"; STRING = "#C9252C"; MAG = "#FF4FA0"; CYAN = "#3EE6FF"; GOLD = "#E8B04A"

def desk(c, W, H, t, lamp=(0.3, 0.2)):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [DESK1, DESK2]))
    for i in range(0, H, 9): rect(c, 0, i, W, 2, "#000000", 0.05 + 0.03 * math.sin(i * 0.13))  # vetas
    c.drawCircle(W * lamp[0], H * lamp[1], W * 0.75, rad_grad(W * lamp[0], H * lamp[1], W * 0.75, [hexc("#FFD9A0", 0.22), hexc("#FFD9A0", 0)]))
    # humo/polvo suave en el haz de luz
    bokeh(c, W, H, t, 14, ("#FFE2B8",), seed=5, size=(4, 14), a=0.18, speed=6)

def silhouette(c, cx, cy, s, rim, hair="long", a=1.0):
    """Silueta genérica de busto (no representa a ningún personaje concreto)."""
    c.save(); c.translate(cx, cy); c.scale(s, s)
    body = skia.Path(); body.moveTo(-150, 200); body.cubicTo(-140, 110, -80, 80, -40, 70); body.lineTo(-30, 30); body.lineTo(30, 30); body.lineTo(40, 70)
    body.cubicTo(80, 80, 140, 110, 150, 200); body.close()
    head = skia.Path(); head.addOval(skia.Rect.MakeXYWH(-55, -110, 110, 140))
    hairp = skia.Path()
    if hair == "long":
        hairp.moveTo(-62, -40); hairp.cubicTo(-75, -130, 75, -130, 62, -40); hairp.cubicTo(80, 20, 85, 70, 60, 95); hairp.lineTo(40, 40); hairp.lineTo(-40, 40); hairp.lineTo(-60, 95); hairp.cubicTo(-85, 70, -80, 20, -62, -40); hairp.close()
    else:
        hairp.moveTo(-58, -50); hairp.cubicTo(-60, -125, 60, -125, 58, -50); hairp.lineTo(50, -70); hairp.lineTo(-50, -70); hairp.close()
    for pth in (hairp, body, head):
        c.drawPath(pth, paint(rim, 0.55 * a, stroke=10, blur=10)); c.drawPath(pth, paint(rim, a, stroke=3.5))
    for pth in (body, head, hairp): c.drawPath(pth, paint("#0B0C10", a))
    c.restore()

def polaroid(c, x, y, rot, rim, hair, label, p, s=1.0):
    if p <= 0: return
    c.save(); c.translate(x, y - (1 - ease_out(p)) * 300); c.rotate(rot * (0.6 + 0.4 * p)); c.scale(s, s)
    rect(c, -170, -200, 340, 410, "#000000", 0.35, blur=14)
    rect(c, -165, -205, 330, 400, "#F6F3EC", 1, r=4)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-145, -185, 290, 290))
    rect(c, -145, -185, 290, 290, "#15151C"); c.drawCircle(0, -60, 220, rad_grad(0, -60, 220, [hexc(rim, 0.35), hexc(rim, 0)]))
    silhouette(c, 0, -20, 0.95, rim, hair)
    c.restore()
    draw_text(c, label, 0, 160, "marker", 40, INK, 1, align="center")
    rect(c, -40, -222, 80, 30, "#E9E1C8", 0.8)  # cinta adhesiva
    c.restore()

def stamp(c, x, y, txt, p, rot=-12, col=STAMP, size=64):
    if p <= 0: return
    s = 1 + 0.6 * (1 - ease_out(p)); a = clamp(p * 2)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w = text_w(txt, font("elite", size), 4) + 50
    rect(c, -w / 2, -size * 0.85, w, size * 1.35, col, 0.9 * a, r=8, stroke=6)
    draw_text(c, txt, 0, size * 0.32, "elite", size, col, 0.9 * a, align="center", tracking=4)
    c.restore()

def typed_field(c, x, y, label, value, t, st, maxw=760, size=34, cps=38):
    if t < st: return 0
    draw_text(c, label, x, y, "courierb", 24, "#6B5B3E", 1, tracking=2)
    shown = typewriter(value, t - st, cps)
    return draw_par(c, shown, x, y + 44, "elite", size, maxw, color=INK, lh=1.25) + 60

def folder(c, W, H, t, name, rim, hair, fields, info, tag_cues, cam=1.0):
    desk(c, W, H, t)
    c.save(); z = 1 + 0.03 * cam * prog(t, 0, info.d); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    rect(c, 110, 110, 1700, 900, "#000000", 0.4, blur=20)
    rect(c, 100, 100, 1700, 880, MANILA, 1, r=10); rect(c, 300, 70, 300, 60, MANILA, 1, r=10)
    rect(c, 940, 100, 4, 880, MANILA_D, 1)
    draw_text(c, "CONFIDENCIAL · CAIMÁN NEÓN", 330, 112, "courierb", 22, "#6B5B3E", 1, tracking=2)
    polaroid(c, 520, 520, -4, rim, hair, name, prog(t, 0.2, 0.9), s=1.15)
    rect(c, 990, 150, 760, 790, PAPER, 1, r=4)
    for k in range(18): rect(c, 990, 210 + k * 42, 760, 1, "#9CB4D0", 0.35)
    y = 200
    for (lab, val, cue) in fields:
        y += typed_field(c, 1020, y, lab, val, t, info.w(cue, default=999) if isinstance(cue, str) else cue, maxw=700)
    for (txt, cue, x, yy, rot) in tag_cues:
        st = info.w(cue, default=999); stamp(c, x, yy, txt, prog(t, st, st + 0.25), rot, size=44, col={"OFICIAL": "#1E7B45", "REPORTADO": "#1F5E8C", "DEDUCCIÓN": "#9C6B00"}.get(txt, STAMP))
    c.restore()

# ---------------------------------------------------------------- escenas
def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H; desk(c, W, H, t)
    z = 1 + 0.05 * prog(t, 0, info.d); c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    s1 = info.w("Ella"); s2 = info.w("Él trabaja")
    polaroid(c, 600, 500, -6, MAG, "long", "SUJETO 1", prog(t, s1 - 0.4, s1 + 0.3))
    polaroid(c, 1320, 500, 5, CYAN, "short", "SUJETO 2", prog(t, s2 - 0.4, s2 + 0.3))
    if t > s1 + 0.6: draw_text(c, typewriter("SALIÓ DE UNA PRISIÓN DE LEONIDA", t - s1 - 0.6, 30), 600, 830, "elite", 34, PAPER, 1, align="center")
    if t > s2 + 0.6: draw_text(c, typewriter("TRABAJA PARA TRAFICANTES", t - s2 - 0.6, 30), 1320, 830, "elite", 34, PAPER, 1, align="center")
    st = info.w("los abrimos"); stamp(c, W / 2, 930, "EXPEDIENTE ABIERTO", prog(t, st, st + 0.3), -4, size=70)
    st = info.w("sin un solo spoiler"); stamp(c, W / 2, 200, "SIN SPOILERS", prog(t, st, st + 0.3), 3, "#1E7B45", 56)
    c.restore(); vignette(c, W, H, 0.6)

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_intro(c, t, info, ctx):
    W, H = ctx.W, ctx.H; desk(c, W, H, t)
    p = ease_out(prog(t, 0, 0.8)); c.save(); c.translate(0, (1 - p) * 200)
    rect(c, 420, 140, 1080, 780, "#000000", 0.4, blur=20); rect(c, 410, 130, 1080, 780, MANILA, 1, r=10); rect(c, 560, 100, 300, 60, MANILA, 1, r=10)
    draw_text(c, "EXPEDIENTE", W / 2, 360, "elite", 110, INK, 1, align="center", tracking=8)
    draw_text(c, "DUVAL · CAMINOS", W / 2, 470, "elite", 76, INK, 1, align="center", tracking=4)
    rect(c, 640, 510, 640, 3, INK, 0.6)
    draw_text(c, "FUENTES: WEB OFICIAL · TRÁILERES · PRENSA", W / 2, 570, "courierb", 30, "#5B4A2E", 1, align="center", tracking=2)
    c.restore()
    stamp(c, 620, 760, "OFICIAL", prog(t, info.w("web"), info.w("web") + 0.3), -8, "#1E7B45", 50)
    stamp(c, 960, 790, "REPORTADO", prog(t, info.w("etiqueta"), info.w("etiqueta") + 0.3), 4, "#1F5E8C", 50)
    stamp(c, 1300, 760, "DEDUCCIÓN", prog(t, info.w("deducción"), info.w("deducción") + 0.3), -5, "#9C6B00", 50)
    vignette(c, W, H, 0.55)

def sc_lucia(c, t, info, ctx):
    fields = [("NOMBRE", "Lucía Caminos", "Expediente número uno"), ("ANTECEDENTES", "Pelear por su familia la llevó a la Penitenciaría de Leonida.", "Penitenciaría"),
              ("SALIDA", "“Pura suerte”. Desde ahora: solo jugadas inteligentes.", "suerte"),
              ("TRÁILER DE LANZAMIENTO", "Tobillera electrónica visible en su pierna.", "tobillera")]
    tags = [("OFICIAL", "Penitenciaría", 1600, 880, -8), ("REPORTADO", "prensa", 1180, 880, 6)]
    folder(c, ctx.W, ctx.H, t, "LUCÍA", MAG, "long", fields, info, tags)
    vignette(c, ctx.W, ctx.H, 0.5)

def sc_jason(c, t, info, ctx):
    fields = [("NOMBRE", "Jason Duval", "Expediente número dos"), ("ORIGEN", "Creció rodeado de estafadores y ladrones.", "estafadores"),
              ("HISTORIAL", "Ejército → los Keys, trabajando para traficantes locales.", "ejército"),
              ("TRÁILER DE LANZAMIENTO", "Se metió en problemas en el servicio y no salió en buenos términos.", "tráiler de lanzamiento")]
    tags = [("OFICIAL", "Keys", 1600, 880, -6), ("REPORTADO", "tráiler de lanzamiento", 1180, 880, 5)]
    folder(c, ctx.W, ctx.H, t, "JASON", CYAN, "short", fields, info, tags)
    vignette(c, ctx.W, ctx.H, 0.5)

def sc_board(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [CORK, "#5E452B"]))
    rng = np.random.default_rng(3)
    for _ in range(500): circle(c, rng.random() * W, rng.random() * H, rng.random() * 2.2, "#3E2C18", 0.35)
    pan = 40 * math.sin(t * 0.15); c.save(); c.translate(pan, 0)
    pl, pj = (430, 360), (1490, 360)
    polaroid(c, *pl, -5, MAG, "long", "LUCÍA", 1.0, 0.8); polaroid(c, *pj, 4, CYAN, "short", "JASON", 1.0, 0.8)
    notes = [("UN GOLPE FÁCIL SALE MAL", (960, 300), "golpe fácil"), ("CONSPIRACIÓN EN TODO LEONIDA", (960, 520), "conspiración"),
             ("CONFIAR EL UNO EN EL OTRO", (960, 740), "confiar")]
    for txt, (x, y), cue in notes:
        st = info.w(cue, default=999); p = prog(t, st, st + 0.4)
        if p <= 0: continue
        e = ease_out(p)
        for src in (pl, pj):
            pth = skia.Path(); pth.moveTo(src[0], src[1] - 140); pth.quadTo((src[0] + x) / 2, (src[1] + y) / 2 + 60, x, y)
            c.drawPath(partial_path(pth, e), paint(STRING, 0.95, stroke=4))
        c.save(); c.translate(x, y); c.rotate(-2 + 4 * ((hash(txt) % 3) - 1)); c.scale(e, e)
        rect(c, -280, -60, 560, 120, "#FFF59A", 1, r=2); draw_text(c, txt, 0, 12, "marker", 36, INK, 1, align="center")
        circle(c, 0, -50, 12, STRING, 1); c.restore()
    cert = info.w("Rockstar los presenta", default=999)
    if t > cert: stamp(c, 960, 930, "OFICIAL", prog(t, cert, cert + 0.3), -6, "#1E7B45", 54)
    c.restore(); vignette(c, W, H, 0.55)

def sc_switch(c, t, info, ctx):
    W, H = ctx.W, ctx.H; desk(c, W, H, t, lamp=(0.5, 0.2))
    st = info.w("cambiar"); p = ease_out(prog(t, st - 0.5, st))
    sw = (math.sin((t - st) * 1.6) > 0) if t > st else True
    for i, (rim, hair, lab) in enumerate(((MAG, "long", "LUCÍA"), (CYAN, "short", "JASON"))):
        act = (i == 0) == sw; x = 640 + i * 640
        c.save(); c.translate(x, 470); s = 0.9 + 0.12 * (1 if act else 0); c.scale(s, s)
        circle(c, 0, 0, 230, rim, 0.18 if act else 0.05); circle(c, 0, 0, 230, rim, 1 if act else 0.25, stroke=5)
        silhouette(c, 0, 10, 0.95, rim, hair, a=1 if act else 0.35); c.restore()
        draw_text(c, lab, x, 790, "elite", 60, rim, 1 if act else 0.35, align="center", tracking=6)
    # flechas de cambio
    pa = paint(GOLD, p, stroke=6); pth = skia.Path(); pth.moveTo(860, 400); pth.quadTo(960, 330, 1060, 400); c.drawPath(pth, pa)
    pth = skia.Path(); pth.moveTo(1060, 540); pth.quadTo(960, 610, 860, 540); c.drawPath(pth, pa)
    draw_poly(c, [(1060, 400), (1035, 375), (1030, 410)], GOLD, p); draw_poly(c, [(860, 540), (885, 565), (890, 530)], GOLD, p)
    draw_text(c, "CAMBIO EN PLENA ACCIÓN · SIN PANTALLA DE CARGA", W / 2, 900, "courierb", 40, PAPER, p, align="center", tracking=2)
    cert_tag(c, W / 2, 940, "OFICIAL", p, 24, align="center", t=p)
    s2 = info.w("opcional", default=999); p2 = ease_out_back(prog(t, s2, s2 + 0.4))
    if p2 > 0:
        c.save(); c.translate(W / 2, 200); c.scale(p2, p2)
        rect(c, -520, -70, 1040, 140, PAPER, 1, r=8); draw_text(c, "RELACIÓN ROMÁNTICA OPCIONAL", 0, 18, "elite", 52, INK, 1, align="center")
        c.restore(); cert_tag(c, W / 2 + 360, 260, "REPORTADO", 1, 24, t=p2)
        cert_tag(c, W / 2 - 560, 260, "SIN CONFIRMAR", 1, 24, t=p2)

CAST = [("CAL HAMPTON", "Amigo y socio de Jason. Desconfiado, de teorías conspirativas.", "Cal", "eye"),
        ("BOOBIE IKE", "Leyenda local de Vice City: de un club nocturno a un estudio de grabación.", "Boobie", "star"),
        ("DRE'QUAN PRIEST", "Busca su gran oportunidad en la industria musical.", "Dre'Quan", "chat"),
        ("REAL DIMEZ", "Dúo de rap con una presencia incansable en redes.", "Real Dimez", "wifi"),
        ("RAUL BAUTISTA", "Ladrón de bancos veterano, siempre buscando talento.", "Raul", "money"),
        ("BRIAN HEDER", "Casero de Jason; veterano del contrabando.", "Brian", "user")]

def sc_cast(c, t, info, ctx):
    W, H = ctx.W, ctx.H; desk(c, W, H, t, lamp=(0.5, 0.1))
    for i, (name, desc, cue, ic) in enumerate(CAST):
        st = info.w(cue, default=999); p = prog(t, st - 0.3, st + 0.3)
        if p <= 0: continue
        col, row = i % 3, i // 3; x = 360 + col * 600; y = 330 + row * 400
        rot = [-4, 2, -2, 3, -3, 4][i]
        c.save(); c.translate(x, y - (1 - ease_out(p)) * 120); c.rotate(rot); c.scale(0.9 + 0.1 * ease_out(p), 0.9 + 0.1 * ease_out(p))
        rect(c, -255, -160, 520, 330, "#000000", 0.35, blur=12)
        rect(c, -260, -170, 520, 330, PAPER, 1, r=4); rect(c, -260, -170, 520, 56, "#E7DCC2", 1, r=4)
        draw_text(c, name, -235, -130, "courierb", 32, INK, 1, tracking=1)
        icon(c, ic, 200, -142, 38, STAMP)
        for k in range(5): rect(c, -260, -60 + k * 44, 520, 1, "#9CB4D0", 0.5)
        draw_par(c, desc, -235, -20, "elite", 31, 470, color=INK, lh=1.35)
        c.restore()
    st = info.w("reparto"); p = ease_out(prog(t, st, st + 0.4))
    draw_text(c, "REPARTO CONFIRMADO", W / 2, 110, "elite", 64, PAPER, p, align="center", tracking=6)
    cert_tag(c, W / 2, 130, "OFICIAL", p, 22, align="center", t=p)
    source_chip(c, 60, 1000, "Web oficial de Rockstar (mayo 2025), vía VGC / GamesRadar", p)

def sc_unknown(c, t, info, ctx):
    W, H = ctx.W, ctx.H; desk(c, W, H, t)
    rect(c, 360, 90, 1200, 900, "#000000", 0.35, blur=16); rect(c, 350, 80, 1200, 900, PAPER, 1, r=4)
    draw_text(c, "LO QUE NO SABEMOS", W / 2, 180, "elite", 64, INK, 1, align="center", tracking=4)
    lines = [("¿Cómo termina?", "termina"), ("¿Hay varios finales?", "finales"), ("¿Cuánto pesan tus decisiones?", "decisiones")]
    for i, (q, cue) in enumerate(lines):
        st = info.w(cue, default=999); y = 300 + i * 110
        if t < st: rect(c, 420, y - 40, 900, 56, INK, 1); continue
        draw_text(c, q, 430, y, "elite", 44, INK, 1)
        rect(c, 1000, y - 40, 480 * (1 - ease_out(prog(t, st, st + 0.6))) + 1, 56, INK, 1)
        draw_text(c, "[CLASIFICADO]", 1260, y, "courierb", 30, STAMP, ease_out(prog(t, st + 0.4, st + 0.8)), align="center")
    st = info.w("Rob Nelson"); p = ease_out(prog(t, st, st + 0.5))
    if p > 0:
        rect(c, 420, 640, 1060, 260, "#F7F1E0", p, r=4); rect(c, 420, 640, 8, 260, "#1E7B45", p)
        draw_par(c, "“Las acciones constantes pueden influir en cómo reacciona el mundo y en cómo se desarrolla la narrativa.”", 460, 700, "dmserifi", 40, 980, color=INK, a=p, lh=1.2)
        draw_text(c, "— Rob Nelson, Rockstar (sobre el Perfil Criminal)", 460, 870, "courierb", 26, "#5B4A2E", p)
        cert_tag(c, 1460, 600, "OFICIAL", p, 22, align="right", t=p)
    vignette(c, W, H, 0.55)

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "¿JASON O LUCÍA?", "Cuéntalo en los comentarios", MAG)

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2.5 < gt < ctx.total - 20:
        watermark(c, W, H, 0.5)
    if gt < 9: ai_notice(c, W, H, clamp(9 - gt), "Siluetas y documentos ilustrados por Caimán Neón · sin arte oficial ni imágenes del juego")

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Ella salió de una prisión de Leonida. Él trabaja para traficantes en los Cayos. Rockstar ya nos dio sus expedientes... y hoy los abrimos, sin un solo spoiler.",
     sc_hook, section="GANCHO", energy=1, sfx=[("w:Ella", "shutter", 0.5), ("w:Él trabaja", "shutter", 0.5), ("w:los abrimos", "stamp", 0.8), ("w:sin un solo spoiler", "stamp", 0.6)])
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=1, trans=("flash", 0.3))
beat("Esto es Caimán Neón. Regla de hoy: solo usamos lo que Rockstar publicó en su web y en sus tráileres, y lo que reportó la prensa que habló con el estudio. "
     "Cada dato lleva su etiqueta. Y si algo es deducción nuestra, te lo vamos a decir en voz alta.",
     sc_intro, section="INTRODUCCIÓN", energy=1, trans=("zoom", 0.5), sfx=[(0.1, "paper", 0.5), ("w:web", "stamp", 0.5), ("w:etiqueta", "stamp", 0.5), ("w:deducción", "stamp", 0.5)])
beat("Expediente número uno: Lucía Caminos. Según la web oficial, su padre le enseñó a pelear desde muy pequeña. Pelear por su familia la llevó a la Penitenciaría de Leonida, y salió gracias a la pura suerte. "
     "Desde entonces, dice Rockstar, solo jugadas inteligentes. "
     "En el tráiler de lanzamiento de octubre se ve una tobillera electrónica en su pierna, y la prensa que habló con Rockstar asegura que tendrá un papel en la historia.",
     sc_lucia, section="EXPEDIENTE 1 · LUCÍA", voice="analista", energy=2, trans=("whip", 0.45),
     sfx=[(0.1, "paper", 0.5), ("w:Lucía Caminos", "typing", 0.4), ("w:Penitenciaría", "typing", 0.4), ("w:suerte", "typing", 0.4), ("w:tobillera", "typing", 0.4), ("w:Penitenciaría", "stamp", 0.5)])
beat("Expediente número dos: Jason Duval. Rockstar cuenta que creció rodeado de estafadores y ladrones. Pasó por el ejército intentando dejar atrás una adolescencia problemática, y terminó en los Keys haciendo lo que mejor sabe: trabajar para traficantes locales. "
     "El tráiler de lanzamiento sugiere que se metió en problemas durante el servicio y que no salió en buenos términos.",
     sc_jason, section="EXPEDIENTE 2 · JASON", voice="analista", energy=2, trans=("whip", 0.45),
     sfx=[(0.1, "paper", 0.5), ("w:Jason Duval", "typing", 0.4), ("w:estafadores", "typing", 0.4), ("w:ejército", "typing", 0.4), ("w:tráiler de lanzamiento", "typing", 0.4), ("w:Keys", "stamp", 0.5)])
beat("¿Y qué los une? Rockstar los presenta así: Jason y Lucía siempre supieron que tenían las cartas en contra. Pero cuando un golpe fácil sale mal, terminan en el lado más oscuro del lugar más soleado de Estados Unidos, "
     "en medio de una conspiración criminal que atraviesa toda Leonida, obligados a confiar el uno en el otro más que nunca si quieren salir con vida.",
     sc_board, section="LA PAREJA", energy=2, trans=("zoom", 0.5), sfx=[("w:golpe fácil", "pin", 0.5), ("w:conspiración", "pin", 0.5), ("w:confiar", "pin", 0.5)])
beat("En la jugabilidad, el Extended Look de agosto mostró algo clave: puedes cambiar entre Jason y Lucía en plena acción, sin pantalla de carga. "
     "Y un detalle que la prensa ha repetido, pero que todavía no podemos comprobar: la relación romántica entre ambos sería opcional.",
     sc_switch, section="DOS PROTAGONISTAS", energy=2, trans=("whip", 0.45), sfx=[("w:cambiar", "whoosh", 0.5), ("w:opcional", "stamp", 0.5)])
beat("Ahora, el reparto que Rockstar ya confirmó. Cal Hampton, amigo y socio de Jason, desconfiado y amante de las teorías de conspiración. "
     "Boobie Ike, una leyenda local de Vice City con negocios que van de la noche a la música. "
     "Dre'Quan Priest, que busca su gran oportunidad en la industria musical. "
     "Real Dimez, un dúo de rap con una presencia incansable en redes. "
     "Raul Bautista, un ladrón de bancos veterano que siempre está buscando talento. "
     "Y Brian Heder, el casero de Jason, un veterano del contrabando.",
     sc_cast, section="REPARTO", energy=2, trans=("whip", 0.45),
     sfx=[("w:Cal", "paper", 0.5), ("w:Boobie", "paper", 0.5), ("w:Dre'Quan", "paper", 0.5), ("w:Real Dimez", "paper", 0.5), ("w:Raul", "paper", 0.5), ("w:Brian", "paper", 0.5)])
beat("¿Y lo que no sabemos? No sabemos cómo termina. No sabemos si hay varios finales. Tampoco sabemos cuánto pesan tus decisiones. "
     "Lo más parecido a una pista lo dio Rob Nelson, de Rockstar: dijo que las acciones constantes pueden influir en cómo reacciona el mundo y en cómo se desarrolla la narrativa. "
     "Cualquier cosa más allá de eso, hoy, sería inventar.",
     sc_unknown, section="LO QUE NO SABEMOS", energy=1, trans=("fade", 0.5), sfx=[("w:termina", "typing", 0.4), ("w:finales", "typing", 0.4), ("w:decisiones", "typing", 0.4), ("w:Rob Nelson", "ding", 0.3)])
beat("El jueves empieza el caso de verdad. Si quieres un análisis de la historia sin spoilers durante la primera semana, suscríbete a Caimán Neón. "
     "Y cuéntame en los comentarios: ¿con quién vas a jugar más, con Jason o con Lucía?",
     sc_end, section="LLAMADA A LA ACCIÓN", energy=2, hold=4.0, min=20, trans=("fade", 0.6))

VIDEO = dict(id="v05", folder="VIDEO_05", file="GTA6_Jason_y_Lucia_expediente_sin_spoilers",
             title="Jason y Lucía: todo lo que Rockstar ya contó de los protagonistas de GTA 6 (sin spoilers)",
             format="Largo (16:9)", music="noir", music_seed=51, voice="host", beats=B, overlay=overlay, music_gain=0.55)

def thumbnail(c):
    W, H = 1280, 720
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [DESK1, DESK2]))
    c.drawCircle(640, 300, 700, rad_grad(640, 300, 700, [hexc("#FFD9A0", 0.18), hexc("#FFD9A0", 0)]))
    rect(c, 300, 60, 680, 620, MANILA, 1, r=10)
    c.drawCircle(380, 380, 320, rad_grad(380, 380, 320, [hexc(MAG, 0.45), hexc(MAG, 0)])); c.drawCircle(900, 380, 320, rad_grad(900, 380, 320, [hexc(CYAN, 0.45), hexc(CYAN, 0)]))
    silhouette(c, 360, 360, 1.25, MAG, "long"); silhouette(c, 920, 360, 1.25, CYAN, "short")
    rect(c, 0, 520, W, 200, "#000000", 0.55)
    draw_text(c, "JASON Y LUCÍA", W / 2, 640, "anton", 120, "#FFFFFF", 1, align="center", tracking=2)
    stamp(c, 640, 110, "EXPEDIENTE", 1.0, -6, STAMP, 70)
    c.save(); c.translate(1120, 470); c.rotate(8); rect(c, -150, -40, 300, 80, "#1E7B45", 1, r=8); draw_text(c, "SIN SPOILERS", 0, 14, "anton", 44, "#FFFFFF", 1, align="center"); c.restore()
