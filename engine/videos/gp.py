"""GTA6_VIDEO_LANZAMIENTO (versión post lanzamiento) — GTA 6 ya se juega: lo que dicen quienes lo han jugado.

Concepto: el veredicto de la crítica (reseñas publicadas el 18/11/2026, tras jugar la versión final) y de los primeros
jugadores (Nueva Zelanda, primer país en desbloquearlo), tema por tema: mundo, atracos, conducción, combate, realismo,
rendimiento e historia. Cada afirmación lleva su fuente en pantalla y su plano de juego real oficial de Rockstar Games
(Extended Look, tráiler, capturas). Los capítulos con imágenes de misiones llevan aviso de spoiler; el título y la
miniatura no tienen ninguno. Audio oficial silenciado. Montaje: videos/gl_render.py (mismo motor que gl.py).
"""
import numpy as np
import audio
from videos import gl_render as R

# tramos de misión del Extended Look que este vídeo SÍ muestra (con aviso de spoiler)
R.EL_RANGES.update({"m1": (686.0, 1000.0), "m3": (1164.0, 1208.0), "m4": (1238.0, 1540.0), "m0": (0.0, 360.0)})
R.BAD[:] = [((a, 686.0) if (a, z) == (574.9, 690.0) else (a, z)) for a, z in R.BAD if not (686.0 <= a < 1000.0)]   # el atraco deja de estar excluido
R.BAD += [(723.4, 735.5), (736.0, 750.0), (1445.5, 1449.5), (1461.0, 1540.0)]   # sin rehenes, diálogos de trama ni cuerpos

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)

# ================================================================ GANCHO
beat("Trece años después de GTA 5, la espera ha terminado: GTA 6 ya se está jugando. Nueva Zelanda fue el primer país en desbloquearlo, y la crítica, que ya lo ha jugado, ha dado su veredicto: un 99 en Metacritic.",
     section="GANCHO", mus=("synthwave", 2), exag=0.65, pre=0.4, cert="OFICIAL",
     shots=[S(None, "e:1133.4", z=(1.0, 1.1)), S("GTA 6 ya se está jugando", "e:1128.0"), S("Nueva Zelanda", "g:nz"), S("la crítica", "s:Vice_City_10", z=(1.0, 1.08)), S("un 99", "g:meta")],
     sfx=[("w:Nueva Zelanda", "whoosh", 0.35), ("w:un 99", "hit", 0.4)])
beat("Hoy repasamos qué dicen de su jugabilidad: los atracos, la conducción, el combate, el realismo y lo que menos ha gustado, con imágenes reales del juego.",
     mus=("synthwave", 2), exag=0.65,
     shots=[S(None, "a:Jason_and_Lucia_Robbery_landscape", z=(1.0, 1.08)), S("la conducción", "e:1086.6"), S("el combate", "s:Jason_Duval_17", z=(1.0, 1.08)), S("el realismo", "e:1039.2"),
            S("lo que menos ha gustado", "g:fps"), S("imágenes reales", "e:509.0")])
beat("", dur=2.4, mus=("synthwave", 1), sfx=[(0.0, "logo", 0.9)], shots=[S(None, "g:sting")])

# ================================================================ INTRO
beat("Estás en Sal y Asfalto. Tres avisos rápidos. Las imágenes son material oficial de Rockstar Games, y en cada plano verás la fuente. "
     "Las opiniones son de los medios que lo han analizado, y te decimos cuál dice cada cosa. "
     "Y en el capítulo de los atracos verás escenas de misiones, así que antes te avisaremos con un cartel de spoiler.",
     section="INTRODUCCIÓN: TRES AVISOS", mus=("synthwave", 1), pre=0.3,
     shots=[S(None, "g:title2"), S("material oficial", "g:media"), S("Las opiniones", "g:outlets"), S("escenas de misiones", "g:spoiler")],
     sfx=[("w:Tres avisos", "pop", 0.35), ("w:Las opiniones", "pop", 0.35), ("w:escenas de misiones", "stamp", 0.5)])

# ================================================================ 1 · EL VEREDICTO
beat("Empecemos por la nota. Las reseñas se publicaron el 18 de noviembre, y GTA 6 tiene un 99 sobre 100 en Metacritic, con más de 140 análisis y ninguno mixto ni negativo. "
     "Iguala el récord histórico de la web, que tenía {The Legend of Zelda: Ocarina of Time|Di Léyend of Zelda, Ocarina of Taim} desde 1998. En OpenCritic, el cien por cien de los críticos lo recomienda.",
     section="1 · EL VEREDICTO", chapter=(1, "EL VEREDICTO"), mus=("electro", 1), pre=0.6, cert="OFICIAL",
     src_note="Metacritic y OpenCritic, 18/11/2026 (vía Bloomberg, Vice y Dot Esports)",
     shots=[S(None, "e:994.6", z=(1.0, 1.08), speed=0.74), S("99 sobre 100", "g:meta", step=1), S("ninguno mixto", "g:meta", step=2),
            S("récord histórico", "g:meta", step=3), S("OpenCritic", "g:meta", step=4)],
     sfx=[(0.0, "whoosh", 0.4), ("w:99 sobre", "hit", 0.4), ("w:récord", "ding", 0.3)])
beat("Algunas frases de las reseñas. IGN le pone un diez y lo llama «el videojuego más impresionante» que ha jugado su analista. "
     "GameSpot, otro diez: cree que no lo superará nadie hasta GTA 7. Eurogamer le da cinco estrellas de cinco, "
     "y GamesRadar habla del mundo abierto más detallado de esta generación.",
     mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "e:1128.0"), S("IGN", "g:quote", q=0), S("GameSpot", "g:quote", q=1), S("Eurogamer", "g:quote", q=2), S("GamesRadar", "g:quote", q=3)],
     sfx=[("w:IGN", "pop", 0.35), ("w:GameSpot", "pop", 0.35), ("w:Eurogamer", "pop", 0.35), ("w:GamesRadar", "pop", 0.35)])

# ================================================================ 2 · LOS PRIMEROS JUGADORES
beat("Mientras tanto, el juego ya se desbloqueaba país a país, a la medianoche de cada uno. Nueva Zelanda fue la primera, a las once de la mañana en hora universal del día 18, y su prensa recogió las primeras impresiones. "
     "Un jugador, a la media hora, destacaba la jugabilidad, los gráficos y la historia. Otro lo resumía como «un festín para los ojos».",
     section="2 · LOS PRIMEROS JUGADORES", chapter=(2, "LOS PRIMEROS JUGADORES"), mus=("synthpop", 1), pre=0.6, cert="OFICIAL",
     src_note="Stuff y NZ Herald (Nueva Zelanda), 18/11/2026",
     shots=[S(None, "e:1208.4"), S("Nueva Zelanda fue la primera", "g:nz", step=1), S("a la media hora", "e:509.0"), S("los gráficos", "e:1570.4"),
            S("la historia", "a:Jason_and_Lucia_Motel_landscape", z=(1.0, 1.08)), S("un festín", "e:1549.0", z=(1.0, 1.06))])
beat("Y un aviso: algunos jugadores cambiaron la región de su consola para jugar antes, el llamado truco de Nueva Zelanda. "
     "Hay medios que advierten de posibles sanciones en las cuentas, y streamers a los que se lo han recordado. Nuestro consejo: espera a tu hora.",
     mus=("synthpop", 1), cert="INTERPRETACIÓN",
     shots=[S(None, "g:nz", step=2), S("posibles sanciones", "g:warn"), S("Nuestro consejo", "e:1208.4")])

# ================================================================ 3 · EL MUNDO
beat("Lo que más repiten los análisis es el mundo. IGN describe Leonida como un lugar exquisitamente detallado, que invita a experimentar sin parar. "
     "GameSpot destaca los pequeños detalles como una de las grandes razones por las que la espera ha merecido la pena.",
     section="3 · EL MUNDO", chapter=(3, "EL MUNDO"), mus=("tropical", 1), pre=0.6, cert="OFICIAL", src_note="IGN y GameSpot, reseñas del 18/11/2026",
     shots=[S(None, "e:571.2", z=(1.0, 1.06)), S("exquisitamente detallado", "e:445.6"), S("experimentar", "e:565.2"), S("los pequeños detalles", "e:437.6"),
            S("la espera", "e:470.2")])
beat("Y en Windows Central subrayan cómo reacciona el mundo a lo que haces: por ejemplo, un robo no sale igual según quién esté cerca. "
     "Es justo lo que se ve en el material oficial: vecinos en la calle, gente en las azoteas, tráfico y peatones que van a lo suyo.",
     mus=("tropical", 1), cert="OFICIAL", src_note="Windows Central, reseña del 18/11/2026",
     shots=[S(None, "e:1028.2"), S("un robo", "a:Jason_and_Lucia_Robbery_landscape", z=(1.0, 1.08)), S("según quién esté cerca", "s:Vice_City_09", z=(1.0, 1.08)), S("vecinos en la calle", "e:554.6"),
            S("gente en las azoteas", "e:573.1"), S("tráfico y peatones", "e:521.0")])

beat("Hay más detalles sobre la gente de Leonida. Según Windows Central, los peatones reaccionan si conduces mal, si los insultas o si les pitas, "
     "y Vice destaca que tienen frases propias. Incluso las caras de la gente están capturadas con actores, y se aprecian en las conversaciones dentro del coche si pones la cámara en primera persona.",
     mus=("tropical", 1), cert="OFICIAL", src_note="Windows Central y Vice, reseñas del 18/11/2026",
     shots=[S(None, "e:380.2"), S("si conduces mal", "e:521.0"), S("si les pitas", "e:528.0"), S("frases propias", "e:554.6"),
            S("las caras", "s:Brian_Heder_01", z=(1.0, 1.1)), S("dentro del coche", "e:794.0"), S("primera persona", "s:Jason_and_Lucia_11", z=(1.0, 1.08))])
beat("Rockstar ya había dicho que Leonida es, más o menos, el doble de grande que el mapa de GTA 5. Y el analista de The Guardian lo resume con una imagen: hacer la reseña de GTA 6 es como hacer la reseña de una ciudad entera, como París.",
     mus=("tropical", 1), cert="OFICIAL", src_note="Aaron Garbut a Game Informer (mapa) · The Guardian, citado por The National (18/11/2026)",
     shots=[S(None, "g:postcards"), S("The Guardian", "e:1142.0"), S("como París", "e:571.2", z=(1.0, 1.08))])

# ================================================================ 3B · QUÉ HACER
beat("¿Y fuera de las misiones? Las reseñas coinciden en que las actividades secundarias pueden comerte horas: pescar, entrenar en el gimnasio, bailar en una discoteca, "
     "jugar al golf, cazar, bucear, observar aves o correr carreras de drones. Según Vice, además, todo empuja hacia algo, porque la historia gira en torno a ganar dinero.",
     section="3B · QUÉ HACER", mus=("electro", 2), pre=0.5, cert="OFICIAL", src_note="The National, Output Lag y Vice, 18/11/2026",
     shots=[S(None, "e:1108.6", label="ACTIVIDADES"), S("pescar", "s:Jason_Duval_03", z=(1.0, 1.1), label="PESCA"), S("el gimnasio", "e:1039.2", label="GIMNASIO"),
            S("bailar", "e:1226.2", label="DISCOTECA"), S("al golf", "s:Cal_Hampton_01", z=(1.0, 1.08), label="GOLF"), S("cazar", "s:Grassrivers_06", z=(1.0, 1.08), label="CAZA"),
            S("bucear", "e:1036.6", label="BUCEO"), S("observar aves", "s:Grassrivers_05", z=(1.1, 1.25), f=(0.5, 0.2), label="AVES"),
            S("carreras de drones", "g:drone"), S("todo empuja", "e:1062.4"), S("ganar dinero", "s:Vice_City_18", z=(1.0, 1.06))])

# ================================================================ 4 · LOS ATRACOS (SPOILERS)
beat("Ahora sí, aviso de spoiler. Las próximas imágenes son de misiones del Extended Look, el vídeo de juego que Rockstar publicó en agosto. "
     "Si no quieres ver nada, salta al siguiente capítulo: el minuto está en la descripción.",
     section="4 · LOS ATRACOS (AVISO DE SPOILER)", chapter=(4, "LOS ATRACOS"), mus=("tension", 1), pre=0.6, cert=None, spoiler=True,
     shots=[S(None, "g:spoiler", step=1)], sfx=[(0.0, "stamp", 0.6)], hold=0.6)
beat("Para GameSpot, los grandes atracos son la joya del juego. Y Windows Central explica que un robo puede salir distinto según quién haya alrededor. "
     "En el atraco que enseñó Rockstar se ve la preparación con pañuelos en la cara, la entrada en la tienda y la huida.",
     mus=("tension", 2), cert="OFICIAL", spoiler=True, src_note="GameSpot y Windows Central, reseñas del 18/11/2026",
     shots=[S(None, "e:688.4"), S("la joya", "e:696.0"), S("puede salir distinto", "e:722.0"), S("quién haya alrededor", "e:706.5"),
            S("la preparación", "e:831.0"), S("la entrada", "e:714.6"), S("la huida", "e:921.5")],
     sfx=[("w:la joya", "hit", 0.35)])
beat("En la persecución se ven disparos desde el coche, un tiroteo en un callejón, coches de policía y un cambio de vehículo en un aparcamiento. "
     "Rockstar ha dicho además que puedes cambiar de Jason a Lucía en plena acción, y en esta misión se ve a los dos al volante.",
     mus=("tension", 2), cert="OFICIAL", spoiler=True,
     shots=[S(None, "e:839.2"), S("un tiroteo", "e:864.4"), S("coches de policía", "e:847.4"), S("un cambio de vehículo", "e:959.2"),
            S("puedes cambiar", "e:796.0"), S("a los dos al volante", "e:893.0")])
beat("Y no todo es acción. En otra misión del mismo vídeo, Jason se cuela en una fiesta de lujo y sube a zonas restringidas, mientras Lucía le avisa por mensaje de que hay tipos por todas partes.",
     mus=("tension", 1), cert="OFICIAL", spoiler=True,
     shots=[S(None, "e:1214.2"), S("una fiesta de lujo", "e:1268.0"), S("zonas restringidas", "e:1320.5"), S("le avisa por mensaje", "e:1428.2"), S("por todas partes", "e:1438.2")])

# ================================================================ 5 · CONDUCCIÓN
beat("Fin de los spoilers. Vamos con la conducción, el tema que más divide. Forbes dice que conducir, que suele ser un problema en los juegos de Rockstar, aquí funciona perfectamente. "
     "GameSpot, en cambio, admite que la física de los coches le exigió más precisión de la que tenía.",
     section="5 · LA CONDUCCIÓN", chapter=(5, "LA CONDUCCIÓN"), mus=("synthpop", 2), pre=0.6, cert="OFICIAL", src_note="Forbes y GameSpot, reseñas del 18/11/2026",
     shots=[S(None, "g:spoiler_end"), S("la conducción", "e:509.0"), S("Forbes", "e:752.4"), S("funciona perfectamente", "e:776.4"),
            S("GameSpot", "e:1062.4"), S("la física", "e:1086.6")],
     sfx=[(0.0, "whoosh", 0.4)])
beat("Varios análisis añaden un matiz: los coches se rompen con más facilidad que en GTA 5, y las reparaciones cuestan dinero. "
     "Si vienes de conducir a lo loco por Los Santos, toca cambiar el chip.",
     mus=("synthpop", 2), cert="OFICIAL", src_note="Resumen de reseñas de The National, 18/11/2026",
     shots=[S(None, "g:realism", step=0), S("las reparaciones", "g:realism", step=1), S("toca cambiar el chip", "e:1222.4")])

# ================================================================ 5B · LA POLICÍA
beat("La policía también cambia. Windows Central dice que el sistema es mucho más complejo que en los GTA anteriores, y que una persecución se puede torcer muy rápido. "
     "Por ejemplo, puedes cortar alarmas y cámaras de seguridad para que la policía sea menos eficaz, o esconderte dentro del coche para que pase a modo de búsqueda.",
     section="5B · LA POLICÍA", mus=("tension", 2), pre=0.5, cert="OFICIAL", src_note="Windows Central, reseña del 18/11/2026",
     shots=[S(None, "s:Jason_Duval_11", z=(1.0, 1.08)), S("mucho más complejo", "s:Lucia_Caminos_14", z=(1.0, 1.08)), S("se puede torcer", "s:Jason_and_Lucia_09", z=(1.0, 1.08)),
            S("cortar alarmas", "g:police", step=0), S("esconderte", "g:police", step=1), S("modo de búsqueda", "s:Jason_and_Lucia_19", z=(1.0, 1.08))])

# ================================================================ 6 · EL COMBATE
beat("Con el combate, la crítica es menos entusiasta. Una reseña lo describe como torpe, y otras dos dicen que el cuerpo a cuerpo es rígido. "
     "También hay quejas por controles algo enrevesados en momentos concretos.",
     section="6 · EL COMBATE", chapter=(6, "EL COMBATE"), mus=("tension", 1), pre=0.6, cert="OFICIAL", src_note="Resúmenes de reseñas de The National y Pure Xbox, 18/11/2026",
     shots=[S(None, "s:Jason_Duval_17", z=(1.0, 1.08)), S("torpe", "s:Jason_Duval_16", z=(1.0, 1.08)), S("el cuerpo a cuerpo", "s:Lucia_Caminos_01", z=(1.0, 1.08)),
            S("controles", "s:Jason_Duval_12", z=(1.0, 1.08))])
beat("Nuestra lectura: en un juego de Rockstar, el combate nunca ha sido lo más pulido, y parece que esta vez tampoco. Pero nadie lo señala como un problema grave.",
     mus=("tension", 1), cert="INTERPRETACIÓN",
     shots=[S(None, "s:Lucia_Caminos_13", z=(1.0, 1.08)), S("nadie lo señala", "s:Jason_and_Lucia_09", z=(1.0, 1.08))])

# ================================================================ 7 · EL REALISMO
beat("Otro cambio grande es el realismo del día a día. Seis reseñas avisan del realismo: coches frágiles, facturas de reparación y tareas cotidianas, "
     "algo que cuesta al principio si vienes de GTA 5. Rockstar ya había adelantado que la comida cambia el peso, el gimnasio se nota en los músculos y la falta de sueño se ve en la cara.",
     section="7 · EL REALISMO", chapter=(7, "EL REALISMO"), mus=("tropical", 1), pre=0.6, cert="OFICIAL",
     src_note="Resumen de reseñas (The National) y entrevista de Rockstar a Dazed (08/2026)",
     shots=[S(None, "e:544.6"), S("coches frágiles", "g:realism", step=0), S("facturas de reparación", "g:realism", step=1), S("tareas cotidianas", "e:432.0"),
            S("cuesta al principio", "e:1144.6"), S("la comida", "e:544.6"), S("el gimnasio", "e:1039.2"), S("la falta de sueño", "s:Jason_Duval_19", z=(1.1, 1.25), f=(0.62, 0.4))])
beat("Para unos es inmersión pura. Para otros, una molestia. Windows Central avisa de que parte de su jugabilidad podría generar debate en la comunidad.",
     mus=("tropical", 1), cert="OFICIAL", src_note="Windows Central, reseña del 18/11/2026",
     shots=[S(None, "e:1033.2"), S("una molestia", "e:1124.0"), S("generar debate", "g:poll2")])

# ================================================================ 8 · RENDIMIENTO
beat("Y el punto más criticado: el rendimiento. GTA 6 funciona a 30 imágenes por segundo en todas las consolas, incluida PS5 Pro, sin modo a 60. "
     "Además, nueve reseñas notaron caídas por debajo de 30 en momentos exigentes.",
     section="8 · EL RENDIMIENTO", chapter=(8, "EL RENDIMIENTO"), mus=("electro", 1), pre=0.6, cert="OFICIAL",
     src_note="Resúmenes de reseñas de The National y Output Lag, 18/11/2026",
     shots=[S(None, "e:509.0"), S("30 imágenes por segundo", "g:fps", step=0), S("sin modo a 60", "g:fps", step=1), S("nueve reseñas", "g:fps", step=2),
            S("momentos exigentes", "e:1226.2")],
     sfx=[("w:30 imágenes", "hit", 0.35)])
beat("Digital Foundry ya lo ha medido. En Xbox Series X, el juego se renderiza internamente a 1440p y apunta a 30, con bajadas en escenas cargadas. "
     "En Series S baja a 720p, que Rockstar reescala a 1080p, y se queda a menudo por debajo de 30. Su recomendación: jugarlo en PS5 o en Series X.",
     mus=("electro", 1), cert="OFICIAL", src_note="Digital Foundry (vía VGC y LevelUp) y Rockstar a Wccftech, 11/2026",
     shots=[S(None, "g:df", step=0), S("En Series S", "g:df", step=1), S("Su recomendación", "g:df", step=2)])
beat("Y en PlayStation, según el análisis de Digital Foundry, PS5 y PS5 Pro renderizan a unos 1440p y también apuntan a 30. "
     "La Pro reescala con PSSR hasta una imagen casi 4K, añade sombras con trazado de rayos y mantiene los 30 casi siempre: para ellos, es la mejor forma de jugarlo. "
     "En la PS5 normal, las caídas por debajo de 30 son más frecuentes en la acción intensa. Su veredicto: un rendimiento aceptable, pero algo decepcionante.",
     mus=("electro", 1), cert="OFICIAL", src_note="Digital Foundry (18/11/2026), vía TweakTown y Twisted Voxel",
     shots=[S(None, "g:dfps", step=0), S("La Pro reescala", "g:dfps", step=1), S("la mejor forma", "e:1214.2"), S("En la PS5 normal", "g:dfps", step=2),
            S("la acción intensa", "e:864.4"), S("Su veredicto", "g:dfps", step=3)])
beat("Nuestra lectura: a cambio, el juego enseña un nivel de detalle que pocos juegos de mundo abierto alcanzan. Pero si para ti los 60 son imprescindibles, conviene saberlo antes.",
     mus=("electro", 1), cert="INTERPRETACIÓN",
     shots=[S(None, "e:1214.2"), S("nivel de detalle", "e:458.0"), S("conviene saberlo", "g:fps", step=1)])

# ================================================================ 9 · LA HISTORIA (SIN SPOILERS)
beat("La historia, sin destripar nada. La crítica coincide en que gana mucho con Jason y Lucía, la primera pareja protagonista de la saga: en un resumen de dieciocho reseñas, dieciséis hablan de ellos. "
     "Las pegas: un arranque lento, misiones que a veces te dejan poco margen y requisitos de progreso que, según GameSpot, cortan el ritmo de la historia. Worthplaying, que le pone un 9,5, avisa de que los primeros capítulos dedican mucho tiempo a la vida cotidiana.",
     section="9 · LA HISTORIA (SIN SPOILERS)", chapter=(9, "LA HISTORIA"), mus=("noir", 1), pre=0.6, cert="OFICIAL",
     src_note="Resúmenes de reseñas (Dot Esports, The National), GameSpot y Worthplaying, 18/11/2026",
     shots=[S(None, "a:Jason_and_Lucia_Beach_landscape", z=(1.0, 1.08)), S("Jason y Lucía", "c:Jason_Duval"), S("primera pareja", "c:Lucia_Caminos"), S("dieciséis hablan", "g:meta", step=5),
            S("un arranque lento", "s:Jason_and_Lucia_16", z=(1.0, 1.08)), S("poco margen", "s:Jason_and_Lucia_06", z=(1.0, 1.08)),
            S("requisitos de progreso", "s:Jason_and_Lucia_11", z=(1.0, 1.08)), S("Worthplaying", "e:432.0"), S("la vida cotidiana", "e:437.6")])
beat("La mayor sorpresa para muchos críticos es la historia de amor entre los dos. Uno llega a decir que no esperaba emocionarse tanto. "
     "Y la sátira sigue afilada: según las reseñas, apunta a los teóricos de la conspiración, a la desigualdad y a los influencers.",
     mus=("noir", 1), cert="OFICIAL", src_note="The National (resumen de reseñas), 18/11/2026",
     shots=[S(None, "s:Jason_and_Lucia_14", z=(1.0, 1.08)), S("la historia de amor", "a:Jason_and_Lucia_Beach_landscape", z=(1.05, 1.15)), S("no esperaba emocionarse", "s:Jason_and_Lucia_13", z=(1.05, 1.15)),
            S("la sátira", "s:Cal_Hampton_03", z=(1.0, 1.08)), S("la conspiración", "c:Cal_Hampton"), S("la desigualdad", "s:Vice_City_02", z=(1.0, 1.08)),
            S("los influencers", "s:Real_Dimez_02", z=(1.0, 1.08))])
beat("¿Y cuánto dura? Rob Nelson, de Rockstar North, calculó antes del lanzamiento unas ochenta horas para la historia principal. Pronto sabremos cuántas les lleva a los jugadores.",
     mus=("noir", 1), cert="OFICIAL", src_note="Rob Nelson a Variety (11/2026)",
     shots=[S(None, "s:Jason_and_Lucia_13", z=(1.0, 1.08)), S("ochenta horas", "g:hours"), S("Pronto sabremos", "s:Vice_City_15", z=(1.0, 1.08))])

# ================================================================ 10 · LO QUE DICE ROCKSTAR
beat("Para cerrar, Sam Houser, cofundador de Rockstar, publicó un mensaje poco habitual en él. Dio las gracias a los jugadores y dijo que espera seguir compartiendo estas experiencias muchos años más. "
     "Y en bolsa, las acciones de Take-Two subieron un seis por ciento el día de las reseñas, con unas reservas que se estiman en más de mil quinientos millones de dólares.",
     section="10 · EL LANZAMIENTO", chapter=(10, "EL LANZAMIENTO"), mus=("synthwave", 1), pre=0.6, cert="OFICIAL",
     src_note="GamesRadar+ (mensaje de Sam Houser) y Forbes (bolsa), 18/11/2026",
     shots=[S(None, "k:cover", st=15.6), S("un mensaje poco habitual", "s:Vice_City_11", z=(1.0, 1.08)), S("Dio las gracias", "g:houser"), S("muchos años", "e:1570.4"), S("en bolsa", "g:stock"), S("reservas", "g:stock", step=1)])

# ================================================================ 11 · LAS PRIMERAS HORAS
beat("¿Y qué ha pasado desde que se desbloqueó? Primero, un récord: entre Twitch, YouTube y Kick, más de seis millones de personas vieron directos de GTA 6 a la vez, según Streams Charts. "
     "Solo en Twitch se superaron los tres millones. Es el mayor lanzamiento de un videojuego en la historia del streaming.",
     section="11 · LAS PRIMERAS HORAS", chapter=(11, "LAS PRIMERAS HORAS"), mus=("synthpop", 2), pre=0.6, cert="OFICIAL",
     src_note="Streams Charts, TalkEsport y Win.gg (19/11/2026); las cifras varían según la plataforma y la hora",
     shots=[S(None, "e:1546.2"), S("un récord", "g:stream", step=0), S("Solo en Twitch", "g:stream", step=1), S("el mayor lanzamiento", "g:stream", step=2)],
     sfx=[(0.0, "whoosh", 0.4), ("w:un récord", "hit", 0.35)])
beat("También han llegado las primeras quejas: jugadores que hablan de personajes que atraviesan objetos, físicas raras y algunos cierres inesperados en consola. "
     "De momento, Rockstar no los ha confirmado, y muchos otros jugadores dicen no haber tenido ningún problema. Antes del lanzamiento, además, PlayStation Network sufrió una caída que Sony reconoció.",
     mus=("synthpop", 1), cert="OFICIAL", src_note="Sportskeeda y Brit Brief (reportes de jugadores, sin confirmar) · Newsweek (caída de PSN)",
     shots=[S(None, "g:bugs", step=0), S("De momento, Rockstar", "g:bugs", step=1), S("muchos otros jugadores", "e:1108.6"), S("PlayStation Network", "g:psn")])

beat("Pausa rápida: ¿tú ya lo estás jugando, o esperas a tu hora? Te leemos en los comentarios.",
     mus=("synthwave", 1), cert=None, pre=0.4, hold=0.4, shots=[S(None, "g:poll3"), S("Te leemos", "s:Jason_and_Lucia_03", z=(1.0, 1.08))], sfx=[("w:¿tú ya", "pop", 0.4)])
beat("¿Merece la pena? Para la crítica, sin ninguna duda. Nuestra lectura: si te preocupan los 30 imágenes por segundo o el combate, dale unas horas antes de juzgarlo: varias reseñas coinciden en que el arranque es lento y en que el juego tarda en despegar.",
     mus=("synthwave", 1), cert="INTERPRETACIÓN", pre=0.3,
     shots=[S(None, "s:Vice_City_26", z=(1.0, 1.08)), S("si te preocupan", "g:fps", step=1), S("dale unas horas", "e:1108.6"), S("el arranque es lento", "s:Jason_and_Lucia_16", z=(1.0, 1.08)), S("tarda en despegar", "e:1133.4")])

# ================================================================ CIERRE
beat("Resumen: un mundo que la crítica considera de récord, atracos espectaculares y un realismo que exige paciencia, con dos peros claros, el combate y los 30 imágenes por segundo. "
     "Si ya lo estás jugando, cuéntanos en los comentarios qué te ha parecido. Sin spoilers, por favor. Y suscríbete a Sal y Asfalto: seguimos con GTA 6 toda la semana.",
     section="CIERRE", mus=("synthwave", 2), pre=0.5, cert=None, hold=0.4,
     shots=[S(None, "e:1128.0"), S("atracos espectaculares", "a:Jason_and_Lucia_Robbery_landscape", z=(1.05, 1.15)), S("un realismo", "e:1039.2"), S("dos peros", "g:fps", step=1),
            S("Si ya lo estás jugando", "e:1133.4"), S("Sin spoilers", "g:nospoil2"), S("suscríbete", "g:subscribe")],
     sfx=[("w:suscríbete", "pop", 0.45)])
beat("", dur=20.0, mus=("synthwave", 1), shots=[S(None, "g:end")])

# ---------------------------------------------------------------- música original por capítulo (misma función que gl.py)
def music_fn(total, beats_tl):
    segs = []
    for b, bd in zip(B, beats_tl):
        st, lv = b.get("mus", ("synthwave", 1))
        if segs and segs[-1]["style"] == st: segs[-1]["en"].append((bd["start"] - segs[-1]["t0"], lv))
        else: segs.append(dict(style=st, t0=bd["start"], en=[(0.0, lv)]))
    n = int(total * audio.SR); out = np.zeros((n, 2)); xf = 1.2
    for i, sg in enumerate(segs):
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        a0 = max(0.0, sg["t0"] - (xf / 2 if i else 0)); dur = (t1 - a0) + (xf / 2 if i + 1 < len(segs) else 0)
        en = [(max(0.0, tt + (sg["t0"] - a0)), lv) for tt, lv in sg["en"]]
        y = audio.compose(sg["style"], dur, energy=en, seed=3100 + 13 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

VIDEO = dict(id="gp", folder="GTA6_VIDEO_LANZAMIENTO", file="VIDEO_FINAL",
             title="GTA 6 ya se juega: qué dicen de su jugabilidad quienes ya lo han jugado",
             format="Largo (16:9) · análisis post lanzamiento con material oficial", music="synthwave", music_fn=music_fn, voice="host", beats=B,
             overlay=R.overlay, grade=None, music_gain=0.42, max_tries=4, qa_metric="fonetica", qa_thr=0.995, trans=("cut", 0.0),
             final_codec="av1", target_mb=94, av1_preset=8,
             names=dict(narr_wav="recursos/narracion_original.flac", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="recursos/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.thumbnail2(c)
