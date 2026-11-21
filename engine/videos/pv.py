"""VIDEO_LARGO_2 — «Planeta Vice City: el documental de los humanos de GTA 6»

Formato nuevo (no lo hace ningún canal): un documental de naturaleza cuya especie son los habitantes de Vice City (los
personajes que el juego mueve por su cuenta). Todo sale de partidas reales publicadas tras el lanzamiento (19/11/2026):
- toaster · «GTA 6 NPC Interactions Are UNREAL» (4K): reacciones de los habitantes; sus frases son las originales del juego
  (transcritas del audio, en inglés en pantalla y traducidas en la voz).
- Yamatum O · «พาเที่ยวเมือง Vice City» (1080p): paseo por la ciudad, la playa, el gimnasio al aire libre y la noche.
Solo se describe lo que se ve. Lo que dijo Rockstar se dice «según Rockstar». Sin spoilers de la historia.
"""
import os
import numpy as np
import audio
from videos import dc_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def X(vid, t): return f"x:{vid}@{t}"

TOA = "cEDUO1zjB5c"   # toaster · «GTA 6 NPC Interactions Are UNREAL» (19/11/2026), 4K
THA = "gvlY1gVmSKM"   # Yamatum O · «พาเที่ยวเมือง Vice City | GTA 6» (19/11/2026), 1080p
LAZ = "NwQKirh2dxE"   # LazarBeam · «Testing Everything In GTA 6» (20/11/2026), 1080p; encuadre que deja fuera su cámara (arriba a la izquierda)
NOCAM = dict(z=(1.42, 1.47), f=(0.8, 0.8))
# toaster lleva subtítulos incrustados (73-86 % de la altura): se encuadra el 72 % de arriba (sobra resolución: es 4K)
TOACAP = dict(z=(1.40, 1.44), f=(0.5, 0.0))

# ================================================================ APERTURA
beat("En el sureste de un país que no existe vive una especie fascinante. Pasa el día tumbada al sol, hace ejercicio delante de desconocidos y, cuando alguien invade su espacio, se lo dice a la cara.",
     mus=("nature", 1), pre=0.3, id="p01", cert="OBSERVADO",
     shots=[S(None, X(THA, 646.0), z=(1.0, 1.06)), S("tumbada al sol", X(THA, 781.0), z=(1.0, 1.06)),
            S("hace ejercicio", X(THA, 1300.0), z=(1.0, 1.06)), S("se lo dice", X(TOA, 9.0), **TOACAP)],
     sfx=[(0.0, "bird", 0.3), ("w:a la cara", "pop", 0.35)])
beat("Durante días la hemos observado en su hábitat natural, a través de partidas reales de GTA 6. Bienvenidos a Planeta Vice City.",
     mus=("nature", 2), id="p02",
     shots=[S(None, X(THA, 1662.0), z=(1.0, 1.05)),
            S("Bienvenidos", "g:cover", kicker="UN DOCUMENTAL DE SAL Y ASFALTO", lines=["PLANETA", "VICE CITY"], sub="Los humanos de GTA 6, observados en libertad")],
     sfx=[("w:Bienvenidos", "chime", 0.45)])
beat("Este es un documental de naturaleza diferente. No vamos a estudiar caimanes ni flamencos, sino a las personas que el juego mueve por su cuenta: los habitantes de Vice City. Aquí no hay misiones ni historia: solo la vida diaria de una ciudad que sigue funcionando aunque nadie la mire. Como en todo buen documental, la regla es no intervenir. El problema es que aquí el equipo de grabación lleva un mando en la mano, y no siempre resiste la tentación.",
     mus=("nature", 1), pre=0.4, id="p03",
     shots=[S(None, "g:sting"), S("sino a las personas", X(THA, 818.0), z=(1.0, 1.05)), S("los habitantes", X(THA, 832.0), z=(1.0, 1.05)),
            S("Como en todo buen documental", X(THA, 676.0), z=(1.0, 1.05))],
     sfx=[(0.0, "logo", 0.5)])
beat("Todo lo que vas a ver son partidas reales, grabadas por jugadores en los primeros días después del lanzamiento. Las frases de los habitantes son las originales del juego: en pantalla las ves en inglés, y aquí te las traducimos.",
     mus=("nature", 1), id="p04",
     shots=[S(None, "g:creators", title="EL EQUIPO DE OBSERVACIÓN", subt="Partidas reales publicadas tras el lanzamiento (19/11/2026)",
              rows=[("toaster", "Encuentros con los habitantes"), ("Yamatum O", "Un día entero por Vice City"), ("LazarBeam", "Visita al zoológico")],
              foot="Créditos de cada plano en pantalla y en la descripción"),
            S("Las frases", X(TOA, 2.0), **TOACAP)],
     sfx=[(0.1, "paper", 0.35)])
beat("Primero, su ficha. Nombre común: habitante de Vice City. Nombre científico: ninguno, porque nos lo acabamos de inventar. Hábitat: playas, avenidas y gimnasios al aire libre. Y su mayor amenaza, como verás, suele ser el jugador.",
     mus=("nature", 1), id="p05",
     shots=[S(None, "g:especie", name="Habitante de Vice City", latin="Homo viceensis (nombre inventado)",
              rows=[("Hábitat", "Playas, avenidas y gimnasios al aire libre"), ("Actividad", "De día y de noche"), ("Mayor amenaza", "El jugador")],
              cues=["Hábitat", "playas", "mayor amenaza"], note="Ficha de broma: el nombre científico no existe")],
     sfx=[(0.1, "paper", 0.4), ("w:el jugador", "pop", 0.4)])

# ================================================================ 1 · EL HÁBITAT
beat("Empecemos por su hábitat preferido: la playa. A mediodía, la arena se llena de toallas, sombrillas y hamacas, y de cuerpos que no se mueven durante horas. Desde lejos, es difícil saber si duermen o si simplemente disfrutan del sol. Probablemente, ni ellos lo saben.",
     chapter=(1, "EL HÁBITAT"), mus=("tropical", 1), pre=1.4, id="h01", cert="OBSERVADO",
     shots=[S(None, X(THA, 606.0), z=(1.0, 1.05)), S("A mediodía", X(THA, 663.0), z=(1.0, 1.05)),
            S("hamacas", X(THA, 690.0), z=(1.0, 1.06)), S("cuerpos", X(THA, 806.0), z=(1.0, 1.06)), S("Desde lejos", X(THA, 653.0), z=(1.0, 1.05))],
     sfx=[(0.0, "water", 0.3)])
beat("Otros ejemplares prefieren el movimiento. Caminan en pareja por la orilla, juegan con flotadores o se meten al agua. Ninguno parece tener prisa, y casi ninguno se fija en el jugador, que cruza la arena en bicicleta. Y si quiere integrarse, también puede sentarse en el césped de un parque y, sencillamente, mirar.",
     mus=("tropical", 1), id="h02", cert="OBSERVADO",
     shots=[S(None, X(THA, 672.0), z=(1.0, 1.05)), S("Caminan en pareja", X(THA, 740.0), z=(1.0, 1.05)), S("juegan con flotadores", X(THA, 796.0), z=(1.0, 1.06)),
            S("Ninguno parece", X(THA, 905.0), z=(1.0, 1.05)), S("cruza la arena", X(THA, 625.0), z=(1.0, 1.05)), S("sentarse en el césped", X(THA, 589.0), z=(1.0, 1.06))])
beat("En la orilla esperan motos de agua, y por la arena circulan cuatrimotos levantando polvo. Para esta especie, la arena es terreno de todos.",
     mus=("tropical", 2), id="h03", cert="OBSERVADO",
     shots=[S(None, X(THA, 872.0), z=(1.0, 1.06)), S("cuatrimotos", X(THA, 962.0), z=(1.0, 1.05)), S("Para esta especie", X(THA, 985.0), z=(1.0, 1.05))],
     sfx=[("w:motos de agua", "water", 0.3)])
beat("Pero el hábitat también está cambiando. En esta playa hay obras: excavadoras y camiones trabajando sobre la arena, a pocos metros de los bañistas.",
     mus=("tropical", 1), id="h04", cert="OBSERVADO",
     shots=[S(None, X(THA, 342.0), z=(1.0, 1.05)), S("excavadoras", X(THA, 433.0), z=(1.0, 1.06)), S("a pocos metros", X(THA, 465.0), z=(1.0, 1.05))],
     sfx=[("w:excavadoras", "rumble", 0.3)])
beat("Lejos del mar, la especie se desplaza en grandes manadas de vehículos, por avenidas con palmeras, edificios de colores y semáforos.",
     mus=("synthpop", 1), id="h05", cert="OBSERVADO",
     shots=[S(None, X(THA, 92.0), z=(1.0, 1.05)), S("por avenidas", X(THA, 212.0), z=(1.0, 1.05)), S("edificios de colores", X(THA, 241.0), z=(1.0, 1.05))])
beat("Al caer la tarde, en las calles más antiguas, los habitantes pasean entre fachadas de colores pastel, autos estacionados y palmeras. Es la hora en que la ciudad pasa del rosa al naranja.",
     mus=("synthpop", 1), id="h06", cert="OBSERVADO",
     shots=[S(None, X(THA, 1046.0), z=(1.0, 1.05)), S("fachadas", X(THA, 1066.0), z=(1.0, 1.05)), S("autos estacionados", X(THA, 1083.0), z=(1.0, 1.05))])
beat("Y cuando cae la noche, el hábitat se transforma. Se encienden las luces de neón de los hoteles, y la especie sale de sus refugios.",
     mus=("synthwave", 1), id="h07", cert="OBSERVADO",
     shots=[S(None, X(THA, 1702.0), z=(1.0, 1.05)), S("Se encienden", X(THA, 1412.0), z=(1.0, 1.06)), S("la especie sale", X(THA, 1440.0), z=(1.0, 1.05))],
     sfx=[("w:neón", "neon", 0.35)])
beat("Vista desde un helicóptero, la ciudad entera parece un organismo vivo: miles de luces que se mueven a la vez, sin que nadie las dirija. Nota de campo número uno: para esta especie, la playa también es una carretera, y la noche, otro día más.",
     mus=("synthwave", 2), id="h08", cert="OBSERVADO",
     shots=[S(None, X(THA, 1690.0 + 30.0), z=(1.0, 1.05)), S("miles de luces", X(THA, 1745.0), z=(1.0, 1.05))])

# ================================================================ 2 · RITUALES
beat("Uno de los rituales más curiosos ocurre al atardecer, junto a la playa: el gimnasio al aire libre. Cualquiera que conozca Miami Beach reconocerá la idea.",
     chapter=(2, "RITUALES"), mus=("tropical", 2), pre=1.4, id="r01", cert="OBSERVADO",
     shots=[S(None, X(THA, 1107.0), z=(1.0, 1.05))])
beat("Allí, con el sol bajando, el jugador puede unirse a la costumbre local: dominadas, press de banca, sentadillas y pesas rusas, con un contador de repeticiones en pantalla. A su alrededor, algunos habitantes entrenan a su ritmo.",
     mus=("tropical", 2), id="r02", cert="OBSERVADO",
     shots=[S(None, X(THA, 1116.0), z=(1.0, 1.06)), S("press de banca", X(THA, 1183.0), z=(1.0, 1.06)), S("sentadillas", X(THA, 1286.0), z=(1.0, 1.06)),
            S("pesas rusas", X(THA, 1331.0), z=(1.0, 1.06)), S("A su alrededor", X(THA, 1140.0), z=(1.06, 1.0))],
     sfx=[("w:dominadas", "hit", 0.25), ("w:sentadillas", "hit", 0.25)])
beat("Y en este gimnasio, el saludo también forma parte del ritual. El jugador le estrecha la mano a un habitante musculoso, que sigue a lo suyo: no suelta las pesas ni un momento.",
     mus=("tropical", 2), id="r025", cert="OBSERVADO",
     shots=[S(None, X(THA, 1245.0), z=(1.0, 1.05)), S("que sigue a lo suyo", X(THA, 1256.5), z=(1.06, 1.0))])
beat("Nadie parece extrañarse: en este ecosistema, levantar pesas en público es lo más normal del mundo. Eso sí, en los gimnasios cerrados el ritual tiene precio: para usar las máquinas, el juego pide comprar una membresía.",
     mus=("tropical", 1), id="r03", cert="OBSERVADO",
     shots=[S(None, X(THA, 1366.0), z=(1.0, 1.05)), S("en los gimnasios cerrados", X(TOA, 299.0), **TOACAP),
            S("pide comprar", X(TOA, 286.0), **TOACAP)],
     sfx=[("w:membresía", "coin", 0.4)])
beat("Otro ritual nocturno es más ruidoso: las carreras. Los vehículos se alinean bajo los focos, aceleran y desaparecen en la oscuridad.",
     mus=("synthwave", 2), id="r04", cert="OBSERVADO",
     shots=[S(None, X(THA, 1866.0), z=(1.0, 1.05)), S("se alinean", X(THA, 1878.0), z=(1.0, 1.06)), S("aceleran", X(THA, 1896.0), z=(1.0, 1.06))],
     sfx=[("w:aceleran", "whoosh", 0.4)])
beat("También hay costumbres de lujo. En este hotel de la costa, el jugador deja su auto deportivo en la entrada, cruza un vestíbulo iluminado de rosa y sube hasta su habitación.",
     mus=("synthwave", 1), id="r05", cert="OBSERVADO",
     shots=[S(None, X(THA, 1566.0), z=(1.0, 1.05)), S("cruza un vestíbulo", X(THA, 1586.0), z=(1.0, 1.05)), S("y sube", X(THA, 1600.0), z=(1.0, 1.05))])
beat("Y a cualquier hora, algunos ejemplares se refugian en las tiendas de conveniencia, iluminadas toda la noche, donde el tiempo parece no pasar. Nota de campo número dos: aquí el ejercicio se hace en público, y el lujo, en privado.",
     mus=("synthwave", 1), id="r06", cert="OBSERVADO",
     shots=[S(None, X(THA, 2131.0), z=(1.0, 1.05)), S("iluminadas", X(THA, 2146.0), z=(1.0, 1.06))])

# ================================================================ 3 · COMUNICACIÓN
beat("La especie se comunica sobre todo con la voz. Y cuando un desconocido se acerca demasiado, el mensaje es muy claro.",
     chapter=(3, "COMUNICACIÓN"), mus=("nature", 1), pre=1.4, id="c01", cert="OBSERVADO",
     shots=[S(None, X(TOA, 4.0), **TOACAP)])
beat("«No me hables». «Aléjate de mí».",
     mus=("nature", 1), id="c02", cert="OBSERVADO",
     shots=[S(None, X(TOA, 8.0), **TOACAP, say="Don't talk to me."), S("«Aléjate", X(TOA, 12.5), **TOACAP, say="Get away from me.")])
beat("Estas dos habitantes, a la puerta de una barbería, lo dejan claro también con las manos: la conversación ha terminado antes de empezar.",
     mus=("nature", 1), id="c03", cert="OBSERVADO",
     shots=[S(None, X(TOA, 15.0), **TOACAP)])
beat("Si el intruso insiste, el tono sube. «¿Tienes algún problema? ¿Lo tienes?».",
     mus=("nature", 2), id="c04", cert="OBSERVADO",
     shots=[S(None, X(TOA, 104.0), **TOACAP), S("«¿Tienes", X(TOA, 110.0), **TOACAP, say="You got a problem? Do you?")])
beat("Otros prefieren calmar la situación: «Tranquilo, amigo, tranquilo». «Relájate». «No pierdas la calma».",
     mus=("nature", 1), id="c05", cert="OBSERVADO",
     shots=[S(None, X(TOA, 121.0), **TOACAP, say="Easy pal, easy!"), S("«Relájate»", X(TOA, 143.0), **TOACAP, say="Just relax."),
            S("«No pierdas", X(TOA, 152.0), **TOACAP, say="Be cool.")])
beat("Y hay quien marca su territorio con una sola pregunta: «¿Quién te dio permiso para tocarme?».",
     mus=("nature", 2), id="c06", cert="OBSERVADO",
     shots=[S(None, X(TOA, 170.0), **TOACAP), S("«¿Quién te dio", X(TOA, 178.0), **TOACAP, say="Who said you could touch me?")])
beat("Para estos encuentros, el juego le da al jugador un pequeño menú con dos opciones: calmar o provocar. Y debajo aparece una etiqueta en inglés que clasifica a cada ejemplar: turista, o local, si vive aquí. Así que el propio juego distingue dos subespecies.",
     mus=("nature", 1), id="c065", cert="OBSERVADO",
     shots=[S(None, X(THA, 694.0), z=(1.0, 1.04)),
            S("una etiqueta", X(THA, 709.0), card=True, card_zoom=(0.78, 0.80, 1.0, 1.0), zoom_at=0.35),
            S("o local", X(THA, 1265.5), card=True, card_zoom=(0.78, 0.80, 1.0, 1.0), zoom_at=0.3)],
     sfx=[("w:etiqueta", "pop", 0.35), ("w:subespecies", "chime", 0.4)])
beat("Estas frases no salen de la nada. Según declaraciones de Rockstar recogidas por la prensa, el estudio montó en Los Ángeles un equipo de guionistas dedicado solo a lo que dicen los peatones.",
     mus=("nature", 1), id="c07",
     shots=[S(None, "g:quote", q="Nadie con quien te cruzas es un extra.", who="UN RESPONSABLE DE ROCKSTAR · SEGÚN LA PRENSA", tag="ROCKSTAR",
              sub="Rockstar tiene un equipo de guionistas solo para los peatones (Los Ángeles)", sub_at=2.0)],
     sfx=[(0.1, "paper", 0.4)])
beat("Uno de sus responsables lo resumió así: nadie con quien te cruzas es un extra. Y se nota: ante el mismo estímulo, unos se apartan, otros discuten y otros, directamente, ignoran al intruso. Nota de campo número tres: en Vice City, nunca toques a un desconocido.",
     mus=("nature", 1), id="c08", cert="OBSERVADO",
     shots=[S(None, X(TOA, 44.0), **TOACAP), S("unos se apartan", X(TOA, 132.0), **TOACAP), S("otros discuten", X(TOA, 160.0), **TOACAP),
            S("ignoran", X(TOA, 240.0), **TOACAP)])

# ================================================================ 4 · DEPREDADORES
beat("Toda especie tiene depredadores. Y en Vice City, a veces el depredador es el propio habitante. Este ejemplar se acerca al jugador con una exigencia muy concreta.",
     chapter=(4, "DEPREDADORES"), mus=("tension", 1), pre=1.4, id="d01", cert="OBSERVADO",
     shots=[S(None, X(TOA, 18.0), **TOACAP), S("Este ejemplar", X(TOA, 22.0), **TOACAP)],
     sfx=[("w:depredadores", "heartbeat", 0.4)])
beat("Quiere su bolsa. En pantalla aparecen dos opciones: entregársela o negarse. El jugador se niega.",
     mus=("tension", 1), id="d02", cert="OBSERVADO",
     shots=[S(None, X(TOA, 24.0), **TOACAP, say="Give bag / Decline"), S("El jugador se niega", X(TOA, 28.0), **TOACAP)],
     sfx=[("w:negarse", "pop", 0.35)])
beat("Lo que sigue es una pelea en plena acera. Y aquí se ve cómo reacciona el resto de la manada: unos huyen corriendo, alguien grita «¡Que alguien llame a la policía!», y otros protestan: «¿Por qué nosotros?».",
     mus=("tension", 2), id="d03", cert="OBSERVADO",
     shots=[S(None, X(TOA, 31.0), **TOACAP), S("unos huyen", X(TOA, 36.5), **TOACAP), S("alguien grita", X(TOA, 38.5), **TOACAP, say="Someone call the cops!"),
            S("y otros protestan", X(TOA, 41.0), **TOACAP, say="Why us? Why us?")],
     sfx=[("w:pelea", "impact", 0.35)])
beat("Y al final, una súplica: «¡Déjennos en paz!».",
     mus=("tension", 1), id="d04", cert="OBSERVADO",
     shots=[S(None, X(TOA, 43.0), **TOACAP, say="Just let us be!")])
beat("En otra calle, el jugador toca a un desconocido a la puerta de una tienda. La respuesta es inmediata, y escala muy rápido: «Mal movimiento, amigo». «Sé cómo usar esto».",
     mus=("tension", 2), id="d05", cert="OBSERVADO",
     shots=[S(None, X(TOA, 166.0), **TOACAP), S("La respuesta", X(TOA, 184.0), **TOACAP, say="Wrong move, bud."),
            S("«Sé cómo", X(TOA, 190.0), **TOACAP, say="I know how to use this!")],
     sfx=[("w:escala", "impact", 0.35)])
beat("Pero no todos los ejemplares huyen. En la playa, esta turista, provocada por el jugador, no sale corriendo: levanta los puños. Y enseguida, otros bañistas se acercan.",
     mus=("tension", 2), id="d055", cert="OBSERVADO",
     shots=[S(None, X(THA, 719.0), z=(1.0, 1.05)), S("otros bañistas", X(THA, 730.5), z=(1.0, 1.04))],
     sfx=[("w:levanta los puños", "hit", 0.3)])
beat("Y de noche aparece el gran depredador del jugador: la policía. En este estacionamiento, las patrullas llegan con las luces encendidas, y los agentes bajan de inmediato. Para el jugador de esta partida, la noche termina mal.",
     mus=("tension", 2), id="d06", cert="OBSERVADO",
     shots=[S(None, X(THA, 2246.0), z=(1.0, 1.05)), S("las patrullas", X(THA, 2262.0), z=(1.0, 1.06)), S("los agentes", X(THA, 2280.0), z=(1.0, 1.06))],
     sfx=[("w:policía", "alarm", 0.25)])
beat("Moraleja de este capítulo: en este ecosistema, la mayoría de los habitantes no busca problemas. Pero tampoco se deja. Nota de campo número cuatro: quien te pide la bolsa no siempre lleva uniforme.",
     mus=("tension", 1), id="d07", cert="OBSERVADO",
     shots=[S(None, X(TOA, 196.0), **TOACAP)])

# ================================================================ 5 · LA MANADA
beat("Como muchas especies sociales, el habitante de Vice City también reacciona en grupo.",
     chapter=(5, "LA MANADA"), mus=("nature", 2), pre=1.4, id="m01", cert="OBSERVADO",
     shots=[S(None, X(TOA, 368.0), **TOACAP)])
beat("Tras este choque, varios ejemplares se acercan al lugar, rodean a los heridos, y alguno termina enzarzado en una pelea.",
     mus=("nature", 2), id="m02", cert="OBSERVADO",
     shots=[S(None, X(TOA, 378.0), **TOACAP), S("rodean", X(TOA, 412.0), **TOACAP), S("alguno termina", X(TOA, 400.0), **TOACAP)])
beat("Otros se quedan mirando desde cierta distancia, como si calcularan el riesgo antes de acercarse.",
     mus=("nature", 1), id="m03", cert="OBSERVADO",
     shots=[S(None, X(TOA, 436.0), **TOACAP), S("como si calcularan", X(TOA, 446.0), **TOACAP)])
beat("En la recepción de un edificio de oficinas, dos ejemplares se plantan frente al jugador, mientras otra lo observa desde detrás del mostrador.",
     mus=("nature", 1), id="m04", cert="OBSERVADO",
     shots=[S(None, X(TOA, 245.0), **TOACAP), S("dos ejemplares", X(TOA, 248.0), **TOACAP), S("mientras otra", X(TOA, 257.0), **TOACAP)])
beat("Y en la piscina de un edificio de apartamentos, la manada descansa: tumbonas, sombrillas y conversaciones al sol.",
     mus=("tropical", 1), id="m05", cert="OBSERVADO",
     shots=[S(None, X(TOA, 312.0), **TOACAP), S("tumbonas", X(TOA, 316.0), **TOACAP), S("conversaciones", X(TOA, 323.0), **TOACAP)])
beat("Y hay ejemplares que, pase lo que pase, siguen con su rutina. Este repartidor en moto continúa su ruta entre el tráfico, como si nada.",
     mus=("synthpop", 1), id="m06", cert="OBSERVADO",
     shots=[S(None, X(TOA, 458.0), **TOACAP), S("Este repartidor", X(TOA, 468.0), **TOACAP), S("como si nada", X(TOA, 504.0), **TOACAP)])
beat("Se detiene en los semáforos, esquiva taxis y sigue adelante. Probablemente es el animal más trabajador de todo el ecosistema. Mientras la manada pelea, él cumple. Nota de campo número cinco: en caso de accidente, la manada se acerca; en caso de trabajo, el repartidor sigue.",
     mus=("synthpop", 1), id="m07", cert="OBSERVADO",
     shots=[S(None, X(TOA, 478.0), **TOACAP), S("esquiva taxis", X(TOA, 490.0), **TOACAP), S("Probablemente", X(TOA, 516.0), **TOACAP)])

# ================================================================ 6 · OTRAS ESPECIES
beat("Los humanos de Vice City no viven solos. Conviven con otras especies, aunque casi siempre al otro lado de una reja.",
     chapter=(6, "OTRAS ESPECIES"), mus=("nature", 1), pre=1.4, id="e01", cert="OBSERVADO",
     shots=[S(None, X(LAZ, 351.0), **NOCAM), S("al otro lado", X(LAZ, 358.0), **NOCAM)])
beat("En este zoológico hay grandes felinos, un aviario lleno de guacamayos y un oceanario con orcas. La entrada al aviario lo anuncia con un arco: Parrot Paradise, el paraíso de los loros.",
     mus=("nature", 1), id="e02", cert="OBSERVADO",
     shots=[S(None, X(LAZ, 366.0), **NOCAM), S("un aviario", X(LAZ, 423.0), **NOCAM), S("un oceanario", X(LAZ, 437.0), **NOCAM),
            S("La entrada", X(LAZ, 392.5), **NOCAM)])
beat("Dentro, los visitantes pasean entre los pájaros sin prisa. El jugador, en cambio, vuelve a demostrar que es la especie más imprudente del ecosistema: se mete en el recinto de los tigres, y la visita termina en la pantalla de muerte.",
     mus=("nature", 1), id="e03", cert="OBSERVADO",
     shots=[S(None, X(LAZ, 395.0), **NOCAM), S("se mete en el recinto", X(LAZ, 368.5), **NOCAM), S("y la visita termina", X(LAZ, 386.0), **NOCAM)])
beat("Y en el oceanario, se lanza al tanque para nadar junto a las orcas.",
     mus=("nature", 2), id="e04", cert="OBSERVADO",
     shots=[S(None, X(LAZ, 446.0), **NOCAM), S("nadar junto", X(LAZ, 453.0), **NOCAM)],
     sfx=[("w:se lanza", "water", 0.35)])

# ================================================================ 7 · EL OBSERVADOR
beat("Después de tantas horas de observación, hay una conclusión que se repite.",
     chapter=(7, "EL OBSERVADOR"), mus=("nature", 1), pre=1.4, id="o01",
     shots=[S(None, X(THA, 1760.0), z=(1.0, 1.05))])
beat("La especie, en sí, no es especialmente peligrosa. Toma el sol, entrena, trabaja y vuelve a casa. Casi todo el caos que hemos visto empezó igual: alguien con un mando en la mano se acercó demasiado. Si algo enseñan estas partidas es que Vice City no está hecha solo de persecuciones: está hecha de miles de pequeñas rutinas.",
     mus=("nature", 1), id="o02", cert="OBSERVADO",
     shots=[S(None, X(THA, 702.0), z=(1.0, 1.05)), S("entrena", X(THA, 1228.0), z=(1.0, 1.05)), S("trabaja", X(TOA, 528.0), **TOACAP),
            S("Casi todo el caos", X(TOA, 393.0), **TOACAP), S("alguien con un mando", X(TOA, 0.5), **TOACAP)])
beat("Según Rockstar, GTA 6 lleva las interacciones con sus habitantes más lejos que Red Dead Redemption 2. Y después de este documental, cuesta llevarle la contraria.",
     mus=("nature", 1), id="o03",
     shots=[S(None, "g:quote", q="GTA 6 lleva las interacciones con los personajes de su mundo más lejos que Red Dead Redemption 2.", who="SEGÚN ROCKSTAR · DECLARACIONES RECOGIDAS POR LA PRENSA", tag="ROCKSTAR"),
            S("Y después", X(TOA, 140.0), **TOACAP)])
beat("Así que, en este documental, la especie más impredecible no vive en Vice City. Está al otro lado de la pantalla.",
     mus=("nature", 2), id="o04",
     shots=[S(None, X(THA, 1795.0), z=(1.0, 1.05)), S("Está al otro lado", "g:cover", kicker="CONCLUSIÓN DEL ESTUDIO", lines=["LA ESPECIE", "ERES TÚ"])],
     sfx=[("w:Está al otro", "chime", 0.45)])

# ================================================================ CIERRE
beat("¿Y tú? ¿Qué es lo más raro que has visto hacer a un habitante de Vice City? Puede ser una frase, una costumbre o una pelea absurda. Cuéntanoslo en los comentarios, y lo estudiamos en el próximo episodio.",
     mus=("tropical", 1), pre=0.6, id="z01",
     shots=[S(None, X(THA, 940.0), z=(1.0, 1.05)),
            S("Cuéntanoslo", "g:list", title="CUÉNTANOSLO EN LOS COMENTARIOS", items=["Lo más raro que has visto hacer a un habitante"], cues=["Cuéntanoslo"])],
     sfx=[("w:Cuéntanoslo", "pop", 0.4)])
beat("Si te gustó este documental, suscríbete a Sal y Asfalto. Nos vemos en el próximo episodio de Planeta Vice City.",
     mus=("tropical", 1), hold=0.6, id="z02",
     shots=[S(None, X(THA, 1000.0), z=(1.0, 1.05)), S("suscríbete", "g:subscribe")],
     sfx=[("w:suscríbete", "pop", 0.45)])
beat("", dur=20.0, mus=("tropical", 1), id="end", shots=[S(None, "g:end")], trans="fade")

def music_fn(total, beats_tl):
    segs = []
    for b, bd in zip(B, beats_tl):
        st, lv = b.get("mus", ("nature", 1))
        if segs and segs[-1]["style"] == st: segs[-1]["en"].append((bd["start"] - segs[-1]["t0"], lv))
        else: segs.append(dict(style=st, t0=bd["start"], en=[(0.0, lv)]))
    n = int(total * audio.SR); out = np.zeros((n, 2)); xf = 1.2
    for i, sg in enumerate(segs):
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        a0 = max(0.0, sg["t0"] - (xf / 2 if i else 0)); dur = (t1 - a0) + (xf / 2 if i + 1 < len(segs) else 0)
        en = [(max(0.0, tt + (sg["t0"] - a0)), lv) for tt, lv in sg["en"]]
        y = audio.compose(sg["style"], dur, energy=en, seed=7300 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "VIDEO_LARGO_2_PLANETA_VICE_CITY"
for _d in ("trabajo", "trabajo/audio"):
    os.makedirs(os.path.join(_ROOT, FOLDER, _d), exist_ok=True)

VIDEO = dict(id="pv", folder=FOLDER, file="VIDEO_FINAL", res_dir="trabajo", theme="planeta",
             title="Planeta Vice City: el documental de los humanos de GTA 6",
             format="Largo (16:9, 1920×1080, 30 fps) · gameplay real posterior al lanzamiento", music="nature", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55,
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="trabajo/audio/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.thumb_planeta(c)
