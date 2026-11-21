"""Shorts verticales (1080×1920) con gameplay de terceros: base común de SHORT_01 y SHORT_02.

Reutiliza de gl_render la tabla de planos anclados a palabras, las ventanas por corte de escena y el catálogo de clips con
sus créditos. Aquí se añade lo propio del formato vertical:
  - recorte de la fuente (SRC_CROP): solo la zona limpia del vídeo original, sin rótulos ni logotipos del autor;
  - encuadre vertical: cada plano elige su centro de interés (cx, cy) y un zoom; se decodifica directamente la ventana
    de la copia 4K a 1080×1920, sin reescalar dos veces;
  - lectura al ritmo nativo de la fuente (60 fps) con mezcla de fotogramas: cámara lenta fluida y sin saltos;
  - nunca hay bucles: si un tramo se acaba, se mantiene el último fotograma; «cont» encadena planos sin repetir imagen;
  - impactos (golpe de zoom y destello) y congelados;
  - crédito discreto en pantalla (autor y plataforma) y dos estilos de subtítulos: «cinético» y «máquina de escribir».
Cada Short define su propio aspecto (scene, overlay, gráficos y música) en su módulo.
"""
import bisect, math, subprocess, numpy as np, skia
from gfx import *
from videos import gl_render as G

W, H, FPS = 1080, 1920, 30
SRC_CROP = {}          # ID → (x, y, w, h) en píxeles del vídeo original
_CL = {}

def _even(v): return int(v) // 2 * 2

def window(meta, crop, aspect, z, fx, fy):
    """Ventana de la fuente (x, y, w, h) con la proporción del panel, zoom z y foco (fx, fy) ∈ [0, 1] dentro de la zona limpia."""
    x0, y0, w0, h0 = crop or (0, 0, meta["w"], meta["h"])
    if w0 / h0 > aspect: ch = h0 / z; cw = ch * aspect
    else: cw = w0 / z; ch = cw / aspect
    x = x0 + clamp(fx) * (w0 - cw); y = y0 + clamp(fy) * (h0 - ch)
    return _even(x), _even(y), _even(cw), _even(ch)

_FPS = {}
EFF_FPS = {}   # ID → ritmo real de imágenes distintas cuando el archivo duplica fotogramas (juego a 30 fps guardado a 60)
def src_fps(path):
    """Fotogramas por segundo reales de la fuente (p. ej. 60 o 59,94): se decodifica a ese ritmo, no a 30.
    Si el archivo repite cada fotograma (30 fps de juego dentro de un archivo de 60), se decodifica a 30: así cada
    fotograma leído es distinto y la mezcla entre dos consecutivos da un movimiento uniforme."""
    import os
    vid = os.path.splitext(os.path.basename(path))[0]
    if vid in EFF_FPS: return (str(EFF_FPS[vid]), float(EFF_FPS[vid]))
    if path not in _FPS:
        o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path],
                           capture_output=True, text=True).stdout.strip()
        n, d_ = (o.split("/") + ["1"])[:2]; fr = float(n) / float(d_ or 1)
        _FPS[path] = (o if fr <= 61 else "60", min(fr, 60.0))
    return _FPS[path]

class VClip:
    """Lee un tramo de vídeo recortado a una ventana y escalado al panel, al ritmo nativo de la fuente.
    frame(i) → fotograma i (desde t0). Guarda los últimos fotogramas para poder mezclar dos consecutivos."""
    def __init__(self, path, t0, dur, win, size):
        self.path, self.t0, self.win, self.size, self.dur = path, t0, win, size, dur
        self.rate, self.fps = src_fps(path)
        self._open()
    def _open(self):
        x, y, w, h = self.win; tw, th = self.size
        vf = f"crop={w}:{h}:{x}:{y},scale={tw}:{th}:flags=bicubic,fps={self.rate},format=rgba"
        self.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "fatal", "-ss", f"{max(0.0, self.t0):.3f}", "-i", self.path, "-t", f"{self.dur + 0.5:.3f}", "-an",
                                   "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE, bufsize=tw * th * 4 * 2)
        self.i = -1; self.cache = {}; self.eof = False; self.last = None
    def frame(self, i):
        tw, th = self.size
        if self.cache and i < min(self.cache): self.close(); self._open()     # hace falta un fotograma anterior: se vuelve a abrir
        while self.i < i and not self.eof:
            buf = self.p.stdout.read(tw * th * 4)
            if len(buf) < tw * th * 4: self.eof = True; break
            self.i += 1
            if self.i >= i - 2:
                self.cache[self.i] = skia.Image.fromarray(np.frombuffer(buf, np.uint8).reshape(th, tw, 4), colorType=skia.ColorType.kRGBA_8888_ColorType)
                for k in [k for k in self.cache if k < self.i - 3]: del self.cache[k]
            self.last = self.i
        if i in self.cache: return self.cache[i]
        return self.cache.get(self.last) if self.last is not None else None      # fin del tramo: se queda en el último
    def close(self):
        try: self.p.stdout.close(); self.p.kill(); self.p.wait(timeout=2)
        except Exception: pass

def focus(sh):
    """Centro de interés del plano → foco (fx, fy) para la ventana. cx/cy: posición del sujeto en la zona limpia (0-1)."""
    if "f" in sh: return sh["f"]
    return sh.get("cx", 0.5), sh.get("cy", 0.5)

def speed_of(sh, Ls, d):
    """Velocidad del plano: 1 si el tramo de la fuente cubre todo el plano; si no, cámara lenta hasta ×0,5 (fluida porque
    la fuente es de 60 fps y se mezclan fotogramas). Si aun así no alcanza, el último fotograma se mantiene: nunca hay bucle."""
    if sh.get("speed"): return sh["speed"]
    return max(0.5, min(1.0, Ls / max(d, 0.1)))

def plan(T):
    """Planos «cont»: empiezan justo donde terminó el plano anterior de la misma fuente (continuidad sin repetir imagen)."""
    if T.get("_planned"): return
    prev = None
    for s in T["shots"]:
        if not s["src"].startswith("x:"): prev = None; continue
        vid = s["src"][2:].split("@")[0]
        if s.get("cont") and prev and prev["src"][2:].split("@")[0] == vid:
            pp, ploc, pLs = G.src_window(dict(prev)); pd = prev["t1"] - prev["t0"]
            end = ploc + min(pLs, pd * speed_of(prev, pLs, pd))
            s["src"] = f"x:{vid}@{end:.3f}"; s.setdefault("minwin", 0.05); s.pop("_win", None)
        prev = s
    T["_planned"] = True

def footage(c, sh, tau, d, box, slot="main"):
    """Dibuja el plano de vídeo en box = (x, y, w, h). Zoom z=(z0, z1) progresivo, cámara lenta fluida (speed), congelado (freeze),
    golpe de zoom (punch) y destello (flash). Nunca vuelve atrás: si el tramo se acaba, se mantiene el último fotograma."""
    k, v = sh["src"].split(":", 1); vid = v.split("@")[0]
    path, loc, Ls = G.src_window(sh)
    meta = G._clip_meta(path); rx, ry, rw, rh = box
    tau = max(0.0, tau)                                    # antes del primer plano (entrada) no hay tiempo negativo
    z0, z1 = sh.get("z", (1.0, 1.06)); fx, fy = focus(sh); zb = min(z0, z1)   # se decodifica al zoom menor: luego solo se amplía
    crop = SRC_CROP.get(vid); x0, y0, w0, h0 = crop or (0, 0, meta["w"], meta["h"])
    a = rw / rh
    def to_f(cx, cy, z):
        if w0 / h0 > a: ch = h0 / z; cw = ch * a
        else: cw = w0 / z; ch = cw / a
        fxx = (cx * w0 - cw / 2) / max(1, (w0 - cw)) if w0 > cw else 0.5
        fyy = (cy * h0 - ch / 2) / max(1, (h0 - ch)) if h0 > ch else 0.5
        return clamp(fxx), clamp(fyy)
    ffx, ffy = to_f(fx, fy, zb)
    win = window(meta, crop, a, zb, ffx, ffy)
    sp = speed_of(sh, Ls, d)
    tt = sh["freeze"] if sh.get("freeze") is not None else min(tau * sp, max(0.0, Ls - 0.02))
    key = (slot,)
    cl = _CL.get(key)
    if cl is None or cl.path != path or abs(cl.t0 - loc) > 1e-3 or cl.win != win or cl.size != (rw, rh):
        if cl: cl.close()
        cl = VClip(path, loc, Ls + 0.3, win, (rw, rh)); _CL[key] = cl
    fpos = tt * cl.fps; i0 = int(fpos); frac = fpos - i0
    img = cl.frame(i0)
    if img is None: return
    img2 = cl.frame(i0 + 1) if (frac > 0.04 and sh.get("freeze") is None) else None
    e = ease_io(clamp(tau / max(d, 0.1))) if sh.get("ease", True) else clamp(tau / max(d, 0.1))
    zz = lerp(z0, z1, e) / zb
    if sh.get("punch"):                                    # golpe de zoom suave en los impactos (sustituye a la sacudida)
        zz *= 1.0 + sh["punch"] * (1 - ease_out(prog(tau, 0.0, 0.32)))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(rx, ry, rw, rh))
    # el zoom progresivo se centra en el sujeto (su posición dentro de la ventana decodificada)
    wx, wy, ww, wh = win
    pxf = rx + rw * clamp((x0 + fx * w0 - wx) / max(1, ww)); pyf = ry + rh * clamp((y0 + fy * h0 - wy) / max(1, wh))
    c.translate(pxf, pyf); c.scale(zz, zz); c.translate(-pxf, -pyf)
    samp = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone); dst = skia.Rect.MakeXYWH(rx, ry, rw, rh)
    p = skia.Paint()
    if sh.get("cf") is not None: p.setColorFilter(sh["cf"])
    c.drawImageRect(img, dst, samp, p)
    if img2 is not None and img2 is not img:               # mezcla con el fotograma siguiente: movimiento continuo a cualquier velocidad
        p2 = skia.Paint(); p2.setAlphaf(frac)
        if sh.get("cf") is not None: p2.setColorFilter(sh["cf"])
        c.drawImageRect(img2, dst, samp, p2)
    c.restore()
    if sh.get("flash"):
        fa = 1 - prog(tau, 0.0, 0.18)
        if fa > 0: rect(c, rx, ry, rw, rh, "#FFFFFF", 0.85 * fa)

def color_matrix(sat=1.0, bright=0.0, contrast=1.0, tint=(0, 0, 0)):
    """Filtro de color sencillo: saturación, brillo, contraste y tinte (r, g, b en -1..1)."""
    lr, lg, lb = 0.2126, 0.7152, 0.0722; s = sat
    m = [lr * (1 - s) + s, lg * (1 - s), lb * (1 - s), 0, 0,
         lr * (1 - s), lg * (1 - s) + s, lb * (1 - s), 0, 0,
         lr * (1 - s), lg * (1 - s), lb * (1 - s) + s, 0, 0,
         0, 0, 0, 1, 0]
    o = (1 - contrast) * 0.5 + bright
    for r in range(3):
        for k in range(3): m[r * 5 + k] *= contrast
        m[r * 5 + 4] = o + tint[r] * 0.12
    return skia.ColorFilters.Matrix(m)

# ---------------------------------------------------------------- crédito y subtítulos
def credit(c, sh, x=44, y=118, a=1.0, dark=False):
    """Crédito discreto del gameplay (autor y plataforma). La narración nunca nombra al autor."""
    if not sh["src"].startswith("x:"): return
    vid = sh["src"][2:].split("@")[0]; txt = "Gameplay: " + G.x_credit(vid, short=True)
    f = font("ovmonomd", 22); w = text_w(txt, f, 0.5) + 30
    rect(c, x, y, w, 40, "#000000" if not dark else "#0B0C10", 0.55 * a, r=6)
    draw_text(c, txt, x + 15, y + 27, "ovmonomd", 22, "#F3F0E9", 0.92 * a, tracking=0.5)

_SUB = {}
def _chunks(ctx, maxc):
    if maxc in _SUB: return _SUB[maxc]
    out = []
    for b in ctx.tl["beats"]:
        for s in b["sents"]:
            cur = []; n = 0
            for w in s.get("words") or []:
                if cur and n + len(w[0]) + 1 > maxc: out.append(cur); cur = []; n = 0
                cur.append(w); n += len(w[0]) + 1
            if cur: out.append(cur)
    _SUB[maxc] = (out, [ch[0][1] for ch in out]); return _SUB[maxc]

def _current(ctx, gt, maxc):
    out, st = _chunks(ctx, maxc); i = bisect.bisect_right(st, gt + 0.02) - 1
    if i < 0: return None
    words = out[i]; end = words[-1][2]; nxt = st[i + 1] if i + 1 < len(st) else end + 1
    if gt > max(end + 0.3, min(nxt - 0.05, end + 0.6)): return None
    return words

def subs_kinetic(c, gt, ctx, y=1330, size=78, col="#FFFFFF", hi="#FFD23F", maxc=16):
    """Subtítulos cinéticos: 2-3 palabras en mayúsculas, la palabra que suena salta y cambia de color."""
    words = _current(ctx, gt, maxc)
    if not words: return
    f = font("anton", size); sp = size * 0.3          # espacio fijo: text_w(" ") devuelve 0 con esta fuente
    ws = [w[0].upper() for w in words]; tot = sum(text_w(x, f, 1) for x in ws) + sp * (len(ws) - 1)
    x = W / 2 - tot / 2
    for w, txt in zip(words, ws):
        on = w[1] - 0.03 <= gt; cur = on and gt < w[2] + 0.06; tw = text_w(txt, f, 1)
        sc = 1.0 + 0.16 * (1 - prog(gt, w[1], w[1] + 0.12)) if cur else 1.0
        c.save(); c.translate(x + tw / 2, y); c.scale(sc, sc); c.translate(-(x + tw / 2), -y)
        draw_text(c, txt, x + 5, y + 6, "anton", size, "#000000", 0.75, tracking=1)
        draw_text(c, txt, x, y, "anton", size, hi if cur else col, 1.0 if on else 0.55, tracking=1)
        c.restore(); x += tw + sp

def subs_typewriter(c, gt, ctx, y=1515, size=40, col="#E8F1F2", hi="#7CF3C4", maxc=30, bg="#05080B"):
    """Subtítulos de «máquina de escribir»: las letras aparecen con la voz; la palabra actual subrayada."""
    words = _current(ctx, gt, maxc)
    if not words: return
    f = font("ovmonomd", size); tw = sum(text_w(w[0], f, 0.5) for w in words) + size * 0.6 * (len(words) - 1)
    x = W / 2 - tw / 2
    rect(c, x - 26, y - size - 16, tw + 52, size + 40, bg, 0.72, r=8)
    xx = x
    for w in words:
        dur = max(0.08, w[2] - w[1]); n = len(w[0]); k = int(clamp((gt - w[1]) / dur) * n + 0.999) if gt >= w[1] - 0.02 else 0
        vis = w[0][:k]; ww = text_w(w[0], f, 0.5) + size * 0.6
        if vis: draw_text(c, vis, xx, y, "ovmonomd", size, col, 1, tracking=0.5)
        if w[1] <= gt < w[2] + 0.05: rect(c, xx, y + 10, text_w(w[0], f, 0.5), 4, hi, 1)
        xx += ww
    if int(gt * 2.5) % 2 == 0: rect(c, xx - 4, y - size + 6, 4, size, hi, 0.9)   # cursor

# ---------------------------------------------------------------- escena (común): plano actual + transición
def make_scene(draw_shot, trans=None):
    """Devuelve scene(c, t, info, ctx). draw_shot(c, sh, tau, d, ctx, slot) lo aporta cada Short.
    trans(sh_prev, sh) → None (corte seco) o duración de un fundido corto."""
    def scene(c, t, info, ctx):
        gt = info.start + t; T = G.table(ctx); plan(T)
        i = max(0, bisect.bisect_right(T["starts"], gt) - 1); sh = T["shots"][i]
        tau = gt - sh["t0"]; d = max(0.05, sh["t1"] - sh["t0"])
        draw_shot(c, sh, tau, d, ctx, "main")
        if i > 0 and trans:
            pv = T["shots"][i - 1]; td = trans(pv, sh)
            if td and tau < td:
                c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * (1 - tau / td)))
                draw_shot(c, pv, gt - pv["t0"], max(0.05, pv["t1"] - pv["t0"]), ctx, "prev"); c.restore()
    return scene

def current(ctx, gt):
    T = G.table(ctx); i = max(0, bisect.bisect_right(T["starts"], gt) - 1)
    bi = max(0, bisect.bisect_right(T["bstarts"], gt) - 1)
    return T["shots"][i], T["beats"][bi]["b"], i, bi
