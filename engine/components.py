"""Componentes de marca reutilizables (con estilo configurable por vídeo)."""
import math, numpy as np, skia
from gfx import *
from brand import PAL, draw_caiman, wordmark

CERT = {"OFICIAL": PAL["caiman"], "DEDUCCIÓN": PAL["sol"], "RUMOR": PAL["flamenco"], "SIN CONFIRMAR": PAL["flamenco"],
        "REPORTADO": PAL["laguna"], "HIPÓTESIS": PAL["sol"], "COMPROBAR EN EL JUEGO": PAL["laguna"]}

def cert_tag(c, x, y, kind, a=1.0, size=30, align="left", t=1.0):
    """Etiqueta del semáforo de certeza. t = progreso de aparición 0..1."""
    if a <= 0 or t <= 0: return 0
    col = CERT.get(kind, PAL["hueso"]); f = font("monob", size); w = text_w(kind, f, 2) + size * 1.4 + size * 0.9; h = size * 1.6
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    s = ease_out_back(clamp(t)); c.save(); c.translate(x + w / 2, y + h / 2); c.scale(s, s); c.translate(-(x + w / 2), -(y + h / 2))
    rect(c, x, y, w, h, PAL["tinta"], 0.82 * a, r=h / 2); rect(c, x, y, w, h, col, a, r=h / 2, stroke=max(2, size / 12))
    circle(c, x + size * 0.85, y + h / 2, size * 0.26, col, a); circle(c, x + size * 0.85, y + h / 2, size * 0.5, col, 0.25 * a * pulse(t * 3, 1))
    draw_text(c, kind, x + size * 1.5, y + h / 2 + size * 0.36, "monob", size, col, a, tracking=2)
    c.restore(); return w

def source_chip(c, x, y, txt, a=1.0, size=22, color=None):
    if a <= 0: return
    f = font("mono", size); w = text_w("FUENTE · " + txt, f, 1) + size * 1.4; h = size * 1.7
    rect(c, x, y, w, h, "#000000", 0.55 * a, r=6); rect(c, x, y, 4, h, color or PAL["laguna"], a)
    draw_text(c, "FUENTE · " + txt, x + size * 0.8, y + h * 0.68, "mono", size, PAL["hueso"], 0.9 * a, tracking=1)

def brand_sting(c, t, info, ctx, accent=None):
    """Cortinilla de marca (≈2.4 s): caimán neón se 'enciende' y muerde."""
    W, H = ctx.W, ctx.H; c.clear(hexc(PAL["noche"]))
    c.drawCircle(W / 2, H / 2, max(W, H) * 0.6, rad_grad(W / 2, H / 2, max(W, H) * 0.6, [hexc("#14302A"), hexc(PAL["noche"])]))
    flick = 1.0 if t > 0.5 else (0.3 if int(t * 30) % 3 == 0 else 1.0) * clamp(t / 0.15)
    s = min(W, H) / 1080.0
    open_ = 0.0
    if 0.45 < t < 0.62: open_ = math.sin((t - 0.45) / 0.17 * math.pi) * 1.4
    cw = 200 * 3.0 * s; draw_caiman(c, W / 2 - cw / 2 - 30 * s, H * 0.5 - 240 * s, 3.0 * s, t=1.0, a=flick, open_=open_)
    p = ease_out(prog(t, 0.6, 1.1))
    if p > 0:
        c.save(); ww = 120 * s
        tw = text_w("CAIMÁN", font("anton", ww), ww * 0.02) + ww * 0.22 + text_w("NEÓN", font("anton", ww), ww * 0.02)
        c.translate(0, (1 - p) * 30); wordmark(c, W / 2 - tw / 2, H * 0.5 + 170 * s, ww, a=p); c.restore()
    if t > 1.9: rect(c, 0, 0, W, H, "#000000", clamp((t - 1.9) / 0.5))

def end_screen(c, t, info, ctx, title="", sub="", accent=None):
    """Pantalla final (20 s): dos huecos para elementos de YouTube + botón de suscripción."""
    W, H = ctx.W, ctx.H; accent = accent or PAL["caiman"]
    c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, [PAL["noche"], "#101B2A", "#0E2A24"]))
    grid(c, W, H, 60, PAL["laguna"], 0.04, oy=t * 8)
    bokeh(c, W, H, t, 16, (PAL["caiman"], PAL["flamenco"], PAL["laguna"]), seed=9, a=0.08)
    p = ease_out(prog(t, 0, 0.8))
    draw_text(c, title or "SIGUE EXPLORANDO", W / 2, 150, "anton", 84, PAL["hueso"], p, align="center", tracking=2)
    if sub: draw_text(c, sub, W / 2, 205, "intermd", 32, PAL["hueso"], 0.8 * p, align="center")
    # huecos de vídeo (las tarjetas reales se añaden en YouTube Studio encima)
    for i, x in enumerate((180, 1020)):
        pp = ease_out_back(prog(t, 0.3 + i * 0.15, 1.0))
        c.save(); c.translate(x + 360, 590); c.scale(pp, pp); c.translate(-(x + 360), -590)
        rect(c, x, 388, 720, 405, "#000000", 0.35, r=16)
        rect(c, x, 388, 720, 405, accent if i == 0 else PAL["flamenco"], 0.9, r=16, stroke=4)
        draw_text(c, "VIDEO RECOMENDADO" if i == 0 else "LISTA: GTA VI EXPLICADO", x + 360, 600, "monob", 30, PAL["hueso"], 0.5, align="center", tracking=3)
        c.restore()
    # suscripción
    pp = ease_out_back(prog(t, 0.6, 1.3))
    c.save(); c.translate(W / 2, 935); c.scale(pp, pp)
    circle(c, 0, 0, 92, PAL["noche"], 1); circle(c, 0, 0, 92, accent, 1, stroke=5)
    draw_caiman(c, -82, -38, 0.82, t=t, lw=4, glow=False)
    c.restore()
    draw_text(c, "SUSCRÍBETE · ACTIVA LA CAMPANA", W / 2 + 130, 950, "monob", 28, PAL["hueso"], pp * 0.9, tracking=2)

def watermark(c, W, H, a=0.55, corner="br", size=64):
    x = W - size - 34 if corner[1] == "r" else 34; y = H - size - 30 if corner[0] == "b" else 30
    circle(c, x + size / 2, y + size / 2, size / 2, PAL["noche"], 0.6 * a); circle(c, x + size / 2, y + size / 2, size / 2 - 2, PAL["caiman"], 0.8 * a, stroke=2)
    draw_caiman(c, x + 4, y + size * 0.27, size / 230, lw=6, glow=False, a=a)

def word_times(sent):
    words = sent["text"].split(); tot = sum(len(w) + 1 for w in words); d = sent["end"] - sent["start"]; acc = 0; out = []
    for w in words:
        st = sent["start"] + d * acc / tot; acc += len(w) + 1; out.append((w, st, sent["start"] + d * acc / tot))
    return out

def short_captions(c, gt, ctx, y=1350, size=74, hl=PAL["caiman"], fontname="anton", maxw=900, box=True):
    """Subtítulos grandes palabra a palabra para Shorts (tiempo global gt)."""
    cur = None
    for b in ctx.tl["beats"]:
        for s in b["sents"]:
            if s["start"] - 0.05 <= gt <= s["end"] + 0.25: cur = s
    if not cur: return
    wt = word_times(cur)
    # agrupar en bloques de ≤ 3 palabras para lectura rápida
    chunks = []; i = 0
    while i < len(wt):
        chunk = wt[i:i + 3]; chunks.append(chunk); i += 3
    act = None
    for ch in chunks:
        if ch[0][1] - 0.02 <= gt <= ch[-1][2] + 0.25: act = ch
    if act is None: return
    words = [w for w, _, _ in act]; W = ctx.W
    f = font(fontname, size); sp = size * 0.28
    total = sum(text_w(w.upper(), f) for w in words) + sp * (len(words) - 1)
    sc = min(1.0, maxw / total); fs = size * sc; f = font(fontname, fs); total *= sc; sp *= sc
    x = W / 2 - total / 2; pop = ease_out_back(prog(gt, act[0][1] - 0.02, act[0][1] + 0.16))
    c.save(); c.translate(W / 2, y); c.scale(0.85 + 0.15 * pop, 0.85 + 0.15 * pop); c.translate(-W / 2, -y)
    if box: rect(c, x - 30, y - fs * 1.0, total + 60, fs * 1.35, "#000000", 0.55, r=18)
    for w, st, en in act:
        on = st <= gt
        col = hl if (st <= gt <= en + 0.05) else PAL["hueso"]
        ww = draw_text(c, w.upper(), x, y, fontname, fs, col, 1.0 if on else 0.45, stroke=fs * 0.09, stroke_color="#000000")
        x += ww + sp
    c.restore()

def ai_notice(c, W, H, a=1.0, text="Ilustraciones y animaciones originales · no son imágenes del juego"):
    draw_text(c, text, W - 36, H - 30, "mono", 18, PAL["hueso"], 0.55 * a, align="right")

def count_up(val, p, fmt="{:,.0f}"):
    return fmt.format(val * ease_out(clamp(p))).replace(",", ".")

def kinetic_words(c, txt, x, y, t, fname, size, color, accent=None, accent_words=(), stagger=0.06, align="left", tracking=0, maxw=None, lh=1.05):
    """Palabras que suben y aparecen escalonadas; las de `accent_words` en color de acento."""
    lines = wrap(txt, fname, size, maxw or 10000, tracking); f = font(fname, size); k = 0
    for li, L in enumerate(lines):
        ws = L.split(); total = text_w(L, f, tracking); xx = x - (total / 2 if align == "center" else total if align == "right" else 0)
        for w in ws:
            p = ease_out(prog(t, k * stagger, k * stagger + 0.35))
            col = accent if (accent and w.strip(".,:;!?¿¡").upper() in [a.upper() for a in accent_words]) else color
            draw_text(c, w, xx, y + li * size * lh + (1 - p) * size * 0.4, fname, size, col, p, tracking=tracking)
            xx += text_w(w + " ", f, tracking); k += 1
    return len(lines) * size * lh
