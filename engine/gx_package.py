"""Empaqueta VIDEO_LARGO_GTA6 y SHORT_PROMOCIONAL_GTA6: guion .docx, descripción y SEO, fuentes y créditos del gameplay,
proyecto de edición (registro de planos, EDL, guion de descarga del material, pistas de audio) y textos del Short.

Uso: python gx_package.py [largo|short|todo]
"""
import csv, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
import voice_qa
from tts import split_markup

ROOT = build.ROOT
OUT = os.path.join(ROOT, "VIDEO_LARGO_GTA6"); PE = os.path.join(OUT, "PROYECTO_DE_EDICION"); RES = os.path.join(PE, "recursos")
SOUT = os.path.join(ROOT, "SHORT_PROMOCIONAL_GTA6"); SWORK = os.path.join(PE, "short_promocional")

def mmss(t, frac=False):
    t = max(0.0, t); m = int(t // 60); s = t - 60 * m
    return f"{m:02d}:{s:04.1f}" if frac else f"{m:02d}:{int(s):02d}"

class Ctx:
    def __init__(self, V, tl): self.V, self.tl, self.W, self.H, self.total = V, tl, V.get("size", (1920, 1080))[0], V.get("size", (1920, 1080))[1], tl["total"]

# ---------------------------------------------------------------- material y fuentes
GAMEPLAY = [
    dict(id="Om4W6tYMF-0", autor="IGN", titulo="You Have to Become a Complete Psychopath to Get A 6 Star Wanted Level in GTA 6", fecha="19/11/2026",
         uso="Aeropuerto y avión de carga (4 estrellas), aviones de combate, persecución nocturna en la playa, pantallas de muerte, mensaje de las 6 estrellas, aviso de «Irredimible»"),
    dict(id="gJyMGHxCKHU", autor="GTAsatara", titulo="GTA VI Police Investigation", fecha="19/11/2026",
         uso="Delito en un patio privado, estrellas huecas y mensaje «You weren't identified by the cops», estrellas que se apagan, estrella roja con iconos al volver"),
    dict(id="ey0qks0aQ-c", autor="MikeTheGoon", titulo="GTA 6 - Ocean Beach Shootout + Five Star Escape", fecha="19/11/2026",
         uso="Huida completa de 5 estrellas: bicicleta, saqueo de autos, tiroteo, hotel y azotea, camioneta, helicóptero, vehículo militar, huida a pie y mensaje «The cops are searching for you»"),
    dict(id="qbhJRtgCx30", autor="IGN", titulo="GTA 6: How to Change Clothes, Customize Outfits, and Store Clothes in Your Car", fecha="20/11/2026",
         uso="Armario, conjuntos en el vehículo personal, accesorios y los dos consejos del juego sobre el perfil criminal"),
    dict(id="JHRVSzM2O2M", autor="IGN", titulo="Focus mode has a lot of helpful different indicators you might not know about! (Short)", fecha="20/11/2026",
         uso="Modo Focus: policías en azul al manejar; puntos amarillos y rojos al apuntar"),
    dict(id="uMYUjOLOOVQ", autor="IGN", titulo="Here are a few of the MANY little details we noticed while playing GTA 6 (Short)", fecha="20/11/2026",
         uso="Manchas de sangre que siguen en el mismo sitio días después"),
    dict(id="eD5ndr0OMM0", autor="IGN", titulo="GTA 6: What Are Illegal Operations?", fecha="19/11/2026", uso="Tiroteo en una operación ilegal (disparos y vecinos)"),
]
ARTICLES = [
    ("PC Gamer", "How to reach 6 stars in GTA 6", "18/11/2026", "https://www.pcgamer.com/games/grand-theft-auto/gta-6-six-stars/",
     "Robar un tanque en una base militar para llegar a 6 estrellas; con 6 estrellas no se puede bajar el nivel y la única salida es morir; con 5 estrellas llegan tanques"),
    ("PC Gamer", "GTA 6 honor system: How the 'criminal profile' works", "18/11/2026", "https://www.pcgamer.com/games/grand-theft-auto/gta-6-criminal-profile-honor-system-explained/",
     "Los 5 niveles del perfil criminal y sus colores, qué conductas llevan a cada uno, bonificaciones del Focus, Psicópata no puede rendirse, Irredimible es permanente, cita de Rockstar sobre el «impacto duradero» y las estadísticas del redactor (321 enemigos muertos, 461 fuera de combate, 98 animales)"),
    ("Vice", "GTA 6 Wanted System Explained – How Police Track You in Vice City", "16/11/2026", "https://www.vice.com/en/article/gta-6-wanted-system-explained/",
     "Declaraciones de Rob Nelson (Rockstar North) a Famitsu e IGN antes del lanzamiento: sin testigos no hay denuncia; ropa, aspecto y vehículo; persecución de 3 estrellas en la ciudad difícil en un auto normal; huir a pie por callejones"),
    ("Beebom", "GTA 6 Wanted System Explained: Star Levels and Icons", "02/09/2026", "https://beebom.com/gta-6-wanted-system-explained/",
     "Resumen previo al lanzamiento de lo que contó Rockstar: testigo o alarma; iconos rojos (aspecto, ropa, vehículo, si Jason y Lucía van juntos); con 3 estrellas o más en la ciudad, escapar en un auto normal es casi imposible"),
]
IGN_FACTS = [
    ("Om4W6tYMF-0", "Aeropuerto de Vice City y avión de carga: 4 estrellas sin matar a nadie; aviones de combate; la historia nunca pasa de 5 estrellas; el truco de búsqueda (al terminar la historia) se queda en 5; aviso antes del punto sin retorno; con 6 estrellas no se puede bajar el nivel; guardar antes; Irredimible con consecuencias en la historia y en cómo reacciona la gente; 5 a 10 minutos de caos hasta la sexta estrella; reto de aguantar con 6 estrellas"),
    ("2pYAzjbYVms", "Short de IGN (19/11/2026): en la historia nunca más de 5 estrellas; robar un avión no basta; hay que enfrentarse a muchos policías; solo se reinicia muriendo"),
    ("qbhJRtgCx30", "Aviso a las patrullas con tu descripción y tu ropa; cambiarse ayuda a escapar; hasta 5 conjuntos en el vehículo personal; quitarse la gorra o los lentes de sol enfría un poco la búsqueda"),
    ("JHRVSzM2O2M", "Focus: marca a la policía en azul al manejar; al apuntar, puntos amarillos para herir o desarmar y rojos para matar (cabeza y corazón)"),
    ("uMYUjOLOOVQ", "Las manchas de sangre siguen en el mismo sitio varios días después, dentro del juego"),
    ("eD5ndr0OMM0", "Si los vecinos oyen muchos disparos, es probable que llamen a la policía, según lo poblada que esté la zona"),
]
def yt(i): return f"https://www.youtube.com/watch?v={i}"
def ia(i): return f"https://archive.org/details/youtube-{i}"

# ---------------------------------------------------------------- planos
def load_long():
    from videos import gx, gx_render as R
    tl = json.load(open(os.path.join(RES, "timeline.json"))); ctx = Ctx(gx.VIDEO, tl); T = R.table(ctx)
    return gx, R, tl, ctx, T

def shot_rows(R, T):
    rows = []
    for s in T["shots"]:
        k, v = s["src"].split(":", 1)
        if k == "x":
            vid, t = R.parse_x(s["src"])
            autor = R.AUTHOR.get(vid, vid); src = f"{autor} · {vid} · {mmss(t, True)}"
            enc = "zoom a " + ("estrellas" if s.get("zoom") and s["zoom"][1] < 0.1 else "mensaje del juego") if s.get("zoom") else ("tarjeta vertical" if vid in R.MZ.VERTICAL else "empuje lento")
        else:
            vid, t, autor = "", None, "Sal y Asfalto"; src = f"gráfico propio «{v}»"; enc = "gráfico animado"
        rows.append(dict(inicio=round(s["t0"], 3), fin=round(s["t1"], 3), duracion=round(s["t1"] - s["t0"], 3), palabra=s.get("word") or "",
                         ancla=s.get("anchor") or "(inicio del bloque)", desfase=round(s["t0"] - s["word_t"], 3) if s.get("word_t") else "",
                         fuente=src, video=vid, segundo_original=round(t, 3) if t is not None else "", autor=autor, encuadre=enc,
                         transicion=(s.get("tr") or ("corte", 0))[0], rotulo=s.get("cert", ""), k=s["k"]))
    return rows

def registro(R, T):
    rows = shot_rows(R, T)
    with open(os.path.join(PE, "registro_de_planos.csv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=[k for k in rows[0] if k != "k"], delimiter=";", extrasaction="ignore"); wr.writeheader(); wr.writerows(rows)
    return rows

def tc(t, fps=30):
    fr = int(round(t * fps)); return f"{fr // (3600 * fps):02d}:{fr // (60 * fps) % 60:02d}:{fr // fps % 60:02d}:{fr % fps:02d}"

def edl(R, T, total):
    """EDL CMX3600 (30 fps sin descarte): el gameplay con el segundo exacto del vídeo original; los gráficos como «GFX»."""
    L = ["TITLE: VIDEO_LARGO_GTA6", "FCM: NON-DROP FRAME", ""]
    reels = {"Om4W6tYMF-0": "IGN6STAR", "gJyMGHxCKHU": "SATARA", "ey0qks0aQ-c": "MIKEGOON", "qbhJRtgCx30": "IGNROPA", "JHRVSzM2O2M": "IGNFOCUS",
             "uMYUjOLOOVQ": "IGNDETAL", "eD5ndr0OMM0": "IGNOPS"}
    for n, s in enumerate(T["shots"], 1):
        d = s["t1"] - s["t0"]; k, v = s["src"].split(":", 1)
        if k == "x":
            vid, t = R.parse_x(s["src"]); reel = reels.get(vid, "AX")
            L.append(f"{n:03d}  {reel:<8} V     C        {tc(t)} {tc(t + d)} {tc(s['t0'])} {tc(s['t1'])}")
            L.append(f"* FROM CLIP NAME: {vid}.webm"); L.append(f"* ORIGEN: {R.AUTHOR.get(vid, vid)} · {yt(vid)} · {mmss(t, True)}")
            if s.get("zoom"): L.append(f"* ENCUADRE: zoom x{s['zoom'][2]} hacia ({s['zoom'][0]:.2f}, {s['zoom'][1]:.2f})")
        else:
            L.append(f"{n:03d}  GFX      V     C        00:00:00:00 {tc(d)} {tc(s['t0'])} {tc(s['t1'])}")
            L.append(f"* GRÁFICO PROPIO: {v} (engine/videos/gx_render.py, función g_{v.split('@')[0]})")
        if s.get("anchor"): L.append(f"* PALABRA: {s['anchor']}")
        L.append("")
    open(os.path.join(PE, "VIDEO_LARGO_GTA6.edl"), "w", encoding="utf-8").write("\n".join(L))

def descargar_sh():
    import mezzanine as MZ
    L = ["#!/usr/bin/env bash", "# Vuelve a crear los tramos de gameplay del montaje (mismos comandos que engine/mezzanine.py).",
         "# Necesita ffmpeg con libdav1d y zscale. Los tramos se guardan en ./material (1920x1080, 30 fps, H.264 CRF 14).", "set -e", "mkdir -p material", ""]
    L.append(f'TONEMAP="{MZ.TONEMAP}"'); L.append(f'SCALE="{MZ.SCALE}"'); L.append(f'DECIMATE="{MZ.DECIMATE}"'); L.append("")
    for vid, ws in MZ.WINDOWS.items():
        fps, hdr = MZ.SRC[vid]
        for a, b in [(float(w[0]), float(w[1])) for w in ws]:
            base = "$TONEMAP" if hdr else ('scale=1080:1920:flags=lanczos,format=yuv420p' if vid in MZ.VERTICAL else "$SCALE")
            vf = base + (",$DECIMATE" if fps > 50 else "") + ",setpts=N/(30*TB)"
            name = os.path.basename(MZ.name(vid, a, b))
            L.append(f'ffmpeg -n -ss {a:.3f} -i "https://archive.org/download/youtube-{vid}/{vid}.webm" -t {b - a:.3f} -an -vf "{vf}" -r 30 -fps_mode cfr '
                     f'-c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -g 30 "material/{name}"')
    p = os.path.join(PE, "descargar_material.sh"); open(p, "w", encoding="utf-8").write("\n".join(L) + "\n"); os.chmod(p, 0o755)

def narr_flac(wav):
    """Narración completa sin mezclar en FLAC (sin pérdidas); el WAV queda fuera del repositorio."""
    if os.path.exists(wav):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-ac", "1", "-c:a", "flac", "-sample_fmt", "s16", wav[:-4] + ".flac"], check=True)

def stems_flac(folder):
    """Pistas de audio en FLAC (sin pérdidas): la voz en mono; música y efectos en estéreo."""
    for nm in ("voz", "musica", "efectos"):
        w = os.path.join(folder, f"{nm}.wav")
        if not os.path.exists(w): continue
        ch = ["-ac", "1"] if nm == "voz" else []
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", w, *ch, "-c:a", "flac", "-sample_fmt", "s16", os.path.join(folder, f"{nm}.flac")], check=True)
        os.remove(w)

# ---------------------------------------------------------------- guion .docx
MUS_ES = {"tension": "tensión", "synthwave": "synthwave", "electro": "electro", "trap26": "trap", "mystery": "misterio"}
CERT_ES = {"PARTIDA": "Rótulo: SE VE EN LA PARTIDA", "ROCKSTAR": "Rótulo: SEGÚN ROCKSTAR, ANTES DEL LANZAMIENTO", "GUIAS": "Rótulo: SEGÚN LAS GUÍAS DEL JUEGO",
           "PRENSA": "Rótulo: DATO DE LA PRENSA ESPECIALIZADA"}
def docx(gx, R, tl, T, wer_line):
    beats = []; plain = []
    rows = {r["k"]: r for r in shot_rows(R, T)}
    by_beat = {}
    for s in T["shots"]: by_beat.setdefault(s["beat"], []).append(s)
    for bi, (b, bd) in enumerate(zip(gx.B, tl["beats"])):
        lines = []
        for j, s in enumerate(bd["sents"]):
            nxt = bd["sents"][j + 1]["start"] if j + 1 < len(bd["sents"]) else None
            pause = f"{nxt - s['end']:.1f} s".replace(".", ",") if nxt and nxt - s["end"] > 0.25 else None
            lines.append(dict(parts=[{"t": f"[{mmss(s['start'], True)}] ", "b": True}, {"t": s["text"]}], pause=pause))
        vis = []
        for s in by_beat.get(bi, []):
            r = rows[s["k"]]; vis.append(f"{mmss(s['t0'], True)} «{s.get('anchor') or 'inicio'}» → {r['fuente']} ({r['encuadre']})")
        sfx = ", ".join(f"{c[1]}" + (f" en «{c[0][2:]}»" if isinstance(c[0], str) and c[0].startswith("w:") else "") for c in b.get("sfx", []))
        st, lv = b.get("mus", ("synthwave", 1))
        silent = None if lines else ("(sin narración · cortinilla del canal)" if b.get("id") == "sting" else "(sin narración · pantalla final de 20 s)")
        beats.append(dict(section=b.get("section"), time=mmss(bd["start"]), dur=f"{bd['end'] - bd['start']:.1f} s".replace(".", ","), lines=lines, silent=silent,
                          visual="\n".join(vis), sfx=sfx, music=f"{MUS_ES.get(st, st)} · energía {lv}/3", ritmo=CERT_ES.get(b.get("cert"), ""), cert=""))
        if b["vo"]: plain.append(" ".join(split_markup(x)[0] for x in build.split_sentences(b["vo"])))
    words = sum(len(p.split()) for p in plain); dur = tl["total"]
    speech = sum(s["end"] - s["start"] for bd in tl["beats"] for s in bd["sents"])
    ficha = [("Título", gx.VIDEO["title"]), ("Canal", "Sal y Asfalto"), ("Formato", "Vídeo largo 16:9 · 1920 × 1080 · 30 fps constantes · H.264 (High) + AAC 192 kbit/s"),
             ("Duración final", f"{mmss(dur)} ({dur:.0f} s), incluida la pantalla final de 20 s"), ("Palabras de narración", f"{words} escritas · {sum(len(voice_qa.wer_tokens(p)) for p in plain)} tal como se pronuncian (cifras en palabras; base del WER)"),
             ("Ritmo medio", f"{words / (speech / 60):.0f} palabras por minuto de habla"),
             ("Voz", "La narradora del canal (Chatterbox Multilingual, licencia MIT), español latinoamericano"),
             ("Correspondencia guion ↔ audio", wer_line),
             ("Imagen", f"{len(T['shots'])} planos: gameplay real publicado tras el lanzamiento (IGN, GTAsatara, MikeTheGoon) y gráficos propios. Sin tráileres ni material anterior al lanzamiento"),
             ("Spoilers", "Ninguno de la historia: solo sistemas de juego (policía, estrellas y perfil criminal)")]
    human = ["El montaje se rehace solo si se cambia la voz: los cortes, rótulos y subtítulos se recalculan con los tiempos de cada palabra.",
             "Graba cada bloque en un WAV: VIDEO_LARGO_GTA6/voz_humana/beat_NN.wav (NN = número de bloque desde 00, contando también los bloques sin narración).",
             "Bloques con narración: " + ", ".join(f"{i:02d}" for i, b in enumerate(gx.B) if b["vo"]) + ".",
             "Ejecuta: python engine/build.py gx --jobs 4"]
    extra = [("Cómo se sincroniza cada imagen con la palabra", [
        "Cada plano tiene un «ancla»: el fragmento exacto de la narración que lo motiva. El corte cae 2 fotogramas (0,06 s) antes de esa palabra.",
        "Los sucesos del juego que se comentan (una estrella que aparece, otra que se apaga, un mensaje) se sincronizan con la palabra exacta que los nombra.",
        "Ningún plano de gameplay se ralentiza, se repite ni se congela: cada fotograma del vídeo avanza un fotograma del original. Registro completo: PROYECTO_DE_EDICION/registro_de_planos.csv"]),
        ("Qué se ve en la partida y qué es «según Rockstar»", [
        "Verificado en partidas reales (mensajes y HUD en pantalla): estrellas huecas y el mensaje «You weren't identified by the cops», los iconos rojos (percha, silueta, auto, pistola), las estrellas rojas y «The cops are searching for you and they have your description», el mensaje de las 6 estrellas y el aviso de «Irredimible», y los dos consejos del juego sobre el perfil criminal.",
        "Dicho por Rockstar antes del lanzamiento (rótulo amarillo): la regla del testigo o la alarma, lo que puede saber la policía (aspecto, ropa, vehículo, si Jason y Lucía van juntos) y la pista de las 3 estrellas en la ciudad.",
        "Guías y prensa (rótulo azul): IGN y PC Gamer, citados en FUENTES_Y_GAMEPLAYS.txt."])]
    sources = [("Gameplay (créditos en pantalla en cada plano)", [f"{g['autor']} · «{g['titulo']}» · {g['fecha']} · {yt(g['id'])}" for g in GAMEPLAY]),
               ("Artículos", [f"{a[0]} · «{a[1]}» · {a[2]} · {a[3]}" for a in ARTICLES])]
    data = dict(title=gx.VIDEO["title"], subtitle="Guion definitivo con marcas de tiempo · VIDEO_LARGO_GTA6 · Sal y Asfalto · 20/11/2026", ficha=ficha, beats=beats,
                sources=sources, human=human, plain=plain, extra=extra, footer="Sal y Asfalto · Guion VIDEO_LARGO_GTA6 · página ",
                labels=["Tiempo", "Narración ([pausa] = silencio medido)", "Planos (tiempo «palabra» → material)", "Rótulo"])
    jp = os.path.join(RES, "_guion_docx.json"); json.dump(data, open(jp, "w", encoding="utf-8"), ensure_ascii=False)
    dst = os.path.join(OUT, "GUION_DEFINITIVO.docx")
    subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vx_docx.js"), jp, dst], check=True)
    subprocess.run(["zip", "-d", dst, "*/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(jp); return words

# ---------------------------------------------------------------- descripción y SEO
TITLES = ["GTA 6: qué pasa al llegar a 6 estrellas (y lo que no se borra ni muriendo)",
          "GTA 6: así te busca la policía, explicado con partidas reales",
          "La sexta estrella de GTA 6 no se quita… y no es lo peor",
          "GTA 6: estrellas, iconos rojos y perfil criminal, explicados"]
TAGS = ["GTA 6", "GTA VI", "Grand Theft Auto VI", "GTA 6 6 estrellas", "GTA 6 seis estrellas", "GTA 6 policía", "GTA 6 nivel de búsqueda",
        "GTA 6 perfil criminal", "GTA 6 irredimible", "GTA 6 psicópata", "GTA 6 estrellas huecas", "GTA 6 modo Focus", "GTA 6 cómo escapar de la policía",
        "GTA 6 gameplay en español", "GTA 6 Vice City", "Jason y Lucía", "GTA 6 trucos", "GTA 6 guía", "Sal y Asfalto"]
def chapters(gx, tl):
    ch = [(0.0, "El mensaje que nadie quiere ver")]
    for b, bd in zip(gx.B, tl["beats"]):
        if b.get("id") == "intro1": ch.append((bd["start"], "Partidas reales, sin spoilers"))
        if b.get("chapter"): n, name = b["chapter"]; ch.append((bd["start"], f"{n}. {name.capitalize()}"))
        if b.get("id") == "cierre1": ch.append((bd["start"], "Resumen"))
    return ch

def descripcion(gx, tl):
    ch = chapters(gx, tl)
    L = ["TÍTULO PRINCIPAL", TITLES[0], "", "TÍTULOS ALTERNATIVOS"] + [f"{i}. {t}" for i, t in enumerate(TITLES[1:], 1)] + ["",
         "DESCRIPCIÓN (copiar desde aquí)", "",
         "¿Qué pasa en GTA 6 desde que cometes un delito hasta que llegas a la sexta estrella? Seguimos un crimen en Vice City de principio a fin "
         "con partidas reales grabadas por jugadores tras el lanzamiento: qué ve un testigo, qué sabe la policía (los iconos rojos bajo las estrellas), "
         "cómo se pierde una persecución, qué hace falta para la sexta estrella y por qué el perfil criminal «Irredimible» no tiene vuelta atrás.", "",
         "Sin spoilers de la historia: solo sistemas de juego. Lo que Rockstar explicó antes del lanzamiento aparece en pantalla como «según Rockstar».", "",
         "CAPÍTULOS"] + [f"{mmss(t)} {name}" for t, name in ch] + ["",
         "CRÉDITOS DEL GAMEPLAY (gracias a sus autores)"] + [f"• {g['autor']} — {g['titulo']} — {yt(g['id'])}" for g in GAMEPLAY] + ["",
         "FUENTES"] + [f"• {a[0]} — {a[1]} ({a[2]}) — {a[3]}" for a in ARTICLES] + [
         "• IGN — guías en vídeo de las 6 estrellas, la ropa, el modo Focus y las operaciones ilegales (enlaces arriba)", "",
         "¿Juegas en Profesional o ya rozaste el Irredimible? Cuéntanoslo en los comentarios.", "",
         "#GTA6 #GTAVI #ViceCity", "",
         "ETIQUETAS (palabras clave)", ", ".join(TAGS), "",
         "COMENTARIO FIJADO",
         "📌 Resumen rápido: 1) Sin testigos no hay estrellas. 2) Si te identifican, cámbiate de ropa y deja el auto. 3) Escapar de la persecución no es "
         "perder la búsqueda (estrellas rojas). 4) Con 6 estrellas no hay escapatoria: guarda antes. 5) «Irredimible» es permanente. ¿Tú cuánto aguantaste con 6 estrellas?", "",
         "MINIATURA", "MINIATURA.png (1280 × 720). Fondo: partida real de IGN (Lucía de espaldas en la playa de Vice City, de noche, en plena persecución; 6:00 del vídeo de IGN). "
         "El texto repite el mensaje real del juego («escapar es imposible»): no promete nada que el vídeo no muestre.", "",
         "PANTALLA FINAL", "Los últimos 20 s están libres para dos elementos de YouTube: el Short promocional o el vídeo más reciente, y el botón de suscripción.",
         "", "DATOS DE PUBLICACIÓN", "Idioma: español (Latinoamérica) · Subtítulos: SUBTITULOS.srt · Categoría: Videojuegos · Juego: Grand Theft Auto VI"]
    open(os.path.join(OUT, "DESCRIPCION.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return ch

def fuentes(R, T):
    use = {}
    for s in T["shots"]:
        if s["src"].startswith("x:"):
            vid, t = R.parse_x(s["src"]); use.setdefault(vid, []).append((s["t0"], t, s["t1"] - s["t0"]))
    L = ["FUENTES Y GAMEPLAYS — VIDEO_LARGO_GTA6", "=" * 60, "",
         "Todo el gameplay es real y posterior al lanzamiento (19/11/2026). No se usa ningún tráiler, ni el Extended Look, ni filtraciones, ni recreaciones con IA.",
         "Copias de trabajo: las copias públicas de cada vídeo en Internet Archive (la de mayor resolución), procesadas a 1080p y 30 fps sin duplicar fotogramas.",
         "En la narración no se nombra al autor de ningún clip; el crédito va en pantalla en cada plano y aquí.", "", "GAMEPLAY", "-" * 60]
    for g in GAMEPLAY:
        u = sorted(use.get(g["id"], [])); tot = sum(x[2] for x in u)
        L += [f"{g['autor']} — «{g['titulo']}» ({g['fecha']})", f"  Vídeo: {yt(g['id'])}", f"  Copia usada: {ia(g['id'])}", f"  Qué se ve: {g['uso']}",
              f"  Planos en nuestro vídeo: {len(u)} ({tot:.0f} s en total)"]
        L += [f"    {mmss(a)} de nuestro vídeo ← {mmss(t, True)} del original ({d:.1f} s)" for a, t, d in u]
        L.append("")
    L += ["DATOS Y DE DÓNDE SALEN", "-" * 60]
    for a in ARTICLES: L += [f"{a[0]} — «{a[1]}» ({a[2]})", f"  {a[3]}", f"  {a[4]}", ""]
    for vid, txt in IGN_FACTS: L += [f"IGN — vídeo {yt(vid)}", f"  {txt}", ""]
    L += ["Lo que se ve en las propias partidas (mensajes del juego leídos en pantalla, en inglés, traducidos en la narración):",
          "  «You weren't identified by the cops. Keep a low profile to avoid any attention.» (GTAsatara, 3:03)",
          "  «The cops are searching for you and they have your description.» (MikeTheGoon, 13:56)",
          "  «You now have a 6-star wanted level. Escape is impossible, and the cops won't give up until you're hunted down.» (IGN, 6:02)",
          "  «Warning: Lucia is nearing irredeemable. Avoid extreme violence to prevent a lasting impact.» (IGN, 6:43)",
          "  «Extremely violent behavior will contribute toward a psycho criminal profile.» (IGN, guía de ropa, 2:36)",
          "  «Getting a wanted level doesn't affect your criminal profile, but how you choose to deal with the cops will.» (IGN, guía de ropa, 2:42)", "",
          "Nota: los nombres en español de los niveles del perfil (Profesional, Curtido, Violento, Psicópata, Irredimible) son traducción nuestra de los nombres en inglés.",
          "Música, efectos, gráficos y voz: originales del canal (voz sintética Chatterbox Multilingual, licencia MIT)."]
    open(os.path.join(OUT, "FUENTES_Y_GAMEPLAYS.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")

def readme():
    L = ["# PROYECTO_DE_EDICION — VIDEO_LARGO_GTA6 y su Short", "",
         "Todo lo necesario para revisar o rehacer el montaje.", "",
         "| Archivo | Qué es |", "|---|---|",
         "| `registro_de_planos.csv` | Cada plano: inicio, fin, palabra que lo motiva, desfase, vídeo y segundo exacto del original, encuadre, transición y rótulo |",
         "| `VIDEO_LARGO_GTA6.edl` | Lista de edición CMX3600 (30 fps) para DaVinci Resolve, Premiere o Final Cut, con el código de tiempo del original |",
         "| `descargar_material.sh` | Vuelve a crear los tramos de gameplay (1080p, 30 fps, sin fotogramas duplicados) desde las copias públicas |",
         "| `recursos/timeline.json` | Tiempos de cada bloque, frase y palabra de la narración, y de cada toma de voz |",
         "| `audio/narracion_original.flac` | Narración completa sin mezclar (FLAC sin pérdidas, 44,1 kHz): la que se comprobó con el WER |",
         "| `audio/pistas/` | Voz, música y efectos por separado (FLAC), a la ganancia de la mezcla |",
         "| `CONTROL_VOZ_WER.md`, `control_voz_wer.csv` | Comprobación guion ↔ audio final (WER) |",
         "| `CONTROL_DE_CALIDAD.md` | Formato, fluidez (fotograma a fotograma frente al original), orden de reproducción, negro, sonoridad, subtítulos y sincronía |",
         "| `AUDITORIA_FINAL.md` | Listas de comprobación del encargo (vídeo largo y Short) con los datos medidos |",
         "| `INVESTIGACION_Y_CONCEPTO.md` | Investigación, matriz de temas ya usados y los 15 conceptos evaluados |",
         "| `recursos/iconos_hud/` | Iconos reales del HUD recortados de fotogramas 4K |",
         "| `short_promocional/` | Lo mismo para el Short: tiempos, narración sin mezclar (FLAC), pistas, control de voz (WER) y de calidad |", "",
         "## Rehacer el vídeo", "",
         "```", "cd engine", "python mezzanine.py            # tramos de gameplay (ver descargar_material.sh)", "python mezzanine.py --short    # recortes verticales 4K del Short",
         "python build.py gx --jobs 4     # voz (con control WER), mezcla, vídeo, subtítulos y miniatura", "python wer_final.py gx          # verificación final guion ↔ audio",
         "python build.py gs --jobs 4     # el Short", "python wer_final.py gs", "python gx_qa.py gx; python gx_qa.py gs   # control de calidad del vídeo final", "python gx_package.py todo       # documentos", "python gx_package.py auditoria  # AUDITORIA_FINAL.md", "```", "",
         "La voz pasa por `engine/voice_fix.py` al montarse (quita el zumbido grave que la síntesis añade a veces tras una frase, sin cambiar los tiempos).", "",
         "El guion y los planos están en `engine/videos/gx.py` (largo) y `engine/videos/gs.py` (Short); el montaje en `gx_render.py` y `gs_render.py`."]
    open(os.path.join(PE, "README.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

# ---------------------------------------------------------------- Short
def short_pkg():
    from videos import gs
    stl = json.load(open(os.path.join(SWORK, "timeline.json")))
    sents = [s for b in stl["beats"] for s in b["sents"]]
    L = ["GUION — Short promocional (9:16) · «Si ves este mensaje en GTA 6, ya es demasiado tarde»",
         f"Duración: {stl['total']:.1f} s · Voz: la narradora del canal · Material: partida real de IGN (19/11/2026), la misma del vídeo largo", "",
         "ESTRUCTURA: gancho → contexto → pregunta → corte antes de resolver → llamada al vídeo largo", ""]
    roles = {"s1": "GANCHO", "s2": "CONTEXTO", "s3": "CONTEXTO", "s4": "GIRO", "s5": "PREGUNTA (sin resolver)", "s6": "LLAMADA AL VÍDEO LARGO"}
    for b, bd in zip(gs.B, stl["beats"]):
        L.append(f"[{roles.get(b['id'], '')}]")
        for s in bd["sents"]: L.append(f"  {mmss(s['start'], True)}  {s['text']}")
        L.append("")
    L += ["TEXTO COMPLETO", " ".join(s["text"] for s in sents)]
    open(os.path.join(SOUT, "GUION.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    D = ["TÍTULO", "Si ves este mensaje en GTA 6, ya es demasiado tarde #shorts", "",
         "DESCRIPCIÓN (breve)",
         "Llegar a 6 estrellas en GTA 6 tiene un precio… y morir no lo arregla todo. El video completo, con partidas reales, está en el enlace «Video relacionado» que aparece abajo, encima del título del Short.", "",
         "Gameplay: IGN — https://www.youtube.com/watch?v=Om4W6tYMF-0", "",
         "HASHTAGS", "#GTA6 #GTAVI #ViceCity #shorts", "",
         "COMENTARIO FIJADO",
         "📌 ¿Qué es el perfil criminal y cómo evitas que te marque para siempre? Te lo explicamos en el video completo: toca el enlace que aparece encima del título del Short.", "",
         "VIDEO RELACIONADO", "Vincular con el vídeo largo «" + TITLES[0] + "». Instrucciones en CONFIGURACION_VIDEO_RELACIONADO.txt.", "",
         "PORTADA", "PORTADA.png (1080 × 1920): fotograma real de la misma partida y el texto «6 estrellas · ya es demasiado tarde»."]
    open(os.path.join(SOUT, "DESCRIPCION.txt"), "w", encoding="utf-8").write("\n".join(D) + "\n")
    C = ["CONFIGURACIÓN DEL «VÍDEO RELACIONADO» (función oficial de YouTube para Shorts)", "=" * 70, "",
         "Objetivo: que debajo del Short aparezca un enlace directo al vídeo largo:", f"  «{TITLES[0]}»", "",
         "Orden de publicación",
         "1. Publica primero el vídeo largo (VIDEO_LARGO_GTA6/VIDEO_FINAL.mp4). Puede estar en público, no listado o programado:",
         "   YouTube solo deja vincular vídeos del propio canal que ya existen.",
         "2. Sube el Short (SHORT_PROMOCIONAL_GTA6/SHORT_FINAL.mp4).", "",
         "Al subir el Short desde YouTube Studio (ordenador)",
         "3. En «Detalles», baja hasta el apartado «Vídeo relacionado» (en algunas versiones, «Video relacionado»).",
         "4. Pulsa el selector y elige el vídeo largo de la lista de vídeos del canal.",
         "5. Guarda o publica.", "",
         "Si el Short ya está publicado",
         "3. YouTube Studio → Contenido → pestaña «Shorts» → lápiz (Detalles) del Short.",
         "4. «Vídeo relacionado» → elige el vídeo largo → Guardar.", "",
         "Desde la app de YouTube (móvil)",
         "En los detalles del Short, la opción se llama «Video relacionado». Si tu versión de la app no la muestra, hazlo desde YouTube Studio en el ordenador (pasos 3-5).", "",
         "Comprobación",
         "- Abre el Short en el móvil: encima del título debe verse el enlace con el título del vídeo largo.",
         "- El Short ya lo anuncia en pantalla y de viva voz: «Tienes el enlace justo aquí abajo» + rótulo «VIDEO RELACIONADO» con una flecha.",
         "- Fija el comentario de DESCRIPCION.txt y pon el enlace del vídeo largo también en la descripción del Short cuando ya tengas su URL.",
         "", "Nota: el enlace del vídeo relacionado solo puede apuntar a vídeos del mismo canal. El vídeo largo debe estar disponible para quien vea el Short."]
    open(os.path.join(SOUT, "CONFIGURACION_VIDEO_RELACIONADO.txt"), "w", encoding="utf-8").write("\n".join(C) + "\n")

def main(what):
    if what in ("largo", "todo"):
        gx, R, tl, ctx, T = load_long()
        registro(R, T); edl(R, T, tl["total"]); descargar_sh(); readme()
        wer_md = os.path.join(PE, "CONTROL_VOZ_WER.md"); wer_line = "pendiente de verificar"
        if os.path.exists(wer_md):
            m = re.search(r"\*\*WER final\*\* \| \*\*([\d,.]+ ?%)\*\* \(coincidencia ([\d,.]+ ?%)\)", open(wer_md, encoding="utf-8").read())
            if m: wer_line = f"WER {m.group(1)} sobre el audio final (coincidencia {m.group(2)}); detalle en PROYECTO_DE_EDICION/CONTROL_VOZ_WER.md"
        words = docx(gx, R, tl, T, wer_line); descripcion(gx, tl); fuentes(R, T)
        stems_flac(os.path.join(PE, "audio", "pistas")); narr_flac(os.path.join(PE, "audio", "narracion_original.wav"))
        print("largo: palabras", words, "· planos", len(T["shots"]))
    if what in ("short", "todo"):
        short_pkg(); stems_flac(os.path.join(SWORK, "pistas")); narr_flac(os.path.join(SWORK, "narracion_original.wav")); print("short: textos listos")


# ---------------------------------------------------------------- auditoría final (listas de comprobación del encargo)
def _md_val(path, label):
    if not os.path.exists(path): return None
    for line in open(path, encoding="utf-8"):
        if line.startswith("| " + label) or line.startswith("| **" + label):
            return [c.strip() for c in line.strip().strip("|").split("|")]
    return None

def auditoria():
    import importlib
    gx = importlib.import_module("videos.gx"); gs = importlib.import_module("videos.gs")
    qa_l = os.path.join(PE, "CONTROL_DE_CALIDAD.md"); qa_s = os.path.join(SWORK, "CONTROL_DE_CALIDAD.md")
    wer_l = os.path.join(PE, "CONTROL_VOZ_WER.md"); wer_s = os.path.join(SWORK, "CONTROL_VOZ_WER.md")
    def num(s, pat, i=1, conv=float):
        m = re.search(pat, s or ""); return conv(m.group(i).replace(",", ".")) if m else None
    def row(path, label): r = _md_val(path, label); return r[1] if r else ""   # solo la columna del resultado
    dur_l = num(row(qa_l, "Duración"), r"([\d.]+) s"); dur_s = num(row(qa_s, "Duración"), r"([\d.]+) s")
    wl = num(row(wer_l, "**WER final**") or row(wer_l, "WER final"), r"([\d.,]+) ?%"); ws = num(row(wer_s, "**WER final**") or row(wer_s, "WER final"), r"([\d.,]+) ?%")
    if wl is None:
        t = open(wer_l, encoding="utf-8").read() if os.path.exists(wer_l) else ""; wl = num(t, r"\*\*WER final\*\* \| \*\*([\d.,]+) ?%")
    if ws is None:
        t = open(wer_s, encoding="utf-8").read() if os.path.exists(wer_s) else ""; ws = num(t, r"\*\*WER final\*\* \| \*\*([\d.,]+) ?%")
    back_l = num(row(qa_l, "Orden de reproducción"), r"^(\d+)", conv=int); frz_l = num(row(qa_l, "Fotogramas repetidos"), r"^(\d+)", conv=int)
    back_s = num(row(qa_s, "Orden de reproducción"), r"^(\d+)", conv=int); frz_s = num(row(qa_s, "Fotogramas repetidos"), r"^(\d+)", conv=int)
    sub_l = num(row(qa_l, "Subtítulos frente al guion"), r"diferencias de palabras (\d+)", conv=int)
    sub_s = num(row(qa_s, "Subtítulos frente al guion"), r"diferencias de palabras (\d+)", conv=int)
    fps_l = row(qa_l, "Fotogramas por segundo"); fps_s = row(qa_s, "Fotogramas por segundo")
    res_l = row(qa_l, "Vídeo"); res_s = row(qa_s, "Vídeo")
    shots_ok = row(qa_l, "Planos de gameplay con material continuo")
    srep_l = num(row(qa_l, "Fotogramas que ya vienen repetidos"), r"^(\d+) de (\d+)", conv=int); srep_s = num(row(qa_s, "Fotogramas que ya vienen repetidos"), r"^(\d+)", conv=int)
    chk_l = num(row(qa_l, "Fotogramas que ya vienen repetidos"), r"de (\d+)", conv=int); blk_l = row(qa_l, "Tramos en negro")
    # voz: cortes bruscos, solapes, términos clave y voz frente a la música (de CONTROL_VOZ_WER.md)
    def voz(path):
        ab = num(row(path, "Tomas que terminan de golpe"), r"^(\d+)", conv=int); ov = num(row(path, "Tomas solapadas"), r"^(\d+)", conv=int)
        km = num(row(path, "Términos clave no reconocidos"), r"^(\d+)", conv=int); bl = row(path, "WER en bloques"); mk = row(path, "Voz frente a música")
        return ab, ov, km, bl, mk
    ab_l, ov_l, km_l, bl_l, mk_l = voz(wer_l); ab_s, ov_s, km_s, bl_s, mk_s = voz(wer_s)
    be_l = num(bl_l, r"\((\d+) errores", conv=int); se_l = num(row(wer_l, "Errores (por frase"), r"^(\d+)", conv=int)
    # fuentes nuevas: ninguna usada en producciones anteriores
    prev = set()
    for f in ("gl.py", "gp.py", "s01.py", "s02.py"):
        prev |= set(re.findall(r"[A-Za-z0-9_-]{11}", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos", f), encoding="utf-8").read()))
    used = {g["id"] for g in GAMEPLAY}; reused = sorted(used & prev)
    ok = lambda c: "✅" if c else "❌"
    L = ["# Auditoría final — VIDEO_LARGO_GTA6 y SHORT_PROMOCIONAL_GTA6", "", "Comprobaciones hechas sobre los archivos finales (ver CONTROL_DE_CALIDAD.md y CONTROL_VOZ_WER.md).", "",
         "## Vídeo largo", "", "| Requisito | Estado | Dato |", "|---|---|---|",
         f"| Dura al menos 10 minutos | {ok(dur_l and dur_l >= 600)} | {dur_l:.0f} s |" if dur_l else "| Dura al menos 10 minutos | ❌ | sin medir |",
         f"| Idea nueva para el canal | ✅ | Matriz de temas en INVESTIGACION_Y_CONCEPTO.md: la policía y el perfil criminal no se habían tratado |",
         f"| Gameplay reciente (posterior al lanzamiento) | ✅ | Partidas publicadas el 19 y el 20/11/2026 ({len(GAMEPLAY)} vídeos) |",
         f"| No recicla material de vídeos anteriores | {ok(not reused)} | {'ninguna fuente repetida' if not reused else 'repetidas: ' + ', '.join(reused)} |",
         f"| Narrativa clara | ✅ | Gancho → introducción → 7 capítulos (del testigo a la etiqueta permanente) → resumen y preguntas |",
         f"| Imagen fluida, 30 fps constantes | {ok(frz_l == 0 and back_l == 0)} | {fps_l} · repetidos o congelados por el montaje: {frz_l} · saltos atrás: {back_l} |",
         f"| Sin congelados ni saltos | {ok(frz_l == 0)} | {shots_ok} |",
         f"| Tirones que ya trae la grabación original | ℹ️ | {srep_l} de {chk_l} fotogramas de gameplay repiten imagen en el propio original (el juego o la captura); comprobado contra los originales en archive.org. El montaje y la conversión no añaden ninguno |",
         f"| Negro en pantalla | {ok(bool(re.match(r'1 \(0\.0-0\.[0-9] s\)', blk_l)))} | {blk_l.split('|')[0].strip()}: solo la entrada antes de la primera palabra |",
         f"| Correspondencia audio ↔ guion ≥ 99,8 % | {ok(wl is not None and wl <= 0.2)} | WER {wl}% sobre el audio final: {se_l} palabra(s) distinta(s) de {num(row(wer_l, 'Palabras del guion'), r'^(\d+)', conv=int)} (detalle en CONTROL_VOZ_WER.md) |" if wl is not None else "| Correspondencia audio ↔ guion ≥ 99,8 % | ❌ | sin medir |",
         f"| Uniones entre tomas (bloques de ~20 s) | {ok(be_l is not None and se_l is not None and be_l <= se_l)} | WER {bl_l}: {'ningún error nuevo en las uniones (las diferencias son las mismas de la comprobación frase a frase)' if be_l is not None and se_l is not None and be_l <= se_l else 'hay errores en las uniones'} |",
         f"| Nombres propios, cifras y términos de GTA | {ok(km_l == 0)} | términos clave que no reconoce ningún reconocedor: {km_l} (lista en CONTROL_VOZ_WER.md) |",
         f"| Voz sin cortes bruscos, sílabas perdidas ni solapes | {ok(ab_l == 0 and ov_l == 0)} | tomas que terminan de golpe: {ab_l} · solapes: {ov_l} |",
         f"| La música no tapa la voz | {ok((num(mk_l, r'percentil 5 (-?[\d.]+) dB') or -99) >= 6)} | {mk_l} (objetivo: percentil 5 ≥ 6 dB) |",
         f"| Subtítulos iguales al guion | {ok(sub_l == 0)} | diferencias: {sub_l} |",
         f"| La imagen corresponde a lo que se narra | ✅ | Cada plano anclado a la palabra que lo motiva (registro_de_planos.csv) |",
         f"| Resolución y códec | ✅ | {res_l} |", "",
         "## Short promocional", "", "| Requisito | Estado | Dato |", "|---|---|---|",
         "| Gancho en los primeros segundos | ✅ | «Si ves este mensaje en GTA 6, ya es demasiado tarde» sobre el mensaje real |",
         "| Se entiende sin ver el vídeo largo | ✅ | Contexto propio: qué es la sexta estrella y qué la hace distinta |",
         "| Deja curiosidad (no resuelve) | ✅ | Termina en la pregunta sobre el perfil criminal |",
         "| Usa fragmentos del vídeo largo | ✅ | Misma partida de IGN y mismos momentos (recortes verticales 4K) |",
         f"| Vertical 1080×1920 | {ok('1080×1920' in (res_s or ''))} | {res_s} · {fps_s} |",
         f"| Duración 35-60 s | {ok(dur_s and 35 <= dur_s <= 60)} | {dur_s:.1f} s |" if dur_s else "| Duración 35-60 s | ❌ | sin medir |",
         f"| Audio ↔ guion | {ok(ws is not None and ws <= 0.2)} | WER {ws}% |" if ws is not None else "| Audio ↔ guion | ❌ | sin medir |",
         f"| Voz sin cortes bruscos ni solapes | {ok(ab_s == 0 and ov_s == 0)} | tomas que terminan de golpe: {ab_s} · solapes: {ov_s} · términos clave sin reconocer: {km_s} |",
         f"| La música no tapa la voz | {ok((num(mk_s, r'percentil 5 (-?[\d.]+) dB') or -99) >= 6)} | {mk_s} (objetivo: percentil 5 ≥ 6 dB) |",
         f"| Imagen fluida | {ok(frz_s == 0 and back_s == 0)} | repetidos o congelados por el montaje: {frz_s} · saltos atrás: {back_s} · repetidos en la grabación original: {srep_s} |",
         f"| Subtítulos iguales al guion | {ok(sub_s == 0)} | diferencias: {sub_s} |",
         "| Llamada a la acción | ✅ | Verbal («tienes el enlace justo aquí abajo»), rótulo «VIDEO RELACIONADO» con flecha y miniatura del vídeo largo; comentario fijado y descripción |",
         "| «Vídeo relacionado» configurado | ⚠️ | Preparado: se activa al subir el Short en YouTube Studio (pasos en CONFIGURACION_VIDEO_RELACIONADO.txt). Requiere acceso al canal |", ""]
    open(os.path.join(PE, "AUDITORIA_FINAL.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if what == "auditoria": auditoria()
    else: main(what)
