"""VIDEO 01 — Kit de lanzamiento: 7 comprobaciones antes de medianoche.
Lenguaje visual: tablero de salidas de aeropuerto (paletas mecánicas), tarjeta de embarque, ámbar sobre negro.
"""
import math, numpy as np, skia
from gfx import *
from components import *
from brand import PAL

AMBER = "#FFB21E"; BOARD = "#0B0B0E"; FLAP = "#18191E"; RED = "#FF4A3D"; GREEN = PAL["caiman"]; WHITE = "#F5F2EA"
CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:·-/ "

# ---------------------------------------------------------------- tablero de paletas
def flap_text(c, txt, x, y, t, t0, cw=44, ch=66, col=AMBER, per=0.045, spin=0.35, seed=0, gap=6, bg=FLAP, size=None):
    """Texto en paletas: cada celda gira por caracteres aleatorios y se asienta escalonadamente."""
    rng = np.random.default_rng(seed); size = size or ch * 0.72
    for i, chr_ in enumerate(txt):
        cx = x + i * (cw + gap)
        rect(c, cx, y, cw, ch, bg, 1, r=5)
        settle = t0 + i * per + spin
        if t < t0 + i * per: shown = " "
        elif t < settle:
            k = int((t - t0) * 40 + i * 7) % len(CHARS); shown = CHARS[(k + rng.integers(0, 40)) % len(CHARS)]
        else: shown = chr_
        # media paleta superior en movimiento
        flipping = t0 + i * per <= t < settle
        draw_text(c, shown, cx + cw / 2, y + ch * 0.5 + size * 0.36, "monob", size, col if not flipping else WHITE, 1.0 if not flipping else 0.7, align="center")
        rect(c, cx, y + ch / 2 - 1.5, cw, 3, "#000000", 0.85)
        if flipping:
            ph = ((t - t0) * 40) % 1; rect(c, cx, y, cw, ch / 2 * (1 - ph), "#26272E", 0.55, r=4)
        rect(c, cx, y, cw, ch / 2, "#ffffff", 0.035, r=4)

def board_bg(c, W, H, t):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, ["#111216", "#08080A"]))
    for i in range(0, W, 6): rect(c, i, 0, 1, H, "#ffffff", 0.012)  # textura de panel cepillado (estática)
    c.drawCircle(W * 0.5, -200, 900, rad_grad(W * 0.5, -200, 900, [hexc(AMBER, 0.10), hexc(AMBER, 0)]))

def header(c, W, t, txt, sub=None, a=1.0):
    rect(c, 0, 0, W, 120, "#000000", 0.6 * a)
    icon(c, "clock", 80, 60, 56, AMBER, a)
    draw_text(c, txt, 130, 78, "barlowblk", 54, WHITE, a, tracking=3)
    if sub: draw_text(c, sub, W - 60, 76, "monob", 30, AMBER, a, align="right", tracking=3)
    rect(c, 0, 120, W, 3, AMBER, 0.8 * a)

def check_header(c, W, t, n, title):
    rect(c, 0, 0, W, 150, "#000000", 0.55)
    draw_text(c, f"COMPROBACIÓN {n:02d}/07", 80, 62, "monob", 30, AMBER, ease_out(prog(t, 0, 0.4)), tracking=4)
    flap_text(c, title, 80, 76, t, 0.05, cw=40, ch=58, per=0.03, spin=0.3, seed=n)
    for i in range(7):  # progreso
        x = W - 80 - (6 - i) * 46; on = i < n
        circle(c, x, 75, 15, GREEN if on else "#2A2B31", 1)
        if i == n - 1: circle(c, x, 75, 22 + 6 * pulse(t, 1.2), GREEN, 0.3, stroke=3)

# ---------------------------------------------------------------- escenas
def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t)
    header(c, W, t, "SALIDAS · DEPARTURES", "JUE 19 NOV")
    cols = [("VUELO", 80), ("DESTINO", 420), ("HORA", 1110), ("ESTADO", 1420)]
    for lab, x in cols: draw_text(c, lab, x, 205, "monob", 28, "#8C8C94", 1, tracking=4)
    rows = [("GTA-VI", "LEONIDA", "00:00", "A TIEMPO"), ("VC-305", "VICE CITY", "00:00", "A TIEMPO"),
            ("LK-019", "LEONIDA KEYS", "00:00", "A TIEMPO"), ("PG-850", "PORT GELLHORN", "00:00", "A TIEMPO"),
            ("AM-863", "AMBROSIA", "00:00", "A TIEMPO")]
    s1 = info.w("puerta")
    for r, (v, d, h, e) in enumerate(rows):
        y = 245 + r * 112; t0 = 0.15 + r * 0.22
        flap_text(c, v, 80, y, t, t0, seed=r)
        flap_text(c, d, 420, y, t, t0 + 0.1, seed=r + 10)
        flap_text(c, h, 1110, y, t, t0 + 0.2, seed=r + 20)
        if r in (2, 4) and t > s1 - 0.6:
            flap_text(c, "CERRADA", 1420, y, t, s1 - 0.6 + r * 0.05, col=RED, seed=r + 40)
        else:
            flap_text(c, e, 1420, y, t, t0 + 0.3, col=GREEN, seed=r + 30)
    # tres causas
    s2 = info.w("Por la hora")
    labels = [("LA HORA", "clock"), ("EL ESPACIO", "disk"), ("UNA DESCARGA FALSA", "warn")]
    for i, (lab, ic) in enumerate(labels):
        st = [s2, info.w("Por el espacio"), info.w("descarga")][i]
        p = ease_out_back(prog(t, st, st + 0.35))
        if p <= 0: continue
        x = 400 + i * 560; y = 880
        c.save(); c.translate(x, y); c.scale(p, p)
        rect(c, -230, -70, 460, 140, "#000000", 0.85, r=14); rect(c, -230, -70, 460, 140, RED if i == 2 else AMBER, 1, r=14, stroke=3)
        icon(c, ic, -170, 0, 64, RED if i == 2 else AMBER)
        draw_text(c, lab, -120, 14, "barlowblk", 40 if i < 2 else 34, WHITE)
        c.restore()
    vignette(c, W, H, 0.5)

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_intro(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t)
    # tarjeta de embarque
    p = ease_out(prog(t, 0.1, 0.8)); y = 140 + (1 - p) * 80
    c.save(); c.translate(0, 0)
    rect(c, 260, y, 1400, 470, "#F3EDE0", p, r=26)
    rect(c, 1210, y, 4, 470, "#000000", 0.0)
    for k in range(18): circle(c, 1215, y + 20 + k * 25.5, 5, "#111216", p)
    draw_text(c, "TARJETA DE EMBARQUE", 320, y + 80, "barlowblk", 52, "#16161A", p, tracking=3)
    draw_text(c, "PASAJERO", 320, y + 150, "monob", 22, "#6A6A70", p, tracking=3)
    draw_text(c, "TÚ", 320, y + 200, "barlowblk", 54, "#16161A", p)
    draw_text(c, "DESTINO", 640, y + 150, "monob", 22, "#6A6A70", p, tracking=3)
    draw_text(c, "LEONIDA", 640, y + 200, "barlowblk", 54, "#16161A", p)
    draw_text(c, "SALIDA", 960, y + 150, "monob", 22, "#6A6A70", p, tracking=3)
    draw_text(c, "00:00 LOCAL", 960, y + 200, "barlowblk", 44, "#16161A", p)
    draw_text(c, "REQUISITOS", 320, y + 280, "monob", 22, "#6A6A70", p, tracking=3)
    draw_text(c, "7 COMPROBACIONES ANTES DE ABORDAR", 320, y + 330, "barlowblk", 50, "#C2410C", p)
    # código de barras original
    rng = np.random.default_rng(4); xx = 320
    while xx < 1150:
        w = rng.integers(2, 9); rect(c, xx, y + 370, w, 70, "#16161A", p); xx += w + rng.integers(3, 8)
    draw_text(c, "SA", 1430, y + 260, "anton", 160, "#16161A", p * 0.9, align="center")
    draw_text(c, "PUERTA", 1430, y + 330, "monob", 22, "#6A6A70", p, align="center", tracking=3)
    c.restore()
    # semáforo de certeza sincronizado con la frase
    s1 = info.w("verde")
    for i, k in enumerate(("OFICIAL", "DEDUCCIÓN", "RUMOR")):
        st = [info.w("verde"), info.w("amarillo"), info.w("en rojo")][i]
        cert_tag(c, 470 + i * 360, 720, k, 1, 34, t=prog(t, st, st + 0.4))
    draw_text(c, "verde = confirmado por Rockstar/Take-Two o por la tienda", W / 2, 840, "intermd", 30, WHITE, 0.75 * prog(t, s1 + 3.5, s1 + 4), align="center")
    vignette(c, W, H, 0.45)

def sc_platform(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 1, "PLATAFORMA")
    cards = [("PS5", "console", True, info.w("PlayStation 5")), ("XBOX SERIES X|S", "console", True, info.w("Xbox Series")),
             ("PS4 / XBOX ONE", "console", False, info.w("PS4")), ("PC", "monitor", False, info.w("PC,")),
             ("MÓVIL", "phone", False, info.w("móvil"))]
    for i, (lab, ic, ok, st) in enumerate(cards):
        x = 120 + i * 345; y = 290; p = ease_out_back(prog(t, st, st + 0.45))
        if p <= 0: continue
        c.save(); c.translate(x + 150, y + 210); c.scale(1, p); c.translate(-(x + 150), -(y + 210))
        col = GREEN if ok else RED
        rect(c, x, y, 300, 420, "#121318", 1, r=20); rect(c, x, y, 300, 420, col, 0.9, r=20, stroke=3)
        icon(c, ic, x + 150, y + 140, 130, WHITE, 0.9)
        draw_par(c, lab, x + 150, y + 290, "barlowblk", 40, 270, align="center", color=WHITE)
        circle(c, x + 150, y + 380, 30, col, 1); icon(c, "check" if ok else "cross", x + 150, y + 380, 34, "#000000")
        c.restore()
    if t > info.w("Take-Two"):
        source_chip(c, 120, 760, "Take-Two (Strauss Zelnick): sin fecha para PC; prioridad consolas", ease_out(prog(t, info.w("Take-Two"), info.w("Take-Two") + 0.4)))
    st = info.w("trampa") - 0.8
    if t > st:
        p = ease_out(prog(t, st + 0.8, st + 1.2))
        rect(c, 120, 850, 1680, 120, RED, 0.18 * p, r=14); rect(c, 120, 850, 1680, 120, RED, p, r=14, stroke=3)
        icon(c, "warn", 200, 910, 70, RED, p)
        draw_text(c, "“GTA 6 APK / PC GRATIS” = TRAMPA. Hay malware robando cuentas.", 270, 925, "barlowblk", 46, WHITE, p)
    cert_tag(c, W - 80, 180, "OFICIAL", 1, 26, align="right", t=prog(t, info.w("PlayStation 5"), info.w("PlayStation 5") + 0.4))

def storage_bar(c, x, y, w, label, usable, game, t, st, col):
    p = ease_out(prog(t, st, st + 0.6)); g = ease_out(prog(t, st + 0.6, st + 1.4))
    draw_text(c, label, x, y - 18, "barlowblk", 40, WHITE, p)
    draw_text(c, f"{usable} GB libres aprox.", x + w, y - 18, "monob", 26, "#9A9AA2", p, align="right")
    rect(c, x, y, w, 64, "#1D1E24", p, r=12)
    gw = w * min(1, game / usable) * g
    rect(c, x, y, gw, 64, col, 0.95 * p, r=12)
    if g > 0.3:
        pct = int(round(100 * game / usable * g))
        draw_text(c, f"GTA VI ≈ {pct}%", x + 18, y + 44, "barlowblk", 36, "#000000", 1)

def sc_storage(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 2, "ESPACIO 210 GB")
    p = ease_out_back(prog(t, info.w("210"), info.w("210") + 0.5))
    c.save(); c.translate(1500, 330); c.scale(p, p)
    circle(c, 0, 0, 130, AMBER, 0.12); circle(c, 0, 0, 130, AMBER, 1, stroke=6)
    draw_text(c, "≈210", 0, 20, "barlowblk", 92, WHITE, 1, align="center"); draw_text(c, "GB", 0, 70, "monob", 32, AMBER, 1, align="center")
    c.restore()
    if t > info.w("209"): draw_text(c, "Xbox Store: 209,86 GB", 1500, 520, "monob", 28, WHITE, ease_out(prog(t, info.w("209"), info.w("209") + 0.4)), align="center")
    s = info.w("PS5")
    storage_bar(c, 120, 330, 1150, "PS5 (825 GB)", 667, 210, t, s, AMBER)
    storage_bar(c, 120, 500, 1150, "XBOX SERIES S (512 GB)", 364, 210, t, info.w("Series S"), RED)
    storage_bar(c, 120, 670, 1150, "XBOX SERIES X (1 TB)", 802, 210, t, info.w("Series X"), GREEN)
    source_chip(c, 120, 800, "Espacio útil: GameSpot / Microsoft. Tamaño: fichas de tienda (nov. 2026)", ease_out(prog(t, s, s + 0.5)))
    st = info.w("Haz espacio")
    if t > st:
        pp = ease_out_back(prog(t, st, st + 0.4))
        c.save(); c.translate(W / 2, 950); c.scale(pp, pp)
        rect(c, -560, -55, 1120, 110, AMBER, 1, r=55)
        draw_text(c, "HAZ ESPACIO HOY, NO A LAS 23:59", 0, 20, "barlowblk", 54, "#000000", 1, align="center")
        c.restore()
    cert_tag(c, W - 80, 180, "OFICIAL", 1, 26, align="right", t=prog(t, info.w("210"), info.w("210") + 0.4))

def sc_preload(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 3, "PRECARGA")
    cx, cy = 560, 560; p = ease_io(prog(t, 0.2, 3.5))
    circle(c, cx, cy, 220, "#1D1E24", 1, stroke=34)
    arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(cx - 220, cy - 220, 440, 440), -90, 360 * p)
    c.drawPath(arc, paint(GREEN, 1, stroke=34, cap="round")); c.drawPath(arc, paint(GREEN, 0.4, stroke=50, blur=12))
    draw_text(c, f"{int(p * 100)}%", cx, cy + 40, "barlowblk", 140, WHITE, 1, align="center")
    icon(c, "download", cx, cy - 120, 70, GREEN)
    s1 = info.w("actualización")
    pp = ease_out_back(prog(t, s1, s1 + 0.4))
    if pp > 0:
        c.save(); c.translate(1300, 420); c.scale(pp, pp)
        rect(c, -330, -90, 660, 180, "#121318", 1, r=18); rect(c, -330, -90, 660, 180, "#27D7F2", 1, r=18, stroke=3)
        draw_text(c, "ACTUALIZACIÓN 1.002", 0, -20, "barlowblk", 52, WHITE, 1, align="center")
        draw_text(c, "≈1 GB en PS5 · ≈2,2 GB en Xbox", 0, 45, "monob", 28, "#27D7F2", 1, align="center")
        c.restore()
        cert_tag(c, 1300, 540, "REPORTADO", 1, 24, align="center", t=prog(t, s1 + 0.3, s1 + 0.7))
    s2 = info.w("modo reposo")
    pp = ease_out(prog(t, s2, s2 + 0.5))
    if pp > 0:
        rect(c, 990, 650, 620, 230, "#121318", pp, r=18)
        circle(c, 1080, 765, 46, AMBER, pp); circle(c, 1100, 750, 40, "#121318", pp)  # luna
        draw_text(c, "MODO REPOSO", 1160, 745, "barlowblk", 48, WHITE, pp)
        draw_text(c, "+ descargas activadas", 1160, 795, "monob", 28, AMBER, pp)
    source_chip(c, 120, 900, "Precarga desde el 10 nov.: PlayStation Store / Microsoft Store, vía prensa", ease_out(prog(t, 0.5, 1)))

ZONES = [("ESPAÑA", 1, "00:00", "00:00"), ("ARGENTINA/CHILE", -3, "00:00", "04:00"), ("VENEZUELA", -4, "00:00", "05:00"),
         ("COLOMBIA/PERÚ/ECUADOR", -5, "00:00", "06:00"), ("MÉXICO (CENTRO)", -6, "00:00", "07:00")]

def sc_time(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 4, "HORA LOCAL 00:00")
    draw_text(c, "TU PAÍS", 120, 250, "monob", 26, "#8C8C94", 1, tracking=4)
    draw_text(c, "TU HORA", 1040, 250, "monob", 26, "#8C8C94", 1, tracking=4)
    draw_text(c, "HORA EN ESPAÑA", 1400, 250, "monob", 26, "#8C8C94", 1, tracking=4)
    cues = [info.w("España"), info.w("Argentina"), info.w("Colombia") - 1.2, info.w("Colombia"), info.w("México")]
    for i, (name, off, loc, es) in enumerate(ZONES):
        st = cues[i]
        y = 280 + i * 120
        flap_text(c, name, 120, y, t, st, cw=34, ch=58, per=0.02, spin=0.25, seed=i)
        flap_text(c, loc, 1040, y, t, st + 0.3, cw=40, ch=58, col=GREEN, seed=i + 5)
        flap_text(c, es, 1400, y, t, st + 0.5, cw=40, ch=58, col=AMBER, seed=i + 9)
    s_us = info.w("Estados Unidos")
    s_last = info.w("tabla")
    pp = ease_out(prog(t, s_us, s_us + 0.5)) * (1 - prog(t, s_last - 0.3, s_last))
    if pp > 0:
        rect(c, 120, 900, 1680, 110, "#27D7F2", 0.15 * pp, r=14)
        draw_text(c, "EE. UU.: abre a las 00:00 de la costa este → 21:00 del miércoles en la costa oeste", 160, 970, "barlowblk", 42, WHITE, pp)
        cert_tag(c, W - 140, 930, "REPORTADO", pp, 22, align="right", t=pp)
    if t > s_last:
        pq = ease_out(prog(t, s_last, s_last + 0.4)); rect(c, 0, 880, W, 200, "#000000", 0.85 * pq)
        icon(c, "check", 170, 960, 70, GREEN, pq)
        draw_text(c, "La ficha de TU tienda manda sobre cualquier tabla de internet", 240, 978, "barlowblk", 50, WHITE, pq)
    cert_tag(c, W - 80, 180, "OFICIAL", 1, 26, align="right", t=prog(t, info.w("Rockstar"), info.w("Rockstar") + 0.4))

def price_tag(c, x, y, top, big, sub, col, p, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot * (1 - p)); s = ease_out_back(p); c.scale(s, s)
    pth = poly([(-240, -150), (170, -150), (250, 0), (170, 150), (-240, 150)]); c.drawPath(pth, paint("#121318", 1))
    c.drawPath(pth, paint(col, 1, stroke=4)); circle(c, 205, 0, 13, col, 1)
    draw_text(c, top, -205, -80, "monob", 26, col, 1, tracking=3)
    draw_text(c, big, -205, 30, "barlowblk", 88, WHITE, 1)
    draw_text(c, sub, -205, 100, "monob", 24, "#A9A9B0", 1)
    c.restore()

def sc_price(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 5, "PRECIO")
    s0 = info.w("79,99") - 0.3; s1 = info.w("1.499") - 0.3; s2 = info.w("PlayStation Store"); s4 = info.w("consejo")
    price_tag(c, 400, 380, "ESTÁNDAR", "US$79,99", "PS5 · Xbox Series", GREEN, prog(t, s0 + 0.3, s0 + 0.9), 0.3)
    price_tag(c, 930, 380, "ULTIMATE", "US$99,99", "PS5 · Xbox Series", GREEN, prog(t, info.w("99,99"), info.w("99,99") + 0.6), -0.3)
    price_tag(c, 1530, 380, "MÉXICO · XBOX", "$1.499", "MXN estándar, imp. incl.", "#27D7F2", prog(t, s1 + 0.3, s1 + 0.9), 0.2)
    price_tag(c, 1530, 715, "COLOMBIA · XBOX", "$339.900", "COP estándar", "#27D7F2", prog(t, info.w("339.900") - 0.3, info.w("339.900") + 0.3), -0.2)
    if t > s1: cert_tag(c, 1530, 200, "REPORTADO", 1, 22, align="center", t=prog(t, s1, s1 + 0.4))
    pp = ease_out(prog(t, s2, s2 + 0.5))
    if pp > 0:
        rect(c, 160, 600, 1000, 230, "#121318", pp, r=18); rect(c, 160, 600, 8, 230, AMBER, pp)
        draw_text(c, "PLAYSTATION STORE", 200, 660, "barlowblk", 44, AMBER, pp)
        draw_par(c, "Según el país: moneda local o dólares. Revisa el total con impuestos.", 200, 720, "intersb", 34, 940, color=WHITE, a=pp)
    pq = ease_out(prog(t, s4, s4 + 0.5))
    if pq > 0:
        rect(c, 0, 900, W, 180, "#000000", 0.85 * pq); icon(c, "warn", 170, 975, 70, RED, pq)
        draw_text(c, "¿Mucho más barato fuera de la tienda oficial? Desconfía.", 240, 993, "barlowblk", 52, WHITE, pq)
    source_chip(c, 120, 170, "Hollywood Reporter (precio USD) · Bloomberg Línea / ADN40 (precios locales)", ease_out(prog(t, s0, s0 + 0.5)))

def sc_language(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 6, "IDIOMA")
    # onda de voz en inglés
    s0 = info.w("doblaje") - 0.5; p = ease_out(prog(t, s0, s0 + 0.6))
    rect(c, 120, 260, 820, 300, "#121318", p, r=20)
    draw_text(c, "VOCES", 160, 320, "monob", 26, "#8C8C94", p, tracking=4)
    draw_text(c, "INGLÉS", 160, 400, "barlowblk", 90, WHITE, p)
    for i in range(46):
        hh = (math.sin(i * 0.7 + t * 6) * 0.5 + 0.5) * (math.sin(i * 0.23 + t * 2) * 0.5 + 0.6) * 90 * p
        rect(c, 160 + i * 16, 500 - hh / 2, 8, hh + 4, AMBER, 0.9, r=4)
    draw_text(c, "SIN DOBLAJE", 900, 320, "barlowblk", 40, RED, p, align="right")
    for i, (lab, sub) in enumerate((("ESPAÑOL (MÉXICO)", "pensado para Latinoamérica"), ("ESPAÑOL (ESPAÑA)", "variante peninsular"))):
        cue = info.w("español de México") if i == 0 else info.w("español de España")
        pp = ease_out_back(prog(t, cue, cue + 0.4))
        if pp <= 0: continue
        y = 260 + i * 160
        c.save(); c.translate(1000 + 410, y + 65); c.scale(pp, pp); c.translate(-(1000 + 410), -(y + 65))
        rect(c, 1000, y, 820, 130, "#121318", 1, r=18); rect(c, 1000, y, 820, 130, GREEN, 1, r=18, stroke=3)
        icon(c, "chat", 1070, y + 65, 60, GREEN); draw_text(c, lab, 1130, y + 62, "barlowblk", 50, WHITE)
        draw_text(c, "TEXTOS Y SUBTÍTULOS · " + sub, 1130, y + 104, "monob", 22, GREEN)
        c.restore()
    s2 = info.w("Así que")
    pq = ease_out(prog(t, s2, s2 + 0.5))
    if pq > 0:
        # sofá + bocadillo humorístico (ilustración original)
        rect(c, 300, 760, 700, 150, "#3A2A1E", pq, r=40); rect(c, 260, 720, 120, 220, "#3A2A1E", pq, r=40); rect(c, 920, 720, 120, 220, "#3A2A1E", pq, r=40)
        circle(c, 520, 700, 60, AMBER, pq); circle(c, 780, 700, 60, "#27D7F2", pq)
        rect(c, 1100, 640, 700, 200, WHITE, pq, r=26); draw_poly(c, [(1100, 760), (1050, 800), (1130, 790)], WHITE, pq)
        draw_par(c, "“Narrador oficial de la sala”: desbloqueado", 1140, 720, "barlowblk", 50, 640, color="#16161A", a=pq)
    cert_tag(c, W - 80, 180, "OFICIAL", 1, 26, align="right", t=prog(t, s0, s0 + 0.4))
    source_chip(c, 120, 980, "Vandal / Microsoft Store: voces en inglés; textos en 13 idiomas", ease_out(prog(t, s0, s0 + 0.5)))

def sc_online(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); check_header(c, W, t, 7, "MODO ONLINE")
    s0, s1, s2 = info.w("experiencia"), info.w("GTA Online"), info.w("¿Llegará")
    p = ease_out_back(prog(t, s0, s0 + 0.5))
    if p > 0:
        c.save(); c.translate(480, 520); c.scale(p, p)
        circle(c, 0, 0, 230, "#121318"); circle(c, 0, 0, 230, GREEN, 1, stroke=5)
        icon(c, "user", 0, -40, 170, WHITE); draw_text(c, "1 JUGADOR", 0, 140, "barlowblk", 64, GREEN, 1, align="center")
        c.restore()
        draw_text(c, "“Una experiencia para un jugador”", 480, 840, "dmserifi", 44, WHITE, p, align="center")
        cert_tag(c, 480, 880, "OFICIAL", p, 24, align="center", t=p)
    p = ease_out(prog(t, s1, s1 + 0.5))
    if p > 0:
        rect(c, 980, 280, 820, 230, "#121318", p, r=18); rect(c, 980, 280, 8, 230, GREEN, p)
        draw_text(c, "GTA ONLINE (GTA V)", 1020, 350, "barlowblk", 52, WHITE, p)
        draw_par(c, "Sigue activo: Take-Two confirmó que lo seguirá actualizando.", 1020, 410, "intersb", 32, 740, color="#C9C9CF", a=p)
    p = ease_out(prog(t, s2, s2 + 0.5))
    if p > 0:
        rect(c, 980, 560, 820, 300, "#121318", p, r=18); rect(c, 980, 560, 820, 300, AMBER, p, r=18, stroke=3)
        draw_text(c, "¿ONLINE EN LEONIDA?", 1020, 640, "barlowblk", 56, WHITE, p)
        draw_text(c, "?", 1700, 790, "barlowblk", 200, AMBER, 0.25 * p + 0.2 * pulse(t, 1.4) * p, align="center")
        draw_par(c, "Probable algún día. Hoy: sin fecha ni anuncio.", 1020, 710, "intersb", 34, 600, color=WHITE, a=p)
        cert_tag(c, 1020, 790, "DEDUCCIÓN", p, 24, t=p)
    source_chip(c, 120, 980, "FAQ de PlayStation · declaraciones de Take-Two", ease_out(prog(t, s0, s0 + 0.5)))

def sc_recap(c, t, info, ctx):
    W, H = ctx.W, ctx.H; board_bg(c, W, H, t); header(c, W, t, "LISTA DE ABORDAJE", "VUELO GTA-VI")
    items = ["PLATAFORMA PS5 / SERIES", "210 GB LIBRES", "PRECARGA HECHA", "HORA LOCAL 00:00", "PRECIO REVISADO", "SUBTÍTULOS ES-MX / ES-ES", "ONLINE: SIN FECHA"]
    for i, it in enumerate(items):
        y = 165 + i * 105; st = 0.3 + i * 0.75
        flap_text(c, f"{i + 1:02d}", 90, y, t, st, cw=40, ch=70, seed=i)
        flap_text(c, it, 210, y, t, st + 0.1, cw=40, ch=70, per=0.02, spin=0.25, seed=i + 3)
        flap_text(c, "LISTO", 1520, y, t, st + 0.7, cw=50, ch=70, col=GREEN, seed=i + 7)
    s1 = info.w("listo")
    if t > s1:
        p = ease_out_back(prog(t, s1, s1 + 0.5)); c.save(); c.translate(W / 2, H / 2); c.rotate(-8); c.scale(p * 1.0, p * 1.0)
        rect(c, -460, -110, 920, 220, GREEN, 0.18, r=20); rect(c, -460, -110, 920, 220, GREEN, 1, r=20, stroke=10)
        draw_text(c, "LISTO PARA ABORDAR", 0, 38, "barlowblk", 110, GREEN, 1, align="center", tracking=4)
        c.restore()

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "PRÓXIMA PARADA: EL MAPA DE LEONIDA", "Región por región · lo oficial separado de lo deducido", AMBER)

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2 < gt < ctx.total - 20: watermark(c, W, H, 0.5)
    if gt < 8: ai_notice(c, W, H, clamp((8 - gt) / 1.0), "Animación original de Sal y Asfalto · no contiene imágenes ni material de Rockstar Games")

# ---------------------------------------------------------------- guion
B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))

beat("El jueves diecinueve de noviembre, a la medianoche, millones de consolas van a intentar entrar a Leonida al mismo tiempo. "
     "Y una parte de esa gente se va a quedar en la puerta. "
     "Por la hora. Por el espacio. O por una descarga que nunca debió hacer.",
     sc_hook, section="GANCHO", energy=1, sfx=[(0.1, "flap", 0.5), (0.6, "flap", 0.4), ("w:puerta", "buzz", 0.5), ("w:Por la hora", "hit", 0.5), ("w:Por el espacio", "hit", 0.5), ("w:descarga", "hit", 0.6)],
     note="Tablero de salidas: vuelos a Leonida 'A TIEMPO'; dos cambian a 'PUERTA CERRADA'. Aparecen las tres causas.")
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=2, trans=("flash", 0.3), note="Cortinilla de marca.")
beat("Estás en Sal y Asfalto, y aquí manda el semáforo: lo oficial va en verde, lo que deducimos va en amarillo y el rumor, en rojo. "
     "Hoy hacemos la lista de abordaje: siete comprobaciones para que a medianoche solo tengas que darle a play.",
     sc_intro, section="INTRODUCCIÓN", energy=2, trans=("zoom", 0.5), sfx=[(0.2, "paper", 0.5), ("w:verde", "pop", 0.4), ("w:amarillo", "pop", 0.4), ("w:en rojo", "pop", 0.4)],
     note="Tarjeta de embarque + semáforo de certeza de la marca.")
beat("Comprobación uno: la plataforma. GTA 6 sale solo en PlayStation 5 y en Xbox Series X y Series S. "
     "No hay versión para PS4 ni para Xbox One. Y tampoco para PC, por ahora: Take-Two no ha anunciado fecha, y su director ejecutivo dijo que la prioridad son las consolas. "
     "Para móvil, ninguna. "
     "Si ves un GTA 6 para Android o un instalador para PC, no es un adelanto: es una trampa. Le dedicamos un video completo, porque ya hay malware robando cuentas con ese anzuelo.",
     sc_platform, section="1 · PLATAFORMA", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:PlayStation 5", "pop", 0.4), ("w:Xbox Series", "pop", 0.4), ("w:PS4", "buzz", 0.3), ("w:PC,", "buzz", 0.3), ("w:móvil", "buzz", 0.3), ("w:trampa", "alarm", 0.25)])
beat("Dos: el espacio. Las tiendas marcan alrededor de {210 GB|doscientos diez gigas}. En Xbox, la ficha dice {209,86|doscientos nueve coma ochenta y seis}. "
     "Ojo con esto: un PS5 original de {825 GB|ochocientos veinticinco gigas} deja libres unos {667|seiscientos sesenta y siete}. "
     "Un Series S de {512|quinientos doce}, apenas unos {364|trescientos sesenta y cuatro}: ahí GTA 6 se come más de la mitad del disco. "
     "Si tienes un Series X, vas más holgado. "
     "Haz espacio hoy, no a las once y cincuenta y nueve.",
     sc_storage, section="2 · ESPACIO", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:210", "hit", 0.4), ("w:PS5", "tick", 0.5), ("w:Series S", "buzz", 0.3), ("w:Haz espacio", "hit", 0.5)])
beat("Tres: la precarga. Ya está disponible en las dos consolas. "
     "Y según la prensa, a las consolas con el juego precargado ya llegó una primera actualización, la uno punto cero cero dos. "
     "Si compraste en digital, deja la consola en modo reposo con las descargas activadas: así, cuando llegue la hora, solo faltará que se desbloquee.",
     sc_preload, section="3 · PRECARGA", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:actualización", "ding", 0.4), ("w:modo reposo", "pop", 0.3)])
beat("Cuatro: la hora. Rockstar confirmó que el juego se desbloquea a la medianoche, hora local. "
     "Eso significa que no hay un único botón global. En España se abre a las cero horas del jueves. "
     "En Argentina y Chile, a su medianoche, cuando en España ya son las cuatro de la mañana. "
     "En Colombia, Perú y Ecuador, a su medianoche, que son las seis en España. Y en el centro de México, a la medianoche local: las siete de la mañana en Madrid. "
     "Un detalle curioso: en Estados Unidos abre a la medianoche de la costa este, así que en la costa oeste se podrá jugar desde las nueve de la noche del miércoles. "
     "Si una tabla en internet te dice otra cosa, revisa la ficha de tu tienda: esa es la que manda.",
     sc_time, section="4 · HORA", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:España", "flap", 0.5), ("w:Argentina", "flap", 0.4), ("w:Colombia", "flap", 0.4), ("w:México", "flap", 0.4), ("w:Estados Unidos", "pop", 0.4), ("w:tabla", "pop", 0.4)])
beat("Cinco: el precio. En dólares, la edición estándar cuesta {79,99|setenta y nueve con noventa y nueve}, y la Ultimate, {99,99|noventa y nueve con noventa y nueve}. "
     "En la tienda de Xbox de México aparece a {1.499 pesos|mil cuatrocientos noventa y nueve pesos} la estándar, y en la de Colombia, a {339.900 pesos|trescientos treinta y nueve mil novecientos pesos}. "
     "En PlayStation Store, según el país, el precio sale en moneda local o en dólares, y la prensa ha visto cifras distintas. "
     "Antes de pagar, revisa el total con impuestos en tu tienda. "
     "Y un consejo de bolsillo: si alguien te ofrece GTA 6 mucho más barato fuera de una tienda oficial, desconfía. Te puedes quedar sin juego y sin dinero.",
     sc_price, section="5 · PRECIO", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:79,99", "coin", 0.4), ("w:1.499", "coin", 0.3), ("w:339.900", "coin", 0.3), ("w:consejo", "buzz", 0.3)])
beat("Seis: el idioma. GTA 6 no tiene doblaje al español: las voces están solo en inglés, como en toda la saga. "
     "Lo que sí trae son textos y subtítulos en dos variantes: español de México, pensado para Latinoamérica, y español de España. "
     "Así que, si vas a jugar con alguien que no lee rápido, prepárate para ser el narrador oficial de la sala.",
     sc_language, section="6 · IDIOMA", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:español de México", "pop", 0.4), ("w:español de España", "pop", 0.4), ("w:narrador", "ding", 0.3)])
beat("Siete: el modo online. Rockstar describe GTA 6 como una experiencia para un jugador, y no ha dado fecha para un nuevo online. "
     "GTA Online, el de GTA 5, sigue funcionando: Take-Two confirmó que lo seguirá actualizando. "
     "¿Llegará un online a Leonida? Es probable que algún día. Pero hoy es una pregunta sin respuesta, y aquí no te la vamos a vender como noticia.",
     sc_online, section="7 · ONLINE", energy=2, trans=("whip", 0.45), sfx=[(0.0, "whoosh", 0.5), ("w:experiencia", "pop", 0.3), ("w:¿Llegará", "riser", 0.3)])
beat("Recapitulemos: consola correcta, doscientos diez gigas libres, precarga hecha, tu hora local clara, el precio revisado, subtítulos en tu español y cero expectativas de online el primer día. "
     "Si todo eso está en verde, estás listo para abordar.",
     sc_recap, section="CIERRE", energy=3, trans=("iris", 0.6), sfx=[(0.2, "flap", 0.5), (2.5, "flap", 0.4), ("w:listo", "stamp", 0.8)])
beat("En el próximo video abrimos el mapa de Leonida, región por región, separando lo que Rockstar mostró de lo que todavía es pura deducción. "
     "Y si quieres que lleguemos juntos a la medianoche, suscríbete: el jueves te contamos qué cambió. Nos vemos en Leonida.",
     sc_end, section="LLAMADA A LA ACCIÓN", energy=2, hold=4.0, trans=("fade", 0.6), min=20)

VIDEO = dict(id="v01", folder="VIDEO_01", file="GTA6_kit_de_lanzamiento_7_comprobaciones",
             title="GTA 6: hora exacta en tu país, precio, peso e idioma — 7 cosas que revisar antes de medianoche",
             format="Largo (16:9)", music="synthwave", music_seed=11, voice="host", speed=1.02, beats=B, overlay=overlay,
             trans=("fade", 0.4), music_gain=0.5)

def thumbnail(c):
    W, H = 1280, 720
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, ["#121318", "#060608"]))
    c.drawCircle(420, 360, 520, rad_grad(420, 360, 520, [hexc(AMBER, 0.28), hexc(AMBER, 0)]))
    # reloj de paletas gigante
    for i, ch in enumerate("00:00"):
        x = 70 + i * 150; w = 132 if ch != ":" else 60
        if ch == ":": x += 0
        rect(c, x if ch != ":" else x + 36, 150, w, 330, "#1B1C22", 1, r=14)
        draw_text(c, ch, (x if ch != ":" else x + 36) + w / 2, 400, "monob", 250, AMBER, 1, align="center")
        rect(c, x if ch != ":" else x + 36, 312, w, 6, "#000000", 0.9)
    draw_text(c, "19 NOV · HORA LOCAL", 80, 560, "ovblk", 58, "#F5F2EA", 1)
    # bloque derecho
    rect(c, 830, 120, 400, 460, "#F3EDE0", 1, r=22)
    draw_text(c, "ANTES DE", 1030, 215, "barlowblk", 66, "#16161A", 1, align="center")
    draw_text(c, "JUGAR", 1030, 300, "barlowblk", 96, "#C2410C", 1, align="center")
    for i, (ic, lab) in enumerate((("disk", "210 GB"), ("tag", "PRECIO"), ("chat", "IDIOMA"))):
        y = 360 + i * 66; icon(c, ic, 900, y, 44, "#16161A"); draw_text(c, lab, 940, y + 16, "barlowblk", 46, "#16161A")
        icon(c, "check", 1180, y, 40, "#16A34A")
    sign_text(c, 80, 590, "GTA VI", 56)
    rect(c, 0, 0, W, H, "#000000", 0)
