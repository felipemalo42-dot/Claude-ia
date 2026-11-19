"""Empaqueta GTA6_VIDEO_LANZAMIENTO (vídeo post lanzamiento, módulo videos/gp.py): registro de planos y sincronía, guion .docx, descripción y SEO,
recursos visuales, permisos con cifras reales y limpieza.
Uso: python gp_package.py [--log] [--docx] [--pub] [--visuals] [--clean]   (sin argumentos: todo)
"""
import csv, importlib, json, math, os, re, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
import build
from tts import split_markup

ROOT = build.ROOT; OUT = os.environ.get("GP_OUT", os.path.join(ROOT, "GTA6_VIDEO_LANZAMIENTO"))
M = importlib.import_module("videos.gp"); V = M.VIDEO; B = V["beats"]; R = M.R
def tl(): return json.load(open(f"{OUT}/recursos/timeline.json"))
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
def ctx(): return build.Ctx(V, tl(), 1920, 1080)

CHAPTERS = {"GANCHO": "GTA 6 ya se juega: el veredicto", "INTRODUCCIÓN: TRES AVISOS": "Tres avisos: fuentes, opiniones y spoilers",
            "1 · EL VEREDICTO": "El veredicto: 99 en Metacritic", "2 · LOS PRIMEROS JUGADORES": "Los primeros jugadores (Nueva Zelanda)",
            "3 · EL MUNDO": "El mundo y la gente de Leonida", "3B · QUÉ HACER": "Qué hacer: actividades secundarias",
            "4 · LOS ATRACOS (AVISO DE SPOILER)": "Los atracos (AVISO: escenas de misiones)", "5 · LA CONDUCCIÓN": "La conducción (fin de los spoilers)",
            "5B · LA POLICÍA": "La policía", "6 · EL COMBATE": "El combate", "7 · EL REALISMO": "El realismo del día a día",
            "8 · EL RENDIMIENTO": "Rendimiento: 30 fps y Digital Foundry", "9 · LA HISTORIA (SIN SPOILERS)": "La historia (sin spoilers)",
            "10 · EL LANZAMIENTO": "El lanzamiento: Sam Houser y la bolsa", "11 · LAS PRIMERAS HORAS": "Las primeras horas: récord de audiencia y primeras quejas", "CIERRE": "Resumen y cierre"}
SFX_ES = {"whoosh": "barrido", "pop": "pop", "paper": "papel", "stamp": "sello", "hit": "golpe grave", "tick": "tic", "ding": "campanita",
          "logo": "sintonía del canal", "tune": "dial de radio"}
MUS_ES = {"synthwave": "synthwave", "electro": "electro", "tension": "tensión (pads oscuros)", "trap26": "trap", "tropical": "tropical",
          "synthpop": "synthpop", "nature": "ambiente tropical tranquilo", "seventies": "piano eléctrico", "mystery": "misterio"}
CERT_ES = {"OFICIAL": "DATO OFICIAL (verde)", "INTERPRETACIÓN": "INTERPRETACIÓN (amarillo)", "ULTIMATE": "EXCLUSIVO EDICIÓN ULTIMATE (morado)",
           "RESERVA": "BONO POR RESERVAR (cian)"}
GFX_ES = {"trailers": "Gráfico: los tres tráileres", "mosaic": "Gráfico: mosaico con las 138 capturas oficiales", "nospoil": "Gráfico: sellos «0 misiones · 0 finales · 0 filtraciones»",
          "sting": "Cortinilla del canal", "title": "Título del vídeo", "media": "Gráfico: el material oficial descargable", "legend": "Gráfico: semáforo verde/amarillo",
          "chapters": "Gráfico: los 10 capítulos", "date": "Gráfico: calendario 19 NOV · 00:00 hora local", "platforms": "Gráfico: PS5 y Xbox Series X|S",
          "lang": "Gráfico: voces en inglés, textos en español", "claim": "Gráfico: sin micropagos / sin IA generativa", "timeline": "Gráfico: línea de tiempo 2023-2026",
          "swap": "Montaje: Jason ⇄ Lucía (dos capturas oficiales)", "poll": "Gráfico: encuesta Jason o Lucía", "cast": "Gráfico: las 6 ilustraciones del reparto",
          "map": "Mapa: representación aproximada sobre Florida real", "postcards": "Gráfico: las 6 postales oficiales", "el_card": "Gráfico: ficha del Extended Look",
          "profile": "Gráfico: perfil criminal (representación)", "editions": "Gráfico: estándar frente a Ultimate", "mute": "Gráfico: audio oficial silenciado",
          "unknown": "Gráfico: lo que falta por saber", "subscribe": "Gráfico: suscripción", "end": "Pantalla final",
          "title2": "Título del vídeo", "meta": "Gráfico: nota de Metacritic y OpenCritic", "quote": "Gráfico: frase de una reseña (traducida)",
          "outlets": "Gráfico: medios citados", "spoiler": "Cartel de aviso de spoiler", "spoiler_end": "Cartel de fin de spoilers",
          "nz": "Gráfico: horas de desbloqueo / truco de Nueva Zelanda", "warn": "Gráfico: riesgo de sanción", "realism": "Gráfico: lo que avisan 6 reseñas",
          "fps": "Gráfico: 30 fps", "df": "Gráfico: medidas de Digital Foundry", "police": "Gráfico: la policía según Windows Central",
          "drone": "Gráfico: carreras de drones (sin imagen oficial)", "poll2": "Gráfico: ¿inmersión o molestia?", "poll3": "Gráfico: ¿ya lo juegas?",
          "hours": "Gráfico: ≈80 horas", "dfps": "Gráfico: Digital Foundry en PlayStation", "stream": "Gráfico: récord de audiencia en directo", "bugs": "Gráfico: quejas de jugadores (sin confirmar)", "psn": "Gráfico: caída de PSN", "houser": "Gráfico: mensaje de Sam Houser", "stock": "Gráfico: bolsa y reservas", "nospoil2": "Gráfico: sin spoilers en comentarios"}

def shot_desc(s):
    k, v = s["src"].split(":", 1)
    if k == "g": return GFX_ES.get(v, v)
    return R.source_label(s["src"]).replace("Rockstar Games · ", "")

# ---------------------------------------------------------------- registro de planos y sincronía
def log():
    C = ctx(); T = R.table(C); rows = []
    for s in T["shots"]:
        k, v = s["src"].split(":", 1)
        win = R.src_window(s) if k in ("e", "l", "p", "k") else None
        src_t = None
        if win:
            path, loc, Ls = win; off = R.EL_RANGES[os.path.basename(path)[:-4]][0] if k == "e" else 0.0
            src_t = f"{mmss(loc + off)}.{int(((loc + off) % 1) * 10)}"
        rows.append(dict(inicio=round(s["t0"], 3), fin=round(s["t1"], 3), duracion=round(s["t1"] - s["t0"], 2), palabra=s.get("word") or "",
                         ancla=s.get("anchor") or "(inicio del bloque)", desfase_s=round(s["t0"] - s["word_t"], 3) if s.get("word_t") is not None else "",
                         tipo={"e": "Extended Look", "l": "Tráiler de lanzamiento", "p": "Vídeo Pre-Load Now", "c": "Vídeo de personaje", "k": "Portada animada",
                               "s": "Captura oficial", "u": "Edición Ultimate", "v": "Vintage Vice City", "a": "Ilustración oficial", "g": "Gráfico propio"}[k],
                         recurso=v if k not in ("e", "l", "p") else ("GTAVI_An_Extended_Look.mp4" if k == "e" else "GTAVI_Launch_Trailer.mp4" if k == "l" else "GTAVI_Pre-Load_Now.mp4"),
                         minuto_en_el_original=src_t or "", rotulo=" | ".join(x for x in [s.get("label"), s.get("region"), (s.get("card") or [None])[0], s.get("quote")] if x) or ""))
    with open(f"{OUT}/recursos/registro_de_planos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";"); w.writeheader(); w.writerows(rows)
    # sincronía imagen ↔ palabra
    anch = [r for r in rows if r["desfase_s"] != ""]
    ok = [r for r in anch if abs(r["desfase_s"]) <= 0.10]
    durs = [r["duracion"] for r in rows if r["tipo"] != "Gráfico propio" and r["fin"] < tl()["total"] - 20.5]
    long_ = [r for r in rows if r["duracion"] > 5.0 and r["fin"] < tl()["total"] - 20.5]
    stats = dict(planos=len(rows), anclados=len(anch), sincronizados=len(ok), pct=100.0 * len(ok) / max(1, len(anch)),
                 dur_media=sum(r["duracion"] for r in rows[:-1]) / max(1, len(rows) - 1), mas_de_5s=len(long_),
                 max_oficial=max(durs) if durs else 0)
    json.dump(stats, open(f"{OUT}/recursos/sincronia.json", "w"), ensure_ascii=False, indent=1)
    # uso por tipo de material (para el registro de permisos)
    use = {}
    for r in rows:
        if r["tipo"] == "Gráfico propio": continue
        u = use.setdefault(r["tipo"], dict(n=0, s=0.0, files=set())); u["n"] += 1; u["s"] += r["duracion"]; u["files"].add(r["recurso"])
    json.dump({k: dict(n=v["n"], s=round(v["s"], 1), archivos=sorted(v["files"])) for k, v in use.items()}, open(f"{OUT}/recursos/uso_por_material.json", "w"), ensure_ascii=False, indent=1)
    print(f"planos {stats['planos']} · anclados {stats['anclados']} · sincronizados ±0,10 s: {stats['sincronizados']} ({stats['pct']:.2f} %) · media {stats['dur_media']:.2f} s · >5 s: {stats['mas_de_5s']}")
    for r in long_: print("   plano largo:", r["inicio"], r["duracion"], r["recurso"], r["ancla"])
    return stats, use

def permissions():
    stats, use = log()
    p = f"{OUT}/REGISTRO_DE_PERMISOS.txt"; s = open(p, encoding="utf-8").read()
    def u(tipo, unit="planos"):
        x = use.get(tipo)
        return f"{x['n']} {unit}, {x['s']:.0f} s en total ({len(x['files'])} archivos distintos)" if x else "no se usa"
    rep = {"{{USO_E}}": u("Extended Look"), "{{USO_L}}": u("Tráiler de lanzamiento"), "{{USO_P}}": u("Vídeo Pre-Load Now"),
           "{{USO_C}}": f"{u('Vídeo de personaje')}; portada animada: {u('Portada animada')}", "{{USO_S}}": u("Captura oficial"),
           "{{USO_A}}": u("Ilustración oficial"), "{{USO_U}}": u("Edición Ultimate"), "{{USO_V}}": u("Vintage Vice City"),
           "{{MAX_PLANO}}": f"{stats['max_oficial']:.1f}".replace(".", ",")}
    for a, b in rep.items(): s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)
    bad = "\n".join(f"  {mmss(a)}-{mmss(b)}  ({a:.1f}-{b:.1f} s)" for a, b in R.BAD)
    open(f"{OUT}/recursos/tramos_excluidos.txt", "w", encoding="utf-8").write(
        "Tramos del Extended Look que el montaje NO muestra (misiones, escenas de historia, violencia explícita, transiciones con glitch, rótulos).\n"
        "Si un plano llegara a uno de ellos, el motor vuelve al inicio del plano. Código: engine/videos/gl_render.py (lista BAD).\n\n" + bad + "\n")
    print("permisos: cifras reales insertadas")

# ---------------------------------------------------------------- guion .docx
def docx():
    T = tl(); C = ctx(); TB = R.table(C); beats = []; plain = []
    by_beat = {}
    for s in TB["shots"]: by_beat.setdefault(s["beat"], []).append(s)
    for i, (b, bd) in enumerate(zip(B, T["beats"])):
        lines = []
        for k, s in enumerate(bd["sents"]):
            nxt = bd["sents"][k + 1]["start"] if k + 1 < len(bd["sents"]) else (T["beats"][i + 1]["start"] if i + 1 < len(T["beats"]) else T["total"])
            gap = nxt - s["end"]; pause = f"{gap:.1f} s".replace(".", ",") if gap >= 0.45 else None
            lines.append(dict(parts=[dict(t=s["text"])], pause=pause))
        vis = []
        for s in by_beat.get(i, []):
            when = mmss(s["t0"]) + (f" «{s['anchor']}»" if s.get("anchor") else "")
            vis.append(f"{when} → {shot_desc(s)}")
        sfx = ", ".join(dict.fromkeys(SFX_ES.get(c[1], c[1]) for c in b.get("sfx", [])))
        st, lv = b.get("mus", ("synthwave", 1))
        silent = None
        if not lines: silent = "(sin narración · cortinilla del canal)" if i < 5 else "(sin narración · pantalla final de 20 s)"
        beats.append(dict(section=b.get("section"), time=mmss(bd["start"]), dur=f"{bd['end'] - bd['start']:.1f} s".replace(".", ","), lines=lines, silent=silent,
                          visual="\n".join(vis), sfx=sfx, music=f"{MUS_ES.get(st, st)} · energía {lv}/3",
                          ritmo=("Rótulo: " + CERT_ES[b["cert"]]) if b.get("cert") in CERT_ES else "", cert=CERT_ES.get(b.get("cert"), "")))
        if b["vo"]: plain.append(" ".join(split_markup(x)[0] for x in build.split_sentences(b["vo"])))
    words = sum(len(p.split()) for p in plain); dur = T["total"]
    speech = sum(s["end"] - s["start"] for bd in T["beats"] for s in bd["sents"])
    st = json.load(open(f"{OUT}/recursos/sincronia.json"))
    ficha = [("Título", V["title"]), ("Canal", "Sal y Asfalto"), ("Formato", "Vídeo largo 16:9 · 1920 × 1080 · 30 fps · H.264 + AAC"),
             ("Duración final", f"{mmss(dur)} ({dur:.0f} s), incluida la pantalla final de 20 s"), ("Palabras de narración", f"{words}"),
             ("Ritmo medio", f"{words / (speech / 60):.0f} palabras por minuto de habla"),
             ("Voz", "La misma narradora del canal (voz C, Chatterbox Multilingual, licencia MIT; referencia OpenSLR SLR72, CC BY-SA 4.0)"),
             ("Imagen", f"Solo material oficial de Rockstar Games ({st['planos']} planos, con la fuente en pantalla) y gráficos propios. Audio oficial silenciado. Sin vídeos de streamers (ver REGISTRO_DE_PERMISOS.txt)"),
             ("Sincronía imagen ↔ voz", f"{st['sincronizados']} de {st['anclados']} cortes ({st['pct']:.1f} %) caen a menos de 0,10 s del inicio de la palabra que los motiva"),
             ("Spoilers", "Solo en el capítulo 4 (escenas de misiones del Extended Look), con cartel de aviso y minuto para saltarlo. Ninguno en título ni miniatura"),
             ("Monetización", "Publicar SIN anuncios: la política de Rockstar solo permite uso no comercial (ver REGISTRO_DE_PERMISOS.txt)")]
    human = ["El motor admite cambiar la voz sintética por una grabación humana sin rehacer el montaje.",
             "Graba cada bloque en un WAV: GTA6_VIDEO_LANZAMIENTO/voz_humana/beat_NN.wav (NN = número de bloque desde 00, contando también los bloques sin narración).",
             "Bloques con narración: " + ", ".join(f"{i:02d}" for i, b in enumerate(B) if b["vo"]) + ".",
             "Ejecuta: python engine/build.py gp --jobs 4. El reconocimiento de voz vuelve a calcular los tiempos de cada palabra, y con ellos los cortes, los rótulos y los subtítulos."]
    extra = [("Cómo se sincroniza cada imagen con la palabra", [
        "Cada plano del guion tiene un «ancla»: el fragmento exacto de la narración que lo motiva (por ejemplo, «un tiroteo» → tiroteo en el callejón del Extended Look, 14:24).",
        "El reconocedor de voz da el instante de inicio de cada palabra. El corte se hace 2 fotogramas (0,06 s) antes de esa palabra, que es lo que el ojo percibe como sincronía exacta.",
        "Los planos de vídeo terminan en su propio corte de escena: no saltan a otra escena del material original mientras se habla del anterior. Si el plano oficial es más corto que la frase, se ralentiza (hasta 0,5×) o se repite.",
        "El registro completo plano a plano está en recursos/registro_de_planos.csv (inicio, palabra, desfase, archivo oficial y minuto)."])]
    data = dict(title=V["title"], subtitle="Guion completo con marcas de tiempo · GTA6_VIDEO_LANZAMIENTO (post lanzamiento) · Sal y Asfalto · 18/11/2026", ficha=ficha, beats=beats,
                sources=SOURCES, human=human, plain=plain, extra=extra, footer="Sal y Asfalto · Guion GTA6_VIDEO_LANZAMIENTO · página ",
                labels=["Tiempo", "Narración ([pausa] = silencio medido)", "Planos (tiempo «palabra» → material)", "Rótulo"])
    jp = os.path.join(OUT, "recursos", "_guion_docx.json"); json.dump(data, open(jp, "w", encoding="utf-8"), ensure_ascii=False)
    dst = os.path.join(OUT, "GUION_COMPLETO.docx")
    subprocess.run(["node", os.path.join(os.path.dirname(__file__), "vx_docx.js"), jp, dst], check=True)
    subprocess.run(["zip", "-d", dst, "*/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(jp); print("docx: palabras", words, "duración", mmss(dur))

SOURCES = [("Notas (18/11/2026)", ["Metacritic 99 (más de 140 reseñas, ninguna mixta ni negativa) y OpenCritic 98-99: Bloomberg, Vice, Dot Esports, Output Lag",
                                    "IGN 10/10, GameSpot 10/10, Eurogamer 5/5, Destructoid 10, Worthplaying 9,5, GamesRadar+, Windows Central, Forbes"]),
           ("Jugabilidad según las reseñas", ["Atracos: GameSpot y Windows Central", "Conducción: Forbes y GameSpot", "Policía y PNJ: Windows Central y Vice",
                                              "Combate, realismo, ritmo y 30 fps: resúmenes de The National, Pure Xbox, Dot Esports y Output Lag",
                                              "Actividades: The National, Output Lag y Vice", "Rendimiento medido: Digital Foundry (vía VGC y LevelUp), Rockstar a Wccftech"]),
           ("Lanzamiento", ["Primeros jugadores: Stuff y NZ Herald (Nueva Zelanda)", "Truco de Nueva Zelanda y riesgo de sanción: Notebookcheck, Newsweek, NME",
                            "Sam Houser: GamesRadar+ · Bolsa y reservas: Forbes · 80 horas: Rob Nelson a Variety"]),
           ("Imágenes", ["Solo material oficial de Rockstar Games (rockstargames.com/VI/media): Extended Look, tráiler de lanzamiento, capturas, ilustraciones y vídeos de personajes"])]

# ---------------------------------------------------------------- publicación (descripción, títulos, SEO)
TITLES = ["GTA 6 ya se juega: qué dicen de su jugabilidad quienes ya lo han jugado (99 en Metacritic)",
          "GTA 6: lo bueno y lo malo según las reseñas (atracos, conducción, combate y 30 FPS)",
          "GTA 6 tras el lanzamiento: un 99 en Metacritic… y dos peros",
          "GTA 6 ya salió: así se juega según la crítica y los primeros jugadores"]
TAGS = ["GTA 6", "GTA VI", "Grand Theft Auto VI", "GTA 6 reseñas", "GTA 6 review en español", "GTA 6 Metacritic", "GTA 6 jugabilidad", "GTA 6 gameplay",
        "GTA 6 atracos", "GTA 6 conducción", "GTA 6 30 fps", "GTA 6 Digital Foundry", "GTA 6 Xbox Series S", "GTA 6 PS5", "GTA 6 lanzamiento",
        "GTA 6 Nueva Zelanda", "GTA 6 vale la pena", "Leonida", "Vice City", "Sal y Asfalto"]
KEYWORDS = dict(principal="gta 6 reseñas", secundarias=["gta 6 metacritic", "gta 6 jugabilidad", "gta 6 vale la pena", "gta 6 30 fps", "gta 6 review español",
                                                         "gta 6 atracos", "gta 6 conducción", "gta 6 series s rendimiento"])
PINNED = ("📌 ¿Ya lo estás jugando o esperas a tu hora? Cuéntanos qué te ha parecido la conducción y el combate 👇 "
          "Espacio SIN SPOILERS: si comentas algo de la historia, empieza con «SPOILER». Las imágenes de misiones del vídeo están en el capítulo de los atracos, con aviso.")
DISCLOSE = ("ℹ️ Transparencia y derechos\n"
            "• Imágenes: solo material oficial de Rockstar Games (rockstargames.com/VI/media): Extended Look, tráiler de lanzamiento, capturas, ilustraciones y vídeos de personajes. "
            "La fuente aparece en pantalla en cada plano. Uso no comercial y con comentario, según la política de Rockstar sobre su material. Vídeo no monetizado. Audio oficial silenciado.\n"
            "• Las opiniones son de los medios citados (reseñas publicadas el 18/11/2026); las frases se muestran traducidas. Nuestra interpretación va marcada en amarillo.\n"
            "• Grand Theft Auto, GTA, Vice City y Leonida son marcas de Take-Two Interactive. Canal independiente, sin relación con Rockstar Games.\n"
            "• Narración con voz sintética (Chatterbox Multilingual, licencia MIT) a partir de una voz de referencia de OpenSLR SLR72 (Google, CC BY-SA 4.0). Música, efectos y gráficos originales.")

def chapters():
    T = tl(); out = []
    for b, bd in zip(B, T["beats"]):
        if b.get("section") in CHAPTERS: out.append((bd["start"], CHAPTERS[b["section"]]))
    out[0] = (0.0, out[0][1])
    return out

def publication():
    T = tl(); ch = chapters()
    desc = ("GTA 6 ya se juega, y la crítica ya ha hablado: 99 en Metacritic. Repasamos qué dicen de su JUGABILIDAD los medios que ya lo han jugado "
            "y los primeros jugadores de Nueva Zelanda: atracos, conducción, policía, combate, realismo, rendimiento a 30 fps e historia (sin spoilers). "
            "Cada dato lleva su fuente en pantalla y su imagen real del juego (material oficial de Rockstar).\n\n"
            "⚠️ AVISO: el capítulo de los atracos muestra escenas de misiones del Extended Look oficial. Si no quieres verlas, salta al capítulo siguiente.\n\n"
            "CAPÍTULOS\n" + "\n".join(f"{mmss(t)} {n}" for t, n in ch) + "\n\n"
            "FUENTES PRINCIPALES\n"
            "• Bloomberg: «Grand Theft Auto VI Becomes the Best-Reviewed Video Game Ever»: https://www.bloomberg.com/news/articles/2026-11-18/-grand-theft-auto-vi-becomes-the-best-reviewed-video-game-ever\n"
            "• Vice, resumen de reseñas: https://www.vice.com/en/article/gta-6-review-roundup/\n"
            "• GameSpot (10/10): https://www.gamespot.com/reviews/grand-theft-auto-6-review/\n"
            "• Windows Central: https://www.windowscentral.com/gaming/xbox/grand-theft-auto-6-xbox-review\n"
            "• GamesRadar+: https://www.gamesradar.com/games/grand-theft-auto/gta-6-review/\n"
            "• Forbes (Paul Tassi): https://www.forbes.com/sites/paultassi/2026/11/18/grand-theft-auto-6-review-a-perfect-crime/\n"
            "• The National, lo que gusta y lo que no: https://www.thenationalnews.com/arts-culture/pop-culture/2026/11/18/gta-6-reviews-metacritic/\n"
            "• Output Lag, resumen: https://outputlag.com/featured-slider/gta-6-review-roundup/\n"
            "• Digital Foundry vía VGC (Series S): https://www.videogameschronicle.com/news/gta-6-xbox-series-s-performance-analysis-admires-the-effort-but-says-significant-frame-drops-are-a-problem/\n"
            "• NZ Herald (primeros jugadores): https://www.nzherald.co.nz/world/gta-6-hits-new-zealand-kiwi-gamers-first-in-the-world-to-play-as-global-launch-begins-in-nz/JAYVNPFB45DPRJPHDWIIQNS6NQ/\n"
            "• Material oficial: https://www.rockstargames.com/VI/media\n"
            "Lista completa: FUENTES_Y_ENLACES.txt (proyecto del canal).\n\n"
            + DISCLOSE + "\n\n#GTA6 #GTAVI #ViceCity")
    open(f"{OUT}/DESCRIPCION_YOUTUBE.txt", "w", encoding="utf-8").write(desc)
    st = json.load(open(f"{OUT}/recursos/sincronia.json"))
    L = ["# GTA6_VIDEO_LANZAMIENTO: paquete de publicación", "", f"**Duración real:** {mmss(T['total'])} · **Formato:** 16:9, 1920×1080, 30 fps, H.264 + AAC",
         "**Archivos:** `VIDEO_FINAL.mp4` · `MINIATURA.png` (1280×720) · `SUBTITULOS.srt` · `NARRACION.mp3` · `GUION_COMPLETO.docx`", "",
         "## Títulos", "", f"- **Principal:** {TITLES[0]}", *[f"- Alternativo {i}: {t}" for i, t in enumerate(TITLES[1:], 1)], "",
         "## Palabras clave", "", f"- **Principal:** {KEYWORDS['principal']}", f"- **Secundarias:** {', '.join(KEYWORDS['secundarias'])}", "",
         "## Etiquetas (copiar y pegar)", "", ", ".join(TAGS), "", "## Descripción", "", "Está en `DESCRIPCION_YOUTUBE.txt` (lista para copiar y pegar, con capítulos y fuentes).", "",
         "## Comentario fijado", "", PINNED, "", "## Capítulos", "", *[f"- {mmss(t)} {n}" for t, n in ch], "",
         "## Configuración en YouTube Studio (obligatoria)", "",
         "- **Monetización: DESACTIVADA en este vídeo.** La política de Rockstar solo permite usar su material sin fines comerciales (ver `REGISTRO_DE_PERMISOS.txt`).",
         "- **Contenido alterado o sintético: SÍ.** La narración es una voz sintética realista.",
         "- **Subtítulos:** el vídeo ya lleva subtítulos dinámicos incrustados. Sube igualmente `SUBTITULOS.srt` (español) para accesibilidad, búsqueda y traducción automática.",
         "- **Contenido para niños:** No. **Restricción de edad:** no hace falta (no hay violencia explícita), pero el juego es para mayores de 18 años.",
         "- **Pantalla final (últimos 20 s):** un vídeo recomendado (sugerido: VIDEO_04, el mapa) y la lista «GTA VI explicado».",
         "- **Publicación sugerida:** cuanto antes, jueves 19/11/2026 (día del lanzamiento en América y Europa). Las notas citadas son del 18/11: si cambian, actualiza la descripción.",
         "- **Si llega una reclamación de Content ID de Rockstar:** no la dispute. Es su material y el vídeo no se monetiza.", "",
         "## Control de calidad", "", f"- Sincronía imagen ↔ palabra: {st['sincronizados']}/{st['anclados']} cortes a menos de 0,10 s ({st['pct']:.1f} %).",
         "- Coincidencia guion ↔ voz: ver `recursos/control_de_voz.csv` y `AUDITORIA_FINAL.md`.", ""]
    open(f"{OUT}/PUBLICACION_YOUTUBE.md", "w", encoding="utf-8").write("\n".join(L))
    print("publicación lista ·", len(ch), "capítulos")

# ---------------------------------------------------------------- recursos visuales
def visuals():
    import skia, gfx
    T = tl(); C = ctx(); TB = R.table(C); groups = build.group_scenes(V, T); info = build.SceneInfo(groups[0])
    d = os.path.join(OUT, "RECURSOS_VISUALES"); os.makedirs(d, exist_ok=True)
    n = 0; seen = set()
    for s in TB["shots"]:
        k, v = s["src"].split(":", 1)
        if k != "g" or (v, s.get("step")) in seen or v in ("sting", "end"): continue
        seen.add((v, s.get("step")))
        tt = s["t0"] + min(1.6, (s["t1"] - s["t0"]) * 0.8)
        surf = gfx.new_surface(1920, 1080); c = surf.getCanvas(); c.clear(skia.ColorBLACK)
        R.scene(c, tt - info.start, info, C); R.overlay(c, tt, C)
        surf.makeImageSnapshot().save(f"{d}/{n + 1:02d}_grafico_{v}{'_' + str(s['step']) if s.get('step') not in (None, 0) else ''}.png", skia.kPNG); n += 1
    shutil.copy(f"{OUT}/MINIATURA.png", f"{d}/00_miniatura.png")
    # índice de material oficial usado
    rows = list(csv.DictReader(open(f"{OUT}/recursos/registro_de_planos.csv", encoding="utf-8"), delimiter=";"))
    idx = {}
    for r in rows:
        if r["tipo"] == "Gráfico propio": continue
        key = (r["tipo"], r["recurso"]); idx.setdefault(key, []).append(f"{mmss(float(r['inicio']))}" + (f" (orig. {r['minuto_en_el_original']})" if r["minuto_en_el_original"] else ""))
    ZIP = {"Captura oficial": "GTAVI_Screenshots.zip", "Edición Ultimate": "GTAVI_Ultimate_Edition_Benefits.zip", "Vintage Vice City": "GTAVI_Vintage_Vice_City_Pack.zip",
           "Ilustración oficial": "GTAVI_Artwork_Wallpapers.zip", "Vídeo de personaje": "GTAVI_Videos.zip", "Portada animada": "GTAVI_Official_Cover_Art_Landscape.mp4",
           "Extended Look": "GTAVI_An_Extended_Look.mp4", "Tráiler de lanzamiento": "GTAVI_Launch_Trailer.mp4", "Vídeo Pre-Load Now": "GTAVI_Pre-Load_Now.mp4"}
    with open(f"{d}/indice_material_oficial.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["tipo", "archivo_oficial", "paquete_de_descarga", "aparece_en_el_video (mm:ss)"])
        for (tp, rec), ts in sorted(idx.items()): w.writerow([tp, rec, ZIP.get(tp, ""), ", ".join(ts)])
    open(f"{d}/LEEME.txt", "w", encoding="utf-8").write(
        "RECURSOS VISUALES · GTA6_VIDEO_LANZAMIENTO\n\n"
        f"1. {n} gráficos propios del vídeo en PNG 1920×1080, exportados desde el motor (títulos, línea de tiempo, mapa, ediciones…).\n"
        "   Son diseño original de Sal y Asfalto; los que incluyen imágenes oficiales las citan en pantalla.\n"
        "2. 00_miniatura.png: la miniatura, con la captura oficial «Jason_and_Lucia_09», sin logotipo ni spoilers.\n"
        "3. indice_material_oficial.csv: cada archivo oficial de Rockstar usado, el paquete de descarga en el que viene y los momentos del vídeo en que aparece.\n"
        "   Los archivos oficiales no se copian aquí: se descargan de https://www.rockstargames.com/VI/media (enlaces directos en FUENTES_Y_ENLACES.txt).\n"
        "   Así no se redistribuyen fuera de la página oficial y siempre se usa la versión vigente.\n"
        "4. ../recursos/hoja_de_contactos.jpg: un fotograma cada 5 s del vídeo final, para revisar el montaje de un vistazo.\n"
        "5. ../recursos/registro_de_planos.csv: los planos uno a uno (inicio, palabra que lo motiva, desfase, archivo y minuto original).\n")
    print("recursos visuales:", n)

def clean():
    r = os.path.join(OUT, "recursos")
    if os.path.exists(f"{r}/musica_original.wav"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{r}/musica_original.wav", "-c:a", "libmp3lame", "-b:a", "256k", f"{r}/musica_original.mp3"], check=True)
        os.remove(f"{r}/musica_original.wav")
    for f in ("mezcla_final.wav",):
        if os.path.exists(f"{r}/{f}"): os.remove(f"{r}/{f}")
    fr = f"{r}/fotogramas"
    if os.path.isdir(fr):
        from PIL import Image
        import glob
        ims = [Image.open(p).convert("RGB") for p in sorted(glob.glob(f"{fr}/*.png"))]
        if ims:
            cols = 6; rows = (len(ims) + cols - 1) // cols; sheet = Image.new("RGB", (cols * 320, rows * 180), (10, 10, 14))
            for i, im in enumerate(ims): sheet.paste(im.resize((320, 180)), ((i % cols) * 320, (i // cols) * 180))
            sheet.save(f"{r}/hoja_de_contactos.jpg", quality=82)
        shutil.rmtree(fr)
    print("limpieza lista")

if __name__ == "__main__":
    args = set(sys.argv[1:]) or {"--log", "--docx", "--pub", "--visuals", "--clean"}
    if "--clean" in args: clean()
    if "--log" in args: permissions()
    if "--pub" in args: publication()
    if "--docx" in args: docx()
    if "--visuals" in args: visuals()
    if "--audit" in args: audit()

# ---------------------------------------------------------------- auditoría final con cifras medidas sobre el MP4
def audit():
    import statistics
    T = tl(); mp4 = f"{OUT}/VIDEO_FINAL.mp4"
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels,bit_rate",
                                    "-of", "json", mp4], capture_output=True, text=True).stdout)
    fmt = pr["format"]; vs = [s for s in pr["streams"] if s.get("width")][0]; aus = [s for s in pr["streams"] if s.get("sample_rate")][0]
    nfr = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", mp4],
                             capture_output=True, text=True).stdout.strip())
    lu = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", lu); lufs = float(m[-1]) if m else float("nan")
    st = json.load(open(f"{OUT}/recursos/sincronia.json"))
    rows = list(csv.DictReader(open(f"{OUT}/recursos/control_de_voz.csv", encoding="utf-8"), delimiter=";"))
    D = sum(int(r["diferencias"] or 0) for r in rows); N = sum(int(r["sonidos"] or 0) for r in rows)
    low = [r for r in rows if float(r["coincidencia"]) < 0.995]
    words = sum(len(" ".join(split_markup(x)[0] for x in build.split_sentences(b["vo"])).split()) for b in B if b["vo"])
    dur = float(fmt["duration"]); exp_fr = int(math.ceil(T["total"] * 30)) if False else None
    L = ["# GTA6_VIDEO_LANZAMIENTO: auditoría final", "",
         f"**Vídeo:** *{V['title']}* · `VIDEO_FINAL.mp4` · revisado el {__import__('time').strftime('%d/%m/%Y')} sobre el archivo final.", "",
         "## Datos técnicos medidos", "", "| Comprobación | Resultado |", "|---|---|",
         f"| Duración | **{mmss(dur)}** ({dur:.1f} s), incluida la pantalla final de 20 s |",
         f"| Vídeo | {vs['codec_name'].upper()} 10 bits, {vs['width']} × {vs['height']}, {vs['r_frame_rate'].split('/')[0]} fps, {nfr} fotogramas |",
         f"| Audio | AAC, {int(aus['sample_rate']) // 1000} kHz, {aus['channels']} canales |",
         f"| Tamaño | {int(fmt['size']) / 1e6:.1f} MB (límite de GitHub: 100 MB) |",
         f"| Sonoridad integrada | {lufs:.1f} LUFS (objetivo de YouTube: −14) |",
         f"| Narración | {words} palabras, voz C (la misma del canal) |",
         f"| Coincidencia guion ↔ voz | **{1 - D / max(1, N):.2%}** global ({D} sonidos distintos de {N}); {len(rows) - len(low)} de {len(rows)} tomas ≥ 99,5 % |",
         f"| Sincronía imagen ↔ palabra | **{st['sincronizados']} de {st['anclados']} cortes ({st['pct']:.1f} %)** a ≤ 0,10 s del inicio de su palabra |",
         f"| Planos | {st['planos']} (media {st['dur_media']:.1f} s por plano) |", ""]
    open(f"{OUT}/recursos/_auditoria_cifras.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L)); print("tomas por debajo de 99,5 %:", [(r["inicio_s"], r["coincidencia"]) for r in low])
