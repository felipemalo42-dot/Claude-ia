"""Título y descripción (con capítulos sacados de la línea de tiempo real) de los vídeos 2 y 3 y sus Shorts.

Uso: python nv_package.py [jz|pv|js|ps|cv ...]   (sin argumentos: todos)
Escribe TITULO_Y_DESCRIPCION.txt en la carpeta de cada vídeo.
"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def yt(i): return f"https://www.youtube.com/watch?v={i}"
def mmss(t): t = max(0, int(t + 0.5)); return f"{t // 60:02d}:{t % 60:02d}"

# fuente → (autor, título exacto, fecha de publicación, enlace); títulos y fechas comprobados en los metadatos de Internet Archive
SRC = {
    "-UuHA1h-Cf8": ("GameV", "Can a TANK Survive a 6-STAR Police Chase in GTA 6? | PS5 Pro Gameplay", "18/11/2026", yt("-UuHA1h-Cf8")),
    "4HCd052lpnA": ("IGN", "GTA 6: You Can Steal a Fighter Jet in Chapter 1 (But Probably Shouldn't)", "20/11/2026", yt("4HCd052lpnA")),
    "3UiRmXUIE9k": ("IGN", "GTA 6: Fix Your Safehouse FIRST! | How to Fix Up Your House", "19/11/2026", yt("3UiRmXUIE9k")),
    "xnNu7YybiCM": ("IGN", "7 Optional Missions in GTA 6 You Won't Want to Miss", "19/11/2026", yt("xnNu7YybiCM")),
    "R9r9ew12GcA": ("IGN", "Drinking from this water fountain in GTA 6 can buff all of your stats instantly! (Short)", "20/11/2026", yt("R9r9ew12GcA")),
    "vpHospital1": ("Video Pump", "Wasted in GTA 6, Then a $1,191 Hospital Bill", "20/11/2026", "https://archive.org/details/videopump-2026-11-20-hospital-bill"),
    "6iQkw3J09OQ": ("IGN", "GTA 6 and the Case of the Missing Prostitutes - IGN Daily Fix", "19/11/2026", yt("6iQkw3J09OQ")),
    "cEDUO1zjB5c": ("toaster", "GTA 6 NPC Interactions Are UNREAL", "19/11/2026", yt("cEDUO1zjB5c")),
    "gvlY1gVmSKM": ("Yamatum O", "พาเที่ยวเมือง Vice City | GTA 6", "19/11/2026", yt("gvlY1gVmSKM")),
    "NwQKirh2dxE": ("LazarBeam", "Testing Everything In GTA 6", "20/11/2026", yt("NwQKirh2dxE")),
    "IG2hfrBVjh4": ("Kotaku", "How To Get A Tank And Fighter Jet In GTA 5", "16/09/2013", yt("IG2hfrBVjh4")),
    "Q5XgKNEnbP4": ("The Escapist", "HOW TO STEAL A FIGHTER JET IN GTA V", "25/09/2013", yt("Q5XgKNEnbP4")),
    "V99Ng_VTBUs": ("LOCAL GAMING", "GTA 5: Enhanced in RTX 5090 -Franklin & Chop-INSANE Ray-Tracing Ultra Realistic Graphics Gameplay 4K", "29/03/2025", yt("V99Ng_VTBUs")),
    "nqmpDCbz3lA": ("Sirloin", "The Military Base in GTA 6 - First Look", "18/11/2026", yt("nqmpDCbz3lA")),
}
def credit(i, uso): a, t, f, u = SRC[i]; return f"• {a} — {t} ({f}) — {u}\n  Usado para: {uso}"

PRENSA_JZ = [
    "• Policía de Atlanta: aviso a los jugadores (17/11/2026), recogido por Türkiye Today — https://www.turkiyetoday.com/world/atlanta-police-warn-gta-vi-players-against-bringing-video-game-crimes-into-real-life-3232672",
    "• PC Gamer: la sheriff de Miami-Dade contra la colaboración «Vice City» — https://www.pcgamer.com/games/grand-theft-auto/grand-theft-auto-is-a-videogame-franchise-built-around-criminal-activity-miami-dade-county-sheriff-comes-out-hard-against-a-proposed-gta-6-collab-with-rockstar/",
    "• Zoomg: supuestas reglas para transmitir GTA 6 en China (documento filtrado, sin confirmar) — https://www.zoomg.ir/game-news/420245-gta-6-chinese-streaming-guidelines/",
    "• IGN Daily Fix (19/11/2026): el comunicado de Rockstar sobre lo que ya no está en el juego, recogido de Shacknews — " + yt("6iQkw3J09OQ"),
    "• Insider Gaming: Rob Nelson (Rockstar North) a The Guardian sobre la empatía en GTA 6 — https://insider-gaming.com/gta-6-empathy-first-time-rockstar-history/",
    "• 80 Level: la misma entrevista, con el matiz de que el juego no castiga a quien prefiere el caos — https://80.lv/articles/gta-6-will-encourage-empathy-rockstar-says/",
]
PRENSA_PV = [
    "• GamesRadar+: Rockstar tiene un equipo de guionistas solo para lo que dicen los peatones («nadie con quien te cruzas es un extra») — https://www.gamesradar.com/games/grand-theft-auto/rockstar-has-a-whole-team-of-gta-6-writers-dedicated-to-pedestrian-dialogue-there-are-no-shortcuts-when-it-comes-to-building-a-world-like-this/",
    "• PC Guide: la misma declaración — https://www.pcguide.com/news/rockstar-games-has-a-whole-team-of-writers-for-gta-6-pedestrians-says-exec-no-one-you-meet-is-an-extra/",
    "• GamesRadar+: según Rockstar, GTA 6 lleva las interacciones con los personajes más lejos que Red Dead Redemption 2 — https://www.gamesradar.com/games/grand-theft-auto/rockstar-lead-says-gta-6-takes-npc-interactions-much-further-than-red-dead-redemption-2-and-its-system-is-returning-and-evolved/",
]

V = {}
V["jz"] = dict(
    folder="VIDEO_LARGO_3_GTA6_A_JUICIO", long=True,
    title="Llevamos GTA 6 a juicio: ¿juego de crímenes o simulador de vida?",
    alts=["GTA 6 a juicio: acusación, defensa y testigos (con partidas reales)",
          "¿GTA 6 es un simulador de crímenes? Lo juzgamos con pruebas reales",
          "Juzgamos a GTA 6: ¿culpable o inocente?"],
    intro=("¿GTA 6 es un juego de crímenes o un simulador de vida? Lo llevamos a juicio. La acusación presenta un tanque que aguanta "
           "seis estrellas, el robo de un avión de combate, la declaración de la sheriff de Miami-Dade y un documento filtrado (sin confirmar) "
           "sobre cómo transmitir el juego en China. La defensa responde con la casa que hay que arreglar, la basura que sube el Focus, "
           "las misiones secundarias más raras y una fuente que mejora tus estadísticas. Y declaran los testigos: Rockstar, Rob Nelson "
           "y la factura de 1.191 dólares del hospital.\n\n"
           "Todo son partidas reales y guías publicadas en los primeros días tras el lanzamiento. Sin spoilers de la historia: solo "
           "actividades libres. Lo que no está confirmado se dice en pantalla. El veredicto lo pones tú."),
    chapters=[("j01", "El caso contra GTA 6"), ("a01", "Sesión 1 · La acusación"), ("d01", "Sesión 2 · La defensa"),
              ("t01", "Sesión 3 · Los testigos"), ("f01", "Sesión 4 · Alegatos finales"), ("v01", "Tu veredicto")],
    credits=[("-UuHA1h-Cf8", "prueba A: el tanque y la persecución de seis estrellas"),
             ("4HCd052lpnA", "prueba B: cómo robar un avión de combate en el primer capítulo"),
             ("3UiRmXUIE9k", "defensa: arreglar la casa y las latas en el contenedor (+3 % de Focus)"),
             ("xnNu7YybiCM", "defensa y objeción: las misiones secundarias"),
             ("R9r9ew12GcA", "defensa: la fuente de Capri"),
             ("vpHospital1", "tercer testigo: la factura del hospital (solo la imagen de juego)")],
    prensa=PRENSA_JZ,
    outro="Culpable o inocente: escribe tu veredicto en los comentarios, y qué prueba te convenció.",
    tags="#GTA6 #GTAVI #ViceCity",
    keywords="GTA 6, GTA VI, Grand Theft Auto VI, GTA 6 a juicio, GTA 6 simulador de vida, GTA 6 crímenes, GTA 6 tanque 6 estrellas, GTA 6 robar avión de combate, GTA 6 arreglar la casa, GTA 6 basura Focus, GTA 6 misiones secundarias, GTA 6 fuente de Capri, GTA 6 factura del hospital, GTA 6 Rob Nelson empatía, GTA 6 sheriff Miami, GTA 6 gameplay en español, Vice City, Sal y Asfalto")
V["pv"] = dict(
    folder="VIDEO_LARGO_2_PLANETA_VICE_CITY", long=True,
    title="Planeta Vice City: el documental de los humanos de GTA 6",
    alts=["Así viven los habitantes de GTA 6 (documental de naturaleza)",
          "Estudiamos a los NPC de GTA 6 como si fueran animales salvajes",
          "Los humanos de Vice City: un documental con partidas reales de GTA 6"],
    intro=("Un documental de naturaleza diferente: la especie que estudiamos son los habitantes de Vice City, las personas que GTA 6 "
           "mueve por su cuenta. Su hábitat (playas, avenidas y gimnasios al aire libre), sus rituales, cómo se comunican, quién es su "
           "depredador, cómo reaccionan en grupo y con qué otras especies conviven. Y un detalle del propio juego: al acercarte a alguien, "
           "el menú lo clasifica como turista o como local.\n\n"
           "Todo son partidas reales publicadas en los primeros días tras el lanzamiento. Las frases de los habitantes son las originales "
           "del juego (en inglés en pantalla, traducidas en la narración). Lo que dijo Rockstar aparece como «según Rockstar». "
           "Sin spoilers de la historia. El nombre científico de la ficha es una broma: no existe."),
    chapters=[("p01", "Bienvenidos a Planeta Vice City"), ("h01", "1. El hábitat"), ("r01", "2. Rituales"), ("c01", "3. Comunicación"),
              ("d01", "4. Depredadores"), ("m01", "5. La manada"), ("e01", "6. Otras especies"), ("o01", "7. El observador"),
              ("z01", "Tu turno")],
    credits=[("gvlY1gVmSKM", "la playa, las avenidas, el gimnasio al aire libre, el saludo, la etiqueta turista/local, el hotel, las carreras y la noche"),
             ("cEDUO1zjB5c", "los encuentros con los habitantes y sus frases, el atraco, la manada y el repartidor"),
             ("NwQKirh2dxE", "el zoológico: tigres, aviario y orcas (encuadre sin la cámara del creador)")],
    prensa=PRENSA_PV,
    outro="¿Qué es lo más raro que has visto hacer a un habitante de Vice City? Cuéntanoslo en los comentarios.",
    tags="#GTA6 #GTAVI #ViceCity",
    keywords="GTA 6, GTA VI, Grand Theft Auto VI, GTA 6 NPC, GTA 6 habitantes, GTA 6 documental, Planeta Vice City, GTA 6 reacciones NPC, GTA 6 interacciones, GTA 6 playa, GTA 6 gimnasio, GTA 6 zoológico, GTA 6 turista local, GTA 6 frases NPC, GTA 6 gameplay en español, Vice City, Sal y Asfalto")
V["js"] = dict(
    folder="SHORT_3_GTA6_A_JUICIO", long=False,
    title="En GTA 6, si te matan, te cobran el hospital #shorts",
    alts=["GTA 6 te cobra 1.191 dólares de hospital #shorts", "¿GTA 6 es un juego de crímenes o un simulador de vida? #shorts"],
    intro=("En GTA 6, si te matan, despiertas junto a la carretera con un cargo de 1.191 dólares de hospital. Pero si sacas la basura, "
           "el Focus sube un 3 %. Y en el primer capítulo ya puedes robar un avión de combate. ¿Juego de crímenes o simulador de vida? "
           "Lo llevamos a juicio con pruebas reales: vídeo completo «Llevamos GTA 6 a juicio» en el canal."),
    credits=[("vpHospital1", "la factura del hospital (solo la imagen de juego)"), ("3UiRmXUIE9k", "las latas en el contenedor (+3 % de Focus)"),
             ("4HCd052lpnA", "el robo del avión de combate")],
    prensa=[], outro="¿Culpable o inocente? Tu veredicto, en los comentarios.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 hospital, GTA 6 factura, GTA 6 Focus, GTA 6 avión de combate, GTA 6 a juicio, Sal y Asfalto")
V["ps"] = dict(
    folder="SHORT_2_PLANETA_VICE_CITY", long=False,
    title="Así reacciona un habitante de GTA 6 cuando invades su espacio #shorts",
    alts=["Los NPC de GTA 6 no se dejan #shorts", "Nunca toques a un desconocido en GTA 6 #shorts"],
    intro=("«No me hables». «¿Quién te dio permiso para tocarme?». Así reaccionan los habitantes de Vice City cuando el jugador se acerca "
           "demasiado, con sus frases originales. Los estudiamos como a una especie salvaje en «Planeta Vice City», el documental completo "
           "en el canal."),
    credits=[("cEDUO1zjB5c", "los encuentros con los habitantes y sus frases")],
    prensa=[], outro="¿Qué es lo más raro que te ha dicho un habitante de Vice City?", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 NPC, GTA 6 reacciones, GTA 6 frases, Planeta Vice City, Sal y Asfalto")

V["cv"] = dict(
    folder="VIDEO_LARGO_4_GTA5_VS_GTA6", long=True,
    title="GTA 5 vs GTA 6: 8 asaltos con partidas reales",
    alts=["GTA 5 contra GTA 6: el combate (sin comparar gráficos)",
          "¿De verdad ha cambiado tanto? GTA 5 vs GTA 6 en 8 asaltos",
          "Pusimos a GTA 5 y GTA 6 frente a frente: este es el marcador"],
    intro=("Trece años separan a GTA 5 de GTA 6. ¿De verdad ha cambiado tanto? Los ponemos frente a frente en un combate de ocho "
           "asaltos, con la misma situación en los dos juegos y partidas reales de cada uno: la ciudad, la policía, robar un avión de "
           "combate, el tanque, la gente, morir, los poderes y la fluidez. Cada asalto tiene un veredicto razonado, y si no hay forma "
           "justa de decidirlo, es empate.\n\n"
           "No comparamos gráficos: las imágenes de GTA 5 vienen de versiones distintas (2013 y la edición mejorada para PC). "
           "Sin spoilers de la historia de GTA 6: solo cosas que puedes hacer por tu cuenta. Los datos de prensa se dicen con su fuente."),
    chapters=[("o01", "El combate"), ("c01", "Asalto 1 · La ciudad"), ("p01", "Asalto 2 · La policía"), ("j01", "Asalto 3 · El caza"),
              ("t01", "Asalto 4 · El tanque"), ("g01", "Asalto 5 · La gente"), ("m01", "Asalto 6 · Morir"), ("h01", "Asalto 7 · Los poderes"),
              ("f01", "Asalto 8 · La fluidez"), ("r01", "El marcador final")],
    credits=[("IG2hfrBVjh4", "GTA 5: Fort Zancudo, el tanque y el caza (guía de 2013)"),
             ("Q5XgKNEnbP4", "GTA 5: cómo robar el caza con Franklin y la pantalla de muerte (guía de 2013)"),
             ("V99Ng_VTBUs", "GTA 5 (edición mejorada para PC): Los Santos, Grove Street, Franklin y Chop"),
             ("-UuHA1h-Cf8", "GTA 6: el tanque y la persecución de seis estrellas"),
             ("4HCd052lpnA", "GTA 6: cómo robar un avión de combate en el primer capítulo"),
             ("nqmpDCbz3lA", "GTA 6: la base militar, el blindado y la valla"),
             ("cEDUO1zjB5c", "GTA 6: el menú para hablar con la gente, sus respuestas y el robo de la bolsa"),
             ("gvlY1gVmSKM", "GTA 6: Vice City, la playa, el gimnasio al aire libre y la etiqueta de turista o local"),
             ("3UiRmXUIE9k", "GTA 6: el Focus (+3 % al tirar las latas a la basura)"),
             ("vpHospital1", "GTA 6: la factura del hospital (solo la imagen de juego)")],
    prensa=["• Newsweek: la nueva policía de GTA 6 (testigos, alarmas, cámaras, estrellas vacías y lo que sabe de ti) — https://www.newsweek.com/gta-6s-new-police-system-ends-the-easy-getaway-with-flock-like-cameras-12743394",
            "• PC Gamer: cómo se llega a seis estrellas y por qué ya no se pueden perder — https://www.pcgamer.com/games/grand-theft-auto/gta-6-six-stars/",
            "• GTA Wiki: la factura del hospital en GTA 5 (hasta 5.000 dólares, según el dinero que lleves) — https://gta.wiki/w/Hospitals",
            "• TweakTown: GTA 5 en PS5 y Xbox Series con modo de 60 imágenes por segundo (2022) — https://www.tweaktown.com/news/84910/gta-has-4k-60fps-raytracing-mode-on-ps5-xbox-series/index.html",
            "• TweakTown: según Rockstar, GTA 6 funciona a 30 y su equipo técnico aún no tenía claro un modo de 60 — https://www.tweaktown.com/news/113337/rockstar-says-gta-6-will-run-at-30-fps-and-its-tech-team-is-still-unsure-about-a-60-fps-mode/index.html",
            PRENSA_PV[2]],
    outro="¿Cuál es tu marcador? Escribe en los comentarios qué asalto le darías a cada uno.",
    tags="#GTA6 #GTA5 #GTAVI",
    keywords="GTA 5 vs GTA 6, GTA V vs GTA VI, GTA 6 vs GTA 5 comparación, GTA 6 diferencias con GTA 5, GTA 6 seis estrellas, GTA 6 policía testigos, GTA 6 robar avión de combate, GTA 5 Fort Zancudo, GTA 6 tanque, GTA 6 NPC calmar provocar, GTA 6 factura del hospital, GTA 5 habilidades especiales, GTA 6 Focus, GTA 6 30 fps, GTA 5 60 fps, GTA 6 gameplay en español, Vice City, Los Santos, Sal y Asfalto")

def chapters(v):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import importlib
    m = importlib.import_module(f"videos.{k_of(v)}")
    tl = json.load(open(os.path.join(ROOT, v["folder"], "trabajo", "timeline.json")))
    ids = [b.get("id") for b in m.B]; out = []
    for bid, name in v["chapters"]:
        st = 0.0 if not out else tl["beats"][ids.index(bid)]["start"]
        out.append((st, name))
    for (a, _), (b, _) in zip(out, out[1:]): assert b - a >= 10, "capítulo de menos de 10 s"
    return out, tl["total"]

def k_of(v): return [k for k, x in V.items() if x is v][0]

def write(k):
    v = V[k]; L = ["TÍTULO", v["title"], "", "TÍTULOS ALTERNATIVOS"] + [f"{i + 1}. {a}" for i, a in enumerate(v["alts"])]
    L += ["", "DESCRIPCIÓN (copiar desde aquí)", "", v["intro"], ""]
    if v["long"]:
        ch, total = chapters(v)
        L += ["CAPÍTULOS"] + [f"{mmss(t)} {n}" for t, n in ch] + [""]
    L += ["CRÉDITOS DEL GAMEPLAY (gracias a sus autores; también en pantalla)"] + [credit(i, u) for i, u in v["credits"]] + [""]
    if v["prensa"]: L += ["FUENTES"] + v["prensa"] + [""]
    L += [v["outro"], "", v["tags"], "", "ETIQUETAS (palabras clave)", v["keywords"], ""]
    if v["long"]: L += [f"Duración del vídeo: {mmss(total)}", ""]
    p = os.path.join(ROOT, v["folder"], "TITULO_Y_DESCRIPCION.txt")
    open(p, "w", encoding="utf-8").write("\n".join(L)); print("escrito", p)

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(V)): write(k)
