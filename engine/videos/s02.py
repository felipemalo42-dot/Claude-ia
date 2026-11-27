"""SHORT_02 · Caso: isla S.O.S. (el perro de la moto de agua de GTA 6).

Descubrimiento viral de jugadores: en una isla perdida hay un S.O.S. escrito en la arena y un teléfono con el vídeo de
una pareja que saluda a cámara (sus «últimos momentos», según parece). Si buceas y vuelves a la superficie, aparece un
perro con gafas pilotando una moto de agua: te lleva de copiloto y te deja otra moto.
Estructura: misterio → giro cómico → pregunta final que devuelve al principio (bucle).
Montaje: expediente policial con «pruebas» numeradas, grano y tono frío; en el giro, destello y paso a color tropical.
Música: misterio original (caja de música) que cambia a tropical (marimba) en la revelación.
Imagen: gameplay de IGN («WE LOVE JET SKI DOG!», copia pública en Internet Archive). Solo se usa la banda limpia del
vídeo vertical (sin sus títulos, subtítulos ni logotipo). Sin spoilers: encuentro secundario, no es una misión.
"""
import random, numpy as np, skia
import audio
from gfx import *
from videos import gl_render as G, sh_render as SR

V2 = "CuGNTq2mFIk"
def X(t): return f"x:{V2}@{t}"
# Fuente: la banda limpia del vídeo vertical de IGN (recorte 880×822 desde y=466: sin su título, su subtítulo ni su logotipo),
# sin fotogramas duplicados (mpdecimate) y llevada a 60 fps reales por interpolación de movimiento (minterpolate):
#   ffmpeg -i CuGNTq2mFIk.webm -vf "crop=880:822:0:466,mpdecimate=hi=64*6:lo=64*3:frac=0.5,minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" CuGNTq2mFIk.mp4
# El original era juego a 30 fps guardado a 60 (la mitad de fotogramas repetidos; en los primeros planos del perro, 4-5 veces).
SR.SRC_CROP[V2] = (0, 0, 880, 822) if G.x_path(V2).endswith(".mp4") else (0, 466, 880, 822)
G.XBAD[V2] = []
G.MANUAL_CUTS[V2] = [1.5]
PANEL = (0, 360, 1080, 1010)
DARK, PAPER, MINT, STAMP = "#061017", "#E8F1F2", "#7CF3C4", "#FF4A3D"
PINK, SUN, AQUA = "#FF4FD8", "#FFD23F", "#36E3FF"

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def scene(c, t, info, ctx): return _scene(c, t, info, ctx)

# ================================================================ GUION Y PLANOS (mood: "dark" = expediente, "bright" = revelación)
beat("Lejos de la costa de Leonida hay una isla diminuta. Y alguien escribió en la arena: {S.O.S.|ese, o, ese}.",
     mus=("mystery", 1), exag=0.55, pre=0.15, mood="dark",
     shots=[S(None, X(5.5), z=(1.0, 1.12)),
            S("una isla diminuta", X(5.5), cont=True, z=(1.12, 1.2)),
            S("Y alguien", X(12.55), z=(1.0, 1.08), evid="PRUEBA 1 · EL MENSAJE"),
            S("en la arena", X(10.25), cx=0.24, cy=0.78, z=(1.2, 1.7))],
     sfx=[(0.0, "tune", 0.3), ("w:arena", "stamp", 0.45)])
beat("Al lado hay un teléfono con un vídeo: una pareja saluda a la cámara… y, por lo que parece, son sus últimos momentos.",
     mus=("mystery", 1), exag=0.5, pre=0.3, mood="dark",
     shots=[S(None, X(15.25), z=(1.0, 1.1), evid="PRUEBA 2 · EL TELÉFONO"),
            S("un vídeo", X(17.45), cx=0.55, z=(1.0, 1.12), speed=0.58),
            S("saluda a la cámara", X(17.45), cont=True, cx=0.55, cy=0.45, z=(1.15, 1.3), speed=0.58),
            S("sus últimos momentos", X(17.45), cont=True, cx=0.55, cy=0.42, z=(1.3, 1.5), speed=0.58, glitch=True)],
     sfx=[("w:teléfono", "tick", 0.35), ("w:últimos", "tune", 0.35)])
beat("No hay nadie más. Solo agua. Así que bajas a bucear.",
     mus=("mystery", 2), exag=0.55, pre=0.3, mood="dark",
     shots=[S(None, X(13.6), z=(1.0, 1.08), minwin=0.3),
            S("Solo agua", X(7.2), z=(1.0, 1.15)),
            S("bajas a bucear", X(21.75), z=(1.0, 1.1), speed=0.5, nocut=True, evid="PRUEBA 3 · EL FONDO")],
     sfx=[("w:bucear", "whoosh", 0.35)])
beat("Y cuando vuelves a la superficie… algo viene directo hacia ti.",
     mus=("mystery", 2), exag=0.6, pre=0.25, mood="dark",
     shots=[S(None, X(21.75), cont=True, z=(1.0, 1.08), speed=0.5, nocut=True),
            S("algo viene", X(21.75), cont=True, cx=0.47, cy=0.4, z=(1.4, 1.85), speed=0.3, nocut=True)],
     sfx=[("w:algo", "tune", 0.45)])
beat("Es un perro. Con gafas. En moto de agua.",
     mus=("tropical", 2), exag=0.8, pre=0.35, mood="bright",
     shots=[S(None, X(0.05), cx=0.55, cy=0.45, z=(1.12, 1.0), flash=True, reveal=True),
            S("Con gafas", X(0.05), cont=True, cx=0.6, cy=0.36, z=(1.55, 1.75)),
            S("En moto de agua", X(1.55), z=(1.0, 1.1))],
     sfx=[(0.0, "hit", 0.6), ("w:gafas", "pop", 0.45), ("w:moto", "pop", 0.4)])
beat("Te subes de copiloto, él conduce, te da una vuelta… y al final te deja otra moto para ti.",
     mus=("tropical", 2), exag=0.7, pre=0.2, mood="bright",
     shots=[S(None, X(26.7), z=(1.0, 1.1)),
            S("él conduce", X(38.8), cx=0.6, cy=0.4, z=(1.2, 1.35)),
            S("te da una vuelta", X(28.95), z=(1.0, 1.12)),
            S("otra moto", X(34.95), z=(1.0, 1.1))],
     sfx=[("w:conduce", "pop", 0.35), ("w:otra moto", "ding", 0.35)])
beat("Y ojo: hay jugadores que se lo han encontrado en otras zonas del mar.",
     mus=("tropical", 1), exag=0.65, pre=0.2, mood="bright",
     shots=[S(None, X(33.05), z=(1.0, 1.15)),
            S("se lo han encontrado", X(31.3), z=(1.0, 1.1)),
            S("en otras zonas", X(3.35), z=(1.0, 1.1))])
beat("Así que dime… ¿quién escribió el {S.O.S.|ese, o, ese}?",
     mus=("mystery", 1), exag=0.6, pre=0.35, mood="dark", hold=0.7,
     shots=[S(None, X(15.6), z=(1.05, 1.15)),
            S("quién escribió", X(10.25), cx=0.24, cy=0.78, z=(1.2, 1.6), speed=0.47)],
     sfx=[(0.0, "tune", 0.35), ("w:escribió", "stamp", 0.5)])

# ================================================================ ESCENA
CF_DARK = SR.color_matrix(sat=0.45, contrast=1.12, bright=-0.06, tint=(-0.25, 0.1, 0.2))
CF_BRIGHT = SR.color_matrix(sat=1.3, contrast=1.08, bright=0.03, tint=(0.05, 0.0, -0.05))

def _grain(c, gt, rect_, a=0.10):
    x, y, w, h = rect_; rnd = random.Random(int(gt * 30))
    for _ in range(260):
        rect(c, x + rnd.random() * w, y + rnd.random() * h, 2, 2, "#FFFFFF" if rnd.random() < 0.5 else "#000000", a)
    for k in range(int(y), int(y + h), 6): rect(c, x, k, w, 1, "#000000", 0.07)

def draw_shot(c, sh, tau, d, ctx, slot):
    T = G.table(ctx); b = T["beats"][sh["beat"]]["b"]; dark = b.get("mood") == "dark"
    rect(c, 0, 0, SR.W, SR.H, DARK if dark else "#0E2A3A", 1)
    sh2 = dict(sh, cf=CF_DARK if dark else CF_BRIGHT)
    SR.footage(c, sh2, tau, d, PANEL, slot)
    x, y, w, h = PANEL
    if dark:
        _grain(c, sh["t0"] + tau, PANEL)
        vg = skia.Paint(); vg.setShader(skia.GradientShader.MakeRadial((540, y + h / 2), 760, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 170)], [0.55, 1.0]))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), vg)
    if sh.get("glitch"):
        rnd = random.Random(int(tau * 4))
        for _ in range(3):
            gy = y + rnd.random() * h; rect(c, x, gy, w, 3 + rnd.random() * 6, MINT if rnd.random() < 0.5 else STAMP, 0.14)
        draw_text(c, "● REC", x + 40, y + 70, "ovmonomd", 34, STAMP, 0.6 + 0.4 * pulse(tau, 0.8))
    if sh.get("evid"):
        p = ease_out_back(prog(tau, 0.1, 0.4))
        c.save(); c.translate(70, y + 70); c.rotate(-3); c.scale(p, p)
        f = font("ovmonomd", 34); tw = text_w(sh["evid"], f, 1) + 50
        rect(c, 0, -48, tw, 70, PAPER, 0.96, r=4); circle(c, tw / 2, -50, 10, STAMP, 1)
        draw_text(c, sh["evid"], 25, 0, "ovmonomd", 34, DARK, 1, tracking=1); c.restore()
    if sh.get("reveal"):
        p = ease_out_back(prog(tau, 0.25, 0.55), 2.4)
        c.save(); c.translate(540, y + h - 170); c.rotate(-7); c.scale(2.0 - p, 2.0 - p)
        rect(c, -330, -80, 660, 140, SUN, clamp(p * 2), r=10, stroke=10)
        draw_text(c, "SOSPECHOSO: UN PERRO", 0, 20, "anton", 70, SUN, clamp(p * 2), align="center", tracking=2); c.restore()
    if not dark and int(tau * 10) % 2 == 0:
        rnd = random.Random(sh["k"] * 7 + int(tau * 5))
        for _ in range(10):
            sx, sy = x + rnd.random() * w, y + rnd.random() * h * 0.5; s = 6 + rnd.random() * 10
            draw_poly(c, [(sx, sy - s), (sx + s * 0.3, sy), (sx, sy + s), (sx - s * 0.3, sy)], "#FFFFFF", 0.8)

_scene = SR.make_scene(draw_shot, trans=lambda a, b: None)

def overlay(c, gt, ctx):
    sh, b, i, bi = SR.current(ctx, gt); dark = b.get("mood") == "dark"
    x, y, w, h = PANEL
    # marco del panel y cabecera del expediente
    rect(c, x, y - 4, w, 4, MINT if dark else PINK, 1); rect(c, x, y + h, w, 4, MINT if dark else PINK, 1)
    if dark:
        draw_text(c, "EXPEDIENTE Nº 06", 60, 170, "ovmonomd", 40, MINT, 0.9, tracking=3)
        draw_text(c, "CASO: ISLA S.O.S.", 60, 280, "anton", 104, PAPER, 1, tracking=3)
    else:
        draw_text(c, "CASO RESUELTO", 60, 170, "ovmonomd", 40, SUN, 1, tracking=3)
        draw_text(c, "PERRO EN MOTO", 60, 280, "anton", 104, PINK, 1, tracking=3)
    if not sh["src"].startswith("g:"): SR.credit(c, sh, x=40, y=y + h - 60)
    SR.subs_typewriter(c, gt, ctx, y=1468, size=48, maxc=24, hi=MINT if dark else SUN)

# ================================================================ MÚSICA, PORTADA Y DATOS
def music_fn(total, beats_tl):
    segs = []
    for b, bd in zip(B, beats_tl):
        st, lv = b.get("mus", ("mystery", 1))
        if segs and segs[-1]["style"] == st: segs[-1]["en"].append((bd["start"] - segs[-1]["t0"], lv))
        else: segs.append(dict(style=st, t0=bd["start"], en=[(0.0, lv)]))
    n = int(total * audio.SR); out = np.zeros((n, 2))
    for i, sg in enumerate(segs):
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        xf = 0.08 if (i + 1 < len(segs) and segs[i + 1]["style"] == "tropical") else 0.6     # corte seco en la revelación
        a0 = sg["t0"]; dur = (t1 - a0) + xf
        y = audio.compose(sg["style"], dur, energy=sg["en"], seed=5200 + 17 * i, key_shift=0)
        s = int(a0 * audio.SR); fo = int(xf * audio.SR)
        if i + 1 < len(segs) and len(y) > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None]
        fi = int(0.05 * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None]
        e = min(n, s + len(y)); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

def _still(t, cx=0.5, cy=0.5, z=1.0, size=(1080, 1010)):
    import subprocess
    path = G.x_path(V2); m = G._clip_meta(path)
    x, y, w, h = SR.window(m, SR.SRC_CROP[V2], size[0] / size[1], z, cx, cy)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf",
                          f"crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:flags=bicubic,format=rgba", "-f", "rawvideo", "-"], capture_output=True).stdout
    return skia.Image.fromarray(np.frombuffer(raw, np.uint8).reshape(size[1], size[0], 4).copy(), colorType=skia.ColorType.kRGBA_8888_ColorType)

def thumbnail(c):
    rect(c, 0, 0, 1080, 1920, DARK, 1)
    top = _still(10.9, 0.24, 0.78, 1.5, (1080, 860)); bot = _still(0.2, 0.55, 0.45, 1.1, (1080, 860))
    p = skia.Paint(); p.setColorFilter(CF_DARK); c.drawImageRect(top, skia.Rect.MakeXYWH(0, 140, 1080, 860), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.drawImageRect(bot, skia.Rect.MakeXYWH(0, 1000, 1080, 860))
    rect(c, 0, 996, 1080, 8, PINK, 1)
    draw_text(c, "CASO: ISLA S.O.S.", 60, 110, "anton", 88, PAPER, 1, tracking=3)
    c.save(); c.translate(540, 1520); c.rotate(-6)
    rect(c, -360, -95, 720, 160, SUN, 1, r=12, stroke=12); draw_text(c, "¿QUIÉN PIDIÓ AYUDA?", 0, 18, "anton", 76, SUN, 1, align="center", tracking=2)
    c.restore()

VIDEO = dict(id="s02", folder="SHORT_02", file="VIDEO_FINAL", size=(1080, 1920), thumb_size=(1080, 1920),
             title="GTA 6: la isla del S.O.S. y el perro de la moto de agua", format="Short vertical (9:16)",
             music="mystery", music_fn=music_fn, voice="host", beats=B, overlay=overlay, grade=None, music_gain=0.48,
             lead_in=0.1, tail=0.6, trim_tail=0.3, max_tries=3, qa_metric="fonetica", qa_thr=0.995, trans=("cut", 0.0),
             names=dict(narr_wav="recursos/narracion_original.flac", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="recursos/guion_con_tiempos.txt", thumb="PORTADA.png"))
THUMB_MARK = None
