"""VIDEO 04 — El mapa de Leonida explicado: 6 regiones y sus lugares reales.
Lenguaje visual: cartografía 3D tipo 'diorama' sobre la FLORIDA REAL (Natural Earth, dominio público),
cámara en perspectiva que viaja de norte a sur, pines por región con semáforo de certeza. DM Serif Display + Inter.
"""
import json, math, os, numpy as np, skia
from gfx import *
from components import *
from brand import PAL

OCEAN1, OCEAN2 = "#0B3440", "#06202A"; LAND = "#EFE4CB"; LAND_SIDE = "#B9A57C"; INK = "#1B2A2F"
TEAL = "#2CC7B5"; CORAL = "#FF6B5A"; GREEN = PAL["caiman"]; SUN = PAL["sol"]; CREAM = "#FFF6E3"
LON0, LAT0 = -83.0, 27.6; KX = 111.0 * math.cos(math.radians(LAT0)); KY = 111.0

def to_xy(lon, lat): return ((lon - LON0) * KX, (lat - LAT0) * KY)

_G = None
def geo():
    global _G
    if _G is None:
        base = os.path.join(os.path.dirname(__file__), "..", "geo")
        d = json.load(open(f"{base}/ne_50m_admin_1_states_provinces.geojson"))
        fl = []; nb = []
        for f in d["features"]:
            n = f["properties"].get("name")
            if n in ("Florida", "Georgia", "Alabama"):
                g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
                for p in polys:
                    arr = np.array([to_xy(lo, la) for lo, la in p[0]])
                    (fl if n == "Florida" else nb).append(arr)
        lk = json.load(open(f"{base}/ne_50m_lakes.geojson")); lake = None
        for f in lk["features"]:
            if "Okee" in str(f["properties"].get("name")): lake = np.array([to_xy(lo, la) for lo, la in f["geometry"]["coordinates"][0]])
        _G = dict(fl=fl, nb=nb, lake=lake)
    return _G

STOPS = [
    dict(key="kalaga", name="MOUNT KALAGA", sub="NATIONAL PARK", lon=-82.6, lat=30.42, cert_pos="OFICIAL",
         off="Frontera norte · “el borde salvaje”: caza, pesca y caminos todoterreno", real="Sin referente real claro", realcert="DEDUCCIÓN",
         fact="Punto más alto de Florida: Britton Hill, ≈105 m (también en la frontera norte)"),
    dict(key="gellhorn", name="PORT GELLHORN", sub="", lon=-85.66, lat=30.16, cert_pos="DEDUCCIÓN",
         off="“La costa olvidada”: moteles baratos, atracciones cerradas, centros comerciales vacíos", real="Panama City · Panhandle", realcert="DEDUCCIÓN",
         fact="Rockstar no ha dicho su ubicación exacta en el mapa"),
    dict(key="ambrosia", name="AMBROSIA", sub="", lon=-80.93, lat=26.75, cert_pos="OFICIAL",
         off="Pueblo industrial en el corazón del estado, alrededor de una refinería de azúcar", real="Clewiston · lago Okeechobee", realcert="DEDUCCIÓN",
         fact="Clewiston se promociona como “la ciudad más dulce de EE. UU.”"),
    dict(key="grass", name="GRASSRIVERS", sub="", lon=-80.85, lat=25.75, cert_pos="DEDUCCIÓN",
         off="El humedal de Leonida: agua, hierba alta y caimanes", real="Everglades", realcert="DEDUCCIÓN",
         fact="Game Informer: más de 170 especies animales en Leonida"),
    dict(key="vice", name="VICE CITY", sub="", lon=-80.19, lat=25.77, cert_pos="OFICIAL",
         off="El centro urbano de Leonida", real="Miami", realcert="DEDUCCIÓN",
         fact="Vice City debutó en la saga en 2002"),
    dict(key="keys", name="LEONIDA KEYS", sub="", lon=-81.2, lat=24.75, cert_pos="OFICIAL",
         off="Cadena de islas · Jason trabaja aquí para traficantes locales", real="Cayos de Florida", realcert="DEDUCCIÓN",
         fact="Islas unidas por puentes sobre el mar"),
]

def cam_for(state):
    lon, lat, dist, pitch, yaw = state
    tx, ty = to_xy(lon, lat); p, y = math.radians(pitch), math.radians(yaw)
    pos = (tx - dist * math.sin(y) * math.cos(p), ty - dist * math.cos(y) * math.cos(p), dist * math.sin(p))
    return pos, (tx, ty, 0)

def draw_map(c, W, H, state, t, active=None, visited=(), route_p=0.0, labels=True, show_pins=True):
    cam = Cam3D(W, H, 42); pos, tgt = cam_for(state); cam.look(pos, tgt)
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [OCEAN1, OCEAN2]))
    # retícula de lat/lon en perspectiva
    for lon in np.arange(-90, -76, 1.0):
        pts = np.array([[*to_xy(lon, la), 0] for la in np.linspace(22, 33, 40)]); P, z = cam.proj(pts)
        if (z > 1).all(): c.drawPath(poly([tuple(p) for p in P], False), paint(TEAL, 0.10, stroke=1.2))
    for lat in np.arange(22, 34, 1.0):
        pts = np.array([[*to_xy(lo, lat), 0] for lo in np.linspace(-90, -76, 40)]); P, z = cam.proj(pts)
        if (z > 1).all(): c.drawPath(poly([tuple(p) for p in P], False), paint(TEAL, 0.10, stroke=1.2))
    G = geo()
    def ring(arr, zval):
        pts = np.c_[arr, np.full(len(arr), zval)]; P, z = cam.proj(pts); return poly([tuple(p) for p in P])
    for arr in G["nb"]:
        c.drawPath(ring(arr, -6), paint("#3C4A4A", 1)); c.drawPath(ring(arr, 0), paint("#5E6B66", 1)); c.drawPath(ring(arr, 0), paint("#9AA59E", 0.4, stroke=1.2))
    # sombra y grosor del 'diorama'
    for arr in G["fl"]: c.drawPath(ring(arr, -14), paint("#000000", 0.35, blur=10))
    for arr in G["fl"]: c.drawPath(ring(arr, -9), paint(LAND_SIDE, 1))
    for arr in G["fl"]:
        pth = ring(arr, 0); c.drawPath(pth, paint(LAND, 1)); c.drawPath(pth, paint(INK, 0.55, stroke=1.6))
    if G["lake"] is not None:
        c.drawPath(ring(G["lake"], 0.2), paint("#1E6F78", 1)); c.drawPath(ring(G["lake"], 0.2), paint(INK, 0.5, stroke=1.2))
    # ruta del viaje
    if route_p > 0:
        pts = np.array([[*to_xy(s["lon"], s["lat"]), 1.0] for s in STOPS]); P, z = cam.proj(pts)
        pp = paint(CORAL, 0.9, stroke=4); pp.setPathEffect(skia.DashPathEffect.Make([14, 10], -t * 30))
        nseg = min(len(P) - 1, int(math.ceil(route_p)))
        for i in range(1, nseg + 1):
            seg = skia.Path(); seg.moveTo(*P[i - 1])
            mx, my = (P[i - 1][0] + P[i][0]) / 2, (P[i - 1][1] + P[i][1]) / 2 - 40
            seg.quadTo(mx, my, *P[i])
            frac = clamp(route_p - (i - 1))
            c.drawPath(partial_path(seg, frac), pp)
    if not show_pins: return cam
    for s in STOPS:
        if s["key"] not in visited and s["key"] != active: continue
        x, y = to_xy(s["lon"], s["lat"]); P, z = cam.proj(np.array([[x, y, 0], [x, y, 34]]))
        isact = s["key"] == active; col = GREEN if s["cert_pos"] == "OFICIAL" else SUN
        line(c, P[0][0], P[0][1], P[1][0], P[1][1], INK, 0.9, 3)
        circle(c, P[0][0], P[0][1], 7, INK, 0.7)
        rr = 18 if isact else 12
        if isact: circle(c, P[1][0], P[1][1], rr + 10 + 6 * pulse(t, 1.0), col, 0.35)
        circle(c, P[1][0], P[1][1], rr, col, 1); circle(c, P[1][0], P[1][1], rr, INK, 1, stroke=3)
        if labels:
            fs = 34 if isact else 24; f = font("dmserif", fs); tw = text_w(s["name"], f) + 30
            bx, by = P[1][0] + rr + 12, P[1][1] - fs * 0.6
            rect(c, bx, by - fs * 0.5, tw, fs * 1.35, CREAM if isact else "#FFFFFF", 0.95 if isact else 0.8, r=8)
            draw_text(c, s["name"], bx + 15, by + fs * 0.55, "dmserif", fs, INK, 1)
    return cam

def info_card(c, s, p, t, cues):
    if p <= 0: return
    x = 60 - (1 - ease_out(p)) * 700; y = 170
    rect(c, x, y, 680, 760, "#0A1B21", 0.88, r=22); rect(c, x, y, 680, 760, CREAM, 0.25, r=22, stroke=2)
    draw_text(c, s["name"], x + 40, y + 95, "dmserif", 66 if len(s["name"]) < 13 else 54, CREAM)
    if s["sub"]: draw_text(c, s["sub"], x + 42, y + 140, "monob", 26, TEAL, 1, tracking=4)
    yy = y + 190
    draw_text(c, "SEGÚN ROCKSTAR", x + 40, yy, "monob", 22, "#9FB7B5", 1, tracking=3)
    cert_tag(c, x + 640, yy - 30, "OFICIAL", 1, 20, align="right", t=1)
    draw_par(c, s["off"], x + 40, yy + 50, "intersb", 32, 600, color=CREAM, a=1)
    yy += 250
    pr = ease_out(prog(t, cues[0], cues[0] + 0.4))
    if pr > 0:
        draw_text(c, "INSPIRACIÓN REAL", x + 40, yy, "monob", 22, "#9FB7B5", pr, tracking=3)
        cert_tag(c, x + 640, yy - 30, s["realcert"], pr, 20, align="right", t=pr)
        draw_text(c, s["real"], x + 40, yy + 60, "dmserif", 46, SUN, pr)
    pf = ease_out(prog(t, cues[1], cues[1] + 0.4))
    if pf > 0:
        rect(c, x + 40, yy + 110, 600, 2, CREAM, 0.2 * pf)
        icon(c, "pin", x + 62, yy + 162, 34, CORAL, pf)
        draw_par(c, s["fact"], x + 95, yy + 170, "intermd", 28, 540, color=CREAM, a=pf)

# ---------------------------------------------------------------- escenas
def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    st = (-83.0, 27.8, 1500, 80, 0)
    draw_map(c, W, H, (st[0], st[1], st[2] - 120 * ease_io(prog(t, 0, info.d)), 80, -6 + 6 * ease_io(prog(t, 0, info.d))), t, show_pins=False)
    rect(c, 0, 0, W, H, "#06202A", 0.45)
    cues = [info.w("seis nombres"), info.w("dos ubicaciones"), info.w("un estado real")]
    labels = ["6 NOMBRES", "2 UBICACIONES CONFIRMADAS", "1 ESTADO REAL"]
    for i, (lab, cu) in enumerate(zip(labels, cues)):
        p = ease_out_back(prog(t, cu, cu + 0.4)); y = 330 + i * 150
        if p <= 0: continue
        c.save(); c.translate(1340, y); c.scale(p, p)
        rect(c, -400, -60, 800, 120, CREAM, 0.95, r=14); draw_text(c, lab, 0, 20, "dmserif", 52, INK, 1, align="center")
        c.restore()
    p = ease_out(prog(t, info.w("rompecabezas"), info.w("rompecabezas") + 0.5))
    if p > 0: draw_text(c, "SIN INVENTAR NI UNA PIEZA", 1340, 860, "monob", 40, SUN, p, align="center", tracking=4)
    draw_text(c, "?", 520, 640, "dmserif", 420, CREAM, 0.12 + 0.05 * pulse(t, 2))

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_rules(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    draw_map(c, W, H, (-83.0, 27.8, 1350, 72, 0), t, show_pins=False); rect(c, 0, 0, W, H, "#06202A", 0.55)
    cert_tag(c, W / 2 - 330, 300, "OFICIAL", 1, 40, t=prog(t, info.w("verde"), info.w("verde") + 0.4))
    cert_tag(c, W / 2 + 40, 300, "DEDUCCIÓN", 1, 40, t=prog(t, info.w("amarillo"), info.w("amarillo") + 0.4))
    p = ease_out(prog(t, info.w("advertencia"), info.w("advertencia") + 0.5))
    if p > 0:
        rect(c, 360, 520, 1200, 300, "#0A1B21", 0.92 * p, r=22); rect(c, 360, 520, 1200, 300, CORAL, p, r=22, stroke=3)
        icon(c, "warn", 470, 670, 110, CORAL, p)
        draw_text(c, "ESTE MAPA ES LA FLORIDA REAL", 560, 640, "dmserif", 60, CREAM, p)
        draw_text(c, "No es el mapa del juego. Leonida es su parodia.", 560, 720, "intersb", 38, CREAM, 0.85 * p)

def sc_size(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, 0, H, [OCEAN1, OCEAN2])); grid(c, W, H, 60, TEAL, 0.07)
    p1 = ease_out(prog(t, info.w("GTA 5") - 0.6, info.w("GTA 5"))); p2 = ease_out_back(prog(t, info.w("doble"), info.w("doble") + 0.6))
    s = 300
    if p1 > 0:
        rect(c, 400, 640 - s * p1, s, s * p1, "#3C5A62", 1); rect(c, 400, 640 - s, s, s, CREAM, p1, stroke=3)
        draw_text(c, "GTA V", 400 + s / 2, 700, "monob", 34, CREAM, p1, align="center", tracking=3)
    if p2 > 0:
        s2 = s * math.sqrt(2) * p2
        rect(c, 1000, 640 - s2, s2, s2, TEAL, 0.35); rect(c, 1000, 640 - s2, s2, s2, TEAL, 1, stroke=4)
        draw_text(c, "×2", 1000 + s2 / 2, 640 - s2 / 2 + 50, "dmserif", 150 * p2, CREAM, 1, align="center")
        draw_text(c, "GTA VI (según Rockstar)", 1000 + s * 0.7, 700, "monob", 34, TEAL, p2, align="center", tracking=2)
    cert_tag(c, 1000, 760, "OFICIAL", 1, 26, t=prog(t, info.w("Game Informer"), info.w("Game Informer") + 0.4))
    source_chip(c, 400, 830, "Aaron Garbut (Rockstar) en Game Informer, n.º 382", ease_out(prog(t, info.w("Game Informer"), info.w("Game Informer") + 0.4)))
    p = ease_out(prog(t, info.w("No sabemos"), info.w("No sabemos") + 0.5))
    if p > 0:
        rect(c, 400, 900, 1120, 100, "#000000", 0.5 * p, r=12)
        draw_text(c, "¿Superficie? ¿Área total? ¿Contenido? → tómalo como escala", 430, 965, "intersb", 36, SUN, p)
        cert_tag(c, 1500, 925, "DEDUCCIÓN", p, 20, align="right", t=p)
    draw_text(c, "TAMAÑO", 400, 230, "dmserif", 90, CREAM, ease_out(prog(t, 0, 0.5)))
    draw_text(c, "Cuadrados ilustrativos: no representan la forma real de ningún mapa", 400, 290, "intermd", 26, CREAM, 0.6 * ease_out(prog(t, 0, 0.5)))

# cámara por parada: (lon, lat, distancia, inclinación, giro)
CAMS = {"start": (-83.0, 28.6, 1100, 62, 0), "kalaga": (-82.6, 30.1, 520, 48, 8), "gellhorn": (-85.4, 29.9, 520, 50, -10),
        "ambrosia": (-81.1, 26.6, 480, 46, 10), "grass": (-80.9, 25.6, 460, 44, 18), "vice": (-80.3, 25.75, 380, 42, 28),
        "keys": (-81.0, 24.85, 520, 44, 6), "end": (-82.6, 27.4, 1350, 66, 0)}

def sc_tour(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    keys = [s["key"] for s in STOPS]; nb = len(info.beats)
    # beat i → parada i (6 paradas)
    starts = [info.b(i) for i in range(nb)]
    idx = max(i for i in range(nb) if starts[i] <= t + 1e-6)
    prev = CAMS["start"] if idx == 0 else CAMS[keys[idx - 1]]; target = CAMS[keys[idx]]
    e = ease_io(prog(t, starts[idx], starts[idx] + 2.6))
    state = tuple(lerp(a, b, e) for a, b in zip(prev, target))
    # ligera deriva para mantener movimiento
    state = (state[0], state[1], state[2] * (1 - 0.04 * prog(t, starts[idx] + 2.6, starts[idx] + 12)), state[3], state[4] + 3 * math.sin(t * 0.2))
    route = (idx - 1 + e) if idx > 0 else 0
    draw_map(c, W, H, state, t, active=keys[idx], visited=keys[:idx], route_p=route)
    # tarjeta informativa
    s = STOPS[idx]; tb = starts[idx]; bend = starts[idx + 1] if idx + 1 < nb else info.d
    p = prog(t, tb + 0.8, tb + 1.4) * (1 - prog(t, bend - 0.4, bend))
    cues = {"kalaga": ("Florida real", "Britton Hill"), "gellhorn": ("comunidad", "Ojo"), "ambrosia": ("pista real", "ciudad más dulce"),
            "grass": ("Everglades", "Game Informer"), "vice": ("Miami", "dos mil dos"), "keys": ("Cayos", "Jason")}[s["key"]]
    info_card(c, s, p, t, (info.w(cues[0], default=tb + 3), info.w(cues[1], default=tb + 6)))
    # contador de parada
    draw_text(c, f"PARADA {idx + 1}/6", W - 60, 80, "monob", 30, CREAM, 0.9, align="right", tracking=4)
    for i in range(6): circle(c, W - 360 + i * 50, 120, 10, CORAL if i <= idx else "#2D4A50", 1)

def sc_unknown(c, t, info, ctx):
    W, H = ctx.W, ctx.H
    draw_map(c, W, H, (-82.6, 27.4, 1350 + 80 * ease_io(prog(t, 0, info.d)), 66, 0), t, visited=[s["key"] for s in STOPS], route_p=5.0, labels=False)
    rect(c, 0, 0, W, H, "#06202A", 0.5)
    qs = [("¿La forma exacta de Leonida?", "forma exacta"), ("¿Cuántos interiores se pueden visitar?", "interiores"),
          ("¿Qué hay entre una región y otra?", "pueblos"), ("¿Son solo estas seis regiones?", "seis regiones son")]
    for i, (q, cue) in enumerate(qs):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.4)); y = 280 + i * 140
        if p <= 0: continue
        rect(c, 500 - (1 - p) * 60, y, 920, 110, "#0A1B21", 0.9 * p, r=16)
        draw_text(c, "?", 560 - (1 - p) * 60, y + 82, "dmserif", 80, SUN, p)
        draw_text(c, q, 630 - (1 - p) * 60, y + 72, "intersb", 42, CREAM, p)
    p = ease_out_back(prog(t, info.w("jugando"), info.w("jugando") + 0.5))
    if p > 0:
        c.save(); c.translate(W / 2, 930); c.scale(p, p); rect(c, -440, -55, 880, 110, SUN, 1, r=55)
        draw_text(c, "SOLO SE RESPONDE JUGANDO", 0, 20, "monob", 46, INK, 1, align="center", tracking=2); c.restore()

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "¿A QUÉ REGIÓN VAS PRIMERO?", "Volvemos a este mapa con el juego en las manos", TEAL)

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2.5 < gt < ctx.total - 20:
        watermark(c, W, H, 0.5)
        draw_text(c, "Mapa: Florida real (Natural Earth) · no es el mapa oficial de Leonida", W - 120, H - 34, "mono", 18, CREAM, 0.55, align="right")

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Rockstar todavía no ha publicado un mapa completo de Leonida. Pero sí dejó pistas: seis nombres, dos ubicaciones confirmadas y un estado real que todos reconocemos. "
     "Hoy armamos el rompecabezas, sin inventar ni una pieza.",
     sc_hook, section="GANCHO", energy=1, sfx=[("w:seis nombres", "pin", 0.5), ("w:dos ubicaciones", "pin", 0.5), ("w:un estado real", "pin", 0.5), ("w:rompecabezas", "whoosh", 0.4)])
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=1, trans=("flash", 0.3))
beat("Estás en Sal y Asfalto. Regla del viaje: en verde, lo que Rockstar confirmó; en amarillo, lo que deducimos nosotros o la comunidad. "
     "Y una advertencia importante: el mapa que vas a ver es la Florida real, no el mapa del juego. Lo usamos porque Leonida es, claramente, su parodia.",
     sc_rules, section="INTRODUCCIÓN", energy=1, trans=("zoom", 0.5), sfx=[("w:verde", "pop", 0.4), ("w:amarillo", "pop", 0.4), ("w:advertencia", "ding", 0.3)])
beat("Primero, el tamaño. Aaron Garbut, de Rockstar, le dijo a la revista Game Informer que el mapa es el doble de grande que el de GTA 5. "
     "No sabemos si habla de superficie de tierra, de área total o de contenido, así que tómalo como una escala, no como una medida exacta.",
     sc_size, section="TAMAÑO", energy=2, trans=("wipe", 0.5), sfx=[("w:doble", "hit", 0.5)])
beat("Primera parada: el extremo norte. La web de Rockstar ubica el Parque Nacional Mount Kalaga contra la frontera norte de Leonida, y lo describe como el borde salvaje del estado: caza, pesca y caminos para todoterreno, lejos del caos de Vice City. "
     "Curiosamente, la Florida real no tiene montañas. Su punto más alto, Britton Hill, mide unos ciento cinco metros... y también está pegado a la frontera norte.",
     sc_tour, section="PARADA 1 · MOUNT KALAGA", energy=2, trans=("zoom", 0.6), sfx=[(0.3, "whoosh", 0.4), (1.0, "pin", 0.5)])
beat("Segunda parada, hacia el oeste: Port Gellhorn. Rockstar lo llama la costa olvidada de Leonida: un antiguo destino de vacaciones lleno de moteles baratos, atracciones cerradas y centros comerciales vacíos. "
     "La comunidad lo asocia con Panama City y el noroeste de Florida, la zona conocida como el Panhandle. Ojo: Rockstar no ha dicho en qué punto exacto del mapa está.",
     None, section="PARADA 2 · PORT GELLHORN", sfx=[(0.3, "whoosh", 0.4), (1.0, "pin", 0.5)])
beat("Tercera parada: el corazón del estado. Según Rockstar, Ambrosia es un pueblo industrial en el centro de Leonida, construido alrededor de una refinería de azúcar, donde la vieja industria y los viejos valores siguen mandando, cueste lo que cueste. "
     "La pista real es casi un regalo: Clewiston, a orillas del lago Okeechobee, se promociona como la ciudad más dulce de Estados Unidos por su industria azucarera.",
     None, section="PARADA 3 · AMBROSIA", sfx=[(0.3, "whoosh", 0.4), (1.0, "pin", 0.5)])
beat("Bajamos al sur, y la carretera empieza a perderse entre el agua. Grassrivers es el humedal de Leonida, inspirado en los Everglades: el famoso río de hierba, un pantano gigantesco que avanza despacio hacia el mar. "
     "Ahí viven los caimanes que vimos desde el primer tráiler. Y según Game Informer, Leonida tendrá más de ciento setenta especies de animales.",
     None, section="PARADA 4 · GRASSRIVERS", sfx=[(0.3, "whoosh", 0.4), (1.0, "pin", 0.5), (3.0, "bird", 0.4), (5.0, "water", 0.3)])
beat("Quinta parada: la estrella. Vice City, la versión de Miami que Rockstar parodia desde el año dos mil dos. Playas, rascacielos y una vida nocturna que no se apaga. "
     "Es el centro urbano de Leonida, y el lugar donde casi todo el marketing ha puesto la cámara.",
     None, section="PARADA 5 · VICE CITY", sfx=[(0.3, "whoosh", 0.4), (1.0, "pin", 0.5)], energy=3)
beat("Y la última parada: las Leonida Keys, el reflejo de los Cayos de Florida, esa cadena de islas unidas por puentes sobre el mar. "
     "Aquí hay un dato oficial clave para la historia: según la web de Rockstar, Jason trabaja en los Keys para traficantes locales.",
     None, section="PARADA 6 · LEONIDA KEYS", sfx=[(0.3, "whoosh", 0.4), (1.0, "pin", 0.5)], energy=2)
beat("¿Y qué no sabemos? Muchísimo. No sabemos la forma exacta de Leonida, ni cuánto se parece su costa a la de Florida. "
     "No sabemos cuántos interiores se pueden visitar, ni qué pueblos hay entre una región y otra. Y no sabemos si estas seis regiones son todas. "
     "Eso solo se responde jugando.",
     sc_unknown, section="LO QUE NO SABEMOS", energy=1, trans=("fade", 0.6), sfx=[("w:forma exacta", "tick", 0.5), ("w:interiores", "tick", 0.5), ("w:pueblos", "tick", 0.5), ("w:seis regiones son", "tick", 0.5), ("w:jugando", "hit", 0.5)])
beat("El jueves, con el juego en las manos, volvemos a este mapa y marcamos qué deducciones acertamos y cuáles fallamos. Si quieres ver ese marcador, suscríbete. "
     "Y cuéntame en los comentarios: ¿a qué región vas a ir primero?",
     sc_end, section="LLAMADA A LA ACCIÓN", energy=2, hold=4.0, min=20, trans=("fade", 0.6))

VIDEO = dict(id="v04", folder="VIDEO_04", file="GTA6_mapa_Leonida_6_regiones_lugares_reales",
             title="El mapa de GTA 6 explicado: las 6 regiones de Leonida y los lugares reales que las inspiran",
             format="Largo (16:9)", music="tropical", music_seed=41, voice="host", beats=B, overlay=overlay, music_gain=0.5)

def thumbnail(c):
    W, H = 1280, 720
    s = gfx_surface = None
    draw_map(c, W, H, (-81.6, 27.0, 900, 58, 12), 0, active="vice", visited=["kalaga", "gellhorn", "ambrosia", "grass", "keys"], route_p=5.0, labels=False)
    rect(c, 0, 0, W, H, "#000000", 0.0)
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, 0, [hexc("#06202A", 0.92), hexc("#06202A", 0.6), hexc("#06202A", 0)], [0, 0.45, 0.75]))
    draw_text(c, "6", 60, 330, "ovblk", 300, PAL["amarillo"], 1)
    draw_text(c, "REGIONES", 270, 210, "ovblk", 88, CREAM, 1)
    draw_text(c, "DE LEONIDA", 270, 310, "ovblk", 88, CREAM, 1)
    sign_text(c, 60, 380, "Y SUS LUGARES REALES", 52)
    draw_text(c, "GTA VI · MAPA EXPLICADO", 60, 560, "monob", 38, CREAM, 0.9, tracking=2)
