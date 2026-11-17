"""Narración en español latinoamericano con Kokoro-82M (licencia Apache-2.0).

- Fonemización propia con espeak-ng en variante `es-419` (seseo, yeísmo): evita el
  acento castellano que produce la variante `es`.
- Diccionario de pronunciación para nombres en inglés (Jason → "Yéison", etc.).
- Síntesis frase a frase: devuelve marcas de tiempo exactas para SRT y para sincronizar
  la animación con la voz.

Modelos (no incluidos en el repositorio por tamaño): descarga
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
y apunta la variable de entorno KOKORO_DIR a la carpeta descomprimida.
"""
import os, re, numpy as np
import onnxruntime as ort
import espeakng_loader
from phonemizer.backend.espeak.wrapper import EspeakWrapper
EspeakWrapper.set_library(espeakng_loader.get_library_path())
EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
from phonemizer.backend import EspeakBackend

KOKORO_DIR = os.environ.get("KOKORO_DIR", "/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad/voices/kokoro-multi-lang-v1_0")
SR = 24000
VOICES = {"host": 29, "analista": 28}  # em_alex (masculina), ef_dora (femenina)

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
    (r"\bPS5\b", "pe ese cinco"), (r"\bPS4\b", "pe ese cuatro"), (r"\bPS Store\b", "pe ese Stor"),
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
    text = text.replace("—", ", ").replace("–", ", ").replace("…", "...").replace("%", " por ciento")
    text = re.sub(r"\s+", " ", text).strip()
    return text


class Kokoro:
    def __init__(self, d=KOKORO_DIR):
        so = ort.SessionOptions(); so.intra_op_num_threads = int(os.environ.get("TTS_THREADS", "4"))
        self.sess = ort.InferenceSession(f"{d}/model.onnx", so, providers=["CPUExecutionProvider"])
        self.vocab = {}
        for line in open(f"{d}/tokens.txt", encoding="utf-8"):
            line = line.rstrip("\n")
            if not line: continue
            sym, idx = line.rsplit(" ", 1) if not line.startswith(" ") else (" ", line.strip())
            self.vocab[sym] = int(idx)
        self.voices = np.fromfile(f"{d}/voices.bin", dtype=np.float32).reshape(-1, 510, 256)
        self.ph = EspeakBackend("es-419", preserve_punctuation=True, with_stress=True,
                                language_switch="remove-flags")

    def phonemes(self, text):
        p = self.ph.phonemize([text], strip=True)[0]
        return p

    def synth(self, text, voice="host", speed=1.0):
        ph = self.phonemes(text)
        ids = [self.vocab[c] for c in ph if c in self.vocab]
        if len(ids) > 500:
            raise ValueError(f"Frase demasiado larga para Kokoro ({len(ids)} tokens): {text[:60]}")
        sid = VOICES.get(voice, voice)
        style = self.voices[sid][min(len(ids), 509)].reshape(1, 256)
        tok = np.array([[0] + ids + [0]], dtype=np.int64)
        out = self.sess.run(None, {"tokens": tok, "style": style, "speed": np.array([speed], dtype=np.float32)})[0]
        a = np.asarray(out, dtype=np.float32).reshape(-1)
        return trim(a)


def trim(a, thr=0.008, pad=0.03):
    env = np.convolve(np.abs(a), np.ones(240) / 240, "same")
    idx = np.where(env > thr)[0]
    if len(idx) == 0: return a
    s = max(0, idx[0] - int(pad * SR)); e = min(len(a), idx[-1] + int(pad * SR))
    return a[s:e]


SENT_RX = re.compile(r"(?<=[\.\?\!…:])\s+(?=[¿¡A-ZÁÉÍÓÚÑ0-9\"«(])")


def sentences(text):
    parts = [p.strip() for p in SENT_RX.split(text.strip()) if p.strip()]
    return parts


def pause_after(s):
    s = s.rstrip()
    if s.endswith("..."): return 0.48
    if s.endswith("?") or s.endswith("!"): return 0.38
    if s.endswith(":"): return 0.28
    if s.endswith("."): return 0.33
    return 0.22
