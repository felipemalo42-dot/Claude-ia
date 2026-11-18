"""Música y efectos de sonido 100 % originales, sintetizados por código (sin muestras de terceros).

Todo el audio de este módulo se genera matemáticamente (osciladores, ruido, FM, envolventes),
por lo que no existe ningún derecho de terceros sobre él.
"""
import numpy as np
from scipy import signal

SR = 48000
rng = np.random.default_rng(7)

# ---------------------------------------------------------------- utilidades
def t_axis(d): return np.arange(int(d * SR)) / SR
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

def chord(name, octave=4):
    """'Am', 'F', 'Cmaj7', 'Dm9', 'G7', 'Esus4' → lista de notas MIDI."""
    import re
    m = re.match(r"([A-G][b#]?)(.*)", name); root = NOTE[m.group(1)] + 12 * (octave + 1); q = m.group(2)
    iv = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10],
          "m9": [0, 3, 7, 10, 14], "maj9": [0, 4, 7, 11, 14], "sus4": [0, 5, 7], "sus2": [0, 2, 7], "add9": [0, 4, 7, 14],
          "m6": [0, 3, 7, 9], "dim": [0, 3, 6], "madd9": [0, 3, 7, 14], "6": [0, 4, 7, 9]}[q]
    return [root + i for i in iv]

def adsr(n, a=0.01, d=0.1, s=0.7, r=0.1, sr=SR):
    a_, d_, r_ = int(a * sr), int(d * sr), int(r * sr)
    s_ = max(0, n - a_ - d_ - r_)
    env = np.concatenate([np.linspace(0, 1, a_, endpoint=False), np.linspace(1, s, d_, endpoint=False),
                          np.full(s_, s), np.linspace(s, 0, r_)])
    if len(env) < n: env = np.pad(env, (0, n - len(env)))
    return env[:n]

def lp(x, fc, order=2):
    fc = np.clip(fc, 20, SR / 2.2); b, a = signal.butter(order, fc / (SR / 2), "low"); return signal.lfilter(b, a, x)
def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), "high"); return signal.lfilter(b, a, x)
def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), min(hi, SR / 2.2) / (SR / 2)], "band"); return signal.lfilter(b, a, x)

def sweep_lp(x, f0, f1, blocks=64):
    """Filtro paso bajo con barrido de corte (por bloques)."""
    out = np.zeros_like(x); n = len(x); bs = max(1, n // blocks); zi = None
    for i in range(0, n, bs):
        fr = i / max(1, n - 1); fc = f0 * (f1 / f0) ** fr
        b, a = signal.butter(2, np.clip(fc, 30, SR / 2.3) / (SR / 2), "low")
        if zi is None: zi = signal.lfilter_zi(b, a) * 0
        out[i:i + bs], zi = signal.lfilter(b, a, x[i:i + bs], zi=zi)
    return out

def saw(f, t, ph=0): return 2 * ((f * t + ph) % 1) - 1
def sq(f, t, duty=0.5): return np.where(((f * t) % 1) < duty, 1.0, -1.0)
def tri(f, t): return 2 * np.abs(saw(f, t)) - 1
def sine(f, t): return np.sin(2 * np.pi * f * t)
def noise(n): return rng.standard_normal(n)

def reverb_ir(dur=2.2, decay=3.0, bright=6000, stereo=True):
    n = int(dur * SR); t = np.arange(n) / SR
    chans = []
    for c in range(2 if stereo else 1):
        ir = noise(n) * np.exp(-decay * t)
        ir = lp(ir, bright, 1); ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
        chans.append(ir / np.sqrt(np.sum(ir ** 2)))
    return chans

_IR = None
def reverb(x, wet=0.25, dur=2.2, decay=3.0):
    global _IR
    if _IR is None or len(_IR[0]) != int(dur * SR): _IR = reverb_ir(dur, decay)
    mono = x if x.ndim == 1 else x.mean(axis=1)
    L = signal.fftconvolve(mono, _IR[0])[: len(mono)]; R = signal.fftconvolve(mono, _IR[1])[: len(mono)]
    dry = np.stack([mono, mono], 1) if x.ndim == 1 else x
    return dry * (1 - wet) + np.stack([L, R], 1) * wet

def delay(x, t=0.375, fb=0.35, mix=0.25):
    d = int(t * SR); y = x.copy()
    for k in range(1, 6):
        g = fb ** k
        if g < 0.02: break
        y[d * k:] += x[: len(x) - d * k] * g * mix
    return y

def pan(x, p):  # p en [-1,1]
    l = np.cos((p + 1) * np.pi / 4); r = np.sin((p + 1) * np.pi / 4)
    return np.stack([x * l, x * r], 1)

def place(buf, x, start):
    s = int(start * SR)
    if s >= len(buf): return
    e = min(len(buf), s + len(x)); buf[s:e] += x[: e - s]

def norm(x, peak=0.9):
    m = np.max(np.abs(x)) + 1e-9; return x * (peak / m)

# ---------------------------------------------------------------- instrumentos
def inst_supersaw(notes, dur, cutoff=2400, voices=5, detune=0.12, a=0.4, r=0.6):
    t = t_axis(dur); out = np.zeros(len(t))
    for n in notes:
        f = midi(n)
        for v in range(voices):
            dt = (v - (voices - 1) / 2) * detune / voices
            out += saw(f * 2 ** (dt / 12), t, ph=rng.random())
    out = lp(out, cutoff) * adsr(len(t), a, 0.3, 0.8, r) / (len(notes) * voices) * 1.6
    return out

def inst_pluck(n, dur=0.25, bright=4000, wave="saw"):
    t = t_axis(dur); f = midi(n)
    x = saw(f, t) if wave == "saw" else sq(f, t, 0.3) if wave == "sq" else tri(f, t)
    env = np.exp(-t * 14)
    return sweep_lp(x * env, bright, 400, 16) * 0.6

def inst_fm(n, dur=0.8, ratio=1.0, index=2.5, decay=4.0, idx_decay=6.0):
    t = t_axis(dur); f = midi(n)
    mod = index * np.exp(-t * idx_decay) * np.sin(2 * np.pi * f * ratio * t)
    x = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * decay)
    att = min(len(t), int(0.004 * SR)); x[:att] *= np.linspace(0, 1, att)
    return x * 0.5

def epiano(n, dur=1.2): return inst_fm(n, dur, ratio=1.0, index=1.8, decay=2.2, idx_decay=4) + 0.3 * inst_fm(n + 12, dur, 14, 0.4, 6, 20)
def marimba(n, dur=0.6): return inst_fm(n, dur, ratio=4.0, index=1.2, decay=9, idx_decay=30)
def bell(n, dur=2.0): return inst_fm(n, dur, ratio=3.5, index=3.0, decay=2.0, idx_decay=2.5)
def musicbox(n, dur=1.5): return inst_fm(n, dur, ratio=5.0, index=1.0, decay=3.5, idx_decay=8) + 0.4 * inst_fm(n + 12, dur, 1, 0.2, 5, 5)
def chip(n, dur=0.15, duty=0.25):
    t = t_axis(dur); return sq(midi(n), t, duty) * adsr(len(t), 0.002, 0.05, 0.6, 0.03) * 0.25

def bass(n, dur, kind="saw", cutoff=500):
    t = t_axis(dur); f = midi(n)
    if kind == "sub": x = sine(f, t) + 0.2 * sine(2 * f, t)
    elif kind == "sq": x = sq(f, t, 0.5)
    elif kind == "808":
        fenv = f * (1 + 1.5 * np.exp(-t * 30)); x = np.sin(2 * np.pi * np.cumsum(fenv) / SR); x = np.tanh(1.6 * x)
        return x * np.exp(-t * 1.6) * 0.8
    else: x = saw(f, t)
    return lp(x, cutoff) * adsr(len(t), 0.005, 0.1, 0.8, 0.05) * 0.7

# ---------------------------------------------------------------- batería
def kick(dur=0.45, punch=1.0):
    t = t_axis(dur); f = 48 + 110 * np.exp(-t * 35)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    click = lp(noise(len(t)), 5000) * np.exp(-t * 300) * 0.3
    return np.tanh((x + click) * 1.5 * punch) * 0.9

def snare(dur=0.25):
    t = t_axis(dur); tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)
    nz = bp(noise(len(t)), 1500, 9000) * np.exp(-t * 18)
    return (tone * 0.5 + nz * 0.8) * 0.7

def clap(dur=0.3):
    t = t_axis(dur); env = np.zeros(len(t))
    for o in (0, 0.01, 0.02, 0.032):
        s = int(o * SR); env[s:] += np.exp(-(t[: len(t) - s]) * 60)
    return bp(noise(len(t)), 900, 6000) * env * 0.5

def hat(dur=0.06, open_=False):
    d = 0.3 if open_ else dur; t = t_axis(d)
    return hp(noise(len(t)), 7000) * np.exp(-t * (12 if open_ else 70)) * 0.35

def shaker(dur=0.08):
    t = t_axis(dur); return bp(noise(len(t)), 4000, 12000) * np.sin(np.pi * t / dur) ** 2 * 0.25

def rim(dur=0.08):
    t = t_axis(dur); return (np.sin(2 * np.pi * 900 * t) + bp(noise(len(t)), 2000, 6000) * 0.5) * np.exp(-t * 60) * 0.4

def chipnoise(dur=0.08):
    t = t_axis(dur); x = np.sign(noise(len(t))); x = np.repeat(x[::8], 8)[: len(t)]
    return x * np.exp(-t * 40) * 0.2

# ---------------------------------------------------------------- estilos
STYLES = {
    # bpm, progresión, octava, patrón de batería, timbres
    "synthwave": dict(bpm=108, prog=["Am", "F", "C", "G"], drums="four", bass="saw8", pad="supersaw", lead="arp_saw", sw=0.0),
    "electro": dict(bpm=124, prog=["Em", "C", "G", "D"], drums="four", bass="saw8", pad="supersaw", lead="arp_sq", sw=0.0),
    "tension": dict(bpm=92, prog=["Dm", "Dm", "Bb", "A"], drums="tension", bass="sub_pulse", pad="dark", lead="ticks", sw=0.0),
    "tropical": dict(bpm=100, prog=["Dm9", "Gm7", "Cmaj7", "Fmaj7"], drums="house", bass="sub_off", pad="soft", lead="marimba", sw=0.08),
    "noir": dict(bpm=84, prog=["Dm9", "G7", "Cmaj7", "A7"], drums="boombap", bass="walk", pad="epiano", lead="none", sw=0.18),
    "dembow": dict(bpm=96, prog=["Am", "F", "C", "G"], drums="dembow", bass="808", pad="stab", lead="bell_hook", sw=0.0),
    "chip": dict(bpm=140, prog=["C", "Am", "F", "G"], drums="chip", bass="chip", pad="none", lead="chip_arp", sw=0.0),
    "nature": dict(bpm=72, prog=["Fmaj7", "Em7", "Dm9", "Cmaj9"], drums="soft", bass="sub_long", pad="soft", lead="marimba_slow", sw=0.1),
    "mystery": dict(bpm=76, prog=["Am", "F", "Dm", "E"], drums="sparse", bass="sub_long", pad="dark", lead="musicbox", sw=0.0),
    "synthpop": dict(bpm=118, prog=["F", "G", "Em", "Am"], drums="four", bass="saw8", pad="supersaw", lead="arp_saw", sw=0.0),
    # estilos de VIDEO_EXTRA (una época por capítulo)
    "storm": dict(bpm=70, prog=["Dm", "Bb", "Gm", "A"], drums="none", bass="sub_long", pad="dark", lead="none", sw=0.0),
    "swing30": dict(bpm=124, prog=["Cmaj7", "A7", "Dm7", "G7"], drums="brush", bass="walk", pad="epiano", lead="vibes", sw=0.22),
    "seventies": dict(bpm=84, prog=["Fmaj7", "Em7", "Dm7", "Cmaj7"], drums="soft", bass="sub_long", pad="epiano", lead="none", sw=0.1),
    "trap26": dict(bpm=140, prog=["Am", "F", "C", "E"], drums="trap", bass="808", pad="dark", lead="bell_hook", sw=0.0),
}

def drum_pattern(kind):
    """Devuelve dict instrumento -> lista de posiciones en semicorcheas (0..15)."""
    if kind == "four": return {"k": [0, 4, 8, 12], "c": [4, 12], "h": [2, 6, 10, 14], "s": list(range(16))}
    if kind == "house": return {"k": [0, 4, 8, 12], "c": [4, 12], "h": [2, 6, 10, 14], "sh": list(range(0, 16, 2)), "r": [3, 11]}
    if kind == "dembow": return {"k": [0, 4, 8, 12], "sn": [3, 6, 11, 14], "h": [0, 2, 4, 6, 8, 10, 12, 14]}
    if kind == "boombap": return {"k": [0, 7, 10], "sn": [4, 12], "h": [0, 2, 4, 6, 8, 10, 12, 14]}
    if kind == "tension": return {"k": [0, 8], "r": [4, 12], "h": [2, 6, 10, 14]}
    if kind == "chip": return {"k": [0, 8], "cn": [4, 12], "h": [2, 6, 10, 14]}
    if kind == "soft": return {"sh": [0, 4, 8, 12], "r": [6, 14]}
    if kind == "sparse": return {"k": [0], "r": [12]}
    if kind == "brush": return {"k": [0, 8], "br": [4, 12], "rd": [0, 4, 6, 8, 12, 14]}
    if kind == "trap": return {"k": [0, 7, 10], "c": [8], "h": [0, 2, 4, 6, 8, 10, 12, 13, 14, 15]}
    return {}

def brush(dur=0.22):
    t = t_axis(dur); return bp(noise(len(t)), 1800, 9000) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.6 * np.exp(-t * 9) * 0.35

def ride(dur=0.5):
    t = t_axis(dur); tone = inst_fm(98, dur, ratio=2.76, index=2.0, decay=6, idx_decay=8)
    return (hp(noise(len(t)), 6000) * np.exp(-t * 14) * 0.18 + tone * 0.12)

def vibes(n, dur=1.4):
    t = t_axis(dur); return inst_fm(n, dur, ratio=4.0, index=0.7, decay=2.2, idx_decay=12) * (1 + 0.25 * np.sin(2 * np.pi * 5.5 * t))

DRUMS = {"k": lambda: kick(), "c": lambda: clap(), "sn": lambda: snare(), "h": lambda: hat(), "s": lambda: shaker() * 0.5,
         "sh": lambda: shaker(), "r": lambda: rim(), "cn": lambda: chipnoise(), "br": lambda: brush(), "rd": lambda: ride()}

def compose(style, duration, energy=None, seed=1, key_shift=0):
    """Genera una pista estéreo original de `duration` segundos.
    energy: lista de (tiempo, nivel 0..3) que activa capas a lo largo del vídeo.
    """
    global rng
    rng = np.random.default_rng(seed)
    S = STYLES[style]; bpm = S["bpm"]; beat = 60 / bpm; bar = beat * 4; step = beat / 4
    n = int(duration * SR) + SR; mix = {k: np.zeros(n) for k in ("drums", "bass", "pad", "lead")}
    energy = energy or [(0, 2)]
    def lvl(t):
        v = energy[0][1]
        for tt, ll in energy:
            if t >= tt: v = ll
        return v
    prog = [chord(c, 3) for c in S["prog"]]; prog = [[x + key_shift for x in c] for c in prog]
    pat = drum_pattern(S["drums"]); dcache = {k: DRUMS[k]() for k in pat}
    nbars = int(duration / bar) + 2
    melody_seed = np.random.default_rng(seed + 11)
    hook = [melody_seed.integers(0, 4) for _ in range(8)]  # motivo fijo, repetido → identidad
    for b in range(nbars):
        t0 = b * bar; L = lvl(t0); ch = prog[b % len(prog)]
        if t0 > duration + bar: break
        # PAD
        if S["pad"] != "none" and L >= 0:
            if S["pad"] == "supersaw": x = inst_supersaw([c + 12 for c in ch], bar + 0.5, cutoff=1400 + 500 * L)
            elif S["pad"] == "dark": x = inst_supersaw([c for c in ch], bar + 0.8, cutoff=700, voices=3, a=0.8, r=0.9) * 0.8
            elif S["pad"] == "soft": x = inst_supersaw([c + 12 for c in ch], bar + 0.6, cutoff=1100, voices=3, a=0.6) * 0.7
            elif S["pad"] == "epiano":
                x = np.zeros(int((bar + 1.2) * SR))
                for i, c in enumerate(ch):
                    place(x, epiano(c + 12, 1.6) * 0.5, 0.012 * i); place(x, epiano(c + 12, 1.0) * 0.3, beat * 2.5 + 0.01 * i)
            elif S["pad"] == "stab":
                x = np.zeros(int((bar + 0.5) * SR))
                for pos in (0, 3, 6, 10, 14):
                    st = inst_supersaw([c + 12 for c in ch], step * 1.2, cutoff=3000, voices=3, a=0.003, r=0.05); place(x, st * 0.8, pos * step)
            else: x = np.zeros(1)
            place(mix["pad"], x * (0.5 if L == 0 else 0.65), t0)
        # BAJO
        if L >= 1 and S["bass"] != "none":
            root = ch[0] - 12
            if S["bass"] == "saw8":
                for i in range(8): place(mix["bass"], bass(root, beat / 2 * 0.9, "saw", 380 + 120 * L), t0 + i * beat / 2)
            elif S["bass"] == "sub_pulse":
                for i in range(4): place(mix["bass"], bass(root, beat * 0.8, "sub"), t0 + i * beat)
            elif S["bass"] == "sub_off":
                for i in range(4): place(mix["bass"], bass(root, beat * 0.45, "sub") * 1.1, t0 + i * beat + beat / 2)
            elif S["bass"] == "sub_long": place(mix["bass"], bass(root, bar * 0.98, "sub") * 0.9, t0)
            elif S["bass"] == "walk":
                walk = [root, root + 7, root + 12 if b % 2 else root + 10, root + 5]
                for i, wn in enumerate(walk): place(mix["bass"], bass(wn, beat * 0.9, "sub", 800), t0 + i * beat + (S["sw"] * step if i % 2 else 0))
            elif S["bass"] == "808":
                for pos in (0, 6, 8): place(mix["bass"], bass(root, beat * 1.4, "808"), t0 + pos * step)
            elif S["bass"] == "chip":
                for i in range(8): place(mix["bass"], chip(root + (12 if i % 2 else 0), step * 1.8, 0.5) * 1.6, t0 + i * beat / 2)
        # BATERÍA
        if L >= 2:
            for inst, poss in pat.items():
                for p in poss:
                    sw = S["sw"] * step if p % 2 else 0
                    g = 1.0 if inst in ("k", "sn", "c") else 0.8
                    if inst == "h" and L < 3 and p % 4 == 2 and S["drums"] == "four": g *= 0.6
                    place(mix["drums"], dcache[inst] * g, t0 + p * step + sw)
            if b % 8 == 7 and S["drums"] in ("four", "house", "dembow"):  # relleno cada 8 compases
                for p in (12, 13, 14, 15): place(mix["drums"], snare() * 0.5, t0 + p * step)
        elif L == 1 and S["drums"] in ("four", "house", "dembow", "chip", "trap"):
            for p in pat.get("h", []): place(mix["drums"], dcache["h"] * 0.5, t0 + p * step)
        elif L == 1 and S["drums"] == "brush":
            for p in pat["rd"]: place(mix["drums"], dcache["rd"] * 0.6, t0 + p * step + (S["sw"] * step if p % 2 else 0))
        # LEAD
        if L >= 3 or (L >= 2 and S["lead"] in ("marimba", "musicbox", "marimba_slow", "ticks", "vibes")):
            ld = S["lead"]
            tones = [c + 24 for c in ch] + [ch[0] + 36]
            if ld in ("arp_saw", "arp_sq"):
                for i in range(16):
                    nn = tones[[0, 1, 2, 3, 2, 1, 0, 2][i % 8] % len(tones)]
                    place(mix["lead"], inst_pluck(nn, step * 1.5, 3500, "saw" if ld == "arp_saw" else "sq") * 0.5, t0 + i * step)
            elif ld == "marimba":
                for i, p in enumerate((0, 3, 6, 8, 11, 14)):
                    place(mix["lead"], marimba(tones[(hook[i % 8] + i) % len(tones)]) * 0.7, t0 + p * step + (S["sw"] * step if p % 2 else 0))
            elif ld == "marimba_slow":
                for i, p in enumerate((0, 6, 10)): place(mix["lead"], marimba(tones[(hook[i] + b) % len(tones)], 1.0) * 0.6, t0 + p * step)
            elif ld == "musicbox":
                for i, p in enumerate((0, 4, 6, 10, 12)): place(mix["lead"], musicbox(tones[(hook[i % 8] + i) % len(tones)] + 12) * 0.5, t0 + p * step)
            elif ld == "bell_hook":
                for i, p in enumerate((0, 3, 6, 10)): place(mix["lead"], bell(tones[hook[i] % len(tones)] + 12, 0.9) * 0.35, t0 + p * step)
            elif ld == "chip_arp":
                for i in range(16): place(mix["lead"], chip(tones[i % 4] + 12, step * 0.9, 0.25), t0 + i * step)
            elif ld == "vibes":
                for i, p in enumerate((0, 6, 8, 14)):
                    place(mix["lead"], vibes(tones[(hook[i % 8] + i + b) % len(tones)] + 12, 1.2) * 0.45, t0 + p * step + (S["sw"] * step if p % 2 else 0))
            elif ld == "ticks":
                for i in range(16): place(mix["lead"], rim() * (0.35 if i % 4 else 0.6), t0 + i * step)
    # mezcla y espacialización
    drums = mix["drums"]; bassx = mix["bass"]; pad = mix["pad"]; lead = mix["lead"]
    # sidechain del kick sobre pad y bajo (bombeo suave)
    if "k" in pat:
        env = np.ones(n)
        for b in range(nbars):
            for p in pat["k"]:
                s = int((b * bar + p * step) * SR); e = min(n, s + int(0.18 * SR))
                if s < n: env[s:e] = np.minimum(env[s:e], 0.55 + 0.45 * np.linspace(0, 1, e - s) ** 2)
        pad = pad * env; bassx = bassx * (0.6 + 0.4 * env)
    # bajo: armónicos para que se oiga en altavoces de móvil + control del subgrave
    bassx = hp(bassx, 35) ; bassx = bassx + 0.35 * np.tanh(bp(bassx, 120, 900) * 4)
    padm = hp(pad, 160); leadm = hp(lead, 200)
    out = pan(hp(drums, 30), 0) * 0.8 + pan(bassx, 0) * 0.42
    out += np.stack([padm, np.roll(padm, int(0.012 * SR))], 1) * 1.15
    if lead.any(): out += reverb(delay(leadm, beat * 0.75, 0.35, 0.3), 0.3) * 1.1
    out = reverb(out, 0.12, 1.6, 3.5)
    out = np.tanh(out * 1.2) / 1.2
    out = out[: int(duration * SR)]
    # fundido de entrada/salida
    fi = int(0.05 * SR); fo = int(min(3.0, duration / 4) * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]; out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return norm(out, 0.8)

# ---------------------------------------------------------------- efectos de sonido
def sfx(name, **k):
    d = k.get("dur", None)
    if name == "whoosh":
        d = d or 0.55; t = t_axis(d); x = noise(len(t))
        env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
        lo = 300 if not k.get("down") else 2500; hi = 4000 if not k.get("down") else 300
        y = sweep_lp(x, lo, hi, 32) * env
        return np.stack([y * np.linspace(1, 0.3, len(t)), y * np.linspace(0.3, 1, len(t))], 1) * 0.7
    if name == "impact":
        d = d or 1.6; t = t_axis(d); f = 40 + 80 * np.exp(-t * 12)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3) + lp(noise(len(t)), 1800) * np.exp(-t * 14) * 0.6
        return reverb(np.tanh(x * 2) * 0.8, 0.35)
    if name == "hit":
        x = kick(0.4, 1.4) * 0.8; x[: int(0.2 * SR)] += snare(0.2) * 0.3; return pan(x, 0)
    if name == "tick":
        t = t_axis(0.03); return pan(np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300) * 0.4, k.get("p", 0))
    if name == "flap":  # tablero de paletas
        n_ = k.get("n", 8); out = np.zeros(int((0.035 * n_ + 0.1) * SR))
        for i in range(n_):
            t = t_axis(0.02); c = (bp(noise(len(t)), 1500, 7000) * np.exp(-t * 400)) * (0.5 + 0.5 * rng.random())
            place(out, c, i * 0.035 + rng.random() * 0.006)
        return pan(out * 0.8, k.get("p", 0))
    if name == "type":
        t = t_axis(0.05); x = bp(noise(len(t)), 1800, 6000) * np.exp(-t * 180) + np.sin(2 * np.pi * 160 * t) * np.exp(-t * 90) * 0.4
        return pan(x * 0.6, k.get("p", 0))
    if name == "typing":
        n_ = k.get("n", 10); out = np.zeros(int((0.09 * n_ + 0.2) * SR))
        for i in range(n_): place(out, sfx("type")[:, 0] * (0.6 + 0.5 * rng.random()), i * (0.07 + 0.04 * rng.random()))
        return pan(out, 0)
    if name == "stamp":
        t = t_axis(0.5); x = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 18) + lp(noise(len(t)), 3000) * np.exp(-t * 40) * 0.7
        return reverb(x * 0.9, 0.15)
    if name == "glitch":
        d = d or 0.35; n_ = int(d * SR); x = np.zeros(n_); pos = 0
        while pos < n_:
            L = int(rng.integers(400, 3000)); seg = np.sign(noise(L)) * rng.random() * 0.6
            seg = np.repeat(seg[:: int(rng.integers(4, 40))], int(rng.integers(4, 40)))[:L]
            x[pos:pos + len(seg)] = seg[: n_ - pos]; pos += L + int(rng.integers(0, 2000))
        return pan(lp(x, 6000) * 0.5, 0)
    if name == "riser":
        d = d or 2.0; t = t_axis(d); f = 200 * (8 ** (t / d))
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + sweep_lp(noise(len(t)), 300, 9000, 40) * 0.6
        return reverb(x * (t / d) ** 2 * 0.8, 0.3)
    if name == "ding":
        x = bell(84, 1.8) + bell(91, 1.8) * 0.5; return reverb(x * 0.7, 0.3)
    if name == "pop":
        t = t_axis(0.12); f = 400 + 900 * t / 0.12; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)
        return pan(x * 0.5, k.get("p", 0))
    if name == "buzz":
        t = t_axis(d or 0.4); x = lp(sq(110, t), 1500) * adsr(len(t), 0.005, 0.05, 0.8, 0.05) * 0.35
        return pan(x, 0)
    if name == "paper":
        d = d or 0.4; t = t_axis(d); x = bp(noise(len(t)), 800, 7000) * np.sin(np.pi * t / d) ** 1.5 * 0.4
        return pan(x, k.get("p", 0))
    if name == "shutter":
        t = t_axis(0.15); x = bp(noise(len(t)), 1000, 8000) * (np.exp(-t * 80) + 0.6 * np.exp(-np.maximum(t - 0.06, 0) * 90) * (t > 0.06))
        return pan(x * 0.7, 0)
    if name == "pin":
        t = t_axis(0.5); x = np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 14) * 0.3 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 20) * 0.2
        return reverb(x, 0.25)
    if name == "alarm":
        t = t_axis(d or 0.8); x = sq(880, t, 0.5) * (np.sin(2 * np.pi * 6 * t) > 0) * 0.15; return pan(lp(x, 3000), 0)
    if name == "coin":
        out = np.zeros(int(0.5 * SR)); place(out, chip(83, 0.08, 0.5) * 2, 0); place(out, chip(88, 0.35, 0.5) * 2, 0.08); return pan(out, 0)
    if name == "snap":  # mordida de caimán (logo sonoro)
        t = t_axis(0.35); x = hp(noise(len(t)), 2500) * np.exp(-t * 120) * 0.9 + np.sin(2 * np.pi * (90 + 120 * np.exp(-t * 50)) * t) * np.exp(-t * 16)
        return reverb(np.tanh(x * 1.5) * 0.8, 0.2)
    if name == "logo":  # sintonía SAL Y ASFALTO: auto que pasa (Doppler) + ola + acorde de piano eléctrico
        n = int(2.6 * SR); st = np.zeros((n, 2))
        d = 1.2; t = t_axis(d); env = np.exp(-((t - 0.55) / 0.2) ** 2)
        f = 150 * (1.3 - 0.55 * np.tanh((t - 0.55) * 6))
        car = (bp(noise(len(t)), 250, 2500) * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 + np.sin(2 * np.pi * np.cumsum(2 * f) / SR) * 0.12) * env
        st[:len(car), 0] += car * np.linspace(1.0, 0.15, len(car)); st[:len(car), 1] += car * np.linspace(0.15, 1.0, len(car))
        tw = t_axis(1.6); wave = sweep_lp(noise(len(tw)), 300, 2200, 24) * np.sin(np.pi * np.clip(tw / 1.6, 0, 1)) ** 2 * 0.35
        place(st, pan(wave, 0), 0.75)
        ch = np.zeros(int(2.0 * SR))
        for i, nn in enumerate((53, 57, 60, 64, 67)): place(ch, epiano(nn + 12, 1.8) * 0.45, 0.018 * i)
        place(ch, bell(84, 1.6) * 0.25, 0.1)
        place(st, pan(ch, 0), 1.05)
        return reverb(st * 0.9, 0.25)
    if name == "bird":
        t = t_axis(0.25); f = 2800 + 1600 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 6)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.25) ** 2 * 0.15
        return reverb(pan(x, k.get("p", 0.3)), 0.4)
    if name == "water":
        d = d or 2.0; t = t_axis(d); x = sweep_lp(noise(len(t)), 600, 900, 8) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)) * 0.2
        return pan(x, 0)
    if name == "heartbeat":
        out = np.zeros(int(1.0 * SR)); place(out, kick(0.3, 0.6) * 0.7, 0); place(out, kick(0.3, 0.5) * 0.5, 0.22); return pan(lp(out, 300), 0)
    if name == "seal":  # lacre que se rompe
        t = t_axis(0.3); x = bp(noise(len(t)), 500, 4000) * np.exp(-t * 25) * (1 + np.sign(noise(len(t))) * 0.3)
        return reverb(pan(x * 0.7, 0), 0.2)
    if name == "wind":  # viento de tormenta: ruido filtrado con ráfagas
        d = d or 4.0; t = t_axis(d); x = noise(len(t)); g = 0.55 + 0.45 * np.sin(2 * np.pi * 0.35 * t + rng.random() * 6) * np.sin(2 * np.pi * 0.13 * t)
        y = sweep_lp(x, 500, 1400, 48) * g * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5
        return np.stack([y, np.roll(y, int(0.03 * SR))], 1) * 0.5
    if name == "rain":
        d = d or 4.0; n_ = int(d * SR); x = hp(noise(n_), 2500) * 0.12
        drops = (rng.random(n_) < 0.0016) * rng.standard_normal(n_) * 2.5; x += hp(lp(drops, 6000), 900) * 0.4
        env = np.sin(np.pi * np.clip(np.arange(n_) / n_, 0, 1)) ** 0.3
        return np.stack([x * env, np.roll(x, 113) * env], 1) * 0.6
    if name == "thunder":
        d = d or 3.0; t = t_axis(d); x = lp(noise(len(t)), 160) * 3.5 * np.exp(-t * 1.3) + lp(noise(len(t)), 900) * np.exp(-t * 6) * 0.9
        return reverb(np.tanh(x) * 0.9, 0.4)
    if name == "brush":  # brochazo de pintura
        d = d or 0.7; t = t_axis(d); env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
        y = bp(noise(len(t)), 700, 5000) * env * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)) * 0.45
        return np.stack([y * np.linspace(1, 0.4, len(t)), y * np.linspace(0.4, 1, len(t))], 1)
    if name == "neon":  # tubo de neón que se enciende: chispazos + zumbido
        d = d or 1.4; t = t_axis(d); out = np.zeros(len(t))
        for o in (0.0, 0.09, 0.16, 0.31):
            s = int(o * SR); e = min(len(t), s + int(0.03 * SR)); out[s:e] += hp(noise(e - s), 2000) * 0.5
        hum = (np.sin(2 * np.pi * 120 * t) * 0.25 + np.sin(2 * np.pi * 240 * t) * 0.1 + sq(120, t, 0.5) * 0.03) * np.clip((t - 0.32) * 4, 0, 1) * np.exp(-np.maximum(t - 0.8, 0) * 3)
        return pan(out + hum, k.get("p", 0)) * 0.8
    if name == "tune":  # dial de radio que cambia de época
        d = d or 1.1; t = t_axis(d); f = 900 + 2600 * (t / d) ** 2
        whistle = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.05 * np.sin(np.pi * t / d)
        st = bp(noise(len(t)), 900, 6000) * (0.25 + 0.2 * np.sin(2 * np.pi * 11 * t)) * np.sin(np.pi * t / d) ** 0.7
        return pan(whistle + st * 0.5, 0)
    if name == "tv_on":  # encendido de tele de tubo
        t = t_axis(0.9); x = np.sin(2 * np.pi * 7800 * t) * 0.02 * np.exp(-t * 2) + lp(noise(len(t)), 300) * np.exp(-t * 14) * 0.9
        x[: int(0.02 * SR)] += hp(noise(int(0.02 * SR)), 1500) * 0.6
        return pan(x / (np.abs(x).max() + 1e-9) * 0.6, 0)
    if name == "rumble":  # maquinaria pesada / demolición
        d = d or 2.5; t = t_axis(d); eng = sq(28 + 3 * np.sin(2 * np.pi * 0.7 * t), t, 0.3) * 0.15
        x = lp(eng + noise(len(t)) * 0.5, 300) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.5
        return reverb(np.tanh(x * 2) * 0.6, 0.2)
    if name == "phone":  # notificación genérica (dos tonos propios)
        out = np.zeros(int(0.5 * SR)); place(out, inst_fm(88, 0.25, 2.0, 1.0, 12, 20) * 0.6, 0); place(out, inst_fm(95, 0.3, 2.0, 1.0, 10, 20) * 0.6, 0.11)
        return pan(out, k.get("p", 0.2))
    if name == "chime":  # revelación suave
        out = np.zeros(int(2.4 * SR))
        for i, nn in enumerate((76, 79, 83, 88)): place(out, bell(nn, 2.0) * 0.22, i * 0.07)
        return reverb(out, 0.45)
    raise KeyError(name)

def to_stereo(x): return x if x.ndim == 2 else np.stack([x, x], 1)

# ---------------------------------------------------------------- tratamiento de voz y mezcla
def voice_chain(v, sr_in=44100):
    """Voz limpia: remuestreo a 48 kHz y filtro de graves. Sin compresión rápida ni reverberación
    (ambas añadían aspereza); el control de picos lo hace el limitador final."""
    from math import gcd
    g = gcd(SR, int(sr_in)); v = signal.resample_poly(v, SR // g, int(sr_in) // g)
    sos = signal.butter(2, 70 / (SR / 2), "high", output="sos"); v = signal.sosfiltfilt(sos, v)
    return np.stack([v, v], 1)

def duck_envelope(voice_st, depth=0.32, attack=0.08, release=0.45):
    m = np.abs(voice_st).mean(axis=1)
    env = signal.lfilter([0.01], [1, -0.99], m)
    active = (env > 0.01).astype(float)
    # suavizado asimétrico
    out = np.zeros_like(active); a = 1 / (attack * SR); r = 1 / (release * SR); cur = 0.0
    for i in range(0, len(active), 240):
        target = active[i]
        cur = cur + (target - cur) * min(1, (a if target > cur else r) * 240)
        out[i:i + 240] = cur
    return 1 - (1 - depth) * out  # 1 = sin voz, depth = con voz

def limiter(x, ceiling=0.84, win_ms=10.0):
    """Limitador con anticipación (look-ahead): reduce solo los picos, con una curva de ganancia suave.
    Mínimo deslizante + media deslizante de la misma ventana ⇒ el pico nunca supera el techo y no hay
    recorte ni distorsión de la forma de onda."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    peak = np.abs(x).max(axis=1) if x.ndim == 2 else np.abs(x)
    g = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    W = int(win_ms * SR / 1000) | 1
    g = minimum_filter1d(g, size=W, mode="nearest")
    g = uniform_filter1d(g, size=W, mode="nearest")
    g = uniform_filter1d(g, size=W, mode="nearest")  # segunda pasada: transiciones aún más suaves
    g = np.minimum(g, 1.0)
    y = x * (g[:, None] if x.ndim == 2 else g)
    pk = np.abs(y).max()
    if pk > ceiling: y *= ceiling / pk
    return y, g


def master(mixst, target_lufs=-14.0):
    import pyloudnorm as pyln
    meter = pyln.Meter(SR); lufs = meter.integrated_loudness(mixst)
    y = mixst * 10 ** ((target_lufs - lufs) / 20)
    y, g = limiter(y)
    # el limitador baja un poco la sonoridad: se corrige una vez
    l2 = meter.integrated_loudness(y)
    if abs(l2 - target_lufs) > 0.3:
        y, g = limiter(y * 10 ** ((target_lufs - l2) / 20))
    master.last_gr = dict(max_db=float(-20 * np.log10(g.min() + 1e-9)), pct_over_1db=float((g < 0.891).mean() * 100))
    return y, lufs
