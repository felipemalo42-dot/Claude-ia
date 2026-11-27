"""Título y descripción (con capítulos sacados de la línea de tiempo real) de los vídeos 2 y 3 y sus Shorts.

Uso: python nv_package.py [jz|pv|js|ps|cv|zp|jg|tb ...]   (sin argumentos: todos)
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

VP = "Video Pump"
SRC.update({
    "vpWeazel": (VP, "Weazel Cartoon", "19/11/2026", "https://archive.org/details/videopump-2026-11-19-weazel-cartoon"),
    "vpBurger": (VP, "Big Ball Burger", "19/11/2026", "https://archive.org/details/videopump-2026-11-19-big-ball-burger"),
    "vpBradlaw": (VP, "The Brad-Law Commercial", "19/11/2026", "https://archive.org/details/videopump-2026-11-19-brad-law"),
    "vpWaffles": (VP, "They Put This Ad on TV in GTA 6: Hank's Waffles Est. 1984", "20/11/2026", "https://archive.org/details/videopump-2026-11-20-hanks-waffles"),
    "vpWestern": (VP, "They Put a Western on TV in GTA 6", "20/11/2026", "https://archive.org/details/videopump-2026-11-20-western-on-tv"),
    "vpGame": (VP, "GTA 6 has a full game inside the game (Street Trash III)", "21/11/2026", "https://archive.org/details/videopump-2026-11-21-midday"),
    "vpDive": (VP, "GTA 6 Treasure Dive Gone Wrong", "21/11/2026", "https://archive.org/details/videopump-2026-11-21-midday"),
    "P-BbiYUPD-o": ("IGN", "GTA 6 : Playing Every Arcade and Console Game", "21/11/2026", yt("P-BbiYUPD-o")),
})
CCBY = " · licencia CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); recortado y sin los textos de la edición original"
V["zp"] = dict(
    folder="SHORT_4_GTA6_ZAPPING", long=False,
    title="Hice zapping en la tele de GTA 6 #shorts",
    alts=["Esto es lo que dan en la tele de GTA 6 #shorts", "Los anuncios más locos de la tele de GTA 6 #shorts"],
    intro=("Encendimos la tele de GTA 6 y fuimos cambiando de canal: un dibujo animado con un caimán, un flamenco y un manatí, el anuncio "
           "de Big Ball Burger, el abogado 1-9-9-9 BRAD-LAW, los gofres de Hank «desde 1984» y un western con un vaquero abrazando a un puma. "
           "Todo son emisiones reales de la tele del juego, grabadas en partida."),
    credits=[(k, u + CCBY) for k, u in (("vpWeazel", "canal 1: el dibujo animado de Weazel"), ("vpBurger", "canal 2: el anuncio de Big Ball Burger"),
             ("vpBradlaw", "canal 3: el anuncio de BRAD-LAW"), ("vpWaffles", "canal 4: el anuncio de Hank's Waffles"), ("vpWestern", "canal 5 y gancho: el western"))],
    prensa=[], outro="¿Qué canal dejarías puesto?", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 tele, GTA 6 televisión, GTA 6 anuncios, GTA 6 Weazel, GTA 6 Big Ball Burger, GTA 6 Brad Law, GTA 6 Hank's Waffles, GTA 6 western, GTA 6 detalles, Sal y Asfalto")
V["jg"] = dict(
    folder="SHORT_5_GTA6_JUEGOS_DENTRO", long=False,
    title="GTA 6 tiene 4 videojuegos completos dentro #shorts",
    alts=["Los 4 juegos escondidos dentro de GTA 6 #shorts", "Un juego dentro del juego: los 4 de GTA 6 #shorts"],
    intro=("GTA 6 trae cuatro videojuegos completos dentro: Street Trash III: Dezombifier (zombis vistos desde arriba, que Jason juega con "
           "Cal en el sofá), Time Jackers (un shooter cyberpunk), Tenebrae Lux (en blanco y negro, una parodia de los juegos de exploración "
           "más pretenciosos) y Bang! For Your Buck (una recreativa de caza que hay que buscar por el mapa). Spoiler leve: la escena del sofá "
           "es de una misión del primer capítulo."),
    credits=[("vpGame", "Street Trash III y la escena del sofá" + CCBY), ("P-BbiYUPD-o", "Time Jackers, Tenebrae Lux y Bang! For Your Buck")],
    prensa=["• IGN: los cuatro juegos y sus géneros (descripción del vídeo) — " + yt("P-BbiYUPD-o"),
            "• Kotaku: los juegos de la consola y las recreativas de GTA 6 — https://kotaku.com/gta-6-arcade-games-console-rob-nelson-vice-city-interview-gta6-2000757904",
            "• Mobalytics: cómo jugar a los juegos de la consola — https://mobalytics.gg/gamebase/guides/grand-theft-auto-6-how-to-play-console-games"],
    outro="¿Cuál jugarías primero?", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 minijuegos, GTA 6 juegos dentro del juego, GTA 6 Street Trash, GTA 6 Time Jackers, GTA 6 Tenebrae Lux, GTA 6 Bang For Your Buck, GTA 6 arcade, GTA 6 consola, Sal y Asfalto")
V["tb"] = dict(
    folder="SHORT_6_GTA6_TOUR_DE_BUCEO", long=False,
    title="Reseña: el tour de buceo de GTA 6 ⭐ (SPOILER) #shorts",
    alts=["El peor tour de buceo de GTA 6 (SPOILER) #shorts", "Le doy una estrella a este tour de GTA 6 (SPOILER) #shorts"],
    intro=("AVISO: spoilers de una misión del primer capítulo. Reseñamos el tour de buceo de GTA 6: el capitán bromea con que ha hecho un "
           "agujero en el barco, el guía es en realidad Jason, el tour es una tapadera para buscar tesoros y los turistas ni siquiera lo "
           "terminan. Nota: una estrella. ¿Tú le darías más?"),
    credits=[("vpDive", "toda la partida de la misión" + CCBY)],
    prensa=["• VGC: guía de la misión del tour de buceo (la tapadera del capitán) — https://www.videogameschronicle.com/guide/gta-6-island-dreams-walkthrough/",
            "• games.gg: guía de la misión — https://games.gg/grand-theft-auto-vi/guides/island-dreams-mission-walkthrough-grand-theft-auto-6/"],
    outro="¿Tú le darías más de una estrella?", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 buceo, GTA 6 tesoro, GTA 6 doblones, GTA 6 tour de buceo, GTA 6 misión, GTA 6 spoiler, Sal y Asfalto")

SRC.update({
    "igPenta": ("IGN", "Have you found the pentagram in GTA 6?", "20/11/2026", yt("xPeXDRxVGVs")),
    "igRocket": ("IGN", "Here's how to get a free rocket launcher early in GTA 6!", "19/11/2026", yt("J-0ssekfWuc")),
    "igPlaneV": ("IGN", "You can start flying very early and easily in GTA 6", "21/11/2026", yt("WflJVoqAQQg")),
    "QBMZ1ZXlflk": ("IGN", "GTA 6 - How to Get a Free Plane or Helicopter", "20/11/2026", yt("QBMZ1ZXlflk")),
    "NKq2GOBaJV8": ("IGN", "How to Get Infinite Money in GTA 6 Very Early On", "20/11/2026", yt("NKq2GOBaJV8")),
    "igFP": ("IGN", "GTA 6 First-Person Mode Glitch: Here's how to do it!", "20/11/2026", yt("0zCHQjDWF20")),
})
V["rt"] = dict(
    folder="SHORT_7_GTA6_RITUAL_SECRETO", long=False,
    title="El ritual secreto de GTA 6 😱 #shorts",
    alts=["El secreto más terrorífico de GTA 6 #shorts", "No hagas este ritual en GTA 6 #shorts"],
    intro=("En un edificio de Capri hay un pentagrama con velas y unas notas. Si llevas a alguien inconsciente, se apagan las luces, se "
           "encienden las velas y oyes la voz de tu pareja… pero no es ella: con Lucía aparece una versión demoníaca de su madre "
           "(según IGN, con Jason es Cal). Y el cuerpo se levanta y te ataca: solo el fuego lo detiene. Spoiler leve de personajes."),
    credits=[("igPenta", "toda la partida del ritual (recorte sin los rótulos del vídeo original)")],
    prensa=[], outro="¿Te atreverías a hacerlo? Suscríbete para más secretos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 secreto, GTA 6 pentagrama, GTA 6 ritual, GTA 6 easter egg, GTA 6 terror, GTA 6 Capri, GTA 6 Lucía, Sal y Asfalto")
V["gr"] = dict(
    folder="SHORT_8_GTA6_3_COSAS_GRATIS", long=False,
    title="3 cosas GRATIS al empezar GTA 6 #shorts",
    alts=["Consigue esto GRATIS al empezar GTA 6 #shorts", "Lanzacohetes, avión y dinero gratis en GTA 6 #shorts"],
    intro=("Tres cosas gratis al empezar GTA 6: un lanzacohetes en una caravana con búnker junto al campo de tiro Griffin (con cuatro "
           "cohetes: guarda antes de disparar), aviones y un helicóptero en la pista de Southwind, al suroeste de Key Lento (sin "
           "policía, pero no vueles sobre la base militar), y una fábrica al este de Hamlet con un botín de unos 7.000 dólares que se "
           "repone si te alejas y vuelves (puede que lo arreglen en una actualización)."),
    credits=[("igRocket", "el lanzacohetes"), ("QBMZ1ZXlflk", "la pista de Southwind y el vuelo"), ("igPlaneV", "el avión gratis"),
             ("NKq2GOBaJV8", "la fábrica y el botín que se repone")],
    prensa=[], outro="¿Cuál vas a probar primero? Suscríbete para más trucos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 trucos, GTA 6 gratis, GTA 6 lanzacohetes, GTA 6 avión gratis, GTA 6 dinero infinito, GTA 6 dinero fácil, GTA 6 al empezar, Sal y Asfalto")
V["fp"] = dict(
    folder="SHORT_9_GTA6_PRIMERA_PERSONA", long=False,
    title="GTA 6 no tiene primera persona… pero hay un truco #shorts",
    alts=["Cómo jugar GTA 6 en primera persona #shorts", "El truco de la primera persona en GTA 6 #shorts"],
    intro=("GTA 6 no tiene un modo oficial en primera persona, pero hay un truco: en los ajustes del mando, cambia el botón del panel "
           "táctil (o Vista) de Mapa a Cámara; entra en un coche, saca el teléfono y guárdalo mientras pulsas sin parar el botón de "
           "cámara. Se mantiene aunque mueras y se va al cargar la partida o salir del juego. No es oficial: tiene fallos."),
    credits=[("igFP", "toda la partida en primera persona (recorte sin los rótulos del vídeo original)")],
    prensa=["• IGN: los pasos, en la guía «How to Play GTA 6 in First-Person (It's a Glitch!)» — " + yt("MVBOE2aAY_g")],
    outro="¿Lo vas a probar? Suscríbete para más trucos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 primera persona, GTA 6 first person, GTA 6 truco, GTA 6 glitch, GTA 6 cámara, Sal y Asfalto")

SRC.update({
    "GByO53W1-fI": ("IGN", "GTA 6 - How to Get the Mario and Luigi Hat Easter Egg", "23/11/2026", yt("GByO53W1-fI")),
    "IqKb-yJGroE": ("IGN", "GTA 6: How to Get the Cursed Knife | Ghost Ship Lighthouse Easter Egg", "24/11/2026", yt("IqKb-yJGroE")),
    "gNMTCbS8Ytg": ("IGN", "GTA 6 - How to Find the PS2 Vice City Easter Egg", "25/11/2026", yt("gNMTCbS8Ytg")),
    "mMBdAMjCEnE": ("Lootward", "You Can Actually Unlock HURRICANE Weather in GTA 6", "23/11/2026", yt("mMBdAMjCEnE")),
    "JPnJPuH4N6Q": ("IGN", "GTA 6: How to Get Paul Walker's Eclipse (The Fast and the Furious)", "22/11/2026", yt("JPnJPuH4N6Q")),
})
SRC.update({
    "B0b5JhrGUJQ": ("TheGamingRevolution", "GTA 6 - ALL 9 Endings Story Explained (Jason & Lucia Cutscenes)", "21/11/2026", yt("B0b5JhrGUJQ")),
    "rK6MXJpcaIA": ("Cynic", "How GTA 6's Wanted System Actually Works", "24/11/2026", yt("rK6MXJpcaIA")),
})
V["fn"] = dict(
    folder="VIDEO_LARGO_5_GTA6_FINALES", long=True,
    title="Todos los finales de GTA 6 explicados (y cómo conseguir el bueno) ⚠️ SPOILERS",
    alts=["GTA 6: los 7 finales y cómo desbloquear el final feliz (SPOILERS)",
          "¿Qué final de GTA 6 te tocó? Todos explicados (SPOILERS)",
          "El final feliz de GTA 6: requisitos y todos los demás finales (SPOILERS)"],
    intro=("⚠️ SPOILERS DEL FINAL DE GTA 6. Todos los finales, del más trágico al más feliz: los dos del ascensor, el del pantano, "
           "los del puente (Bonnie y Clyde, el salto fallido y su variante), el de la cárcel y el reencuentro familiar. Además, lo que piden "
           "las partidas publicadas para conseguir el final feliz (dos millones en el ahorro familiar, un perfil criminal bajo y perdonar al "
           "policía), la escena de después de los créditos y el misterio del archivo de Cal.\n\n"
           "Rockstar no ha dicho cuál es el final oficial. La versión «Jason libre y Lucía presa» no aparece en ninguna partida publicada: "
           "se menciona solo como rumor."),
    chapters=[("o01", "Aviso y presentación"), ("c1a", "El último golpe"), ("c2a", "Los finales del ascensor"), ("c3a", "El final del pantano"),
              ("c4a", "Los finales del puente"), ("c5a", "El final de la cárcel"), ("c6a", "El reencuentro familiar"),
              ("c7a", "Cómo conseguir el final feliz"), ("c8a", "Después de los créditos"), ("r01", "¿Cuál es el oficial?")],
    credits=[("B0b5JhrGUJQ", "todas las escenas de los finales (recortadas, sin sus rótulos ni marcas de agua). Ese vídeo reúne a su vez "
              "partidas de Sirloin (youtube.com/@Sirloin1), meloo (youtube.com/@meloo), BabyZoneGaming y Ben-Gun: gracias a todos")],
    prensa=[], outro="¿Qué final conseguiste tú? Cuéntalo en los comentarios y suscríbete para más GTA 6 contado a fondo.",
    tags="#GTA6 #GTAVI #GTA6Finales",
    keywords="GTA 6, GTA VI, GTA 6 finales, GTA 6 final feliz, GTA 6 final bueno, GTA 6 ending, GTA 6 spoilers, GTA 6 Jason Lucía, GTA 6 reencuentro, Sal y Asfalto")
V["pl"] = dict(
    folder="VIDEO_LARGO_6_GTA6_POLICIA", long=True,
    title="La policía de GTA 6: qué significa cada estrella (y cómo escapar siempre)",
    alts=["GTA 6: el sistema de búsqueda explicado con partidas reales",
          "Cómo escapar de la policía en GTA 6 (guía de estrellas e iconos)",
          "GTA 6: cómo robar sin que te atrapen"],
    intro=("Guía sin spoilers del sistema de búsqueda de GTA 6 con una partida real: las seis estrellas, qué significa cada color y forma "
           "(grises, huecas, sólidas, apagadas y rojas), los círculos del minimapa, los siete iconos de lo que la policía sabe de ti y cómo "
           "borrar cada pista, el robo limpio (cámaras, alarma y caja fuerte), joyerías, escondites de bandas y cómo huir (ruedas, helicópteros, "
           "separarse de tu pareja).\n\nLos consejos son de la partida de Cynic y de lo que se ve en ella, no reglas oficiales de Rockstar."),
    chapters=[("o01", "Presentación"), ("c1a", "Seis estrellas"), ("c2a", "Cómo leer las estrellas"), ("c3a", "Lo que saben de ti"),
              ("c4a", "El robo limpio"), ("c5p", "Joyerías y bandas"), ("c5a", "La huida"), ("r01", "Resumen")],
    credits=[("rK6MXJpcaIA", "toda la partida de la guía (sus explicaciones y consejos, contados en español)")],
    prensa=[], outro="¿Cuál es tu mejor huida? Cuéntala en los comentarios y suscríbete para más guías de GTA 6.",
    tags="#GTA6 #GTAVI #GTA6Guia",
    keywords="GTA 6, GTA VI, GTA 6 policía, GTA 6 estrellas, GTA 6 nivel de búsqueda, GTA 6 wanted, GTA 6 escapar, GTA 6 robos, GTA 6 guía, Sal y Asfalto")
V["mh"] = dict(
    folder="SHORT_10_GTA6_GORRAS_MARIO_LUIGI", long=False,
    title="¿Mario y Luigi en GTA 6? 🍄 #shorts",
    alts=["Las gorras de Mario y Luigi en GTA 6 #shorts", "El easter egg de Nintendo en GTA 6 #shorts"],
    intro=("Rockstar escondió en GTA 6 dos gorras que parecen las de Mario y Luigi. En unas ruinas junto a un río hay algo de dinero y "
           "una pipa: al usarla aparece un bloque flotando sobre las ruinas. Ponte debajo, salta… y salen dos gorras, una con la J y otra "
           "con la L. Una te la pones al momento; la de tu pareja, en el armario."),
    credits=[("GByO53W1-fI", "toda la partida del secreto")],
    prensa=[], outro="¿Qué otro guiño crees que esconde Rockstar? Suscríbete para más secretos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 easter egg, GTA 6 Mario, GTA 6 Luigi, GTA 6 Nintendo, GTA 6 gorras, GTA 6 secretos, Sal y Asfalto")
V["ck"] = dict(
    folder="SHORT_11_GTA6_BARCO_FANTASMA", long=False,
    title="El barco fantasma de GTA 6 👻 #shorts",
    alts=["No vayas a este faro a medianoche en GTA 6 #shorts", "El cuchillo maldito de GTA 6 #shorts"],
    intro=("A medianoche, en un faro al norte de Vice City, dos fantasmas discuten arriba y uno empuja al otro. Abajo hay una foto que "
           "lleva a una casa en un islote con un libro en la chimenea; después, con equipo de buceo, hay que nadar mar adentro entre la "
           "niebla hasta un bote hundido con un cuchillo verde: el cuchillo maldito. De vuelta en el faro, con binoculares, se ve el "
           "barco fantasma."),
    credits=[("IqKb-yJGroE", "toda la partida del secreto")],
    prensa=[], outro="¿Irías de noche? Suscríbete para más secretos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 barco fantasma, GTA 6 faro, GTA 6 cuchillo maldito, GTA 6 fantasmas, GTA 6 easter egg, GTA 6 misterio, Sal y Asfalto")
V["po"] = dict(
    folder="SHORT_12_GTA6_PORTAL_VICE_CITY_PS2", long=False,
    title="GTA 6 tiene un portal a la Vice City de PS2 😱 #shorts",
    alts=["Volví a la Vice City original dentro de GTA 6 #shorts", "El secreto más difícil de GTA 6 #shorts"],
    intro=("El secreto más elaborado de GTA 6: activar la torre de radio de Key Lento y recorrer doce subestaciones cuyas letras "
           "forman «Life is passing me by», el truco de GTA Vice City que adelantaba el tiempo. En cada una se pulsa un botón en el orden "
           "de ese truco, sin viaje rápido, sin conducción automática, sin morir y sin que te arresten (más o menos una hora). Al final "
           "llega el mensaje «U-235 REACTOR2» y, de noche, en la central eléctrica se abre un portal a la Vice City con aspecto de 2002. "
           "Vuelves con la camisa hawaiana de Tommy Vercetti. Lo descubrió Memeio (youtube.com/c/Memeio): todo el mérito para él."),
    credits=[("gNMTCbS8Ytg", "toda la partida del secreto")],
    prensa=[], outro="¿Lo intentarías? Suscríbete para más secretos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 Vice City, GTA Vice City, GTA 6 PS2, GTA 6 portal, GTA 6 Tommy Vercetti, GTA 6 easter egg, GTA 6 secretos, Sal y Asfalto")
V["hu"] = dict(
    folder="SHORT_13_GTA6_HURACAN_SECRETO", long=False,
    title="La misión secreta del HURACÁN en GTA 6 🌀 #shorts",
    alts=["Este tipo de GTA 6 sabía que venía el huracán #shorts", "El búnker del apocalipsis en GTA 6 #shorts"],
    intro=("En GTA 6, Freddie vive en un búnker esperando el apocalipsis, protegido con minas y drones. Si atraviesas sus defensas te "
           "invita a su pódcast… hasta que su cámara ve algo y salta el aviso de huracán. Te da dinero, te dice que lo gastes rápido y, al "
           "salir, el huracán ya está ahí. (Quien grabó la partida dice que así se desbloquea el clima de huracán; no lo hemos comprobado.)"),
    credits=[("mMBdAMjCEnE", "toda la partida de la misión")],
    prensa=[], outro="¿Te quedarías en el búnker? Suscríbete para más secretos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 huracán, GTA 6 hurricane, GTA 6 misión secreta, GTA 6 búnker, GTA 6 Freddie, GTA 6 clima, Sal y Asfalto")
V["ec"] = dict(
    folder="SHORT_14_GTA6_AUTO_PAUL_WALKER", long=False,
    title="El auto de Paul Walker está en GTA 6 💚 #shorts",
    alts=["El Eclipse de Rápido y Furioso en GTA 6 #shorts", "Cómo conseguir el auto de Brian O'Conner en GTA 6 #shorts"],
    intro=("El Eclipse verde de Brian O'Conner en la primera Rápido y Furioso está en GTA 6 como Penumbra FF, con la matrícula «HAD YOU». "
           "Está en un garaje de Vespucci: entra por la puerta lateral, abre el portón, rompe el cristal y hazle el puente (si desactivas "
           "antes la alarma, evitas a la policía). Moses lo registra gratis si es tu primer auto; si no, cuesta 6.750 dólares. Es rapidísimo "
           "pero frágil."),
    credits=[("JPnJPuH4N6Q", "toda la partida del auto")],
    prensa=[], outro="¿Vas a ir por él? Suscríbete para más secretos de GTA 6.", tags="#GTA6 #GTAVI #shorts",
    keywords="GTA 6, GTA VI, GTA 6 Paul Walker, GTA 6 Rápido y Furioso, GTA 6 Eclipse, GTA 6 Brian O'Conner, GTA 6 autos, GTA 6 easter egg, Sal y Asfalto")

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
    L += ["CRÉDITOS DEL GAMEPLAY (gracias a sus autores; " + ("también en pantalla" if v.get("onscreen", k not in ("zp", "jg", "tb", "rt", "gr", "fp", "mh", "ck", "po", "hu", "ec", "fn", "pl")) else "pégalos también en un comentario fijado") + ")"] + [credit(i, u) for i, u in v["credits"]] + [""]
    if v["prensa"]: L += ["FUENTES"] + v["prensa"] + [""]
    L += [v["outro"], "", v["tags"], "", "ETIQUETAS (palabras clave)", v["keywords"], ""]
    if v["long"]: L += [f"Duración del vídeo: {mmss(total)}", ""]
    p = os.path.join(ROOT, v["folder"], "TITULO_Y_DESCRIPCION.txt")
    open(p, "w", encoding="utf-8").write("\n".join(L)); print("escrito", p)

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(V)): write(k)
