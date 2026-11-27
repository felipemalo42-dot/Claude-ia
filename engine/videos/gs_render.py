"""Montaje del Short promocional (9:16, 1080×1920, 30 fps).

Fuentes: v:<ID>@<segundo>@<cx> = recorte vertical 4K (mezzanine.build_v), c:<ID>@<segundo> = imagen 16:9 en tarjeta sobre su
propio fondo desenfocado (tramo 1080p de mezzanine.build), g:<gráfico>. Igual que en el vídeo largo: velocidad 1, cada
fotograma avanza uno del original, sin bucles ni congelados (validate() lo comprueba antes de renderizar).
"""
import bisect, math, os
import numpy as np, skia
from gfx import *
from brand import PAL, draw_badge, wordmark
import components as K
import mezzanine as MZ
from videos import gl_render as G
from videos import gx_render as X

W, H, FPS = 1080, 1920, 30
LEAD = 0.06
YEL, GRN, RED, CYA, INK, WHITE, GRAY = X.YEL, X.GRN, X.RED, X.CYA, X.INK, X.WHITE, X.GRAY
SO, SO_HQ = X.SO, X.SO_HQ
LONG_THUMB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_GTA6", "MINIATURA.png")

def parse(src):
    k, v = src.split(":", 1); parts = v.split("@")
    return k, parts[0], float(parts[1]), (float(parts[2]) if len(parts) > 2 else None)

def window(sh):
    """→ (archivo, inicio en el tramo, segundos continuos disponibles, tipo)"""
    if "_w" in sh: return sh["_w"]
    k, vid, T, cx = parse(sh["src"])
    if k == "v":
        r = MZ.locate_v(vid, T, cx)
        if not r: raise ValueError(f"no hay recorte vertical para {sh['src']}")
        sh["_w"] = (r[0], r[1], r[2], "v"); return sh["_w"]
    path, loc, avail, _ = X.x_window(dict(src=f"x:{vid}@{T}"))
    sh["_w"] = (path, loc, avail, "c"); return sh["_w"]

_CL = {}
def frame(sh, tau, slot):
    path, loc, avail, kind = window(sh)
    k = int(math.floor(tau * FPS + 1e-6)); kmax = max(0, int(avail * FPS) - 1)
    if k > kmax: sh["_over"] = max(sh.get("_over", 0), k - kmax); k = kmax
    cl = _CL.get(slot); size = (W, H) if kind == "v" else (1920, 1080)
    if cl is None or cl.path != path or abs(cl.t0 - loc) > 1e-3:
        if cl: cl.close()
        cl = X.Clip(path, loc, avail + 0.3, size); _CL[slot] = cl
    return cl.get(k), kind

def footage(c, sh, tau, d, slot="main"):
    img, kind = frame(sh, tau, slot)
    if img is None: return
    if kind == "v":
        z0, z1 = sh.get("z", (1.0, 1.05)); z = lerp(z0, z1, clamp(tau / max(d, 0.1)))
        s = z; dw, dh = W * s, H * s
        c.drawImageRect(img, skia.Rect.MakeXYWH((W - dw) / 2, (H - dh) / 2, dw, dh), SO_HQ if z > 1.2 else SO)
    else:
        # tarjeta 16:9: fondo con la misma imagen ampliada y desenfocada; encima, la zona `crop` (0-1) de la imagen, nítida
        bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(40, 40))
        bw = H * 16 / 9; c.drawImageRect(img, skia.Rect.MakeXYWH((W - bw) / 2, 0, bw, H), SO, bg); rect(c, 0, 0, W, H, "#05060A", 0.5)
        u0, v0, u1, v1 = sh.get("crop", (0, 0, 1, 1)); iw, ih = img.width(), img.height()
        src = skia.Rect.MakeLTRB(u0 * iw, v0 * ih, u1 * iw, v1 * ih)
        cw = W - 40; ch = cw * (v1 - v0) * ih / ((u1 - u0) * iw); y = sh.get("cy", 700) - ch / 2
        zz = 1 + 0.04 * clamp(tau / max(d, 0.1)); cw2, ch2 = cw * zz, ch * zz
        rect(c, (W - cw2) / 2 + 10, y + 14, cw2, ch2, "#000000", 0.5, r=26, blur=16)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH((W - cw2) / 2, y - (ch2 - ch) / 2, cw2, ch2), 24, 24), True)
        c.drawImageRect(img, src, skia.Rect.MakeXYWH((W - cw2) / 2, y - (ch2 - ch) / 2, cw2, ch2), SO_HQ, skia.Paint()); c.restore()
        rect(c, (W - cw2) / 2, y - (ch2 - ch) / 2, cw2, ch2, WHITE, 0.85, r=24, stroke=4)
        if sh.get("top"):
            p = ease_out(prog(tau, 0.1, 0.4)); G.chip(c, 40, y - (ch2 - ch) / 2 - 64, sh["top"], p, 28, CYA)

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
    # el primer plano empieza en el fotograma 0 (sin negro al principio: el gancho se ve desde el primer instante); su
    # material se adelanta lo mismo, así que desde el inicio de la voz se ve exactamente lo mismo que antes
    if shots and shots[0]["t0"] > 0:
        s0 = shots[0]; d = s0["t0"]
        if not s0["src"].startswith("g:"):
            k_, vid_, T_, cx_ = parse(s0["src"]); s0["src"] = f"{k_}:{vid_}@{T_ - d * 1.001:.3f}" + (f"@{cx_}" if cx_ is not None else "")
        if s0.get("st"): s0["st"] = [round(x + d, 3) for x in s0["st"]]
        s0["t0"] = 0.0
    for i, s in enumerate(shots): s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else tl["total"]
    lastv = {}
    for s in shots:
        if s["src"].startswith("g:"): continue
        k, vid, T, cx = parse(s["src"])
        if s.get("cont"):
            pT, pt0 = lastv[(k, vid, cx)]; T = pT + (s["t0"] - pt0) * 1.001
            s["src"] = f"{k}:{vid}@{T:.3f}" + (f"@{cx}" if cx is not None else "")
        lastv[(k, vid, cx)] = (T, s["t0"])
    _T.update(shots=shots, starts=[s["t0"] for s in shots]); return _T

def validate(ctx, verbose=True):
    T = table(ctx); bad = []
    for s in T["shots"]:
        if s["src"].startswith("g:"): continue
        d = s["t1"] - s["t0"] + 0.17; path, loc, avail, kind = window(s)   # + el fundido de 0,12 s hacia el plano siguiente
        if d > avail: bad.append((s, f"dura {d:.2f} s y solo hay {avail:.2f} s continuos"))
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
    else: footage(c, sh, tau, d, slot)

def overlay(c, gt, ctx):
    T = table(ctx); i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    # cabecera fija
    p = ease_out(prog(gt, 0.0, 0.4))
    rect(c, 40, 120, W - 80, 104, INK, 0.78 * p, r=52)
    for k in range(6): X.star(c, 112 + k * 50, 172, 19, "white", p)
    draw_text(c, "GTA 6 · PARTIDA REAL", W - 90, 186, "anton", 46, YEL, p, align="right", tracking=2)
    if not sh["src"].startswith("g:"):
        f = font("ovmonomd", 24); txt = "Gameplay: IGN · YouTube"; w = text_w(txt, f, 0.5) + 36
        rect(c, W - w - 36, 246, w, 40, "#000000", 0.55, r=6); draw_text(c, txt, W - w - 18, 274, "ovmonomd", 24, "#F3F0E9", 0.9, tracking=0.5)
    if not sh.get("nocap"): K.short_captions(c, gt, ctx, y=1420, size=86, maxw=960)

# ================================================================ gráficos verticales
def panel(c, t):
    rect(c, 0, 0, W, H, "#0A0B10", 1); grid(c, W, H, 80, "#FFFFFF", 0.035)
    r = 0.5 + 0.5 * math.sin(t * 2.4)
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(-100, 200, 1200, [hexc("#FF2D55", 0.12 * r), hexc("#FF2D55", 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(W + 100, 200, 1200, [hexc("#2D7BFF", 0.12 * (1 - r)), hexc("#2D7BFF", 0)]))

def g_sladder(c, t, d, sh, ctx):
    panel(c, t)
    draw_text(c, "PERFIL CRIMINAL", W / 2, 400, "anton", 104, YEL, ease_out(prog(t, 0, 0.3)), align="center", tracking=3)
    for k, (es, en, col) in enumerate(X.TIERS):
        q = ease_out_back(prog(t, 0.1 + 0.08 * k, 0.45 + 0.08 * k))
        if q <= 0: continue
        y = 540 + k * 130; on = k == 4; a = 1.0 if on else 0.4
        c.save(); c.translate(W / 2, y); c.scale(q, q); c.translate(-W / 2, -y)
        rect(c, 90, y - 52, W - 180, 104, INK, 0.92 * a, r=14); rect(c, 90, y - 52, 10, 104, RED if on else col, a)
        if on: rect(c, 90, y - 52, W - 180, 104, RED, 1, r=14, stroke=5)
        X.horns(c, 170, y + 6, 32, "#8A8F99" if on else col, a, crack=ease_out(prog(t, 0.9, 1.6)) if on else 0)
        draw_text(c, es, 230, y + 24, "anton", 66, WHITE, a, tracking=2); c.restore()
    e = ease_out_back(prog(t, 1.0, 1.4))
    if e > 0:
        c.save(); c.translate(W / 2, 1180); c.scale(e, e)
        rect(c, -400, -58, 800, 116, RED, 1, r=58); icon(c, "lock", -330, 0, 60, WHITE, 1)
        draw_text(c, "IMPACTO DURADERO", 40, 22, "anton", 60, WHITE, 1, align="center", tracking=2); c.restore()
        draw_text(c, "SEGÚN ROCKSTAR", W / 2, 1275, "ovmono", 34, YEL, clamp(e), align="center", tracking=2)

def g_squestion(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out_back(prog(t, 0.0, 0.45))
    c.save(); c.translate(W / 2, 600); c.scale(p, p); X.horns(c, 0, 0, 150, "#4B5060", 1, crack=ease_out(prog(t, 0.3, 1.0))); c.restore()
    for j, ln in enumerate(["¿QUÉ ES EL", "PERFIL CRIMINAL?"]):
        draw_text(c, ln, W / 2, 920 + j * 120, "anton", 112, WHITE if j == 0 else YEL, ease_out(prog(t, 0.2 + 0.1 * j, 0.5 + 0.1 * j)), align="center", tracking=2)
    q = ease_out(prog(t, 1.2, 1.6))
    for j, ln in enumerate(["¿Y CÓMO EVITAS QUE", "TE MARQUE PARA SIEMPRE?"]):
        draw_text(c, ln, W / 2, 1180 + j * 76, "anton", 66, WHITE, q, align="center", tracking=1)

def g_scta(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out_back(prog(t, 0.0, 0.45))
    draw_text(c, "VIDEO COMPLETO", W / 2, 420, "anton", 120, YEL, ease_out(prog(t, 0, 0.3)), align="center", tracking=3)
    if os.path.exists(LONG_THUMB):
        img = G.load_img(LONG_THUMB); cw = 960; ch = cw * 9 / 16; x = (W - cw) / 2; y = 500
        c.save(); c.translate(W / 2, y + ch / 2); c.scale(p, p); c.translate(-W / 2, -(y + ch / 2))
        rect(c, x + 12, y + 16, cw, ch, "#000000", 0.5, r=24, blur=16)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, cw, ch), 22, 22), True)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, cw, ch), SO_HQ); c.restore()
        rect(c, x, y, cw, ch, WHITE, 1, r=22, stroke=5)
        circle(c, W / 2, y + ch / 2, 70, "#E62117", 0.95); draw_poly(c, [(W / 2 - 22, y + ch / 2 - 34), (W / 2 - 22, y + ch / 2 + 34), (W / 2 + 36, y + ch / 2)], WHITE, 1)
        c.restore()
    draw_text(c, "Con partidas reales · sin spoilers", W / 2, 1150, "intersb", 46, WHITE, ease_out(prog(t, 0.4, 0.8)), align="center")
    st = sh.get("st") or [2.0]
    q = ease_out_back(prog(t, st[0] - 0.4, st[0]))
    if q > 0:
        yb = 1640 + 18 * math.sin(t * 6)
        c.save(); c.translate(W / 2, yb); c.scale(q, q)
        rect(c, -360, -70, 720, 110, YEL, 1, r=55); draw_text(c, "VIDEO RELACIONADO", 0, 8, "anton", 60, INK, 1, align="center", tracking=2)
        draw_poly(c, [(-50, 60), (50, 60), (0, 130)], YEL, 1); c.restore()

GFX = {k[2:]: v for k, v in list(globals().items()) if k.startswith("g_")}

# ================================================================ portada del Short (1080×1920)
def cover(c):
    p = os.path.join(os.path.dirname(X.ICON_DIR), "miniatura_fondo.png")
    if os.path.exists(p):
        img = G.load_img(p, maxw=2600); iw, ih = img.width(), img.height(); s = H / ih; dw = iw * s
        c.drawImageRect(img, skia.Rect.MakeXYWH(W / 2 - dw * 0.30, 0, dw, H), SO_HQ)
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, H)], [skia.Color(8, 8, 14, 230), skia.Color(8, 8, 14, 40), skia.Color(8, 8, 14, 235)], [0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), g)
    for k in range(6): X.star(c, 165 + k * 150, 300, 58, "white", 1)
    draw_text(c, "6 ESTRELLAS", W / 2, 520, "anton", 170, WHITE, 1, align="center", tracking=2)
    draw_text(c, "YA ES", W / 2, 1460, "anton", 150, YEL, 1, align="center", tracking=2)
    draw_text(c, "DEMASIADO TARDE", W / 2, 1610, "anton", 128, YEL, 1, align="center", tracking=2)
    draw_text(c, "GTA 6 · PARTIDA REAL", W / 2, 1760, "ovmono", 40, WHITE, 0.92, align="center", tracking=3)
