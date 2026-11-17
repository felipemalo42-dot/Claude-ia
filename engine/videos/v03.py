"""VIDEO 03 — Investigación: 'GTA 6 para PC / Android' — anatomía de la estafa que roba cuentas.
Lenguaje visual: laboratorio forense digital. Carbón + rojo alarma + cian frío, Share Tech Mono / VT323,
diagramas de flujo animados, 'rayos X' sobre archivos, cortes con glitch. Dos voces: narrador + analista.
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL

BG = "#0B0D10"; PANEL = "#12161C"; RED = "#FF3B4E"; CYAN = "#3EE6FF"; WHITE = "#E9EEF2"; DIM = "#5D6875"; GREEN = PAL["caiman"]; AMB = "#FFB020"

def lab_bg(c, W, H, t, alert=0.0):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [BG, "#0E1218", "#0A0C0F"]))
    grid(c, W, H, 48, CYAN, 0.035)
    grid(c, W, H, 240, CYAN, 0.06, wline=1.5)
    # línea de escaneo
    y = (t * 220) % (H + 200) - 100
    c.drawRect(skia.Rect.MakeXYWH(0, y - 60, W, 120), lin_grad(0, y - 60, 0, y + 60, [hexc(CYAN, 0), hexc(CYAN, 0.06), hexc(CYAN, 0)]))
    if alert > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(W / 2, H / 2, W * 0.7, [hexc(RED, 0), hexc(RED, 0.22 * alert)], [0.5, 1]))
    vignette(c, W, H, 0.6)

def hud(c, W, t, title, code):
    draw_text(c, "CAIMÁN NEÓN // LAB", 60, 64, "techmono", 26, CYAN, 0.8, tracking=3)
    draw_text(c, title, 60, 112, "techmono", 46, WHITE, 1, tracking=2)
    draw_text(c, f"EXP-{code} · {int(t * 10) % 10000:04d}", W - 60, 64, "techmono", 24, DIM, 1, align="right", tracking=2)
    rect(c, 60, 132, 560, 2, CYAN, 0.6)
    if int(t * 2) % 2 == 0: circle(c, W - 470, 56, 7, RED, 1)
    draw_text(c, "REC", W - 456, 64, "techmono", 22, RED, 0.9)

def speaker_badge(c, gt, ctx):
    """Indicador de quién habla (sin rostros: solo voz)."""
    cur = None
    for b in ctx.tl["beats"]:
        for s in b["sents"]:
            if s["start"] <= gt <= s["end"] + 0.2: cur = s["voice"]
    if not cur: return
    lab = "NARRADOR" if cur == "host" else "ANALISTA"; col = CYAN if cur == "host" else AMB
    x, y = 60, ctx.H - 110
    rect(c, x, y, 300, 56, "#000000", 0.6, r=10); rect(c, x, y, 6, 56, col, 1)
    for i in range(10):
        h = (0.3 + 0.7 * abs(math.sin(gt * 9 + i * 1.3))) * 30
        rect(c, x + 22 + i * 9, y + 28 - h / 2, 5, h, col, 0.9, r=2)
    draw_text(c, lab, x + 130, y + 38, "techmono", 28, col, 1, tracking=2)

def file_icon(c, x, y, s, name, col=WHITE, a=1.0, xray=0.0, inner="VIDAR"):
    c.save(); c.translate(x, y); c.scale(s, s)
    pth = poly([(-70, -90), (40, -90), (70, -60), (70, 90), (-70, 90)])
    c.drawPath(pth, paint(PANEL, a)); c.drawPath(pth, paint(col, a, stroke=4))
    draw_poly(c, [(40, -90), (40, -60), (70, -60)], col, a * 0.7, stroke=3)
    draw_text(c, ".EXE", 0, 10, "techmono", 34, col, a, align="center")
    if xray > 0:
        c.save(); c.clipPath(pth, doAntiAlias=True)
        hh = 180 * xray; rect(c, -70, -90, 140, hh, RED, 0.25 * a)
        rect(c, -70, -90 + hh - 3, 140, 6, RED, a)
        if xray > 0.5:
            icon(c, "skull", 0, 30, 70, RED, a * (xray - 0.5) * 2)
            draw_text(c, inner, 0, 80, "techmono", 22, RED, a * (xray - 0.5) * 2, align="center")
        c.restore()
    c.restore()
    draw_text(c, name, x, y + 90 * s + 40, "techmono", 30, col, a, align="center")

# ---------------------------------------------------------------- escenas
def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t, alert=prog(t, info.w("Todo falso"), info.w("Todo falso") + 0.4))
    # buscador genérico (no imita ninguna marca)
    p = ease_out(prog(t, 0.1, 0.5))
    rect(c, 260, 120, 1400, 90, "#1A2029", p, r=45); icon(c, "magnify", 320, 165, 44, DIM, p)
    q = typewriter("gta 6 descargar pc gratis", t - 0.4, 20)
    draw_text(c, q + ("|" if int(t * 3) % 2 == 0 else ""), 370, 180, "inter", 40, WHITE, p)
    res = [("DESCARGAR GTA 6 PC — VERSIÓN COMPLETA", "★★★★★ 4,9 · 2.381.004 descargas"),
           ("GTA 6 APK ANDROID + OBB (FUNCIONA 100%)", "★★★★★ 4,8 · “¡me funcionó!”"),
           ("ACCESO ANTICIPADO GTA VI — BETA EXCLUSIVA", "★★★★☆ 4,7 · plazas limitadas")]
    for i, (a, b) in enumerate(res):
        st = 1.6 + i * 0.5; pp = ease_out(prog(t, st, st + 0.4)); y = 280 + i * 220
        if pp <= 0: continue
        rect(c, 260, y, 1400, 180, "#141922", pp, r=16)
        draw_text(c, a, 300, y + 70, "interb", 42, "#8AB4FF", pp)
        draw_text(c, b, 300, y + 125, "intermd", 30, "#F5C04A", pp)
        bx = 1370; rect(c, bx, y + 50, 250, 80, GREEN, pp, r=40); draw_text(c, "DESCARGAR", bx + 125, y + 102, "interxb", 30, "#000000", pp, align="center")
        ts = info.w("Todo falso") + i * 0.35; sp = ease_out_back(prog(t, ts, ts + 0.3))
        if sp > 0:
            c.save(); c.translate(bx + 125, y + 90); c.rotate(-12); c.scale(sp, sp)
            rect(c, -170, -50, 340, 100, "#1A0508", 0.92, r=8); rect(c, -170, -50, 340, 100, RED, 1, r=8, stroke=6)
            draw_text(c, "FALSO", 0, 24, "techmono", 64, RED, 1, align="center", tracking=6)
            c.restore()
    if t > info.w("esta semana"):
        pp = ease_out(prog(t, info.w("esta semana"), info.w("esta semana") + 0.4))
        rect(c, 0, 960, W, 120, "#000000", 0.8 * pp)
        draw_text(c, "13 NOV 2026 · ALERTAS DE ESET Y CYNET", W / 2, 1035, "techmono", 46, RED, pp, align="center", tracking=4)

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_intro(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "EXPEDIENTE: LA DESCARGA FALSA", "0613")
    p = ease_out(prog(t, 0.2, 0.8))
    for i, (lab, col, cue) in enumerate((("NARRADOR", CYAN, 0.0), ("ANALISTA", AMB, info.w("Hola", default=info.w("analista"))))):
        pp = ease_out_back(prog(t, cue, cue + 0.5)); x = 520 + i * 880; y = 560
        if pp <= 0: continue
        c.save(); c.translate(x, y); c.scale(pp, pp)
        circle(c, 0, 0, 170, PANEL); circle(c, 0, 0, 170, col, 1, stroke=4)
        for k in range(24):
            ang = k / 24 * math.tau; h = 30 + 40 * abs(math.sin(t * 6 + k))
            line(c, math.cos(ang) * 120, math.sin(ang) * 120, math.cos(ang) * (120 + h * 0.6), math.sin(ang) * (120 + h * 0.6), col, 0.8, 5)
        icon(c, "user", 0, 0, 120, col)
        c.restore()
        draw_text(c, lab, x, y + 240, "techmono", 44, col, pp, align="center", tracking=6)
        draw_text(c, "VOZ SINTÉTICA", x, y + 285, "techmono", 22, DIM, pp, align="center", tracking=4)

def sc_truth(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "01 · LA VERDAD CORTA", "0613")
    rows = [("PLAYSTATION 5", True, "PlayStation 5"), ("XBOX SERIES X|S", True, "Xbox"), ("PC (WINDOWS)", False, "PC anunciada"),
            ("ANDROID", False, "Android"), ("IPHONE", False, "iPhone")]
    draw_text(c, "PLATAFORMA", 300, 250, "techmono", 28, DIM, 1, tracking=4); draw_text(c, "¿EXISTE GTA VI?", 1300, 250, "techmono", 28, DIM, 1, tracking=4)
    for i, (lab, ok, cue) in enumerate(rows):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.35)); y = 290 + i * 118
        if p <= 0: continue
        rect(c, 280, y, 1360, 96, PANEL, p, r=10)
        draw_text(c, "> " + lab, 310, y + 63, "techmono", 46, WHITE, p)
        col = GREEN if ok else RED
        draw_text(c, "SÍ" if ok else "NO", 1360, y + 66, "techmono", 56, col, p, tracking=4)
        icon(c, "check" if ok else "cross", 1540, y + 48, 50, col, p)
    st = info.w("mintiendo")
    pp = ease_out(prog(t, st, st + 0.4))
    if pp > 0:
        rect(c, 280, 900, 1360, 110, RED, 0.15 * pp, r=10); rect(c, 280, 900, 1360, 110, RED, pp, r=10, stroke=3)
        draw_text(c, "Si dice “GTA 6 para PC/Android”, miente desde el nombre", W / 2, 970, "techmono", 42, WHITE, pp, align="center")
    cert_tag(c, W - 60, 170, "OFICIAL", 1, 24, align="right", t=prog(t, info.w("PlayStation 5"), info.w("PlayStation 5") + 0.4))

def sc_why(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "01B · POR QUÉ FUNCIONA", "0613")
    items = [("MILLONES SIN PS5 NI XBOX SERIES", "console", "sin PS5"), ("UNA ESPERA DE AÑOS", "clock", "espera"), ("LA CULTURA DEL “TRUCO”", "magnify", "trucos")]
    for i, (lab, ic, cue) in enumerate(items):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.4)); y = 250 + i * 170
        if p <= 0: continue
        c.save(); c.translate((1 - p) * 80, 0)
        rect(c, 300, y, 1320, 130, PANEL, p, r=14); rect(c, 300, y, 8, 130, AMB, p)
        icon(c, ic, 400, y + 65, 70, AMB, p); draw_text(c, lab, 480, y + 82, "techmono", 46, WHITE, p)
        c.restore()
    st = info.w("no vende"); p = ease_out_back(prog(t, st, st + 0.5))
    if p > 0:
        c.save(); c.translate(W / 2, 860); c.scale(p, p)
        rect(c, -700, -90, 1400, 180, "#000000", 0.85, r=20); rect(c, -700, -90, 1400, 180, RED, 1, r=20, stroke=4)
        draw_text(c, "NO VENDE UN JUEGO:", 0, -12, "techmono", 52, WHITE, 1, align="center")
        draw_text(c, "VENDE NO QUEDARTE AFUERA", 0, 58, "techmono", 52, RED, 1, align="center")
        c.restore()
    cert_tag(c, W - 60, 170, "DEDUCCIÓN", 1, 24, align="right", t=prog(t, 0.3, 0.7))

def sc_hook_parts(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "02 · ANATOMÍA DEL ANZUELO", "0613")
    parts = [("PÁGINA QUE IMITA\nUNA TIENDA", "monitor", info.w("página")), ("BOTÓN DE\nDESCARGA", "download", info.w("botón")), ("UNA EXCUSA PARA\nBAJAR LA GUARDIA", "shield", info.w("excusa"))]
    for i, (lab, ic, st) in enumerate(parts):
        p = ease_out_back(prog(t, st, st + 0.4)); x = 330 + i * 630; y = 330
        if p <= 0: continue
        c.save(); c.translate(x, y); c.scale(p, p)
        rect(c, -230, -130, 460, 260, PANEL, 1, r=14); rect(c, -230, -130, 460, 260, CYAN, 0.8, r=14, stroke=3)
        icon(c, ic, 0, -45, 90, CYAN)
        for k, L in enumerate(lab.split("\n")): draw_text(c, L, 0, 60 + k * 40, "techmono", 32, WHITE, 1, align="center")
        c.restore()
        if i < 2: line(c, x + 240, y, x + 390, y, CYAN, p * 0.6, 3, dash=[12, 10])
    # archivo con rayos X
    st = info.w("ESET"); p = ease_out(prog(t, st - 0.3, st + 0.3))
    if p > 0:
        file_icon(c, 640, 720, 1.2, "gta6_installer.exe", WHITE, p, xray=prog(t, info.w("Vidar") - 0.6, info.w("Vidar") + 0.4), inner="VIDAR")
        draw_text(c, "DETECTADO POR ESET", 640, 1000, "techmono", 26, DIM, p, align="center", tracking=3)
    st2 = info.w("Cynet"); p2 = ease_out(prog(t, st2 - 0.3, st2 + 0.3))
    if p2 > 0:
        file_icon(c, 1280, 720, 1.2, "“GTA 6 EXE”", WHITE, p2, xray=prog(t, info.w("WARDEN") - 0.6, info.w("WARDEN") + 0.4), inner="WARDEN")
        draw_text(c, "DETECTADO POR CYNET", 1280, 1000, "techmono", 26, DIM, p2, align="center", tracking=3)
    if t > st: cert_tag(c, W - 120, 900, "REPORTADO", 1, 26, align="right", t=prog(t, st, st + 0.4))

def dialog(c, x, y, title, btn, p, struck):
    """Ventana de diálogo genérica (no imita ningún sistema operativo concreto)."""
    if p <= 0: return
    c.save(); c.translate(x, y); s = ease_out_back(p); c.scale(s, s)
    rect(c, -300, -150, 600, 300, "#1C222B", 1, r=14); rect(c, -300, -150, 600, 50, "#28303B", 1, r=14); rect(c, -300, -115, 600, 15, "#28303B", 1)
    circle(c, -270, -125, 8, RED); circle(c, -245, -125, 8, AMB); circle(c, -220, -125, 8, GREEN)
    icon(c, "warn", -200, 10, 80, AMB)
    draw_par(c, title, -140, -20, "intersb", 30, 400, color=WHITE)
    rect(c, 20, 80, 250, 52, CYAN, 1, r=8); draw_text(c, btn, 145, 115, "interb", 24, "#000000", 1, align="center")
    if struck > 0:
        k = ease_out(struck); line(c, -280, -130, -280 + 560 * k, -130 + 260 * k, RED, 1, 14); line(c, 280, -130, 280 - 560 * k, -130 + 260 * k, RED, 1, 14)
    c.restore()

def sc_asks(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t, alert=0.5 * prog(t, info.w("alarma") - 0.5, info.w("alarma"))); hud(c, W, t, "03 · LO QUE TE PIDE EL INSTALADOR", "0613")
    d = [("Ejecutar con permisos de administrador", "PERMITIR", info.w("administrador")), ("El sistema bloqueó un archivo sospechoso", "IGNORAR", info.w("ignorar")),
         ("Agregar excepción al antivirus", "AGREGAR", info.w("excepción"))]
    for i, (ti, b, st) in enumerate(d):
        dialog(c, 360 + i * 600, 480 + (i % 2) * 60, ti, b, prog(t, st - 0.2, st + 0.3), prog(t, info.w("En otras palabras"), info.w("En otras palabras") + 0.5))
    st = info.w("alarma"); p = ease_out_back(prog(t, st, st + 0.5))
    if p > 0:
        c.save(); c.translate(W / 2, 880); c.scale(p, p)
        rect(c, -620, -70, 1240, 140, "#000000", 0.85, r=70); rect(c, -620, -70, 1240, 140, RED, 1, r=70, stroke=4)
        draw_text(c, "TE PIDE APAGAR LA ALARMA ANTES DE ENTRAR", 0, 18, "techmono", 50, RED, 1, align="center")
        c.restore()
    if t > info.w("¿Y qué pide"): cert_tag(c, W - 60, 170, "REPORTADO", 1, 24, align="right", t=prog(t, info.w("administrador"), info.w("administrador") + 0.4))

def sc_steals(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "04 · LO QUE SE LLEVA", "0613")
    cx, cy = 500, 580
    circle(c, cx, cy, 150, PANEL); circle(c, cx, cy, 150, RED, 1, stroke=5); icon(c, "skull", cx, cy - 10, 140, RED)
    draw_text(c, "INFOSTEALER", cx, cy + 210, "techmono", 36, RED, 1, align="center", tracking=4)
    items = [("CONTRASEÑAS GUARDADAS", "lock", "contraseñas"), ("COOKIES DE SESIÓN", "user", "cookies"), ("CUENTAS STEAM · ROBLOX", "pad", "Steam"), ("MONEDEROS CRIPTO", "money", "criptomonedas")]
    srv = (1640, 580)
    for i, (lab, ic, cue) in enumerate(items):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.4)); y = 260 + i * 170; x = 1000
        if p <= 0: continue
        rect(c, x - 140, y - 60, 520, 120, PANEL, p, r=12); rect(c, x - 140, y - 60, 520, 120, AMB, p, r=12, stroke=2)
        icon(c, ic, x - 80, y, 56, AMB, p); draw_text(c, lab, x - 30, y + 12, "techmono", 30, WHITE, p)
        line(c, cx + 150, cy, x - 140, y, RED, 0.5 * p, 2, dash=[8, 8])
        # paquetes viajando al servidor remoto
        for k in range(3):
            ph = ((t - st) * 0.6 + k / 3) % 1
            if t > st + 0.5: circle(c, lerp(x + 380, srv[0] - 90, ph), lerp(y, srv[1], ph), 7, RED, 0.9)
    pp = ease_out(prog(t, info.w("contraseñas"), info.w("contraseñas") + 0.4))
    rect(c, srv[0] - 90, srv[1] - 120, 180, 240, PANEL, pp, r=12); rect(c, srv[0] - 90, srv[1] - 120, 180, 240, RED, pp, r=12, stroke=3)
    for k in range(4): rect(c, srv[0] - 70, srv[1] - 95 + k * 55, 140, 36, "#000000", pp, r=6); circle(c, srv[0] + 50, srv[1] - 77 + k * 55, 6, RED if int(t * 4 + k) % 2 else DIM, pp)
    draw_text(c, "SERVIDOR REMOTO", srv[0], srv[1] + 165, "techmono", 26, DIM, pp, align="center", tracking=2)
    st = info.w("Las cookies"); p = ease_out(prog(t, st, st + 0.4)) * (1 - prog(t, info.w("O sea"), info.w("O sea") + 0.3))
    if p > 0:
        rect(c, 0, 900, W, 180, "#000000", 0.88 * p)
        draw_text(c, "COOKIE DE SESIÓN = PASE PARA ENTRAR SIN TU CONTRASEÑA", W / 2, 1000, "techmono", 46, AMB, p, align="center")
    st = info.w("O sea"); p = ease_out_back(prog(t, st, st + 0.4))
    if p > 0:
        rect(c, 0, 900, W, 180, "#000000", 0.92); draw_text(c, "NO PIERDES UN JUEGO: PIERDES TUS CUENTAS", W / 2, 1005, "techmono", 54, RED, p, align="center")

def sc_variants(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "05 · OTRAS VERSIONES DEL MISMO TRUCO", "0613")
    cards = [("ENCUESTAS ANTES\nDEL ENLACE", "chat", "encuestas", "REPORTADO"), ("BETA O ACCESO\nANTICIPADO DE PAGO", "money", "accesos anticipados", "REPORTADO"),
             ("APK QUE PIDE\nPERMISOS RAROS", "phone", "APK", "DEDUCCIÓN")]
    for i, (lab, ic, cue, cert) in enumerate(cards):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.5)); x = 200 + i * 540
        if p <= 0: continue
        c.save(); c.translate(x + 230, 560); c.rotate((1 - p) * 20 * (1 if i % 2 else -1)); c.scale(p, p); c.translate(-(x + 230), -560)
        rect(c, x, 300, 460, 520, PANEL, 1, r=18); rect(c, x, 300, 460, 520, RED, 0.8, r=18, stroke=3)
        icon(c, ic, x + 230, 440, 130, RED)
        for k, L in enumerate(lab.split("\n")): draw_text(c, L, x + 230, 620 + k * 48, "techmono", 38, WHITE, 1, align="center")
        cert_tag(c, x + 230, 730, cert, 1, 22, align="center", t=1)
        c.restore()

def sc_steps(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "06 · SI YA LO EJECUTASTE", "0613")
    steps = [("Desconecta el equipo y analízalo con tu antivirus", "Desconecta"), ("Cambia contraseñas desde OTRO dispositivo limpio (empieza por el correo)", "Cambia"),
             ("Cierra todas las sesiones abiertas", "cierra"), ("Activa la verificación en dos pasos", "verificación"),
             ("¿Escribiste la frase de una billetera cripto? Considérala comprometida", "frase de recuperación")]
    for i, (s, cue) in enumerate(steps):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.4)); y = 240 + i * 150
        if p <= 0: continue
        c.save(); c.translate((1 - p) * -60, 0)
        rect(c, 180, y, 1560, 120, PANEL, p, r=12)
        circle(c, 250, y + 60, 40, GREEN if p >= 1 else AMB, p); draw_text(c, str(i + 1), 250, y + 78, "techmono", 50, "#000000", p, align="center")
        draw_par(c, s, 320, y + 72, "intersb", 38, 1380, color=WHITE, a=p)
        c.restore()
    source_chip(c, 180, 1000, "Recomendaciones de Help Net Security / Security Boulevard (nov. 2026)", ease_out(prog(t, 0.5, 1.0)))

def sc_rules(c, t, info, ctx):
    W, H = ctx.W, ctx.H; lab_bg(c, W, H, t); hud(c, W, t, "07 · REGLA DE LOS 5 SEGUNDOS", "0613")
    rules = [("¿No viene de PlayStation Store, Microsoft Store o una tienda de confianza?", "NO ES GTA 6", "Regla rápida"),
             ("¿Te pide desactivar el antivirus?", "ES MALWARE", "antivirus, es"), ("¿Es gratis?", "EL PRODUCTO ERES TÚ", "gratis")]
    for i, (q, a_, cue) in enumerate(rules):
        st = info.w(cue); y = 250 + i * 240
        if t < st: continue
        typed = typewriter("> " + q, t - st, 45)
        draw_text(c, typed, 160, y + 50, "techmono", 40, WHITE, 1)
        p = ease_out_back(prog(t, st + len(q) / 45 + 0.1, st + len(q) / 45 + 0.5))
        if p > 0:
            c.save(); c.translate(160, y + 90); c.scale(p, p)
            rect(c, 0, 0, text_w(a_, font("techmono", 64), 4) + 60, 96, RED, 1, r=10)
            draw_text(c, a_, 30, 72, "techmono", 64, "#000000", 1, tracking=4)
            c.restore()

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "LA ÚNICA DESCARGA BUENA ES LA OFICIAL", "Guía de horarios y precios en la descripción", CYAN)

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2.5 < gt < ctx.total - 20:
        watermark(c, W, H, 0.5); speaker_badge(c, gt, ctx)
    if gt < 9: ai_notice(c, W, H, clamp((9 - gt)), "Recreación gráfica original · páginas y diálogos genéricos, no capturas reales")

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Escribe “GTA 6 descargar PC” en un buscador y vas a encontrar botones gigantes, contadores de descargas y comentarios felices. "
     "Todo falso. Y esta semana, empresas de ciberseguridad encontraron lo que hay detrás.",
     sc_hook, section="GANCHO", energy=1, sfx=[(0.3, "typing", 0.5), ("w:Todo falso", "stamp", 0.8), ("w:Todo falso", "glitch", 0.5), ("w:esta semana", "alarm", 0.3)])
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=1, trans=("glitch", 0.4))
beat("Esto es Caimán Neón. Hoy no hablamos de Leonida: hablamos de la trampa que la rodea. Y para eso me acompaña nuestra analista.",
     sc_intro, section="INTRODUCCIÓN", energy=1, trans=("glitch", 0.35))
beat("Hola. Vamos a abrir el archivo paso a paso, sin tecnicismos.", None, voice="analista", sfx=[(0.0, "pop", 0.4)])
beat("Primero, el dato que desarma toda la estafa. GTA 6 solo existe en PlayStation 5 y en Xbox Series X y Series S. "
     "No hay versión de PC anunciada. Y no hay versión para Android ni para iPhone. "
     "Cualquier archivo que diga lo contrario está mintiendo desde el nombre.",
     sc_truth, section="1 · LA VERDAD CORTA", energy=2, trans=("glitch", 0.35),
     sfx=[("w:PlayStation 5", "tick", 0.5), ("w:Xbox", "tick", 0.5), ("w:PC anunciada", "buzz", 0.3), ("w:Android", "buzz", 0.3), ("w:iPhone", "buzz", 0.3), ("w:mintiendo", "hit", 0.4)])
beat("¿Y por qué cae tanta gente? Porque el anzuelo se aprovecha de tres cosas reales. "
     "Hay millones de jugadores sin PS5 ni Xbox Series. La espera duró años. Y en internet abundan los trucos para todo. "
     "La estafa no vende un juego: vende la ilusión de no quedarte afuera.",
     sc_why, section="1B · POR QUÉ FUNCIONA", voice="analista", energy=2, trans=("glitch", 0.35),
     sfx=[("w:sin PS5", "pop", 0.4), ("w:espera", "pop", 0.4), ("w:trucos", "pop", 0.4), ("w:no vende", "hit", 0.5)])
beat("El anzuelo tiene tres piezas. Una página que imita a una tienda. Un botón de descarga. Y una excusa para que bajes la guardia. "
     "La empresa ESET detectó un archivo llamado {gta6_installer.exe|ge te a seis, guion bajo, installer, punto e equis e}, que en realidad transporta Vidar: un programa diseñado para robar información. "
     "Y la firma Cynet encontró otra variante, con un ladrón de datos llamado WARDEN.",
     sc_hook_parts, section="2 · ANATOMÍA DEL ANZUELO", voice="analista", energy=2, trans=("glitch", 0.35),
     sfx=[("w:página", "pop", 0.4), ("w:botón", "pop", 0.4), ("w:excusa", "pop", 0.4), ("w:Vidar", "alarm", 0.3), ("w:WARDEN", "alarm", 0.3)])
beat("¿Y qué te pide el instalador?", sc_asks, section="3 · LO QUE PIDE", energy=2, trans=("glitch", 0.35))
beat("Justo lo que un juego legítimo nunca te pediría: ejecutarlo como administrador, ignorar la advertencia de seguridad y agregar una excepción en el antivirus. "
     "En otras palabras: te pide que apagues la alarma antes de entrar.", None, voice="analista",
     sfx=[("w:administrador", "pop", 0.4), ("w:ignorar", "pop", 0.4), ("w:excepción", "pop", 0.4), ("w:En otras palabras", "glitch", 0.4), ("w:alarma", "alarm", 0.4)])
beat("Según los reportes, este tipo de programa busca las contraseñas guardadas en el navegador, las cookies de sesión, cuentas de Steam y de Roblox, y datos de monederos de criptomonedas. "
     "Las cookies son lo más delicado: con ellas, alguien puede entrar a tu cuenta sin saber tu contraseña.",
     sc_steals, section="4 · LO QUE SE LLEVA", voice="analista", energy=2, trans=("glitch", 0.35),
     sfx=[("w:contraseñas", "tick", 0.5), ("w:cookies", "tick", 0.5), ("w:Steam", "tick", 0.5), ("w:criptomonedas", "tick", 0.5)])
beat("O sea que no pierdes un juego: pierdes tus cuentas.", None, sfx=[(0.0, "hit", 0.6)], music_stop=1.5)
beat("No siempre es un ejecutable. También circulan otras versiones del mismo truco.", sc_variants, section="5 · VARIANTES", energy=2, trans=("glitch", 0.35))
beat("Páginas que te piden completar encuestas antes de mostrar el enlace. Falsos accesos anticipados o betas que exigen un pago por adelantado. "
     "Y en Android, archivos APK que piden permisos que ningún juego necesita.", None, voice="analista",
     sfx=[("w:encuestas", "pop", 0.4), ("w:accesos anticipados", "pop", 0.4), ("w:APK", "pop", 0.4)])
beat("Si ya ejecutaste uno de estos archivos, no entres en pánico, pero actúa hoy. "
     "Desconecta el equipo de internet y analízalo con tu antivirus. "
     "Cambia tus contraseñas desde otro dispositivo limpio, empezando por el correo, y cierra todas las sesiones abiertas. "
     "Activa la verificación en dos pasos. "
     "Y si escribiste la frase de recuperación de una billetera de criptomonedas, considérala comprometida: mueve los fondos a una billetera nueva desde un dispositivo limpio.",
     sc_steps, section="6 · SI YA LO EJECUTASTE", voice="analista", energy=2, trans=("glitch", 0.35),
     sfx=[("w:Desconecta", "tick", 0.5), ("w:Cambia", "tick", 0.5), ("w:cierra", "tick", 0.5), ("w:verificación", "tick", 0.5), ("w:frase de recuperación", "tick", 0.5)])
beat("Regla rápida para la próxima vez. Si no viene de PlayStation Store, de Microsoft Store o de una tienda de confianza, no es GTA 6. "
     "Si te pide desactivar el antivirus, es malware. "
     "Y si es gratis, el producto eres tú.",
     sc_rules, section="7 · REGLA DE LOS 5 SEGUNDOS", energy=3, trans=("glitch", 0.35), sfx=[("w:Regla rápida", "typing", 0.4), ("w:antivirus, es", "stamp", 0.6), ("w:gratis", "stamp", 0.7)])
beat("Comparte este video con ese primo que siempre encuentra “versiones especiales”. Y si quieres jugar GTA 6 de verdad, en la descripción tienes nuestra guía con la hora de tu país. "
     "Suscríbete a Caimán Neón: aquí, la única descarga que recomendamos es la oficial.",
     sc_end, section="LLAMADA A LA ACCIÓN", energy=2, hold=4.0, min=20, trans=("fade", 0.6))

VIDEO = dict(id="v03", folder="VIDEO_03", file="GTA6_PC_Android_estafa_malware_investigacion",
             title="GTA 6 para PC y Android: la verdad (y la estafa que está robando cuentas)",
             format="Largo (16:9)", music="tension", music_seed=31, voice="host", beats=B, overlay=overlay, music_gain=0.5)

def thumbnail(c):
    W, H = 1280, 720
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, ["#16070A", BG]))
    grid(c, W, H, 40, RED, 0.06)
    c.drawCircle(360, 380, 420, rad_grad(360, 380, 420, [hexc(RED, 0.35), hexc(RED, 0)]))
    # botón de descarga con anzuelo
    rect(c, 70, 230, 600, 240, GREEN, 1, r=120)
    icon(c, "download", 175, 350, 120, "#000000")
    draw_text(c, "GTA 6", 430, 335, "interblk", 96, "#000000", 1, align="center")
    draw_text(c, "PC GRATIS", 430, 425, "interblk", 70, "#000000", 1, align="center")
    pth = skia.Path(); pth.moveTo(700, 40); pth.lineTo(700, 420); pth.quadTo(700, 520, 630, 520); pth.quadTo(570, 520, 570, 465)
    c.drawPath(pth, paint("#D8DEE6", 1, stroke=18)); draw_poly(c, [(555, 450), (585, 450), (570, 420)], "#D8DEE6")
    draw_text(c, "NO LO", 1010, 250, "anton", 150, WHITE, 1, align="center")
    draw_text(c, "DESCARGUES", 1010, 400, "anton", 104, RED, 1, align="center", glow=(RED, 14))
    rect(c, 780, 450, 470, 90, "#000000", 0.7, r=12); icon(c, "skull", 835, 495, 60, RED)
    draw_text(c, "ROBA CUENTAS", 1050, 515, "techmono", 56, WHITE, 1, align="center")
    draw_text(c, "ALERTA ESET · CYNET · NOV 2026", 70, 660, "techmono", 36, WHITE, 0.85, tracking=2)
