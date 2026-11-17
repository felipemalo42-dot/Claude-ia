"""VIDEO 10 — POST-LANZAMIENTO: Abrimos los 7 sobres — comprobamos los misterios de GTA 6 JUGANDO.
ESTADO: PREPRODUCCIÓN. Requiere capturas propias del juego tras el 19/11/2026.
Este módulo genera: (1) un ANIMÁTICO de referencia (no publicable) con la narración que ya puede grabarse,
huecos rotulados para las capturas y veredictos en blanco; (2) rótulos PNG transparentes para la edición final;
(3) la miniatura definitiva (válida sea cual sea el resultado).
"""
import math, os, numpy as np, skia
from gfx import *
from components import *
from brand import PAL, draw_caiman, draw_badge
from videos.v09 import velvet, envelope, candle, gauge, MYST, GOLD, WAX, LAV, WHITE, SUN

TEST = [  # protocolo de verificación por sobre
    "Menú principal y Newswire de Rockstar del 19-20 nov.: ¿hay opción online o fecha anunciada?",
    "Menú de ajustes gráficos en PS5 / PS5 Pro / Series X: ¿existe modo rendimiento o 60 fps?",
    "Recorrido fijo de 3 zonas (centro de Vice City, Port Gellhorn, Ambrosia): contar edificios con interior.",
    "Misma zona, dos estilos de juego (agresivo vs. discreto) durante 2 h: anotar reacciones del mundo.",
    "10 días de juego libre: ¿aparece un huracán fuera de misión? Registrar fecha y hora del juego.",
    "Menú o compendio de fauna: ¿qué especies figuran como legendarias? (sin revelar ubicaciones).",
    "Mapa del menú: contar regiones con nombre y anotar zonas nuevas sin spoilers de historia.",
]

def slot(c, x, y, w, h, txt, t):
    rect(c, x, y, w, h, "#000000", 0.55, r=12)
    pp = paint("#FFFFFF", 0.7, stroke=4); pp.setPathEffect(skia.DashPathEffect.Make([18, 12], -t * 20))
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 12, 12, pp)
    icon(c, "film", x + w / 2, y + h / 2 - 70, 90, "#FFFFFF", 0.8)
    draw_text(c, "INSERTAR CAPTURA PROPIA", x + w / 2, y + h / 2 + 20, "monob", 30, SUN, 1, align="center", tracking=3)
    draw_par(c, txt, x + 40, y + h / 2 + 75, "intermd", 26, w - 80, color=WHITE, a=0.9)

def animatic_band(c, W, H):
    rect(c, 0, 0, W, 54, "#C1121F", 0.92)
    draw_text(c, "ANIMÁTICO DE PREPRODUCCIÓN · NO PUBLICAR · FALTAN CAPTURAS Y VEREDICTOS", W / 2, 37, "monob", 26, "#FFFFFF", 1, align="center", tracking=2)

def sc_hook(c, t, info, ctx):
    W, H = ctx.W, ctx.H; velvet(c, W, H, t); candle(c, 1700, 780, t)
    for i in range(7):
        x = 300 + (i % 4) * 340 + (170 if i >= 4 else 0); y = 380 + (i // 4) * 330
        envelope(c, x, y, 0.55, i + 1, "", t, rot=[-6, 4, -3, 5, -4, 3, -5][i], open_p=ease_io(prog(t, info.w("los abrimos") + i * 0.2, info.w("los abrimos") + i * 0.2 + 0.6)))
    st = info.w("sin maquillar"); p = ease_out_back(prog(t, st, st + 0.4))
    if p > 0: c.save(); c.translate(W / 2, 960); c.scale(p, p); rect(c, -520, -60, 1040, 120, "#000000", 0.6, r=60); draw_text(c, "ACIERTOS Y FALLOS, SIN MAQUILLAR", 0, 22, "syne", 56, GOLD, 1, align="center"); c.restore()

def sc_sting(c, t, info, ctx): brand_sting(c, t, info, ctx)

def sc_rules(c, t, info, ctx):
    W, H = ctx.W, ctx.H; velvet(c, W, H, t)
    rows = [("CAPTURAS PROPIAS", "capturas"), ("SIN SPOILERS DE HISTORIA", "spoilers"), ("“SIN DATOS” ≠ ACIERTO", "sin datos")]
    for i, (lab, cue) in enumerate(rows):
        st = info.w(cue); p = ease_out(prog(t, st, st + 0.4)); y = 300 + i * 200
        if p <= 0: continue
        rect(c, 360, y, 1200, 150, "#000000", 0.5 * p, r=16); rect(c, 360, y, 8, 150, GOLD, p)
        draw_text(c, lab, 420, y + 95, "syne", 64, WHITE, p)

def make_open(i):
    m = MYST[i]
    def sc(c, t, info, ctx):
        W, H = ctx.W, ctx.H; velvet(c, W, H, t)
        envelope(c, 300, 300, 0.55, i + 1, "", t, open_p=1.0)
        draw_text(c, f"SOBRE {i + 1}", 120, 520, "syne", 60, GOLD, 1)
        draw_par(c, m["q"], 120, 590, "syne", 40, 520, color=WHITE, lh=1.1)
        draw_text(c, "PREDICCIÓN", 120, 760, "monob", 24, SUN, 1, tracking=3)
        draw_par(c, f"{m['pred']} ({int(m['conf'] * 100)} %)", 120, 810, "intersb", 32, 520, color=WHITE)
        slot(c, 700, 140, 1120, 630, TEST[i], t)
        # veredicto en blanco (se decide tras las pruebas)
        rect(c, 700, 810, 1120, 150, "#000000", 0.6, r=16); rect(c, 700, 810, 1120, 150, LAV, 1, r=16, stroke=3)
        draw_text(c, "VEREDICTO: PENDIENTE DE COMPROBAR EN EL JUEGO", 1260, 900, "syne", 38, LAV, 1, align="center")
        animatic_band(c, W, H)
    return sc

def sc_score(c, t, info, ctx):
    W, H = ctx.W, ctx.H; velvet(c, W, H, t)
    draw_text(c, "MARCADOR FINAL", W / 2, 180, "syne", 90, GOLD, 1, align="center")
    for i in range(7):
        x = 230 + i * 245; envelope(c, x, 470, 0.42, i + 1, "", t, open_p=1.0)
        draw_text(c, "?", x, 700, "syne", 120, LAV, 0.8, align="center")
    draw_text(c, "ACIERTOS: ?  ·  FALLOS: ?  ·  SIN DATOS: ?", W / 2, 900, "monob", 44, WHITE, 1, align="center", tracking=2)
    animatic_band(c, W, H)

def sc_end(c, t, info, ctx):
    end_screen(c, t, info, ctx, "¿QUÉ COMPROBAMOS AHORA?", "Propón la próxima prueba en los comentarios", GOLD)
    animatic_band(c, ctx.W, ctx.H)

def overlay(c, gt, ctx):
    if 2.5 < gt < ctx.total - 20: watermark(c, ctx.W, ctx.H, 0.45)

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))
beat("Hace unos días metimos siete preguntas sobre GTA 6 en sobres sellados, cada una con una predicción y un porcentaje de confianza. Hoy, con el juego en las manos, los abrimos. "
     "Y vamos a contar los aciertos y los fallos, sin maquillar ninguno.",
     sc_hook, section="GANCHO (narración lista)", energy=1, sfx=[("w:los abrimos", "seal", 0.6), ("w:sin maquillar", "hit", 0.5)])
beat("", sc_sting, dur=2.4, sfx=[(0.0, "logo", 0.9)], energy=1, trans=("flash", 0.3))
beat("Las reglas. Todas las pruebas son capturas nuestras, jugando. Nada de spoilers de la historia más allá de las primeras horas. "
     "Y si algo todavía no se puede comprobar, lo marcamos como sin datos, no como acierto.",
     sc_rules, section="REGLAS (narración lista)", energy=1, trans=("zoom", 0.5), sfx=[("w:capturas", "pop", 0.4), ("w:spoilers", "pop", 0.4), ("w:sin datos", "pop", 0.4)])
for i, m in enumerate(MYST):
    beat(f"Sobre {['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete'][i]}: {m['q'].capitalize().replace('¿c', '¿C').replace('¿h', '¿H').replace('¿q', '¿Q')} "
         f"Nuestra predicción fue: {m['pred'].lower()}.",
         make_open(i), section=f"SOBRE {i + 1} — [GRABAR PRUEBA] + [ESCRIBIR Y GRABAR VEREDICTO]", hold=8.0, energy=1, trans=("slide_up", 0.5),
         note=f"PROTOCOLO: {TEST[i]}", sfx=[(0.2, "seal", 0.5)])
beat("", sc_score, dur=8.0, section="MARCADOR — [COMPLETAR CON RESULTADOS REALES]", energy=2, trans=("fade", 0.5))
beat("¿Qué otra pregunta quieres que comprobemos jugando? Déjala en los comentarios. Y si quieres más pruebas con método, suscríbete a Sal y Asfalto.",
     sc_end, section="LLAMADA A LA ACCIÓN (narración lista)", energy=2, hold=4.0, min=20, trans=("fade", 0.6))

VIDEO = dict(id="v10", folder="VIDEO_10", file="V10_ANIMATICO_preproduccion_NO_PUBLICAR",
             title="Abrimos los 7 sobres: comprobamos los misterios de GTA 6 jugando (¿acertamos?)",
             format="Largo (16:9) · POST-LANZAMIENTO · animático de preproducción", music="mystery", music_seed=101, voice="host",
             beats=B, overlay=overlay, music_gain=0.5)

def thumbnail(c):
    W, H = 1280, 720
    velvet(c, W, H, 0.3)
    for i, (x, y, rot) in enumerate(((260, 300, -8), (520, 250, 5), (380, 500, -3))):
        envelope(c, x, y, 0.6, [1, 4, 7][i], "", 0.3, open_p=1.0, rot=rot)
    draw_text(c, "ABRIMOS", 740, 230, "syne", 110, WHITE, 1)
    draw_text(c, "LOS 7", 740, 350, "syne", 130, GOLD, 1)
    draw_text(c, "SOBRES", 740, 470, "syne", 110, WHITE, 1)
    rect(c, 740, 510, 470, 90, SUN, 1, r=12); draw_text(c, "¿ACERTAMOS?", 975, 572, "syne", 56, "#1B1040", 1, align="center")
    draw_text(c, "GTA VI · PROBADO JUGANDO", 70, 680, "monob", 36, WHITE, 0.9, tracking=2)

def overlays_png(outdir):
    """Rótulos transparentes 1920x1080 para la edición final en cualquier editor."""
    os.makedirs(outdir, exist_ok=True)
    def save(fn, draw):
        s = new_surface(1920, 1080); cc = s.getCanvas(); cc.clear(skia.ColorTRANSPARENT); draw(cc); s.makeImageSnapshot().save(f"{outdir}/{fn}", skia.kPNG)
    for lab, col in (("ACERTAMOS", PAL["caiman"]), ("FALLAMOS", PAL["flamenco"]), ("A MEDIAS", SUN), ("SIN DATOS", LAV)):
        def d(cc, lab=lab, col=col):
            cc.save(); cc.translate(960, 540); cc.rotate(-8)
            w = text_w(lab, font("syne", 150), 8) + 140
            rect(cc, -w / 2, -130, w, 260, "#000000", 0.55, r=26); rect(cc, -w / 2, -130, w, 260, col, 1, r=26, stroke=14)
            draw_text(cc, lab, 0, 55, "syne", 150, col, 1, align="center", tracking=8); cc.restore()
        save(f"veredicto_{lab.replace(' ', '_')}.png", d)
    def lt(cc):
        rect(cc, 60, 880, 820, 120, "#000000", 0.75, r=14); rect(cc, 60, 880, 10, 120, GOLD, 1)
        draw_text(cc, "CAPTURA PROPIA", 100, 935, "syne", 44, WHITE, 1); draw_text(cc, "GTA VI · consola: ____ · fecha: __/11/2026", 100, 980, "monob", 26, GOLD, 1)
    save("rotulo_captura_propia.png", lt)
    for i, m in enumerate(MYST):
        def d(cc, i=i, m=m):
            rect(cc, 60, 60, 900, 170, "#000000", 0.75, r=16); rect(cc, 60, 60, 10, 170, GOLD, 1)
            draw_text(cc, f"SOBRE {i + 1} · PRUEBA", 100, 115, "monob", 26, GOLD, 1, tracking=3)
            draw_par(cc, m["q"], 100, 170, "syne", 44, 840, color=WHITE)
        save(f"rotulo_sobre_{i + 1}.png", d)
