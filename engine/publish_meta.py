"""Metadatos de publicación de los 10 vídeos + generador de paquetes (publicacion.md, descripción, etiquetas, narración, hoja de contactos)."""
import json, os, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

AI_NO = ("**Casilla “contenido alterado o sintético”: NO.** Todo el material visual es animación/infografía claramente no realista "
         "y la voz sintética no imita a ninguna persona real ni presenta hechos inventados como reales. Según los ejemplos de YouTube, "
         "esto no exige la etiqueta. Por transparencia, la descripción lo declara igualmente.")
DISCLOSE_LINE = ("ℹ️ Transparencia: narración con voz sintética (modelo Chatterbox de Resemble AI, licencia MIT, con marca de agua inaudible) y animaciones originales de Sal y Asfalto. "
                 "Este video NO contiene imágenes, música ni material de Rockstar Games. GTA y Grand Theft Auto son marcas de Take-Two Interactive; "
                 "canal independiente, sin relación con Rockstar Games.")
COMMON_LIC = [
    "Música y efectos: compuestos y sintetizados por código para este video (engine/audio.py) · obra original, sin muestras de terceros.",
    "Voz: Chatterbox Multilingual de Resemble AI (licencia MIT) con referencia de una locutora anónima del corpus abierto OpenSLR SLR72 (Google, CC BY-SA 4.0; atribución: Guevara-Rukoz et al., LREC 2020). Ver engine/voces/README.md.",
    "Verificación y sincronización de la voz: reconocedor Parakeet TDT v3 de NVIDIA (CC-BY-4.0), usado solo como herramienta; no aparece en el video.",
    "Tipografías: Google Fonts con licencia SIL OFL 1.1 o Apache 2.0 (Anton, Inter, JetBrains Mono y las específicas del video).",
    "Gráficos: dibujados por código con Skia (BSD) · iconos propios (rutas SVG originales en engine/gfx.py).",
    "Codificación: FFmpeg (libx264 / AAC).",
]

META = {
"v01": dict(
    titles=["GTA 6: hora exacta en tu país, precio, peso e idioma — 7 cosas que revisar antes de medianoche",
            "GTA 6 sale a medianoche: la lista de 7 comprobaciones para no quedarte afuera",
            "¿A qué hora, cuánto cuesta y cuánto pesa GTA 6? Todo antes del 19 de noviembre",
            "GTA 6: antes de jugar revisa esto (hora local, 210 GB, precio en pesos y subtítulos)"],
    kw="gta 6 hora de lanzamiento", kw2=["gta 6 precio méxico", "gta 6 precio colombia", "gta 6 cuánto pesa", "gta 6 en español", "gta 6 ps4", "gta 6 pc", "gta 6 online", "gta 6 precarga"],
    intent="Informativa urgente (pre-lanzamiento): resolver todas las dudas prácticas en un solo lugar.",
    audience="Jugadores hispanohablantes que van a comprar o ya compraron GTA VI y quieren jugar la noche del lanzamiento.",
    dur="4:29 (formato largo compacto).", why="Promete y entrega una lista clara y verificada en 7 puntos, con datos locales (México, Colombia, Argentina, España) que los medios dan contradictorios.",
    desc="GTA 6 se desbloquea a la medianoche HORA LOCAL del jueves 19 de noviembre de 2026. En este video revisamos las 7 cosas que tienes que tener listas antes: consola, espacio (≈210 GB), precarga, hora por país, precio, idioma y modo online.\n\nEn Sal y Asfalto manda el semáforo: lo OFICIAL en verde, lo DEDUCIDO en amarillo y el RUMOR en rojo.",
    tags=["gta 6", "gta vi", "gta 6 hora", "gta 6 hora de lanzamiento", "a qué hora sale gta 6", "gta 6 precio", "gta 6 precio méxico", "gta 6 precio colombia", "gta 6 cuánto pesa", "gta 6 210 gb", "gta 6 español", "gta 6 doblaje latino", "gta 6 ps5", "gta 6 xbox series", "gta 6 ps4", "gta 6 pc", "gta 6 online", "gta 6 precarga", "grand theft auto 6", "sal y asfalto"],
    pinned="📌 Resumen rápido: 00:00 hora local del jueves 19 · ≈210 GB · PS5 y Xbox Series (no PS4/One, no PC aún) · voces en inglés con textos en español de México y de España · sin online por ahora. ¿Desde qué país lo vas a jugar y a qué hora te toca? 👇",
    sources=["Forbes (12 y 16 nov. 2026): hora de desbloqueo y tamaño", "El Comercio / eldiario.es / Heraldo Binario: horarios por país; PS Store México: 00:00 del 19 (hora del centro)",
             "Hollywood Reporter: precio 79,99 / 99,99 USD", "Bloomberg Línea / ADN40 (nov. 2026): precios en México y Colombia", "Notebookcheck / gta6filesize: 209,86 GB en Xbox Store",
             "Vice / Timesaver: actualización 1.002", "Vandal / Microsoft Store: idiomas", "FAQ de PlayStation y Take-Two: un jugador; soporte a GTA Online",
             "Wccftech / Digital Citizen: sin fecha de PC", "GameSpot: espacio útil de PS5 (667 GB) y Series S (364 GB)"],
    lic_extra=["Fuentes: Barlow Condensed (OFL)."],
    status="TERMINADO · listo para publicar", phase="Pre-lanzamiento (100 % producible con información oficial)",
    risk="Datos de precio y tamaño pueden variar por región o por parche: verifica tu tienda antes de publicar. Riesgo de copyright: nulo (sin material de terceros)."),
"v02": dict(
    titles=["¿A qué hora sale GTA 6 en tu país? (medianoche local, 19 de noviembre) #shorts",
            "GTA 6: la medianoche recorre el mundo — tu hora exacta #shorts", "Hora de GTA 6 en México, Colombia, Argentina y España #shorts", "GTA 6 sale a las 00:00… ¿de dónde? #shorts"],
    kw="a qué hora sale gta 6", kw2=["gta 6 hora méxico", "gta 6 hora colombia", "gta 6 hora argentina", "gta 6 hora españa", "gta 6 medianoche"],
    intent="Informativa urgente, consumo móvil.", audience="Jugadores LatAm/España que buscan su hora exacta desde el móvil.", dur="0:41 (Short vertical 9:16).",
    why="Responde la pregunta exacta en menos de un minuto con un globo 3D que la hace visual y compartible.",
    desc="GTA 6 se desbloquea a la medianoche HORA LOCAL del jueves 19 de noviembre de 2026. España 00:00 · Argentina/Chile 00:00 (04:00 en España) · Colombia/Perú/Ecuador 00:00 (06:00 en España) · México centro 00:00 (07:00 en España). Manda la ficha de tu tienda.",
    tags=["gta 6", "gta 6 hora", "a qué hora sale gta 6", "gta 6 méxico", "gta 6 colombia", "gta 6 argentina", "gta 6 españa", "gta 6 shorts", "shorts"],
    pinned="📌 Regla única: 00:00 de TU hora local del jueves 19. Si tu tienda dice otra cosa, manda la tienda. ¿De qué país eres? 🌎",
    sources=["Soporte de Rockstar (3 nov. 2026), vía prensa", "PS Store México (00:00 del 19, hora del centro)", "Forbes (12 nov. 2026): EE. UU. abre a las 00:00 ET"],
    lic_extra=["Mapa del mundo: Natural Earth (dominio público)."], status="TERMINADO · listo para publicar", phase="Pre-lanzamiento",
    risk="Caduca tras el lanzamiento (diseñado para 24-48 h). Sin riesgo de copyright."),
"v03": dict(
    titles=["GTA 6 para PC y Android: la verdad (y la estafa que está robando cuentas)",
            "NO descargues “GTA 6 PC gratis”: así funciona el malware que roba tus cuentas",
            "GTA 6 APK y GTA 6 PC: por qué son falsos y qué hacer si ya lo instalaste",
            "La descarga más peligrosa de noviembre: anatomía de la estafa de GTA 6"],
    kw="gta 6 pc descargar", kw2=["gta 6 apk", "gta 6 android", "gta 6 gratis", "gta 6 malware", "gta 6 estafa", "gta 6 para pc"],
    intent="Navegacional riesgosa → la convertimos en protección (servicio público).",
    audience="Jugadores sin PS5/Series que buscan alternativas, sobre todo en Latinoamérica; padres y familiares.",
    dur="3:24", why="Ocupa una búsqueda masiva dominada por contenido engañoso con información verificada por empresas de seguridad (ESET, Cynet) y pasos de recuperación útiles.",
    desc="No existe GTA 6 para PC (sin fecha anunciada), ni para Android ni para iPhone. Los archivos que lo prometen son malware: ESET detectó “gta6_installer.exe” con el infostealer Vidar y Cynet otra variante con WARDEN. En este video: cómo funciona el anzuelo, qué roba y qué hacer si ya lo ejecutaste.",
    tags=["gta 6 pc", "gta 6 pc descargar", "gta 6 apk", "gta 6 android", "gta 6 gratis", "gta 6 descargar", "gta 6 malware", "gta 6 estafa", "gta 6 virus", "seguridad gamer", "infostealer", "gta 6", "sal y asfalto"],
    pinned="📌 Si ya ejecutaste un “instalador de GTA 6”: 1) desconecta y analiza el equipo, 2) cambia contraseñas desde OTRO dispositivo (empieza por el correo), 3) cierra sesiones y activa 2FA. Comparte esto con quien lo necesite 🛡️",
    sources=["Help Net Security (13 nov. 2026): falsa descarga de GTA 6 que roba credenciales de Steam y monederos", "Security Boulevard (nov. 2026): “GTA 6 download” como búsqueda peligrosa",
             "Shattered.io: ESET y Vidar en gta6_installer.exe", "Neowin: estafas de descarga gratuita", "Take-Two: sin fecha para PC"],
    lic_extra=["Fuentes: Share Tech Mono, VT323 (OFL). Interfaces (buscador, diálogos) genéricas e inventadas: no imitan ninguna marca."],
    status="TERMINADO · listo para publicar", phase="Pre-lanzamiento (útil también durante los 30 días posteriores)",
    risk="Tema sensible pero educativo: no muestra cómo crear malware, solo cómo reconocerlo. Sin enlaces a sitios maliciosos. Revisa la política de YouTube sobre engaños: no aplica (contenido de prevención)."),
"v04": dict(
    titles=["El mapa de GTA 6 explicado: las 6 regiones de Leonida y los lugares reales que las inspiran",
            "Leonida región por región: lo que Rockstar confirmó del mapa de GTA 6 (y lo que no)",
            "Mapa de GTA 6: Vice City, Grassrivers, Ambrosia y más… sobre la Florida real",
            "Viajamos por Leonida antes del lanzamiento: 6 regiones, 6 pistas reales"],
    kw="mapa gta 6", kw2=["leonida gta 6", "regiones gta 6", "vice city gta 6", "grassrivers", "port gellhorn", "ambrosia gta 6", "mount kalaga", "leonida keys"],
    intent="Exploración y curiosidad pre-lanzamiento.", audience="Fans que quieren entender el mundo antes de jugar; interesados en Florida/Miami.",
    dur="3:31", why="Combina datos oficiales con inspiraciones reales, marcando qué es deducción; animación 3D original que evita los mapas falsos que circulan.",
    desc="Rockstar no ha publicado un mapa completo de Leonida. Con lo oficial (6 regiones, Mount Kalaga en la frontera norte, Ambrosia en el corazón del estado, el mapa “el doble que el de GTA 5” según Aaron Garbut en Game Informer) y la geografía real de Florida, recorremos Mount Kalaga, Port Gellhorn, Ambrosia, Grassrivers, Vice City y Leonida Keys.\n\n⚠️ El mapa que ves es la FLORIDA REAL (Natural Earth), no el mapa del juego.",
    tags=["mapa gta 6", "gta 6 mapa", "leonida", "vice city", "grassrivers", "port gellhorn", "ambrosia", "mount kalaga", "leonida keys", "gta 6 florida", "gta 6 regiones", "gta 6", "sal y asfalto"],
    pinned="📌 Marcador de deducciones: el jueves volvemos a este mapa con el juego y marcamos aciertos ✅ y fallos ❌. ¿A qué región vas primero?",
    sources=["Web oficial de Rockstar (regiones y descripciones), vía GTA BOOM / The Games Wiki / guías que la citan", "Game Informer n.º 382 (Aaron Garbut: mapa el doble que GTA V; +170 especies)",
             "Clewiston, “America's Sweetest Town” (dato real)", "Britton Hill, ≈105 m, punto más alto de Florida (dato real)"],
    lic_extra=["Geografía: Natural Earth 1:50m (dominio público).", "Fuentes: DM Serif Display (OFL)."],
    status="TERMINADO · listo para publicar", phase="Pre-lanzamiento (actualizar con comentario fijado tras jugar)",
    risk="Las ubicaciones de Port Gellhorn y Grassrivers son deducciones (se dice en voz alta y en pantalla). Sin uso de mapas oficiales."),
"v05": dict(
    titles=["Jason y Lucía: todo lo que Rockstar ya contó de los protagonistas de GTA 6 (sin spoilers)",
            "Expediente Jason y Lucía: quiénes son los protagonistas de GTA 6", "GTA 6: la historia de Jason y Lucía antes de jugar (solo datos oficiales)",
            "Lucía salió de prisión, Jason trabaja para traficantes: el expediente de GTA 6"],
    kw="jason y lucia gta 6", kw2=["lucia gta 6", "jason gta 6", "personajes gta 6", "historia gta 6", "reparto gta 6", "cal hampton", "boobie ike"],
    intent="Narrativa / contexto de historia sin spoilers.", audience="Jugadores que quieren llegar al juego entendiendo a los personajes; público que sigue la historia.",
    dur="3:06", why="Formato de expediente con fuentes y etiquetas de certeza; evita spoilers y especulación disfrazada.",
    desc="Lo que Rockstar publicó sobre Jason Duval y Lucía Caminos (web oficial y tráileres), lo que reportó la prensa y lo que aún no sabemos. Sin spoilers.",
    tags=["jason y lucia", "lucia gta 6", "jason gta 6", "personajes gta 6", "historia gta 6", "gta 6 sin spoilers", "cal hampton", "boobie ike", "real dimez", "raul bautista", "brian heder", "gta 6", "sal y asfalto"],
    pinned="📌 Cero spoilers en este canal durante la primera semana. ¿Con quién vas a jugar más: Jason o Lucía? 💗🩵",
    sources=["Web oficial de Rockstar (perfiles de personajes, mayo 2025) vía VGC / GamesRadar / PCGamesN", "Descripción oficial del tráiler 2 (mayo 2025)",
             "Tráiler de lanzamiento (15 oct. 2026) vía GameSpot / Vice", "Extended Look (agosto 2026) vía TechRadar / Red Bull", "Rob Nelson (Rockstar) sobre el Perfil Criminal, vía prensa"],
    lic_extra=["Siluetas genéricas dibujadas por código: no reproducen el aspecto de ningún personaje.", "Fuentes: Special Elite (Apache 2.0), Courier Prime (OFL), Permanent Marker (Apache 2.0)."],
    status="TERMINADO · listo para publicar", phase="Pre-lanzamiento (válido durante la primera semana)",
    risk="Las descripciones son paráfrasis en español de textos oficiales: verifica la redacción en rockstargames.com/VI antes de publicar. La “relación opcional” se presenta como REPORTADO/SIN CONFIRMAR."),
"v06": dict(
    titles=["GTA 6 vs GTA 5: 10 cambios confirmados, 1 que no cambió y 3 rumores",
            "GTA 6 contra GTA 5: lo que de verdad cambia (sin humo)", "13 años después: 10 diferencias confirmadas entre GTA 5 y GTA 6",
            "GTA 6 vs GTA 5: mapa, estrellas, protagonistas, precio y más"],
    kw="gta 6 vs gta 5", kw2=["diferencias gta 5 gta 6", "gta 6 estrellas", "perfil criminal gta 6", "gta 6 huracanes", "gta 6 animales", "gta 6 60 fps"],
    intent="Comparativa.", audience="Jugadores veteranos de GTA V que deciden cuánto cambia la experiencia.", dur="3:19",
    why="Formato rápido de rondas con fuentes; separa los 3 rumores más repetidos con etiqueta propia.",
    desc="Diez cambios confirmados entre GTA 5 y GTA 6 (mapa, protagonistas, estrellas, Perfil Criminal, foco, clima, fauna, precio, online y plataformas), lo que no cambió (el idioma) y tres rumores señalados.",
    tags=["gta 6 vs gta 5", "gta 5 vs gta 6", "diferencias gta 6", "gta 6 cambios", "gta 6 estrellas", "perfil criminal", "gta 6 huracanes", "gta 6 animales", "gta 6 precio", "gta 6 60 fps", "gta 6", "sal y asfalto"],
    pinned="📌 ¿Cuál es el cambio más importante para ti? Después del jueves hacemos la comparación JUGANDO, con pruebas propias. 🎮",
    sources=["Game Informer n.º 382 (mapa ×2, clima, +170 especies)", "Extended Look (Rockstar, agosto 2026) vía TechRadar / Red Bull", "Rob Nelson (Rockstar), vía prensa",
             "Hollywood Reporter (precio)", "FAQ de PlayStation / Take-Two (un jugador)", "TweakTown / RockstarINTEL (objetivo 30 fps)", "Historial de lanzamiento de GTA V (2013, PC en 2015)"],
    lic_extra=["Fuentes: Anton (OFL)."], status="TERMINADO · listo para publicar", phase="Pre-lanzamiento y primera semana",
    risk="Datos de GTA V de conocimiento público. Ninguna imagen de GTA V/VI."),
"v07": dict(
    titles=["GTA 6 pesa 210 GB: ¿te cabe en tu consola? #shorts", "¿Te cabe GTA 6? PS5 vs Series S #shorts", "210 GB: el examen de espacio de GTA 6 #shorts", "GTA 6 y tu disco: la cuenta rápida #shorts"],
    kw="gta 6 cuánto pesa", kw2=["gta 6 210 gb", "gta 6 series s", "gta 6 espacio ps5"],
    intent="Informativa técnica, móvil.", audience="Dueños de PS5/Series S/X preparando la descarga.", dur="0:44 (Short 9:16).",
    why="Cuenta visual instantánea por consola; el Series S (58 %) genera conversación.",
    desc="GTA 6 ocupa ≈210 GB. PS5 original (667 GB libres): te sobra. Series S (364 GB): casi el 60 %. Series X (802 GB) y PS5 Slim 1 TB (≈840 GB): holgado. En PS4/Xbox One no existe.",
    tags=["gta 6", "gta 6 cuánto pesa", "gta 6 210 gb", "gta 6 series s", "gta 6 ps5", "shorts"],
    pinned="📌 ¿Cuánto espacio libre te queda? Escribe tu consola y tus GB 👇",
    sources=["Xbox Store (209,86 GB) / fichas de PS5 vía Notebookcheck y gta6filesize", "GameSpot: espacio útil PS5 y Series S", "Microsoft: Series X ≈802 GB", "Swappa: PS5 Slim ≈840-848 GB"],
    lic_extra=["Fuentes: Bungee (OFL)."], status="TERMINADO · listo para publicar", phase="Pre-lanzamiento",
    risk="El tamaño puede cambiar con parches (dato a fecha 17/11/2026)."),
"v08": dict(
    titles=["Los 4 animales de GTA 6 que Rockstar ya confirmó (y 170 especies más) #shorts", "Guía de campo de Leonida: fauna de GTA 6 #shorts",
            "Caimanes, flamencos y manatíes: la fauna de GTA 6 #shorts", "¿Qué animal será legendario en GTA 6? #shorts"],
    kw="animales gta 6", kw2=["fauna gta 6", "caimán gta 6", "gta 6 170 especies", "animales legendarios gta 6"],
    intent="Curiosidad evergreen.", audience="Público curioso y jugadores exploradores.", dur="0:37 (Short 9:16).",
    why="Estética de cuaderno de naturalista poco común en gaming; dato llamativo (170+ especies) y pregunta abierta.",
    desc="Según Game Informer, en Leonida hay más de 170 especies. Rockstar ya nombró al aligátor americano, el flamenco, el pelícano y el manatí. Algunas especies serán raras, descubribles o legendarias.",
    tags=["gta 6 animales", "fauna gta 6", "gta 6 caimán", "gta 6 flamenco", "gta 6 manatí", "gta 6", "shorts"],
    pinned="📌 Apuesta: ¿qué animal será legendario? Guardamos las respuestas para la guía completa 🐊",
    sources=["Game Informer n.º 382 (+170 especies), vía Insider Gaming / Beebom", "Michael Kane (Rockstar): caimanes, flamencos, pelícanos y manatíes, vía Gfinity", "Rarezas: Rara, Descubrible, Legendaria (prensa)"],
    lic_extra=["Ilustraciones de animales dibujadas por código (originales).", "Fuentes: Abril Fatface, Caveat (OFL)."], status="TERMINADO · listo para publicar",
    phase="Pre-lanzamiento (evergreen)", risk="Ninguno relevante."),
"v09": dict(
    titles=["7 misterios de GTA 6 que se resuelven el jueves (y nuestras predicciones)", "Lo que todavía NO sabemos de GTA 6: 7 sobres sellados",
            "GTA 6: online, 60 fps, interiores… 7 preguntas sin respuesta", "Apostamos: 7 predicciones de GTA 6 antes del lanzamiento"],
    kw="gta 6 misterios", kw2=["gta 6 online fecha", "gta 6 60 fps", "gta 6 interiores", "gta 6 preguntas", "gta 6 predicciones"],
    intent="Curiosidad y conversación; puente a contenido post-lanzamiento.", audience="Fans que siguen el lanzamiento y comentan.", dur="2:55",
    why="Formato de apuesta con medidor de confianza: invita a comentar y a volver para ver el resultado (VIDEO 10).",
    desc="Siete preguntas que Rockstar no ha respondido, lo que sí sabemos y nuestras predicciones con un porcentaje de confianza. Las predicciones son opinión del canal (en amarillo), no información. El jueves los abrimos jugando.",
    tags=["gta 6 misterios", "gta 6 preguntas", "gta 6 online", "gta 6 60 fps", "gta 6 predicciones", "perfil criminal", "gta 6 huracanes", "gta 6", "sal y asfalto"],
    pinned="📌 Deja tu predicción para el sobre que quieras (1-7). La más acertada se lleva este fijado después del lanzamiento 🔮",
    sources=["FAQ de PlayStation / Take-Two (online)", "TweakTown / RockstarINTEL (30 fps)", "Rob Nelson (Rockstar), vía prensa (Perfil Criminal)", "Game Informer n.º 382 (huracanes, fauna, mapa ×2)", "Web oficial (6 regiones)"],
    lic_extra=["Fuentes: Syne (OFL)."], status="TERMINADO · listo para publicar", phase="Pre-lanzamiento (publicar antes de la medianoche del 18/19)",
    risk="Predicciones claramente rotuladas como DEDUCCIÓN en voz y pantalla."),
"v10": dict(
    titles=["Abrimos los 7 sobres: comprobamos los misterios de GTA 6 jugando (¿acertamos?)", "GTA 6 PROBADO: ¿acertamos nuestras 7 predicciones?",
            "Online, 60 fps, interiores, huracanes… lo comprobamos en GTA 6", "7 pruebas en GTA 6 con método (aciertos y fallos)"],
    kw="gta 6 probado", kw2=["gta 6 60 fps", "gta 6 online", "gta 6 interiores", "gta 6 huracanes", "gta 6 animales legendarios", "gta 6 perfil criminal"],
    intent="Experiencial / verificación post-lanzamiento.", audience="Jugadores en la primera semana y quienes aún dudan en comprar.", dur="Estimada 8-10 min con capturas.",
    why="Cierra el arco iniciado en VIDEO 09: el espectador vuelve para ver el resultado.",
    desc="(Completar tras las pruebas) Abrimos los 7 sobres del video anterior y comprobamos cada misterio jugando, con capturas propias. Aciertos, fallos y “sin datos”, sin maquillar.",
    tags=["gta 6", "gta 6 probado", "gta 6 gameplay español", "gta 6 60 fps", "gta 6 online", "gta 6 huracanes", "sal y asfalto"],
    pinned="(Completar) 📌 Marcador final: __ aciertos · __ fallos · __ sin datos. ¿Qué probamos ahora?",
    sources=["Capturas propias del juego (fecha, consola)", "Newswire / soporte de Rockstar en la fecha de publicación"],
    lic_extra=["Gameplay: capturas propias. La política de Rockstar sobre material del juego tolera los vídeos de jugadores pero no concede licencia comercial explícita; ver 00_INFORMES/POLITICAS_Y_DERECHOS.md."],
    status="PREPRODUCCIÓN · NO PUBLICABLE todavía (faltan capturas y veredictos)", phase="Post-lanzamiento (grabar 19-23 nov.)",
    risk="Desactiva radio/música con licencia al capturar; evita cinemáticas largas y spoilers; no subas tramos de cinemáticas sin comentario."),
}

def fmt(t): return f"{int(t // 60)}:{int(t % 60):02d}"

def chapters(V, tl):
    out = []
    for b, bd in zip(V["beats"], tl["beats"]):
        sec = b.get("section")
        if sec:
            nice = sec.split(" (")[0].split(" — ")[0]
            nice = "Despedida" if nice.startswith("LLAMADA") else nice[0] + nice[1:].lower()
            for a, b_ in (("gta", "GTA"), ("leonida keys", "Leonida Keys"), ("leonida", "Leonida"), ("jason", "Jason"), ("lucía", "Lucía"), ("mount kalaga", "Mount Kalaga"),
                          ("port gellhorn", "Port Gellhorn"), ("ambrosia", "Ambrosia"), ("grassrivers", "Grassrivers"), ("vice city", "Vice City")):
                nice = nice.replace(a, b_)
            out.append((bd["start"], nice))
    if out: out[0] = (0.0, out[0][1])
    # descartar capítulos de menos de 10 s (requisito de YouTube)
    ded = []
    for t, n in out:
        if ded and ded[-1][1] == n: continue
        ded.append((t, n))
    out = ded; res = []
    for i, (t, n) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else tl["total"]
        if nxt - t >= 10 or i == 0: res.append((t, n))
    return res

def contact_sheet(folder):
    from PIL import Image
    frames = sorted(glob.glob(f"{folder}/recursos/fotogramas/*.png"))
    if not frames: return None
    ims = [Image.open(f).convert("RGB") for f in frames]
    vert = ims[0].height > ims[0].width
    tw, th = (180, 320) if vert else (384, 216); cols = 8 if vert else 5
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (10, 10, 14))
    for i, im in enumerate(ims): sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    p = f"{folder}/recursos/hoja_de_contactos.jpg"; sheet.save(p, quality=82)
    for f in frames: os.remove(f)
    os.rmdir(f"{folder}/recursos/fotogramas")
    return p

def write_all():
    import importlib
    only = os.environ.get("ONLY")
    for vid, M in META.items():
        if only and vid != only: continue
        V = importlib.import_module(f"videos.{vid}").VIDEO; folder = os.path.join(ROOT, V["folder"])
        tl = json.load(open(f"{folder}/recursos/timeline.json")); ch = chapters(V, tl)
        mp4 = glob.glob(f"{folder}/*.mp4")
        # narración en texto plano
        with open(f"{folder}/narracion.txt", "w", encoding="utf-8") as f:
            for bd in tl["beats"]:
                for s in bd["sents"]: f.write(s["text"] + "\n")
                if bd["sents"]: f.write("\n")
        # marcas de tiempo
        with open(f"{folder}/marcas_de_tiempo.csv", "w", encoding="utf-8") as f:
            f.write("inicio_s;fin_s;voz;texto\n")
            for bd in tl["beats"]:
                for s in bd["sents"]: f.write(f"{s['start']:.2f};{s['end']:.2f};{s['voice']};{s['text']}\n")
        is_short = "Short" in V["format"]
        desc = M["desc"] + "\n\n"
        if not is_short and vid != "v10":
            desc += "CAPÍTULOS\n" + "\n".join(f"{fmt(t)} {n}" for t, n in ch) + "\n\n"
        desc += "FUENTES\n" + "\n".join(f"• {s}" for s in M["sources"]) + "\n\n" + DISCLOSE_LINE + "\n\n#GTA6 #GTAVI #Leonida" + (" #shorts" if is_short else "")
        open(f"{folder}/descripcion_youtube.txt", "w", encoding="utf-8").write(desc)
        open(f"{folder}/etiquetas.txt", "w", encoding="utf-8").write(", ".join(M["tags"]) + "\n")
        L = [f"# {V['folder']} — {M['titles'][0]}", "", f"**Estado real:** {M['status']}  ", f"**Fase:** {M['phase']}  ",
             f"**Formato:** {V['format']} · **Duración:** {fmt(tl['total'])} · **Música:** estilo «{V['music']}» original · **Voz:** {'narradora + copiloto' if any(b.get('voice') == 'copiloto' for b in V['beats']) else 'narradora'}",
             "", "## A. Estrategia y posicionamiento", "", f"- **Título principal (SEO):** {M['titles'][0]}",
             "- **Títulos alternativos:**", *[f"  {i}. {t}" for i, t in enumerate(M['titles'][1:], 1)],
             f"- **Palabra clave principal:** {M['kw']}", f"- **Palabras clave secundarias:** {', '.join(M['kw2'])}",
             f"- **Intención de búsqueda:** {M['intent']}", f"- **Público:** {M['audience']}", f"- **Duración:** {M['dur'] if vid == 'v10' else fmt(tl['total']) + (' ' + M['dur'].split(' ', 1)[1] if ' ' in M['dur'] else '')}",
             f"- **Por qué hacer clic:** {M['why']}", "", "## B-C. Guion, voz y subtítulos", "",
             "- Guion completo con marcas de tiempo y notas visuales: `guion.txt`", "- Texto de narración: `narracion.txt` · marcas por frase: `marcas_de_tiempo.csv`",
             "- Audio de narración: `narracion.wav` (24 kHz, original) y `narracion.mp3` (procesada, 48 kHz)", "- Subtítulos: `subtitulos.srt` (súbelos como subtítulos en español en YouTube Studio)",
             "", "## D-F. Recursos visuales, animación y montaje", "",
             f"- Vídeo final: `{os.path.basename(mp4[0]) if mp4 else '(no renderizado)'}` · H.264 High, AAC 192 kbps 48 kHz, 30 fps, sonoridad −14 LUFS",
             "- Hoja de contactos (un fotograma cada 5 s): `recursos/hoja_de_contactos.jpg`", "- Música original del vídeo: `recursos/musica_original.mp3`",
             "- Código fuente de todas las escenas: `engine/videos/" + vid + ".py` (re-renderizable)", "", "## Descripción para YouTube (copiar y pegar)", "", "```", desc, "```", "",
             "## Etiquetas", "", ", ".join(M["tags"]), "", "## Comentario fijado recomendado", "", M["pinned"], "",
             "## Divulgación de IA (YouTube Studio → Detalles → Contenido alterado)", "", AI_NO if vid != "v10" else AI_NO + " En la versión final con capturas propias, la casilla sigue siendo NO (el gameplay es real).", "",
             "## Fuentes de investigación", "", *[f"- {s}" for s in M["sources"]], "", "## Recursos utilizados y licencias", "", *[f"- {s}" for s in COMMON_LIC + M["lic_extra"]], "",
             "## Auditoría de calidad", "", AUDIT.get(vid, ""), "", f"**Riesgos y notas:** {M['risk']}", ""]
        open(f"{folder}/publicacion.md", "w", encoding="utf-8").write("\n".join(L))
        cs = contact_sheet(folder)
        print(vid, "ok", len(ch), "capítulos", cs or "")

AUDIT = {}
_AUD_ROWS = ["¿Contenido original?", "¿Aporta valor?", "¿Guion distinto a los demás?", "¿Imágenes adecuadas y autorizadas?", "¿Voz con calidad profesional?",
             "¿Montaje con buen ritmo?", "¿Título honesto?", "¿Miniatura corresponde?", "¿Información sin verificar?", "¿Riesgo de copyright?", "¿Declarar contenido sintético?", "¿Problema de monetización?"]
def _aud(vals):
    return "| Comprobación | Resultado |\n|---|---|\n" + "\n".join(f"| {q} | {v} |" for q, v in zip(_AUD_ROWS, vals))
_VOICE = "Buena: voz femenina expresiva (Chatterbox Multilingual), leída por frases y párrafos cortos; cada toma verificada con reconocimiento de voz (ver recursos/control_de_voz.csv). Es una voz sintética: grabar con voz humana mejora autenticidad (ver README)."
AUDIT["v01"] = _aud(["Sí: guion, música, gráficos y miniatura originales", "Sí: 7 respuestas prácticas con fuentes", "Sí: estructura de lista de embarque (única)", "Sí: todo dibujado por código", _VOICE, "Sí: cambio de escena cada 20-40 s, animación sincronizada por palabra clave", "Sí", "Sí (00:00 + 210 GB + precio + idioma están en el vídeo)", "Precios locales marcados como REPORTADO; verificar en tienda antes de publicar", "No", "No (ver sección IA)", "Riesgo moderado inherente a canales nuevos con voz sintética; mitigado por originalidad y valor"])
AUDIT["v02"] = _aud(["Sí", "Sí: hora exacta por país", "Sí: Short con globo 3D", "Sí: Natural Earth (dominio público)", _VOICE, "Sí: ritmo rápido, subtítulos palabra a palabra", "Sí", "Sí", "EE. UU. marcado como REPORTADO", "No", "No", "Bajo"])
AUDIT["v03"] = _aud(["Sí", "Sí: prevención y pasos de recuperación", "Sí: investigación con dos voces", "Sí: interfaces genéricas inventadas", _VOICE, "Sí", "Sí: el vídeo explica que no existe versión PC/Android", "Sí", "Datos de malware atribuidos a ESET/Cynet (REPORTADO)", "No", "No", "Bajo (contenido educativo de seguridad)"])
AUDIT["v04"] = _aud(["Sí", "Sí: guía geográfica con certeza etiquetada", "Sí: viaje de norte a sur en 3D", "Sí: Natural Earth + dibujo propio; aviso permanente de que no es el mapa oficial", _VOICE, "Sí: cámara 3D continua", "Sí", "Sí", "Ubicaciones deducidas marcadas en amarillo", "No", "No", "Bajo"])
AUDIT["v05"] = _aud(["Sí", "Sí: contexto sin spoilers", "Sí: expediente con dos voces", "Sí: siluetas genéricas, sin arte oficial", _VOICE, "Sí", "Sí", "Sí (siluetas, no los personajes)", "Paráfrasis de textos oficiales: verificar redacción; relación opcional = SIN CONFIRMAR", "Bajo (sin arte; nombres usados en comentario)", "No", "Bajo"])
AUDIT["v06"] = _aud(["Sí", "Sí", "Sí: rondas tipo transmisión deportiva", "Sí: infografías propias", _VOICE, "Sí: ritmo alto, música dembow original", "Sí", "Sí", "3 rumores rotulados como RUMOR", "No", "No", "Bajo"])
AUDIT["v07"] = _aud(["Sí", "Sí", "Sí: concurso arcade", "Sí", _VOICE, "Sí", "Sí", "Sí", "Tamaño puede variar por parches", "No", "No", "Bajo"])
AUDIT["v08"] = _aud(["Sí", "Sí", "Sí: guía de campo ilustrada", "Sí: ilustraciones originales", _VOICE + " (voz femenina)", "Sí", "Sí", "Sí", "Solo los 4 animales nombrados por Rockstar", "No", "No", "Bajo"])
AUDIT["v09"] = _aud(["Sí", "Sí: separa hechos de predicciones", "Sí: sobres sellados + medidores", "Sí", _VOICE, "Sí", "Sí", "Sí", "Predicciones = DEDUCCIÓN, dicho en voz y pantalla", "No", "No", "Bajo"])
AUDIT["v10"] = _aud(["Sí (cuando se graben las pruebas)", "Sí: verificación con método", "Sí: cierre del arco de V09", "Pendiente: capturas propias", "Narración de intro/cierre lista; veredictos por grabar (idealmente voz humana)", "Animático listo; montaje final pendiente", "Sí (pregunta, no afirma resultados)", "Sí", "TODO pendiente de comprobar: NO publicar el animático", "Moderado: gameplay de Rockstar (tolerado, sin licencia comercial explícita)", "No", "Moderado (ver políticas)"])

if __name__ == "__main__":
    write_all()
