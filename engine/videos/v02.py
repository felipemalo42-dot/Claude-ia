"""VIDEO 02 — SHORT vertical: ¿A qué hora sale GTA 6 en tu país?
Lenguaje visual: globo 3D ortográfico (Natural Earth, dominio público) que gira siguiendo la medianoche;
cada país se 'enciende' cuando le llega su hora. Neón cian/magenta, tipografía Bebas/Anton, subtítulos palabra a palabra.
"""
import json, math, os, numpy as np, skia
from gfx import *
from components import *
from brand import PAL, draw_caiman

W, H = 1080, 1920
CY, R = 790, 395
CYAN = "#27D7F2"; MAG = "#FF4FA0"; GREEN = PAL["caiman"]; BG = "#070B16"

_GEO = None
def geo():
    global _GEO
    if _GEO is None:
        d = json.load(open(os.path.join(os.path.dirname(__file__), "..", "geo", "ne_110m_admin_0_countries.geojson")))
        out = []
        for f in d["features"]:
            name = f["properties"]["ADMIN"]; g = f["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            rings = []
            for p in polys:
                ring = np.array(p[0], float)
                lon, lat = np.radians(ring[:, 0]), np.radians(ring[:, 1])
                rings.append(np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], 1))
            out.append((name, rings))
        _GEO = out
    return _GEO

def rot_matrix(lon0, lat0):
    lo, la = math.radians(lon0), math.radians(lat0)
    Rz = np.array([[math.cos(-lo), -math.sin(-lo), 0], [math.sin(-lo), math.cos(-lo), 0], [0, 0, 1]])
    Ry = np.array([[math.cos(la), 0, math.sin(la)], [0, 1, 0], [-math.sin(la), 0, math.cos(la)]])
    return Ry @ Rz

def draw_globe(c, cx, cy, r, lon0, lat0, lit, t, pulses=()):
    """lit: dict país -> intensidad 0..1"""
    c.drawCircle(cx, cy, r * 1.25, rad_grad(cx, cy, r * 1.25, [hexc(CYAN, 0.22), hexc(CYAN, 0.0)], [0.75, 1]))
    c.drawCircle(cx, cy, r, rad_grad(cx - r * 0.3, cy - r * 0.3, r * 1.4, [hexc("#12305A"), hexc("#081428"), hexc("#040810")]))
    M = rot_matrix(lon0, lat0)
    # retícula
    for lon in range(-180, 180, 30):
        la = np.radians(np.linspace(-90, 90, 60)); lo = math.radians(lon)
        P = np.stack([np.cos(la) * math.cos(lo), np.cos(la) * math.sin(lo), np.sin(la)], 1) @ M.T
        vis = P[:, 0] > 0
        pts = [(cx + p[1] * r, cy - p[2] * r) for p, v in zip(P, vis) if v]
        if len(pts) > 1: c.drawPath(poly(pts, False), paint(CYAN, 0.10, stroke=1.2))
    for lat in range(-60, 90, 30):
        lo = np.radians(np.linspace(-180, 180, 120)); la = math.radians(lat)
        P = np.stack([math.cos(la) * np.cos(lo), math.cos(la) * np.sin(lo), np.full_like(lo, math.sin(la))], 1) @ M.T
        seg = []
        for p in P:
            if p[0] > 0: seg.append((cx + p[1] * r, cy - p[2] * r))
            elif len(seg) > 1: c.drawPath(poly(seg, False), paint(CYAN, 0.10, stroke=1.2)); seg = []
            else: seg = []
        if len(seg) > 1: c.drawPath(poly(seg, False), paint(CYAN, 0.10, stroke=1.2))
    for name, rings in geo():
        L = lit.get(name, 0.0)
        for ring in rings:
            P = ring @ M.T
            if (P[:, 0] <= 0).all(): continue
            Q = P.copy(); hidden = Q[:, 0] <= 0
            if hidden.any():  # proyectar puntos ocultos al borde
                n = np.linalg.norm(Q[hidden][:, 1:], axis=1, keepdims=True) + 1e-9
                Q[hidden, 1:] = Q[hidden][:, 1:] / n
            pts = [(cx + q[1] * r, cy - q[2] * r) for q in Q]
            pth = poly(pts)
            base = mixc("#1B3A5C", "#2BFF88", L) if L > 0 else hexc("#1A3354")
            c.drawPath(pth, paint(base))
            if L > 0: c.drawPath(pth, paint(GREEN, 0.5 * L, blur=8))
            c.drawPath(pth, paint("#7FD8FF" if L == 0 else "#CFFFE4", 0.35 + 0.4 * L, stroke=1.3))
    # pulsos (ondas desde el país que se desbloquea)
    for (lon, lat, p) in pulses:
        if not (0 < p < 1): continue
        v = np.array([math.cos(math.radians(lat)) * math.cos(math.radians(lon)), math.cos(math.radians(lat)) * math.sin(math.radians(lon)), math.sin(math.radians(lat))]) @ M.T
        if v[0] <= 0: continue
        x, y = cx + v[1] * r, cy - v[2] * r
        for k in range(3):
            pp = clamp(p * 1.4 - k * 0.2)
            if 0 < pp < 1: circle(c, x, y, 10 + 160 * pp, GREEN, (1 - pp) * 0.8, stroke=4)
        circle(c, x, y, 9, "#ffffff", 1)
    # brillo especular y borde
    c.drawCircle(cx - r * 0.35, cy - r * 0.4, r * 0.7, rad_grad(cx - r * 0.35, cy - r * 0.4, r * 0.7, [hexc("#ffffff", 0.10), hexc("#ffffff", 0)]))
    circle(c, cx, cy, r, CYAN, 0.6, stroke=3)

STOPS = [  # (frase clave, países, lon, lat, hora local, hora España)
    ("España", ["Spain"], -3.7, 40.4, "00:00", "00:00"),
    ("Argentina", ["Argentina", "Chile", "Uruguay", "Paraguay"], -64, -34, "00:00", "04:00"),
    ("Venezuela", ["Venezuela", "Bolivia", "Dominican Republic", "Puerto Rico"], -66, 8, "00:00", "05:00"),
    ("Colombia", ["Colombia", "Peru", "Ecuador", "Panama"], -74, 4.6, "00:00", "06:00"),
    ("México", ["Mexico", "Guatemala", "El Salvador", "Honduras", "Nicaragua", "Costa Rica"], -99, 19.4, "00:00", "07:00"),
    ("Estados Unidos", ["United States of America"], -98, 39, "00:00 ET", "06:00"),
]
LABEL = {"España": "ESPAÑA", "Argentina": "ARGENTINA · CHILE · URUGUAY · PARAGUAY", "Venezuela": "VENEZUELA · BOLIVIA · R. DOMINICANA",
         "Colombia": "COLOMBIA · PERÚ · ECUADOR · PANAMÁ", "México": "MÉXICO (CENTRO) · CENTROAMÉRICA", "Estados Unidos": "EE. UU. · COSTA ESTE (OESTE: 21:00 DEL 18)"}

def sc_main(c, t, info, ctx):
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [BG, "#0A1024", "#120A1E"]))
    bokeh(c, W, H, t, 20, (CYAN, MAG), seed=4, size=(10, 50), a=0.10, speed=20)
    # marcas de tiempo de cada parada
    cues = [(info.w(k, default=999) if k != "España" else info.w("España")) for k, *_ in STOPS]
    lit = {}; pulses = []; cur = None
    for (k, names, lon, lat, loc, es), ct in zip(STOPS, cues):
        p = prog(t, ct, ct + 0.6)
        if t >= ct: cur = (k, names, lon, lat, loc, es, ct)
        for n in names: lit[n] = max(lit.get(n, 0), ease_out(p))
        pulses.append((lon, lat, (t - ct) / 1.6))
    # rotación: interpolar hacia la parada actual
    lon0, lat0 = 20 - 6 * t, 25.0  # deriva inicial
    if cur:
        k, names, lon, lat, loc, es, ct = cur; idx = [s[0] for s in STOPS].index(k)
        prev = STOPS[idx - 1] if idx > 0 else (None, None, 10, 30)
        e = ease_io(prog(t, ct - 0.2, ct + 0.9))
        plon = prev[2] if idx > 0 else 20 - 6 * ct; plat = prev[3] if idx > 0 else 25
        lon0 = lerp(plon, lon, e); lat0 = lerp(plat, lat * 0.6, e)
    draw_globe(c, W / 2, CY, R, lon0, lat0, lit, t, pulses)
    # título
    tp = ease_out_back(prog(t, 0.0, 0.5))
    c.save(); c.translate(W / 2, 230); c.scale(tp, tp)
    draw_text(c, "¿A QUÉ HORA", 0, -40, "bebas", 150, "#FFFFFF", 1, align="center", tracking=4)
    draw_text(c, "SALE GTA VI?", 0, 100, "bebas", 150, CYAN, 1, align="center", tracking=4, glow=(CYAN, 18))
    c.restore()
    # regla
    rp = ease_out(prog(t, info.w("medianoche"), info.w("medianoche") + 0.5)) * (1 - prog(t, cues[0] - 0.4, cues[0]))
    if rp > 0:
        rect(c, 90, 1240, 900, 210, "#000000", 0.7 * rp, r=26); rect(c, 90, 1240, 900, 210, GREEN, rp, r=26, stroke=4)
        draw_text(c, "00:00", W / 2, 1360, "bebas", 150, GREEN, rp, align="center", glow=(GREEN, 12))
        draw_text(c, "HORA LOCAL · JUEVES 19 NOV", W / 2, 1425, "monob", 32, "#FFFFFF", rp, align="center", tracking=2)
    # tarjeta de la parada actual
    if cur:
        k, names, lon, lat, loc, es, ct = cur; p = ease_out_back(prog(t, ct, ct + 0.4))
        c.save(); c.translate(W / 2, 1345); c.scale(p, p); c.translate(-W / 2, -1345)
        rect(c, 70, 1230, 940, 235, "#050812", 0.85, r=26); rect(c, 70, 1230, 940, 235, GREEN, 1, r=26, stroke=4)
        lab = LABEL[k]; fs = 40 if len(lab) < 30 else 30
        draw_text(c, lab, W / 2, 1290, "monob", fs, "#FFFFFF", 1, align="center")
        draw_text(c, loc, 300, 1415, "bebas", 125, GREEN, 1, align="center")
        draw_text(c, "TU HORA", 300, 1450, "monob", 22, "#9FB3C8", 1, align="center", tracking=3)
        draw_text(c, es, 780, 1415, "bebas", 125, MAG, 1, align="center")
        draw_text(c, "EN ESPAÑA", 780, 1450, "monob", 22, "#9FB3C8", 1, align="center", tracking=3)
        rect(c, W / 2 - 1, 1320, 2, 130, "#ffffff", 0.2)
        c.restore()
        if k == "Estados Unidos": cert_tag(c, W / 2, 1180, "REPORTADO", 1, 24, align="center", t=prog(t, ct, ct + 0.4))
    # cierre
    s_end = info.w("ficha")
    pe = ease_out(prog(t, s_end, s_end + 0.4))
    if pe > 0:
        rect(c, 0, 1200, W, 300, BG, 0.95 * pe)
        icon(c, "check", 170, 1330, 80, GREEN, pe)
        draw_par(c, "Manda la ficha de TU tienda", 240, 1310, "bebas", 86, 760, color="#FFFFFF", a=pe, lh=0.95)
    sb = info.w("doscientos", default=999)
    pb = ease_out_back(prog(t, sb, sb + 0.4))
    if pb > 0:
        c.save(); c.translate(W / 2, 560); c.scale(pb, pb)
        rect(c, -300, -80, 600, 160, MAG, 1, r=80); draw_text(c, "210 GB LIBRES", 0, 30, "bebas", 96, "#000000", 1, align="center")
        c.restore()

def overlay(c, gt, ctx):
    short_captions(c, gt, ctx, y=1590, size=78, hl=GREEN, fontname="anton", maxw=960)
    draw_caiman(c, W / 2 - 150, 22, 0.36, lw=6, glow=True, a=0.9)
    draw_text(c, "CAIMÁN NEÓN", W / 2 - 66, 52, "monob", 24, "#FFFFFF", 0.8, tracking=3)

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("¿A qué hora sale GTA 6 en tu país? Sin tablas raras: la regla es una sola. "
     "Rockstar lo desbloquea a la medianoche, hora local, del jueves diecinueve de noviembre. "
     "La medianoche va a recorrer el mundo como una ola. "
     "En España llega a las cero horas del jueves. "
     "Cuatro horas después, Argentina y Chile. "
     "Una hora más tarde, Venezuela. "
     "Luego Colombia, Perú y Ecuador. "
     "Y casi al final, el centro de México y Centroamérica. "
     "En Estados Unidos abre a la medianoche de la costa este: en la costa oeste serán las nueve de la noche del miércoles. "
     "Si una tabla te dice otra cosa, manda la ficha de tu tienda. "
     "Y si todavía no tienes doscientos diez gigas libres... ya sabes qué hacer esta noche.",
     sc_main, energy=3, speed=1.08, pause_mul=0.7,
     sfx=[(0.0, "riser", 0.3), ("w:medianoche", "hit", 0.4), ("w:España", "pin", 0.6), ("w:Argentina", "pin", 0.6), ("w:Venezuela", "pin", 0.6),
          ("w:Colombia", "pin", 0.6), ("w:México", "pin", 0.6), ("w:Estados Unidos", "pin", 0.6), ("w:ficha", "pop", 0.5), ("w:doscientos", "hit", 0.5)])

VIDEO = dict(id="v02", folder="VIDEO_02", file="GTA6_hora_por_pais_SHORT", size=(W, H),
             title="¿A qué hora sale GTA 6 en tu país? (medianoche local, 19 de noviembre) #shorts",
             format="Short vertical (9:16)", music="electro", music_seed=21, voice="host", beats=B, overlay=overlay,
             lead_in=0.15, tail=1.2, music_gain=0.45)

def thumbnail(c):
    Wt, Ht = 1280, 720
    c.drawRect(skia.Rect.MakeWH(Wt, Ht), lin_grad(0, 0, Wt, Ht, [BG, "#120A1E"]))
    lit = {n: 1.0 for n in ["Spain", "Argentina", "Chile", "Colombia", "Peru", "Ecuador", "Mexico"]}
    draw_globe(c, 930, 380, 330, -55, 12, lit, 0)
    draw_text(c, "¿A QUÉ", 60, 200, "bebas", 170, "#FFFFFF", 1, tracking=3)
    draw_text(c, "HORA?", 60, 360, "bebas", 190, CYAN, 1, tracking=3, glow=(CYAN, 16))
    rect(c, 60, 420, 470, 130, GREEN, 1, r=20); draw_text(c, "00:00 LOCAL", 295, 515, "bebas", 104, "#000000", 1, align="center")
    draw_text(c, "GTA VI · 19 NOV · TU PAÍS", 60, 640, "monob", 40, "#FFFFFF", 0.9, tracking=2)
