"""Montaje de los Shorts 2 y 3 (9:16, 1080×1920, 30 fps): «Planeta Vice City» y «GTA 6 a juicio».

Fuentes: v:<ID>@<segundo>@<cx> = recorte vertical 4K/1080p (mezzanine.build_v) · c:<ID>@<segundo> = imagen 16:9 en tarjeta
sobre su propio fondo desenfocado (tramo de mezzanine.build) · g:<gráfico>. Velocidad 1, cada fotograma avanza uno del
original, sin bucles ni congelados (validate() lo comprueba). Tiempos del original según el ritmo de cada fuente (mezzanine.rate).
"""
import bisect, math, os
import numpy as np, skia
from gfx import *
from brand import PAL, draw_badge, wordmark
import components as K
import mezzanine as MZ
from videos import gl_render as G
from videos import dc_render as D

W, H, FPS = 1080, 1920, 30
LEAD = 0.06
INK, WHITE, GRAY, RED, BLUE, YEL = D.INK, D.WHITE, D.GRAY, D.RED, D.BLUE, D.YEL
SO, SO_HQ = D.SO, D.SO_HQ

def th(ctx): return D.THEMES[ctx.V.get("theme", "planeta")]

def parse(src):
    k, v = src.split(":", 1); parts = v.split("@")
    return k, parts[0], float(parts[1]), (float(parts[2]) if len(parts) > 2 else None)

def window(sh):
    if "_w" in sh: return sh["_w"]
    k, vid, T, cx = parse(sh["src"])
    if k == "v":
        r = MZ.locate_v(vid, T, cx)
        if not r: raise ValueError(f"no hay recorte vertical para {sh['src']}")
        sh["_w"] = (r[0], r[1], r[2], "v"); return sh["_w"]
    path, loc, avail, _ = D.x_window(dict(src=f"x:{vid}@{T}"))
    sh["_w"] = (path, loc, avail, "c"); return sh["_w"]

_CL = {}
def frame(sh, tau, slot):
    path, loc, avail, kind = window(sh)
    k = int(math.floor(tau * FPS + 1e-6)); kmax = max(0, int(avail * FPS) - 1)
    if k > kmax: sh["_over"] = max(sh.get("_over", 0), k - kmax); k = kmax
    cl = _CL.get(slot); size = (W, H) if kind == "v" else (1920, 1080)
    if cl is None or cl.path != path or abs(cl.t0 - loc) > 1e-3:
        if cl: cl.close()
        cl = D.Clip(path, loc, avail + 0.3, size); _CL[slot] = cl
    return cl.get(k), kind

def footage(c, sh, tau, d, ctx, slot="main"):
    img, kind = frame(sh, tau, slot)
    if img is None: return
    if kind == "v":
        z0, z1 = sh.get("z", (1.0, 1.05)); z = lerp(z0, z1, clamp(tau / max(d, 0.1))); dw, dh = W * z, H * z
        fy = sh.get("fy", 0.5)   # 0 = se ve la parte de arriba (deja fuera subtítulos incrustados en el original)
        c.drawImageRect(img, skia.Rect.MakeXYWH((W - dw) / 2, (H - dh) * fy, dw, dh), SO_HQ if z > 1.2 else SO)
    else:
        bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(40, 40))
        bw = H * 16 / 9; c.drawImageRect(img, skia.Rect.MakeXYWH((W - bw) / 2, 0, bw, H), SO, bg); rect(c, 0, 0, W, H, "#05060A", 0.5)
        u0, v0, u1, v1 = sh.get("crop", (0, 0, 1, 1)); iw, ih = img.width(), img.height()
        src = skia.Rect.MakeLTRB(u0 * iw, v0 * ih, u1 * iw, v1 * ih)
        cw = W - 40; ch = cw * (v1 - v0) * ih / ((u1 - u0) * iw); y = sh.get("cy", 760) - ch / 2
        zz = 1 + 0.04 * clamp(tau / max(d, 0.1)); cw2, ch2 = cw * zz, ch * zz; y2 = y - (ch2 - ch) / 2
        rect(c, (W - cw2) / 2 + 10, y2 + 14, cw2, ch2, "#000000", 0.5, r=26, blur=16)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH((W - cw2) / 2, y2, cw2, ch2), 24, 24), True)
        c.drawImageRect(img, src, skia.Rect.MakeXYWH((W - cw2) / 2, y2, cw2, ch2), SO_HQ, skia.Paint()); c.restore()
        rect(c, (W - cw2) / 2, y2, cw2, ch2, th(ctx)["acc"], 0.9, r=24, stroke=5)
        if sh.get("top"): G.chip(c, 40, y2 - 64, sh["top"], ease_out(prog(tau, 0.1, 0.4)), 28, th(ctx)["acc"])
    if sh.get("say"):
        p = ease_out(prog(tau, 0.15, 0.45)) * (1 - prog(tau, d - 0.15, d))
        if p > 0:
            lines = wrap(f"«{sh['say']}»", "dmserifi", 50, W - 160); hh = 40 + 62 * len(lines); y = sh.get("say_y", 330)
            rect(c, 60, y, W - 120, hh, INK, 0.82 * p, r=28); rect(c, 60, y, W - 120, hh, th(ctx)["acc"], p, r=28, stroke=4)
            for j, ln in enumerate(lines): draw_text(c, ln, W / 2, y + 62 + j * 62, "dmserifi", 50, WHITE, p, align="center")
    if sh.get("prueba"):
        col = {"acusacion": RED, "defensa": BLUE, "gta5": "#2E8B47", "gta6": "#C2185B"}.get(sh.get("lado"), "#B8860B")
        p = ease_out_back(prog(tau, 0.1, 0.45)) * (1 - prog(tau, d - 0.15, d))
        if p > 0:
            c.save(); c.translate(W / 2, 360); c.rotate(-4 * (1 - p)); c.scale(p, p)
            rect(c, -260, -62, 520, 124, "#F4EBD0", 0.97, r=10); rect(c, -260, -62, 520, 124, col, 1, r=10, stroke=6)
            draw_text(c, sh["prueba"], 0, 24, "anton", 72, col, 1, align="center", tracking=2); c.restore()
    vignette(c, W, H, 0.3)

# ================================================================ tabla de planos
_T = {}
def table(ctx):
    if "shots" in _T: return _T
    V, tl = ctx.V, ctx.tl; shots = []
    for bi, (b, bd) in enumerate(zip(V["beats"], tl["beats"])):
        last = bd["start"]
        for sh in b.get("shots", []):
            if sh["anchor"] is None: t0 = bd["start"]; wt = None
            else:
                wt, _ = G._word_time(bd["sents"], sh["anchor"], last)
                if wt is None: raise ValueError(f"ancla «{sh['anchor']}» no encontrada en el beat {bi}")
                t0 = wt - LEAD
            t0 += sh.get("dt", 0.0)
            ns = dict(sh, t0=t0, beat=bi, k=len(shots), word_t=wt); after = (wt + 0.01) if wt is not None else bd["start"]
            if sh.get("cues"):
                st = []; aft = after - 0.02
                for frag in sh["cues"]:
                    ct, _ = G._word_time(bd["sents"], frag, aft)
                    if ct is None: raise ValueError(f"cue «{frag}» no encontrada")
                    st.append(round(ct - t0, 3)); aft = ct + 0.01
                ns["st"] = st
            shots.append(ns); last = after
    shots.sort(key=lambda s: s["t0"])
    # el primer plano empieza en el fotograma 0: el gancho se ve desde el primer instante
    if shots and shots[0]["t0"] > 0:
        s0 = shots[0]; dd = s0["t0"]
        if not s0["src"].startswith("g:"):
            k_, vid_, T_, cx_ = parse(s0["src"]); s0["src"] = f"{k_}:{vid_}@{T_ - dd * MZ.rate(vid_):.3f}" + (f"@{cx_}" if cx_ is not None else "")
        if s0.get("st"): s0["st"] = [round(x + dd, 3) for x in s0["st"]]
        s0["t0"] = 0.0
    for i, s in enumerate(shots): s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else tl["total"]
    _T.update(shots=shots, starts=[s["t0"] for s in shots]); return _T

def validate(ctx, verbose=True):
    T = table(ctx); bad = []; used = {}
    for s in T["shots"]:
        if s["src"].startswith("g:"): continue
        d = s["t1"] - s["t0"] + 0.17; path, loc, avail, kind = window(s)
        if not os.path.exists(path): bad.append((s, "falta el tramo")); continue
        if d > avail: bad.append((s, f"dura {d:.2f} s y solo hay {avail:.2f} s continuos"))
        # el mismo momento del original no sale dos veces (aunque sea con otro encuadre)
        k, vid, T0, cx = parse(s["src"]); seg = (T0, T0 + (s["t1"] - s["t0"]) * MZ.rate(vid))
        for o in used.get(vid, []):
            if seg[0] < o[1] - 0.05 and o[0] < seg[1] - 0.05: bad.append((s, f"repite material de {vid} ({o[0]:.1f}-{o[1]:.1f})"))
        used.setdefault(vid, []).append(seg)
    if verbose:
        for s, why in bad: print(f"  [plano] {s['t0']:6.2f} s · {s['src']} · {why}")
        print(f"  validación de planos del Short: {len(T['shots'])} planos · {len(bad)} con problemas")
    return bad

_SURF = {}
def scene(c, t, info, ctx):
    gt = info.start + t; T = table(ctx)
    i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    tau = gt - sh["t0"]; d = max(0.05, sh["t1"] - sh["t0"])
    if i > 0 and tau < 0.12:
        pv = T["shots"][i - 1]
        for nm in ("A", "B"):
            if nm not in _SURF: _SURF[nm] = skia.Surface(W, H)
        ca = _SURF["A"].getCanvas(); ca.clear(skia.ColorBLACK); draw_shot(ca, pv, gt - pv["t0"], max(0.05, pv["t1"] - pv["t0"]), ctx, "prev")
        cb = _SURF["B"].getCanvas(); cb.clear(skia.ColorBLACK); draw_shot(cb, sh, tau, d, ctx)
        c.drawImage(_SURF["A"].makeImageSnapshot(), 0, 0); pp = skia.Paint(); pp.setAlphaf(ease_io(tau / 0.12))
        c.drawImage(_SURF["B"].makeImageSnapshot(), 0, 0, SO, pp)
    else: draw_shot(c, sh, tau, d, ctx)

def draw_shot(c, sh, tau, d, ctx, slot="main"):
    if sh["src"].startswith("g:"): GFX[sh["src"][2:]](c, tau, d, sh, ctx)
    else: footage(c, sh, tau, d, ctx, slot)

def overlay(c, gt, ctx):
    T = table(ctx); i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]; TH = th(ctx)
    p = ease_out(prog(gt, 0.0, 0.4))
    rect(c, 40, 120, W - 80, 104, INK, 0.78 * p, r=52)
    if ctx.V.get("theme") == "juicio": D.gavel(c, 128, 166, 40, TH["acc"], p, base=False)
    elif ctx.V.get("theme") == "combate":
        for k in range(3): star(c, 98 + k * 46, 172, 19, TH["acc"], p)
    elif ctx.V.get("theme") == "tv":
        rect(c, 76, 146, 70, 50, TH["acc"], p, r=8, stroke=5); line(c, 98, 146, 86, 128, TH["acc"], p, w=4); line(c, 124, 146, 136, 128, TH["acc"], p, w=4)
    elif ctx.V.get("theme") == "arcade":
        rect(c, 78, 150, 74, 42, TH["acc"], p, r=12, stroke=5); circle(c, 98, 171, 7, TH["glow1"], p); circle(c, 134, 171, 7, TH["acc"], p)
    elif ctx.V.get("theme") == "playa":
        circle(c, 112, 166, 26, TH["acc"], p); rect(c, 74, 176, 76, 22, TH["glow1"], p, r=8)
    else:
        for k in range(3): D.leaf(c, 100 + k * 34, 172, 20, TH["glow1"], p, rot=k * 35)
    draw_text(c, ctx.V.get("header", ""), W - 90, 188, "anton", 50, TH["acc"], p, align="right", tracking=2)
    if not sh["src"].startswith("g:") and ctx.V.get("credit", True):   # credit=False: el crédito va solo en la descripción
        _, vid, _, _ = parse(sh["src"])
        f = font("ovmonomd", 24); txt = f"Gameplay: {D.AUTHOR.get(vid, vid)}"; w = text_w(txt, f, 0.5) + 36
        rect(c, W - w - 36, 246, w, 40, "#000000", 0.55, r=6); draw_text(c, txt, W - w - 18, 274, "ovmonomd", 24, "#F3F0E9", 0.9, tracking=0.5)
    if not sh.get("nocap"): K.short_captions(c, gt, ctx, y=1420, size=86, maxw=960)

def star(c, x, y, r, col, a=1.0):
    """Estrella de cinco puntas (las del nivel de búsqueda)."""
    pts = [(x + (r if k % 2 == 0 else r * 0.45) * math.sin(k * math.pi / 5), y - (r if k % 2 == 0 else r * 0.45) * math.cos(k * math.pi / 5)) for k in range(10)]
    draw_poly(c, pts, col, a)

# ================================================================ gráficos verticales
def panel(c, t, ctx):
    TH = th(ctx); rect(c, 0, 0, W, H, TH["bg"], 1); grid(c, W, H, 80, "#FFFFFF", 0.03)
    r = 0.5 + 0.5 * math.sin(t * 1.8)
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(-100, 200, 1200, [hexc(TH["glow1"], 0.12 * r), hexc(TH["glow1"], 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(W + 100, H - 200, 1200, [hexc(TH["glow2"], 0.12 * (1 - r)), hexc(TH["glow2"], 0)]))

def g_sq(c, t, d, sh, ctx):
    """Pregunta o título grande, línea a línea."""
    panel(c, t, ctx); TH = th(ctx)
    lines = sh["lines"]; y0 = sh.get("y", 700)
    for j, ln in enumerate(lines):
        q = ease_out_back(prog(t, 0.1 + 0.15 * j, 0.45 + 0.15 * j))
        c.save(); c.translate(W / 2, y0 + j * 135); c.scale(0.7 + 0.3 * q, 0.7 + 0.3 * q)
        draw_text(c, ln, 0, 45, "anton", 120, TH["acc"] if j in sh.get("hl", [len(lines) - 1]) else WHITE, clamp(q * 1.4), align="center", tracking=2); c.restore()
    if sh.get("sub"): draw_text(c, sh["sub"], W / 2, y0 + len(lines) * 135 + 70, "intersb", 46, GRAY, ease_out(prog(t, 0.7, 1.1)), align="center")

def g_scta(c, t, d, sh, ctx):
    """Llamada al vídeo largo: está completo en el canal (sin enlace de «vídeo relacionado»)."""
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out_back(prog(t, 0.0, 0.45))
    draw_text(c, "VIDEO COMPLETO", W / 2, 420, "anton", 120, TH["acc"], ease_out(prog(t, 0, 0.3)), align="center", tracking=3)
    thumb = sh.get("thumb")
    if thumb and os.path.exists(thumb):
        img = G.load_img(thumb); cw = 960; ch = cw * 9 / 16; x = (W - cw) / 2; y = 500
        c.save(); c.translate(W / 2, y + ch / 2); c.scale(p, p); c.translate(-W / 2, -(y + ch / 2))
        rect(c, x + 12, y + 16, cw, ch, "#000000", 0.5, r=24, blur=16)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, cw, ch), 22, 22), True)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, cw, ch), SO_HQ); c.restore()
        rect(c, x, y, cw, ch, WHITE, 1, r=22, stroke=5)
        circle(c, W / 2, y + ch / 2, 70, "#E62117", 0.95); draw_poly(c, [(W / 2 - 22, y + ch / 2 - 34), (W / 2 - 22, y + ch / 2 + 34), (W / 2 + 36, y + ch / 2)], WHITE, 1)
        c.restore()
    draw_text(c, sh.get("sub", "Con partidas reales · sin spoilers"), W / 2, 1150, "intersb", 46, WHITE, ease_out(prog(t, 0.4, 0.8)), align="center")
    st = sh.get("st") or [2.0]
    q = ease_out_back(prog(t, st[0] - 0.4, st[0]))
    if q > 0:
        c.save(); c.translate(W / 2, 1650 + 14 * math.sin(t * 5)); c.scale(q, q)
        rect(c, -400, -66, 800, 120, TH["acc"], 1, r=60); draw_text(c, "EN EL CANAL", 0, 22, "anton", 70, INK, 1, align="center", tracking=3); c.restore()

def g_static(c, t, d, sh, ctx):
    """Cambio de canal: nieve de televisión y el número del canal (zapping)."""
    rng = np.random.default_rng(int(t * 30) + 7)
    rect(c, 0, 0, W, H, "#111111", 1)
    for k in range(260):
        y = float(rng.integers(0, H)); hh = float(rng.integers(2, 9)); g = int(rng.integers(40, 235))
        rect(c, 0, y, W, hh, "#%02x%02x%02x" % (g, g, g), 0.55)
    for k in range(900):
        x = float(rng.integers(0, W)); y = float(rng.integers(0, H)); g = int(rng.integers(120, 255))
        rect(c, x, y, float(rng.integers(3, 14)), float(rng.integers(3, 9)), "#%02x%02x%02x" % (g, g, g), 0.8)
    if sh.get("ch"):
        rect(c, W - 330, 330, 270, 120, "#000000", 0.6, r=10)
        draw_text(c, sh["ch"], W - 195, 418, "ovmonomd", 84, "#3DDC97", 1, align="center", tracking=2)

def g_review(c, t, d, sh, ctx):
    """Tarjeta de reseña con estrellas (formato «una estrella»)."""
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out_back(prog(t, 0.0, 0.4)); y0 = sh.get("y", 560)
    c.save(); c.translate(W / 2, y0 + 300); c.scale(p, p); c.translate(-W / 2, -(y0 + 300))
    rect(c, 80, y0, W - 160, 600, "#F7F4EC", 0.98, r=32); rect(c, 80, y0, W - 160, 600, TH["acc"], 1, r=32, stroke=6)
    draw_text(c, sh.get("kicker", "RESEÑA"), 140, y0 + 80, "ovmonomd", 34, "#6B6B6B", 1, tracking=3)
    for j, ln in enumerate(wrap(sh["title"], "anton", 82, W - 300)):
        draw_text(c, ln, 140, y0 + 190 + j * 92, "anton", 82, INK, 1, tracking=1)
    n = sh.get("stars", 1)
    for k in range(5):
        q = ease_out_back(prog(t, 0.35 + 0.12 * k, 0.6 + 0.12 * k))
        if q > 0: star(c, 175 + k * 120, y0 + 430, 48 * q, "#F5B700" if k < n else "#D6D2C4", 1)
    if sh.get("sub"): draw_text(c, sh["sub"], 140, y0 + 540, "intersb", 40, "#444444", ease_out(prog(t, 0.8, 1.1)))
    c.restore()

GFX = {k[2:]: v for k, v in list(globals().items()) if k.startswith("g_")}
