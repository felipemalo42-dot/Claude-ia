"""Narración en español con Supertonic 3 (voz femenina, 44,1 kHz) + verificación y alineación automáticas.

- Motor de voz: Supertonic 3 (Supertone) vía sherpa-onnx. Código MIT; pesos del modelo bajo licencia
  OpenRAIL-M (uso comercial permitido con restricciones de uso responsable). Voces preestablecidas
  del propio modelo: no imitan a ninguna persona conocida.
- Diccionario de pronunciación: los nombres en inglés se reescriben con ortografía española
  ("Jason" → "Yéison") para que el modelo no cambie a entonación inglesa.
- Síntesis por párrafos (varias frases seguidas) para que el ritmo y las pausas suenen naturales.
- Cada toma se verifica con reconocimiento de voz (Parakeet TDT v3): si el texto reconocido no coincide
  con el guion, se repite con otra semilla. El mismo reconocedor da el tiempo exacto de cada palabra,
  que se usa para subtítulos y para sincronizar la animación.

Modelos (no incluidos en el repositorio por tamaño):
  https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2
  https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2
Variables de entorno: SUPERTONIC_DIR y ALIGN_ASR_DIR (carpetas descomprimidas).
"""
import difflib, os, re, unicodedata, zlib
import numpy as np
from scipy import signal

_SCR = "/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad"
SUPERTONIC_DIR = os.environ.get("SUPERTONIC_DIR", f"{_SCR}/voices/sherpa-onnx-supertonic-3-tts-int8-2026-05-11")
ALIGN_ASR_DIR = os.environ.get("ALIGN_ASR_DIR", f"{_SCR}/asr/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8")
SR = 44100
# Voces de Supertonic 3 (sid 0-4 femeninas F1-F5; 5-9 masculinas M1-M5)
VOICES = {
    "host": dict(sid=2, speed=1.06),      # F3: clara, articulada, estilo locutora
    "copiloto": dict(sid=5, speed=1.06),  # M1: animada (segunda voz ocasional)
}
STEPS = int(os.environ.get("TTS_STEPS", "16"))

# Pronunciación: (regex, reemplazo hablado). Solo afecta al audio, nunca a subtítulos.
PRON = [
    (r"\bGTA VI\b", "ge te a seis"), (r"\bGTA 6\b", "ge te a seis"), (r"\bGTA V\b", "ge te a cinco"),
    (r"\bGTA 5\b", "ge te a cinco"), (r"\bGTA\b", "ge te a"),
    (r"\bJason\b", "Yéison"), (r"\bLucia\b", "Lucía"), (r"\bDuval\b", "Duval"),
    (r"\bVice City\b", "Vais Síti"), (r"\bLeonida Keys\b", "Leonida Kis"), (r"\bKeys\b", "Kis"),
    (r"\bGrassrivers\b", "Grasrívers"), (r"\bPort Gellhorn\b", "Port Guélhorn"),
    (r"\bMount Kalaga\b", "Maunt Kalága"), (r"\bKalaga\b", "Kalága"), (r"\bNational Park\b", "Náshonal Park"),
    (r"\bRockstar Games\b", "Rokstar Geims"), (r"\bRockstar\b", "Rokstar"), (r"\bTake-Two\b", "Teik Tu"),
    (r"\bPlayStation 5\b", "Pleistéishon cinco"), (r"\bPlayStation\b", "Pleistéishon"), (r"\bPS5 Pro\b", "pe ese cinco Pro"),
    (r"\bPS5\b", "pe ese cinco"), (r"\bPS4\b", "pe ese cuatro"), (r"\bPS3\b", "pe ese tres"), (r"\bPS Store\b", "pe ese Stor"),
    (r"\bXbox Series X\|S\b", "Équis box Síries Equis y Ese"), (r"\bXbox Series X\b", "Équis box Síries Equis"),
    (r"\bXbox Series S\b", "Équis box Síries Ese"), (r"\bSeries X\b", "Síries Equis"), (r"\bSeries S\b", "Síries Ese"),
    (r"\bXbox\b", "Équis box"), (r"\bStore\b", "Stor"), (r"\bUltimate\b", "Áltimet"),
    (r"\bonline\b", "onláin"), (r"\bOnline\b", "Onláin"), (r"\bplay\b", "plei"), (r"\bShorts\b", "shorts"),
    (r"\btráiler\b", "tráiler"), (r"\btrailer\b", "tráiler"), (r"\bspoilers?\b", "espóiler"),
    (r"\bGame Informer\b", "Geim Infórmer"), (r"\bExtended Look\b", "Extended Luk"),
    (r"\bFlorida Man\b", "Flórida Man"), (r"\bLeonida Man\b", "Leonida Man"),
    (r"\bCal Hampton\b", "Kal Jámpton"), (r"\bBoobie Ike\b", "Búbi Aik"), (r"\bDre'Quan Priest\b", "Drikuán Prist"),
    (r"\bReal Dimez\b", "Ril Dáims"), (r"\bRaul Bautista\b", "Raúl Bautista"), (r"\bBrian Heder\b", "Bráian Jéder"),
    (r"\bAaron Garbut\b", "Áron Gárbut"), (r"\bRob Nelson\b", "Rob Nélson"), (r"\bMichael Kane\b", "Máikol Kein"),
    (r"\bMichael\b", "Máikol"), (r"\bFranklin\b", "Fránklin"), (r"\bTrevor\b", "Trévor"),
    (r"\bLos Santos\b", "Los Santos"), (r"\bSan Andreas\b", "San Andreas"), (r"\bRed Dead Redemption 2\b", "Red Ded Ridémpshon dos"),
    (r"\bRDR2\b", "Red Ded Ridémpshon dos"), (r"\bSteam\b", "Estim"), (r"\bRoblox\b", "Róblox"), (r"\bDiscord\b", "Díscord"),
    (r"\bESET\b", "Éset"), (r"\bCynet\b", "Sáinet"), (r"\bVidar\b", "Vídar"), (r"\bWARDEN\b", "Uórden"),
    (r"\bAPK\b", "a pe ka"), (r"\bPC\b", "pe ce"), (r"\bEXE\b", "punto e equis e"), (r"\b\.exe\b", "punto e equis e"),
    (r"\binfostealer\b", "infostíler"), (r"\bmalware\b", "málguer"), (r"\bwallet\b", "uólet"), (r"\bcrypto\b", "cripto"),
    (r"\bGB\b", "gigas"), (r"\bTB\b", "terabait"), (r"\bfps\b", "cuadros por segundo"), (r"\bUSD\b", "dólares"),
    (r"\bEverglades\b", "Évergleids"), (r"\bMiami\b", "Miami"), (r"\bOverseas Highway\b", "Ouversís Jáiuei"),
    (r"\bClewiston\b", "Clúiston"), (r"\bPanama City\b", "Pánama Síti"), (r"\bOcala\b", "Ocala"),
    (r"\bOkeechobee\b", "Okichóubi"), (r"\bhype\b", "jáip"),
    (r"\bstreaming\b", "estrímin"), (r"\bcheckpoint\b", "chécpoint"), (r"\bsetup\b", "sétap"),
    (r"\bupdate\b", "ápdeit"), (r"\bpatch\b", "pach"), (r"\bpreload\b", "prilóud"), (r"\bslow motion\b", "slou móshon"),
    (r"\bwanted\b", "uónted"), (r"\bfeed\b", "fid"), (r"\binfluencers?\b", "influénser"), (r"\bmemes?\b", "mem"),
    (r"\bNewswire\b", "Niúsguaier"), (r"\bCloud Gaming\b", "Cláud Guéimin"), (r"\bCustoms\b", "Cástoms"),
    (r"\bOne-Eyed Willie's\b", "Uán Áid Uílis"), (r"\bRideout\b", "Ráidaut"), (r"\bWeazel News\b", "Uísel Nius"),
    (r"\bJustice\b", "Yóstis"), (r"\bNetflix\b", "Nétflix"), (r"\bYouTube\b", "Yutub"), (r"\bTikTok\b", "Tíktok"),
    (r"\bReddit\b", "Rédit"), (r"\bGoogle\b", "Gúgol"), (r"\bAndroid\b", "Ándroid"), (r"\biPhone\b", "áifon"),
    (r"\bWindows\b", "Uíndous"), (r"\blink\b", "link"), (r"\bbeta\b", "beta"), (r"\bcheat\b", "chit"),
]
_PRON = [(re.compile(a), b) for a, b in PRON]


def split_markup(text):
    """'{sub|habla}' → (subtítulo, texto hablado)."""
    sub = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\1", text)
    spk = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", text)
    return sub, spk


def spoken(text):
    for rx, rep in _PRON:
        text = rx.sub(rep, text)
    text = re.sub(r"\s*[—–]\s*", ", ", text).replace("…", "...").replace("%", " por ciento")
    text = digits_to_words(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text



def split_markup(text):
    """'{sub|habla}' → (subtítulo, texto hablado)."""
    sub = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\1", text)
    spk = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", text)
    return sub, spk


def spoken(text):
    for rx, rep in _PRON:
        text = rx.sub(rep, text)
    text = re.sub(r"\s*[—–]\s*", ", ", text).replace("…", "...").replace("%", " por ciento")
    text = text.replace("“", "").replace("”", "").replace("«", "").replace("»", "").replace('"', "")
    text = digits_to_words(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def trim(a, sr=SR, rel=0.02, pad=0.06):
    """Recorta silencio inicial y final (umbral relativo al pico)."""
    if len(a) == 0: return a
    w = max(1, int(0.01 * sr)); env = np.convolve(np.abs(a), np.ones(w) / w, "same")
    idx = np.where(env > rel * (np.abs(a).max() + 1e-9))[0]
    if len(idx) == 0: return a
    s = max(0, idx[0] - int(pad * sr)); e = min(len(a), idx[-1] + int(pad * sr))
    a = a[s:e].copy(); f = min(len(a) // 2, int(0.012 * sr))
    if f > 1: a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)  # sin clics en los cortes
    return a


def level(a, target_rms=0.2):
    """Iguala el volumen de cada toma (RMS de los tramos con voz)."""
    w = 1024; n = len(a) // w
    if n < 2: return a
    fr = np.sqrt((a[: n * w].reshape(n, w) ** 2).mean(axis=1)); act = fr[fr > 0.1 * fr.max()]
    g = target_rms / (np.sqrt((act ** 2).mean()) + 1e-9)
    return a * min(g, 8.0)


def pause_after(s):
    s = s.rstrip()
    if s.endswith("..."): return 0.50
    if s.endswith("?") or s.endswith("!"): return 0.42
    if s.endswith(":"): return 0.30
    if s.endswith("."): return 0.40
    return 0.25


_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince",
      "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco",
      "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
_T = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
_C = {2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def n2w(n):
    """Entero → palabras en español (lista)."""
    if n < 30: return [_U[n]]
    if n < 100:
        t, u = divmod(n, 10); return [_T[t]] + (["y", _U[u]] if u else [])
    if n < 1000:
        c, r = divmod(n, 100)
        head = ["cien"] if (c == 1 and r == 0) else (["ciento"] if c == 1 else [_C[c]])
        return head + (n2w(r) if r else [])
    if n < 1_000_000:
        m, r = divmod(n, 1000); head = ["mil"] if m == 1 else n2w(m) + ["mil"]
        return head + (n2w(r) if r else [])
    m, r = divmod(n, 1_000_000); head = ["un", "millón"] if m == 1 else n2w(m) + ["millones"]
    return head + (n2w(r) if r else [])


_NUM_RX = re.compile(r"(?<![A-Za-z0-9])(?:\d{1,3}(?:\.\d{3})+|\d+)(?![A-Za-z0-9])")


def digits_to_words(text):
    """Convierte los números escritos con cifras en palabras ('2027' → 'dos mil veintisiete')."""
    def rep(m):
        v = int(m.group(0).replace(".", ""))
        return " ".join(n2w(v)) if v < 10 ** 9 else m.group(0)
    return _NUM_RX.sub(rep, text)


_EQUIV = {"gb": ["gigas"], "tb": ["teras"], "ps5": ["ps", "cinco"], "ps4": ["ps", "cuatro"], "ps3": ["ps", "tres"], "vs": ["versus"],
          "playstation5": ["playstation", "cinco"], "pc": ["pc"], "fps": ["cuadros", "por", "segundo"], "untera": ["un", "tera"], "tera": ["tera"], "ee": ["estados"], "uu": ["unidos"]}


def norm_tokens(word):
    """Normaliza una palabra a tokens comparables: minúsculas, sin tildes ni signos, cifras en palabras."""
    w = digits_to_words(word.lower())
    s = unicodedata.normalize("NFD", w); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    out = []
    s = s.replace("%", " por ciento ")
    for tk in re.findall(r"[a-z0-9]+", s):
        out += _EQUIV.get(tk, [tk])
    return out


def canon(text):
    """Texto → lista de tokens canónicos (para puntuar la coincidencia guion ↔ voz reconocida)."""
    toks = []
    for w in text.split(): toks += norm_tokens(w)
    for i in range(1, len(toks)):  # 'GTA VI' / 'GTA V' → seis / cinco
        if toks[i - 1] == "gta" and toks[i] in ("vi", "v"): toks[i] = "seis" if toks[i] == "vi" else "cinco"
    return toks


class Supertonic:
    sr = SR

    def __init__(self, d=SUPERTONIC_DIR, threads=None):
        import sherpa_onnx
        self._so = sherpa_onnx
        threads = threads or int(os.environ.get("TTS_THREADS", "4"))
        cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
            supertonic=sherpa_onnx.OfflineTtsSupertonicModelConfig(
                duration_predictor=f"{d}/duration_predictor.int8.onnx", text_encoder=f"{d}/text_encoder.int8.onnx",
                vector_estimator=f"{d}/vector_estimator.int8.onnx", vocoder=f"{d}/vocoder.int8.onnx",
                tts_json=f"{d}/tts.json", unicode_indexer=f"{d}/unicode_indexer.bin", voice_style=f"{d}/voice.bin"),
            debug=False, num_threads=threads, provider="cpu"))
        if not cfg.validate():
            raise RuntimeError(f"No se encontró el modelo Supertonic 3 en {d}. Ver instrucciones en engine/README.md")
        self.tts = sherpa_onnx.OfflineTts(cfg)

    def synth(self, text, voice="host", speed=1.0, seed=0, steps=None):
        v = VOICES.get(voice, VOICES["host"])
        g = self._so.GenerationConfig(); g.sid = v["sid"]; g.num_steps = steps or STEPS; g.speed = v["speed"] * speed
        g.extra["lang"] = "es"; g.extra["seed"] = int(seed); g.extra["max_len"] = 2000
        a = self.tts.generate(text, g)
        return np.asarray(a.samples, dtype=np.float32)


class Aligner:
    """Reconocimiento de voz con tiempos por palabra (solo como herramienta de verificación y sincronización)."""

    def __init__(self, d=ALIGN_ASR_DIR, threads=None):
        import sherpa_onnx
        if not os.path.exists(f"{d}/encoder.int8.onnx"):
            raise RuntimeError(f"No se encontró el reconocedor de voz en {d}. Ver instrucciones en engine/README.md")
        threads = threads or int(os.environ.get("TTS_THREADS", "4"))
        self.rec = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx", joiner=f"{d}/joiner.int8.onnx",
            tokens=f"{d}/tokens.txt", model_type="nemo_transducer", num_threads=threads)

    def transcribe(self, x, sr):
        """→ (texto, [(palabra, inicio, fin)])"""
        PAD0, PAD1 = 0.32, 0.56  # silencio de relleno: el reconocedor falla menos en la primera y la última palabra
        x16 = signal.resample_poly(x, 16000, sr).astype(np.float32)
        x16 = np.concatenate([np.zeros(int(PAD0 * 16000), np.float32), x16, np.zeros(int(PAD1 * 16000), np.float32)])
        st = self.rec.create_stream(); st.accept_waveform(16000, x16); self.rec.decode_stream(st); r = st.result
        words = []; cur = None
        durs = list(getattr(r, "durations", [])) or [0.16] * len(r.tokens)
        for tok, t, d in zip(r.tokens, [tt - PAD0 for tt in r.timestamps], durs):
            if tok.startswith(" ") or cur is None:
                if cur and cur[0]: words.append(cur)
                cur = [tok.strip(), None if not tok.strip() else t, t + d]
            else:
                cur[0] += tok
                if cur[1] is None: cur[1] = t
                cur[2] = t + d
        if cur and cur[0]: words.append(cur)
        dur = len(x) / sr
        # el fin de cada palabra no puede pasar del último instante con voz antes de la palabra siguiente
        w = max(1, int(0.01 * sr)); env = np.convolve(np.abs(x), np.ones(w) / w, "same"); act = env > 0.03 * (env.max() + 1e-9)
        out = []
        words = [wd for wd in words if wd[1] is not None]
        for i, (wd, s0, e0) in enumerate(words):
            nxt = words[i + 1][1] if i + 1 < len(words) else dur
            e0 = min(e0, nxt, dur); a = int(s0 * sr); b = max(a + 1, int(e0 * sr))
            seg = np.where(act[a:b])[0]
            e1 = (a + seg[-1]) / sr + 0.02 if len(seg) else e0
            out.append((wd, max(0.0, s0), max(min(e1, e0 + 0.02), s0 + 0.03)))
        return r.text, out

    def align(self, x, sr, sub_words, expected_text=None):
        """Alinea las palabras del subtítulo con el audio.
        → ([(inicio, fin)] por palabra, puntuación 0-1 de coincidencia con el guion, texto reconocido)"""
        text, hyp = self.transcribe(x, sr)
        dur = len(x) / sr
        w = max(1, int(0.01 * sr)); env = np.convolve(np.abs(x), np.ones(w) / w, "same"); on = np.where(env > 0.03 * (env.max() + 1e-9))[0]
        t_on = on[0] / sr if len(on) else 0.0; t_off = on[-1] / sr if len(on) else dur
        E = []; emap = []
        for i, sw in enumerate(sub_words):
            for tk in norm_tokens(sw): E.append(tk); emap.append(i)
        Hh = []; hmap = []
        for j, (hw, hs, he) in enumerate(hyp):
            for tk in norm_tokens(hw): Hh.append(tk); hmap.append(j)
        for toks in (E, Hh):
            for i in range(1, len(toks)):
                if toks[i - 1] == "gta" and toks[i] in ("vi", "v"): toks[i] = "seis" if toks[i] == "vi" else "cinco"
        sm = difflib.SequenceMatcher(None, E, Hh, autojunk=False)
        times = [None] * len(sub_words)
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                i = emap[a + k]; j = hmap[b + k]
                s, e = hyp[j][1], hyp[j][2]
                times[i] = (s, e) if times[i] is None else (min(times[i][0], s), max(times[i][1], e))
        # puntuación: guion hablado (números en palabras, nombres con su ortografía normal) frente a lo reconocido
        Es = canon(expected_text) if expected_text else E
        score = difflib.SequenceMatcher(None, Es, Hh, autojunk=False).ratio() if Es else 1.0
        # palabras sin ancla: se reparte el hueco por número de caracteres
        i = 0; n = len(sub_words)
        while i < n:
            if times[i] is not None: i += 1; continue
            j = i
            while j < n and times[j] is None: j += 1
            left = times[i - 1][1] if i > 0 else t_on
            right = times[j][0] if j < n else t_off
            right = max(right, left + 0.01)
            tot = sum(len(sub_words[k]) + 1 for k in range(i, j)); acc = 0
            for k in range(i, j):
                s = left + (right - left) * acc / tot; acc += len(sub_words[k]) + 1
                times[k] = (s, left + (right - left) * acc / tot)
            i = j
        out = []; prev = 0.0
        for (s, e) in times:
            s = min(max(s, prev, 0.0), dur); e = min(max(e, s + 0.03), dur); out.append((s, e)); prev = s
        if out and t_off - out[-1][1] < 0.5: out[-1] = (out[-1][0], max(out[-1][1], t_off))
        return out, score, text


def take_seed(text, voice):
    return zlib.crc32((voice + "|" + text).encode("utf-8")) % 100000
