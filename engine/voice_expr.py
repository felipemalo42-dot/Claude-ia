"""Elegir la toma más animada sin cambiar la voz.

Chatterbox genera cada frase de forma distinta según la semilla: con los mismos ajustes, unas tomas salen
planas y otras con más euforia (tono más alto y más variado, más energía, más ritmo). En vez de forzar la
expresividad del modelo o acelerar el audio (lo que suena robótico), se generan varias tomas de cada frase
con la voz de siempre y se elige la más animada entre las que se entienden perfecto y no tienen saltos raros.

Rasgos por toma (tono en semitonos respecto a 205 Hz, la voz de la narradora):
  med  tono medio (más alto = más entusiasmo)        iqr  variación del tono (rango intercuartílico)
  rng  rango del tono (percentiles 5-95)             dyn  dinámica de volumen en las partes con voz (dB)
  syl  sílabas por segundo                           jps  saltos bruscos de tono por segundo (artefacto)
  gap  pausa más larga entre palabras (s)
"""
import re
import numpy as np

W = dict(med=1.2, iqr=1.0, rng=0.7, dyn=0.6, syl=0.5)   # pesos de la puntuación de euforia
MAX_JPS, MAX_GAP = 0.5, 1.0                              # límites para descartar tomas raras (p95 de las pruebas)

def feats(x, sr, times, text):
    import librosa
    f0, vf, _ = librosa.pyin(x, fmin=120, fmax=450, sr=sr, frame_length=1024, hop_length=240)
    ok = vf & ~np.isnan(f0)
    if ok.sum() < 10: return None
    st = 12 * np.log2(f0[ok] / 205.0)
    rms = librosa.feature.rms(y=x, frame_length=1024, hop_length=240)[0][: len(ok)][ok]; db = 20 * np.log10(rms + 1e-6)
    sp = (times[-1][1] - times[0][0]) if times else len(x) / sr
    gaps = [b[0] - a[1] for a, b in zip(times, times[1:])] if times else [0.0]
    return dict(med=float(np.median(st)), iqr=float(np.percentile(st, 75) - np.percentile(st, 25)),
                rng=float(np.percentile(st, 95) - np.percentile(st, 5)), dyn=float(np.percentile(db, 95) - np.percentile(db, 20)),
                syl=len(re.findall(r"[aeiouáéíóúü]+", text.lower())) / max(sp, 0.1),
                jps=int(np.sum(np.abs(np.diff(st)) > 5)) / (len(x) / sr), gap=float(max(gaps) if gaps else 0.0))

def clean(f): return f is not None and f["jps"] <= MAX_JPS and f["gap"] < MAX_GAP

def scores(fs):
    """Puntuación de euforia de cada toma, relativa a las demás tomas de la misma frase."""
    out = np.zeros(len(fs))
    for k, w in W.items():
        v = np.array([f[k] for f in fs]); out += w * (v - v.mean()) / (v.std() + 1e-9)
    return out
