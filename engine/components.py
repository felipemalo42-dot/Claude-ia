"""Componentes de marca reutilizables — identidad SAL Y ASFALTO (señalización vial, semáforo de certeza)."""
import math, numpy as np, skia
from gfx import *
from brand import PAL, wordmark, draw_badge, guide_sign, traffic_light, coast_scene, BRAND

CERT = {"OFICIAL": (PAL["verde"], 0), "DEDUCCIÓN": (PAL["ambar"], 1), "RUMOR": (PAL["rojo"], 2), "SIN CONFIRMAR": (PAL["rojo"], 2),
        "REPORTADO": (PAL["mar"], None), "HIPÓTESIS": (PAL["ambar"], 1), "COMPROBAR EN EL JUEGO": (PAL["mar"], None)}

def cert_tag(c, x, y, kind, a=1.0, size=30, align="left", t=1.0):
    """Etiqueta del semáforo de certeza: mini semáforo + rótulo. t = progreso de aparición 0..1."""
    if a <= 0 or t <= 0: return 0
    col, lit = CERT.get(kind, (PAL["sal"], None)); f = font("ovmono", size); h = size * 1.6
    lw = h * 0.42 if lit is not None else size * 0.5
    w = text_w(kind, f, 1) + lw + size * 1.4
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    s = ease_out_back(clamp(t)); c.save(); c.translate(x + w / 2, y + h / 2); c.scale(s, s); c.translate(-(x + w / 2), -(y + h / 2))
    rect(c, x, y, w, h, PAL["asfalto"], 0.9 * a, r=h * 0.2); rect(c, x, y, w, h, col, a, r=h * 0.2, stroke=max(2, size / 12))
    if lit is not None: traffic_light(c, x + size * 0.45, y + h * 0.1, h * 0.8, lit, a)
    else: rect(c, x + size * 0.45, y + h * 0.25, size * 0.5, h * 0.5, col, a, r=4)
    draw_text(c, kind, x + size * 0.45 + lw + size * 0.45, y + h / 2 + size * 0.36, "ovmono", size, col, a, tracking=1)
    c.restore(); return w

def source_chip(c, x, y, txt, a=1.0, size=22, color=None):
    if a <= 0: return
    f = font("ovmonomd", size); w = text_w("FUENTE · " + txt, f, 1) + size * 1.4; h = size * 1.7
    rect(c, x, y, w, h, "#000000", 0.6 * a, r=4); rect(c, x, y, 6, h, color or PAL["amarillo"], a)
    draw_text(c, "FUENTE · " + txt, x + size * 0.8, y + h * 0.68, "ovmonomd", size, PAL["sal"], 0.92 * a, tracking=1)

def brand_sting(c, t, info, ctx, accent=None):
    """Cortinilla de marca (≈2.4 s): viaje por la carretera costera que se cierra en el emblema y la señal SAL Y ASFALTO."""
    W, H = ctx.W, ctx.H; s = min(W, H) / 1080.0
    coast_scene(c, W, H, t * 2.2, hy=H * 0.48)
    # iris hacia el emblema
    p = ease_io(prog(t, 0.55, 1.15)); r_end = 210 * s; cx, cy = W / 2, H * 0.40
    if p > 0:
        R = lerp(math.hypot(W, H), r_end, p)
        mask = skia.Path(); mask.setFillType(skia.PathFillType.kEvenOdd); mask.addRect(skia.Rect.MakeWH(W, H)); mask.addCircle(cx, cy, R)
        c.drawPath(mask, paint(PAL["asfalto"], 1))
        if p >= 1: draw_badge(c, cx, cy, r_end, t=t)
        else: circle(c, cx, cy, R, PAL["sal"], p, stroke=16 * s)
    q = ease_out_back(prog(t, 1.05, 1.45))
    if q > 0:
        sw, sh = 900 * s, 150 * s; sy = H * 0.40 + r_end + 50 * s
        c.save(); c.translate(W / 2, sy + sh / 2); c.scale(q, q); c.translate(-W / 2, -(sy + sh / 2))
        guide_sign(c, W / 2 - sw / 2, sy, sw, sh)
        wordmark(c, W / 2, sy + sh * 0.68, 80 * s, align="center")
        c.restore()
    if t > 1.95: rect(c, 0, 0, W, H, "#000000", clamp((t - 1.95) / 0.45))

def end_screen(c, t, info, ctx, title="", sub="", accent=None):
    """Pantalla final (20 s) estilo señal de autopista: dos 'salidas' para los elementos de YouTube + suscripción."""
    W, H = ctx.W, ctx.H; accent = accent or PAL["amarillo"]
    coast_scene(c, W, H, t, hy=H * 0.30, road=True, sun=True); rect(c, 0, 0, W, H, "#000000", 0.35)
    p = ease_out(prog(t, 0, 0.8))
    c.save(); c.translate(0, (1 - p) * -60)
    guide_sign(c, W / 2 - 760, 40, 1520, 190, a=p)
    draw_text(c, title or "SIGUIENTE SALIDA", W / 2, 140, "ovblk", 60, PAL["sal"], p, align="center")
    if sub: draw_text(c, sub, W / 2, 195, "ovsb", 30, PAL["sal"], 0.9 * p, align="center")
    c.restore()
    for i, x in enumerate((180, 1020)):
        pp = ease_out_back(prog(t, 0.3 + i * 0.15, 1.0))
        c.save(); c.translate(x + 360, 590); c.scale(pp, pp); c.translate(-(x + 360), -590)
        rect(c, x, 388, 720, 405, "#000000", 0.45, r=12)
        rect(c, x, 388, 720, 405, PAL["sal"], 0.95, r=12, stroke=6)
        rect(c, x, 340, 230, 52, PAL["amarillo"] if i == 0 else PAL["senal"], 1, r=6)
        draw_text(c, "SALIDA 1" if i == 0 else "SALIDA 2", x + 115, 377, "ovblk", 30, PAL["asfalto"] if i == 0 else PAL["sal"], 1, align="center")
        draw_text(c, "VIDEO RECOMENDADO" if i == 0 else "LISTA: GTA VI EXPLICADO", x + 360, 600, "ovmono", 30, PAL["sal"], 0.55, align="center", tracking=2)
        c.restore()
    pp = ease_out_back(prog(t, 0.6, 1.3))
    c.save(); c.translate(W / 2, 935); c.scale(pp, pp); draw_badge(c, 0, 0, 88, t=t); c.restore()
    rect(c, W / 2 + 115, 905, 560, 64, PAL["amarillo"], pp, r=8)
    draw_text(c, "SUSCRÍBETE · ACTIVA LA CAMPANA", W / 2 + 395, 948, "ovblk", 30, PAL["asfalto"], pp, align="center")

def watermark(c, W, H, a=0.55, corner="br", size=64):
    x = W - size - 34 if corner[1] == "r" else 34; y = H - size - 30 if corner[0] == "b" else 30
    draw_badge(c, x + size / 2, y + size / 2, size / 2 - 3, a=a)

def sign_text(c, x, y, txt, size, bg=None, fg=None, align="left", pad=None):
    """Texto dentro de un panel tipo señal vial (verde con borde blanco por defecto). (x, y) = esquina sup. izq. o centro superior."""
    bg = bg or PAL["senal"]; fg = fg or PAL["sal"]; pad = pad or size * 0.45
    w = text_w(txt, font("ovblk", size), size * 0.01) + 2 * pad; h = size * 1.45
    if align == "center": x -= w / 2
    guide_sign(c, x, y, w, h, col=bg)
    draw_text(c, txt, x + pad, y + h * 0.5 + size * 0.36, "ovblk", size, fg, 1, tracking=size * 0.01)
    return w

def thumb_mark(c, x, y, r=34):
    """Constante de marca para miniaturas: emblema pequeño."""
    draw_badge(c, x, y, r)

def word_times(sent):
    if sent.get("words"): return [(w, s, e) for w, s, e in sent["words"]]
    words = sent["text"].split(); tot = sum(len(w) + 1 for w in words); d = sent["end"] - sent["start"]; acc = 0; out = []
    for w in words:
        st = sent["start"] + d * acc / tot; acc += len(w) + 1; out.append((w, st, sent["start"] + d * acc / tot))
    return out

def short_captions(c, gt, ctx, y=1350, size=74, hl=PAL["amarillo"], fontname="anton", maxw=900, box=True):
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
