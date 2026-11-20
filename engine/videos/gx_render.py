"""Montaje de VIDEO_LARGO_GTA6 (16:9, 1920×1080, 30 fps) con gameplay real posterior al lanzamiento.

- Cada plano empieza en la palabra exacta del guion que lo motiva (tiempos por palabra del reconocedor; corte 2 fotogramas antes).
- Gameplay: tramos «mezzanine» (mezzanine.py) a 1080p y 30 fps constantes, solo imágenes únicas. Se reproducen a velocidad 1:
  cada fotograma del vídeo avanza exactamente un fotograma del original (sin repetir, sin saltar, sin bucles ni congelados).
  validate() comprueba antes de renderizar que ningún plano dura más que su material continuo disponible.
- Encuadre: empuje lento (Ken Burns) o zoom animado a un punto (HUD, mensajes del juego) sobre la imagen 1080p.
- Vídeos verticales (Shorts de IGN): tarjeta vertical sobre su propia imagen desenfocada.
- Rótulos: capítulo, origen del dato (se ve en la partida / según Rockstar / según las guías), crédito del gameplay,
  subtítulos palabra a palabra y gráficos propios (g:).
"""
import bisect, json, math, os, subprocess
import numpy as np, skia
from gfx import *
from brand import PAL, draw_badge, wordmark
import components as K
import mezzanine as MZ
from videos import gl_render as G

W, H, FPS = 1920, 1080, 30
LEAD = 0.06
YEL, GRN, RED, CYA, MAG, ORA, PUR = "#FFC72C", "#22C55E", "#FF3B3B", "#36E3FF", "#FF4FD8", "#FF8A1F", "#A855F7"
INK = "#0B0C10"; WHITE = "#FFFFFF"; GRAY = "#9AA0AA"
XCAT = G.XCAT
SO = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
SO_HQ = skia.SamplingOptions(skia.CubicResampler.Mitchell())
# fuentes editadas (guías con cortes de montaje): un plano no puede cruzar un corte. Las partidas continuas no tienen cortes.
EDITED = {"Om4W6tYMF-0", "qbhJRtgCx30", "eD5ndr0OMM0", "JHRVSzM2O2M", "uMYUjOLOOVQ"}
AUTHOR = {"Om4W6tYMF-0": "IGN", "qbhJRtgCx30": "IGN", "eD5ndr0OMM0": "IGN", "JHRVSzM2O2M": "IGN", "uMYUjOLOOVQ": "IGN",
          "gJyMGHxCKHU": "GTAsatara", "ey0qks0aQ-c": "MikeTheGoon"}

# ================================================================ material
def parse_x(src):
    vid, t = src[2:].split("@"); return vid, float(t)

_CUTS = {}
MANUAL_CUTS = {"Om4W6tYMF-0": [287.0, 293.4, 361.7, 366.9, 373.1],   # inserto de IGN, zooms de IGN, menú de armas (373,2-373,7)
               # partidas continuas: menús del juego que tapan la imagen (inicio y fin de cada uno)
               "ey0qks0aQ-c": [35.0, 43.5, 150.0, 153.5, 174.0, 175.8, 392.5, 394.0, 677.0, 680.5, 715.5, 717.0, 791.25, 793.0],
               "gJyMGHxCKHU": [117.0, 119.5, 203.4]}   # segundos del original: inserto de IGN (persona real) y zooms de IGN
def mez_cuts(path):
    """Cortes de montaje dentro de un tramo (detección de cambio de escena, umbral 0,32 + cortes medidos a mano), en segundos del tramo."""
    if path in _CUTS: return _CUTS[path]
    base = os.path.basename(path); vid = base[:11]; a0 = float(base[12:19])
    manual = [(T - a0) / 1.001 for T in MANUAL_CUTS.get(vid, [])]
    cache = path + ".cuts.json"
    if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(path):
        _CUTS[path] = sorted(json.load(open(cache)) + manual); return _CUTS[path]
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", path, "-an", "-vf", "scale=480:270,select='gt(scene,0.32)',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True)
    cs = []
    for line in r.stderr.splitlines():
        if "pts_time:" in line:
            try: cs.append(round(float(line.split("pts_time:")[1].split()[0]), 3))
            except ValueError: pass
    json.dump(cs, open(cache, "w")); _CUTS[path] = sorted(cs + manual); return _CUTS[path]

def x_window(sh):
    """→ (archivo del tramo, inicio dentro del tramo, segundos continuos disponibles, ¿vertical?)"""
    if "_xw" in sh: return sh["_xw"]
    vid, T = parse_x(sh["src"])
    for a, b in MZ.windows_for(vid):
        if a <= T < b:
            path = MZ.name(vid, a, b); loc = (T - a) / 1.001; avail = (b - T) / 1.001 - 0.12
            if os.path.exists(path):
                cs = mez_cuts(path) if (vid in EDITED and not sh.get("nocut")) else sorted((T_ - a) / 1.001 for T_ in MANUAL_CUTS.get(vid, []))
                nxt = next((x for x in cs if x > loc + 0.05), None)
                if nxt is not None: avail = min(avail, nxt - loc - 0.05)
            sh["_xw"] = (path, loc, avail, vid in MZ.VERTICAL); return sh["_xw"]
    raise ValueError(f"no hay tramo extraído para {sh['src']}")

class Clip(G.Clip):
    """Lector de un tramo mezzanine (ya está a 1920×1080 o 1080×1920 y 30 fps): sin reescalar ni cambiar la cadencia."""
    def _open(self):
        w, h = self.size
        self.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "fatal", "-ss", f"{self.t0:.3f}", "-i", self.path, "-t", f"{self.dur:.3f}", "-an",
                                   "-vf", f"scale={w}:{h},format=rgba", "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                                  stdout=subprocess.PIPE, bufsize=w * h * 4 * 2)
        self.i = -1; self.eof = False

_CL = {}
def x_frame(sh, tau, slot):
    path, loc, avail, vert = x_window(sh)
    k = int(math.floor(tau * FPS + 1e-6))
    kmax = max(0, int(avail * FPS) - 1)
    if k > kmax: sh["_over"] = max(sh.get("_over", 0), k - kmax); k = kmax     # validate() impide que pase
    cl = _CL.get(slot)
    size = (1080, 1920) if vert else (W, H)
    if cl is None or cl.path != path or abs(cl.t0 - loc) > 1e-3:
        if cl: cl.close()
        cl = Clip(path, loc, avail + 0.3, size); _CL[slot] = cl
    return cl.get(k), vert

def draw_img(c, img, z=1.0, cx=0.5, cy=0.5, k=0.0, a=1.0, cf=None):
    """Dibuja la imagen cubriendo el cuadro con zoom z. El punto (cx, cy) de la imagen se lleva hacia el centro en
    proporción k (0 = queda en su sitio, 1 = centrado), sin dejar bordes vacíos."""
    iw, ih = img.width(), img.height(); s = max(W / iw, H / ih) * z; dw, dh = iw * s, ih * s
    tx = lerp(W * cx, W / 2, k); ty = lerp(H * cy, H / 2, k)
    x = tx - dw * cx; y = ty - dh * cy
    x = min(0, max(W - dw, x)); y = min(0, max(H - dh, y))
    p = skia.Paint(); p.setAlphaf(a)
    if cf is not None: p.setColorFilter(cf)
    c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, dw, dh), SO_HQ if z > 1.25 else SO, p)
    return x, y, s

def footage(c, sh, tau, d, slot="main"):
    img, vert = x_frame(sh, tau, slot)
    if img is None: return
    if vert:
        # tarjeta vertical: fondo con la misma imagen ampliada y desenfocada, y el vídeo nítido a la derecha o al centro
        bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(36, 36))
        c.drawImageRect(img, skia.Rect.MakeXYWH(-100, -H * 0.9, W + 200, (W + 200) * 1920 / 1080), SO, bg)
        rect(c, 0, 0, W, H, "#06070A", 0.55)
        vh = 1000 * (1 + 0.03 * clamp(tau / max(d, 0.1))); vw = vh * 1080 / 1920
        side = sh.get("vside", "right"); x = W - vw - 150 if side == "right" else (W - vw) / 2; y = (H - vh) / 2
        rect(c, x + 14, y + 18, vw, vh, "#000000", 0.5, r=34, blur=18)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, vw, vh), 30, 30), True)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, vw, vh), SO_HQ); c.restore()
        rect(c, x, y, vw, vh, "#FFFFFF", 0.85, r=30, stroke=4)
        if sh.get("vtitle"):
            p = ease_out(prog(tau, 0.1, 0.5))
            draw_par(c, sh["vtitle"], 140, 420, "anton", 92, 820, lh=1.05, color=WHITE, a=p, tracking=1)
        return
    zm = sh.get("zoom")
    if zm:   # zoom animado a un punto: (cx, cy, z final, segundos)
        cx, cy, z1, tz = zm; t0z = sh.get("zoom_at", 0.0)
        e = ease_io(prog(tau, t0z, t0z + tz)); z = lerp(sh.get("z0", 1.0), z1, e)
        ox, oy, sc = draw_img(c, img, z, cx, cy, e)
    else:
        z0, z1 = sh.get("z", (1.0, 1.05)); fx, fy = sh.get("f", (0.5, 0.5))
        z = lerp(z0, z1, clamp(tau / max(d, 0.1)))
        ox, oy, sc = draw_img(c, img, z, fx, fy, 0.0, cf=_bw() if sh.get("bw") else None)
    hl = sh.get("hl")
    if sh.get("hl_src"):   # recuadro en coordenadas de la imagen original (0-1): sigue al zoom
        u0, v0, u1, v1 = sh["hl_src"]; iw, ih = img.width(), img.height()
        hl = (ox + u0 * iw * sc, oy + v0 * ih * sc, (u1 - u0) * iw * sc, (v1 - v0) * ih * sc)
    if hl:   # recuadro que señala un elemento de la imagen
        x, y, w_, h_ = hl; x = max(6, x); w_ = min(w_, W - 6 - x); p = ease_out_back(prog(tau, sh.get("hl_at", 0.45), sh.get("hl_at", 0.45) + 0.35))
        if p > 0:
            c.save(); c.translate(x + w_ / 2, y + h_ / 2); c.scale(1.15 - 0.15 * p, 1.15 - 0.15 * p); c.translate(-(x + w_ / 2), -(y + h_ / 2))
            rect(c, x, y, w_, h_, YEL, clamp(p * 1.5), r=10, stroke=7); c.restore()
            if sh.get("hl_txt"): G.chip(c, x, y + h_ + 14, sh["hl_txt"], clamp(p * 1.5), 24, YEL)

def _bw():
    m = [0.3, 0.59, 0.11, 0, 0] * 3 + [0, 0, 0, 1, 0]
    return skia.ColorFilters.Matrix(m)

# ================================================================ tabla de planos
_T = {}
def table(ctx):
    if "shots" in _T: return _T
    V, tl = ctx.V, ctx.tl; shots = []; beats = []; chapters = []
    for bi, (b, bd) in enumerate(zip(V["beats"], tl["beats"])):
        beats.append(dict(b=b, bd=bd))
        if b.get("chapter"): chapters.append((bd["start"] + 0.05, b["chapter"]))
        last = bd["start"]
        for sh in b.get("shots", []):
            if sh["anchor"] is None: t0 = bd["start"]; wt = None; word = None
            else:
                wt, word = G._word_time(bd["sents"], sh["anchor"], last)
                if wt is None: raise ValueError(f"ancla «{sh['anchor']}» no encontrada en el beat {bi} ({b.get('id')})")
                t0 = wt - LEAD
            t0 += sh.get("dt", 0.0)
            ns = dict(sh, t0=t0, beat=bi, word_t=wt, word=word, k=len(shots))
            after = (wt + 0.01) if wt is not None else bd["start"]
            # cues: momentos (relativos al inicio del plano) en que la voz dice cada fragmento → animaciones a tiempo
            if sh.get("cues"):
                st = []; aft = after - 0.02
                for frag in sh["cues"]:
                    ct, _ = G._word_time(bd["sents"], frag, aft)
                    if ct is None: raise ValueError(f"cue «{frag}» no encontrada en el beat {bi} ({b.get('id')})")
                    st.append(round(ct - t0, 3)); aft = ct + 0.01
                ns["st"] = st
            # sync: el suceso del juego (segundo T del original) coincide con la palabra `frag` (+ desfase)
            if sh.get("sync"):
                frag, Tev, lag = sh["sync"]; ct, _ = G._word_time(bd["sents"], frag, after - 0.02)
                if ct is None: raise ValueError(f"sync «{frag}» no encontrada en el beat {bi}")
                vid, _tt = parse_x(sh["src"]); ns["src"] = f"x:{vid}@{Tev - (ct + lag - t0) * 1.001:.3f}"
            shots.append(ns)
            last = after
    shots.sort(key=lambda s: s["t0"])
    # cont: el plano sigue el mismo vídeo justo donde lo dejó el plano anterior de esa fuente (sin repetir ni saltar)
    lastx = {}
    for s in shots:
        if not s["src"].startswith("x:"): continue
        vid, T = parse_x(s["src"])
        if s.get("cont"):
            if vid not in lastx: raise ValueError(f"cont sin plano anterior de {vid}")
            pT, pt0 = lastx[vid]; T = pT + (s["t0"] - pt0) * 1.001; s["src"] = f"x:{vid}@{T:.3f}"
        lastx[vid] = (T, s["t0"])
    for i, s in enumerate(shots): s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else tl["total"]
    _T.update(shots=shots, starts=[s["t0"] for s in shots], beats=beats, chapters=chapters, bstarts=[x["bd"]["start"] for x in beats])
    return _T

def validate(ctx, verbose=True):
    """Cada plano de gameplay debe tener material continuo para toda su duración (más su transición de entrada del siguiente)."""
    T = table(ctx); bad = []
    for i, s in enumerate(T["shots"]):
        if not s["src"].startswith("x:"): continue
        nx = T["shots"][i + 1] if i + 1 < len(T["shots"]) else None
        # el plano se sigue dibujando durante la transición hacia el siguiente (los cortes secos entre gameplay no tienen)
        trd = (nx.get("tr") or (0, 0.13 if nx["src"].startswith("g:") else 0.0))[1] if nx else 0.0
        d = s["t1"] - s["t0"] + trd + 0.05
        path, loc, avail, vert = x_window(s)
        if not os.path.exists(path): bad.append((s, "falta el tramo", 0)); continue
        if d > avail: bad.append((s, f"dura {d:.2f} s y solo hay {avail:.2f} s continuos", d - avail))
    if verbose:
        for s, why, _ in bad: print(f"  [plano] {s['t0']:7.2f} s · {s['src']} · {why} · ancla «{s['anchor']}»")
        print(f"  validación de planos: {len(T['shots'])} planos · {len(bad)} con problemas")
    return bad

# ================================================================ escena única (todo el vídeo)
_SURF = {}
def _surf(name):
    if name not in _SURF: _SURF[name] = skia.Surface(W, H)
    return _SURF[name]

def scene(c, t, info, ctx):
    gt = info.start + t; T = table(ctx)
    i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    tau = gt - sh["t0"]; d = max(0.05, sh["t1"] - sh["t0"])
    tr = sh.get("tr"); trd = tr[1] if tr else (0.13 if (i > 0 and (sh["src"].startswith("g:") or T["shots"][i - 1]["src"].startswith("g:"))) else 0)
    if i > 0 and tau < trd:
        pv = T["shots"][i - 1]; kind = tr[0] if tr else "fade"; p = tau / trd
        sa = _surf("A"); ca = sa.getCanvas(); ca.clear(skia.ColorBLACK); draw_shot(ca, pv, gt - pv["t0"], max(0.05, pv["t1"] - pv["t0"]), ctx, slot="prev")
        sb = _surf("B"); cb = sb.getCanvas(); cb.clear(skia.ColorBLACK); draw_shot(cb, sh, tau, d, ctx)
        blend(c, sa.makeImageSnapshot(), sb.makeImageSnapshot(), kind, p)
    else:
        draw_shot(c, sh, tau, d, ctx)

def blend(c, A, B, kind, p):
    e = ease_io(clamp(p))
    if kind == "flash":
        c.drawImage(A if p < 0.5 else B, 0, 0); rect(c, 0, 0, W, H, "#FFFFFF", math.sin(p * math.pi) ** 2 * 0.85)
    elif kind in ("whip", "whipl"):
        sg = 1 if kind == "whip" else -1
        c.save(); c.translate(-sg * W * e, 0); c.drawImage(A, 0, 0); c.restore()
        c.save(); c.translate(sg * W * (1 - e), 0); c.drawImage(B, 0, 0); c.restore()
        if 0.1 < p < 0.9:
            pp = skia.Paint(); pp.setImageFilter(skia.ImageFilters.Blur(30 * math.sin(p * math.pi), 0)); c.saveLayer(skia.Rect.MakeWH(W, H), pp); c.restore()
    elif kind == "zoom":
        c.save(); s = 1 + 0.3 * e; c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
        pa = skia.Paint(); pa.setAlphaf(1 - e); c.drawImage(A, 0, 0, SO, pa); c.restore()
        c.save(); s = 0.88 + 0.12 * e; c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
        pb = skia.Paint(); pb.setAlphaf(e); c.drawImage(B, 0, 0, SO, pb); c.restore()
    elif kind == "dip":
        c.drawImage(A if p < 0.5 else B, 0, 0); rect(c, 0, 0, W, H, "#000000", math.sin(p * math.pi))
    elif kind == "glitch":
        c.drawImage(A if p < 0.5 else B, 0, 0); rng = np.random.default_rng(int(p * 997))
        for _ in range(8):
            y = int(rng.integers(0, H)); h = int(rng.integers(8, 80)); dx = float(rng.integers(-110, 110)) * math.sin(p * math.pi)
            c.save(); c.clipRect(skia.Rect.MakeXYWH(0, y, W, h)); c.drawImage(B if rng.random() < p else A, dx, 0); c.restore()
        rect(c, 0, 0, W, H, RED, 0.10 * math.sin(p * math.pi))
    else:   # fundido
        c.drawImage(A, 0, 0); pp = skia.Paint(); pp.setAlphaf(e); c.drawImage(B, 0, 0, SO, pp)

def draw_shot(c, sh, tau, d, ctx, slot="main"):
    k, v = sh["src"].split(":", 1)
    if k == "g":
        name = v.split("@")[0]; GFX[name](c, tau, d, sh, ctx)
    else: footage(c, sh, tau, d, slot)
    if sh.get("dim"): rect(c, 0, 0, W, H, "#05060A", sh["dim"])
    if sh.get("label"): G.act_label(c, sh["label"], prog(tau, 0.05, 0.35) * (1 - prog(tau, d - 0.2, d)))
    if sh.get("big"): big_text(c, sh["big"], tau, d, sh.get("big_col", YEL))
    if sh.get("stamp"): G.stamp_label(c, sh["stamp"], prog(tau, sh.get("stamp_at", 0.4), sh.get("stamp_at", 0.4) + 0.3))
    if sh.get("timer"): timer_badge(c, sh["timer"], tau)
    if sh.get("gamemsg"): game_msg_chip(c, sh["gamemsg"], tau, d)
    if sh.get("vig", True) and k == "x": vignette(c, W, H, 0.35)

def big_text(c, lines, tau, d, col):
    if isinstance(lines, str): lines = [lines]
    p = ease_out_back(prog(tau, 0.08, 0.42)); q = 1 - prog(tau, d - 0.18, d)
    if p <= 0: return
    y0 = H / 2 - (len(lines) - 1) * 70
    for j, ln in enumerate(lines):
        y = y0 + j * 140; s = 0.6 + 0.4 * p
        c.save(); c.translate(W / 2, y); c.scale(s, s)
        draw_text(c, ln, 6, 46, "anton", 150, "#000000", 0.55 * clamp(p) * q, align="center", tracking=3)
        draw_text(c, ln, 0, 40, "anton", 150, col if j == len(lines) - 1 else WHITE, clamp(p * 1.5) * q, align="center", tracking=3)
        c.restore()

def timer_badge(c, txt, tau):
    p = ease_out_back(prog(tau, 0.15, 0.5))
    if p <= 0: return
    x, y = W / 2, 250; c.save(); c.translate(x, y); c.scale(p, p)
    f = font("anton", 96); w = text_w(txt, f, 3) + 170
    rect(c, -w / 2, -80, w, 150, INK, 0.88, r=20); rect(c, -w / 2, -80, w, 150, YEL, 1, r=20, stroke=6)
    icon(c, "clock", -w / 2 + 75, -5, 84, YEL, 1)
    draw_text(c, txt, 40, 30, "anton", 96, WHITE, 1, align="center", tracking=3); c.restore()

def game_msg_chip(c, txt, tau, d):
    """Rótulo «mensaje del juego» junto al recuadro del mensaje original (la traducción va en los subtítulos)."""
    p = ease_out(prog(tau, 0.2, 0.5)) * (1 - prog(tau, d - 0.15, d))
    if p > 0: G.chip(c, W / 2 - 300, 142, txt, p, 26, CYA)

# ================================================================ rótulos fijos
TAGS = {"PARTIDA": (GRN, "SE VE EN LA PARTIDA"), "ROCKSTAR": (YEL, "SEGÚN ROCKSTAR, ANTES DEL LANZAMIENTO"),
        "GUIAS": (CYA, "SEGÚN LAS GUÍAS DEL JUEGO"), "PRENSA": (CYA, "DATO DE LA PRENSA ESPECIALIZADA")}
def cert(c, kind, a=1.0, y=82, left=False):
    if a <= 0 or kind not in TAGS: return
    col, txt = TAGS[kind]; size = 24; f = font("ovmono", size); w = text_w(txt, f, 1) + size * 2.2; h = size * 1.75
    x = 40 if left else W / 2 - w / 2
    rect(c, x, y, w, h, INK, 0.84 * a, r=h / 2); rect(c, x, y, w, h, col, a, r=h / 2, stroke=3)
    circle(c, x + size * 0.95, y + h / 2, size * 0.32, col, a)
    draw_text(c, txt, x + size * 1.6, y + h / 2 + size * 0.36, "ovmono", size, col, a, tracking=1)

def credit(c, sh):
    vid, T = parse_x(sh["src"])
    txt = f"Gameplay: {AUTHOR.get(vid, XCAT.get(vid, {}).get('autor', vid))} · YouTube · {int(T // 60)}:{int(T % 60):02d}"
    f = font("ovmonomd", 20); w = text_w(txt, f, 0.5) + 34
    rect(c, W - w - 30, H - 64, w, 36, "#000000", 0.55, r=5); draw_text(c, txt, W - w - 13, H - 39, "ovmonomd", 20, "#F3F0E9", 0.9, tracking=0.5)

def overlay(c, gt, ctx):
    T = table(ctx)
    i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    bi = max(0, bisect.bisect_right(T["bstarts"], gt) - 1); b = T["beats"][bi]["b"]
    if gt > ctx.total - 20.3 or sh["src"] in ("g:sting",): return
    ch = None
    for st, cc in T["chapters"]:
        if gt >= st: ch = (st, cc)
    if ch and gt < ctx.total - 60:
        st, (n, name) = ch; tt = gt - st
        if tt < 2.7:
            p = ease_out(prog(tt, 0, 0.35)) * (1 - prog(tt, 2.3, 2.7))
            rect(c, 0, H / 2 - 120, W * ease_out(prog(tt, 0, 0.35)), 240, INK, 0.84 * p)
            rect(c, 0, H / 2 - 120, W * ease_out(prog(tt, 0, 0.35)), 8, YEL, p)
            draw_text(c, f"{n:02d}", 120, H / 2 + 62, "anton", 200, YEL, p)
            draw_text(c, name, 380, H / 2 + 50, "anton", 120, WHITE, p, tracking=3)
        elif not sh.get("clean"):
            txt = f"{n:02d} · {name}"; f = font("ovmonomd", 22); w = text_w(txt, f, 0.5) + 44
            G.chip(c, W / 2 - w / 2, 26, txt, 0.95, 22, YEL)
    if not sh.get("clean"):
        ck = sh.get("cert", b.get("cert"))
        if ck and (not sh["src"].startswith("g:") or sh.get("cert")): cert(c, ck, 1.0, y=82 if not sh["src"].startswith("g:") else 92, left=sh["src"].startswith("g:"))
        if sh["src"].startswith("x:"): credit(c, sh)
    G.subtitles(c, gt, ctx)
    if gt > 3: K.watermark(c, W, H, 0.45, corner="tl", size=40)

# ================================================================ gráficos propios (g:)
def panel(c, t, dark=0.0):
    """Fondo de los gráficos: asfalto nocturno con rejilla y luz de sirena muy suave."""
    rect(c, 0, 0, W, H, "#0A0B10", 1)
    grid(c, W, H, 80, "#FFFFFF", 0.035)
    r = 0.5 + 0.5 * math.sin(t * 2.4)
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(-100, -100, 1300, [hexc("#FF2D55", 0.10 * r), hexc("#FF2D55", 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(W + 100, -100, 1300, [hexc("#2D7BFF", 0.10 * (1 - r)), hexc("#2D7BFF", 0)]))
    if dark: rect(c, 0, 0, W, H, "#000000", dark)

def star(c, x, y, r, mode, a=1.0):
    """mode: 'hollow' | 'white' | 'red' | 'grey' | 'off'"""
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    if mode == "hollow": draw_poly(c, pts, "#FFFFFF", a, stroke=max(2, r * 0.12))
    elif mode == "off": draw_poly(c, pts, "#3A3D46", a)
    else: draw_poly(c, pts, {"white": "#FFFFFF", "red": "#E23B3B", "grey": "#8A8F99"}[mode], a)

def title_top(c, txt, p, sub=None, col=YEL):
    draw_text(c, txt, W / 2, 190, "anton", 96, col, p, align="center", tracking=3)
    if sub: draw_text(c, sub, W / 2, 250, "intersb", 34, WHITE, 0.85 * p, align="center")

def g_sting(c, t, d, sh, ctx):
    class I: pass
    K.brand_sting(c, t, I(), ctx)

def g_creators(c, t, d, sh, ctx):
    panel(c, t)
    title_top(c, "PARTIDAS REALES", ease_out(prog(t, 0, 0.4)), "Grabadas por jugadores después del lanzamiento (19 de noviembre de 2026)")
    rows = [("MikeTheGoon", "Huida de 5 estrellas en la playa"), ("GTAsatara", "Un delito sin testigos"), ("IGN", "Guías: 6 estrellas, ropa, modo Focus")]
    for j, (a_, b_) in enumerate(rows):
        p = ease_out_back(prog(t, 0.25 + 0.15 * j, 0.6 + 0.15 * j)); y = 400 + j * 150
        if p <= 0: continue
        c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        rect(c, W / 2 - 620, y - 60, 1240, 120, INK, 0.9, r=16); rect(c, W / 2 - 620, y - 60, 12, 120, YEL, 1)
        draw_text(c, a_, W / 2 - 570, y + 22, "anton", 70, WHITE, 1, tracking=1)
        draw_text(c, b_, W / 2 + 580, y + 14, "intersb", 34, YEL, 1, align="right"); c.restore()
    draw_text(c, "Créditos de cada plano en pantalla y en la descripción", W / 2, 900, "ovmonomd", 26, GRAY, ease_out(prog(t, 0.8, 1.2)), align="center")

def g_legend(c, t, d, sh, ctx):
    panel(c, t)
    title_top(c, "DOS TIPOS DE DATO", ease_out(prog(t, 0, 0.35)))
    for j, (kind, sub) in enumerate([("PARTIDA", "Lo que aparece en pantalla en partidas reales"), ("ROCKSTAR", "Lo que Rockstar explicó antes de que saliera el juego")]):
        p = ease_out_back(prog(t, sh.get("st", [0.3, 1.2])[j], sh.get("st", [0.3, 1.2])[j] + 0.4))
        if p <= 0: continue
        col, txt = TAGS[kind]; y = 470 + j * 220
        c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        rect(c, W / 2 - 700, y - 80, 1400, 160, INK, 0.9, r=80); rect(c, W / 2 - 700, y - 80, 1400, 160, col, 1, r=80, stroke=6)
        circle(c, W / 2 - 610, y, 26, col, 1)
        draw_text(c, txt, W / 2 - 550, y + 8, "anton", 64, col, 1, tracking=2)
        draw_text(c, sub, W / 2 - 550, y + 55, "intersb", 30, WHITE, 0.9); c.restore()

def g_nospoil(c, t, d, sh, ctx):
    panel(c, t)
    for j, txt in enumerate(["0 MISIONES", "0 FINALES", "0 TRAMA"]):
        p = ease_out_back(prog(t, 0.12 * j, 0.12 * j + 0.35), 2.0)
        c.save(); c.translate(W / 2, 330 + j * 190); c.rotate(-4 + 4 * j); c.scale(1.6 - 0.6 * p, 1.6 - 0.6 * p)
        f = font("ovblk", 92); w = text_w(txt, f, 4) + 90
        rect(c, -w / 2, -88, w, 130, "#FF4A3D", clamp(p * 2), r=12, stroke=9)
        draw_text(c, txt, 0, 12, "ovblk", 92, "#FF4A3D", clamp(p * 2), align="center", tracking=4); c.restore()
    p = ease_out(prog(t, 0.9, 1.3)); draw_text(c, "SOLO CÓMO FUNCIONA EL JUEGO POR DENTRO", W / 2, 880, "anton", 54, WHITE, p, align="center", tracking=2)

def g_teaser(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out(prog(t, 0, 0.4)); title_top(c, "AL FINAL DEL VIDEO", p)
    q = ease_out_back(prog(t, 0.3, 0.8))
    if q > 0:
        n = int(count_up(321, prog(t, 0.3, 2.2)))
        c.save(); c.translate(W / 2 - 330, 560); c.scale(q, q)
        draw_text(c, f"{n}+", 0, 60, "anton", 230, RED, 1, align="center"); draw_text(c, "ENEMIGOS MUERTOS", 0, 140, "anton", 48, WHITE, 1, align="center", tracking=2); c.restore()
    st = sh.get("st") or [1.6]
    r = ease_out_back(prog(t, st[0], st[0] + 0.5))
    if r > 0:
        c.save(); c.translate(W / 2 + 360, 560); c.scale(r, r)
        rect(c, -300, -110, 600, 220, INK, 0.9, r=20); rect(c, -300, -110, 600, 220, YEL, 1, r=20, stroke=6)
        draw_text(c, "PERFIL:", 0, -20, "anton", 54, WHITE, 1, align="center", tracking=2)
        draw_text(c, "PROFESIONAL", 0, 70, "anton", 96, YEL, 1, align="center", tracking=2); c.restore()
        draw_text(c, "?", W / 2 + 760, 640, "anton", 220, YEL, r * (0.6 + 0.4 * pulse(t, 0.8)), align="center")

def count_up(val, p): return val * ease_out(clamp(p))

def g_witness(c, t, d, sh, ctx):
    panel(c, t)
    title_top(c, "LA POLICÍA SE ENTERA SI…", ease_out(prog(t, 0, 0.35)))
    items = [("eye", "ALGUIEN LO VE", "un testigo"), ("bolt", "SALTA UNA ALARMA", "una alarma")]
    st = sh.get("st", [0.3, 1.0])
    for j, (ic, a_, b_) in enumerate(items):
        p = ease_out_back(prog(t, st[j], st[j] + 0.4))
        if p <= 0: continue
        x = W / 2 + (-380 if j == 0 else 380); y = 560
        c.save(); c.translate(x, y); c.scale(p, p)
        circle(c, 0, -60, 150, INK, 0.92); circle(c, 0, -60, 150, YEL, 1, stroke=8); icon(c, ic, 0, -60, 150, YEL, 1)
        draw_text(c, a_, 0, 170, "anton", 64, WHITE, 1, align="center", tracking=2); c.restore()
    q = ease_out(prog(t, 1.6, 2.0)); draw_text(c, "SIN TESTIGOS, NO HAY ESTRELLAS", W / 2, 880, "anton", 60, YEL, q, align="center", tracking=3)

def g_hollow(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out_back(prog(t, 0.05, 0.45))
    for j in range(2): star(c, W / 2 - 110 + j * 220, 400, 120 * p, "hollow", clamp(p * 1.5))
    q = ease_out(prog(t, 0.6, 1.0))
    draw_text(c, "ESTRELLA HUECA", W / 2, 640, "anton", 110, WHITE, q, align="center", tracking=3)
    st = sh.get("st") or [1.2, 2.0]
    r = ease_out(prog(t, st[0], st[0] + 0.4))
    draw_text(c, "Saben que hubo un delito", W / 2 - 40, 760, "intersb", 50, GRN, r, align="right")
    draw_text(c, "No saben quién fue", W / 2 + 40, 760, "intersb", 50, RED, ease_out(prog(t, st[1], st[1] + 0.4)), align="left")
    draw_text(c, "·", W / 2, 760, "anton", 50, WHITE, r, align="center")

def g_stars(c, t, d, sh, ctx):
    """Los tres estados que se ven en las partidas (hueca / blanca / roja)."""
    panel(c, t)
    title_top(c, "EL COLOR DE LAS ESTRELLAS", ease_out(prog(t, 0, 0.35)))
    rows = [("hollow", "HUECAS", "No saben quién eres"), ("white", "BLANCAS", "Te están persiguiendo"), ("red", "ROJAS", "Te perdieron de vista, pero te siguen buscando")]
    st = sh.get("st", [0.3, 1.0, 1.7])
    for j, (m, a_, b_) in enumerate(rows):
        p = ease_out_back(prog(t, st[j], st[j] + 0.4))
        if p <= 0: continue
        y = 380 + j * 200; c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        rect(c, W / 2 - 760, y - 80, 1520, 160, INK, 0.9, r=18)
        for k in range(3): star(c, W / 2 - 660 + k * 90, y, 38, m, 1)
        draw_text(c, a_, W / 2 - 340, y + 24, "anton", 76, {"hollow": WHITE, "white": WHITE, "red": "#FF5A5A"}[m], 1, tracking=2)
        draw_text(c, b_, W / 2 - 20, y + 16, "intersb", 36, WHITE, 0.92); c.restore()

# --- iconos del HUD (recortes reales de las partidas, ver PROYECTO_DE_EDICION/recursos/iconos_hud)
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_GTA6", "PROYECTO_DE_EDICION", "recursos", "iconos_hud")
def hud_icon(c, name, x, y, size, a=1.0):
    p = os.path.join(ICON_DIR, f"{name}.png")
    if os.path.exists(p):
        img = G.load_img(p); pa = skia.Paint(); pa.setAlphaf(a)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x - size / 2, y - size / 2, size, size), SO_HQ, pa)
    else:
        circle(c, x, y, size / 2, "#B3202A", a); icon(c, {"percha": "tag", "silueta": "user", "auto": "car", "pistola": "bolt"}[name], x, y, size * 0.55, WHITE, a)

def g_icons(c, t, d, sh, ctx):
    panel(c, t)
    step = sh.get("step", 0)
    title_top(c, "LO QUE SABE LA POLICÍA", ease_out(prog(t, 0, 0.35)), "Iconos rojos bajo las estrellas, vistos en partidas reales")
    items = [("percha", "TU ROPA"), ("silueta", "TU ASPECTO"), ("auto", "TU VEHÍCULO"), ("pistola", "")]
    st = sh.get("st") or [0.2, 0.6, 1.0, 1.4]
    # paso 0: los iconos aparecen al nombrarlos; paso 1: ya están y se etiquetan en el orden de la voz (aspecto, ropa, vehículo)
    lab_at = {"silueta": st[0], "percha": st[1], "auto": st[2]} if step >= 1 else {}
    for j, (ic, lab) in enumerate(items):
        p = 1.0 if step >= 1 else ease_out_back(prog(t, st[j], st[j] + 0.35))
        if p <= 0: continue
        x = W / 2 - 630 + j * 420; y = 560; dim = 0.35 if (step >= 1 and ic == "pistola") else 1.0
        c.save(); c.translate(x, y); c.scale(p, p)
        rect(c, -170, -200, 340, 400, INK, 0.9 * dim, r=24); hud_icon(c, ic, 0, -50, 190, dim)
        if step == 0:
            draw_text(c, {"percha": "UNA PERCHA", "silueta": "UNA SILUETA", "auto": "UN AUTO", "pistola": "UNA PISTOLA"}[ic], 0, 135, "anton", 50, WHITE, 1, align="center", tracking=1)
        elif ic in lab_at:
            e = ease_out_back(prog(t, lab_at[ic], lab_at[ic] + 0.3))
            if e > 0:
                rect(c, -170, -200, 340, 400, YEL, clamp(e), r=24, stroke=6)
                draw_text(c, lab, 0, 135, "anton", 50, YEL, clamp(e * 1.5), align="center", tracking=1)
        c.restore()
    if step >= 1:
        ta = st[3] if len(st) > 3 else 2.0
        q = ease_out_back(prog(t, ta, ta + 0.4))
        if q > 0:
            c.save(); c.translate(W / 2, 900); c.scale(q, q)
            rect(c, -560, -55, 1120, 110, INK, 0.92, r=55); rect(c, -560, -55, 1120, 110, YEL, 1, r=55, stroke=5)
            draw_text(c, "SEGÚN ROCKSTAR, TAMBIÉN SI JASON Y LUCÍA VAN JUNTOS", 0, 17, "anton", 46, YEL, 1, align="center", tracking=1); c.restore()

def g_ficha(c, t, d, sh, ctx):
    """Ficha policial en directo: los datos que tiene la policía, y cómo se van tachando."""
    panel(c, t)
    p = ease_out_back(prog(t, 0.0, 0.45))
    c.save(); c.translate(W / 2, H / 2 + 20); c.scale(p, p); c.rotate(-2.0); c.translate(-W / 2, -(H / 2 + 20))
    x, y, w, h = W / 2 - 560, 170, 1120, 780
    rect(c, x + 16, y + 20, w, h, "#000000", 0.5, r=12, blur=20); rect(c, x, y, w, h, "#F2EAD3", 1, r=12)
    rect(c, x, y, w, 120, "#1E3A8A", 1, r=12); rect(c, x, y + 100, w, 20, "#1E3A8A", 1)
    draw_text(c, "VICE CITY POLICE · FICHA EN DIRECTO", x + 50, y + 78, "ovblk", 44, "#FFFFFF", 1, tracking=2)
    rows = [("percha", "ROPA", "La que llevas puesta"), ("silueta", "ASPECTO", "Tu descripción"), ("auto", "VEHÍCULO", "El que usas ahora")]
    st = sh.get("st") or []
    cross = sh.get("cross") or ([("percha", st[0] + 0.1), ("auto", st[0] + 0.7)] if st else [])
    for j, (ic, a_, b_) in enumerate(rows):
        yy = y + 210 + j * 170; q = ease_out(prog(t, 0.35 + 0.2 * j, 0.6 + 0.2 * j))
        hud_icon(c, ic, x + 120, yy, 110, q)
        draw_text(c, a_, x + 210, yy + 4, "anton", 66, "#1A1A1A", q, tracking=2)
        draw_text(c, b_, x + 210, yy + 52, "intersb", 30, "#444444", q)
        if ic in [cc[0] for cc in cross]:
            ct = [cc[1] for cc in cross if cc[0] == ic][0]; e = ease_out(prog(t, ct, ct + 0.35))
            if e > 0:
                line(c, x + 200, yy - 10, x + 200 + 760 * e, yy - 4, "#D7263D", 1, w=14)
                if e >= 1: draw_text(c, "BORRADO", x + w - 90, yy + 14, "ovblk", 44, "#D7263D", 1, align="right", tracking=3)
    c.restore()

def g_meter(c, t, d, sh, ctx):
    """Medidor de 6 estrellas: lo que provoca cada nivel, según las partidas y las guías."""
    panel(c, t)
    lvl = sh.get("lvl", 4); note = sh.get("note"); lock6 = sh.get("lock6", False); st = sh.get("st") or []
    if st: sh = dict(sh, lock_at=st[0], note_at=st[0] + 0.15)
    p = ease_out(prog(t, 0, 0.35)); title_top(c, sh.get("title", "LA ESCALADA"), p)
    if sh.get("reset"):   # de 6 estrellas a ninguna, cuando la voz dice «se reinician»
        ra = st[0] if st else sh.get("reset_at", 0.6); lvl = 6 - int(6 * clamp(prog(t, ra, ra + 0.5)))
    for k in range(6):
        q = ease_out_back(prog(t, 0.08 * k, 0.08 * k + 0.35)); x = W / 2 - 500 + k * 200; y = 470
        mode = "white" if k < lvl else "off"
        if k == 5 and lock6: mode = "off"
        star(c, x, y, 78 * q, mode, clamp(q * 1.5))
        if k == 5 and lock6:
            e = ease_out_back(prog(t, sh.get("lock_at", 0.6), sh.get("lock_at", 0.6) + 0.4)); icon(c, "lock", x, y + 6, 70 * e, RED, clamp(e * 1.5))
    if note:
        r = ease_out_back(prog(t, sh.get("note_at", 0.5), sh.get("note_at", 0.5) + 0.4))
        if r > 0:
            c.save(); c.translate(W / 2, 760); c.scale(r, r)
            f = font("anton", 64); w = text_w(note, f, 2) + 120
            rect(c, -w / 2, -70, w, 140, INK, 0.92, r=20); rect(c, -w / 2, -70, w, 140, sh.get("note_col", YEL), 1, r=20, stroke=6)
            draw_text(c, note, 0, 24, "anton", 64, sh.get("note_col", YEL), 1, align="center", tracking=2); c.restore()
    if sh.get("sub"): draw_text(c, sh["sub"], W / 2, 885, "intersb", 38, WHITE, ease_out(prog(t, 0.9, 1.3)), align="center")

def g_split(c, t, d, sh, ctx):
    panel(c, t)
    st = sh.get("st") or [0.05, 1.2, 0.6]   # persecución, ≠, búsqueda (orden de la voz)
    p = ease_out_back(prog(t, st[0], st[0] + 0.4)); r = ease_out_back(prog(t, st[1], st[1] + 0.3), 2.2); q = ease_out_back(prog(t, st[2], st[2] + 0.4))
    for j, (a_, b_, col, pp) in enumerate([("PERSECUCIÓN", "Te ven y te siguen", WHITE, p), ("BÚSQUEDA", "Tienen tu descripción", "#FF5A5A", q)]):
        if pp <= 0: continue
        x = W / 2 + (-430 if j == 0 else 430); c.save(); c.translate(x, 520); c.scale(pp, pp)
        rect(c, -360, -200, 720, 400, INK, 0.9, r=24); rect(c, -360, -200, 720, 400, col, 1, r=24, stroke=6)
        for k in range(3): star(c, -90 + k * 90, -90, 36, "white" if j == 0 else "red", 1)
        draw_text(c, a_, 0, 40, "anton", 84, col, 1, align="center", tracking=2)
        draw_text(c, b_, 0, 110, "intersb", 38, WHITE, 0.9, align="center"); c.restore()
    if r > 0:
        c.save(); c.translate(W / 2, 520); c.scale(r, r); circle(c, 0, 0, 70, YEL, 1)
        rect(c, -34, -22, 68, 12, INK, 1, r=3); rect(c, -34, 10, 68, 12, INK, 1, r=3); line(c, -22, 38, 22, -38, INK, 1, w=10); c.restore()

def g_save(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out_back(prog(t, 0.05, 0.45))
    c.save(); c.translate(W / 2, 430); c.scale(p, p)
    circle(c, 0, 0, 190, INK, 0.92); circle(c, 0, 0, 190, GRN, 1, stroke=10); icon(c, "disk", 0, 0, 220, GRN, 1); c.restore()
    q = ease_out(prog(t, 0.4, 0.8))
    draw_text(c, sh.get("txt", "GUARDA LA PARTIDA"), W / 2, 770, "anton", 110, WHITE, q, align="center", tracking=3)
    if sh.get("sub"): draw_text(c, sh["sub"], W / 2, 860, "intersb", 42, GRN, ease_out(prog(t, 0.8, 1.2)), align="center")

def g_record(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out_back(prog(t, 0.05, 0.4))
    c.save(); c.translate(W / 2, 420); c.scale(p, p)
    rect(c, -520, -150, 1040, 300, INK, 0.92, r=26); rect(c, -520, -150, 1040, 300, RED, 1, r=26, stroke=6)
    for k in range(6): star(c, -350 + k * 140, -60, 42, "white", 1)
    s = t * 1.0; draw_text(c, f"{int(s // 60):02d}:{int(s % 60):02d}.{int((s * 100) % 100):02d}", 0, 100, "monob", 110, WHITE, 1, align="center"); c.restore()
    q = ease_out(prog(t, 0.5, 0.9)); draw_text(c, "RETO: ¿CUÁNTO AGUANTAS VIVO?", W / 2, 760, "anton", 84, YEL, q, align="center", tracking=2)

TIERS = [("PROFESIONAL", "Professional", "#FFC72C"), ("CURTIDO", "Hardened", "#FF8A1F"), ("VIOLENTO", "Violent", "#A855F7"),
         ("PSICÓPATA", "Psycho", "#C9CDD4"), ("IRREDIMIBLE", "Irredeemable", "#4B5060")]
def horns(c, x, y, r, col, a=1.0, crack=0.0):
    """Icono del perfil (cara con cuernos, dibujo propio inspirado en el del juego)."""
    circle(c, x, y, r, col, a)
    for sg in (-1, 1):
        draw_poly(c, [(x + sg * r * 0.45, y - r * 0.75), (x + sg * r * 0.95, y - r * 1.35), (x + sg * r * 0.85, y - r * 0.55)], col, a)
    circle(c, x - r * 0.35, y - r * 0.1, r * 0.13, INK, a); circle(c, x + r * 0.35, y - r * 0.1, r * 0.13, INK, a)
    pth = skia.Path(); pth.moveTo(x - r * 0.4, y + r * 0.35); pth.quadTo(x, y + r * 0.6, x + r * 0.4, y + r * 0.35)
    c.drawPath(pth, paint(INK, a, stroke=r * 0.1))
    if crack > 0:
        pts = [(x - r * 0.1, y - r), (x + r * 0.1, y - r * 0.4), (x - r * 0.15, y), (x + r * 0.12, y + r * 0.5), (x - r * 0.05, y + r)]
        n = max(2, int(len(pts) * crack)); pth = skia.Path(); pth.moveTo(*pts[0])
        for q in pts[1:n]: pth.lineTo(*q)
        c.drawPath(pth, paint("#000000", a, stroke=r * 0.08))

def g_ladder(c, t, d, sh, ctx):
    """Escalera del perfil criminal. hi = índice resaltado; reveal = tiempos de aparición; extras por modo."""
    panel(c, t)
    mode = sh.get("mode", "all"); hi = sh.get("hi"); reveal = sh.get("reveal", [0.1 + 0.25 * k for k in range(5)])
    st = sh.get("st") or []
    if sh.get("reveal_cues") and len(st) >= 5: reveal = [max(0.0, x - 0.1) for x in st]
    crack_at = st[0] if sh.get("crack_cue") and st else sh.get("crack_at", 99)
    lock_at = st[0] if sh.get("lock_cue") and st else sh.get("lock")
    nos_at = st[0] if sh.get("nosurrender_cue") and st else sh.get("nosurrender")
    p = ease_out(prog(t, 0, 0.35)); title_top(c, sh.get("title", "PERFIL CRIMINAL"), p, sh.get("sub"))
    x0 = W / 2 - 820; y0 = 340; dy = 132
    for k, (es, en, col) in enumerate(TIERS):
        q = ease_out_back(prog(t, reveal[k], reveal[k] + 0.35))
        if q <= 0: continue
        y = y0 + k * dy; on = hi is None or k in (hi if isinstance(hi, (list, tuple)) else [hi])
        a = 1.0 if on else 0.35
        c.save(); c.translate(x0 + 40, y); c.scale(q, q); c.translate(-(x0 + 40), -y)
        rect(c, x0, y - 56, 1640 if mode != "duo" else 980, 112, INK, 0.9 * a, r=14)
        rect(c, x0, y - 56, 10, 112, col, a)
        horns(c, x0 + 80, y + 6, 36, col, a, crack=ease_out(prog(t, crack_at, crack_at + 0.8)) if k == 4 else 0)
        draw_text(c, es, x0 + 150, y + 26, "anton", 72, col if on else WHITE, a, tracking=2)
        draw_text(c, en, x0 + 150 + text_w(es, font("anton", 72), 2) + 30, y + 22, "ovmonomd", 26, GRAY, 0.9 * a)
        txt = (sh.get("notes") or {}).get(k)
        if txt and mode != "duo":
            e = ease_out(prog(t, (sh.get("note_at") or {}).get(k, reveal[k] + 0.3), (sh.get("note_at") or {}).get(k, reveal[k] + 0.3) + 0.35))
            draw_text(c, txt, x0 + 1610, y + 18, "intersb", 34, col, e * a, align="right")
        c.restore()
    if mode == "duo":   # una escalera para cada protagonista
        for j, nm in enumerate(["JASON", "LUCÍA"]):
            q = ease_out_back(prog(t, sh.get("duo_at", 1.5) + 0.25 * j, sh.get("duo_at", 1.5) + 0.25 * j + 0.4))
            if q <= 0: continue
            x = W / 2 + 330 + j * 300; c.save(); c.translate(x, 600); c.scale(q, q)
            rect(c, -130, -250, 260, 500, INK, 0.92, r=20); rect(c, -130, -250, 260, 500, YEL, 1, r=20, stroke=5)
            draw_text(c, nm, 0, -190, "anton", 58, YEL, 1, align="center", tracking=2)
            lv = 0 if j == 0 else 1
            for k in range(5): horns(c, 0, -110 + k * 80, 26, TIERS[k][2], 1.0 if k == lv else 0.25)
            c.restore()
    if lock_at is not None:
        e = ease_out_back(prog(t, lock_at, lock_at + 0.4))
        if e > 0:
            y = y0 + 4 * dy; c.save(); c.translate(x0 + 1540, y); c.scale(e, e)
            rect(c, -190, -50, 380, 100, RED, 1, r=50); icon(c, "lock", -130, 0, 56, WHITE, 1)
            draw_text(c, "PERMANENTE", 30, 18, "anton", 50, WHITE, 1, align="center", tracking=2); c.restore()
    if nos_at is not None:
        e = ease_out_back(prog(t, nos_at, nos_at + 0.4))
        if e > 0:
            y = y0 + 3 * dy; c.save(); c.translate(x0 + 1440, y); c.scale(e, e)
            rect(c, -300, -50, 600, 100, RED, 1, r=50); icon(c, "cross", -240, 0, 50, WHITE, 1)
            draw_text(c, "NO PUEDES RENDIRTE", 30, 18, "anton", 48, WHITE, 1, align="center", tracking=2); c.restore()

def g_bonus(c, t, d, sh, ctx):
    panel(c, t)
    title_top(c, "CÓMO SE RECARGA EL FOCUS", ease_out(prog(t, 0, 0.35)))
    cols = [((0, 1), "Dejar fuera de combate · buenos gestos", "PROFESIONAL Y CURTIDO"), ((2, 3), "Disparos a la cabeza", "VIOLENTO Y PSICÓPATA")]
    st = sh.get("st", [0.3, 2.2])
    for j, (ks, txt, head) in enumerate(cols):
        p = ease_out_back(prog(t, st[j], st[j] + 0.4))
        if p <= 0: continue
        x = W / 2 + (-430 if j == 0 else 430); c.save(); c.translate(x, 560); c.scale(p, p)
        rect(c, -390, -230, 780, 460, INK, 0.92, r=24)
        for m, k in enumerate(ks): horns(c, -70 + m * 140, -120, 52, TIERS[k][2], 1)
        draw_text(c, head, 0, 20, "anton", 54, YEL, 1, align="center", tracking=2)
        draw_text(c, txt, 0, 110, "intersb", 38, WHITE, 1, align="center")
        c.restore()

def g_quote(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out(prog(t, 0.05, 0.45))
    c.save(); c.translate(0, (1 - p) * 40)
    rect(c, 180, 300, W - 360, 420, INK, 0.9 * p, r=20); rect(c, 180, 300, 12, 420, YEL, p)
    draw_text(c, "«", 250, 480, "dmserif", 220, YEL, p)
    for j, ln in enumerate(wrap(sh["q"], "dmserif", 76, W - 700)): draw_text(c, ln, 380, 440 + j * 92, "dmserif", 76, WHITE, p)
    draw_text(c, sh.get("who", "Rockstar Games"), 380, 680, "ovmonomd", 28, YEL, p, tracking=1)
    c.restore()
    if sh.get("sub"):
        q = ease_out(prog(t, sh.get("sub_at", 1.5), sh.get("sub_at", 1.5) + 0.4)); draw_text(c, sh["sub"], W / 2, 860, "intersb", 40, GRAY, q, align="center")

def g_stats(c, t, d, sh, ctx):
    panel(c, t)
    step = sh.get("step", 0)
    p = ease_out(prog(t, 0, 0.35)); title_top(c, "FINAL DE LA HISTORIA EN «PROFESIONAL»", p, "Estadísticas de un redactor de PC Gamer (18/11/2026)")
    st = sh.get("st") or [0.3, 1.4]
    boxes = [("ENEMIGOS MUERTOS", 321, RED, st[0]), ("FUERA DE COMBATE", 461, GRN, st[1])]
    if step >= 1: boxes = [("ANIMALES MUERTOS", 98, ORA, 0.2)]
    for j, (lab, val, col, at) in enumerate(boxes):
        q = ease_out_back(prog(t, at, at + 0.4))
        if q <= 0: continue
        x = W / 2 + ((-420 if j == 0 else 420) if len(boxes) == 2 else 0); c.save(); c.translate(x, 580); c.scale(q, q)
        rect(c, -380, -220, 760, 440, INK, 0.92, r=26); rect(c, -380, -220, 760, 440, col, 1, r=26, stroke=7)
        n = int(round(count_up(val, prog(t, at, at + 1.2))))
        draw_text(c, str(n), 0, 70, "anton", 240, col, 1, align="center")
        draw_text(c, lab, 0, 160, "anton", 54, WHITE, 1, align="center", tracking=2); c.restore()
    if step >= 1:
        q = ease_out(prog(t, 1.4, 1.8)); draw_text(c, "«Casi todos pájaros: no se apartan de ningún vehículo»", W / 2, 885, "dmserifi", 50, WHITE, q, align="center")

def g_recap(c, t, d, sh, ctx):
    panel(c, t)
    title_top(c, "RESUMEN", ease_out(prog(t, 0, 0.3)))
    rows = ["Sin testigos, no hay estrellas", "Si te identifican: cambia de ropa y deja el auto", "Escapar de la persecución no es perder la búsqueda",
            "La sexta estrella solo se apaga muriendo", "Quien te juzga es tu perfil criminal"]
    st = sh.get("st", [0.2 + 0.9 * k for k in range(5)])
    for j, txt in enumerate(rows):
        p = ease_out_back(prog(t, st[j], st[j] + 0.35))
        if p <= 0: continue
        y = 330 + j * 130; c.save(); c.translate(W / 2 - 700, y); c.scale(p, p); c.translate(-(W / 2 - 700), -y)
        rect(c, W / 2 - 760, y - 50, 1520, 100, INK, 0.9, r=14); circle(c, W / 2 - 690, y, 30, GRN, 1); icon(c, "check", W / 2 - 690, y, 36, INK, 1)
        draw_text(c, txt, W / 2 - 630, y + 18, "anton", 56, WHITE, 1, tracking=1); c.restore()

def g_poll(c, t, d, sh, ctx):
    panel(c, t)
    title_top(c, "CUÉNTANOSLO EN LOS COMENTARIOS", ease_out(prog(t, 0, 0.3)))
    qs = [("¿Profesional o casi Irredimible?", sh.get("st", [0.3, 1.6])[0]), ("¿Cuánto aguantaste con 6 estrellas?", sh.get("st", [0.3, 1.6])[1])]
    for j, (txt, at) in enumerate(qs):
        p = ease_out_back(prog(t, at, at + 0.4))
        if p <= 0: continue
        y = 470 + j * 220; c.save(); c.translate(W / 2, y); c.scale(p, p)
        rect(c, -780, -80, 1560, 160, INK, 0.92, r=80); rect(c, -780, -80, 1560, 160, YEL, 1, r=80, stroke=6)
        icon(c, "chat", -680, 0, 80, YEL, 1); draw_text(c, txt, 40, 26, "anton", 72, WHITE, 1, align="center", tracking=1); c.restore()

def g_subscribe(c, t, d, sh, ctx):
    panel(c, t)
    p = ease_out_back(prog(t, 0.05, 0.45))
    c.save(); c.translate(W / 2, 470); c.scale(p, p); draw_badge(c, 0, 0, 200, t=t); c.restore()
    wordmark(c, W / 2, 790, 90, a=ease_out(prog(t, 0.3, 0.7)), align="center")
    q = ease_out_back(prog(t, 0.6, 1.0))
    c.save(); c.translate(W / 2, 900); c.scale(q, q); rect(c, -260, -55, 520, 110, "#E62117", 1, r=16)
    draw_text(c, "SUSCRÍBETE", 0, 22, "anton", 64, WHITE, 1, align="center", tracking=3); c.restore()

def g_end(c, t, d, sh, ctx):
    class I: pass
    K.end_screen(c, t, I(), ctx, title="SIGUIENTE SALIDA", sub="Más descubrimientos de GTA 6, sin spoilers")

def g_msgcard(c, t, d, sh, ctx):
    """El mensaje del juego tal como aparece (en inglés), ampliado; la traducción la dicen la voz y los subtítulos."""
    panel(c, t)
    p = ease_out_back(prog(t, 0.0, 0.4))
    G.chip(c, W / 2 - 330, 230, "MENSAJE DEL JUEGO · TEXTO ORIGINAL EN INGLÉS", ease_out(prog(t, 0.1, 0.4)), 26, CYA)
    lines = wrap(sh["en"], "intersb", 62, 1300)
    h = 80 + 82 * len(lines); x = W / 2 - 720; y = H / 2 - h / 2 + 30
    c.save(); c.translate(W / 2, y + h / 2); c.scale(0.85 + 0.15 * p, 0.85 + 0.15 * p); c.translate(-W / 2, -(y + h / 2))
    rect(c, x + 12, y + 16, 1440, h, "#000000", 0.5 * clamp(p), r=18, blur=16)
    rect(c, x, y, 1440, h, "#1C1F2A", 0.94 * clamp(p), r=18)
    for j, ln in enumerate(lines):
        draw_text(c, ln, x + 70, y + 92 + j * 82, "intersb", 62, WHITE, clamp(p * 1.4))
    c.restore()

GFX = {k[2:]: v for k, v in list(globals().items()) if k.startswith("g_")}

# ================================================================ miniatura (1280×720)
def thumbnail(c):
    """Miniatura 1280×720: fotograma real (Lucía frente a un vehículo en llamas en la playa, partida de IGN) y el mensaje real del juego."""
    Wt, Ht = 1280, 720
    p = os.path.join(os.path.dirname(ICON_DIR), "miniatura_fondo.png")
    if os.path.exists(p):
        img = G.load_img(p, maxw=2600); iw, ih = img.width(), img.height(); s = Ht / ih * 1.2   # sin el minimapa (abajo a la izquierda)
        c.drawImageRect(img, skia.Rect.MakeXYWH(-60, -62, iw * s, ih * s), SO_HQ)
    else: rect(c, 0, 0, Wt, Ht, "#101218", 1)
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(Wt, 0), (Wt - 820, 0)], [skia.Color(8, 8, 14, 235), skia.Color(8, 8, 14, 175), skia.Color(8, 8, 14, 0)], [0, 0.6, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(Wt - 860, 0, 860, Ht), g)
    for k in range(6): star(c, Wt - 70 - k * 92, 92, 38, "white", 1)
    draw_text(c, "6 ESTRELLAS", Wt - 40, 270, "anton", 150, WHITE, 1, align="right", tracking=2)
    draw_text(c, "ESCAPAR ES", Wt - 44, 390, "anton", 108, YEL, 1, align="right", tracking=2)
    draw_text(c, "IMPOSIBLE", Wt - 44, 500, "anton", 108, YEL, 1, align="right", tracking=2)
    rect(c, Wt - 518, 548, 470, 84, "#E23B3B", 1, r=42); draw_text(c, "Y NO SE BORRA", Wt - 283, 606, "ovblk", 44, WHITE, 1, align="center", tracking=2)
    draw_text(c, "GTA 6 · GAMEPLAY REAL", Wt - 48, 682, "ovmono", 28, WHITE, 0.92, align="right", tracking=2)
