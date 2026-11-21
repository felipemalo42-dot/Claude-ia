"""Limpieza de artefactos de la síntesis de voz que no cambia la duración de la toma (los tiempos del montaje no se mueven).

Zumbido grave: Chatterbox a veces añade, tras el final de una frase, un zumbido o carraspeo grave (50-110 Hz) de hasta 1,5 s.
El alineador lo pega a la última palabra, así que el recorte de la cola no lo ve y el reconocedor de voz tampoco lo cuenta
como palabra. La voz del canal (femenina, tono fundamental ≈ 200 Hz) casi no tiene energía por debajo de 150 Hz; el
zumbido la tiene casi toda ahí, y casi nada por encima de 300 Hz (donde están los formantes de la voz). Por eso:
  · ventana de 20 ms con zumbido y sin voz (nada por encima de 300 Hz) → silencio;
  · ventana con zumbido y con voz a la vez → solo se quita la banda grave (< 150 Hz), que la voz no usa.
Las ganancias se suavizan (15 ms) para no producir chasquidos.
"""
import numpy as np
from scipy.signal import butter, sosfiltfilt

HOP_S = 0.02

def _rms(y, hop):
    m = len(y) // hop
    return np.sqrt(np.mean(y[:m * hop].reshape(m, hop) ** 2, axis=1) + 1e-14)

def _smooth_gain(gf, n, hop, sr):
    """ganancia por ventana → ganancia por muestra, con transiciones de 15 ms"""
    g = np.repeat(gf, hop)
    g = np.concatenate([g, np.full(max(0, n - len(g)), gf[-1] if len(gf) else 1.0)])[:n]
    k = max(1, int(0.015 * sr)); ker = np.ones(k) / k
    return np.convolve(np.pad(g, (k // 2, k - 1 - k // 2), mode="edge"), ker, mode="valid")

def analyse(x, sr):
    x64 = x.astype(np.float64)
    lo = sosfiltfilt(butter(4, 150, "low", fs=sr, output="sos"), x64); hi = x64 - lo
    h3 = x64 - sosfiltfilt(butter(4, 300, "low", fs=sr, output="sos"), x64)
    h5 = x64 - sosfiltfilt(butter(4, 3000, "low", fs=sr, output="sos"), x64)
    hop = int(HOP_S * sr); rl, rh, r3, r5 = _rms(lo, hop), _rms(hi, hop), _rms(h3, hop), _rms(h5, hop)
    ref = np.percentile(rh, 95) + 1e-9; ref3 = np.percentile(r3, 95) + 1e-9; ref5 = np.percentile(r5, 95) + 1e-9
    # voz: energía por encima de 300 Hz audible y mayor que la de la banda grave (en el zumbido queda 15-20 dB por debajo),
    # o una fricativa (s, f, j) por encima de 3 kHz (el zumbido queda 34-47 dB por debajo de la voz en esa banda)
    speech = ((r3 > ref3 * 10 ** (-32 / 20)) & (r3 > rl)) | (r5 > ref5 * 10 ** (-30 / 20))
    core = (rl > 1.5 * rh) & (rl > ref * 10 ** (-40 / 20))
    ext = (rl > 0.7 * rh) & (rl > ref * 10 ** (-55 / 20))
    # zumbido de tono más alto (100-300 Hz): sin nada por encima de 600 Hz (la voz siempre tiene formantes ahí), de al menos
    # 0,25 s y justo después de un hueco de silencio o de otro tramo de zumbido (así no se confunde con una nasal final)
    h6 = x64 - sosfiltfilt(butter(4, 600, "low", fs=sr, output="sos"), x64); r6 = _rms(h6, hop); rt = _rms(x64, hop)
    reft = np.percentile(rt, 95) + 1e-9
    quiet = rt < reft * 10 ** (-33 / 20)
    hum2 = (r6 < 0.1 * rt) & (rt > reft * 10 ** (-40 / 20)) & ~(r5 > ref5 * 10 ** (-30 / 20))
    m = len(rl); segs = []; i = 0
    while i < m:
        if core[i]:
            j = i
            while j < m and (core[j] or (j + 2 < m and core[j + 1:j + 3].any())): j += 1
            a, b = i, j
            while a > 0 and ext[a - 1]: a -= 1
            while b < m and ext[b]: b += 1
            if (j - i) * HOP_S >= 0.06: segs.append((a, b))
            i = max(b, i + 1)
        else: i += 1
    # segundo tipo: tramos de hum2 tras silencio o pegados a un tramo de zumbido grave
    seg1 = list(segs); i = 0
    while i < m:
        if hum2[i]:
            j = i
            while j < m and (hum2[j] or (j + 2 < m and hum2[j + 1:j + 3].any())): j += 1
            if (j - i) * HOP_S >= 0.25:
                w0 = max(0, i - 25); q = quiet[w0:i]
                gap = any(q[k:k + 3].all() for k in range(max(0, len(q) - 2)))
                near = any(a_ - 6 <= j and i <= b_ + 6 for a_, b_ in seg1)
                if gap or near: segs.append((i, j))
            i = j
        else: i += 1
    segs.sort()
    # unir tramos separados por menos de 0,12 s sin voz clara (≥ 80 ms seguidos) y alargar hasta el final de la toma si lo
    # que queda (< 0,3 s) tampoco tiene voz clara: el zumbido a veces trae pequeñas interrupciones o chasquidos
    def clear_speech(k0, k1):
        run = 0
        for k in range(k0, k1):
            run = run + 1 if speech[k] and not hum2[k] else 0
            if run >= 4: return True
        return False
    merged = []
    for a_, b_ in segs:
        if merged and a_ - merged[-1][1] <= 6 and not clear_speech(merged[-1][1], a_): merged[-1] = (merged[-1][0], max(merged[-1][1], b_))
        elif merged and a_ < merged[-1][1]: merged[-1] = (merged[-1][0], max(merged[-1][1], b_))
        else: merged.append((a_, b_))
    if merged and m - merged[-1][1] <= 15 and not clear_speech(merged[-1][1], m): merged[-1] = (merged[-1][0], m)
    segs = merged
    return dict(lo=lo, hi=hi, rl=rl, rh=rh, r3=r3, ref=ref, speech=speech, segs=segs, hop=hop, hum2=hum2)

def drone_clean(x, sr, report=None):
    """Devuelve una copia de x sin el zumbido grave (misma duración)."""
    if len(x) < sr * 0.2: return x
    A = analyse(x, sr)
    if not A["segs"]: return x
    m = len(A["rl"]); g_all = np.ones(m); g_lo = np.ones(m)
    for a, b in A["segs"]:
        sp = A["speech"][a:b] & ~A["hum2"][a:b]   # en un tramo de hum2 no hay formantes: no es voz
        # ráfagas de «voz» de menos de 80 ms dentro del zumbido: chasquidos, no voz
        k = 0
        while k < len(sp):
            if sp[k]:
                e_ = k
                while e_ < len(sp) and sp[e_]: e_ += 1
                if e_ - k < 4 and k > 0 and e_ < len(sp): sp[k:e_] = False
                k = e_
            else: k += 1
        g_all[a:b][~sp] = 0.0          # sin voz: silencio
        g_lo[a:b][sp] = 0.0            # con voz: fuera la banda grave
        if report is not None:
            report.append((round(a * HOP_S, 3), round(b * HOP_S, 3), int((~sp).sum()), int(sp.sum()),
                           round(20 * np.log10(A["rl"][a:b].max() / A["ref"]), 1)))
    n = len(x); hop = A["hop"]
    ga = _smooth_gain(g_all, n, hop, sr); gl = _smooth_gain(g_lo, n, hop, sr)
    y = ga * (A["hi"] + gl * A["lo"])
    return y.astype(x.dtype)
