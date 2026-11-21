"""Empaqueta VIDEO_EXTRA: guion .docx, paquete de publicación, recursos visuales y limpieza.
Uso: python vx_package.py [--docx] [--pub] [--visuals] [--clean]   (sin argumentos: todo)
"""
import importlib, json, os, re, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
import build
from tts import split_markup

ROOT = build.ROOT; OUT = os.path.join(ROOT, "VIDEO_EXTRA")
V = importlib.import_module("videos.vx").VIDEO
B = V["beats"]
def tl(): return json.load(open(f"{OUT}/recursos/timeline.json"))
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"

SFX_ES = {"neon": "neón que se enciende", "whoosh": "barrido", "brush": "brochazo", "hit": "golpe grave", "paper": "papel", "tick": "tic", "ding": "campanita",
          "pop": "pop", "chime": "campanas suaves", "flap": "abanico de muestras", "stamp": "sello", "tune": "dial de radio (cambio de época)", "water": "agua",
          "pin": "marca", "coin": "moneda", "thunder": "trueno", "wind": "viento", "rain": "lluvia", "impact": "impacto", "rumble": "maquinaria pesada",
          "typing": "máquina de escribir", "buzz": "zumbido de error", "tv_on": "encendido de televisor de tubo", "glitch": "interferencia digital",
          "phone": "notificación", "shutter": "obturador", "logo": "sintonía del canal"}
MUS_ES = {"synthwave": "synthwave", "nature": "ambiente tropical tranquilo", "storm": "tormenta (pads oscuros)", "swing30": "swing de los años 30",
          "seventies": "piano eléctrico de los 70", "synthpop": "synthpop de los 80", "electro": "electro de 2002", "trap26": "trap de 2026"}
CHAPTERS = {"GANCHO": "Los colores que esconden algo", "INTRODUCCIÓN: LA PREGUNTA": "La pregunta: ¿por qué Vice City se ve así?",
            "LO QUE DICE ROCKSTAR": "Lo que dice Rockstar de Ocean Beach", "CAPA 1 · 1912 · LA ARENA": "Capa 1 · 1912: la arena y el nombre Ocean Beach",
            "LA TORMENTA · 1926": "1926: el huracán que acabó con el boom", "CAPA 2 · AÑOS 30 · EL BLANCO": "Capa 2 · Años 30: eran blancos",
            "CAPA 3 · AÑOS 70 · EL ABANDONO": "Capa 3 · Años 70: la mujer frente a las excavadoras", "CAPA 4 · 1980 · EL PASTEL": "Capa 4 · 1980: el diseñador del pastel",
            "CAPA 5 · 1984 · LA TELEVISIÓN": "Capa 5 · 1984: la regla de Miami Vice", "CAPA 6 · 2002 · EL VIDEOJUEGO": "Capa 6 · 2002: el videojuego",
            "CAPA 7 · 2026 · LAS PANTALLAS": "Capa 7 · 2026: Hotel Dixon y las pantallas", "LA VUELTA COMPLETA": "Miami se viste de Vice City",
            "EL PRECIO DEL PASTEL": "El precio del pastel", "GUÍA DE CAMPO PARA MAÑANA": "Tu misión en Ocean Beach (guía de campo)",
            "CIERRE": "Una copia de una copia de una copia"}
SOURCES = [
    ("Lo que dice Rockstar · Capa 7", ["Rockstar Games, web oficial de GTA VI y «Only in Leonida» (rockstargames.com/VI, consultado el 18/11/2026)"]),
    ("Capa 1 · 1912", ["City of Miami Beach, «How Miami Beach Began – July 1912»", "Wikipedia, «Miami Beach, Florida» (Ocean Beach como nombre de la propiedad de los Lummus)"]),
    ("La tormenta · 1926", ["Wikipedia, «1926 Miami hurricane»"]),
    ("Capa 2 · años 30", ["NPS, T. Alam (2018): edificios mayormente blancos con toques de verde jade, ocre o coral", "Wikipedia, «Miami Beach, Florida» (hoteles pequeños de estuco para alquilar por temporada)",
                          "Time Out Miami; Ciudad de Miami, Preservación Histórica (rasgos del art déco)"]),
    ("Capa 3 · años 70", ["National Trust for Historic Preservation (2014), «Barbara Baer Capitman: South Beach's Art Deco Hero»", "Wikipedia, «Barbara Baer Capitman»",
                          "NPS (2018): Registro Nacional, mayo de 1979; demoliciones"]),
    ("Capa 4 · 1980", ["WLRN (2013), «Meet The Man Behind All Those South Beach Pastels»", "NPS (2018): Friedman's Bakery, continuidad de color y regla actual de tonos pastel"]),
    ("Capa 5 · 1984", ["Wikipedia, «Miami Vice» (cita a TIME, 1985)", "Mental Floss: Michael Mann a Los Angeles Times (1987)", "NPS (2018): carritos de comida", "WLRN (2013): muerte de Horowitz"]),
    ("Capa 6 · 2002", ["Wikipedia, «Grand Theft Auto (video game)» y «Grand Theft Auto: Vice City»", "GamesRadar+ (contexto del desarrollo)"]),
    ("Capa 7 · 2026 y la vuelta completa", ["AP vía WLRN (17/11/2026)", "Axios Miami (2023)", "Miami New Times (mapa de lugares reales)"]),
    ("El precio del pastel", ["NPS (2018)", "National Trust (2014): cita de John Capitman"]),
]

def emph_parts(text, emph):
    """Divide la frase en fragmentos y marca en negrita las expresiones de énfasis."""
    spans = []
    for e in emph or []:
        for m in re.finditer(re.escape(e), text): spans.append((m.start(), m.end()))
    spans.sort(); parts = []; i = 0
    for a, b in spans:
        if a < i: continue
        if a > i: parts.append(dict(t=text[i:a]))
        parts.append(dict(t=text[a:b], b=True)); i = b
    if i < len(text): parts.append(dict(t=text[i:]))
    return parts

def cert_of(b):
    vo = b["vo"]
    if "nuestra lectura" in vo or "Para nosotros" in vo: return "INTERPRETACIÓN (amarillo) + DOCUMENTADO (verde)"
    if "Rockstar describe" in vo or "En la web de Rockstar" in vo or "Vintage Vice City" in vo: return "OFICIAL (verde)"
    if "Según" in vo or "según" in vo: return "DOCUMENTADO (verde)"
    return ""

def docx():
    T = tl(); beats = []; plain = []
    for i, (b, bd) in enumerate(zip(B, T["beats"])):
        lines = []
        for k, s in enumerate(bd["sents"]):
            nxt = bd["sents"][k + 1]["start"] if k + 1 < len(bd["sents"]) else (T["beats"][i + 1]["start"] if i + 1 < len(T["beats"]) else T["total"])
            gap = nxt - s["end"]; pause = f"{gap:.1f} s".replace(".", ",") if gap >= 0.45 else None
            lines.append(dict(parts=emph_parts(s["text"], b.get("emph")), pause=pause))
        sfx = ", ".join(dict.fromkeys(SFX_ES.get(c[1], c[1]) for c in b.get("sfx", [])))
        st, lv = b.get("mus", ("synthwave", 1))
        silent = None
        if not lines:
            silent = "(sin narración · cortinilla de marca)" if b["scene"].__name__ == "sc_sting" else "(sin narración · pantalla final con video recomendado y suscripción)"
        beats.append(dict(section=b.get("section"), time=mmss(bd["start"]), dur=f"{bd['end'] - bd['start']:.1f} s".replace(".", ","), lines=lines, silent=silent,
                          visual=b.get("note", "Cortinilla del canal." if silent and "cortinilla" in silent else "Pantalla final: dos videos y botón de suscripción."),
                          sfx=sfx, music=f"{MUS_ES.get(st, st)} · energía {lv}/3", ritmo=b.get("ritmo", ""), cert=cert_of(b) if lines else ""))
        if b["vo"]: plain.append(" ".join(split_markup(x)[0] for x in build.split_sentences(b["vo"])))
    words = sum(len(p.split()) for p in plain); dur = T["total"]
    speech = sum(s["end"] - s["start"] for bd in T["beats"] for s in bd["sents"])
    ficha = [("Título", V["title"]), ("Canal", "Sal y Asfalto"), ("Formato", "Video largo 16:9 · 1920 × 1080 · 30 fps · H.264 + AAC"),
             ("Duración final", f"{mmss(dur)} ({dur:.0f} s), incluida la pantalla final de 20 s"), ("Palabras de narración", f"{words}"),
             ("Ritmo medio", f"{words / (speech / 60):.0f} palabras por minuto de habla"),
             ("Voz", "Narradora sintética (Chatterbox Multilingual, licencia MIT; referencia de voz OpenSLR SLR72, CC BY-SA 4.0). Español latinoamericano."),
             ("Música y sonido", "Originales, sintetizados por código: un estilo distinto por época"),
             ("Pregunta central", "¿Por qué la Vice City de GTA 6 se ve como se ve, con sus hoteles pastel, su art déco y su neón?"),
             ("Estructura", "Gancho → pregunta → 7 capas (1912, años 30, años 70, 1980, 1984, 2002 y 2026) → vuelta completa → matiz → guía de campo → cierre"),
             ("Imágenes", "Ilustración y animación vectorial original. Ningún material de Rockstar (ver REGISTRO_DE_DERECHOS.txt)")]
    human = ["El motor admite reemplazar la voz sintética por una grabación humana sin rehacer la animación.",
             "Graba cada bloque de narración en un WAV: VIDEO_EXTRA/voz_humana/beat_NN.wav. NN es el número del bloque, empezando en 00 y contando también los bloques sin narración.",
             "Bloques con narración: " + ", ".join(f"{i:02d}" for i, b in enumerate(B) if b["vo"]) + ".",
             "Ejecuta: python engine/build.py vx. El reconocimiento de voz vuelve a sincronizar automáticamente palabras, animaciones, efectos y subtítulos.",
             "Respeta las negritas (énfasis) y las pausas indicadas. El ritmo de la columna derecha es una guía, no una regla."]
    data = dict(title=V["title"], subtitle="Guion completo con marcas de tiempo · VIDEO_EXTRA · Sal y Asfalto · 18/11/2026", ficha=ficha, beats=beats,
                sources=SOURCES, human=human, plain=plain)
    jp = os.path.join(OUT, "recursos", "_guion_docx.json"); json.dump(data, open(jp, "w", encoding="utf-8"), ensure_ascii=False)
    dst = os.path.join(OUT, "GUION_COMPLETO.docx")
    subprocess.run(["node", os.path.join(os.path.dirname(__file__), "vx_docx.js"), jp, dst], check=True)
    subprocess.run(["zip", "-d", dst, "*/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(jp); print("palabras", words, "duración", mmss(dur))

def chapters():
    T = tl(); out = []
    for b, bd in zip(B, T["beats"]):
        if b.get("section") in CHAPTERS: out.append((bd["start"], CHAPTERS[b["section"]]))
    out[0] = (0.0, out[0][1])
    return out

TITLES = ["¿Por qué Vice City es rosa? La historia real de sus colores (GTA 6)",
          "El hombre que eligió los colores de Vice City… sin saberlo | GTA 6",
          "Ocean Beach existió de verdad: la historia real detrás de Vice City en GTA 6",
          "GTA 6: por qué los hoteles de Vice City son pastel si en 1930 eran blancos"]
TAGS = ["GTA 6", "GTA VI", "Vice City", "GTA 6 Vice City", "Ocean Beach GTA 6", "GTA 6 Miami", "GTA 6 vida real", "Vice City historia", "art déco",
        "Miami Beach art deco", "Ocean Drive", "Miami Vice", "Hotel Dixon GTA 6", "colores de Vice City", "GTA Vice City 2002", "GTA 6 explicado",
        "GTA 6 en español", "Leonida", "Rockstar Games", "Sal y Asfalto"]
KEYWORDS = dict(principal="gta 6 vice city", secundarias=["vice city historia real", "ocean beach gta 6", "gta 6 miami vida real", "art deco miami beach",
                                                           "miami vice gta", "hotel dixon gta 6", "por qué vice city es rosa", "colores de vice city"])
PINNED = ("Misión para mañana 🌴 Cuando entres a Ocean Beach, busca la fachada más art déco que encuentres (cejas sobre las ventanas, ojos de buey, "
          "adornos de tres en tres, bloques de vidrio, esquinas redondeadas, neón vertical) y cuéntanos cuántas pistas viste. "
          "La respuesta más completa se queda fijada. Las fuentes de cada dato están en la descripción. ¿Qué capa te sorprendió más?")
DISCLOSE = ("ℹ️ Transparencia: ilustraciones, animaciones, música y efectos originales de Sal y Asfalto (hechos por código, sin material de Rockstar). "
            "Narración con voz sintética (Chatterbox Multilingual, licencia MIT) a partir de una voz de referencia del corpus abierto OpenSLR SLR72 "
            "(Google, CC BY-SA 4.0 · Guevara-Rukoz et al., LREC 2020). Grand Theft Auto, GTA y Vice City son marcas de Take-Two Interactive; "
            "canal independiente, sin relación con Rockstar Games.")

def publication():
    T = tl(); ch = chapters()
    desc = ("¿Por qué los hoteles de Vice City son rosa, menta y lavanda? Porque los edificios reales que los inspiran eran BLANCOS. "
            "Los colores llegaron en los años 80, de la mano de un diseñador real que murió ocho años antes del primer GTA. "
            "Raspamos la pintura de Vice City capa por capa: de una barra de arena en 1912 al letrero «Welcome to Vice City» de 2026.\n\n"
            "En este video:\n• De dónde viene el nombre Ocean Beach (no lo inventó un videojuego)\n• El huracán de 1926 y el art déco modesto de los años 30\n"
            "• Barbara Capitman, la activista que se plantó frente a las excavadoras\n• Leonard Horowitz y la panadería que parecía un pastel de cumpleaños\n"
            "• La regla de Miami Vice: nada de tonos tierra\n• De la Vice City de 2002 al Hotel Dixon de GTA 6\n• Tu guía de campo para reconocer el art déco en el juego\n\n"
            "CAPÍTULOS\n" + "\n".join(f"{mmss(t)} {n}" for t, n in ch) + "\n\n"
            "FUENTES PRINCIPALES\n"
            "• Rockstar Games, web oficial de GTA VI: https://www.rockstargames.com/VI/only-in-leonida/vice-city\n"
            "• NPS, «Color Palettes to the Rescue» (2018): https://www.nps.gov/articles/000/color-pallets-saving-buildings-from-demolition.htm\n"
            "• WLRN, «Meet The Man Behind All Those South Beach Pastels» (2013): https://www.wlrn.org/culture/2013-11-16/meet-the-man-behind-all-those-south-beach-pastels\n"
            "• National Trust, «Barbara Baer Capitman» (2014): https://savingplaces.org/stories/barbara-baer-capitman-south-beach-art-deco-hero\n"
            "• City of Miami Beach, «How Miami Beach Began» (julio de 1912): https://www.miamibeachfl.gov/this-month-in-miami-beach-history-july-1912/\n"
            "• AP vía WLRN (17/11/2026): https://www.wlrn.org/arts-culture/2026-11-17/miami-embraces-its-vice-city-alter-ego-seizing-buzz-around-gta-vi-release\n"
            "• Axios Miami (2023): https://www.axios.com/local/miami/2023/12/05/gta-6-trailer-vice-city-landmarks\n"
            "• Wikipedia: «Miami Vice», «Grand Theft Auto: Vice City», «1926 Miami hurricane», «Miami Beach, Florida»\n"
            "Lista completa con qué dato respalda cada fuente: FUENTES_Y_REFERENCIAS.txt (proyecto del canal).\n\n"
            + DISCLOSE + "\n\n#GTA6 #ViceCity #GTAVI #ArtDeco")
    open(f"{OUT}/DESCRIPCION_YOUTUBE.txt", "w", encoding="utf-8").write(desc)
    open(f"{OUT}/ETIQUETAS.txt", "w", encoding="utf-8").write(", ".join(TAGS) + "\n")
    L = [f"# VIDEO_EXTRA: paquete de publicación", "", f"**Duración real:** {mmss(T['total'])} · **Formato:** 16:9, 1920×1080, 30 fps, H.264 + AAC",
         "**Archivo:** `VIDEO_FINAL.mp4` · **Miniatura:** `MINIATURA.png` (1280×720) · **Subtítulos:** `SUBTITULOS.srt` (español)", "",
         "## Títulos", "", f"- **Principal:** {TITLES[0]}", *[f"- Alternativo {i}: {t}" for i, t in enumerate(TITLES[1:], 1)], "",
         "## Palabras clave", "", f"- **Principal:** {KEYWORDS['principal']}", f"- **Secundarias:** {', '.join(KEYWORDS['secundarias'])}", "",
         "## Etiquetas (copiar y pegar)", "", ", ".join(TAGS), "", "## Descripción (copiar y pegar)", "", "```", desc, "```", "",
         "## Comentario fijado", "", PINNED, "", "## Capítulos", "", *[f"- {mmss(t)} {n}" for t, n in ch], "",
         "## Configuración recomendada en YouTube Studio", "",
         "- **Idioma del video:** español (Latinoamérica). Subir `SUBTITULOS.srt` como subtítulos en español.",
         "- **Uso de IA («AI use» en Atributos): SÍ, recomendado.** Lo visual es animación claramente no realista y la música no es IA generativa. "
         "La narración, en cambio, es una voz sintética realista. La política vigente (support.google.com/youtube/answer/14328491) no la nombra "
         "entre los cuatro casos obligatorios, pero dice que divulgar «no limita la audiencia ni la elegibilidad para monetizar». "
         "YouTube también puede aplicar etiquetas automáticas. Marcarlo es la opción honesta y no tiene costo.",
         "- **Contenido para niños:** No.",
         "- **Pantalla final (últimos 20 s):** un video recomendado (sugerido: VIDEO_04, el mapa) y una lista de reproducción («GTA VI explicado»).",
         "- **Publicación sugerida:** HOY, miércoles 18/11/2026, antes de la medianoche de España (por ejemplo, 20:00 UTC = 14:00 en Ciudad de México "
         "y 15:00 en Bogotá), porque el guion habla de «mañana» y el juego se desbloquea a la medianoche local del jueves 19.",
         "- **Si se publica después del lanzamiento**, hay que cambiar tres frases y volver a generar la voz (las demás tomas están en caché): "
         "«Desde mañana vas a poder caminar…» → «Ya puedes caminar…»; «Séptima capa: la de mañana» → «Séptima capa: la de hoy»; "
         "«tu misión para mañana» → «tu misión para tu próxima partida». Comando: `python engine/build.py vx` y `python engine/vx_package.py`.", ""]
    open(f"{OUT}/PUBLICACION_YOUTUBE.md", "w", encoding="utf-8").write("\n".join(L))
    print("publicación lista ·", len(ch), "capítulos")

def visuals():
    """Exporta fotogramas clave en alta calidad a RECURSOS_VISUALES/."""
    import skia, gfx
    T = tl(); W, H = 1920, 1080; ctx = build.Ctx(V, T, W, H); groups = build.group_scenes(V, T); infos = [build.SceneInfo(g) for g in groups]
    d = os.path.join(OUT, "RECURSOS_VISUALES"); os.makedirs(d, exist_ok=True)
    picks = {"sc_hook": [0.55, 0.62, 0.9], "sc_intro": [0.85], "sc_oficial": [0.5], "sc_island": [0.75], "sc_storm": [0.7], "sc_blueprint": [0.85], "sc_white": [0.7],
             "sc_decline": [0.8], "sc_capitman": [0.9], "sc_register": [0.4], "sc_bakery": [0.9], "sc_continuity": [0.8], "sc_tv": [0.6], "sc_coda": [0.6],
             "sc_game": [0.8], "sc_game2": [0.9], "sc_2026": [0.85], "sc_phones": [0.5], "sc_loop": [0.6], "sc_guide": [0.95], "sc_close": [0.95]}
    n = 0
    for g, info in zip(groups, infos):
        nm = g["fn"].__name__
        for k, f in enumerate(picks.get(nm, [])):
            t = info.d * f; gt = g["start"] + t
            s = gfx.new_surface(W, H); c = s.getCanvas(); c.clear(skia.ColorBLACK); g["fn"](c, t, info, ctx)
            if V.get("grade"): V["grade"](c, gt, ctx)
            s.makeImageSnapshot().save(f"{d}/{n + 1:02d}_{nm[3:]}{'_' + str(k + 1) if len(picks[nm]) > 1 else ''}.png", skia.kPNG); n += 1
    shutil.copy(f"{OUT}/MINIATURA.png", f"{d}/00_miniatura.png")
    # lámina de paletas por época (referencia de dirección de arte)
    from videos.vx_lib import PASTEL, WHITE30, NEON, SEPIA, BLUE, LAYERS, cross_section
    from gfx import draw_text, rect, lin_grad
    s = gfx.new_surface(W, H); c = s.getCanvas(); c.drawRect(skia.Rect.MakeWH(W, H), lin_grad(0, 0, W, H, ["#16181B", "#2A1F38"]))
    draw_text(c, "PALETAS POR ÉPOCA · VIDEO_EXTRA", 80, 110, "abril", 64, "#F3F0E9")
    rows_ = [("1912 · 1926 (sepia)", [SEPIA["papel"], SEPIA["papel2"], SEPIA["tinta2"], SEPIA["tinta"]]),
             ("AÑOS 30 (blanco + toques)", [WHITE30["body"], WHITE30["body2"], WHITE30["jade"], WHITE30["ocre"], WHITE30["coral"]]),
             ("PLANO (años 30)", [BLUE["fondo"], BLUE["fondo2"], BLUE["linea"]]),
             ("AÑOS 70 (descolorido)", ["#B9B3A8", "#A9A59C", "#C2BBAE", "#9E9A91", "#8C877E"]),
             ("1980 · PASTEL (Horowitz)", [PASTEL[k] for k in ("rosa", "pervinca", "crema", "menta", "lavanda", "durazno", "aqua")]),
             ("2026 · NEÓN", [NEON[k] for k in ("rosa", "cian", "menta", "ambar", "lila")])]
    for i, (nm, cols) in enumerate(rows_):
        y = 180 + i * 140; draw_text(c, nm, 80, y + 70, "ovsb", 30, "#F3F0E9")
        for k, col in enumerate(cols):
            rect(c, 600 + k * 160, y + 10, 140, 100, col, 1, r=10); draw_text(c, col.upper(), 670 + k * 160, y + 132, "ovmono", 16, "#F3F0E9", 0.8, align="center")
    s.makeImageSnapshot().save(f"{d}/{n + 1:02d}_paletas_por_epoca.png", skia.kPNG); n += 1
    s = gfx.new_surface(900, 1100); c = s.getCanvas(); c.drawRect(skia.Rect.MakeWH(900, 1100), lin_grad(0, 0, 900, 1100, ["#16181B", "#2A1F38"]))
    draw_text(c, "CORTE DE PINTURA", 450, 90, "abril", 60, "#F3F0E9", align="center")
    cross_section(c, 190, 150, 520, 880, 7, 0.0, labels=True, scale_txt=1.4)
    s.makeImageSnapshot().save(f"{d}/{n + 1:02d}_corte_de_pintura.png", skia.kPNG); n += 1
    open(f"{d}/LEEME.txt", "w", encoding="utf-8").write(
        "RECURSOS VISUALES · VIDEO_EXTRA\n\nFotogramas clave del video, en 1920×1080 PNG, exportados directamente desde el motor (no son capturas del MP4 comprimido).\n"
        "Todo es ilustración vectorial original de Sal y Asfalto, dibujada por código: los hoteles MAREA, CORAL, BRISA y SOL son inventados y reúnen rasgos genéricos del art déco.\n"
        "Código fuente: engine/videos/vx_lib.py (biblioteca visual) y engine/videos/vx_scenes.py (escenas). Para regenerar: python engine/vx_package.py --visuals\n"
        "Hoja de contactos completa (un fotograma cada 5 s): VIDEO_EXTRA/recursos/hoja_de_contactos.jpg\n"
        "Música original del video: VIDEO_EXTRA/recursos/musica_original.mp3\n")
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
    args = set(sys.argv[1:]) or {"--docx", "--pub", "--visuals", "--clean"}
    if "--clean" in args: clean()
    if "--pub" in args: publication()
    if "--docx" in args: docx()
    if "--visuals" in args: visuals()
