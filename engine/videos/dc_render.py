"""Montaje de los vídeos largos 2 y 3 tras el lanzamiento (16:9, 1920×1080, 30 fps): «Planeta Vice City» y «GTA 6 a juicio».

Mismo método que gx_render.py (vídeo 1):
- Cada plano empieza en la palabra exacta del guion que lo motiva (2 fotogramas antes).
- Gameplay desde tramos «mezzanine» (mezzanine.py) a 1080p y 30 fps constantes, solo imágenes únicas; cada fotograma del
  vídeo avanza exactamente un fotograma del original (sin repetir, sin saltar, sin bucles). validate() lo comprueba.
- La correspondencia de tiempos depende de la fuente: 1,001 s del original por segundo del tramo si va a 29,97/59,94 fps,
  1 s si va a 30/60 fps exactos (mezzanine.rate).
Cambian el estilo (tema por vídeo: V["theme"]) y los gráficos propios (g:).
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
INK = "#0B0C10"; WHITE = "#FFFFFF"; GRAY = "#A3A8B3"
RED, BLUE, GRN, YEL = "#E5484D", "#4C8DF6", "#3DD68C", "#FFC72C"
SO = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
SO_HQ = skia.SamplingOptions(skia.CubicResampler.Mitchell())

THEMES = {
    # documental de naturaleza: verde selva y ámbar de atardecer
    "planeta": dict(acc="#9BE38D", acc2="#F2C94C", bg="#07110C", glow1="#2FBF71", glow2="#F2C94C", chap="CAPÍTULO"),
    # sala de juicio: dorado y madera; rojo acusación, azul defensa
    "juicio": dict(acc="#E8C468", acc2="#F5E6B8", bg="#0E0B08", glow1="#E5484D", glow2="#4C8DF6", chap="SESIÓN"),
    # combate por asaltos: oro de cinturón de campeón; verde GTA V, rosa GTA VI
    "terror": dict(acc="#FF3B3B", acc2="#FFFFFF", bg="#07050A", glow1="#8B0000", glow2="#5B1A8B", chap="SECRETO"),
    "arcade": dict(acc="#36E3FF", acc2="#FFFFFF", bg="#07060F", glow1="#FF2BD6", glow2="#36E3FF", chap="NIVEL"),
    "tv": dict(acc="#FFD23F", acc2="#FFFFFF", bg="#0A0A0C", glow1="#FF4D4D", glow2="#3DDC97", chap="CANAL"),
    "playa": dict(acc="#FFB347", acc2="#FFFFFF", bg="#061218", glow1="#2EC4B6", glow2="#FF6B6B", chap="PARADA"),
    "combate": dict(acc="#F5C542", acc2="#FFFFFF", bg="#0B0B10", glow1="#5BC26A", glow2="#F25C9B", chap="ASALTO"),
    "retro": dict(acc="#FFD23F", acc2="#FFFFFF", bg="#0B0710", glow1="#E52521", glow2="#43B047", chap="NIVEL"),
    "fantasma": dict(acc="#7CFFB2", acc2="#E6FFF3", bg="#030C0A", glow1="#0F5E46", glow2="#1E3A5F", chap="PISTA"),
    "neon": dict(acc="#FF4FD8", acc2="#FFFFFF", bg="#0A0614", glow1="#22D3EE", glow2="#FF4FD8", chap="PASO"),
    "tormenta": dict(acc="#FF9F1C", acc2="#FFFFFF", bg="#070B12", glow1="#3A6EA5", glow2="#9FB8D0", chap="ALERTA"),
    "racing": dict(acc="#39FF14", acc2="#FFFFFF", bg="#05090A", glow1="#2F80FF", glow2="#39FF14", chap="VUELTA"),
    "finales": dict(acc="#FF5A5F", acc2="#FFFFFF", bg="#0A0708", glow1="#7A1020", glow2="#2B3A67", chap="PARTE"),
    "policia": dict(acc="#4DA3FF", acc2="#FFFFFF", bg="#05080F", glow1="#E5484D", glow2="#2F6BFF", chap="NIVEL"),
}
G5, G6 = "#5BC26A", "#F25C9B"
LADO_COL = {"acusacion": "#E5484D", "defensa": "#4C8DF6", "gta5": G5, "gta6": G6}
LADO_TXT = {"acusacion": "ACUSACIÓN", "defensa": "DEFENSA", "gta5": "LOS SANTOS · 2013", "gta6": "VICE CITY · 2026"}
def th(ctx): return THEMES[ctx.V.get("theme", "planeta")]

# fuentes (copias públicas en Internet Archive; créditos en pantalla y en la descripción)
AUTHOR = {"IG2hfrBVjh4": "Kotaku", "Q5XgKNEnbP4": "The Escapist", "V99Ng_VTBUs": "LOCAL GAMING", "nqmpDCbz3lA": "Sirloin",
          "cEDUO1zjB5c": "toaster", "-UuHA1h-Cf8": "GameV", "3UiRmXUIE9k": "IGN", "xnNu7YybiCM": "IGN", "jZka1Ay1-gI": "IGN",
          "4HCd052lpnA": "IGN", "gN5qaT7u-uM": "IGN", "R9r9ew12GcA": "IGN", "vpHospital1": "Video Pump", "gvlY1gVmSKM": "Yamatum O", "NwQKirh2dxE": "LazarBeam"}
EDITED = set(AUTHOR)          # todas son vídeos montados: un plano no puede cruzar un corte (detección de escena + cortes a mano)
MANUAL_CUTS = {"3UiRmXUIE9k": [33.0, 36.0],      # icono de IGN sobre la imagen
               "xnNu7YybiCM": []}
# tramos que nunca se usan como gameplay (en segundos del original): carteles negros con texto de la guía de The Escapist
# Rótulos del montaje original en la franja de arriba (filas 20-91 de 1080) que no se pueden evitar sin cambiar los planos:
# en los planos que los pisan se amplía la imagen un 9-12 % anclada abajo, de modo que la franja queda fuera del encuadre.
# B0b5JhrGUJQ (recopilación de los finales): título blanco de cada final arriba a la izquierda (detectado fotograma a fotograma)
TOPMASK = {"B0b5JhrGUJQ": [(113.0, 116.0), (144.4, 147.4), (170.6, 173.6), (230.4, 233.4), (309.0, 312.0), (359.4, 362.4),
                           (405.4, 408.4), (529.6, 532.6), (678.4, 681.4), (724.0, 727.0)]}
EXCLUDE = {"Q5XgKNEnbP4": [(53.4, 55.9), (62.0, 64.9), (70.6, 73.3), (78.2, 82.2), (90.7, 93.9), (102.8, 106.0), (116.4, 121.7), (132.1, 134.8)]}

# ================================================================ material
def parse_x(src):
    vid, t = src[2:].split("@"); return vid, float(t)

_CUTS = {}
def mez_cuts(path, vid, a0):
    if path in _CUTS: return _CUTS[path]
    manual = [(T - a0) / MZ.rate(vid) for T in MANUAL_CUTS.get(vid, [])]
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
    vid, T = parse_x(sh["src"]); rt = MZ.rate(vid)
    # si dos ventanas solapadas contienen T, la que más material deja por delante
    for a, b in sorted(MZ.windows_for(vid), key=lambda w: -(w[1] - T) if w[0] <= T < w[1] else 1e9):
        if a <= T < b:
            path = MZ.name(vid, a, b); loc = (T - a) / rt; avail = (b - T) / rt - 0.12
            if not os.path.exists(path): continue   # ventana de otro vídeo que ya no está extraída
            if True:
                avail = min(avail, file_dur(path) - loc - 0.12)
                cs = mez_cuts(path, vid, a) if (vid in EDITED and not sh.get("nocut")) else []
                nxt = next((x for x in cs if x > loc + 0.05), None)
                if nxt is not None: avail = min(avail, nxt - loc - 0.05)
            sh["_xw"] = (path, loc, avail, vid in MZ.VERTICAL); return sh["_xw"]
    raise ValueError(f"no hay tramo extraído para {sh['src']}")

class Clip(G.Clip):
    def _open(self):
        w, h = self.size
        self.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "fatal", "-ss", f"{self.t0:.3f}", "-i", self.path, "-t", f"{self.dur:.3f}", "-an",
                                   "-vf", f"scale={w}:{h},format=rgba", "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                                  stdout=subprocess.PIPE, bufsize=w * h * 4 * 2)
        self.i = -1; self.eof = False

_CL = {}
def x_frame(sh, tau, slot):
    path, loc, avail, vert = x_window(sh)
    k = int(math.floor(tau * FPS + 1e-6)); kmax = max(0, int(avail * FPS) - 1)
    if k > kmax: sh["_over"] = max(sh.get("_over", 0), k - kmax); k = kmax
    cl = _CL.get(slot); size = (1080, 1920) if vert else (W, H)
    if cl is None or cl.path != path or abs(cl.t0 - loc) > 1e-3:
        if cl: cl.close()
        cl = Clip(path, loc, avail + 0.3, size); _CL[slot] = cl
    return cl.get(k), vert

def draw_img(c, img, z=1.0, cx=0.5, cy=0.5, k=0.0, a=1.0):
    iw, ih = img.width(), img.height(); s = max(W / iw, H / ih) * z; dw, dh = iw * s, ih * s
    tx = lerp(W * cx, W / 2, k); ty = lerp(H * cy, H / 2, k)
    x = tx - dw * cx; y = ty - dh * cy
    x = min(0, max(W - dw, x)); y = min(0, max(H - dh, y))
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, dw, dh), SO_HQ if z > 1.25 else SO, p)
    return x, y, s

def footage(c, sh, tau, d, ctx, slot="main"):
    img, vert = x_frame(sh, tau, slot)
    if img is None: return
    T = th(ctx)
    if vert or sh.get("card"):
        # tarjeta: el vídeo (vertical, o una imagen de baja resolución) nítido sobre su propia imagen desenfocada
        bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(36, 36))
        if vert: c.drawImageRect(img, skia.Rect.MakeXYWH(-100, -H * 0.9, W + 200, (W + 200) * 1920 / 1080), SO, bg)
        else: c.drawImageRect(img, skia.Rect.MakeXYWH(-80, -60, W + 160, H + 120), SO, bg)
        rect(c, 0, 0, W, H, "#05060A", 0.6)
        g = 1 + 0.03 * clamp(tau / max(d, 0.1))
        if vert: vh = 960 * g; vw = vh * 1080 / 1920
        else: vw = 1240 * g; vh = vw * 9 / 16
        side = sh.get("side", "right" if vert else "center")
        x = W - vw - 150 if side == "right" else ((W - vw) / 2 if side == "center" else 150); y = (H - vh) / 2 + (20 if not vert else 0)
        rect(c, x + 14, y + 18, vw, vh, "#000000", 0.5, r=26, blur=18)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, vw, vh), 22, 22), True)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, vw, vh), SO_HQ); c.restore()
        rect(c, x, y, vw, vh, T["acc"], 0.9, r=22, stroke=5)
        if sh.get("card_zoom"):   # recuadro ampliado de una zona de la imagen (u0, v0, u1, v1) junto a la tarjeta
            u0, v0, u1, v1 = sh["card_zoom"]; p = ease_out_back(prog(tau, sh.get("zoom_at", 1.0), sh.get("zoom_at", 1.0) + 0.4))
            if p > 0:
                iw, ih = img.width(), img.height(); zw = 560; zh = zw * (v1 - v0) * ih / ((u1 - u0) * iw)
                zx, zy = (70 if (u0 + u1) / 2 > 0.5 else W - zw - 70), 120   # en el lado contrario a la zona ampliada, para que se vean las dos
                c.save(); c.translate(zx + zw / 2, zy + zh / 2); c.scale(p, p); c.translate(-(zx + zw / 2), -(zy + zh / 2))
                rect(c, zx + 8, zy + 10, zw, zh, "#000000", 0.6, r=14, blur=12)
                c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(zx, zy, zw, zh), 14, 14), True)
                c.drawImageRect(img, skia.Rect.MakeLTRB(u0 * iw, v0 * ih, u1 * iw, v1 * ih), skia.Rect.MakeXYWH(zx, zy, zw, zh), SO_HQ); c.restore()
                rect(c, zx, zy, zw, zh, YEL, 1, r=14, stroke=6); c.restore()
                rect(c, x + u0 * vw - 6, y + v0 * vh - 6, (u1 - u0) * vw + 12, (v1 - v0) * vh + 12, YEL, clamp(p), r=8, stroke=5)
        if sh.get("vtitle"):
            p = ease_out(prog(tau, 0.1, 0.5)); draw_par(c, sh["vtitle"], 140, 420, "anton", 92, 820, lh=1.05, color=WHITE, a=p, tracking=1)
        return
    zm = sh.get("zoom")
    if zm:
        cx, cy, z1, tz = zm; t0z = sh.get("zoom_at", 0.0)
        e = ease_io(prog(tau, t0z, t0z + tz)); z = lerp(sh.get("z0", 1.0), z1, e)
        draw_img(c, img, z, cx, cy, e)
    else:
        z0, z1 = sh.get("z", (1.0, 1.05)); fx, fy = sh.get("f", (0.5, 0.5))
        draw_img(c, img, lerp(z0, z1, clamp(tau / max(d, 0.1))), fx, fy, 0.0)

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
            if sh.get("cues"):
                st = []; aft = after - 0.02
                for frag in sh["cues"]:
                    ct, _ = G._word_time(bd["sents"], frag, aft)
                    if ct is None: raise ValueError(f"cue «{frag}» no encontrada en el beat {bi} ({b.get('id')})")
                    st.append(round(ct - t0, 3)); aft = ct + 0.01
                ns["st"] = st
            shots.append(ns); last = after
    shots.sort(key=lambda s: s["t0"])
    # el primer plano empieza en el fotograma 0 (sin negro al principio); si es gameplay, su material se adelanta lo mismo
    if shots and shots[0]["t0"] > 0:
        s0 = shots[0]; pre = s0["t0"]; s0["t0"] = 0.0
        if s0.get("st"): s0["st"] = [round(x + pre, 3) for x in s0["st"]]
        if s0["src"].startswith("x:"):
            vid0, T0 = parse_x(s0["src"]); s0["src"] = f"x:{vid0}@{T0 - pre * MZ.rate(vid0):.3f}"
    lastx = {}
    for s in shots:
        if not s["src"].startswith("x:"): continue
        vid, T = parse_x(s["src"])
        if s.get("cont"):
            if vid not in lastx: raise ValueError(f"cont sin plano anterior de {vid}")
            pT, pt0 = lastx[vid]; T = pT + (s["t0"] - pt0) * MZ.rate(vid); s["src"] = f"x:{vid}@{T:.3f}"
        lastx[vid] = (T, s["t0"])
    for i, s in enumerate(shots): s["t1"] = shots[i + 1]["t0"] if i + 1 < len(shots) else tl["total"]
    shots = fit(shots, tl["total"])
    for s_ in shots:
        if not s_["src"].startswith("x:") or s_.get("zoom"): continue
        vid_, T_ = parse_x(s_["src"]); T1_ = T_ + (s_["t1"] - s_["t0"] + 0.2) * MZ.rate(vid_)
        if any(T_ < b_ + 0.3 and T1_ > a_ - 0.3 for a_, b_ in TOPMASK.get(vid_, [])): s_["z"] = (1.09, 1.12); s_["f"] = (0.5, 1.0); s_["topmask"] = True
    _T.update(shots=shots, starts=[s["t0"] for s in shots], beats=beats, chapters=chapters, bstarts=[x["bd"]["start"] for x in beats])
    return _T

# ================================================================ ajuste automático de los planos de gameplay
# Los vídeos de origen están montados (cortes) y la narración marca cuánto dura cada plano. Si un plano no cabe en el
# material continuo que hay desde su segundo de origen, o pisa material que ya salió antes, se ajusta así:
#  1) se mantiene el momento anclado mientras haya material continuo y sin usar (si hay al menos FIT_MIN s);
#  2) el resto continúa en el tramo libre y sin cortes más cercano de la MISMA fuente (primero hacia delante, que suele
#     ser la misma escena o la siguiente de la guía), sin repetir nunca material.
# Los rótulos del plano (etiqueta de prueba, frase original, texto grande, ampliación) solo van en el primer trozo.
FIT_MIN = 1.2
FIT_LOG = []

_DUR = {}
def file_dur(path):
    """Duración real del archivo del tramo (por si quedó más corto que la ventana)."""
    if path not in _DUR:
        _DUR[path] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))
    return _DUR[path]

def _segments(vid):
    """Tramos sin cortes de las ventanas extraídas de una fuente, en segundos del original: [(Ta, Tb)]."""
    out = []; rt = MZ.rate(vid)
    for a, b in MZ.windows_for(vid):
        p = MZ.name(vid, a, b)
        if not os.path.exists(p): continue
        cs = sorted(mez_cuts(p, vid, a)) if vid in EDITED else []
        end = min((b - a) / rt, file_dur(p)) - 0.12; edges = [0.0] + [c for c in cs if 0.0 < c < end] + [end]
        for x0, x1 in zip(edges, edges[1:]):
            s0 = x0 + (0.10 if x0 > 0 else 0.0); s1 = x1 - 0.06
            if s1 - s0 > 0.35: out.append((a + s0 * rt, a + s1 * rt))
    for e0, e1 in EXCLUDE.get(vid, []):
        out = [p for a_, b_ in out for p in ((a_, min(b_, e0)), (max(a_, e1), b_)) if p[1] - p[0] > 0.35]
    return out

def _free(segs, used):
    """Partes de los tramos que no se han usado todavía (margen de 0,06 s)."""
    out = []
    for a, b in segs:
        pieces = [(a, b)]
        for u0, u1 in used:
            nxt = []
            for x0, x1 in pieces:
                if u1 + 0.06 <= x0 or u0 - 0.06 >= x1: nxt.append((x0, x1)); continue
                if u0 - 0.06 > x0: nxt.append((x0, u0 - 0.06))
                if u1 + 0.06 < x1: nxt.append((u1 + 0.06, x1))
            pieces = nxt
        out += [(x0, x1) for x0, x1 in pieces if x1 - x0 > 0.35]
    return sorted(out)

def _place(free, T0, needT, minT):
    """Mejor inicio para needT segundos de material: (inicio, longitud disponible) o None.
    Coste: distancia al segundo pedido (hacia atrás pesa más) + lo que falte para cubrirlo todo."""
    best = None
    for a, b in free:
        if a <= T0 < b and b - T0 >= minT: st = T0; cost = 0.0
        elif a >= T0: st = a; cost = a - T0
        else: st = max(a, b - needT); cost = 2.5 * (T0 - st) + 6.0   # volver atrás se nota: solo si no hay nada cerca hacia delante
        ln = b - st
        if ln < minT: continue
        if ln < needT: cost += 0.5 * (needT - ln)
        if best is None or cost < best[2]: best = (st, ln, cost)
    return best and best[:2]

def _trd(shots, i):
    nx = shots[i + 1] if i + 1 < len(shots) else None
    return (nx.get("tr") or (0, 0.13 if nx["src"].startswith("g:") else 0.0))[1] if nx else 0.0

def fit(shots, total):
    FIT_LOG.clear(); used = {}; out = []; segs = {}; reserved = {}
    # pase 1: los planos anclados a una palabra (o con la frase original en pantalla) se quedan con su momento exacto;
    # el resto de planos (comienzos de bloque y continuaciones) se ajusta después alrededor de esos momentos
    prio = [i for i, s in enumerate(shots) if s["src"].startswith("x:") and not s.get("cont") and not s.get("nofit")
            and (s.get("anchor") is not None or s.get("say"))]
    starts = {}
    for i in prio: vid, T0 = parse_x(shots[i]["src"]); starts.setdefault(vid, []).append(T0)
    for i in prio:
        s = shots[i]; vid, T0 = parse_x(s["src"]); rt = MZ.rate(vid)
        if vid not in segs: segs[vid] = _segments(vid)
        # un ancla que cae justo antes de un corte (≤ 0,25 s) empieza en el primer fotograma del plano siguiente
        here = next(((a, b) for a, b in _free(segs[vid], used.get(vid, [])) if a - 0.25 <= T0 < b and b - max(a, T0) >= FIT_MIN * rt), None)
        if not here: continue
        T0 = max(here[0], T0); s["src"] = f"x:{vid}@{T0:.3f}"
        # la reserva no invade el momento anclado de otro plano de la misma fuente
        cap = min([x for x in starts[vid] if x > T0 + 0.01] + [here[1]]) - 0.06
        take = min((s["t1"] - s["t0"]) + _trd(shots, i) + 0.05, (cap - T0) / rt)
        if take * rt < FIT_MIN * rt * 0.5: continue
        reserved[i] = (vid, (T0, T0 + take * rt)); used.setdefault(vid, []).append(reserved[i][1])
    for i, s in enumerate(shots):
        if i in reserved: used[reserved[i][0]].remove(reserved[i][1])   # su propio momento vuelve a quedar libre para él
        if not s["src"].startswith("x:") or s.get("cont") or s.get("nofit"):
            out.append(s)
            if s["src"].startswith("x:"):
                vid, T = parse_x(s["src"]); used.setdefault(vid, []).append((T, T + (s["t1"] - s["t0"]) * MZ.rate(vid)))
            continue
        vid, T0 = parse_x(s["src"]); rt = MZ.rate(vid)
        if vid not in segs: segs[vid] = _segments(vid)
        trd = _trd(shots, i)
        t, left = s["t0"], (s["t1"] - s["t0"]) + trd + 0.05; first = True; T = T0; pieces = []
        while left > 0.02:
            fr = _free(segs[vid], used.get(vid, [])); minT = min(FIT_MIN, left) * rt
            here = next(((a, b) for a, b in fr if a <= T < b and b - T >= minT), None)
            # trozo siguiente justo a continuación del anterior (ventanas solapadas): mismo fotograma, sin saltos
            nxt = None if first else next(((a, b) for a, b in fr if a - 0.08 <= T < a + 1e-6 and b - T >= minT), None)
            pl = (T, here[1] - T) if (first and here) else ((T, nxt[1] - T) if nxt else _place(fr, T, left * rt, minT))
            if pl is None: raise ValueError(f"no queda material libre de {vid} para el plano de {s['t0']:.2f} s («{s.get('anchor')}»)")
            st, ln = pl; take = min(left, ln / rt); rem = left - take
            if 0 < rem < FIT_MIN and take - (FIT_MIN - rem) >= FIT_MIN: take -= FIT_MIN - rem   # que el último trozo no sea un destello
            d = take - (0.05 + trd if take >= left - 1e-6 else 0.05)
            ns = {k: v for k, v in s.items() if k != "_xw"}
            if not first:
                for k in ("prueba", "lado", "say", "big", "card_zoom", "zoom_at", "cues", "st", "top"): ns.pop(k, None)
                ns["fit"] = True
            ns["src"] = f"x:{vid}@{st:.3f}"; ns["t0"] = t
            pieces.append(ns); used.setdefault(vid, []).append((st, st + take * rt))
            t += d; left -= d if take < left else left; T = st + take * rt; first = False
        if len(pieces) > 1 or abs(parse_x(pieces[0]["src"])[1] - T0) > 0.01:
            FIT_LOG.append((s["t0"], s.get("anchor"), vid, T0, [(round(p["t0"], 2), round(parse_x(p["src"])[1], 2)) for p in pieces]))
        out += pieces
    for i, s in enumerate(out): s["t1"] = out[i + 1]["t0"] if i + 1 < len(out) else total
    # un trozo de relleno de menos de 0,1 s sería un destello de 1-3 fotogramas de otro momento: lo absorbe el plano anterior
    out = [s for i, s in enumerate(out) if not (i and s.get("fit") and s["t1"] - s["t0"] < 0.1 and out[i - 1]["src"].startswith("x:"))]
    for i, s in enumerate(out): s["t1"] = out[i + 1]["t0"] if i + 1 < len(out) else total
    return out

def validate(ctx, verbose=True):
    """Cada plano de gameplay debe tener material continuo para toda su duración (más su transición hacia el siguiente)."""
    T = table(ctx); bad = []; used = {}
    for i, s in enumerate(T["shots"]):
        if not s["src"].startswith("x:"): continue
        nx = T["shots"][i + 1] if i + 1 < len(T["shots"]) else None
        trd = (nx.get("tr") or (0, 0.13 if nx["src"].startswith("g:") else 0.0))[1] if nx else 0.0
        d = s["t1"] - s["t0"] + trd + 0.05
        path, loc, avail, vert = x_window(s)
        if not os.path.exists(path): bad.append((s, "falta el tramo", 0)); continue
        if d > avail: bad.append((s, f"dura {d:.2f} s y solo hay {avail:.2f} s continuos", d - avail))
        vid, T0 = parse_x(s["src"]); seg = (T0, T0 + (s["t1"] - s["t0"]) * MZ.rate(vid))
        for o in used.get(vid, []):   # el mismo material no se repite en dos planos
            if seg[0] < o[1] - 0.05 and o[0] < seg[1] - 0.05 and not s.get("cont"):
                bad.append((s, f"repite material de {vid} ({o[0]:.1f}-{o[1]:.1f})", 0))
        used.setdefault(vid, []).append(seg)
    if verbose:
        for s, why, _ in bad: print(f"  [plano] {s['t0']:7.2f} s · {s['src']} · {why} · ancla «{s['anchor']}»")
        print(f"  validación de planos: {len(T['shots'])} planos · {len(bad)} con problemas")
    return bad

# ================================================================ escena única
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
    elif kind == "zoom":
        c.save(); s = 1 + 0.3 * e; c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
        pa = skia.Paint(); pa.setAlphaf(1 - e); c.drawImage(A, 0, 0, SO, pa); c.restore()
        c.save(); s = 0.88 + 0.12 * e; c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2, -H / 2)
        pb = skia.Paint(); pb.setAlphaf(e); c.drawImage(B, 0, 0, SO, pb); c.restore()
    elif kind == "dip":
        c.drawImage(A if p < 0.5 else B, 0, 0); rect(c, 0, 0, W, H, "#000000", math.sin(p * math.pi))
    else:
        c.drawImage(A, 0, 0); pp = skia.Paint(); pp.setAlphaf(e); c.drawImage(B, 0, 0, SO, pp)

def draw_shot(c, sh, tau, d, ctx, slot="main"):
    k, v = sh["src"].split(":", 1)
    if k == "g": GFX[v.split("@")[0]](c, tau, d, sh, ctx)
    else: footage(c, sh, tau, d, ctx, slot)
    if sh.get("dim"): rect(c, 0, 0, W, H, "#05060A", sh["dim"])
    if sh.get("big"): big_text(c, sh["big"], tau, d, sh.get("big_col", th(ctx)["acc"]))
    if sh.get("prueba"): exhibit_tag(c, sh["prueba"], sh.get("lado", "acusacion"), tau, d, ctx)
    if sh.get("say"): say_chip(c, sh["say"], tau, d, ctx)
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

def exhibit_tag(c, txt, lado, tau, d, ctx):
    """Etiqueta de prueba (juicio): «PRUEBA A» en rojo (acusación) o azul (defensa), arriba a la izquierda."""
    col = LADO_COL.get(lado, "#B8860B")
    p = ease_out_back(prog(tau, 0.1, 0.45)) * (1 - prog(tau, d - 0.15, d))
    if p <= 0: return
    side = LADO_TXT.get(lado, "DECLARA")
    f = font("anton", 64); w = max(330, text_w(txt, f, 2) + 80)
    c.save(); c.translate(70 + w / 2, 230); c.rotate(-4 * (1 - p)); c.scale(p, p)
    rect(c, -w / 2, -66, w, 132, "#F4EBD0", 0.97, r=10); rect(c, -w / 2, -66, w, 132, col, 1, r=10, stroke=6)
    draw_text(c, txt, 0, 14, "anton", 64, col, 1, align="center", tracking=2)
    draw_text(c, side, 0, 50, "ovmonomd", 22, INK, 0.9, align="center", tracking=3)
    c.restore()

def say_chip(c, txt, tau, d, ctx):
    """Lo que dice un personaje del juego (texto original en inglés); la traducción la dicen la voz y los subtítulos."""
    p = ease_out(prog(tau, 0.15, 0.45)) * (1 - prog(tau, d - 0.15, d))
    if p <= 0: return
    f = font("dmserifi", 44); w = min(1500, text_w(f"«{txt}»", f) + 90)
    x = W / 2 - w / 2; y = 150
    rect(c, x, y, w, 96, INK, 0.82 * p, r=48); rect(c, x, y, w, 96, th(ctx)["acc"], p, r=48, stroke=4)
    draw_text(c, f"«{txt}»", W / 2, y + 63, "dmserifi", 44, WHITE, p, align="center")

# ================================================================ rótulos fijos
TAGS = {"PARTIDA": (GRN, "SE VE EN LA PARTIDA"), "GUIA": ("#36E3FF", "SEGÚN LA GUÍA DE IGN"), "PRENSA": ("#36E3FF", "SEGÚN LA PRENSA"),
        "ROCKSTAR": (YEL, "SEGÚN ROCKSTAR"), "FILTRADO": ("#FF8A1F", "DOCUMENTO FILTRADO · SIN CONFIRMAR"),
        "OBSERVADO": ("#9BE38D", "OBSERVADO EN PARTIDAS REALES"),
        "GUIA2013": ("#36E3FF", "SEGÚN UNA GUÍA DE 2013"), "GUIAS": ("#36E3FF", "SEGÚN LAS GUÍAS")}
def cert(c, kind, a=1.0, y=82, left=False):
    if a <= 0 or kind not in TAGS: return
    col, txt = TAGS[kind]; size = 24; f = font("ovmono", size); w = text_w(txt, f, 1) + size * 2.2; h = size * 1.75
    x = 40 if left else W / 2 - w / 2
    rect(c, x, y, w, h, INK, 0.84 * a, r=h / 2); rect(c, x, y, w, h, col, a, r=h / 2, stroke=3)
    circle(c, x + size * 0.95, y + h / 2, size * 0.32, col, a)
    draw_text(c, txt, x + size * 1.6, y + h / 2 + size * 0.36, "ovmono", size, col, a, tracking=1)

def credit(c, sh):
    vid, T = parse_x(sh["src"])
    txt = f"Gameplay: {AUTHOR.get(vid, vid)} · {'Internet Archive' if vid.startswith('vp') else 'YouTube'} · {int(T // 60)}:{int(T % 60):02d}"
    f = font("ovmonomd", 20); w = text_w(txt, f, 0.5) + 34
    rect(c, W - w - 30, H - 64, w, 36, "#000000", 0.55, r=5); draw_text(c, txt, W - w - 13, H - 39, "ovmonomd", 20, "#F3F0E9", 0.9, tracking=0.5)

def overlay(c, gt, ctx):
    T = table(ctx); TH = th(ctx)
    i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
    bi = max(0, bisect.bisect_right(T["bstarts"], gt) - 1); b = T["beats"][bi]["b"]
    if gt > ctx.total - 20.3 or sh["src"] == "g:sting": return
    ch = None
    for st, cc in T["chapters"]:
        if gt >= st: ch = (st, cc)
    if ch and gt < ctx.total - 60:
        st, (n, name) = ch; tt = gt - st
        if tt < 2.7:
            p = ease_out(prog(tt, 0, 0.35)) * (1 - prog(tt, 2.3, 2.7)); wv = W * ease_out(prog(tt, 0, 0.35))
            rect(c, 0, H / 2 - 130, wv, 260, INK, 0.86 * p); rect(c, 0, H / 2 - 130, wv, 8, TH["acc"], p)
            draw_text(c, f"{TH['chap']} {n}", 120, H / 2 - 50, "ovmonomd", 34, TH["acc"], p, tracking=4)
            draw_text(c, name, 116, H / 2 + 70, "anton", 120, WHITE, p, tracking=3)
        elif not sh.get("clean"):
            txt = f"{n:02d} · {name}"; f = font("ovmonomd", 22); w = text_w(txt, f, 0.5) + 44
            G.chip(c, W / 2 - w / 2, 26, txt, 0.95, 22, TH["acc"])
    if not sh.get("clean"):
        ck = sh.get("cert", b.get("cert"))
        if ck and (not sh["src"].startswith("g:") or sh.get("cert")): cert(c, ck, 1.0, y=82 if not sh["src"].startswith("g:") else 92, left=sh["src"].startswith("g:"))
        if sh["src"].startswith("x:") and ctx.V.get("credit", True): credit(c, sh)   # credit=False: créditos solo en la descripción
    if b.get("cta"): cta_pill(c, gt - T["bstarts"][bi], ctx)
    if not sh.get("nosub"): G.subtitles(c, gt, ctx)   # nosub: el plano enseña el subtítulo del propio juego
    if gt > 3: K.watermark(c, W, H, 0.45, corner="tl", size=40)

def cta_pill(c, tt, ctx):
    """Llamada a mitad del vídeo sin tapar la partida: «DALE LIKE» y «SUSCRÍBETE» abajo a la izquierda, con un pulso."""
    TH = th(ctx); p = ease_out_back(prog(tt, 0.2, 0.7)) * (1 - prog(tt, 7.0, 7.5))
    if p <= 0: return
    beat_ = 1 + 0.04 * math.sin(tt * 6)
    c.save(); c.translate(70, H - 250); c.scale(p * beat_, p * beat_)
    rect(c, 0, 0, 330, 84, WHITE, 0.96, r=42); draw_text(c, "DALE LIKE", 165, 56, "anton", 44, INK, 1, align="center", tracking=1)
    rect(c, 350, 0, 360, 84, "#E62117", 1, r=42); draw_text(c, "SUSCRÍBETE", 530, 56, "anton", 44, WHITE, 1, align="center", tracking=2)
    c.restore()

# ================================================================ gráficos propios (g:)
def panel(c, t, ctx, dark=0.0):
    TH = th(ctx)
    rect(c, 0, 0, W, H, TH["bg"], 1)
    if ctx.V.get("theme") == "juicio":   # vetas de madera muy suaves
        for k in range(14):
            y = k * 82 + 20 * math.sin(k * 1.7); line(c, 0, y, W, y + 14 * math.sin(k), "#C9A227", 0.035, w=3)
    else: grid(c, W, H, 90, "#FFFFFF", 0.03)
    r = 0.5 + 0.5 * math.sin(t * 1.6)
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(-100, -100, 1300, [hexc(TH["glow1"], 0.10 * r), hexc(TH["glow1"], 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), rad_grad(W + 100, H + 100, 1300, [hexc(TH["glow2"], 0.10 * (1 - r)), hexc(TH["glow2"], 0)]))
    if dark: rect(c, 0, 0, W, H, "#000000", dark)

def title_top(c, txt, p, ctx, sub=None, col=None):
    draw_text(c, txt, W / 2, 190, "anton", 96, col or th(ctx)["acc"], p, align="center", tracking=3)
    if sub: draw_text(c, sub, W / 2, 250, "intersb", 34, WHITE, 0.85 * p, align="center")

def g_sting(c, t, d, sh, ctx):
    class I: pass
    K.brand_sting(c, t, I(), ctx)

def g_cover(c, t, d, sh, ctx):
    """Portada del vídeo dentro del montaje: rótulo pequeño + título grande + subtítulo."""
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out(prog(t, 0.05, 0.45))
    draw_text(c, sh.get("kicker", ""), W / 2, 330, "ovmonomd", 34, TH["acc"], p, align="center", tracking=6)
    for j, ln in enumerate(sh["lines"]):
        q = ease_out_back(prog(t, 0.2 + 0.15 * j, 0.55 + 0.15 * j))
        c.save(); c.translate(W / 2, 470 + j * 150); c.scale(0.7 + 0.3 * q, 0.7 + 0.3 * q)
        draw_text(c, ln, 0, 50, "anton", 150, WHITE if j == 0 else TH["acc"], clamp(q * 1.4), align="center", tracking=3); c.restore()
    if sh.get("sub"): draw_text(c, sh["sub"], W / 2, 860, "intersb", 40, GRAY, ease_out(prog(t, 0.8, 1.2)), align="center")

def g_quote(c, t, d, sh, ctx):
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out(prog(t, 0.05, 0.45))
    c.save(); c.translate(0, (1 - p) * 40)
    lines = wrap(sh["q"], "dmserif", 70, W - 760); hh = 200 + 86 * len(lines)
    y0 = H / 2 - hh / 2 - 20
    rect(c, 180, y0, W - 360, hh, INK, 0.9 * p, r=20); rect(c, 180, y0, 12, hh, sh.get("col", TH["acc"]), p)
    draw_text(c, "«", 250, y0 + 180, "dmserif", 220, sh.get("col", TH["acc"]), p)
    for j, ln in enumerate(lines): draw_text(c, ln, 380, y0 + 130 + j * 86, "dmserif", 70, WHITE, p)
    draw_text(c, sh.get("who", ""), 380, y0 + hh - 50, "ovmonomd", 28, sh.get("col", TH["acc"]), p, tracking=1)
    c.restore()
    if sh.get("tag"): cert(c, sh["tag"], ease_out(prog(t, 0.3, 0.6)), y=y0 - 80 + (1 - p) * 40)
    if sh.get("sub"):
        q = ease_out(prog(t, sh.get("sub_at", 1.5), sh.get("sub_at", 1.5) + 0.4)); draw_text(c, sh["sub"], W / 2, min(890, y0 + hh + 90), "intersb", 38, GRAY, q, align="center")

def g_list(c, t, d, sh, ctx):
    """Lista que aparece punto a punto al ritmo de la voz (cues)."""
    panel(c, t, ctx); TH = th(ctx)
    title_top(c, sh["title"], ease_out(prog(t, 0, 0.3)), ctx, sh.get("subt"))
    items = sh["items"]; st = sh.get("st") or [0.3 + 0.8 * k for k in range(len(items))]
    gap = min(135, 640 / max(1, len(items))); y0 = 360 if len(items) > 3 else 420
    for j, it in enumerate(items):
        txt, col = (it, TH["acc"]) if isinstance(it, str) else it
        p = ease_out_back(prog(t, st[j], st[j] + 0.35))
        if p <= 0: continue
        y = y0 + j * gap; c.save(); c.translate(W / 2 - 700, y); c.scale(p, p); c.translate(-(W / 2 - 700), -y)
        rect(c, W / 2 - 760, y - 50, 1520, 100, INK, 0.9, r=14); circle(c, W / 2 - 690, y, 30, col, 1)
        draw_text(c, str(j + 1), W / 2 - 690, y + 13, "anton", 38, INK, 1, align="center")
        draw_text(c, txt, W / 2 - 630, y + 18, "anton", 54, WHITE, 1, tracking=1); c.restore()

def g_creators(c, t, d, sh, ctx):
    panel(c, t, ctx); TH = th(ctx)
    title_top(c, sh.get("title", "PARTIDAS REALES"), ease_out(prog(t, 0, 0.4)), ctx, sh.get("subt"))
    for j, (a_, b_) in enumerate(sh["rows"]):
        p = ease_out_back(prog(t, 0.25 + 0.15 * j, 0.6 + 0.15 * j)); y = 400 + j * 130
        if p <= 0: continue
        c.save(); c.translate(W / 2, y); c.scale(p, p); c.translate(-W / 2, -y)
        rect(c, W / 2 - 640, y - 52, 1280, 104, INK, 0.9, r=16); rect(c, W / 2 - 640, y - 52, 12, 104, TH["acc"], 1)
        draw_text(c, a_, W / 2 - 590, y + 20, "anton", 60, WHITE, 1, tracking=1)
        draw_text(c, b_, W / 2 + 600, y + 12, "intersb", 32, TH["acc"], 1, align="right"); c.restore()
    if sh.get("foot"): draw_text(c, sh["foot"], W / 2, 890, "ovmonomd", 26, GRAY, ease_out(prog(t, 0.8, 1.2)), align="center")

# ---------------------------------------------------------------- Planeta Vice City
def leaf(c, x, y, s, col, a=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    pth = skia.Path(); pth.moveTo(0, -s); pth.cubicTo(s * 0.9, -s * 0.5, s * 0.7, s * 0.6, 0, s); pth.cubicTo(-s * 0.7, s * 0.6, -s * 0.9, -s * 0.5, 0, -s)
    c.drawPath(pth, paint(col, a)); line(c, 0, -s * 0.8, 0, s * 0.9, INK, 0.35 * a, w=3); c.restore()

def g_especie(c, t, d, sh, ctx):
    """Ficha de campo (formato de documental): nombre común, nombre «científico» (de broma, indicado en pantalla) y rasgos."""
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out(prog(t, 0.05, 0.4))
    for k in range(6): leaf(c, 120 + k * 50, 120 + 30 * math.sin(k + t), 26, TH["glow1"], 0.25 * p, rot=k * 40 + t * 6)
    x0, y0, w0, h0 = 260, 200, W - 520, 700
    rect(c, x0 + 14, y0 + 18, w0, h0, "#000000", 0.45 * p, r=24, blur=18)
    rect(c, x0, y0, w0, h0, "#EFE6CF", 0.97 * p, r=24); rect(c, x0, y0, w0, 110, TH["glow1"], 0.95 * p, r=24); rect(c, x0, y0 + 80, w0, 30, TH["glow1"], 0.95 * p)
    draw_text(c, sh.get("head", "FICHA DE CAMPO"), x0 + 50, y0 + 75, "ovmonomd", 40, INK, p, tracking=6)
    draw_text(c, sh["name"], x0 + 50, y0 + 210, "anton", 92, INK, p, tracking=1)
    if sh.get("latin"): draw_text(c, sh["latin"], x0 + 54, y0 + 268, "dmserifi", 46, "#3A4A3E", p)
    st = sh.get("st") or [0.6 + 0.7 * k for k in range(len(sh["rows"]))]
    for j, (k_, v_) in enumerate(sh["rows"]):
        q = ease_out(prog(t, st[j], st[j] + 0.35))
        y = y0 + 360 + j * 82
        draw_text(c, k_.upper(), x0 + 54, y, "ovmonomd", 28, "#5A6B5E", q, tracking=3)
        draw_text(c, v_, x0 + 380, y + 4, "intersb", 40, INK, q)
        line(c, x0 + 50, y + 26, x0 + w0 - 50, y + 26, "#5A6B5E", 0.25 * q, w=2)
    if sh.get("note"): draw_text(c, sh["note"], W / 2, min(890, y0 + h0 + 70), "ovmonomd", 24, GRAY, p, align="center")

# ---------------------------------------------------------------- GTA 6 a juicio
def gavel(c, x, y, s, col, a=1.0, ang=0.0, base=True):
    """Mazo de juez: cabeza con aros en los extremos, mango en diagonal y (opcional) taco debajo. ang en radianes (giro del golpe)."""
    if base:
        rect(c, x - s * 0.95, y + s * 0.52, s * 0.9, s * 0.16, col, a * 0.8, r=s * 0.05)
        rect(c, x - s * 0.85, y + s * 0.40, s * 0.7, s * 0.14, col, a * 0.8, r=s * 0.04)
    c.save(); c.translate(x, y); c.rotate(math.degrees(ang) - 40)
    rect(c, -s * 0.055, 0, s * 0.11, s * 1.0, col, a, r=s * 0.05)
    rect(c, -s * 0.40, -s * 0.17, s * 0.80, s * 0.34, col, a, r=s * 0.07)
    rect(c, -s * 0.50, -s * 0.22, s * 0.13, s * 0.44, col, a, r=s * 0.04); rect(c, s * 0.37, -s * 0.22, s * 0.13, s * 0.44, col, a, r=s * 0.04)
    c.restore()

def g_cargo(c, t, d, sh, ctx):
    """Cargo de la acusación o argumento de la defensa: número, texto y lado."""
    panel(c, t, ctx); TH = th(ctx)
    col = LADO_COL.get(sh.get("lado", "acusacion"), th(ctx)["acc"])
    p = ease_out_back(prog(t, 0.05, 0.45))
    draw_text(c, sh.get("kicker", "CARGO"), W / 2, 300, "ovmonomd", 40, col, clamp(p), align="center", tracking=8)
    for j, ln in enumerate(wrap(sh["txt"], "anton", 110, W - 300)):
        q = ease_out(prog(t, 0.2 + 0.12 * j, 0.55 + 0.12 * j))
        draw_text(c, ln, W / 2, 470 + j * 125, "anton", 110, WHITE, q, align="center", tracking=2)
    gavel(c, W / 2, 860, 90, TH["acc"], ease_out(prog(t, 0.5, 0.8)), ang=-0.5 + 0.5 * ease_out_back(prog(t, 0.5, 0.8)))

def g_marcador(c, t, d, sh, ctx):
    """Marcador del juicio: pruebas de la acusación (rojo) y de la defensa (azul)."""
    panel(c, t, ctx); TH = th(ctx)
    title_top(c, sh.get("title", "LAS PRUEBAS"), ease_out(prog(t, 0, 0.3)), ctx)
    names = sh.get("names", ("ACUSACIÓN", "DEFENSA")); colors = sh.get("colors", (RED, BLUE))
    cols = [(names[0], colors[0], sh.get("acu", []), W / 2 - 470), (names[1], colors[1], sh.get("def", []), W / 2 + 470)]
    st = sh.get("st") or []; k = 0
    for name, col, items, cx in cols:
        p = ease_out(prog(t, 0.1, 0.4))
        rect(c, cx - 420, 290, 840, 90, col, 0.95 * p, r=14); draw_text(c, name, cx, 352, "anton", 58, WHITE, p, align="center", tracking=4)
        for j, it in enumerate(items):
            at = st[k] if k < len(st) else 0.5 + 0.4 * k; k += 1
            q = ease_out_back(prog(t, at, at + 0.35))
            if q <= 0: continue
            y = 450 + j * 112
            c.save(); c.translate(cx, y); c.scale(q, q)
            rect(c, -420, -44, 840, 88, INK, 0.9, r=12); rect(c, -420, -44, 10, 88, col, 1)
            draw_text(c, it, -385, 16, "anton", 44, WHITE, 1, tracking=1); c.restore()

def g_testigo(c, t, d, sh, ctx):
    """Testigo: quién es, qué dijo (traducido) y dónde lo dijo."""
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out(prog(t, 0.05, 0.4))
    draw_text(c, "TESTIGO", 200, 250, "ovmonomd", 34, TH["acc"], p, tracking=8)
    draw_text(c, sh["name"], 196, 370, "anton", 110, WHITE, p, tracking=2)
    draw_text(c, sh["role"], 200, 440, "intersb", 40, GRAY, p)
    q = ease_out(prog(t, 0.6, 1.0))
    for j, ln in enumerate(wrap(f"«{sh['q']}»", "dmserif", 62, W - 460)): draw_text(c, ln, 200, 580 + j * 80, "dmserif", 62, WHITE, q)
    draw_text(c, sh["fuente"], 200, 890, "ovmonomd", 26, TH["acc"], q, tracking=1)
    gavel(c, W - 260, 300, 110, TH["acc"], 0.25 * p, ang=-0.4)

def g_veredicto(c, t, d, sh, ctx):
    panel(c, t, ctx); TH = th(ctx)
    title_top(c, sh.get("title", "TU VEREDICTO"), ease_out(prog(t, 0, 0.3)), ctx, sh.get("subt"))
    st = sh.get("st") or [0.4, 0.9]
    for j, (txt, sub, col) in enumerate(sh.get("opts", [("CULPABLE", "juego de crímenes", RED), ("INOCENTE", "simulador de vida", BLUE)])):
        p = ease_out_back(prog(t, st[j], st[j] + 0.4))
        if p <= 0: continue
        cx = W / 2 + (-430 if j == 0 else 430); c.save(); c.translate(cx, 600); c.scale(p, p)
        rect(c, -380, -190, 760, 380, INK, 0.92, r=28); rect(c, -380, -190, 760, 380, col, 1, r=28, stroke=8)
        draw_text(c, txt, 0, 20, "anton", 130, col, 1, align="center", tracking=3)
        draw_text(c, sub, 0, 110, "intersb", 42, WHITE, 1, align="center"); c.restore()
    q = ease_out(prog(t, st[-1] + 0.6, st[-1] + 1.0))
    if sh.get("foot"): draw_text(c, sh["foot"], W / 2, 920, "anton", 60, WHITE, q, align="center", tracking=2)

def g_ronda(c, t, d, sh, ctx):
    """Resultado de un asalto: quién lo gana (o empate), por qué y el marcador acumulado GTA V – GTA VI."""
    panel(c, t, ctx); TH = th(ctx)
    p = ease_out(prog(t, 0.05, 0.4))
    draw_text(c, f"ASALTO {sh['n']}", W / 2, 230, "ovmonomd", 40, TH["acc"], p, align="center", tracking=10)
    draw_text(c, sh["tema"], W / 2, 330, "anton", 86, WHITE, p, align="center", tracking=2)
    g = sh["gana"]; col = {"gta5": G5, "gta6": G6}.get(g, TH["acc"]); txt = {"gta5": "GANA GTA V", "gta6": "GANA GTA VI"}.get(g, "EMPATE")
    q = ease_out_back(prog(t, 0.45, 0.85))
    if q > 0:
        c.save(); c.translate(W / 2, 520); c.scale(q, q); f = font("anton", 120); w = text_w(txt, f, 3) + 140
        rect(c, -w / 2, -100, w, 200, col, 1, r=24); draw_text(c, txt, 0, 46, "anton", 120, INK, 1, align="center", tracking=3); c.restore()
    r = ease_out(prog(t, 1.0, 1.4))
    for j, ln in enumerate(wrap(sh.get("razon", ""), "intersb", 44, W - 500)): draw_text(c, ln, W / 2, 720 + j * 58, "intersb", 44, GRAY, r, align="center")
    a5, a6 = sh["score"]; m = ease_out(prog(t, 1.4, 1.8))
    draw_text(c, "GTA V", W / 2 - 260, 880, "anton", 54, G5, m, align="center", tracking=2)
    draw_text(c, f"{a5}  –  {a6}", W / 2, 884, "anton", 64, WHITE, m, align="center", tracking=4)
    draw_text(c, "GTA VI", W / 2 + 260, 880, "anton", 54, G6, m, align="center", tracking=2)

def g_subscribe(c, t, d, sh, ctx):
    panel(c, t, ctx)
    p = ease_out_back(prog(t, 0.05, 0.45))
    c.save(); c.translate(W / 2, 470); c.scale(p, p); draw_badge(c, 0, 0, 200, t=t); c.restore()
    wordmark(c, W / 2, 790, 90, a=ease_out(prog(t, 0.3, 0.7)), align="center")
    q = ease_out_back(prog(t, 0.6, 1.0))
    c.save(); c.translate(W / 2, 900); c.scale(q, q); rect(c, -260, -55, 520, 110, "#E62117", 1, r=16)
    draw_text(c, "SUSCRÍBETE", 0, 22, "anton", 64, WHITE, 1, align="center", tracking=3); c.restore()

def g_end(c, t, d, sh, ctx):
    class I: pass
    K.end_screen(c, t, I(), ctx, title="SIGUIENTE SALIDA", sub="Más GTA 6 contado de otra forma, sin spoilers")

GFX = {k[2:]: v for k, v in list(globals().items()) if k.startswith("g_")}

# ================================================================ miniaturas (1280×720)
def _bg(c, path, x, y, w, h, crop=None, tint=None):
    if not os.path.exists(path): rect(c, x, y, w, h, "#101218", 1); return
    img = G.load_img(path, maxw=3840); iw, ih = img.width(), img.height()
    u0, v0, u1, v1 = crop or (0, 0, 1, 1); src = skia.Rect.MakeLTRB(u0 * iw, v0 * ih, u1 * iw, v1 * ih)
    sw, sh_ = src.width(), src.height(); s = max(w / sw, h / sh_); dw, dh = sw * s, sh_ * s
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    c.drawImageRect(img, src, skia.Rect.MakeXYWH(x + (w - dw) / 2, y + (h - dh) / 2, dw, dh), SO_HQ, skia.Paint())
    if tint: rect(c, x, y, w, h, tint[0], tint[1])
    c.restore()

def thumb_juicio(c):
    """Mitad crimen (tanque en la pista, partida de GameV) / mitad vida (Jason arreglando el techo, guía de IGN) y el mazo."""
    Wt, Ht = 1280, 720; base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_3_GTA6_A_JUICIO", "trabajo")
    _bg(c, os.path.join(base, "miniatura_crimen.png"), 0, 0, 660, Ht, crop=(0.25, 0.08, 0.80, 0.92), tint=("#7A0B12", 0.35))
    _bg(c, os.path.join(base, "miniatura_vida.png"), 620, 0, 660, Ht, crop=(0.08, 0.05, 0.62, 0.95), tint=("#0B2A6E", 0.30))
    pth = skia.Path(); pth.moveTo(610, 0); pth.lineTo(690, 0); pth.lineTo(650, Ht); pth.lineTo(570, Ht); pth.close(); c.drawPath(pth, paint("#0E0B08", 1))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, Ht)], [skia.Color(0, 0, 0, 150), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 200)], [0, 0.45, 1]))
    c.drawRect(skia.Rect.MakeWH(Wt, Ht), g)
    draw_text(c, "¿CULPABLE?", 330, 150, "anton", 104, "#FF6B6B", 1, align="center", tracking=2)
    draw_text(c, "¿INOCENTE?", 960, 150, "anton", 104, "#8FB8FF", 1, align="center", tracking=2)
    rect(c, 250, 500, 780, 180, "#0E0B08", 0.94, r=22); rect(c, 250, 500, 780, 180, "#E8C468", 1, r=22, stroke=7)
    draw_text(c, "GTA 6 A JUICIO", 640, 618, "anton", 124, "#E8C468", 1, align="center", tracking=3)
    draw_text(c, "CON PRUEBAS REALES", 640, 474, "ovmono", 30, WHITE, 0.95, align="center", tracking=4)

def thumb_combate(c):
    """Tanque contra tanque: GTA 5 (guía de Kotaku, 2013) a la izquierda, GTA 6 (persecución de seis estrellas de GameV) a la derecha."""
    Wt, Ht = 1280, 720; base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_4_GTA5_VS_GTA6", "trabajo")
    _bg(c, os.path.join(base, "miniatura_gta5.png"), 0, 0, 660, Ht, crop=(0.26, 0.22, 0.86, 1.0), tint=("#0E3B1A", 0.12))
    _bg(c, os.path.join(base, "miniatura_gta6.png"), 620, 0, 660, Ht, crop=(0.16, 0.16, 0.70, 1.0), tint=("#4A0B2A", 0.12))
    pth = skia.Path(); pth.moveTo(612, 0); pth.lineTo(688, 0); pth.lineTo(652, Ht); pth.lineTo(576, Ht); pth.close(); c.drawPath(pth, paint("#0B0B10", 1))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, Ht)], [skia.Color(0, 0, 0, 190), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 225)], [0, 0.32, 0.62, 1]))
    c.drawRect(skia.Rect.MakeWH(Wt, Ht), g)
    draw_text(c, "GTA V", 300, 160, "anton", 150, G5, 1, align="center", tracking=3)
    draw_text(c, "GTA VI", 985, 160, "anton", 150, G6, 1, align="center", tracking=3)
    circle(c, 632, 330, 92, "#0B0B10", 1); circle(c, 632, 330, 92, "#F5C542", 1, stroke=8)
    draw_text(c, "VS", 632, 366, "anton", 100, "#F5C542", 1, align="center", tracking=2)
    rect(c, 330, 600, 620, 96, "#0B0B10", 0.94, r=18); rect(c, 330, 600, 620, 96, "#F5C542", 1, r=18, stroke=6)
    draw_text(c, "8 ASALTOS", 640, 676, "anton", 74, "#F5C542", 1, align="center", tracking=4)
    draw_text(c, "CON PARTIDAS REALES", 640, 586, "ovmono", 26, WHITE, 0.95, align="center", tracking=4)

def thumb_planeta(c):
    """Fotograma real (dos habitantes rechazan a Jason a la puerta de una barbería, partida de toaster) con ficha de documental."""
    Wt, Ht = 1280, 720; base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_2_PLANETA_VICE_CITY", "trabajo")
    _bg(c, os.path.join(base, "miniatura_fondo.png"), 0, 0, Wt, Ht, crop=(0.12, 0.0, 1.0, 0.70))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, 300)], [skia.Color(5, 14, 9, 240), skia.Color(5, 14, 9, 170), skia.Color(5, 14, 9, 0)], [0, 0.6, 1]))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, Wt, 300), g)
    for k in range(4): leaf(c, 74 + k * 46, 70, 24, "#2FBF71", 0.95, rot=k * 30)
    draw_text(c, "PLANETA", 300, 120, "anton", 118, WHITE, 1, tracking=3)
    draw_text(c, "VICE CITY", 735, 120, "anton", 118, "#9BE38D", 1, tracking=3)
    draw_text(c, "DOCUMENTAL CON PARTIDAS REALES", Wt / 2, 182, "ovmono", 28, WHITE, 0.95, align="center", tracking=3)
    rect(c, 40, 540, 600, 140, "#EFE6CF", 0.96, r=16); rect(c, 40, 540, 600, 34, "#2FBF71", 1, r=16); rect(c, 40, 556, 600, 18, "#2FBF71", 1)
    draw_text(c, "ESPECIE OBSERVADA", 64, 566, "ovmonomd", 22, INK, 1, tracking=3)
    draw_text(c, "LOS HUMANOS DE GTA 6", 64, 640, "anton", 54, INK, 1, tracking=1)
