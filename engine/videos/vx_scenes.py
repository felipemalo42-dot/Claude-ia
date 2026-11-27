"""Escenas de VIDEO_EXTRA. Cada función recibe (canvas, t relativo a la escena, info de tiempos, contexto)."""
import math, numpy as np, skia
from gfx import *
from components import cert_tag, source_chip, brand_sting, end_screen, sign_text, kinetic_words
from brand import PAL, guide_sign, draw_badge, wordmark
from videos.vx_lib import *

YEL = PAL["amarillo"]; SAL = PAL["sal"]

def fin(t, t0, d=0.45): return ease_out(prog(t, t0, t0 + d))
def pop(t, t0, d=0.4): return ease_out_back(prog(t, t0, t0 + d))

def layer_alpha(c, a, fn):
    """Dibuja fn() en una capa con opacidad a."""
    if a <= 0.003: return
    if a >= 0.997: fn(); return
    p = skia.Paint(); p.setAlphaf(a); c.saveLayer(skia.Rect.MakeWH(W, H), p); fn(); c.restore()

def zoomed(c, s, cx, cy, fn):
    c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy); fn(); c.restore()

def label(c, x, y, txt, t, col=YEL, size=30, bg="#000000", a=1.0, align="left", font_="ovblk"):
    """Rótulo con fondo que entra desde abajo. t = progreso 0..1."""
    if t <= 0: return
    f = font(font_, size); w = text_w(txt, f, 1) + size * 1.1; h = size * 1.55
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    yy = y + (1 - ease_out(clamp(t))) * 20
    rect(c, x, yy, w, h, bg, 0.72 * a * clamp(t), r=8)
    draw_text(c, txt, x + size * 0.55, yy + h * 0.5 + size * 0.36, font_, size, col, a * clamp(t), tracking=1)
    return w

def xmark(c, x, y, s, p, col=PAL["rojo"], a=1.0):
    if p <= 0: return
    line(c, x - s, y - s, x - s + 2 * s * clamp(p * 2), y - s + 2 * s * clamp(p * 2), col, a, s * 0.28)
    if p > 0.5: line(c, x + s, y - s, x + s - 2 * s * clamp(p * 2 - 1), y - s + 2 * s * clamp(p * 2 - 1), col, a, s * 0.28)

def swatch(c, x, y, w, h, col, name=None, a=1.0, tcol=INK, size=22):
    rect(c, x + 4, y + 6, w, h, "#000000", 0.25 * a, r=8, blur=6); rect(c, x, y, w, h, col, a, r=8)
    if name: draw_text(c, name, x + 14, y + h - 16, "ovsb", size, tcol, 0.85 * a)

# ====================================================================== GANCHO
def sc_hook(c, t, info, ctx):
    t_white = info.w("no son"); t_80 = info.w("Son de los años ochenta"); t_des = info.w("diseñador"); t_died = info.w("Murió"); t_8 = info.w("Ocho años")
    cam = min(t, 30) * 4.0; zs = 1.0 + 0.012 * min(t, 25)
    ons = [0.3, 0.8, 1.3, 1.75]
    neon = [clamp((t - o) / 0.25) for o in ons]
    flick = [0.0 if t > o + 0.45 else (0.7 if math.sin((t - o) * 60) > 0.2 else 0.0) for o in ons]
    flick = [f if n > 0 else 1.0 for f, n in zip(flick, neon)]
    def night(): zoomed(c, zs, W / 2, H * 0.55, lambda: street(c, t, "night", cam=cam, neon=1.0, lights=clamp(t / 1.2), flick=flick))
    night()
    kw = fin(t, t_white - 0.1, 0.9); k8 = fin(t, t_80 - 0.05, 0.6)
    if kw > 0 and k8 < 1:
        layer_alpha(c, kw * (1 - k8), lambda: zoomed(c, zs, W / 2, H * 0.55, lambda: street(c, t, "white", cam=cam)))
        label(c, 80, 120, "LOS ORIGINALES: BLANCOS · AÑOS 30", kw * (1 - k8), WHITE30["jade"], 34, bg="#FFFFFF")
    if k8 > 0:
        fade_out = 1 - fin(t, t_died - 0.2, 0.6) * 0.0
        layer_alpha(c, k8 * fade_out, lambda: zoomed(c, zs, W / 2, H * 0.55, lambda: street(c, t, "pastel", cam=cam)))
        # brochazo diagonal que «pinta» el año
        p = pop(t, t_80, 0.5) * (1 - fin(t, t_des - 0.3, 0.4))
        if p > 0.01:
            c.save(); c.translate(W / 2, 470); c.rotate(-6); c.scale(p, p)
            rect(c, -330, -110, 660, 200, PASTEL["rosa"], 0.95, r=30); rect(c, -330, -110, 660, 200, "#FFFFFF", 0.9, r=30, stroke=6)
            draw_text(c, "1980", 0, 50, "monoton", 150, "#7A1E48", 1, align="center")
            c.restore()
    # el diseñador: abanico de colores
    pd = fin(t, t_des - 0.1, 0.6)
    if pd > 0 and t < t_died + 0.3:
        a = pd * (1 - fin(t, t_died - 0.1, 0.4))
        cx, cy = 1520, 620
        cols = [PASTEL["rosa"], PASTEL["menta"], PASTEL["lavanda"], PASTEL["crema"], PASTEL["aqua"], PASTEL["durazno"]]
        for i, col in enumerate(cols):
            ang = -60 + i * 22 * pd
            c.save(); c.translate(cx, cy); c.rotate(ang); rect(c, -36, -330, 72, 330, col, a, r=10); rect(c, -36, -330, 72, 330, "#000000", 0.15 * a, r=10, stroke=2); c.restore()
        circle(c, cx, cy, 16, "#444444", a)
        label(c, 1180, 860, "UN DISEÑADOR REAL", a, INK, 38, bg="#FFFFFF")
    # línea de tiempo 1989 → 1997
    pt = fin(t, t_died - 0.1, 0.5)
    if pt > 0:
        rect(c, 0, 0, W, H, "#000000", 0.55 * pt)
        x0, x1, y = 460, 1460, 560
        line(c, x0 - 100, y, x0 - 100 + (x1 - x0 + 200) * pt, y, SAL, pt, 6)
        for xx, yr, lab in ((x0, "1989", "MUERE EL DISEÑADOR"), (x1, "1997", "PRIMER GTA")):
            pp = fin(t, t_died + (0 if yr == "1989" else 0.9), 0.4)
            circle(c, xx, y, 16, YEL if yr == "1997" else SAL, pp)
            draw_text(c, yr, xx, y - 50, "monoton", 96, SAL, pp, align="center")
            draw_text(c, lab, xx, y + 70, "ovmono", 30, SAL, pp * 0.9, align="center", tracking=3)
        p8 = fin(t, t_8 - 0.1, 0.5)
        if p8 > 0:
            pth = skia.Path(); pth.moveTo(x0, y + 120); pth.quadTo(x0, y + 170, x0 + 60, y + 170); pth.lineTo((x0 + x1) / 2 - 40, y + 170)
            pth.quadTo((x0 + x1) / 2, y + 170, (x0 + x1) / 2, y + 210); pth.quadTo((x0 + x1) / 2, y + 170, (x0 + x1) / 2 + 40, y + 170)
            pth.lineTo(x1 - 60, y + 170); pth.quadTo(x1, y + 170, x1, y + 120)
            c.drawPath(partial_path(pth, p8), paint(YEL, 1, stroke=6))
            draw_text(c, "8 AÑOS", (x0 + x1) / 2, y + 290, "abril", 84, YEL, p8, align="center")

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

# ====================================================================== INTRO
def sc_intro(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, ["#1A1B22", "#262033"]))
    grid(c, W, H, 60, "#FFFFFF", 0.035)
    tq = info.w("¿Por qué"); tr = info.w("raspar"); t7 = info.w("Siete capas"); tv = info.w("en verde"); ta = info.w("en amarillo")
    p = fin(t, tq - 0.2, 0.7)
    draw_text(c, "¿POR QUÉ", 120, 330 + (1 - p) * 30, "abril", 120, SAL, p)
    draw_text(c, "VICE CITY", 120, 470 + (1 - p) * 30, "abril", 150, PASTEL["rosa"], p, glow=(NEON["rosa"], 16))
    draw_text(c, "SE VE ASÍ?", 120, 600 + (1 - p) * 30, "abril", 120, SAL, p)
    # corte de pintura: primero vacío; la espátula lo «raspa» y deja ver las capas un instante
    pc = fin(t, 0.6, 0.6)
    x, y, w, h = 1240, 170, 520, 700
    ps = prog(t, tr, tr + 2.4)
    n = 7 * ease_io(clamp(ps * 1.6)) if ps < 0.85 else 7 * (1 - ease_io(clamp((ps - 0.85) / 0.15)))
    n = n if t < t7 + 1.5 else 7 * fin(t, t7, 1.0)
    layer_alpha(c, pc, lambda: cross_section(c, x, y, w, h, n, t, labels=True, scale_txt=1.35))
    if 0 < ps < 1:  # espátula
        sx = x + w + 30; sy = y + h - h * ps
        c.save(); c.translate(sx, sy); c.rotate(-20)
        rect(c, -120, -12, 130, 24, "#C0C6CC", 1, r=4); rect(c, 10, -16, 150, 32, "#6B4A2E", 1, r=10)
        c.restore()
    p7 = fin(t, t7 - 0.1, 0.5)
    label(c, 1240, 900, "7 CAPAS · MÁS DE 100 AÑOS", p7, YEL, 34)
    cert_tag(c, 120, 760, "DOCUMENTADO", 1.0, 34, t=prog(t, tv - 0.1, tv + 0.35))
    cert_tag(c, 120, 850, "INTERPRETACIÓN", 1.0, 34, t=prog(t, ta - 0.1, ta + 0.35))

# ====================================================================== LO OFICIAL
NEIGH = ["OCEAN BEACH", "LITTLE CUBA", "TISHA-WOCKA", "VC PORT"]
def sc_oficial(c, t, info, ctx):
    street(c, t, "pastel", cam=t * 3, cars=True); rect(c, 0, 0, W, H, "#120E1E", 0.72)
    tq = info.w("En su web"); tb = info.w("barrios"); tg = info.w("Guarda ese nombre"); te = info.w("existió")
    pq = fin(t, tq - 0.2, 0.6) * (1 - fin(t, tb - 0.3, 0.5))
    if pq > 0:
        quote_card(c, 160, 220, 1600, "Estamos muy lejos de los ochenta, pero Vice City sigue siendo la capital del sol y la diversión de Estados Unidos.",
                   sub="«We're a long way from the '80s, but Vice City is still the sun and fun capital of America.»",
                   src="FUENTE · rockstargames.com/VI · Only in Leonida · consultado el 18/11/2026", t=1.0, a=pq, size=52)
        cert_tag(c, 160, 140, "OFICIAL", pq, 30, t=1.0)
    pb = fin(t, tb - 0.2, 0.5)
    if pb > 0:
        hl = fin(t, tg - 0.2, 0.6)
        for i, nm in enumerate(NEIGH):
            pi = pop(t, tb + i * 0.18, 0.45)
            if pi <= 0: continue
            sw = 700; sh = 120; x = 160 + (i % 2) * 820; y = 260 + (i // 2) * 190
            if i == 0: x, y = lerp(x, W / 2 - sw * 0.75, hl), lerp(y, 330, hl)
            a = pi * (1 - 0.75 * hl) if i else pi
            s = 1.0 + 0.5 * hl if i == 0 else 1.0
            c.save(); c.translate(x + sw / 2, y + sh / 2); c.scale(pi * s, pi * s); c.translate(-(x + sw / 2), -(y + sh / 2))
            guide_sign(c, x, y, sw, sh, a=a); draw_text(c, nm, x + sw / 2, y + sh * 0.66, "ovblk", 58, SAL, a, align="center")
            c.restore()
        draw_text(c, "Barrios de Vice City según la web oficial", 160, 720, "inter", 30, SAL, pb * (1 - hl) * 0.85)
        label(c, 160, 760, "«HOTELES ART DÉCO EN TONOS PASTEL Y ARENA BLANCA»", pb * (1 - hl), YEL, 32)
        cert_tag(c, 160, 180, "OFICIAL", pb * (1 - hl), 30, t=1.0)
    pe = fin(t, te - 0.1, 0.5)
    if pe > 0:
        stamp(c, W / 2 + 470, 700, ["¿1912?"], t - te, col="#E7C27A", rot=-10, size=70)
        draw_text(c, "un nombre más viejo que cualquier videojuego", W / 2, 840, "dmserifi", 44, SAL, pe, align="center")

# ====================================================================== CAPA 1 · 1912
def island_path(widen=0.0):
    pts_l, pts_r = [], []
    for k in range(29):
        y = 70 + k * 34; base = 1180 + 40 * math.sin(k * 0.35) + 25 * math.sin(k * 0.9)
        wv = 34 + 18 * math.sin(k * 0.7 + 1) + widen * (60 + 20 * math.sin(k * 0.5))
        pts_l.append((base - wv * 0.5, y)); pts_r.append((base + wv, y))
    return poly(pts_l + pts_r[::-1])

def sc_island(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [SEPIA["papel"], SEPIA["papel2"]]))
    tm = info.w("manglares"); tp = info.w("primer plano"); to = info.w("Ocean Beach Realty"); tn = info.w("no es la ciudad")
    t2 = info.w("dos ciudades"); tw = info.w("En la web de Rockstar")
    # agua de la bahía (líneas) y tierra firme
    for k in range(16):
        yy = 90 + k * 60; line(c, 640, yy + math.sin(t + k) * 4, 1090, yy + math.sin(t + k) * 4, SEPIA["tinta2"], 0.18, 2)
    for k in range(10):
        yy = 60 + k * 100; line(c, 1350, yy + math.sin(t * 0.8 + k) * 5, W - 20, yy + math.sin(t * 0.8 + k) * 5, SEPIA["tinta2"], 0.16, 2)
    land = poly([(0, 0), (560, 0), (600, 160), (585, 420), (640, 700), (610, 1080), (0, 1080)])
    c.drawPath(land, paint(SEPIA["papel2"], 1)); c.drawPath(land, paint(SEPIA["tinta"], 0.7, stroke=3))
    for k in range(40):  # textura de tierra
        rng = np.random.default_rng(k); circle(c, rng.random() * 520, rng.random() * 1050, 2.5, SEPIA["tinta2"], 0.25)
    draw_text(c, "MIAMI", 260, 520, "abril", 72, SEPIA["tinta"], 0.9, align="center")
    draw_text(c, "tierra firme", 260, 570, "elite", 30, SEPIA["tinta2"], 0.8, align="center")
    draw_text(c, "BAHÍA", 865, 560, "elite", 34, SEPIA["tinta2"], 0.7, align="center", tracking=6)
    draw_text(c, "OCÉANO ATLÁNTICO", 1660, 560, "elite", 32, SEPIA["tinta2"], 0.7, align="center", tracking=4)
    widen = fin(t, tp - 1.2, 2.5)
    isl = island_path(widen)
    c.drawPath(isl, paint("#E3CFA0", 1)); c.drawPath(isl, paint(SEPIA["tinta"], 0.85, stroke=3))
    pm = fin(t, tm - 0.3, 0.8) * (1 - 0.7 * widen)
    for k in range(26):  # manglares
        rng = np.random.default_rng(100 + k); yy = 90 + rng.random() * 900; xx = 1160 + 40 * math.sin(yy / 34 * 0.35) + rng.random() * 40
        for j in range(3): circle(c, xx + j * 9 - 9, yy + (j % 2) * 6, 11, "#5E7A4A", pm * 0.85)
    pp = fin(t, tp - 0.2, 1.6)
    if pp > 0:  # cuadrícula del plano
        c.save(); c.clipPath(isl, doAntiAlias=True)
        for k in range(30):
            q = clamp(pp * 30 - k)
            if q <= 0: break
            yy = 90 + k * 32; line(c, 1100, yy, 1100 + 300 * q, yy, SEPIA["tinta"], 0.55, 1.5)
        for k in range(8):
            xx = 1120 + k * 30; line(c, xx, 80, xx, 80 + 960 * pp, SEPIA["tinta"], 0.35, 1.2)
        c.restore()
        draw_text(c, "PLANO · JULIO 1912", 1240, 1050, "elite", 28, SEPIA["tinta"], pp, align="center")
    if t > to - 0.05:
        stamp(c, 820, 230, ["OCEAN BEACH", "REALTY COMPANY"], t - to, col="#8E2A1E", rot=-7, size=54)
    pn = fin(t, tn - 0.2, 0.7)
    if pn > 0:
        line(c, 1095, 60, 1095, 60 + 980 * pn, "#8E2A1E", 0.9, 5, dash=[22, 14])
        label(c, 300, 640, "CIUDAD DE MIAMI", pn, SEPIA["papel"], 30, bg=SEPIA["tinta"])
        label(c, 1280, 760, "MIAMI BEACH · MUNICIPIO DESDE 1915", pn, SEPIA["papel"], 28, bg="#8E2A1E")
    p2 = fin(t, t2 - 0.1, 0.5)
    if p2 > 0 and t < tw: draw_text(c, "2 CIUDADES", 860, 900, "abril", 90, "#8E2A1E", p2 * (1 - fin(t, tw - 0.3, 0.3)), align="center")
    pw = pop(t, tw - 0.1, 0.5)
    if pw > 0:
        c.save(); c.translate(860, 860); c.scale(pw, pw)
        guide_sign(c, -330, -70, 660, 120); draw_text(c, "OCEAN BEACH", 0, 10, "ovblk", 56, SAL, 1, align="center")
        c.restore()
        draw_text(c, "= barrio de Vice City en la web de Rockstar", 860, 990, "inter", 30, SEPIA["tinta"], pw, align="center")
        cert_tag(c, 560, 715, "OFICIAL", 1.0, 26, t=pw)
    draw_text(c, "esquema ilustrado · no a escala", 40, 1050, "elite", 22, SEPIA["tinta2"], 0.7)
    chapter_header(c, t, 1, "1912", "LA ARENA", "#FFF4DD", info.d)

# ====================================================================== TORMENTA 1926
def med_building(c, x, yb, w, h, col, k, shake=0.0):
    c.save(); c.translate(shake * math.sin(k * 7.3), 0)
    rect(c, x, yb - h, w, h, col)
    roof = poly([(x - 14, yb - h), (x + w / 2, yb - h - h * 0.18), (x + w + 14, yb - h)]); c.drawPath(roof, paint("#8C5A3C"))
    for i in range(3):  # arcos
        ax = x + w * (0.18 + 0.3 * i); pth = skia.Path(); pth.addRect(skia.Rect.MakeXYWH(ax, yb - h * 0.45, w * 0.16, h * 0.3))
        c.drawPath(pth, paint("#3D2B1F", 0.8)); circle(c, ax + w * 0.08, yb - h * 0.45, w * 0.08, "#3D2B1F", 0.8)
    for i in range(2):
        rect(c, x + w * (0.2 + 0.4 * i), yb - h * 0.85, w * 0.14, h * 0.18, "#3D2B1F", 0.75)
    c.restore()

def sc_storm(c, t, info, ctx):
    tf = info.w("fiebre"); th = info.w("Hasta el 18"); tc = info.w("categoría cuatro"); tm = info.w("El mar entró"); tk = info.w("casinos")
    tg = info.w("La fiebre se acabó"); td = info.w("Gran Depresión")
    dark = fin(t, th - 0.3, 1.2)
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [mixc("#BFD3DD", "#2E3338", dark), mixc("#F1E6CF", "#4A4F52", dark)]))
    shake = 6 * fin(t, tc, 1.0) * (1 - fin(t, tg, 1.0))
    cols = ["#E9D9BB", "#E2CBA6", "#EFE3C8", "#DCC4A0", "#E6D3B0", "#F0E2C2"]
    for i in range(6):
        if i == 4 and t > tk:  # se derrumba un casino frente a la playa
            pcol = fin(t, tk, 1.2); c.save(); c.translate(0, pcol * 300); c.rotate(pcol * 8)
            med_building(c, 70 + i * 310, 820, 260, 330 + (i % 3) * 60, cols[i], i, shake); c.restore()
            continue
        med_building(c, 70 + i * 310, 820, 260, 330 + (i % 3) * 60, cols[i], i, shake)
    rect(c, 0, 820, W, 260, "#C9B48C")
    pf = fin(t, tf - 0.2, 0.6) * (1 - dark)
    if pf > 0:  # carteles de venta y precio que sube
        for i in range(3):
            x = 220 + i * 600; rect(c, x, 860, 220, 110, "#F7F1E1", pf, r=6); rect(c, x, 860, 220, 110, "#8E2A1E", pf, r=6, stroke=4)
            draw_text(c, "SE VENDE", x + 110, 905, "ovblk", 34, "#8E2A1E", pf, align="center")
            draw_text(c, "LOTES", x + 110, 948, "elite", 30, SEPIA["tinta"], pf, align="center")
        val = 100 + 900 * prog(t, tf, tf + 3.0)
        label(c, 1460, 120, f"PRECIO DEL LOTE ↑ {int(val)} %", pf, "#8E2A1E", 34, bg="#F7F1E1")
    if dark > 0:  # huracán
        cx, cy = 1500 - 500 * prog(t, th, th + 9), 230; R = 380 * dark
        for k in range(5):
            pth = skia.Path(); ang0 = t * 1.6 + k * 2 * math.pi / 5
            for j in range(60):
                rr = R * (1 - j / 60); a = ang0 + j * 0.12; pt = (cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.55)
                pth.lineTo(*pt) if j else pth.moveTo(*pt)
            c.drawPath(pth, paint("#E8ECEE", 0.35 * dark, stroke=26))
        circle(c, cx, cy, 30 * dark, "#2E3338", dark)
        for k in range(140):  # lluvia
            rng = np.random.default_rng(k); x = (rng.random() * W + t * 900) % (W + 200) - 100; y = (rng.random() * H + t * 1600) % H
            line(c, x, y, x - 40, y + 70, "#DDE6EA", 0.35 * dark, 2)
        for k in range(10):  # viento
            yy = 120 + k * 90; xx = (k * 300 - t * 1400) % (W + 600) - 300
            line(c, xx, yy, xx + 260, yy - 20, "#FFFFFF", 0.25 * dark, 3)
    pd = pop(t, th, 0.5)
    if pd > 0:
        c.save(); c.translate(360, 210); c.scale(pd, pd)
        rect(c, -260, -90, 520, 160, "#F4ECD9", 0.95, r=10); draw_text(c, "18 · SEP · 1926", 0, 18, "abril", 64, "#2B2620", 1, align="center")
        c.restore()
    label(c, 120, 330, "HURACÁN · CATEGORÍA 4", fin(t, tc - 0.1, 0.4), "#FFFFFF", 34, bg="#8E2A1E")
    pm = fin(t, tm - 0.2, 2.0)
    if pm > 0:  # el mar sube
        lvl = 1080 - 330 * pm * (1 - 0.4 * fin(t, tg, 2.0))
        pth = skia.Path(); pth.moveTo(0, H)
        for k in range(49): pth.lineTo(k * 40, lvl + 14 * math.sin(k * 0.6 + t * 4))
        pth.lineTo(W, H); pth.close(); c.drawPath(pth, paint("#56707A", 0.85))
    if t > tg - 0.05:
        rect(c, 0, 0, W, H, "#000000", 0.35 * fin(t, tg - 0.05, 0.4))
        stamp(c, W / 2, 460, ["FIN DEL BOOM"], t - tg, col="#E7C27A", rot=-6, size=84)
    if t > td:
        pdp = fin(t, td, 0.5); rect(c, W / 2 - 560, 640, 1120, 90, "#000000", 0.6 * pdp, r=14)
        draw_text(c, "la Gran Depresión llegó antes a Florida", W / 2, 700, "dmserifi", 46, "#FFFFFF", pdp, align="center")

# ====================================================================== CAPA 2 · AÑOS 30
def sc_blueprint(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [BLUE["fondo"], BLUE["fondo2"]])); grid(c, W, H, 40, BLUE["linea"], 0.07)
    th = info.w("hoteles pequeños"); tm = info.w("Murray Dixon"); te = info.w("cejas"); tr = info.w("ventanas redondas"); t3 = info.w("de tres en tres")
    dp = prog(t, 1.2, max(1.3, te - 0.4))
    hotel_row(c, t, "white", yb=900, x0=70, s=1.0, outline=BLUE["linea"], draw_p=dp)
    ph = fin(t, th - 0.2, 0.5)
    if ph > 0:
        for i, lab in enumerate(("PEQUEÑOS", "BARATOS", "DE ESTUCO", "POR TEMPORADA")):
            label(c, 90 + i * 330, 120, lab, fin(t, th + i * 0.35, 0.4) * (1 - fin(t, te - 0.4, 0.4)), BLUE["fondo"], 30, bg=BLUE["linea"])
    pm = fin(t, tm - 0.2, 0.5) * (1 - fin(t, te - 0.4, 0.4))
    if pm > 0: name_card(c, 1180, 160, "L. Murray Dixon", "arquitecto · Miami Beach, años 30", t - tm + 0.2, col=BLUE["linea"], a=pm)
    # rótulos con líneas guía
    def callout(x0, y0, x1, y1, txt, tt):
        p = fin(t, tt - 0.1, 0.5)
        if p <= 0: return
        circle(c, x0, y0, 12, YEL, p); line(c, x0, y0, lerp(x0, x1, p), lerp(y0, y1, p), YEL, p, 3)
        label(c, x1 - 10, y1 - 26, txt, p, BLUE["fondo"], 30, bg=YEL)
    callout(170, 520, 300, 210, "CEJAS: SOMBRA SIN AIRE ACONDICIONADO", te)
    callout(1145, 520, 1250, 300, "OJOS DE BUEY: ESTILO TRASATLÁNTICO", tr)
    callout(270, 280, 520, 380, "REGLA DE TRES", t3)
    chapter_header(c, t, 2, "AÑOS 30", "EL BLANCO", "#F2EFE6", info.d)

def sc_white(c, t, info, ctx):
    tb = info.w("eran blancos"); ts = info.w("Servicio"); tj = info.w("verde jade"); tn = info.w("Nada de rosa")
    pw = fin(t, tb - 0.3, 1.0)
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [BLUE["fondo"], BLUE["fondo2"]])); grid(c, W, H, 40, BLUE["linea"], 0.07)
    hotel_row(c, t, "white", yb=900, x0=70, s=1.0, outline=BLUE["linea"], draw_p=1.0)
    layer_alpha(c, pw, lambda: street(c, t, "white", cam=0))
    p0 = fin(t, 0.0, 0.6) * (1 - fin(t, tb - 0.4, 0.4))
    draw_text(c, "ART DÉCO TROPICAL", W / 2, 200, "abril", 110, SAL, p0, align="center", shadow=(0, 4, 10, "#000000", 0.6))
    pb = pop(t, tb, 0.5)
    if pb > 0:
        c.save(); c.translate(W / 2, 180); c.scale(pb, pb)
        rect(c, -500, -100, 1000, 170, "#FFFFFF", 0.92, r=18); draw_text(c, "ERAN BLANCOS", 0, 40, "abril", 120, INK, 1, align="center")
        c.restore()
    if t > ts:
        source_chip(c, 90, 980, "Servicio de Parques Nacionales (NPS), 2018", fin(t, ts, 0.5))
        cert_tag(c, 90, 900, "DOCUMENTADO", 1.0, 28, t=prog(t, ts, ts + 0.4))
    pj = fin(t, tj - 0.2, 0.5)
    if pj > 0:
        rect(c, 1030, 300, 860, 560, "#FFFFFF", 0.88 * pj, r=20)
        for i, (nm, col) in enumerate((("verde jade", WHITE30["jade"]), ("ocre", WHITE30["ocre"]), ("coral", WHITE30["coral"]))):
            q = pop(t, tj + i * 0.35, 0.4); swatch(c, 1070 + i * 270, 330, 240, 130, col, nm, q, "#FFFFFF")
        draw_text(c, "solo pequeños toques", 1460, 520, "dmserifi", 40, INK, pj, align="center")
    pn = fin(t, tn - 0.1, 0.4)
    if pn > 0:
        for i, (nm, col) in enumerate((("rosa chicle", "#FF7FB6"), ("lavanda", PASTEL["lavanda"]))):
            q = fin(t, tn + i * 0.9, 0.3); x = 1120 + i * 360
            swatch(c, x, 580, 300, 140, col, nm, q); xmark(c, x + 150, 650, 70, fin(t, tn + i * 0.9 + 0.2, 0.4))
        draw_text(c, "nada de esto", 1460, 800, "dmserifi", 40, "#8E2A1E", pn, align="center")

# ====================================================================== CAPA 3 · AÑOS 70
def porch_people(c, t, n=6, a=1.0):
    for k in range(n):
        x = 160 + k * 300 + (k % 2) * 40; y = 700
        rect(c, x - 28, y - 46, 56, 8, "#6B6457", a); line(c, x - 24, y - 40, x - 30, y, "#6B6457", a, 4); line(c, x + 24, y - 40, x + 30, y, "#6B6457", a, 4)
        rect(c, x - 22, y - 96, 44, 54, "#5A5448", a, r=12); circle(c, x, y - 112, 17, "#5A5448", a)
        line(c, x + 18, y - 70, x + 34 + 4 * math.sin(t + k), y - 56, "#5A5448", a, 7)

def bulldozer(c, x, y, s, t, col="#C9A227"):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -160, -120, 240, 90, col, 1, r=8); rect(c, -40, -200, 110, 90, col, 1, r=6); rect(c, -28, -190, 80, 60, "#2B2B2B", 0.8, r=4)
    rect(c, -190, -40, 300, 50, "#2B2B2B", 1, r=25)
    for k in range(6): circle(c, -165 + k * 52, -15, 16, "#555555")
    blade = poly([(80, -130), (190, -150), (215, 10), (90, 0)]); c.drawPath(blade, paint("#8A8A8A")); c.drawPath(blade, paint("#333333", 1, stroke=4))
    c.restore()

def sc_decline(c, t, info, ctx):
    tr = info.w("renovación urbana")
    street(c, t, "faded", cam=t * 2, cars=True)
    for k in range(18):  # manchas y descascarado
        rng = np.random.default_rng(k); circle(c, 80 + rng.random() * 1700, 250 + rng.random() * 400, 10 + rng.random() * 26, "#6F6A60", 0.18)
    porch_people(c, t, 6, fin(t, 1.8, 0.8))
    pr = fin(t, tr - 0.2, 0.6)
    if pr > 0:
        paper(c, 120, 140, 760, 330, ["Proyecto: demoler y reconstruir", "Zona: South Beach", "Estado: aprobado (?)"], (t - tr) * 1.0, cps=34, size=34, rot=-3, a=pr,
              title="PLAN DE RENOVACIÓN URBANA")
        bx = W + 300 - 900 * fin(t, tr, 2.5); bulldozer(c, bx, 860, 1.2, t)
    chapter_header(c, t, 3, "AÑOS 70", "EL ABANDONO", "#E9E2D0", info.d)

def sc_capitman(c, t, info, ctx):
    tb = info.w("Barbara Capitman"); t76 = info.w("En 1976"); tv = info.w("vigilias"); tx = info.w("excavadoras")
    street(c, t, "faded", cam=10 + t * 2, cars=False); rect(c, 0, 0, W, H, "#000000", 0.35)
    name_card(c, 110, 130, "Barbara Capitman", "activista · Miami Beach · 1920–1990", t - tb + 0.3, col="#E7C27A")
    p76 = fin(t, t76 - 0.2, 0.5) * (1 - fin(t, tv - 0.3, 0.4))
    if p76 > 0: paper(c, 1040, 120, 780, 300, ["1976", "Liga de Preservación del Diseño", "de Miami (MDPL)"], (t - t76) * 1.4, cps=30, size=40, rot=2, a=p76)
    pv = fin(t, tv - 0.2, 0.6)
    if pv > 0:  # velas de vigilia
        for k in range(14):
            x = 820 + (k % 7) * 90; y = 960 - (k // 7) * 70
            rect(c, x - 8, y - 40, 16, 40, "#F4ECD9", pv); fl = 4 * math.sin(t * 12 + k)
            circle(c, x, y - 50 + fl * 0.3, 7, "#FFC14D", pv); circle(c, x, y - 50, 26, "#FFC14D", 0.18 * pv, blur=10)
    px = fin(t, tx - 0.3, 1.2)
    if px > 0:  # una silueta frena a la excavadora
        bx = W - 300 * px; bulldozer(c, bx + 260, 880, 1.15, t)
        x = 1260; rect(c, x - 24, 760, 48, 120, "#1D1B18", px, r=16); circle(c, x, 735, 22, "#1D1B18", px)
        line(c, x + 20, 790, x + 80, 740, "#1D1B18", px, 9); rect(c, x + 60, 640, 150, 100, "#F4ECD9", px, r=6)
        draw_text(c, "¡ALTO!", x + 135, 705, "ovblk", 38, "#8E2A1E", px, align="center")

def sc_register(c, t, info, ctx):
    tl = info.w("lo logró"); tp = info.w("primer barrio"); tn = info.w("no detuvo"); ta = info.w("algo más llamativo")
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, ["#2A2620", "#3A342B"]))
    pc = fin(t, 0.0, 0.6)
    c.save(); c.translate(W / 2 - 40, H / 2 - 20); c.rotate(-2)
    rect(c, -560, -380, 1120, 720, "#F4ECD9", pc); rect(c, -530, -350, 1060, 660, "#9C8A5E", pc, stroke=4)
    draw_text(c, "REGISTRO NACIONAL DE", 0, -230, "abril", 60, "#2B2620", pc, align="center")
    draw_text(c, "LUGARES HISTÓRICOS", 0, -160, "abril", 60, "#2B2620", pc, align="center")
    draw_text(c, "Distrito arquitectónico de Miami Beach", 0, -60, "elite", 38, "#2B2620", pc, align="center")
    pp = fin(t, tp - 0.2, 0.5)
    draw_text(c, "primer barrio del siglo XX reconocido como histórico", 0, 40, "dmserifi", 40, "#8E2A1E", pp, align="center")
    c.restore()
    if t > tl - 0.05: stamp(c, W / 2 + 330, 640, ["14 · MAYO · 1979"], t - tl, col="#1E5E3A", rot=-12, size=60)
    if pp > 0: cert_tag(c, 140, 120, "DOCUMENTADO", 1.0, 28, t=pp)
    pn = fin(t, tn - 0.2, 0.5)
    if pn > 0:
        rect(c, 0, 0, W, H, "#16130F", 0.88 * pn)
        for i, (nm, yr) in enumerate((("HOTEL BOULEVARD", "1980"), ("HOTEL NEW YORKER", "1981"), ("HOTEL SENATOR", "1988"))):
            q = fin(t, tn + i * 0.45, 0.4); y = 330 + i * 170
            rect(c, 420, y, 1080, 130, "#E9E2D0", q, r=10)
            draw_text(c, nm, 470, y + 82, "ovblk", 52, "#2B2620", q); draw_text(c, f"DEMOLIDO · {yr}", 1460, y + 82, "ovmono", 34, "#8E2A1E", q, align="right")
            xmark(c, 1490, y + 65, 40, fin(t, tn + i * 0.45 + 0.25, 0.3))
        draw_text(c, "Fuentes: NPS (2018) · National Trust for Historic Preservation (2014)", W / 2, 900, "inter", 26, SAL, pn * 0.8, align="center")
    pa = fin(t, ta - 0.1, 0.6)
    if pa > 0:  # una gota de pintura cae
        y = lerp(-80, 560, ease_in(pa)); circle(c, W / 2, y, 34, PASTEL["rosa"], 1)
        c.drawPath(poly([(W / 2 - 30, y - 10), (W / 2, y - 80), (W / 2 + 30, y - 10)]), paint(PASTEL["rosa"]))

# ====================================================================== CAPA 4 · 1980
def sc_horowitz(c, t, info, ctx):
    tl = info.w("Leonard Horowitz"); tm = info.w("se mudó"); ti = info.w("una idea")
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [PASTEL["rosa"], PASTEL["lavanda"], PASTEL["aqua"]]))
    for k in range(9):  # franjas de pintura
        rect(c, -200 + k * 260 + (t * 20) % 260, 0, 120, H, "#FFFFFF", 0.08)
    c.save(); c.translate(0, 300); layer_alpha(c, 0.35, lambda: hotel_row(c, t, "pastel", yb=780, x0=70 - t * 6, s=1.0)); c.restore()
    name_card(c, 110, 150, "Leonard Horowitz", "diseñador · Nueva York → South Beach · murió en 1989", t - tl + 0.2, col="#7A1E48")
    pm = fin(t, tm - 0.2, 1.2)
    if pm > 0:  # trayecto NY → South Beach
        x0, y0, x1, y1 = 1500, 260, 1320, 820
        pth = skia.Path(); pth.moveTo(x0, y0); pth.cubicTo(1750, 450, 1250, 600, x1, y1)
        c.drawPath(partial_path(pth, pm), paint("#2B2B44", 0.9, stroke=6, cap="round")); circle(c, x0, y0, 14, "#2B2B44")
        draw_text(c, "NUEVA YORK", x0 + 30, y0 + 10, "ovblk", 34, "#2B2B44", 1)
        if pm > 0.95: circle(c, x1, y1, 16, "#7A1E48"); draw_text(c, "SOUTH BEACH", x1 - 30, y1 + 60, "ovblk", 34, "#7A1E48", fin(t, tm + 1.0, 0.4), align="right")
    pi = fin(t, ti - 0.1, 0.6)
    if pi > 0:
        rect(c, 0, 0, W, H, "#1A1424", 0.6 * pi)
        kinetic_words(c, "SI NADIE MIRA ESTOS EDIFICIOS, HAY QUE OBLIGAR A LA GENTE A MIRARLOS", W / 2, 420, t - ti, "abril", 92, "#FFFFFF",
                      accent=PASTEL["rosa"], accent_words=("OBLIGAR", "MIRARLOS"), align="center", maxw=1500)
    chapter_header(c, t, 4, "1980", "EL PASTEL", "#FFFFFF", info.d)

def bakery(c, x, yb, s, cols, prog_paint, t, candles=0.0):
    """Edificio de esquina de dos plantas (panadería ilustrada). cols: (cuerpo, cornisa, franja, toldo)."""
    w, h = 820 * s, 520 * s; y0 = yb - h
    body = cols[0]
    rect(c, x, y0, w, h, "#F4F1EA"); rect(c, x - 10 * s, y0 - 20 * s, w + 20 * s, 34 * s, "#F4F1EA")
    def painted():
        rect(c, x, y0, w, h, body)
        rect(c, x - 10 * s, y0 - 20 * s, w + 20 * s, 34 * s, cols[1])
        rect(c, x, y0 + h * 0.48, w, 26 * s, cols[2])
        rect(c, x + w * 0.04, yb - h * 0.36, w * 0.92, 40 * s, cols[3], r=10)
    if prog_paint > 0:  # máscara de brochazos
        p = skia.Paint(); c.saveLayer(skia.Rect.MakeWH(W, H), p); painted()
        mp = skia.Paint(); mp.setBlendMode(skia.BlendMode.kDstIn); mp.setAntiAlias(True)
        mp.setStyle(skia.Paint.kStroke_Style); mp.setStrokeWidth(150 * s); mp.setStrokeCap(skia.Paint.kRound_Cap)
        pth = skia.Path(); rows = 5
        for r in range(rows):
            yy = y0 - 20 * s + r * (h + 40 * s) / (rows - 1)
            (pth.moveTo(x - 40 * s, yy) if r % 2 == 0 else pth.moveTo(x + w + 40 * s, yy))
            pth.lineTo(x + w + 40 * s, yy + 30 * s) if r % 2 == 0 else pth.lineTo(x - 40 * s, yy + 30 * s)
        c.drawPath(partial_path(pth, clamp(prog_paint)), mp); c.restore()
    for f in range(2):  # ventanas
        for k in range(4):
            wx = x + w * (0.08 + 0.23 * k); wy = y0 + 70 * s + f * 200 * s
            rect(c, wx, wy, w * 0.15, 120 * s, "#4A5A70", 0.95, r=6)
            rect(c, wx - 8 * s, wy - 18 * s, w * 0.15 + 16 * s, 12 * s, cols[1] if prog_paint > 0.6 else "#E6E1D6")
    draw_text(c, "PANADERÍA", x + w / 2, yb - h * 0.36 + 32 * s, "abril", 34 * s, "#FFFFFF" if prog_paint > 0.8 else "#8A857A", 1, align="center")
    if candles > 0:
        for k in range(5):
            cx = x + w * (0.18 + 0.16 * k); cy = y0 - 20 * s
            rect(c, cx - 9 * s, cy - 80 * s * candles, 18 * s, 80 * s * candles, ["#FFB3C7", "#AFC3F0", "#A8E6C9", "#F6E3A8", "#FFB3C7"][k])
            if candles > 0.9:
                fl = 3 * math.sin(t * 13 + k); circle(c, cx, cy - 92 * s + fl * 0.3, 10 * s, "#FFC14D"); circle(c, cx, cy - 92 * s, 30 * s, "#FFC14D", 0.2, blur=10)

def sc_bakery(c, t, info, ctx):
    tp = info.w("paleta"); tb = info.w("panadería"); tf = info.w("Friedman's"); tw = info.w("completamente blanca")
    tr = info.w("rosa algodón"); ta = info.w("azul pervinca"); tc = info.w("crema"); tm = info.w("verde menta"); tk = info.w("pastel de cumpleaños")
    sky(c, "day", t, hy=H); rect(c, 0, 880, W, 200, "#BDB7AA"); rect(c, 0, 870, W, 14, "#9E978A")
    # abanico de la paleta: sol, cielo, mar, arena
    pf = fin(t, tp - 0.2, 0.8) * (1 - fin(t, tb - 0.3, 0.5))
    if pf > 0:
        items = [("SOL", PASTEL["crema"]), ("CIELO", PASTEL["pervinca"]), ("MAR", PASTEL["aqua"]), ("ARENA", PASTEL["arena"]), ("ATARDECER", PASTEL["rosa"])]
        for i, (nm, col) in enumerate(items):
            c.save(); c.translate(W / 2, 900); c.rotate(-50 + i * 25 * pf)
            rect(c, -60, -620, 120, 620, col, pf, r=14); rect(c, -60, -620, 120, 620, "#000000", 0.12 * pf, r=14, stroke=2)
            draw_text(c, nm, 0, -560, "ovblk", 26, INK, pf, align="center"); c.restore()
        circle(c, W / 2, 900, 22, "#444444", pf)
    pb = fin(t, tb - 0.2, 0.6)
    if pb > 0:
        q = ease_io(prog(t, tr - 0.2, tm + 0.6))
        cols = (PASTEL["rosa"], PASTEL["pervinca"], PASTEL["crema"], PASTEL["menta"])
        # cada color entra cuando se nombra (cuerpo, cornisa, franja, toldo)
        cc = [cols[0] if t > tr else "#F4F1EA", cols[1] if t > ta else "#F4F1EA", cols[2] if t > tc else "#F4F1EA", cols[3] if t > tm else "#F4F1EA"]
        layer_alpha(c, pb, lambda: bakery(c, 550, 880, 1.0, cc, q, t, candles=fin(t, tk - 0.1, 0.6)))
        label(c, 80, 120, "FRIEDMAN'S · CALLE 7 Y AVENIDA WASHINGTON", fin(t, tf - 0.2, 0.5), INK, 32, bg="#FFFFFF")
        pw = fin(t, tw - 0.2, 0.4) * (1 - fin(t, tr - 0.3, 0.3))
        label(c, 80, 200, "ERA COMPLETAMENTE BLANCA", pw, "#FFFFFF", 34, bg=INK)
        for i, (nm, col, tt) in enumerate((("ROSA ALGODÓN DE AZÚCAR", cols[0], tr), ("AZUL PERVINCA", cols[1], ta), ("CREMA", cols[2], tc), ("VERDE MENTA", cols[3], tm))):
            q2 = pop(t, tt - 0.05, 0.4)
            if q2 > 0: swatch(c, 1460, 180 + i * 150, 380, 120, col, nm, q2, INK, 24)
        if t > tk: draw_text(c, "«parecía un pastel de cumpleaños»", W / 2, 1010, "dmserifi", 48, INK, fin(t, tk, 0.5), align="center")
        source_chip(c, 80, 980, "WLRN (2013) · NPS (2018)", fin(t, tb, 0.5) * (1 - fin(t, tk - 0.3, 0.3)))

def sc_continuity(c, t, info, ctx):
    td = info.w("esto no somos"); te = info.w("edificio por edificio"); tc = info.w("color principal"); tu = info.w("una sola pieza")
    pe = prog(t, te - 0.2, te + 2.2)
    street(c, t, "white", cam=0, cars=True)
    # la paleta se extiende edificio por edificio
    for i in range(4):
        q = clamp(pe * 4 - i)
        if q > 0:
            sp = HOTELS[i]; x = 70 + sum(h["w"] + 24 for h in HOTELS[:i])
            c.save(); c.clipRect(skia.Rect.MakeXYWH(x - 30, 0, (sp["w"] + 60) * q, 720))
            facade(c, x, 700, sp, hotel_colors("pastel", i), t, "pastel"); c.restore()
    pd = pop(t, td - 0.1, 0.45) * (1 - fin(t, te - 0.4, 0.4))
    if pd > 0:  # globo de diálogo
        c.save(); c.translate(1300, 260); c.scale(pd, pd)
        rect(c, -420, -110, 840, 200, "#FFFFFF", 1, r=60); c.drawPath(poly([(-160, 80), (-240, 180), (-80, 85)]), paint("#FFFFFF"))
        draw_text(c, "«Esto no somos nosotros»", 0, 20, "dmserifi", 64, INK, 1, align="center"); c.restore()
        draw_text(c, "una vecina, según WLRN (2013) · también dijo «Deco schmeco»", 1300, 430, "inter", 28, INK, pd * 0.85, align="center")
    pc = fin(t, tc - 0.2, 0.6)
    if pc > 0:  # flechas: el cuerpo de uno pasa a los detalles del siguiente
        rect(c, 0, 0, W, H, "#000000", 0.25 * pc)
        xs = [70 + sum(h["w"] + 24 for h in HOTELS[:i]) for i in range(4)]
        for i in range(3):
            q = fin(t, tc + i * 0.5, 0.6); x0 = xs[i] + HOTELS[i]["w"] * 0.5; x1 = xs[i + 1] + HOTELS[i + 1]["w"] * 0.5
            col = hotel_colors("pastel", i)["body"]
            pth = skia.Path(); pth.moveTo(x0, 470); pth.quadTo((x0 + x1) / 2, 230, x1, 300)
            c.drawPath(partial_path(pth, q), paint("#FFFFFF", 0.9, stroke=14)); c.drawPath(partial_path(pth, q), paint(col, 1, stroke=8))
            if q > 0.95: circle(c, x1, 300, 18, col); circle(c, x1, 300, 18, "#FFFFFF", 1, stroke=4)
        label(c, W / 2, 120, "CUERPO DE UNO = DETALLES DEL SIGUIENTE", pc, INK, 38, bg="#FFFFFF", align="center")
    pu = pop(t, tu - 0.1, 0.5)
    if pu > 0:
        c.save(); c.translate(W / 2, 960); c.scale(pu, pu)
        rect(c, -420, -70, 840, 110, INK, 0.85, r=14); draw_text(c, "UNA SOLA PIEZA", 0, 10, "abril", 70, PASTEL["rosa"], 1, align="center"); c.restore()

def sc_today(c, t, info, ctx):
    to = info.w("obligatorio"); th = info.w("como si fuera histórica")
    street(c, t, "pastel", cam=20 + t * 3, cars=True)
    if t > to - 0.05:
        rect(c, 0, 0, W, H, "#FFFFFF", 0.45 * fin(t, to - 0.05, 0.3))
        stamp(c, W / 2, 360, ["HOY: OBLIGATORIO", "TONOS PASTEL CLAROS"], t - to, col="#7A1E48", rot=-6, size=64)
    source_chip(c, 90, 980, "Servicio de Parques Nacionales (NPS), 2018", fin(t, to, 0.5))
    ph = pop(t, th - 0.1, 0.5)
    if ph > 0:
        c.save(); c.translate(W / 2, 650); c.rotate(4); c.scale(ph, ph)
        rect(c, -430, -80, 860, 140, "#FFF4DD", 0.97, r=10); rect(c, -430, -80, 860, 140, "#8E2A1E", 1, r=10, stroke=5)
        draw_text(c, "«HISTÓRICO» DESDE 1980", 0, 18, "abril", 64, "#8E2A1E", 1, align="center"); c.restore()

# ====================================================================== CAPA 5 · 1984
def living(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, ["#2B1B3D", "#4A2A55"]))
    for k in range(7): rect(c, 0, k * 160, W, 80, "#FFFFFF", 0.025)
    rect(c, 0, 880, W, 200, "#3A2233")
    palm(c, 120, 900, 380, "#1C1028"); palm(c, 1800, 900, 420, "#1C1028", 0.3)

def tv_content(cc, x, y, w, h, t):
    cc.save(); cc.translate(x, y); cc.scale(w / W, h / H); street(cc, t, "pastel", cam=t * 8, sky_mode="dusk"); cc.restore()

def sc_tv(c, t, info, ctx):
    tn = info.w("NBC"); tmn = info.w("Michael Mann"); tt = info.w("nada de tonos tierra"); t2 = info.w("con dos colores"); t3 = info.w("con tres")
    living(c, t)
    on = prog(t, 0.9, 1.5)
    crt(c, 360, 150, 1200, 680, t, tv_content, on=on)
    pn = fin(t, tn - 0.2, 0.5) * (1 - fin(t, tt - 0.4, 0.4))
    label(c, 380, 110, "16 · SEP · 1984 · NBC ESTRENA MIAMI VICE", pn, "#FFFFFF", 30, bg="#000000")
    pm = fin(t, tmn - 0.2, 0.5) * (1 - fin(t, tt - 0.4, 0.4))
    if pm > 0: name_card(c, 1160, 860, "Michael Mann", "productor ejecutivo", t - tmn + 0.2, col=PASTEL["aqua"], a=pm, w=600)
    pt = fin(t, tt - 0.2, 0.5) * (1 - fin(t, t2 - 0.3, 0.4))
    if pt > 0:
        rect(c, 0, 0, W, H, "#000000", 0.5 * pt)
        draw_text(c, "NADA DE TONOS TIERRA", W / 2, 260, "abril", 96, "#FFFFFF", pt, align="center")
        for i, (nm, col) in enumerate((("marrón", "#7B4B2A"), ("beige", "#CDB891"), ("óxido", "#9A4A2A"))):
            x = 420 + i * 380; swatch(c, x, 380, 320, 200, col, nm, pt, "#FFFFFF", 28); xmark(c, x + 160, 480, 90, fin(t, tt + 0.3 + i * 0.3, 0.3))
    p2 = fin(t, t2 - 0.2, 0.5)
    if p2 > 0:
        rect(c, 0, 0, W, H, "#000000", 0.55 * p2)
        for i, col in enumerate((PASTEL["rosa"], PASTEL["aqua"])): swatch(c, 300 + i * 200, 360, 170, 260, col, None, p2)
        draw_text(c, "= nada", 760, 520, "abril", 80, "#FFFFFF", p2)
        p3 = fin(t, t3 - 0.1, 0.5)
        for i, col in enumerate((PASTEL["rosa"], PASTEL["aqua"], PASTEL["crema"])): swatch(c, 1060 + i * 200, 360, 170, 260, col, None, p3)
        draw_text(c, "= una historia", 1100, 720, "abril", 80, YEL, p3)
        source_chip(c, 300, 900, "Michael Mann a Los Angeles Times (1987), vía Mental Floss", p2)
    chapter_header(c, t, 5, "1984", "LA TELEVISIÓN", "#FFFFFF", info.d)

def tv_wall(cc, x, y, w, h, t, rp, carts):
    cc.save(); cc.translate(x, y); cc.scale(w / W, h / H)
    sky(cc, "dusk", t, hy=H)
    rect(cc, 200, 160, 1520, 760, "#CDB891");
    if rp > 0:
        cc.save(); cc.clipRect(skia.Rect.MakeXYWH(200, 160, 1520 * rp, 760)); rect(cc, 200, 160, 1520, 760, PASTEL["rosa"]); cc.restore()
        rect(cc, 200 + 1520 * rp - 30, 140, 60, 800, "#FFFFFF", 0.6 * (1 - rp))
    for k in range(5): rect(cc, 300 + k * 290, 300, 160, 260, "#3B4E66", 0.9, r=6)
    if carts > 0:
        for k in range(3):
            xx = 330 + k * 520; cols = [PASTEL["menta"], PASTEL["crema"], PASTEL["pervinca"]]
            rect(cc, xx, 760, 300, 140, cols[k], carts, r=12); circle(cc, xx + 60, 910, 26, "#333333", carts); circle(cc, xx + 240, 910, 26, "#333333", carts)
            c_ = poly([(xx - 30, 700), (xx + 150, 620), (xx + 330, 700)]); cc.drawPath(c_, paint(PASTEL["rosa"], carts))
    cc.restore()

def sc_tv2(c, t, info, ctx):
    tr = info.w("repintaba"); tc = info.w("carritos"); tl = info.w("Leonard Horowitz")
    living(c, t)
    rp = ease_io(prog(t, tr - 0.1, tr + 1.4)); carts = fin(t, tc - 0.2, 0.6)
    crt(c, 360, 150, 1200, 680, t, lambda cc, x, y, w, h, tt: tv_wall(cc, x, y, w, h, tt, rp, carts))
    source_chip(c, 380, 950, "Servicio de Parques Nacionales (NPS), 2018", fin(t, tc, 0.5))
    pl = pop(t, tl - 0.1, 0.5)
    if pl > 0:
        c.save(); c.translate(W / 2, 520); c.scale(pl, pl)
        rect(c, -560, -90, 1120, 160, "#000000", 0.8, r=16); draw_text(c, "LEONARD HOROWITZ", 0, 22, "abril", 92, PASTEL["rosa"], 1, align="center"); c.restore()

def sc_coda(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, ["#070814", "#141634", "#1F1C3A"]))
    for k in range(120):
        rng = np.random.default_rng(k); circle(c, rng.random() * W, rng.random() * 420, 1.3, "#FFFFFF", 0.3 + 0.3 * math.sin(t + k))
    # la fila de hoteles a lo lejos, iluminada
    c.save(); c.translate(W * 0.18, 300); c.scale(0.38, 0.38)
    hotel_row(c, t, "night", yb=700, x0=70, s=1.0, neon=0.9, lights=1.0); c.restore()
    hy = 570; c.drawRect(skia.Rect.MakeXYWH(0, hy, W, H - hy), lin_grad(0, hy, 0, H, ["#1D2147", "#0A0B1A"]))
    for k in range(40):  # reflejos
        rng = np.random.default_rng(300 + k); x = W * 0.2 + rng.random() * W * 0.6; y = hy + 10 + rng.random() * 260
        line(c, x, y, x + 30 + 30 * rng.random(), y, [NEON["rosa"], NEON["cian"], NEON["menta"], "#FFD9A0"][k % 4], 0.25 * (0.6 + 0.4 * math.sin(t * 2 + k)), 3)
    # bote y partículas
    bx = 1360 + 10 * math.sin(t * 0.7); by = 880 + 6 * math.sin(t * 1.1)
    c.drawPath(poly([(bx - 170, by), (bx + 170, by), (bx + 120, by + 60), (bx - 130, by + 60)]), paint("#05060D"))
    rect(c, bx - 40, by - 70, 80, 70, "#05060D")
    for k in range(60):
        rng = np.random.default_rng(500 + k); life = (t * 0.25 + rng.random()) % 1.0
        x = bx - 120 - life * 260 + 30 * math.sin(life * 6 + k); y = by - 40 + life * 120
        circle(c, x, y, 2.2, "#FFF3D6", 0.6 * (1 - life))
    p = fin(t, 1.0, 1.2) * (1 - fin(t, info.d - 1.2, 1.0))
    draw_text(c, "Leonard Horowitz", W / 2, 180, "dmserifi", 70, "#FFFFFF", p, align="center")
    draw_text(c, "murió en 1989, a los 43 años", W / 2, 245, "inter", 34, "#FFFFFF", 0.8 * p, align="center")
    source_chip(c, 80, 980, "WLRN (2013)", p)

# ====================================================================== CAPA 6 · 2002
def topdown_city(cc, t):
    """Ciudad abstracta vista desde arriba (no reproduce ningún mapa real ni del juego)."""
    cc.drawRect(skia.Rect.MakeWH(W, H), paint("#2F6B3E"))
    cc.drawRect(skia.Rect.MakeXYWH(1560, 0, W - 1560, H), paint("#2C6BB0"))
    for k in range(20): cc.drawRect(skia.Rect.MakeXYWH(1560 + (k % 2) * 6, k * 56, 10, 30), paint("#E8D9A8"))
    cc.drawRect(skia.Rect.MakeXYWH(1480, 0, 80, H), paint("#E8D9A8"))
    cols = ["#C9B8A0", "#B8A890", "#D8C8B0", "#A89880", "#E3B7C4", "#B7E0CF"]
    for i in range(9):
        for j in range(7):
            x = 40 + i * 160; y = 40 + j * 150
            cc.drawRect(skia.Rect.MakeXYWH(x, y, 120, 110), paint(cols[(i * 3 + j) % len(cols)]))
            cc.drawRect(skia.Rect.MakeXYWH(x + 14, y + 14, 92, 82), paint("#000000", 0.12))
    for i in range(10): cc.drawRect(skia.Rect.MakeXYWH(i * 160, 0, 40, H), paint("#3A3A3A"))
    for j in range(8): cc.drawRect(skia.Rect.MakeXYWH(0, j * 150, 1480, 40), paint("#3A3A3A"))
    for i in range(10):
        for k in range(14): cc.drawRect(skia.Rect.MakeXYWH(i * 160 + 18, k * 80 + 20, 4, 30), paint("#E8E3D3", 0.6))
    for k in range(30):
        rng = np.random.default_rng(k); cc.drawCircle(1500 + rng.random() * 50, rng.random() * H, 10, paint("#1F5A2E"))
    for k in range(4):
        y = 150 * (k + 1) + 8; x = (t * (180 + 40 * k) + k * 400) % 1480
        cc.drawRect(skia.Rect.MakeXYWH(x, y, 46, 24), paint(["#FF4FA3", "#FFFFFF", "#3FF5FF", "#FFC14D"][k]))

def sc_game(c, t, info, ctx):
    t97 = info.w("1997"); t02 = info.w("llegó en 2002"); t86 = info.w("1986")
    k = fin(t, t02 - 0.2, 0.5)
    if k < 1:
        layer_alpha(c, 1 - k, lambda: (pixelated(c, topdown_city, 10, t=t), label(c, 80, 120, "1997 · VICE CITY, VISTA DESDE ARRIBA", fin(t, t97 - 0.2, 0.5), "#FFFFFF", 34, bg="#000000")))
    if k > 0:
        def g(): pixelated(c, lambda cc, tt: street(cc, tt, "pixel", cam=tt * 10, neon=1.0, lights=1.0), 5, t=t)
        layer_alpha(c, k, g)
        p86 = fin(t, t86 - 0.2, 0.5)
        rect(c, 1500, 60, 360, 110, "#000000", 0.6 * k, r=10)
        draw_text(c, "1986", 1680, 145, "vt323", 100, "#7CFFC4", max(k * 0.35, p86), align="center")
        label(c, 80, 120, "2002 · AMBIENTADO EN 1986", k, "#FFFFFF", 34, bg="#000000")
        draw_text(c, "recreación ilustrada · no es una captura del juego", 80, 1040, "ovmono", 22, "#FFFFFF", 0.7 * k)
    chapter_header(c, t, 6, "2002", "EL VIDEOJUEGO", "#FFFFFF", info.d)

def sc_game2(c, t, info, ctx):
    tv = info.w("veía Miami Vice"); tg = info.w("Aaron Garbut"); tl = info.w("Lance Vance"); tf = info.w("Fíjate")
    ti = info.w("imita"); tfi = info.w("filmó"); tp = info.w("pintó")
    pixelated(c, lambda cc, tt: street(cc, tt, "pixel", cam=40 + tt * 10, neon=1.0, lights=1.0), 5, t=t)
    rect(c, 0, 0, W, H, "#0A0716", 0.55 + 0.25 * fin(t, tf - 0.3, 0.5))
    pc = 1 - fin(t, tf - 0.4, 0.4)
    cards = [("EL EQUIPO VEÍA MIAMI VICE", "mientras desarrollaba el juego", tv), ("AARON GARBUT · DIRECTOR DE ARTE", "usó la serie como referencia para el neón", tg),
             ("LANCE VANCE  ←  PHILIP MICHAEL THOMAS", "el actor de Tubbs en Miami Vice le puso la voz", tl)]
    for i, (a_, b_, tt) in enumerate(cards):
        q = fin(t, tt - 0.2, 0.5) * pc
        if q <= 0: continue
        y = 200 + i * 220; rect(c, 160, y + (1 - q) * 30, 1600, 170, "#000000", 0.7 * q, r=14); rect(c, 160, y + (1 - q) * 30, 12, 170, NEON["cian"], q)
        draw_text(c, a_, 210, y + 75 + (1 - q) * 30, "ovblk", 52, "#FFFFFF", q); draw_text(c, b_, 212, y + 130 + (1 - q) * 30, "inter", 32, "#FFFFFF", 0.8 * q)
    if pc > 0: source_chip(c, 160, 900, "Wikipedia: «Grand Theft Auto: Vice City» y entrevistas citadas · GamesRadar+", fin(t, tv, 0.5) * pc)
    pf = fin(t, tf - 0.2, 0.5)
    if pf > 0:
        boxes = [("JUEGO", "2002", NEON["cian"]), ("SERIE", "1984", PASTEL["aqua"]), ("PALETA", "1980", PASTEL["rosa"]), ("EDIFICIOS BLANCOS", "AÑOS 30", "#F2EFE6")]
        lights = [tf, ti, tfi, tp]
        for i, (nm, yr, col) in enumerate(boxes):
            q = fin(t, lights[i] - 0.1, 0.4); x = 110 + i * 450; y = 400
            rect(c, x, y, 380, 240, col, 0.25 + 0.75 * q, r=16); rect(c, x, y, 380, 240, "#FFFFFF", q, r=16, stroke=4)
            draw_text(c, nm, x + 190, y + 110, "ovblk", 40 if len(nm) < 10 else 30, INK, 0.4 + 0.6 * q, align="center")
            draw_text(c, yr, x + 190, y + 180, "monoton", 50, INK, 0.4 + 0.6 * q, align="center")
            if i < 3:
                qa = fin(t, lights[i + 1] - 0.2, 0.3); line(c, x + 390, y + 120, x + 390 + 50 * qa, y + 120, "#FFFFFF", 1, 8)
                if qa > 0.9: c.drawPath(poly([(x + 445, y + 104), (x + 445, y + 136), (x + 462, y + 120)]), paint("#FFFFFF"))
        draw_text(c, "una cadena de copias", W / 2, 780, "dmserifi", 56, "#FFFFFF", pf, align="center")

# ====================================================================== CAPA 7 · 2026
def sc_2026(c, t, info, ctx):
    tg = info.w("Según Aaron Garbut"); tv = info.w("Hotel Victor"); td = info.w("Hotel Dixon"); tm = info.w("Como L. Murray Dixon")
    zoomed(c, 1.0 + 0.01 * t, W / 2, H * 0.5, lambda: street(c, t, "night", cam=t * 5, neon=1.0, lights=1.0))
    pg = fin(t, tg - 0.2, 0.5) * (1 - fin(t, tv - 0.4, 0.4))
    if pg > 0:
        quote_card(c, 160, 220, 1600, "Recorrieron el sur de Florida e investigaron la historia y la arquitectura de Miami.",
                   sub="Aaron Garbut (Rockstar), citado por la agencia AP", src="FUENTE · AP vía WLRN, 17/11/2026", t=1.0, a=pg, size=48)
    pv = fin(t, tv - 0.2, 0.5)
    if pv > 0:
        rect(c, 0, 0, W, H, "#000000", 0.45 * pv)
        c.save(); c.translate(560, 420); c.scale(pv, pv)
        rect(c, -380, -120, 760, 240, "#F2EFE6", 1, r=12); draw_text(c, "HOTEL VICTOR", 0, -10, "abril", 80, INK, 1, align="center")
        draw_text(c, "Ocean Drive · 1937 · el hotel real", 0, 70, "inter", 34, INK, 0.8, align="center"); c.restore()
        pdx = fin(t, td - 0.1, 0.5)
        if pdx > 0:
            line(c, 960, 420, 960 + 120 * pdx, 420, "#FFFFFF", 1, 8)
            if pdx > 0.95: c.drawPath(poly([(1080, 396), (1080, 444), (1110, 420)]), paint("#FFFFFF"))
            fl = 1.0 if t > td + 0.5 else (1.0 if math.sin((t - td) * 50) > 0 else 0.3)
            c.save(); c.translate(1460, 420); c.scale(pdx, pdx)
            rect(c, -340, -120, 680, 240, "#120A1E", 0.9, r=12)
            draw_text(c, "HOTEL DIXON", 0, 30, "monoton", 84, NEON["rosa"], fl, align="center", glow=(NEON["rosa"], 20))
            draw_text(c, "su versión en Vice City (tráiler 1)", 0, 100, "inter", 30, "#FFFFFF", 0.8, align="center"); c.restore()
        pm = fin(t, tm - 0.2, 0.5)
        if pm > 0:
            name_card(c, 560, 640, "L. Murray Dixon", "el arquitecto del Hotel Victor (1937)", t - tm + 0.2, col=NEON["rosa"], a=pm, w=800)
            source_chip(c, 560, 820, "Axios (2023) · Miami New Times · AP (2026)", pm)
    chapter_header(c, t, 7, "2026", "LAS PANTALLAS", "#FFFFFF", info.d)

def sc_vintage(c, t, info, ctx):
    tv = info.w("Vintage Vice City"); tg = info.w("guiños")
    street(c, t, "night", cam=40 + t * 5, neon=1.0, lights=1.0); rect(c, 0, 0, W, H, "#0A0716", 0.55)
    pq = fin(t, tv - 0.2, 0.5)
    quote_card(c, 160, 200, 1600, "Para volver a cuando el neón brillaba más.", sub="Descripción del paquete Vintage Vice City, bono de reserva (traducción)",
               src="FUENTE · rockstargames.com/VI · consultado el 18/11/2026", t=1.0, a=pq, size=60)
    cert_tag(c, 160, 120, "OFICIAL", pq, 30, t=1.0)
    pg = fin(t, tg - 0.6, 0.6)
    for i, (nm, sub) in enumerate((("OCEAN VIEW HOTEL", "nombre de hotel de Vice City (2002)"), ("VERCETTI", "apellido del protagonista de 2002"))):
        q = pop(t, tg - 1.2 + i * 0.4, 0.45)
        if q <= 0: continue
        x = 260 + i * 760; y = 640
        c.save(); c.translate(x + 330, y + 90); c.scale(q, q); c.translate(-(x + 330), -(y + 90))
        rect(c, x, y, 660, 180, "#120A1E", 0.9, r=14); rect(c, x, y, 660, 180, NEON["cian"], 1, r=14, stroke=4)
        draw_text(c, nm, x + 330, y + 85, "ovblk", 52, "#FFFFFF", 1, align="center"); draw_text(c, sub, x + 330, y + 140, "inter", 28, "#FFFFFF", 0.8, align="center")
        c.restore()
    if pg > 0: label(c, W / 2, 900, "= GUIÑOS A 2002", pg, INK, 40, bg=NEON["cian"], align="center")

_BG = {}
def phone_content(kind, img):
    def f(cc, x, y, w, h, t):
        sx = 200 + kind * 380; src = skia.Rect.MakeXYWH(sx, 120, 520, 1040 * 0.95)
        cc.drawImageRect(img, src, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kLinear))
    return f

def sc_phones(c, t, info, ctx):
    tg = info.w("grabando"); ts = info.w("selfi"); tv = info.w("virales"); tl = info.w("nuestra lectura")
    if "s" not in _BG: _BG["s"] = new_surface(W, H)
    bc = _BG["s"].getCanvas(); street(bc, t, "night", cam=60 + t * 5, neon=1.0, lights=1.0); img = _BG["s"].makeImageSnapshot()
    c.drawImage(img, 0, 0)
    rect(c, 0, 0, W, H, "#000000", 0.25)
    pts = [(170, 260), (620, 210), (1080, 250), (1530, 230)]
    for i, (x, y) in enumerate(pts):
        q = pop(t, tg + i * 0.35, 0.45) * (1 - fin(t, tl - 0.4, 0.4))
        if q <= 0: continue
        c.save(); c.translate(x + 140, y + 280); c.rotate((-1) ** i * 4); c.scale(q, q); c.translate(-(x + 140), -(y + 280))
        phone_frame(c, x, y, 280, 560, t + i, 1.0, phone_content(i, img)); c.restore()
    if t > ts:
        pf = fin(t, ts, 0.15) * (1 - fin(t, ts + 0.2, 0.4)); rect(c, 0, 0, W, H, "#FFFFFF", 0.6 * pf)
        label(c, 620, 820, "SELFI", fin(t, ts, 0.4) * (1 - fin(t, tl - 0.4, 0.4)), INK, 34, bg="#FFFFFF")
    pv = fin(t, tv - 0.2, 0.5) * (1 - fin(t, tl - 0.4, 0.4))
    if pv > 0:
        n = int(1000 + 2_400_000 * ease_in(prog(t, tv, tv + 3)))
        label(c, 1080, 900, f"▶ {n:,} VISTAS".replace(",", "."), pv, "#FFFFFF", 38, bg="#C2185B")
    plq = fin(t, tl - 0.1, 0.5)
    if plq > 0:
        rect(c, 0, 0, W, H, "#000000", 0.55 * plq)
        cert_tag(c, W / 2, 330, "INTERPRETACIÓN", 1.0, 40, align="center", t=plq)
        kinetic_words(c, "EN 2026, LA BROCHA DE VICE CITY ES LA CÁMARA DEL CELULAR", W / 2, 520, t - tl, "abril", 86, "#FFFFFF", accent=NEON["rosa"],
                      accent_words=("CÁMARA", "CELULAR"), align="center", maxw=1500)
        draw_text(c, "Lectura del canal a partir de las imágenes oficiales (celulares en alto, selfis, videos virales)", W / 2, 880, "inter", 28, "#FFFFFF", 0.75 * plq, align="center")

def arena(c, t, sign_on):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, ["#07061A", "#21123F", "#3A1A55"]))
    for k in range(10):
        x = 60 + k * 190; hh = 220 + (k * 73) % 260; rect(c, x, 760 - hh, 120, hh, "#120D24")
        for j in range(int(hh / 40)):
            for i in range(3): rect(c, x + 14 + i * 36, 760 - hh + 18 + j * 40, 18, 16, "#FFD9A0", 0.35 if (i + j + k) % 3 else 0.05)
    pth = skia.Path(); pth.addOval(skia.Rect.MakeXYWH(260, 600, 1400, 330)); c.drawPath(pth, paint("#1C1A2A"))
    pth2 = skia.Path(); pth2.addOval(skia.Rect.MakeXYWH(320, 560, 1280, 250)); c.drawPath(pth2, paint("#2A2740"))
    rect(c, 260, 760, 1400, 260, "#1C1A2A")
    for k in range(14): rect(c, 300 + k * 96, 820, 50, 150, NEON["cian"], 0.15 + 0.1 * math.sin(t * 2 + k))
    if sign_on > 0:
        fl = 1.0 if sign_on >= 1 else (1.0 if math.sin(t * 60) > 0 else 0.2)
        draw_text(c, "WELCOME TO VICE CITY", W / 2, 690, "monoton", 108, NEON["rosa"], fl * sign_on, align="center", glow=(NEON["rosa"], 24))
        c.drawRect(skia.Rect.MakeXYWH(200, 500, 1520, 300), rad_grad(W / 2, 650, 800, [hexc(NEON["rosa"], 0.18 * sign_on), hexc(NEON["rosa"], 0)]))

def sc_loop(c, t, info, ctx):
    tm = info.w("3,9 millones"); tw = info.w("Welcome to Vice City"); tv = info.w("se viste"); to = info.w("No a todos")
    arena(c, t, fin(t, tw - 0.1, 0.6))
    pm = fin(t, tm - 0.2, 0.5) * (1 - fin(t, to - 0.4, 0.4))
    if pm > 0:
        label(c, 120, 110, "MIAMI-DADE × ROCKSTAR · 3,9 MILLONES DE DÓLARES", pm, INK, 38, bg=YEL)
        source_chip(c, 120, 200, "Agencia AP vía WLRN, 17/11/2026", pm)
    pv = fin(t, tv - 0.2, 0.6) * (1 - fin(t, to - 0.4, 0.4))
    draw_text(c, "la ciudad real se viste de ciudad ficticia", W / 2, 1020, "dmserifi", 52, "#FFFFFF", pv, align="center")
    draw_text(c, "ilustración genérica · no es el edificio real", W - 40, 1060, "ovmono", 20, "#FFFFFF", 0.6, align="right")
    po = fin(t, to - 0.2, 0.5)
    if po > 0:
        for i, txt in enumerate(("LA SHERIFF DEL CONDADO: EN CONTRA", "UN COMISIONADO DE MIAMI BEACH: EN CONTRA")):
            label(c, 120, 120 + i * 90, txt, fin(t, to + i * 0.5, 0.4), "#FFFFFF", 34, bg="#8E2A1E")

# ====================================================================== EL PRECIO DEL PASTEL
def chair(c, x, yb, s, col="#E9E2D0"):
    c.save(); c.translate(x, yb); c.scale(s, s)
    line(c, -60, 0, 40, -150, col, 1, 10); line(c, 60, 0, -40, -150, col, 1, 10)
    rect(c, -70, -150, 140, 22, col, 1, r=6); rect(c, -70, -300, 26, 170, col, 1, r=6); rect(c, 44, -300, 26, 170, col, 1, r=6)
    for k in range(4): rect(c, -60, -290 + k * 34, 120, 18, "#F7B7C8" if k % 2 == 0 else "#FFFFFF", 1, r=4)
    c.restore()

def sc_price(c, t, info, ctx):
    ts = info.w("salvó"); tv = info.w("vecinos"); tn = info.w("Servicio"); th = info.w("El hijo de Barbara Capitman"); tp = info.w("Para nosotros")
    street(c, t, "pastel", cam=t * 2, cars=False); rect(c, 0, 0, W, H, "#FFFFFF", 0.18)
    chair(c, 1500, 1040, 1.6)
    p1 = fin(t, ts - 0.2, 0.6) * (1 - fin(t, th - 0.4, 0.4))
    rect(c, 80, 130, 1320, 330, "#FFFFFF", 0.82 * p1, r=18)
    draw_text(c, "El pastel salvó los edificios…", 120, 220, "abril", 76, INK, p1, shadow=(0, 3, 10, "#FFFFFF", 0.9))
    p2 = fin(t, tv - 0.2, 0.6) * (1 - fin(t, th - 0.4, 0.4))
    draw_text(c, "…pero no a todos sus vecinos", 120, 320, "abril", 76, "#7A1E48", p2, shadow=(0, 3, 10, "#FFFFFF", 0.9))
    if t > tn: source_chip(c, 120, 380, "Servicio de Parques Nacionales (NPS), 2018", fin(t, tn, 0.5) * (1 - fin(t, th - 0.4, 0.4)))
    ph = fin(t, th - 0.2, 0.6) * (1 - fin(t, tp - 0.4, 0.4))
    if ph > 0:
        quote_card(c, 120, 200, 1200, "¿Cómo pasó eso? ¿Era eso lo que queríamos?", sub="John Capitman, hijo de Barbara Capitman (traducción)",
                   src="FUENTE · National Trust for Historic Preservation, 2014", t=1.0, a=ph, size=56, col="#FFFFFF", bg="#2B1B3D")
    pp = fin(t, tp - 0.1, 0.5)
    if pp > 0:
        rect(c, 0, 0, W, H, "#1A1424", 0.55 * pp)
        cert_tag(c, 120, 200, "INTERPRETACIÓN", 1.0, 34, t=pp)
        kinetic_words(c, "UNA CIUDAD QUE SE BURLA DEL EXCESO… Y QUE NACIÓ DE ÉL", 120, 420, t - tp, "abril", 90, "#FFFFFF", accent=PASTEL["rosa"],
                      accent_words=("EXCESO…", "NACIÓ"), maxw=1300)

# ====================================================================== GUÍA DE CAMPO
GUIDE = [("cejas", "CEJAS", "w:cejas"), ("ojo", "OJOS DE BUEY", "w:ojos de buey"), ("tres", "DE TRES EN TRES", "w:de tres en tres"),
         ("vidrio", "BLOQUES DE VIDRIO", "w:bloques de vidrio"), ("esquina", "ESQUINAS REDONDEADAS", "w:esquinas redondeadas"), ("neon", "NEÓN VERTICAL", "w:letreros verticales")]
def sc_guide(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, ["#16181B", "#2A1F38"])); grid(c, W, H, 48, "#FFFFFF", 0.035)
    pt = fin(t, 0.2, 0.6)
    c.save(); c.translate(W / 2, 120); c.scale(pt, pt); guide_sign(c, -560, -70, 1120, 130); draw_text(c, "TU MISIÓN EN OCEAN BEACH", 0, 18, "ovblk", 60, SAL, 1, align="center"); c.restore()
    for i, (ic, nm, cue) in enumerate(GUIDE):
        tt = info.w(cue[2:]); q = pop(t, 0.6 + i * 0.12, 0.5)
        if q <= 0: continue
        x = 150 + (i % 3) * 560; y = 260 + (i // 3) * 360; on = fin(t, tt - 0.1, 0.4)
        c.save(); c.translate(x + 250, y + 150); c.scale(q, q); c.translate(-(x + 250), -(y + 150))
        rect(c, x, y, 500, 300, "#000000", 0.45, r=18); rect(c, x, y, 500, 300, YEL if on > 0 else "#FFFFFF", 0.35 + 0.65 * on, r=18, stroke=4)
        deco_icon(c, ic, x + 130, y + 140, 120, PASTEL["rosa"] if on > 0 else "#FFFFFF", 0.6 + 0.4 * on)
        draw_text(c, nm, x + 250, y + 260, "ovblk", 34 if len(nm) < 16 else 28, "#FFFFFF", 1, align="center")
        check_box(c, x + 380, y + 90, 80, on); c.restore()
    th = info.w("hizo la tarea")
    if t > th - 0.05: stamp(c, W / 2, 1000, ["ROCKSTAR HIZO LA TAREA"], t - th, col=PAL["verde"], rot=-4, size=50)

# ====================================================================== CIERRE
COPIES = [("Una tormenta", "1926"), ("un estilo barato", "AÑOS 30"), ("una activista", "1976"), ("un diseñador", "1980"), ("una serie", "1984"), ("un estudio", "2002 · 2026")]
def sc_close(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, ["#16181B", "#2A1F38"]))
    tc = info.w("una copia de una copia"); tz = info.w("capa de pintura")
    cross_section(c, 140, 160, 520, 760, 7, t, labels=True, scale_txt=1.35)
    pc = fin(t, tc - 0.2, 0.6)
    if pc > 0:
        draw_text(c, "UNA COPIA DE UNA COPIA", 760, 230, "abril", 76, "#FFFFFF", pc)
        draw_text(c, "DE UNA COPIA", 760, 320, "abril", 76, PASTEL["rosa"], pc)
    for i, (frag, yr) in enumerate(COPIES):
        tt = info.w(frag); q = fin(t, tt - 0.1, 0.4)
        if q <= 0: continue
        y = 410 + i * 82; rect(c, 760, y, 1000, 66, "#000000", 0.4 * q, r=10)
        txt = {0: "una tormenta", 1: "un estilo barato", 2: "una activista tenaz", 3: "un diseñador con una carta de colores", 4: "una serie de televisión", 5: "un estudio de videojuegos"}[i]
        draw_text(c, txt, 790, y + 46, "intersb", 36, "#FFFFFF", q); draw_text(c, yr, 1740, y + 46, "ovmono", 30, YEL, q, align="right")
    pz = fin(t, tz - 0.2, 0.6)
    if pz > 0:
        for i in range(7):  # brillo que recorre las capas
            lh = 760 / 7; yy = 160 + 760 - (i + 1) * lh; a = clamp(pz * 7 - i) * (0.5 + 0.5 * math.sin(t * 4 - i))
            rect(c, 140, yy, 520, lh - 2, "#FFFFFF", 0.18 * a)

def sc_cta(c, t, info, ctx):
    tc = info.w("comentarios"); ts = info.w("suscríbete")
    zoomed(c, 1.04, W / 2, H / 2, lambda: street(c, t, "night", cam=t * 4, neon=1.0, lights=1.0))
    rect(c, 0, 0, W, H, "#000000", 0.35)
    pc = fin(t, tc - 0.3, 0.6)
    if pc > 0:
        rect(c, 220, 220, 1480, 260, "#000000", 0.65 * pc, r=20); icon(c, "chat", 340, 350, 120, YEL, pc)
        draw_text(c, "¿Cuál es la fachada más art déco", 440, 330, "abril", 66, "#FFFFFF", pc)
        draw_text(c, "que encontraste en el juego?", 440, 410, "abril", 66, PASTEL["rosa"], pc)
    ps = pop(t, ts - 0.1, 0.5)
    if ps > 0:
        c.save(); c.translate(W / 2, 700); c.scale(ps, ps)
        rect(c, -380, -70, 760, 130, YEL, 1, r=16); draw_text(c, "SUSCRÍBETE · CAPA POR CAPA", 0, 20, "ovblk", 48, INK, 1, align="center"); c.restore()

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "SIGUIENTE CAPA", "Más historias de Vice City, capa por capa", PASTEL["rosa"])

# ====================================================================== MINIATURA (1280 × 720)
def thumbnail(c):
    Wt, Ht = 1280, 720
    # fondo: izquierda cielo pálido (1936) · derecha atardecer (hoy)
    c.drawRect(skia.Rect.MakeXYWH(0, 0, 640, Ht), lin_grad(0, 0, 0, Ht, ["#D9E1E3", "#F4F2EC"]))
    c.drawRect(skia.Rect.MakeXYWH(640, 0, 640, Ht), lin_grad(0, 0, 0, Ht, ["#3A1A55", "#C2577E", "#FFB17A"]))
    spec = dict(name="MAREA", w=600, h=560, floors=3, top="tower", sign="left", eyebrows=True, fins=True, port=0, glass=False, corner=None, stripes=True)
    x, yb = 340, 690
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, 640, Ht)); facade(c, x, yb, spec, hotel_colors("white", 0), 0, "white"); c.restore()
    c.save(); c.clipRect(skia.Rect.MakeXYWH(640, 0, 640, Ht))
    colp = dict(hotel_colors("pastel", 0)); colp["sign"] = NEON["rosa"]
    facade(c, x, yb, spec, colp, 0, "pastel")
    c.restore()
    palm(c, 70, 720, 430, "#3C4A3E"); palm(c, 1180, 720, 470, "#2B1B3D", 0.4)
    # brochazo rosa con chorreones en la línea divisoria
    pth = skia.Path(); pth.moveTo(640, -20); pth.cubicTo(625, 200, 655, 430, 640, 740)
    c.drawPath(pth, paint(PASTEL["rosa"], 1, stroke=34)); c.drawPath(pth, paint("#FFFFFF", 0.55, stroke=5))
    for k, (dx, L) in enumerate(((-12, 60), (9, 95), (-4, 40))):
        line(c, 640 + dx, 330 + k * 40, 640 + dx, 330 + k * 40 + L, PASTEL["rosa"], 1, 12)
    # años
    rect(c, 40, 34, 230, 86, "#FFFFFF", 0.96, r=12); rect(c, 40, 34, 230, 86, INK, 1, r=12, stroke=4); draw_text(c, "1936", 155, 100, "abril", 70, INK, 1, align="center")
    rect(c, 1010, 34, 230, 86, PASTEL["rosa"], 0.98, r=12); draw_text(c, "1980", 1125, 100, "abril", 70, "#7A1E48", 1, align="center")
    # titular
    rect(c, 30, 470, 1220, 220, "#120E1E", 0.9, r=22)
    draw_text(c, "ANTES ERA BLANCO", 640, 588, "abril", 112, "#FFFFFF", 1, align="center")
    draw_text(c, "LA HISTORIA REAL DE LOS COLORES DE VICE CITY", 640, 660, "ovblk", 38, PASTEL["rosa"], 1, align="center")
    draw_badge(c, 1212, 425, 34)
