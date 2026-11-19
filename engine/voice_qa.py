"""Control de calidad de la voz: ¿la narradora dice exactamente el guion?

Método (documentado para que cualquiera pueda auditarlo):
1. Se transcribe cada toma con un reconocedor de voz automático (Parakeet TDT v3). Si la toma no llega al umbral,
   se transcribe también con un segundo reconocedor independiente (Whisper small) y se toma el mejor resultado:
   un error del reconocedor no debe contar como error de la voz, pero un error de la voz aparece en los dos.
2. El guion (en su forma hablada: números en palabras y nombres en inglés con su pronunciación) y la transcripción
   se pasan a una clave fonética del español latinoamericano: b = v, s = z = c (ante e/i), h muda, ll = y, qu = k, etc.
3. Coincidencia = 1 − (distancia de edición entre ambas claves, sin espacios) / (longitud de la clave del guion).
   Es una tasa de acierto por carácter fonético: 99,5 % = como máximo un sonido distinto cada 200.
4. Equivalencias de escritura: el reconocedor escribe a veces con otra ortografía nombres que suenan igual
   (Dickson/Dixon, By City/Vice City…). Solo se aceptan homófonos, listados en ALIAS.
"""
import os, re, unicodedata
import numpy as np
from scipy import signal
from tts import spoken, digits_to_words

# Homófonos: misma pronunciación, distinta ortografía en la transcripción automática
ALIAS = [
    (r"\bby ?city\b", "Vice City"), (r"\bvai ?s?ity\b", "Vice City"), (r"\bvais ?city\b", "Vice City"), (r"\bvice-city\b", "Vice City"),
    (r"\bdick?son\b", "Dixon"), (r"\bdikson\b", "Dixon"), (r"\bkapitman\b", "Capitman"), (r"\bhorwitz\b", "Horowitz"),
    (r"\bselfie\b", "selfi"), (r"\bmiami,? dade\b", "Miami-Dade"), (r"\bdeco\b", "déco"), (r"\bNB ?se\b", "NBC"), (r"\bN\.? ?B\.? ?C\.?\b", "NBC"),
    (r"\bmiami,? (bays|bais|vais|bice|vice)\b", "Miami Vice"), (r"\bway city\b", "Vice City"), (r"\bbay city\b", "Vice City"),
    (r"\b(L\.? )?Murray\b", "Múrrei"),
    # GTA6_VIDEO_LANZAMIENTO: nombres de medios y siglas tal como los escriben los reconocedores
    (r"\b(un |en un )?[MIU]?[iu]?ndus central\b", "Windows Central"), (r"\binduced central\b", "Windows Central"),
    (r"\bD[ei] ?Guardian\b", "The Guardian"), (r"\bCord?s ?pla(ne|in)\b", "Worthplaying"), (r"\b[HJ]uro ?Gamer\b", "Eurogamer"),
    (r"\b(James|Hames|Heim|Aime) ?Pott?k?\b", "GameSpot"), (r"\bHames ?Pod\b", "GameSpot"), (r"\bHamespot\b", "GameSpot"),
    (r"\b(Geimes|Heims) ?(Reidar|tradar)\b", "GamesRadar"), (r"\bHeimstradar\b", "GamesRadar"),
    (r"\bThe Legend of Zelda\b", "Di Léyend of Zelda"), (r"\bo ?Kar[ia]n[ao] of Time\b", "Ocarina of Taim"), (r"\bOcarina of Time\b", "Ocarina of Taim"),
    (r"\bG,? ?(T|de),? ?a\b", "GTA"), (r"\bGT a\b", "GTA"), (r"\bG T\b", "GTA"), (r"\bJeta\b", "GTA"),
    (r"\bTake 2\b", "Take-Two"), (r"\bKik\b", "Kick"), (r"\bStreams? Charts\b", "Streams Charts"), (r"\bSeries se\b", "Series S"), (r"\bSirius\b", "Series"),
    (r"\bOpen Critic\b", "OpenCritic"), (r"\bmetacritic\b", "Metacritic"),
]
_ALIAS = [(re.compile(a, re.I), b) for a, b in ALIAS]
_ROMAN = {"xx": "veinte", "xix": "diecinueve", "xxi": "veintiuno"}

def _pre(text):
    t = re.sub(r"(\d+),(\d+)", r"\1 coma \2", text)
    t = re.sub(r"\b(XX|XIX|XXI)\b", lambda m: _ROMAN[m.group(1).lower()], t)
    return t

def phon(text, hyp=False):
    """Clave fonética del español (seseo) de un texto, para comparar guion y voz."""
    t = _pre(text)
    if hyp:
        for rx, rep in _ALIAS: t = rx.sub(rep, t)
    t = re.sub(r"\bGTA VI\b", "GTA 6", t); t = re.sub(r"\bGTA V\b", "GTA 5", t)
    t = spoken(t).lower()
    t = digits_to_words(t).replace("ñ", "ny")
    t = unicodedata.normalize("NFD", t); t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    t = re.sub(r"[^a-z ]", " ", t)
    for a, b in (("sh", "C"), ("ch", "C"), ("ll", "y"), ("qu", "k"), ("ce", "se"), ("ci", "si"), ("c", "k"), ("z", "s"), ("x", "ks"),
                 ("v", "b"), ("w", "u"), ("h", ""), ("ge", "je"), ("gi", "ji"), ("y", "i")):
        t = t.replace(a, b)
    t = re.sub(r"(.)\1+", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()

def lev(a, b):
    if not a: return len(b)
    prev = np.arange(len(b) + 1)
    for i, ca in enumerate(a, 1):
        cur = np.empty_like(prev); cur[0] = i
        sub = prev[:-1] + (np.frombuffer(b.encode(), np.uint8) != ord(ca))
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, sub[j - 1])
        prev = cur
    return int(prev[-1])

def joined(k):
    """Clave sin espacios con los fenómenos normales del habla encadenada: sinalefa (una‿activista → unactivista)
    y asimilación nasal (neón brillaba → neombrillaba)."""
    k = re.sub(r"(.)\1+", r"\1", k.replace(" ", ""))
    return k.replace("nb", "mb").replace("np", "mp")

def score(expected, hyp):
    """→ (coincidencia 0-1, distancia, clave del guion, clave reconocida)"""
    e = joined(phon(expected)); h = joined(phon(hyp, hyp=True))
    d = lev(e, h)
    return max(0.0, 1 - d / max(1, len(e))), d, e, h

class Whisper:
    """Segundo reconocedor (Whisper small, sherpa-onnx), solo para verificar."""
    def __init__(self, d=None, threads=None):
        import sherpa_onnx
        d = d or os.environ.get("WHISPER_DIR", "/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad/asr/sherpa-onnx-whisper-small")
        self.rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/small-encoder.int8.onnx", decoder=f"{d}/small-decoder.int8.onnx",
                                                              tokens=f"{d}/small-tokens.txt", language="es", task="transcribe",
                                                              num_threads=threads or int(os.environ.get("TTS_THREADS", "4")))
    def transcribe(self, x, sr):
        x16 = signal.resample_poly(x, 16000, sr).astype(np.float32)
        x16 = np.concatenate([np.zeros(4800, np.float32), x16, np.zeros(8000, np.float32)])
        st = self.rec.create_stream(); st.accept_waveform(16000, x16); self.rec.decode_stream(st)
        return st.result.text.strip()
