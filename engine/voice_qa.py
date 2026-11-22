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
    (r"\bOpen Critic\b", "OpenCritic"), (r"\b[YJHyjh][uaá]s?t? [Ll](?:a?i|ai)ke? [Pp][aá]ra ?[Dd]a?i[sc]e?\b", "Just Like Paradise"), (r"\b[Ii]mponte [Ff](?:í|i)nix\b", "Imponte Phoenix"), (r"\b[Bb][aá]ckyard [Aa]m[eé]rican? [Mm][ae]i?n[ií]a\b", "Backyard American Mania"), (r"\b(?:[Tt]he|[Dd]i|[Dd]e) [YyJjGg][eé]ntrif[ae]i(?:er|ier|r)\b", "The Gentrifier"), (r"\b[JjHh][aá]mlet\b", "Hamlet"), (r"\b(?:SOS|S\.O\.S\.?|ese o ese)\b", "S.O.S."), (r"\bmetacritic\b", "Metacritic"),
]
_ALIAS = [(re.compile(a, re.I), b) for a, b in ALIAS]
_ROMAN = {"xx": "veinte", "xix": "diecinueve", "xxi": "veintiuno"}

def _pre(text):
    t = re.sub(r"\$\s?(\d{1,3}),(\d{3})\b", r"$\1\2", text)   # «$1,191»: separador de miles a la inglesa en cantidades en dólares
    t = re.sub(r"(\d+),(\d+)", r"\1 coma \2", t)
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

# ================================================================ WER: tasa de error de palabras guion ↔ voz
# Método (GTA6 VIDEO_LARGO y SHORT_PROMOCIONAL, noviembre de 2026):
#  1. Guion y transcripción se normalizan igual: minúsculas, sin signos de puntuación, sin tildes, cifras escritas
#     en palabras («321» = «trescientos veintiuno»). No se toca ninguna otra palabra.
#  2. En la transcripción se unifican SOLO las grafías distintas de un mismo nombre propio o término inglés
#     (el reconocedor escribe «Yeison» lo que en el guion es «Jason»). Lista cerrada en WER_ALIAS.
#  3. WER = (sustituciones + omisiones + inserciones) / palabras del guion (distancia de Levenshtein por palabras).
#     No cuentan como error (se listan aparte): homófonos del español latinoamericano (seseo, yeísmo, b/v, h muda:
#     «caza» = «casa») y la unión o separación de palabras cuando las letras coinciden («escapar es» = «escapares»),
#     porque en el audio son idénticos y la diferencia solo está en cómo escribe el reconocedor.
#  4. Cada toma se transcribe con Parakeet TDT v3; si hay alguna diferencia, también con Whisper small, y cuenta la
#     transcripción con menos errores: un fallo de la voz aparece en los dos reconocedores, un fallo de un
#     reconocedor normalmente no. Las dos transcripciones se guardan en el informe.
WER_ALIAS = [
    (r"\b(?:ge|g)[ .-]?(?:te|t)[ .-]?(?:a|á)\b", "GTA"), (r"\bGTA ?(?:VI|seis)\b", "GTA 6"), (r"\bGTA6\b", "GTA 6"), (r"\bGT ?6\b", "GTA 6"), (r"\bGT ?5\b", "GTA 5"), (r"\bGT ?A\b", "GTA"),
    (r"\b[YyJj][eé][iy]?son\b", "Jason"), (r"\b[YyJj]a[iy]?son\b", "Jason"), (r"\bYason\b", "Jason"),
    (r"\b[VvBb][aá][iy]s[ -]?[CcSs][ií]t[iy]?\b", "Vice City"), (r"\b[Bb]y ?[Cc]ity\b", "Vice City"), (r"\b[Bb]ai ?[CcSs]ity\b", "Vice City"), (r"\b[VvBb]ice[ -]?[CcSs]ity\b", "Vice City"), (r"\b[VvBb]aisiti\b", "Vice City"),
    (r"\b[Ff][oó]u?[ck]us\b", "Focus"), (r"\b[Rr]o[ck]+ ?[Ss]tar\b", "Rockstar"), (r"\b[Rr]okstar\b", "Rockstar"),
    (r"\b[Ss]ic[oó]patas?\b", lambda m: "Psicópata" + ("s" if m.group(0).endswith("s") else "")),
    # vídeos 2 y 3 (Planeta Vice City, GTA 6 a juicio): grafías de nombres propios y términos ingleses
    (r"\b[Gg]ran[dt]?[ -]?(?:th|z|s|t|c)?e(?:ph|[fp])?t,?[ -]?[aoó]u?t+o\b", "Grand Theft Auto"), (r"\bTheft,? ?otro\b", "Theft Auto"), (r"\b[CcKk]arl\b", "Karl"),
    (r"\b(?:M[ae]?c?[ -]?)?(?:qu|[CcKkGg])+[eiíy]*[ií]+t+h?r[ií]+[ck]+k?\b", "McKittrick"), (r"\bR[aáe][iy]?[sz]+[ie]ng?\b", "Rising"),
    (r"\b(?:e?s[ck]o?u?n[ck]?k?[ -]?(?:qu|k)?e?i?p|skunk ?ape)\b", "Skunk Ape"), (r"\b(?:K|C|Qu)[eiu]r[ck]k?\b", "Kirk"),
    (r"\b(?:Key|K[iy]|Qu?i)[ -]?[Ll]ento\b", "Key Lento"), (r"\bBr[aá]?[iy]+[aá]n\b", "Brian"),
    (r"\b(?:g?[uü]|w|b)[eéa][iy]?st[eé]d\b", "wasted"), (r"\be?s?trip[ -]?t[iíe]+[aá]?[sz]e?\b", "striptease"),
    (r"\binfluen[cs]er\b", "influencer"), (r"\b[OoÓó]u?[sc]h?[eé]?a?n[ -]?B[ie]+a?[ct]?ch\b", "Ocean Beach"),
    (r"\bMiami[ -]?B[ie]+a?ch\b", "Miami Beach"), (r"\bMiami,?[ -]?D[aeé]i?(?:gh)?[dt]e?\b", "Miami-Dade"),
    (r"\b(?:the|de|di|za|da)[ -]?[Gg]u?[aá]rdi[aá]n\b", "The Guardian"), (r"\b(?:pe ?ce|p ?c)[ -]?[Gg]u?[aeé]i?mer\b", "PC Gamer"), (r"\b[Nn][iey]?[uú]s[ -]?[GgWw]?[uü]?[ie]+[kc]k?\b", "Newsweek"), (r"\b[Nn]ews ?[Ww]eek\b", "Newsweek"), (r"\b[Bb]ig[ -]?[Bb][oa]ll?[ -]?[Bb][eéuú]rg[ue]?e?r\b", "Big Ball Burger"), (r"\b[Bb]rad[ -]?[Ll](?:aw|o|ou|ow)\b", "Brad Law"), (r"\b[Jj]ank\b", "Hank"),
    (r"\b[Ss](?:treet|trit|trick)[ -]?[Tt]rash\b", "Street Trash"), (r"\b(?:[Tt]aim|[Tt]ime)[ -]?[YyJj][aá]c?kers?\b", "Time Jackers"),
    (r"\b[Tt][eé]nebr(?:ae|e|a|ay)[ -]?[Ll]ux\b", "Tenebrae Lux"), (r"\b[Bb]ang?,?[ -]?(?:for|four|fur|4)[ -]?(?:your|yur|yor|you)[ -]?[Bb][uaoú]ck\b", "Bang For Your Buck"),
    (r"\b[Ss]h[uú]ter\b", "shooter"), (r"\b[Ss]?[Cc]?[Ss]?[aá]i?ber[ -]?p[aou]nk\b", "cyberpunk"), (r"\b[Kk]al\b", "Cal"), (r"\b[ZzSs][aá]pp?(?:ing|in|en)?\b", "zapping"), (r"\b[Ww][eé]st[ -]?[Ee]nd?\b", "western"), (r"\b[Ww]esten\b", "western"), (r"\b(?:[GgWw]u?[aá]f(?:o?l)?e?s|[Ww]affles?|[Gg]uafles)\b", "waffles"), (r"\b[Bb]radl[oa]w?\b", "Brad Law"), (r"\b[Zz]ombies\b", "zombis"), (r"\b[Tt]h?[aiy]i?n[ -]?[YyJj][aá]c?kers?\b", "Time Jackers"), (r"\b[Tt]ynjackers\b", "Time Jackers"),
    (r"\b(?:equis|x)[ -]?box\b", "Xbox"), (r"\bs[ií]ries\b", "Series"), (r"\bNor[tzs]h?\b", "North"),
    (r"\bRed[ -]?D[eé]d\b", "Red Dead"), (r"\bR[ei]d[eé]mp?(?:sh|ch|s)[ie]?[oó]n\b", "Redemption"),
    (r"\bP[aá]r+o[td]\b", "Parrot"), (r"\bP[aá]r[aá]d[aá][iy]s[e]?\b", "Paradise"),
]
_WALIAS = [(re.compile(a, re.I), b) for a, b in WER_ALIAS]

def wer_tokens(text, hyp=False):
    from tts import canon
    t = _pre(text)
    if hyp:
        for rx, rep in _WALIAS: t = rx.sub(rep, t)
    t = re.sub(r"\bGTA VI\b", "GTA 6", t); t = re.sub(r"\bGTA V\b", "GTA 5", t)
    t = re.sub(r"\b(Theft Auto) VI\b", r"\1 6", t); t = re.sub(r"\b(Theft Auto) V\b", r"\1 5", t)   # número romano del título = el número dicho
    t = re.sub(r"(\d),(\d{3})\b", r"\1\2", t)   # separador de miles a la inglesa («$1,191»): es el mismo número
    t = re.sub(r"\$\s?(\d)", r"\1", t)             # «$1191 dólares»: el símbolo no se pronuncia (ya se dice «dólares»)
    t = re.sub(r"[«»“”\"¿?¡!.,;:()…—–]", " ", t)
    # apócope de los numerales («veintiún enemigos», «noventa y un dólares»): misma palabra que el número escrito con cifras
    ws = ["veintiuno" if w == "veintiun" else w for w in canon(t)]
    return ["uno" if w == "un" and i and ws[i - 1] == "y" else w for i, w in enumerate(ws)]

def _pk(w):
    """Clave fonética de una palabra (seseo, yeísmo, b = v, h muda): dos palabras con la misma clave suenan igual."""
    return joined(phon(w))

def join_eq(a, b, ka, kb, c, kc):
    """¿Dos palabras seguidas (a b) suenan como una sola (c)? Mismas letras o misma pronunciación encadenada:
    la sinalefa funde vocales iguales y consonantes iguales en la frontera («apunta a» = «apunta», «vuelve en» = «vuelven»)."""
    return a + b == c or (bool(kc) and joined(ka + kb) == joined(kc))

def wer(expected, hyp):
    """→ dict(err, n, sub, dele, ins, diff=[(tipo, guion, reconocido)], homof=[...], uniones=[...]) con la alineación mínima por palabras.
    Igualdades que no son errores (se listan aparte en el informe):
      - homófonos del español latinoamericano (seseo, yeísmo, b/v, h muda): «caza» = «casa», «a» = «ha»;
      - unión o separación de palabras: la separación entre palabras no se oye; «escapares» = «escapar es»
        solo si las letras (o su pronunciación) coinciden exactamente."""
    E = wer_tokens(expected); Hh = wer_tokens(hyp, True); n, m = len(E), len(Hh)
    kE = [_pk(w) for w in E]; kH = [_pk(w) for w in Hh]
    def eq(i, j): return E[i] == Hh[j] or (kE[i] and kE[i] == kH[j])
    INF = 10 ** 9
    D = np.full((n + 1, m + 1), INF, np.int64); D[0, :] = np.arange(m + 1); D[:, 0] = np.arange(n + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            best = min(D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 1, j - 1] + (0 if eq(i - 1, j - 1) else 1))
            if i >= 2 and join_eq(E[i - 2], E[i - 1], kE[i - 2], kE[i - 1], Hh[j - 1], kH[j - 1]): best = min(best, D[i - 2, j - 1])
            if j >= 2 and join_eq(Hh[j - 2], Hh[j - 1], kH[j - 2], kH[j - 1], E[i - 1], kE[i - 1]): best = min(best, D[i - 1, j - 2])
            D[i, j] = best
    i, j = n, m; ops = []; homof = []; un = []; ref_err = [None] * n; ins_at = [[] for _ in range(n + 1)]
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i, j] == D[i - 1, j - 1] + (0 if eq(i - 1, j - 1) else 1):
            if not eq(i - 1, j - 1): ops.append(("sustitución", E[i - 1], Hh[j - 1])); ref_err[i - 1] = Hh[j - 1]
            elif E[i - 1] != Hh[j - 1]: homof.append((E[i - 1], Hh[j - 1]))
            i -= 1; j -= 1
        elif i >= 2 and j >= 1 and D[i, j] == D[i - 2, j - 1] and join_eq(E[i - 2], E[i - 1], kE[i - 2], kE[i - 1], Hh[j - 1], kH[j - 1]):
            un.append((E[i - 2] + " " + E[i - 1], Hh[j - 1])); i -= 2; j -= 1
        elif j >= 2 and i >= 1 and D[i, j] == D[i - 1, j - 2] and join_eq(Hh[j - 2], Hh[j - 1], kH[j - 2], kH[j - 1], E[i - 1], kE[i - 1]):
            un.append((E[i - 1], Hh[j - 2] + " " + Hh[j - 1])); i -= 1; j -= 2
        elif i > 0 and D[i, j] == D[i - 1, j] + 1: ops.append(("omisión", E[i - 1], "")); ref_err[i - 1] = ""; i -= 1
        else: ops.append(("inserción", "", Hh[j - 1])); ins_at[i].append(Hh[j - 1]); j -= 1
    ops.reverse()
    s_ = sum(o[0] == "sustitución" for o in ops); d = sum(o[0] == "omisión" for o in ops); ins = sum(o[0] == "inserción" for o in ops)
    return dict(err=s_ + d + ins, n=n, sub=s_, dele=d, ins=ins, diff=ops, homof=homof[::-1], uniones=un[::-1], E=E, ref_err=ref_err, ins_at=ins_at)

def wer_combined(expected, hyp_a, hyp_b):
    """WER con dos reconocedores independientes, palabra a palabra: una palabra del guion cuenta como error solo si los
    DOS reconocedores la fallan (un fallo de la voz aparece en ambos; un fallo de un reconocedor, normalmente en uno);
    una palabra de más cuenta solo si los dos la añaden en el mismo sitio."""
    ra = wer(expected, hyp_a); rb = wer(expected, hyp_b) if hyp_b is not None else ra
    diff = []
    for k, w in enumerate(ra["E"]):
        if ra["ref_err"][k] is not None and rb["ref_err"][k] is not None:
            diff.append(("omisión" if ra["ref_err"][k] == "" and rb["ref_err"][k] == "" else "sustitución", w, f"{ra['ref_err'][k] or '—'} / {rb['ref_err'][k] or '—'}"))
    for k in range(len(ra["ins_at"])):
        for _ in range(min(len(ra["ins_at"][k]), len(rb["ins_at"][k]))): diff.append(("inserción", "", f"{ra['ins_at'][k][0]} / {rb['ins_at'][k][0]}"))
    return dict(err=len(diff), n=ra["n"], diff=diff, homof=ra["homof"] + rb["homof"], uniones=ra["uniones"] + rb["uniones"], a=ra, b=rb)
