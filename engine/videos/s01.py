"""SHORT_01 · El ring secreto de GTA 6 (Backyard American Mania).

Descubrimiento de jugadores: un ring de lucha libre escondido en un patio de Hamlet, defendido por «The Gentrifier».
Si no esquivas su salto desde la tercera cuerda, mueres al instante; si ganas, te llevas una máscara de luchador.
Estructura: guía de «jefe final» en cuatro rondas (lugar, preparación, combate, premio), contada como una retransmisión
de lucha libre. Montaje: cortes muy rápidos, impactos con sacudida y destello, cámara lenta en el salto, tarjeta VS,
subtítulos cinéticos. Música: trap original (140 bpm) con campana de ring.
Imagen: gameplay de IGN («GTA 6 - How to Become a Backyard Wrestler», copia pública en Internet Archive), recortado en
vertical desde la copia 4K. Datos: lo que se ve en ese gameplay y su narración (transcrita). Sin spoilers: actividad
secundaria disponible casi en cualquier momento de la campaña.
"""
import numpy as np, skia
import audio
from gfx import *
from videos import gl_render as G, sh_render as SR

V1 = "fIWUHYFBmrI"
def X(t): return f"x:{V1}@{t}"
G.XBAD[V1] = [(0.0, 4.9), (11.5, 16.3), (19.4, 27.9), (146.8, 150.0)]     # rótulos del autor, cortinilla de título y cierre de IGN
SR.EFF_FPS[V1] = 30          # la guía de IGN es juego a 30 fps guardado a 60: la mitad de los fotogramas son copias (medido)
G.MANUAL_CUTS[V1] = [91.0, 105.0, 106.0, 114.0, 117.0, 123.2, 125.45, 126.2, 126.85]   # medidos a 0,2 s
RED, GOLD, INK = "#E10600", "#FFD23F", "#0B0B0F"

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)

def scene(c, t, info, ctx): return _scene(c, t, info, ctx)

# ================================================================ GUION Y PLANOS
beat("En GTA 6 hay un combate de lucha libre escondido en un patio. Y un solo error te mata.",
     mus=("trap26", 2), exag=0.75, pre=0.15, round=None,
     shots=[S(None, X(110.6), cx=0.44, cy=0.45, z=(1.18, 1.0), speed=0.8, flash=True),
            S("lucha libre", X(96.6), cx=0.47, z=(1.05, 1.15), punch=0.06),
            S("escondido en un patio", X(72.6), cx=0.42, z=(1.0, 1.08)),
            S("un solo error", X(112.2), cx=0.45, cy=0.42),
            S("te mata", X(113.6), cx=0.42, cy=0.45, freeze=0.05, minwin=0.05, cf="bw", big=("UN ERROR", "= MUERTO"), punch=0.05)],
     sfx=[(0.0, "ding", 0.55), ("w:lucha", "hit", 0.4), ("w:te mata", "hit", 0.55)])
beat("Cruza el puente hasta Hamlet y busca esta casa: detrás está el ring de Backyard American Mania.",
     mus=("trap26", 1), exag=0.7, pre=0.25, round=(1, "EL LUGAR"),
     shots=[S(None, X(31.0), cx=0.56, z=(1.0, 1.12)),
            S("Hamlet", X(35.2), cx=0.55, z=(1.05, 1.2), tag=("HAMLET", 0.5, 0.47)),
            S("esta casa", X(28.3), cx=0.4, z=(1.0, 1.08)),
            S("el ring", X(75.0), cx=0.42, z=(1.0, 1.1)),
            S("Backyard American Mania", X(90.3), cx=0.3, z=(1.0, 1.1), speed=0.84, nocut=True, big=("BACKYARD", "AMERICAN MANIA"))],
     sfx=[(0.0, "whoosh", 0.5), ("w:Hamlet", "pop", 0.4), ("w:Backyard", "hit", 0.35)])
beat("Antes de subir: guarda la partida, compra barritas de proteína para aguantar, y llévate la carta de las gradas. Se vende en las casas de empeño.",
     mus=("trap26", 1), exag=0.7, pre=0.25, round=(2, "LA PREPARACIÓN"),
     shots=[S(None, X(46.6), cx=0.5, z=(1.0, 1.1)),
            S("guarda la partida", "g:save"),
            S("barritas de proteína", X(55.6), cx=0.5, z=(1.05, 1.2), label="+ RESISTENCIA"),
            S("para aguantar", X(61.0), cx=0.36, z=(1.0, 1.1)),
            S("la carta", X(69.42), cx=0.46, z=(1.0, 1.12), speed=0.5),
            S("casas de empeño", X(69.42), cont=True, cx=0.4, cy=0.5, z=(1.15, 1.3), label="SE VENDE EN CASAS DE EMPEÑO")],
     sfx=[("w:guarda", "pop", 0.4), ("w:barritas", "pop", 0.35), ("w:la carta", "pop", 0.35)])
beat("Toca la caravana. A la primera te echa; puedes tirarle latas solo por diversión. A la segunda, sale él: The Gentrifier.",
     mus=("trap26", 2), exag=0.75, pre=0.25, round=(3, "EL COMBATE"),
     shots=[S(None, X(78.0), cx=0.5, z=(1.0, 1.08)),
            S("A la primera", X(78.0), cont=True, cx=0.5, z=(1.1, 1.2), label="1ª VEZ: TE ECHA"),
            S("tirarle latas", X(86.0), cx=0.44, z=(1.0, 1.1)),
            S("A la segunda", X(94.2), cx=0.36, z=(1.0, 1.1), punch=0.04),
            S("sale él", X(94.97), cx=0.55, z=(1.12, 1.0), flash=True, minwin=0.3),
            S("The Gentrifier", "g:vs")],
     sfx=[("w:Toca", "tick", 0.4), ("w:latas", "pop", 0.35), ("w:sale", "ding", 0.6), ("w:The Gentrifier", "hit", 0.5)])
beat("Machaca el botón para soltarte de sus llaves. Y cuando suba a la tercera cuerda, esquiva su salto: si te cae encima, estás muerto.",
     mus=("trap26", 2), exag=0.8, pre=0.2, round=(3, "EL COMBATE"),
     shots=[S(None, X(97.0), cx=0.46, z=(1.05, 1.15), punch=0.04, mash=True),
            S("sus llaves", X(48.8), cx=0.4, z=(1.0, 1.1), punch=0.06),
            S("la tercera cuerda", X(102.4), cx=0.45, cy=0.42, z=(1.0, 1.18)),
            S("esquiva su salto", X(106.3), cx=0.42, z=(1.0, 1.1), label="¡RUEDA!"),
            S("si te cae encima", X(112.1), cx=0.45, cy=0.4),
            S("estás muerto", X(113.2), cx=0.45, cy=0.35, freeze=0.0, minwin=0.05, cf="bw", big=("SI TE CAE ENCIMA:", "ESTÁS MUERTO"))],
     sfx=[(0.0, "hit", 0.4), ("w:sus llaves", "hit", 0.45), ("w:esquiva", "whoosh", 0.45), ("w:estás muerto", "stamp", 0.6)])
beat("Si falla, ahora subes tú… y se acabó.",
     mus=("trap26", 2), exag=0.85, pre=0.15, round=(3, "EL COMBATE"),
     shots=[S(None, X(114.15), cx=0.46, z=(1.1, 1.0), punch=0.07, flash=True),
            S("subes tú", X(117.55), cx=0.45, z=(1.0, 1.15)),
            S("se acabó", X(120.25), cx=0.45, z=(1.1, 1.0), punch=0.08, flash=True)],
     sfx=[(0.0, "hit", 0.6), ("w:se acabó", "hit", 0.7)])
beat("¿El premio? En su caravana: adrenalina y una máscara de luchador para tapar tu cara en los golpes.",
     mus=("trap26", 1), exag=0.7, pre=0.3, round=(4, "EL PREMIO"),
     shots=[S(None, X(120.25), cont=True, cx=0.45, z=(1.0, 1.08)),
            S("En su caravana", X(123.3), cx=0.5, z=(1.0, 1.08)),
            S("adrenalina", X(123.3), cont=True, cx=0.5, cy=0.55, z=(1.2, 1.35), label="ADRENALINA"),
            S("una máscara", X(127.42), cx=0.48, z=(1.0, 1.12), label="MÁSCARA DE LUCHADOR"),
            S("tapar tu cara", X(129.9), cx=0.88, cy=0.4, z=(1.3, 1.45))],
     sfx=[("w:premio", "ding", 0.5), ("w:máscara", "pop", 0.4)])
beat("¿Te subes al ring?",
     mus=("trap26", 2), exag=0.75, pre=0.25, round=None, hold=0.6,
     shots=[S(None, X(110.0), cx=0.44, cy=0.45, z=(1.0, 1.15), flash=True)],
     sfx=[(0.0, "ding", 0.6)])

# ================================================================ ESCENA
CF = {"bw": SR.color_matrix(sat=0.0, contrast=1.15, bright=0.07)}

def _still(t, size=(1080, 960), cx=0.5, cy=0.5):
    """Fotograma del gameplay como imagen (para la tarjeta VS y la portada)."""
    import subprocess
    path = G.x_path(V1); m = G._clip_meta(path); tw, th = size
    x, y, w, h = SR.window(m, None, tw / th, 1.0, 0.0, 0.0)
    cw = w; x = int(max(0, min(m["w"] - cw, cx * m["w"] - cw / 2))) // 2 * 2; y = int(max(0, min(m["h"] - h, cy * m["h"] - h / 2))) // 2 * 2
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf",
                          f"crop={cw}:{h}:{x}:{y},scale={tw}:{th}:flags=bicubic,format=rgba", "-f", "rawvideo", "-"], capture_output=True).stdout
    return skia.Image.fromarray(np.frombuffer(raw, np.uint8).reshape(th, tw, 4).copy(), colorType=skia.ColorType.kRGBA_8888_ColorType)

_ST = {}
def still(key, *a, **k):
    if key not in _ST: _ST[key] = _still(*a, **k)
    return _ST[key]

def g_save(c, tau, d, sh, ctx):
    rect(c, 0, 0, SR.W, SR.H, INK, 1)
    for k in range(14): rect(c, 0, 120 + k * 130, SR.W, 2, RED, 0.18)
    p = ease_out_back(prog(tau, 0, 0.35)); c.save(); c.translate(540, 640); c.scale(p, p)
    rect(c, -170, -170, 340, 340, GOLD, 1, r=26); rect(c, -110, -170, 220, 120, INK, 1, r=6); rect(c, 30, -150, 50, 80, GOLD, 1)
    rect(c, -120, 20, 240, 130, "#FFFFFF", 1, r=10)
    for k in range(3): rect(c, -90, 50 + k * 32, 180, 8, INK, 0.6)
    c.restore()
    draw_text(c, "GUARDA", 540, 980, "anton", 150, "#FFFFFF", clamp(prog(tau, 0.1, 0.3) * 3), align="center", tracking=4)
    draw_text(c, "LA PARTIDA", 540, 1100, "anton", 110, GOLD, clamp(prog(tau, 0.15, 0.35) * 3), align="center", tracking=4)
    q = ease_out(prog(tau, 0.35, 0.6)); rect(c, 540 - 300, 1150, 600, 70, RED, q, r=8)
    draw_text(c, "PUEDES PERDER", 540, 1200, "ovblk", 40, "#FFFFFF", q, align="center", tracking=3)

def g_vs(c, tau, d, sh, ctx):
    rect(c, 0, 0, SR.W, SR.H, INK, 1)
    top = still("jason", 118.5, (1080, 960), cx=0.45, cy=0.5); bot = still("gentri", 104.4, (1080, 960), cx=0.45, cy=0.45)
    p = ease_out(prog(tau, 0, 0.3)); q = ease_out(prog(tau, 0.08, 0.38))
    c.save(); path = skia.Path(); path.moveTo(0, 0); path.lineTo(SR.W, 0); path.lineTo(SR.W, 860); path.lineTo(0, 1000); path.close()
    c.clipPath(path, True); c.translate(-(1 - p) * 300, 0); c.drawImageRect(top, skia.Rect.MakeXYWH(0, 0, 1080, 960)); c.restore()
    c.save(); path = skia.Path(); path.moveTo(0, 1060); path.lineTo(SR.W, 920); path.lineTo(SR.W, SR.H); path.lineTo(0, SR.H); path.close()
    c.clipPath(path, True); c.translate((1 - q) * 300, 0); c.drawImageRect(bot, skia.Rect.MakeXYWH(0, 940, 1080, 980)); c.restore()
    draw_poly(c, [(0, 1000), (SR.W, 860), (SR.W, 920), (0, 1060)], GOLD, 1)
    s = ease_out_back(prog(tau, 0.2, 0.5), 2.4); c.save(); c.translate(540, 960); c.scale(s, s); c.rotate(-8)
    circle(c, 0, 0, 120, RED, 1); circle(c, 0, 0, 120, "#FFFFFF", 1, stroke=10)
    draw_text(c, "VS", 0, 52, "anton", 150, "#FFFFFF", 1, align="center"); c.restore()
    for (txt, y, al, x, a) in (("JASON", 300, "left", 60, p), ("THE GENTRIFIER", 1700, "right", 1020, q)):
        f = font("anton", 112); w = text_w(txt, f, 3); xx = x if al == "left" else x - w
        rect(c, xx - 24, y - 112, w + 48, 136, INK, 0.82 * a, r=8)
        draw_text(c, txt, xx, y, "anton", 112, GOLD if al == "right" else "#FFFFFF", a, tracking=3)

def g_end(c, tau, d, sh, ctx): rect(c, 0, 0, SR.W, SR.H, INK, 1)
GFX = {"save": g_save, "vs": g_vs, "end": g_end}

def draw_shot(c, sh, tau, d, ctx, slot):
    k, v = sh["src"].split(":", 1)
    if k == "g": GFX[v](c, tau, d, sh, ctx); return
    sh2 = dict(sh); sh2["cf"] = CF.get(sh.get("cf")) if isinstance(sh.get("cf"), str) else sh.get("cf")
    SR.footage(c, sh2, tau, d, (0, 0, SR.W, SR.H), slot)
    # degradados para que se lean los rótulos
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, 420)], [skia.Color(0, 0, 0, 170), skia.Color(0, 0, 0, 0)]))
    c.drawRect(skia.Rect.MakeWH(SR.W, 420), g)
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 1100), (0, SR.H)], [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 200)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1100, SR.W, SR.H - 1100), g)
    if sh.get("big"):
        a_, b_ = sh["big"]; p = ease_out_back(prog(tau, 0.02, 0.25), 2.0)
        c.save(); c.translate(540, 760); c.scale(1.6 - 0.6 * p, 1.6 - 0.6 * p); c.rotate(-4)
        for txt, y, col, sz in ((a_, -40, "#FFFFFF", 96), (b_, 80, RED, 128)):
            f = font("anton", sz); w = text_w(txt, f, 2)
            rect(c, -w / 2 - 24, y - sz * 0.92, w + 48, sz * 1.12, INK, 0.85 * clamp(p * 2), r=8)
            draw_text(c, txt, 0, y, "anton", sz, col, clamp(p * 2), align="center", tracking=2)
        c.restore()
    if sh.get("label"):
        p = ease_out_back(prog(tau, 0.05, 0.3)) * (1 - prog(tau, d - 0.15, d))
        if p > 0:
            f = font("anton", 66); w = text_w(sh["label"], f, 3) + 56
            c.save(); c.translate(540, 1080); c.scale(p, p)
            rect(c, -w / 2, -60, w, 84, GOLD, 1, r=6); draw_text(c, sh["label"], 0, 6, "anton", 66, INK, 1, align="center", tracking=3); c.restore()
    if sh.get("tag"):
        txt, x, y = sh["tag"]; p = ease_out_back(prog(tau, 0.15, 0.45)); X0, Y0 = x * SR.W, y * SR.H
        circle(c, X0, Y0, 26 * p + 8 * pulse(tau, 0.7), RED, 1); circle(c, X0, Y0, 46 * p, RED, 0.6, stroke=6)
        f = font("anton", 90); w = text_w(txt, f, 3)
        rect(c, X0 - w / 2 - 22, Y0 - 190, w + 44, 112, INK, 0.85 * p, r=8); draw_text(c, txt, X0, Y0 - 104, "anton", 90, GOLD, p, align="center", tracking=3)
    if sh.get("mash"):
        for k in range(3):
            ph = (tau * 7 + k * 0.33) % 1.0; s = 1.0 + 0.25 * (1 - ph)
            c.save(); c.translate(380 + k * 160, 1080); c.scale(s, s)
            circle(c, 0, 0, 52, "#FFFFFF", 0.95); circle(c, 0, 0, 52, RED, 1, stroke=8); draw_text(c, "X", 0, 22, "anton", 60, INK, 1, align="center")
            c.restore()
        draw_text(c, "¡MACHÁCALO!", 540, 1220, "anton", 84, GOLD, 1, align="center", tracking=3)

_scene = SR.make_scene(draw_shot, trans=lambda a, b: 0.12 if (a["src"].startswith("g:") or b["src"].startswith("g:")) else None)

def overlay(c, gt, ctx):
    sh, b, i, bi = SR.current(ctx, gt)
    if not sh["src"].startswith("g:"):
        # «bug» de retransmisión y crédito discreto
        rect(c, 44, 56, 300, 52, INK, 0.82, r=6); circle(c, 74, 82, 11, RED, 0.5 + 0.5 * pulse(gt, 1.0))
        draw_text(c, "B.A.M. · EN VIVO", 96, 95, "anton", 36, "#FFFFFF", 1, tracking=2)
        SR.credit(c, sh, y=118)
    r = b.get("round")
    if r:
        T = G.table(ctx); st = T["bstarts"][bi]; tt = gt - st
        n, name = r; p = ease_out(prog(tt, 0, 0.3)) * (1 - prog(tt, 1.6, 1.9))
        if p > 0 and not (bi > 0 and T["beats"][bi - 1]["b"].get("round") == r):
            c.save(); c.translate(0, -(1 - p) * 60)
            rect(c, 0, 200, SR.W, 150, RED, 0.92 * p); draw_text(c, f"RONDA {n}", 540, 262, "ovblk", 40, GOLD, p, align="center", tracking=8)
            draw_text(c, name, 540, 334, "anton", 70, "#FFFFFF", p, align="center", tracking=4); c.restore()
        elif not (p > 0):
            draw_text(c, f"R{n} · {name}", 1036, 95, "anton", 34, GOLD, 0.95, align="right", tracking=2)
    SR.subs_kinetic(c, gt, ctx, y=1330)

# ================================================================ MÚSICA, PORTADA Y DATOS
def music_fn(total, beats_tl):
    en = [(bd["start"], b.get("mus", ("trap26", 1))[1]) for b, bd in zip(B, beats_tl)]
    y = audio.compose("trap26", total, energy=en, seed=4101, key_shift=-2)
    return y / (np.abs(y).max() + 1e-9) * 0.8

def thumbnail(c):
    img = still("portada", 110.6, (1080, 1920), cx=0.44, cy=0.45)
    c.drawImageRect(img, skia.Rect.MakeWH(1080, 1920))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 1000), (0, 1920)], [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 235)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1000, 1080, 920), g)
    rect(c, 60, 1180, 440, 92, RED, 1, r=8); draw_text(c, "GTA 6", 280, 1250, "anton", 80, "#FFFFFF", 1, align="center", tracking=4)
    draw_text(c, "EL RING", 70, 1440, "anton", 190, "#FFFFFF", 1, tracking=4)
    draw_text(c, "SECRETO", 70, 1620, "anton", 190, GOLD, 1, tracking=4)
    draw_text(c, "UN ERROR = MUERTO", 74, 1720, "ovblk", 52, "#FFFFFF", 0.95, tracking=3)

VIDEO = dict(id="s01", folder="SHORT_01", file="VIDEO_FINAL", size=(1080, 1920), thumb_size=(1080, 1920),
             title="GTA 6 tiene un ring de lucha libre secreto (y un error te mata)", format="Short vertical (9:16)",
             music="trap26", music_fn=music_fn, voice="host", beats=B, overlay=overlay, grade=None, music_gain=0.5,
             lead_in=0.1, tail=0.6, trim_tail=True, max_tries=3, qa_metric="fonetica", qa_thr=0.995, trans=("cut", 0.0),
             names=dict(narr_wav="recursos/narracion_original.flac", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="recursos/guion_con_tiempos.txt", thumb="PORTADA.png"))
THUMB_MARK = None
