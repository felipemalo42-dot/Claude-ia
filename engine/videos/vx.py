"""VIDEO_EXTRA — ¿Por qué Vice City es rosa? La historia real de sus colores, capa por capa.

Concepto: el video «raspa» la pintura de Vice City como un restaurador. Cada capítulo es una capa (1912 → 2026) con su
propia paleta, su propio tratamiento de color y su propia música original (se cambia de época como quien gira el dial de
una radio). Todas las imágenes son ilustraciones vectoriales originales: no se usa ningún material de Rockstar.
Fuentes y derechos: VIDEO_EXTRA/FUENTES_Y_REFERENCIAS.txt y VIDEO_EXTRA/REGISTRO_DE_DERECHOS.txt.
"""
import math, numpy as np, skia
import audio
from gfx import *
from components import watermark, ai_notice
from videos import vx_scenes as S

B = []
def beat(vo="", scene=None, **k): B.append(dict(vo=vo, scene=scene, **k))

# era → tratamiento de color; mus → (estilo musical original, nivel de energía 0..3)
# ---------------------------------------------------------------- GANCHO
beat("Desde mañana vas a poder caminar por una calle como esta. Hoteles rosa, menta y lavanda frente al mar, con letreros de neón. Es la Vice City de GTA 6.",
     S.sc_hook, section="GANCHO", era="none", mus=("synthwave", 1), exag=0.65, pre=0.7,
     note="Calle nocturna ilustrada (hoteles inventados, rasgos art déco genéricos). Los neones se encienden uno a uno.",
     emph=["calle como esta", "Vice City"], ritmo="Íntimo, con curiosidad. Pausa breve después de «neón».",
     sfx=[(0.25, "neon", 0.5), (0.75, "neon", 0.5), (1.25, "neon", 0.5), (1.7, "neon", 0.4)])
beat("Pero esos colores esconden algo. Los edificios reales que la inspiran se construyeron en los años treinta... y sus colores no son de los años treinta. Son de los años ochenta.",
     None, era="none", mus=("synthwave", 2), exag=0.65,
     note="Al decir «no son», la calle se vuelve blanca y de día; con «Son de los años ochenta», la pintura pastel vuelve de golpe.",
     emph=["esconden algo", "no son", "años ochenta"], ritmo="Suspenso: pausa larga en los puntos suspensivos; «Son de los años ochenta» seco y rotundo.",
     sfx=[("w:no son", "whoosh", 0.5), ("w:Son de los años ochenta", "brush", 0.7), ("w:Son de los años ochenta", "hit", 0.35)])
beat("Los eligió un diseñador de carne y hueso, con una carta de colores en la mano. Murió en 1989. Ocho años antes de que existiera el primer GTA.",
     None, era="none", mus=("synthwave", 2), exag=0.65, hold=0.5,
     note="Abanico de muestras de color; línea de tiempo 1989 → 1997 con la llave «8 años».",
     emph=["carne y hueso", "1989", "Ocho años antes"], ritmo="Bajar el volumen en «Murió en 1989»; remate firme.",
     sfx=[("w:carta de colores", "paper", 0.5), ("w:Murió", "tick", 0.5), ("w:Ocho años", "ding", 0.3)])
beat("", S.sc_sting, dur=2.4, era="none", mus=("synthwave", 1), sfx=[(0.0, "logo", 0.9)], trans=("flash", 0.3))
# ---------------------------------------------------------------- INTRO
beat("Estás en Sal y Asfalto. Hoy no traemos noticias: traemos una pregunta. ¿Por qué Vice City se ve así? "
     "Para responderla vamos a raspar la pintura, capa por capa, como hacen los restauradores. Siete capas y más de un siglo de historia. "
     "Y como siempre, el semáforo: en verde, lo documentado; en amarillo, nuestra interpretación.",
     S.sc_intro, section="INTRODUCCIÓN: LA PREGUNTA", era="none", mus=("synthwave", 1), trans=("zoom", 0.5),
     note="Título «¿Por qué Vice City se ve así?»; corte de pintura de 7 capas vacío; espátula que raspa; leyenda del semáforo.",
     emph=["una pregunta", "capa por capa", "Siete capas"], ritmo="Ritmo de presentación, claro y cálido.",
     sfx=[("w:¿Por qué", "pop", 0.4), ("w:raspar", "brush", 0.6), ("w:Siete capas", "chime", 0.3), ("w:en verde", "pop", 0.35), ("w:en amarillo", "pop", 0.35)])
beat("Empecemos por lo oficial. En su web, Rockstar describe Vice City así: «estamos muy lejos de los ochenta, pero Vice City sigue siendo la capital del sol y la diversión de Estados Unidos». "
     "Y al presentar sus barrios, nombra primero uno: Ocean Beach, con sus hoteles art déco en tonos pastel y su arena blanca. "
     "Guarda ese nombre: Ocean Beach. Porque existió mucho antes que cualquier videojuego.",
     S.sc_oficial, section="LO QUE DICE ROCKSTAR", era="none", mus=("synthwave", 1), trans=("slide_up", 0.5),
     note="Cita oficial (traducción + original en inglés) con etiqueta OFICIAL; señales viales con los barrios oficiales de Vice City.",
     emph=["lo oficial", "Ocean Beach", "mucho antes"], ritmo="Leer la cita con tono de cita; frenar en «Guarda ese nombre».",
     sfx=[("w:En su web", "paper", 0.4), ("w:barrios", "flap", 0.5), ("w:Guarda ese nombre", "ding", 0.3), ("w:existió", "stamp", 0.45)])
# ---------------------------------------------------------------- CAPA 1 · 1912
beat("Primera capa: la arena. A comienzos del siglo veinte, la isla que inspira esta parte de Vice City era una barra de arena llena de manglares, del otro lado de la bahía de Miami. "
     "En julio de 1912, los hermanos Lummus registraron el primer plano oficial para urbanizarla. ¿El nombre de su empresa? Ocean Beach Realty Company.",
     S.sc_island, section="CAPA 1 · 1912 · LA ARENA", era="1912", mus=("nature", 1), pre=1.0, trans=("paint", 0.7),
     note="Mapa esquemático en sepia (no a escala): tierra firme, bahía e isla con manglares; se dibuja la cuadrícula del plano y cae el sello.",
     emph=["la arena", "1912", "Ocean Beach Realty Company"], ritmo="Narrativo, de crónica; pausa antes de revelar el nombre de la empresa.",
     sfx=[(0.0, "tune", 0.5), ("w:manglares", "water", 0.35), ("w:primer plano", "paper", 0.5), ("w:Ocean Beach Realty", "stamp", 0.6)])
beat("Esa isla no es la ciudad de Miami: es Miami Beach, otro municipio, fundado en 1915. En la vida real son dos ciudades. "
     "En la web de Rockstar, Ocean Beach aparece como un barrio de Vice City.",
     None, era="1912", mus=("nature", 1),
     note="Línea de límite entre las dos ciudades; señal OCEAN BEACH con etiqueta OFICIAL.",
     emph=["no es la ciudad de Miami", "dos ciudades"], ritmo="Aclaración precisa, sin prisa.",
     sfx=[("w:otro municipio", "pop", 0.4), ("w:En la web de Rockstar", "pin", 0.4)])
beat("En los años veinte, la isla vivió una fiebre inmobiliaria. Hasta el 18 de septiembre de 1926. Ese día, un huracán de categoría cuatro golpeó de lleno la zona de Miami. "
     "El mar entró a las calles de la isla y derribó casinos frente a la playa. La fiebre se acabó de golpe, y en Florida, la Gran Depresión empezó antes que en el resto del país.",
     S.sc_storm, section="LA TORMENTA · 1926", era="storm", mus=("storm", 1), trans=("glitch", 0.4),
     note="Edificios estilo renacimiento mediterráneo y carteles de venta; llega la espiral del huracán; lluvia, viento y agua.",
     emph=["Hasta el 18 de septiembre de 1926", "categoría cuatro", "de golpe"], ritmo="Acelera con la fiebre; seco en «Hasta el 18 de septiembre».",
     sfx=[("w:fiebre", "coin", 0.35), ("w:Hasta el 18", "thunder", 0.7), ("w:Ese día", "wind", 0.6), ("w:categoría cuatro", "rain", 0.6),
          ("w:El mar entró", "wind", 0.6), ("w:casinos", "impact", 0.45), ("w:Gran Depresión", "stamp", 0.4)])
# ---------------------------------------------------------------- CAPA 2 · AÑOS 30
beat("Segunda capa, y primera sorpresa. Cuando la isla se levantó, en los años treinta, no había dinero para palacios. Se construyeron hoteles pequeños y modestos, de estuco, para alquilar por temporada. "
     "Arquitectos como {L. Murray Dixon|Él Múrrei Díxon} los llenaron de trucos: cejas de concreto sobre las ventanas para dar sombra, ventanas redondas como de barco y adornos agrupados de tres en tres.",
     S.sc_blueprint, section="CAPA 2 · AÑOS 30 · EL BLANCO", era="1930", mus=("swing30", 2), pre=1.0, trans=("paint", 0.7),
     note="Plano azul: los hoteles se dibujan trazo a trazo; flechas señalan cejas, ojos de buey y la regla de tres.",
     emph=["primera sorpresa", "cejas", "de tres en tres"], ritmo="Ágil, enumerativo, con swing.",
     sfx=[(0.0, "tune", 0.5), ("w:hoteles pequeños", "paper", 0.4), ("w:Murray Dixon", "pop", 0.4), ("w:cejas", "tick", 0.5),
          ("w:ventanas redondas", "tick", 0.5), ("w:de tres en tres", "tick", 0.5)])
beat("Era el art déco tropical. Y aquí viene lo bueno: casi todos esos edificios eran blancos. "
     "Según el Servicio de Parques Nacionales de Estados Unidos, se pintaban de blanco, con pequeños toques de verde jade, ocre o coral. Nada de rosa chicle. Nada de lavanda.",
     S.sc_white, era="1930b", mus=("swing30", 3), trans=("fade", 0.5),
     note="El plano se convierte en la calle blanca de los años 30; muestras jade/ocre/coral; rosa y lavanda tachados.",
     emph=["eran blancos", "verde jade, ocre o coral", "Nada de rosa chicle"], ritmo="Revelación: pausa antes de «eran blancos».",
     sfx=[("w:eran blancos", "chime", 0.45), ("w:verde jade", "pop", 0.35), ("w:Nada de rosa", "buzz", 0.22)])
# ---------------------------------------------------------------- CAPA 3 · AÑOS 70
beat("Tercera capa: el abandono. En los años setenta, South Beach era un barrio de jubilados con pocos recursos, muchos de ellos judíos y sobrevivientes del Holocausto, en hoteles viejos que nadie cuidaba. "
     "Los planes de renovación urbana querían demoler casi todo.",
     S.sc_decline, section="CAPA 3 · AÑOS 70 · EL ABANDONO", era="1970", mus=("seventies", 1), pre=1.0, trans=("paint", 0.7),
     note="La misma calle, gastada y gris; sillas en los porches; entra una excavadora con un plan de demolición.",
     emph=["el abandono", "demoler casi todo"], ritmo="Más lento y grave.",
     sfx=[(0.0, "tune", 0.5), ("w:renovación urbana", "rumble", 0.5)])
beat("Entonces apareció Barbara Capitman: una viuda de más de cincuenta años, tímida y de voz suave... y tenaz como pocas. "
     "En 1976 fundó la Liga de Preservación del Diseño de Miami. Organizó vigilias y marchas, y se plantó delante de las excavadoras.",
     S.sc_capitman, era="1970", mus=("seventies", 2), trans=("fade", 0.4),
     note="Tarjeta de nombre; documento mecanografiado de 1976; velas de vigilia; una silueta frena a la excavadora.",
     emph=["tenaz como pocas", "delante de las excavadoras"], ritmo="Pausa en los puntos suspensivos; «tenaz como pocas» con orgullo.",
     sfx=[("w:Barbara Capitman", "paper", 0.4), ("w:En 1976", "typing", 0.4), ("w:excavadoras", "rumble", 0.35)])
beat("En mayo de 1979, lo logró: el distrito entró al Registro Nacional de Lugares Históricos. Fue el primer barrio del siglo veinte reconocido como histórico en Estados Unidos. "
     "Pero ese sello no detuvo las demoliciones. Hacía falta algo más llamativo que un papel.",
     S.sc_register, era="1970", mus=("seventies", 2), trans=("slide_up", 0.5),
     note="Certificado y sello «14 de mayo de 1979»; lista de hoteles demolidos (Boulevard 1980, New Yorker 1981, Senator 1988).",
     emph=["lo logró", "primer barrio del siglo veinte", "algo más llamativo"], ritmo="Triunfal y luego seco.",
     sfx=[("w:lo logró", "stamp", 0.6), ("w:no detuvo", "impact", 0.35)])
# ---------------------------------------------------------------- CAPA 4 · 1980
beat("Cuarta capa: el color. Y aquí entra nuestro protagonista: Leonard Horowitz. Un diseñador neoyorquino que se mudó a South Beach cuando su padre le retiró el apoyo económico por ser gay. "
     "Fundó la Liga junto a Capitman... y tuvo una idea: si nadie mira estos edificios, hay que obligar a la gente a mirarlos.",
     S.sc_horowitz, section="CAPA 4 · 1980 · EL PASTEL", era="1980", mus=("synthpop", 1), pre=1.0, trans=("paint", 0.7),
     note="Tarjeta de nombre de Leonard Horowitz; trayecto Nueva York → South Beach; la idea en tipografía grande.",
     emph=["nuestro protagonista", "obligar a la gente a mirarlos"], ritmo="Cálido; la idea se dice como una ocurrencia brillante.",
     sfx=[(0.0, "tune", 0.5), ("w:Leonard Horowitz", "pop", 0.45), ("w:una idea", "ding", 0.3)])
beat("Armó una paleta con el sol, el cielo, el mar y la arena. La primera prueba fue una panadería, Friedman's, en la calle siete y la avenida Washington. Era completamente blanca. "
     "La dejó en rosa algodón de azúcar, azul pervinca, crema y verde menta: parecía un pastel de cumpleaños.",
     S.sc_bakery, era="1980", mus=("synthpop", 2), trans=("fade", 0.4),
     note="Abanico de muestras; la panadería blanca se pinta a brochazos con los cuatro colores; aparecen velitas de cumpleaños.",
     emph=["completamente blanca", "pastel de cumpleaños"], ritmo="Juguetón; cada color con su golpe.",
     sfx=[("w:paleta", "flap", 0.5), ("w:panadería", "pop", 0.35), ("w:rosa algodón", "brush", 0.6), ("w:azul pervinca", "brush", 0.6),
          ("w:crema", "brush", 0.55), ("w:verde menta", "brush", 0.6), ("w:pastel de cumpleaños", "chime", 0.4)])
beat("A muchos vecinos no les gustó. Una señora protestó: «esto no somos nosotros». Pero edificio por edificio, la paleta se fue extendiendo. "
     "Y hubo un truco más fino: el color principal de un edificio pasaba a los detalles del siguiente, para que la calle entera se leyera como una sola pieza.",
     S.sc_continuity, era="1980", mus=("synthpop", 2), trans=("whip", 0.45),
     note="Globo de diálogo «Esto no somos nosotros» (y la cita original «Deco schmeco»); la calle se pinta edificio por edificio; flechas: el cuerpo de uno pasa a los detalles del siguiente.",
     emph=["esto no somos nosotros", "una sola pieza"], ritmo="Humor en la cita; luego explicativo.",
     sfx=[("w:esto no somos", "pop", 0.4), ("w:edificio por edificio", "brush", 0.5), ("w:color principal", "brush", 0.5), ("w:una sola pieza", "ding", 0.3)])
beat("Hoy, según el Servicio de Parques Nacionales, en el distrito es obligatorio usar tonos pastel claros: una estética que nació en los ochenta... y que ahora se protege como si fuera histórica.",
     S.sc_today, era="1980", mus=("synthpop", 3), trans=("zoom", 0.45),
     note="Sello «OBLIGATORIO: PASTEL CLARO»; la etiqueta «histórico» se pega sobre «1980».",
     emph=["obligatorio", "como si fuera histórica"], ritmo="Ironía suave en el final.",
     sfx=[("w:obligatorio", "stamp", 0.55)])
# ---------------------------------------------------------------- CAPA 5 · 1984
beat("Quinta capa: la televisión. En septiembre de 1984, NBC estrenó Miami Vice, con Michael Mann como productor ejecutivo. Mann tenía una regla famosa: nada de tonos tierra. Ni marrones, ni beige. "
     "Contó que lo entendió jugando con muestras de una tienda de pintura: con dos colores no pasa nada; con tres, ya puedes contar una historia.",
     S.sc_tv, section="CAPA 5 · 1984 · LA TELEVISIÓN", era="1984", mus=("synthwave", 2), pre=1.0, trans=("paint", 0.7),
     note="Televisor de tubo en un living de los 80; muestras de tonos tierra tachadas; dos muestras = nada, tres = una historia.",
     emph=["nada de tonos tierra", "con tres"], ritmo="Enérgico, ochentero.",
     sfx=[(0.0, "tune", 0.5), (0.9, "tv_on", 0.5), ("w:nada de tonos tierra", "buzz", 0.22), ("w:con tres", "chime", 0.3)])
beat("Si una pared no encajaba, el equipo de la serie la repintaba. Y según el Servicio de Parques Nacionales, hasta los colores de los carritos de comida que se ven en la presentación de la serie los eligió... Leonard Horowitz.",
     S.sc_tv2, era="1984", mus=("synthwave", 3), trans=("fade", 0.3),
     note="Una pared beige se repinta en la pantalla; carritos de comida pastel; aparece el nombre de Horowitz.",
     emph=["la repintaba", "Leonard Horowitz"], ritmo="Pausa de intriga antes del nombre.",
     sfx=[("w:repintaba", "brush", 0.6), ("w:carritos", "pop", 0.35), ("w:Leonard Horowitz", "ding", 0.35)])
beat("Él no llegó a ver lo que vino después. Murió de sida en 1989, con cuarenta y tres años. Sus amigos esparcieron sus cenizas en el mar, frente a los hoteles de Ocean Drive que él había pintado.",
     S.sc_coda, era="coda", mus=("seventies", 0), pre=0.6, hold=1.4, exag=0.45, cfg=0.45, trans=("fade", 1.0),
     note="Noche en el mar: un bote pequeño, la fila de hoteles iluminados a lo lejos, partículas que caen al agua.",
     emph=["no llegó a ver", "1989"], ritmo="Lento, íntimo, voz baja. Silencio al final.",
     sfx=[(0.2, "water", 0.45)])
# ---------------------------------------------------------------- CAPA 6 · 2002
beat("Sexta capa: el videojuego. Vice City ya aparecía en el primer GTA, de 1997, vista desde arriba. Pero la Vice City que todos recordamos llegó en 2002, ambientada en 1986.",
     S.sc_game, section="CAPA 6 · 2002 · EL VIDEOJUEGO", era="2002", mus=("electro", 2), pre=1.0, trans=("paint", 0.7),
     note="Ciudad abstracta vista desde arriba en píxeles (1997); luego la calle pixelada de noche (2002) con un reloj genérico «1986».",
     emph=["1997", "2002", "1986"], ritmo="Vuelve la energía.",
     sfx=[(0.0, "tune", 0.5), ("w:1997", "coin", 0.4), ("w:llegó en 2002", "glitch", 0.3)])
beat("Según la historia de su desarrollo, el equipo veía Miami Vice mientras trabajaba y el director de arte, Aaron Garbut, la usó como referencia para la luz de neón. "
     "Hasta Lance Vance, el socio de Tommy Vercetti, tenía la voz de Philip Michael Thomas: el Tubbs de Miami Vice. "
     "Fíjate en la cadena: un juego que imita a una serie, que filmó una paleta, que se pintó sobre edificios blancos.",
     S.sc_game2, era="2002", mus=("electro", 3), trans=("fade", 0.4),
     note="Fichas con los datos del desarrollo; la cadena de cuatro eslabones se ilumina: juego → serie → paleta → edificios blancos.",
     emph=["referencia para la luz de neón", "el Tubbs de Miami Vice", "la cadena"], ritmo="Enumerativo; la cadena se dice in crescendo.",
     sfx=[("w:Aaron Garbut", "pop", 0.4), ("w:Lance Vance", "pop", 0.4), ("w:Fíjate", "whoosh", 0.4), ("w:imita", "tick", 0.5), ("w:filmó", "tick", 0.5), ("w:pintó", "tick", 0.5)])
# ---------------------------------------------------------------- CAPA 7 · 2026
beat("Séptima capa: la de mañana. Según Aaron Garbut, el equipo recorrió el sur de Florida y estudió la historia y la arquitectura de Miami. "
     "Según la prensa de Miami, en el primer tráiler aparece una versión del Hotel Victor, un hotel real de Ocean Drive. En Vice City se llama... Hotel Dixon. Como {L. Murray Dixon|Él Múrrei Díxon}, el arquitecto que lo diseñó en 1937.",
     S.sc_2026, section="CAPA 7 · 2026 · LAS PANTALLAS", era="2026", mus=("trap26", 2), pre=1.0, trans=("paint", 0.7),
     note="Calle de neón; placas de nombre: «Hotel Victor (1937)» → «Hotel Dixon»; fichas de fuente (AP, Axios, Miami New Times).",
     emph=["Hotel Dixon", "L. Murray Dixon", "1937"], ritmo="Revelación: pausa antes de «Hotel Dixon».",
     sfx=[(0.0, "tune", 0.5), (0.6, "neon", 0.45), ("w:Hotel Dixon", "neon", 0.6), ("w:en 1937", "ding", 0.3)])
beat("Rockstar incluso le da a quien reservó el juego un paquete, Vintage Vice City, para volver, dice, a cuando el neón brillaba más, con el Ocean View Hotel y el apellido Vercetti en su material oficial: guiños directos a 2002.",
     S.sc_vintage, era="2026", mus=("trap26", 2), trans=("fade", 0.4),
     note="Cita breve del paquete oficial (bono por reservar el juego); fichas «Ocean View Hotel» y «Vercetti» enlazadas a 2002.",
     emph=["cuando el neón brillaba más", "guiños directos a 2002"], ritmo="Cómplice.",
     sfx=[("w:Vintage Vice City", "pop", 0.4), ("w:guiños", "ding", 0.3)])
beat("Pero hay algo nuevo. En varias imágenes oficiales de GTA 6, la gente está grabando: celulares en alto, una selfi frente a la policía, videos virales. "
     "Esta es nuestra lectura, en amarillo: en 2026, la brocha de Vice City es la cámara del celular.",
     S.sc_phones, era="2026", mus=("trap26", 3), trans=("glitch", 0.35),
     note="Celulares que graban la calle; contador de vistas; etiqueta amarilla INTERPRETACIÓN.",
     emph=["algo nuevo", "la cámara del celular"], ritmo="Rápido en la enumeración; remate pausado.",
     sfx=[("w:grabando", "phone", 0.45), ("w:selfi", "shutter", 0.5), ("w:virales", "phone", 0.4), ("w:nuestra lectura", "pop", 0.4)])
beat("Y la cadena ya dio la vuelta completa. Según la agencia AP, el condado de Miami-Dade firmó un acuerdo de {3,9 millones|tres coma nueve millones} de dólares con Rockstar, "
     "que incluye un letrero gigante en el techo de la arena del Heat de Miami {que dice: Welcome to Vice City|que dice: Güélcom tu Vais Síti}. La ciudad real ahora se viste de ciudad ficticia. "
     "No a todos les gusta: la sheriff del condado y un comisionado de Miami Beach se opusieron.",
     S.sc_loop, section="LA VUELTA COMPLETA", era="2026", mus=("trap26", 2), trans=("whip", 0.45),
     note="Ilustración genérica de una arena con el letrero «WELCOME TO VICE CITY»; cifra del acuerdo; dos posturas en contra.",
     emph=["vuelta completa", "Welcome to Vice City", "se viste de ciudad ficticia"], ritmo="Asombro contenido; neutral al citar las críticas.",
     sfx=[("w:3,9 millones", "coin", 0.4), ("w:Welcome to Vice City", "neon", 0.6), ("w:se opusieron", "buzz", 0.18)])
# ---------------------------------------------------------------- MATIZ
beat("Antes de cerrar, una verdad incómoda. El pastel salvó los edificios, pero no a todos sus vecinos. "
     "Según el Servicio de Parques Nacionales, cuando South Beach se puso de moda, desplazó a la mayoría de los jubilados por los que había empezado la lucha. "
     "El hijo de Barbara Capitman se preguntaba en 2014 si eso era lo que querían. Para nosotros, esa contradicción también es Vice City: una ciudad que se burla del exceso... y que nació de él.",
     S.sc_price, section="EL PRECIO DEL PASTEL", era="1980", mus=("seventies", 1), exag=0.5, trans=("fade", 0.8),
     note="Mañana pastel y tranquila; una silla vacía en un porche; cita del hijo de Capitman; etiqueta INTERPRETACIÓN.",
     emph=["verdad incómoda", "no a todos sus vecinos", "y que nació de él"], ritmo="Sereno y honesto; sin dramatizar.",
     sfx=[("w:Para nosotros", "pop", 0.3)])
# ---------------------------------------------------------------- GUÍA DE CAMPO
beat("Y ahora, tu misión para mañana. Cuando llegues a Ocean Beach, busca estas pistas: cejas sobre las ventanas, ojos de buey, adornos de tres en tres, bloques de vidrio, esquinas redondeadas y letreros verticales de neón. "
     "Si las encuentras, Rockstar hizo la tarea.",
     S.sc_guide, section="GUÍA DE CAMPO PARA MAÑANA", era="none", mus=("synthwave", 2), trans=("paint", 0.7),
     note="Seis tarjetas con iconos propios; cada una se marca cuando se nombra.",
     emph=["tu misión", "hizo la tarea"], ritmo="Práctico, como una lista de chequeo.",
     sfx=[(0.0, "tune", 0.4), ("w:cejas", "tick", 0.5), ("w:ojos de buey", "tick", 0.5), ("w:de tres en tres", "tick", 0.5), ("w:bloques de vidrio", "tick", 0.5),
          ("w:esquinas redondeadas", "tick", 0.5), ("w:letreros verticales", "tick", 0.5), ("w:hizo la tarea", "ding", 0.35)])
# ---------------------------------------------------------------- CIERRE
beat("La próxima vez que alguien te diga que Vice City es una copia de Miami, ya sabes la respuesta: es una copia de una copia de una copia. "
     "Una tormenta, un estilo barato, una activista tenaz, un diseñador con una carta de colores, una serie de televisión y un estudio de videojuegos. Cada uno le puso una capa de pintura encima.",
     S.sc_close, section="CIERRE", era="none", mus=("synthwave", 2), trans=("zoom", 0.5),
     note="El corte de pintura completo: cada capa recibe su nombre mientras se enumera.",
     emph=["una copia de una copia de una copia", "una capa de pintura encima"], ritmo="Conclusión con aplomo; enumeración en crescendo.",
     sfx=[("w:una copia de una copia", "whoosh", 0.4), ("w:Una tormenta", "pop", 0.35), ("w:un estilo barato", "pop", 0.35), ("w:una activista", "pop", 0.35),
          ("w:un diseñador", "pop", 0.35), ("w:una serie", "pop", 0.35), ("w:un estudio", "pop", 0.35), ("w:capa de pintura", "chime", 0.4)])
beat("Cuéntame en los comentarios cuál es la fachada más art déco que encuentres en el juego. Y si te gustan estas historias, suscríbete a Sal y Asfalto: aquí, Vice City se explica capa por capa.",
     S.sc_cta, era="none", mus=("synthwave", 1), exag=0.6, hold=0.6, trans=("fade", 0.5),
     note="Calle de neón; pregunta para comentarios; botón de suscripción.",
     emph=["la fachada más art déco", "capa por capa"], ritmo="Cercano.",
     sfx=[("w:comentarios", "pop", 0.35), ("w:suscríbete", "ding", 0.3)])
beat("", S.sc_end, dur=20, section="PANTALLA FINAL", era="none", mus=("synthwave", 1), trans=("fade", 0.6))

for b in B:  # energía musical por beat (la usa el compositor por épocas)
    if "mus" in b: b["energy"] = b["mus"][1]

# ---------------------------------------------------------------- música original por épocas
def music_fn(total, beats_tl):
    """Une pistas originales de distinto estilo según la época de cada capítulo, con fundidos cruzados.
    Los cambios coinciden con el efecto «dial de radio» del inicio de cada capa."""
    segs = []
    for b, bd in zip(B, beats_tl):
        st, lv = b.get("mus", ("synthwave", 1))
        if segs and segs[-1]["style"] == st: segs[-1]["en"].append((bd["start"] - segs[-1]["t0"], lv))
        else: segs.append(dict(style=st, t0=bd["start"], en=[(0.0, lv)]))
    n = int(total * audio.SR); out = np.zeros((n, 2)); xf = 1.4
    for i, sg in enumerate(segs):
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        a0 = max(0.0, sg["t0"] - (xf / 2 if i else 0)); dur = (t1 - a0) + (xf / 2 if i + 1 < len(segs) else 0)
        en = [(max(0.0, tt + (sg["t0"] - a0)), lv) for tt, lv in sg["en"]]
        y = audio.compose(sg["style"], dur, energy=en, seed=1100 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

# ---------------------------------------------------------------- tratamiento de color por época
GRADES = {
    "none": dict(sat=1.0, sep=0.0, warm=0.0, con=1.0, lift=0.0, grain=0.0, vig=0.0),
    "1912": dict(sat=0.25, sep=0.85, warm=0.0, con=1.04, lift=0.03, grain=0.55, vig=0.35),
    "storm": dict(sat=0.2, sep=0.7, warm=-0.02, con=1.12, lift=0.0, grain=0.6, vig=0.5),
    "1930": dict(sat=0.35, sep=0.12, warm=0.0, con=1.03, lift=0.0, grain=0.25, vig=0.2),
    "1930b": dict(sat=0.75, sep=0.06, warm=0.01, con=1.02, lift=0.0, grain=0.2, vig=0.15),
    "1970": dict(sat=0.72, sep=0.2, warm=0.05, con=0.93, lift=0.05, grain=0.35, vig=0.25),
    "1980": dict(sat=1.06, sep=0.0, warm=0.02, con=1.0, lift=0.0, grain=0.0, vig=0.1),
    "1984": dict(sat=1.12, sep=0.0, warm=0.0, con=1.04, lift=0.0, grain=0.0, vig=0.2),
    "coda": dict(sat=0.85, sep=0.0, warm=-0.04, con=1.0, lift=0.0, grain=0.1, vig=0.35),
    "2002": dict(sat=1.1, sep=0.0, warm=0.0, con=1.02, lift=0.0, grain=0.0, vig=0.15),
    "2026": dict(sat=1.12, sep=0.0, warm=0.0, con=1.06, lift=0.0, grain=0.0, vig=0.22),
}
_LW = (0.2126, 0.7152, 0.0722)
def _matrix(g):
    s = g["sat"]; lw = _LW
    M = np.array([[lw[0] * (1 - s) + s, lw[1] * (1 - s), lw[2] * (1 - s)],
                  [lw[0] * (1 - s), lw[1] * (1 - s) + s, lw[2] * (1 - s)],
                  [lw[0] * (1 - s), lw[1] * (1 - s), lw[2] * (1 - s) + s]])
    SEP = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
    M = (1 - g["sep"]) * M + g["sep"] * SEP
    M = np.diag([1 + g["warm"], 1.0, 1 - g["warm"]]) @ M
    con = g["con"]; M = M * con; off = np.full(3, 0.5 * (1 - con))
    M = M * (1 - g["lift"]); off = off * (1 - g["lift"]) + g["lift"]
    out = []
    for r in range(3): out += [float(M[r, 0]), float(M[r, 1]), float(M[r, 2]), 0.0, float(off[r])]
    return out + [0, 0, 0, 1, 0]

_GR = {}
def _grain():
    if "g" not in _GR: _GR["g"] = Grain(1920, 1080, amount=28, seed=11)
    return _GR["g"]

def _era_at(gt, ctx):
    if "eras" not in _GR:
        _GR["eras"] = [(bd["start"], b.get("era", "none")) for b, bd in zip(B, ctx.tl["beats"])]
    eras = _GR["eras"]; cur = eras[0][1]; prev = cur; tchg = -99
    for st, e in eras:
        if gt >= st - 0.35:
            if e != cur: prev, cur, tchg = cur, e, st - 0.35
    k = clamp((gt - tchg) / 0.7)
    a, b = GRADES[prev], GRADES[cur]
    return {key: a[key] + (b[key] - a[key]) * k for key in a}

def grade(c, gt, ctx):
    g = _era_at(gt, ctx)
    if all(abs(g[k] - GRADES["none"][k]) < 1e-3 for k in g): return
    surf = c.getSurface(); img = surf.makeImageSnapshot()
    p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Matrix(_matrix(g)))
    c.drawImage(img, 0, 0, skia.SamplingOptions(), p)
    if g["grain"] > 0.01: _grain().draw(c, g["grain"])
    if g["vig"] > 0.01: vignette(c, ctx.W, ctx.H, g["vig"])

def overlay(c, gt, ctx):
    W, H = ctx.W, ctx.H
    if 2.5 < gt < ctx.total - 20: watermark(c, W, H, 0.42)
    if gt < 9: ai_notice(c, W, H, clamp(9 - gt), "Ilustración original de Sal y Asfalto · no es una imagen del juego")

VIDEO = dict(id="vx", folder="VIDEO_EXTRA", file="VIDEO_FINAL",
             title="¿Por qué Vice City es rosa? La historia real de sus colores (GTA 6)",
             format="Largo (16:9) · producción especial", music="synthwave", music_fn=music_fn, voice="host", beats=B,
             overlay=overlay, grade=grade, music_gain=0.5, max_tries=12, qa_metric="fonetica", qa_thr=0.995,
             names=dict(narr_wav="recursos/narracion_original.flac", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="recursos/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    S.thumbnail(c)
