"""GTA6_VIDEO_LANZAMIENTO — GTA 6: todo lo que Rockstar ha enseñado antes del lanzamiento (sin spoilers).

Concepto: guía de bienvenida a Leonida montada SOLO con material oficial que Rockstar ofrece para descargar y compartir
(Extended Look, tráiler de lanzamiento, vídeo de precarga, capturas, ilustraciones y vídeos de personajes).
Cada mención concreta del guion lleva su plano oficial, sincronizado con la palabra exacta de la narración.
Reglas: audio oficial silenciado (los tráileres llevan música con licencia); fuente en pantalla en cada plano;
nada de misiones, finales ni filtraciones; el contenido exclusivo de la edición Ultimate va rotulado.

Formato de los planos (shots): S(ancla, fuente, **opciones)
  ancla   = fragmento exacto del texto del beat (el corte cae en esa palabra) o None (inicio del beat)
  fuente  = s:<captura> · u:<Ultimate> · v:<Vintage> · a:<ilustración> · e:<segundo del Extended Look>
            l:<segundo del tráiler de lanzamiento> · p:<segundo del vídeo de precarga> · c:<vídeo de personaje>
            k:cover (portada animada) · g:<gráfico propio>
"""
import numpy as np
import audio
from videos import gl_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)

# ================================================================ GANCHO
beat("Veintiséis minutos de juego, tres tráileres y 138 capturas oficiales. Es todo lo que Rockstar ha enseñado de GTA 6 antes del lanzamiento.",
     section="GANCHO", mus=("synthwave", 2), exag=0.65, pre=0.4, cert=None,
     shots=[S(None, "e:994.6", z=(1.0, 1.12), label="26 MIN"), S("tres tráileres", "g:trailers"), S("138", "g:mosaic"),
            S("Es todo", "e:1133.4", z=(1.0, 1.1)), S("antes del lanzamiento", "k:cover", st=15.6)],
     sfx=[("w:tres", "whoosh", 0.35), ("w:138", "pop", 0.5), ("w:antes del", "whoosh", 0.35)],
     note="Plano aéreo de Vice City (Extended Look) → tres fichas de tráiler → mosaico de las 138 capturas → paracaídas → portada animada.")
beat("Lo hemos revisado todo para contarte, en un solo vídeo, qué te espera en Leonida. Y sin destriparte la historia: aquí no hay misiones, ni finales, ni filtraciones.",
     mus=("synthwave", 2), exag=0.65,
     shots=[S(None, "e:752.4", z=(1.0, 1.1)), S("qué te espera", "a:Vice_City_Postcard_landscape", z=(1.05, 1.15)),
            S("sin destriparte", "s:Jason_and_Lucia_16", z=(1.1, 1.0)), S("ni filtraciones", "g:nospoil")],
     sfx=[("w:sin destriparte", "whoosh", 0.3), ("w:ni filtraciones", "stamp", 0.55)])
beat("", dur=2.4, mus=("synthwave", 1), sfx=[(0.0, "logo", 0.9)], shots=[S(None, "g:sting")], trans="flash")

# ================================================================ INTRO
beat("Estás en Sal y Asfalto. Antes de empezar, dos reglas. La primera: todo lo que vas a ver es material oficial que Rockstar Games ofrece para descargar y compartir, y en cada plano te indicamos de dónde sale. Lo hemos ordenado en diez capítulos, y los tienes en la descripción.",
     section="INTRODUCCIÓN: DOS REGLAS", mus=("synthwave", 1), pre=0.3,
     shots=[S(None, "g:title"), S("dos reglas", "e:1128.4", z=(1.0, 1.08)), S("material oficial", "g:media"),
            S("de dónde sale", "s:Vice_City_02", z=(1.0, 1.06), point_chip=True), S("diez capítulos", "g:chapters")],
     sfx=[("w:dos reglas", "pop", 0.35), ("w:material oficial", "paper", 0.4), ("w:de dónde", "pop", 0.35)])
beat("La segunda: separamos lo oficial de nuestra opinión. En verde, el dato oficial. En amarillo, nuestra interpretación.",
     mus=("synthwave", 1),
     shots=[S(None, "s:Vice_City_27", z=(1.0, 1.08)), S("En verde", "g:legend", step=0), S("En amarillo", "g:legend", step=1)],
     sfx=[("w:En verde", "pop", 0.4), ("w:En amarillo", "pop", 0.4)])

# ================================================================ 1 · LO ESENCIAL
beat("Lo esencial, en treinta segundos. GTA 6 sale el 19 de noviembre de 2026, a medianoche, hora local de cada país. Solo en PlayStation 5 y en Xbox Series X|S.",
     section="1 · LO ESENCIAL", chapter=(1, "LO ESENCIAL"), mus=("electro", 1), pre=0.6, cert="OFICIAL",
     shots=[S(None, "a:Official_Cover_Art_landscape", z=(1.0, 1.08)), S("19 de noviembre", "g:date"),
            S("Solo en", "g:platforms")],
     sfx=[(0.0, "whoosh", 0.4), ("w:19 de", "pop", 0.45), ("w:Solo en", "pop", 0.4)])
beat("Es una aventura para un jugador, en tercera persona, con voces en inglés y textos en español. Y por primera vez en la saga principal, los protagonistas son una pareja: Lucía Caminos y Jason Duval.",
     mus=("electro", 1), cert="OFICIAL",
     shots=[S(None, "e:760.4", z=(1.0, 1.06)), S("tercera persona", "e:1074.4", z=(1.0, 1.06)), S("voces en inglés", "g:lang"),
            S("una pareja", "a:Jason_and_Lucia_Beach_landscape", z=(1.0, 1.1)), S("Lucía Caminos", "c:Lucia_Caminos", card=("LUCÍA CAMINOS", "Protagonista")),
            S("Jason Duval", "c:Jason_Duval", card=("JASON DUVAL", "Protagonista"))])
beat("Dos confirmaciones más, de Rob Nelson, codirector de Rockstar North, en una entrevista: el juego sale sin micropagos con dinero real, y no se ha usado inteligencia artificial generativa para crearlo.",
     mus=("electro", 1), cert="OFICIAL",
     shots=[S(None, "s:Vice_City_26", z=(1.0, 1.08)), S("sin micropagos", "g:claim", step=0), S("inteligencia artificial", "g:claim", step=1)],
     sfx=[("w:sin micropagos", "pop", 0.45), ("w:inteligencia", "pop", 0.45)])
beat("¿Cómo hemos llegado hasta aquí? El primer tráiler se publicó en diciembre de 2023 y batió récords en YouTube. El segundo llegó en mayo de 2025, con setenta capturas nuevas, y sumó 475 millones de visualizaciones en veinticuatro horas, entre todas las plataformas.",
     section="1 · LA CRONOLOGÍA", mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "g:timeline", step=-1), S("diciembre de 2023", "g:timeline", step=0), S("mayo de 2025", "g:timeline", step=1),
            S("475 millones", "g:timeline", step=2)],
     sfx=[("w:diciembre", "tick", 0.5), ("w:mayo", "tick", 0.5), ("w:475", "ding", 0.3)])
beat("En junio de 2026 se presentaron la portada y las ediciones. En agosto, el Extended Look se estrenó en Netflix. En octubre llegó el tráiler de lanzamiento, y el 10 de noviembre empezó la precarga.",
     mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "g:timeline", step=3), S("En agosto", "g:timeline", step=4), S("En octubre", "g:timeline", step=5),
            S("10 de noviembre", "g:timeline", step=6)],
     sfx=[("w:En junio", "tick", 0.5), ("w:En agosto", "tick", 0.5), ("w:En octubre", "tick", 0.5), ("w:10 de", "tick", 0.5)])

# ================================================================ 2 · JASON Y LUCÍA
beat("Empecemos por ella. Según su ficha oficial, a Lucía su padre le enseñó a pelear en cuanto aprendió a caminar. Pelear por su familia la llevó a la Penitenciaría de Leonida, y salió, dice Rockstar, por pura suerte.",
     section="2 · JASON Y LUCÍA", chapter=(2, "JASON Y LUCÍA"), mus=("tension", 1), pre=0.6, cert="OFICIAL",
     shots=[S(None, "a:Jason_and_Lucia_02_landscape", z=(1.0, 1.08)), S("Según su ficha", "s:Lucia_Caminos_01", z=(1.0, 1.1)),
            S("a pelear", "s:Lucia_Caminos_09", z=(1.05, 1.15)), S("Penitenciaría", "s:Lucia_Caminos_05", z=(1.0, 1.1)),
            S("por pura suerte", "c:Lucia_Caminos")],
     sfx=[(0.0, "whoosh", 0.4), ("w:Penitenciaría", "hit", 0.3)])
beat("Ahora quiere la buena vida con la que su madre soñaba desde sus días en Liberty City. Y está dispuesta a conseguirla por su cuenta, cueste lo que cueste. Su frase en la web: lo único que importa es a quién conoces y qué tienes.",
     mus=("tension", 1), cert="OFICIAL",
     shots=[S(None, "s:Lucia_Caminos_02", z=(1.0, 1.08)), S("Liberty City", "s:Lucia_Caminos_10", z=(1.05, 1.12)),
            S("por su cuenta", "s:Lucia_Caminos_08", z=(1.0, 1.08)), S("cueste lo que cueste", "s:Lucia_Caminos_13", z=(1.0, 1.1)),
            S("Su frase", "s:Lucia_Caminos_11", z=(1.0, 1.1), quote="«Lo único que importa es a quién conoces y qué tienes»")])
beat("Jason creció rodeado de estafadores y delincuentes. Pasó por el ejército para dejar atrás una adolescencia complicada, y terminó en los Cayos haciendo lo que mejor sabe: trabajar para traficantes de la zona.",
     mus=("tension", 1), cert="OFICIAL",
     shots=[S(None, "s:Jason_Duval_14", z=(1.0, 1.08)), S("ejército", "s:Jason_Duval_15", z=(1.05, 1.12)),
            S("los Cayos", "s:Jason_Duval_03", z=(1.0, 1.1)), S("trabajar para", "s:Jason_Duval_02", z=(1.0, 1.08))])
beat("Rockstar lo resume así: Jason quiere una vida fácil, pero todo se le complica cada vez más. Su frase: otro día en el paraíso, ¿no?",
     mus=("tension", 1), cert="OFICIAL",
     shots=[S(None, "c:Jason_Duval", card=("JASON DUVAL", "«Quiere una vida fácil»")), S("todo se le complica", "s:Jason_Duval_07", z=(1.0, 1.1)),
            S("Su frase", "s:Jason_Duval_06", z=(1.0, 1.1), quote="«Otro día en el paraíso, ¿no?»")])
beat("¿Y juntos? La premisa oficial dice que un golpe que parecía fácil sale mal, y los deja en el lado más oscuro del lugar más soleado de Estados Unidos, en medio de una conspiración que atraviesa todo el estado de Leonida.",
     mus=("tension", 2), cert="OFICIAL",
     shots=[S(None, "a:Jason_and_Lucia_Motel_landscape", z=(1.0, 1.08)), S("un golpe", "a:Jason_and_Lucia_Robbery_landscape", z=(1.0, 1.08)),
            S("el lado más oscuro", "s:Vice_City_27", z=(1.0, 1.08)), S("más soleado", "s:Vice_City_05", z=(1.0, 1.08)),
            S("una conspiración", "a:Jason_Lucia_Rooftop_landscape", z=(1.0, 1.08))],
     sfx=[("w:sale mal", "hit", 0.3)])
beat("Hasta ahí cuenta Rockstar, y hasta ahí contamos nosotros.",
     mus=("tension", 1), hold=0.3,
     shots=[S(None, "s:Jason_and_Lucia_16", z=(1.0, 1.06), stamp="FIN DE LA PREMISA")],
     sfx=[("w:contamos nosotros", "stamp", 0.5)])
beat("Un detalle jugable importante: según Rockstar, puedes jugar con los dos juntos, solo con Lucía o solo con Jason, y cambiar de uno a otro en plena acción, salvo en ciertos momentos de la historia.",
     mus=("tension", 1), cert="OFICIAL", src_note="Rockstar a la revista Dazed (agosto de 2026)",
     shots=[S(None, "e:1086.6", z=(1.0, 1.08)), S("solo con Lucía", "e:1074.4", z=(1.0, 1.06)), S("solo con Jason", "e:1034.4", z=(1.0, 1.06)),
            S("cambiar de uno a otro", "g:swap"), S("ciertos momentos", "s:Jason_and_Lucia_06", z=(1.0, 1.08))],
     sfx=[("w:cambiar de", "whoosh", 0.4)])
beat("Pausa rápida: si tuvieras que elegir a uno, ¿Jason o Lucía? Déjalo en los comentarios, y seguimos.",
     mus=("tension", 1), cert=None, hold=0.3,
     shots=[S(None, "g:poll"), S("Déjalo en los comentarios", "s:Jason_and_Lucia_03", z=(1.0, 1.08))], sfx=[("w:¿Jason", "pop", 0.4), ("w:Lucía?", "pop", 0.4)])

# ================================================================ 3 · EL REPARTO
beat("Ahora, el reparto que Rockstar ya ha presentado. Cal Hampton es amigo de Jason, y donde más seguro se siente es en casa, espiando las comunicaciones de la Guardia Costera con unas cervezas. Su lema: ¿y si todo lo que dice internet fuera verdad?",
     section="3 · EL REPARTO", chapter=(3, "EL REPARTO"), mus=("trap26", 1), pre=0.6, cert="OFICIAL",
     shots=[S(None, "g:cast"), S("Cal Hampton", "c:Cal_Hampton", card=("CAL HAMPTON", "Amigo de Jason")),
            S("en casa", "s:Cal_Hampton_04", z=(1.0, 1.08)), S("Guardia Costera", "a:Cal_Hampton_landscape", z=(1.0, 1.08)),
            S("Su lema", "s:Cal_Hampton_03", z=(1.0, 1.1), quote="«¿Y si todo lo que dice internet fuera verdad?»")],
     sfx=[(0.0, "whoosh", 0.4), ("w:Cal Hampton", "pop", 0.35)])
beat("Boobie Ike es una leyenda local de Vice City. Pasó de la calle a un imperio legal de inmuebles, un club y un estudio de grabación.",
     mus=("trap26", 1), cert="OFICIAL",
     shots=[S(None, "c:Boobie_Ike", card=("BOOBIE IKE", "Leyenda local de Vice City")), S("un imperio", "s:Boobie_Ike_01", z=(1.0, 1.08)),
            S("un club", "s:Boobie_Ike_02", z=(1.0, 1.08)), S("estudio de grabación", "s:DreQuan_Priest_04", z=(1.0, 1.08))],
     sfx=[("w:Boobie", "pop", 0.35)])
beat("Su gran apuesta es el sello Only Raw Records, junto a Dre'Quan Priest, que siempre fue más buscavidas que gánster y que solo quería entrar en la música.",
     mus=("trap26", 1), cert="OFICIAL",
     shots=[S(None, "a:Boobie_Ike_landscape", z=(1.0, 1.08)), S("Dre'Quan Priest", "c:DreQuan_Priest", card=("DRE'QUAN PRIEST", "Only Raw Records")),
            S("buscavidas", "s:DreQuan_Priest_02", z=(1.0, 1.08)), S("la música", "s:DreQuan_Priest_03", z=(1.0, 1.08))],
     sfx=[("w:Dre'Quan", "pop", 0.35)])
beat("Su fichaje estrella es Real Dimez: Bae-Luxe y Roxy, amigas desde la escuela, que convirtieron sus temas de rap picantes y su presencia en redes en dinero. Ya tuvieron un primer éxito, y ahora buscan el segundo. Su lema: vídeos virales, estribillos virales.",
     mus=("trap26", 2), cert="OFICIAL",
     shots=[S(None, "c:Real_Dimez", card=("REAL DIMEZ", "Bae-Luxe y Roxy")), S("Bae-Luxe", "s:Real_Dimez_04", z=(1.0, 1.08)),
            S("presencia en redes", "s:Real_Dimez_02", z=(1.0, 1.08)), S("primer éxito", "s:Real_Dimez_03", z=(1.0, 1.08)),
            S("buscan el segundo", "a:Real_Dimez_landscape", z=(1.0, 1.08)),
            S("Su lema", "s:Real_Dimez_01", z=(1.0, 1.1), quote="«Vídeos virales. Estribillos virales.»")],
     sfx=[("w:Real Dimez", "pop", 0.35)])
beat("Raúl Bautista es un atracador de bancos veterano, siempre a la caza de talento dispuesto a arriesgarse. Su lema: la experiencia cuenta.",
     mus=("trap26", 1), cert="OFICIAL",
     shots=[S(None, "c:Raul_Bautista", card=("RAÚL BAUTISTA", "Atracador de bancos")), S("a la caza", "s:Raul_Bautista_03", z=(1.0, 1.08)),
            S("Su lema", "s:Raul_Bautista_02", z=(1.0, 1.1), quote="«La experiencia cuenta»")],
     sfx=[("w:Raúl", "pop", 0.35)])
beat("Y Brian Heder, contrabandista de la vieja escuela de los Cayos, deja vivir a Jason sin pagar alquiler en una de sus casas, a cambio de que le eche una mano con algunas extorsiones... y de que se pase de vez en cuando a probar la sangría de Lori, su tercera esposa.",
     mus=("trap26", 1), cert="OFICIAL",
     shots=[S(None, "c:Brian_Heder", card=("BRIAN HEDER", "Contrabandista de los Cayos")), S("vieja escuela", "s:Brian_Heder_02", z=(1.0, 1.08)),
            S("sin pagar alquiler", "a:Brian_Heder_landscape", z=(1.0, 1.08)), S("extorsiones", "s:Brian_Heder_04", z=(1.0, 1.08)),
            S("la sangría", "s:Brian_Heder_03", z=(1.0, 1.1))],
     sfx=[("w:Brian", "pop", 0.35)])

# ================================================================ 4 · LEONIDA
beat("Todo esto pasa en Leonida, el estado inspirado en Florida. En el material oficial aparecen seis zonas, y cada una tiene hasta su propia postal de recuerdo.",
     section="4 · LEONIDA, EL MAPA", chapter=(4, "LEONIDA"), mus=("tropical", 1), pre=0.6, cert="OFICIAL",
     shots=[S(None, "e:1142.0", z=(1.0, 1.1)), S("inspirado en Florida", "g:map"), S("seis zonas", "g:postcards"),
            S("postal de recuerdo", "a:Vice_City_Postcard_landscape", z=(1.0, 1.12))],
     sfx=[(0.0, "whoosh", 0.4), ("w:seis zonas", "paper", 0.5)])
beat("Vice City es el corazón: rascacielos, playas, puertos deportivos y neón. Rockstar la presenta con una frase: cuando el sol se apaga y se encienden los neones, todos tienen algo que ganar... y más que perder.",
     mus=("tropical", 1), cert="OFICIAL",
     shots=[S(None, "s:Vice_City_10", z=(1.0, 1.08), region="VICE CITY"), S("playas", "s:Vice_City_05", z=(1.0, 1.08)),
            S("puertos deportivos", "s:Vice_City_15", z=(1.0, 1.08)), S("neón", "s:Vice_City_22", z=(1.0, 1.08)),
            S("Rockstar la presenta", "s:Vice_City_01", z=(1.0, 1.1)), S("cuando el sol", "e:1570.4", z=(1.0, 1.06)), S("todos tienen algo", "s:Vice_City_25", z=(1.0, 1.08)),
            S("más que perder", "s:Vice_City_17", z=(1.0, 1.08))])
beat("Luego están los Cayos de Leonida: islas unidas por puentes sobre el mar, hidroaviones, arrecifes para bucear y bares de playa.",
     mus=("tropical", 1), cert="OFICIAL",
     shots=[S(None, "a:Leonida_Keys_Postcard_landscape", z=(1.0, 1.1), region="LEONIDA KEYS"), S("islas", "s:Leonida_Keys_01", z=(1.0, 1.08)),
            S("hidroaviones", "s:Leonida_Keys_01", z=(1.6, 1.75), f=(0.62, 0.62)), S("arrecifes", "s:Leonida_Keys_04", z=(1.0, 1.08)),
            S("bares de playa", "s:Leonida_Keys_03", z=(1.0, 1.08))])
beat("Grassrivers es el pantano: hierba alta, aerobotes y caimanes. Es la versión de Leonida de los Everglades.",
     mus=("tropical", 1), cert="OFICIAL",
     shots=[S(None, "a:Grassrivers_Postcard_landscape", z=(1.0, 1.1), region="GRASSRIVERS"), S("hierba alta", "s:Grassrivers_05", z=(1.0, 1.08)),
            S("aerobotes", "s:Grassrivers_03", z=(1.0, 1.1)), S("caimanes", "s:Grassrivers_08", z=(1.0, 1.1)),
            S("Everglades", "s:Grassrivers_04", z=(1.0, 1.08))])
beat("Port Gellhorn es la Leonida de carretera: moteles, neones gastados y atardeceres naranjas.",
     mus=("tropical", 1), cert="OFICIAL",
     shots=[S(None, "a:Port_Gellhorn_Postcard_landscape", z=(1.0, 1.1), region="PORT GELLHORN"), S("moteles", "s:Port_Gellhorn_01", z=(1.0, 1.08)),
            S("neones gastados", "s:Port_Gellhorn_01", z=(1.7, 1.85), f=(0.2, 0.3)), S("atardeceres", "s:Port_Gellhorn_06", z=(1.0, 1.08))])
beat("Ambrosia es el interior industrial, con refinerías, tendidos eléctricos y bandas de moteros.",
     mus=("tropical", 1), cert="OFICIAL",
     shots=[S(None, "a:Ambrosia_Postcard_landscape", z=(1.0, 1.1), region="AMBROSIA"), S("refinerías", "s:Ambrosia_02", z=(1.0, 1.08)),
            S("tendidos eléctricos", "s:Ambrosia_04", z=(1.0, 1.08)), S("moteros", "s:Ambrosia_01", z=(1.0, 1.08))])
beat("Y Mount Kalaga es el parque nacional: bosques, ríos, cañones, motos de montaña y kayak.",
     mus=("tropical", 2), cert="OFICIAL",
     shots=[S(None, "a:Mount_Kalaga_National_Park_Postcard_landscape", z=(1.0, 1.1), region="MOUNT KALAGA"),
            S("bosques", "s:Mount_Kalaga_National_Park_03", z=(1.0, 1.08)), S("cañones", "s:Mount_Kalaga_National_Park_04", z=(1.0, 1.08)),
            S("motos de montaña", "s:Mount_Kalaga_National_Park_01", z=(1.0, 1.08)), S("kayak", "s:Mount_Kalaga_National_Park_06", z=(1.0, 1.08))])
beat("Nuestra lectura: no es una ciudad con un poco de campo alrededor. Es un estado entero, y cada zona tiene su propio carácter.",
     mus=("tropical", 1), cert="INTERPRETACIÓN",
     shots=[S(None, "e:1116.2", z=(1.0, 1.06)), S("Es un estado entero", "g:postcards", step=1)])

# ================================================================ 5 · UN DÍA EN VICE CITY
beat("Ahora, lo que más nos ha sorprendido del Extended Look, el vídeo de veintiséis minutos que Rockstar estrenó en agosto. Por cierto: el día del estreno, la demanda fue tal que Netflix y Twitch tuvieron problemas técnicos.",
     section="5 · UN DÍA EN VICE CITY", chapter=(5, "UN DÍA EN VICE CITY"), mus=("synthpop", 1), pre=0.6, cert="OFICIAL",
     shots=[S(None, "e:1208.4", z=(1.0, 1.04)), S("Extended Look", "g:el_card"), S("Por cierto", "e:380.2", z=(1.0, 1.08)),
            S("Netflix y Twitch", "g:el_card", step=1)],
     sfx=[(0.0, "whoosh", 0.4), ("w:Por cierto", "pop", 0.35)])
beat("Y lo que más nos ha sorprendido no son las persecuciones. Es la vida cotidiana. Hay un tramo en el que seguimos a Jason por un apartamento.",
     mus=("synthpop", 1), cert="INTERPRETACIÓN",
     shots=[S(None, "e:776.4", z=(1.0, 1.06)), S("la vida cotidiana", "e:432.0", z=(1.0, 1.06)), S("seguimos a Jason", "e:426.4", z=(1.0, 1.05))])
beat("Pasa junto a un espejo lleno de bombillas, abre la nevera, y en la tele echan dibujos animados, un documental de naturaleza y hasta un anuncio de hamburguesas.",
     mus=("synthpop", 1), cert="OFICIAL",
     shots=[S(None, "e:422.6"), S("abre la nevera", "e:437.6"), S("dibujos animados", "e:445.6"), S("documental", "e:458.0"),
            S("de naturaleza", "e:465.6"), S("hamburguesas", "e:470.2")],
     sfx=[("w:nevera", "pop", 0.3), ("w:hamburguesas", "pop", 0.35)])
beat("Después sale a la calle, se sube a un descapotable rojo y cruza la ciudad entre tráfico y peatones, hasta un puente con los rascacielos al fondo.",
     mus=("synthpop", 2), cert="OFICIAL",
     shots=[S(None, "e:484.2"), S("descapotable rojo", "e:490.0"), S("cruza la ciudad", "e:509.0"), S("peatones", "e:521.0"),
            S("un puente", "e:535.6")])
beat("Fíjate en el minimapa de la esquina: esto es juego, no una cinemática.",
     mus=("synthpop", 2), cert="INTERPRETACIÓN",
     shots=[S(None, "e:513.0", z=(1.0, 1.0), ring=(0.075, 0.905, 0.07)), S("esto es juego", "e:527.0")])
beat("Y la ciudad no se detiene. Vecinos charlando frente a un motel, un combate de lucha libre en el patio de una casa, una azotea llena de gente.",
     mus=("synthpop", 2), cert="OFICIAL",
     shots=[S(None, "e:1028.2", z=(1.0, 1.08)), S("Vecinos", "e:554.6"), S("lucha libre", "e:565.2"), S("una azotea", "e:571.2", z=(1.0, 1.06))])
beat("Cuando cae la noche, Vice City cambia de piel: calles de neón, clubes, carreras callejeras y piscinas en lo alto de los rascacielos.",
     mus=("trap26", 2), cert="OFICIAL",
     shots=[S(None, "e:1546.2", z=(1.0, 1.06)), S("cambia de piel", "e:1214.2", z=(1.0, 1.08)), S("calles de neón", "p:18.7"), S("clubes", "e:1226.2"),
            S("carreras callejeras", "e:1222.4"), S("piscinas", "e:1548.6", z=(1.0, 1.06))],
     sfx=[("w:Cuando cae", "whoosh", 0.35)])

# ================================================================ 6 · QUÉ PUEDES HACER
beat("¿Y qué se puede hacer cuando no estás en una misión? Esto es lo que se ve en el material oficial.",
     section="6 · QUÉ PUEDES HACER", chapter=(6, "QUÉ PUEDES HACER"), mus=("electro", 2), pre=0.6, cert="OFICIAL",
     shots=[S(None, "e:1108.6", z=(1.0, 1.08)), S("Esto es lo que", "e:1045.0", z=(1.0, 1.06))], sfx=[(0.0, "whoosh", 0.4)])
beat("Jugar al baloncesto en una cancha de barrio. Entrenar en el gimnasio, con press de banca y pesas. Correr en un circuito, con vueltas y cronómetro.",
     mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "e:1033.2", label="BALONCESTO"), S("Entrenar", "e:1039.2", label="GIMNASIO"), S("pesas", "s:Jason_Duval_15", z=(1.0, 1.08)),
            S("Correr en un circuito", "e:1062.4", label="CARRERAS"), S("cronómetro", "e:1064.4", z=(1.9, 2.0), f=(0.9, 0.86))])
beat("Subir a lo más alto de un rascacielos... y lanzarte en paracaídas sobre Vice City.",
     mus=("electro", 3), cert="OFICIAL",
     shots=[S(None, "e:1128.0", label="SALTO BASE"), S("lanzarte", "e:1129.6"), S("paracaídas", "e:1133.3", label="PARACAÍDAS")],
     sfx=[("w:paracaídas", "whoosh", 0.5)], hold=0.6)
beat("Tumbarte en la playa bajo una sombrilla. Pescar desde un barco. Bucear entre peces. Remar en kayak.",
     mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "e:1108.6", label="PLAYA"), S("Pescar", "s:Jason_Duval_03", z=(1.0, 1.1), label="PESCA"),
            S("Bucear", "e:1036.6", label="BUCEO"), S("Remar", "e:1049.2", label="KAYAK")])
beat("Y en las capturas aparecen más planes: una partida de billar, un minigolf con un caimán gigante de adorno y una quedada de coches tuneados.",
     mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "s:Vice_City_03", z=(1.0, 1.08)), S("billar", "s:Cal_Hampton_02", z=(1.0, 1.08), label="BILLAR"),
            S("minigolf", "s:Cal_Hampton_01", z=(1.0, 1.08), label="MINIGOLF"), S("coches tuneados", "s:Vice_City_24", z=(1.0, 1.08), label="QUEDADAS")])
beat("O, simplemente, salir a dar una vuelta en moto o en descapotable, sin rumbo, de día o de noche.",
     mus=("electro", 2), cert="OFICIAL",
     shots=[S(None, "e:1086.6"), S("descapotable", "e:528.0"), S("de noche", "e:1124.0")])

# ================================================================ 7 · CÓMO SE JUEGA
beat("Las mecánicas que Rockstar ha explicado en entrevistas. La comida afecta al peso de los personajes, el ejercicio se nota en los músculos, y si no duermen... se les nota en la cara.",
     section="7 · CÓMO SE JUEGA", chapter=(7, "CÓMO SE JUEGA"), mus=("synthwave", 1), pre=0.6, cert="OFICIAL", src_note="Rockstar a la revista Dazed (agosto de 2026)",
     shots=[S(None, "e:1144.6", z=(1.0, 1.08)), S("La comida", "e:544.6", z=(1.0, 1.06)),
            S("el ejercicio", "s:Lucia_Caminos_09", z=(1.0, 1.08)), S("se les nota en la cara", "s:Jason_Duval_19", z=(1.1, 1.25), f=(0.62, 0.4))],
     sfx=[(0.0, "whoosh", 0.4)])
beat("Vuelve Snapmatic, la red social del juego, como parodia de las redes de hoy. Y puedes cambiar el peinado, la ropa y los accesorios de Jason y de Lucía.",
     mus=("synthwave", 1), cert="OFICIAL", src_note="Rockstar a la revista Dazed y Extended Look",
     shots=[S(None, "s:Real_Dimez_02", z=(1.0, 1.08)), S("parodia", "e:1104.6", z=(1.0, 1.04)),
            S("el peinado", "s:Lucia_Caminos_06", z=(1.0, 1.08)), S("la ropa", "s:Lucia_Caminos_03", z=(1.0, 1.08)),
            S("los accesorios", "s:Jason_Duval_04", z=(1.0, 1.08))])
beat("Rockstar también ha hablado de un perfil criminal, que tiene en cuenta cómo cometes tus delitos: si actúas como un profesional o si te pasas de violento.",
     mus=("synthwave", 1), cert="OFICIAL", src_note="Rob Nelson (Rockstar North) a la revista Edge",
     shots=[S(None, "a:Jason_Lucia_Lock_And_Load_landscape", z=(1.0, 1.08)), S("cómo cometes", "g:profile", step=0),
            S("si te pasas", "g:profile", step=1)])
beat("Y en el Extended Look se ven detalles de la interfaz: el aviso para forzar la cerradura de un coche o romper la ventanilla, y el minimapa con la ruta marcada.",
     mus=("synthwave", 1), cert="OFICIAL",
     shots=[S(None, "e:1062.4"), S("forzar la cerradura", "e:365.4", z=(1.25, 1.35), f=(0.55, 0.62)), S("romper la ventanilla", "e:367.0"),
            S("el minimapa", "e:509.0", z=(2.2, 2.3), f=(0.0, 1.0))])

# ================================================================ 8 · VEHÍCULOS Y FAUNA
beat("Vehículos vistos hasta ahora: deportivos, descapotables, motos, lanchas, aerobotes, hidroaviones, helicópteros... y hasta una avioneta que suelta humo rosa sobre la playa.",
     section="8 · VEHÍCULOS Y FAUNA", chapter=(8, "VEHÍCULOS Y FAUNA"), mus=("tropical", 2), pre=0.6, cert="OFICIAL",
     shots=[S(None, "e:1566.0", z=(1.0, 1.06)), S("deportivos", "s:Jason_and_Lucia_11", z=(1.0, 1.08)), S("descapotables", "e:515.0"),
            S("motos", "l:50.0"), S("lanchas", "s:Leonida_Keys_05", z=(1.0, 1.08)),
            S("aerobotes", "e:1030.4"), S("hidroaviones", "e:1567.35"),
            S("helicópteros", "s:Mount_Kalaga_National_Park_02", z=(1.0, 1.08)), S("una avioneta", "l:55.6", z=(1.0, 1.04))],
     sfx=[(0.0, "whoosh", 0.4)])
beat("Y la fauna: caimanes, iguanas, ciervos y peces de arrecife. En Leonida, los animales también forman parte del paisaje.",
     mus=("nature", 1), cert="OFICIAL",
     shots=[S(None, "s:Grassrivers_08", z=(1.05, 1.15)), S("iguanas", "l:21.5"), S("ciervos", "s:Mount_Kalaga_National_Park_05", z=(1.0, 1.08)),
            S("peces de arrecife", "s:Leonida_Keys_07", z=(1.1, 1.2)), S("forman parte del paisaje", "s:Leonida_Keys_06", z=(1.0, 1.1))])

# ================================================================ 9 · EDICIONES
beat("Las ediciones. La edición Ultimate añade ropa, peinados, tatuajes, vehículos, armas, lugares y misiones extra.",
     section="9 · EDICIONES", chapter=(9, "EDICIONES"), mus=("synthpop", 1), pre=0.6, cert="ULTIMATE",
     shots=[S(None, "u:ULTIMATE_EDITION_01", z=(1.0, 1.08)), S("ropa", "u:ULTIMATE_EDITION_VICE_CITY_STYLE_01", z=(1.0, 1.08)),
            S("peinados", "u:ULTIMATE_EDITION_SARAS_SALON_02", z=(1.0, 1.08)), S("tatuajes", "u:ULTIMATE_EDITION_ELECTRIC_FANG_04", z=(1.0, 1.08)),
            S("vehículos", "u:ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_01", z=(1.0, 1.08)), S("armas", "u:ULTIMATE_EDITION_HAWK_AND_LITTLE_MORGAN_REVOLVERS_02", z=(1.0, 1.08)),
            S("lugares", "u:ULTIMATE_EDITION_SAFEHOUSE_VEHICLES_01", z=(1.0, 1.08)), S("misiones", "u:ULTIMATE_EDITION_ONE_EYED_WILLIE_03", z=(1.0, 1.08))],
     sfx=[(0.0, "whoosh", 0.4)])
beat("Por ejemplo: el estudio de tatuajes Electric Fang, la peluquería de Sara, la tienda Stock 305, el deportivo Grotti Cheetah o la lancha Squalo. Ojo: todo eso es exclusivo de la edición Ultimate. No viene en la estándar.",
     mus=("synthpop", 1), cert="ULTIMATE",
     shots=[S(None, "u:ULTIMATE_EDITION_ELECTRIC_FANG_01", z=(1.0, 1.08)), S("peluquería de Sara", "u:ULTIMATE_EDITION_SARAS_SALON_03", z=(1.0, 1.08)),
            S("Stock 305", "u:ULTIMATE_EDITION_STOCK_305_03", z=(1.0, 1.08)), S("Grotti Cheetah", "u:ULTIMATE_EDITION_GROTTI_CHEETAH_01", z=(1.0, 1.08)),
            S("Squalo", "u:ULTIMATE_EDITION_SQUALO_01", z=(1.0, 1.08)), S("Ojo", "g:editions")],
     sfx=[("w:Ojo", "hit", 0.35)])
beat("Y quien reservó el juego recibe el paquete Vintage Vice City: ropa, un Vapid Stanier y diseños de armas inspirados en el Vice City de 2002.",
     mus=("synthpop", 1), cert="RESERVA",
     shots=[S(None, "v:VINTAGE_VICE_CITY_PACK_01", z=(1.0, 1.08)), S("ropa", "v:VINTAGE_VICE_CITY_PACK_EXCLUSIVE_LOOKS_04", z=(1.0, 1.08)),
            S("Vapid Stanier", "v:VINTAGE_VICE_CITY_PACK_VAPID_STANIER_01", z=(1.0, 1.08)), S("diseños de armas", "v:VINTAGE_VICE_CITY_WEAPON_PATTERN_01", z=(1.0, 1.08)),
            S("2002", "v:VINTAGE_VICE_CITY_PACK_02", z=(1.0, 1.08))])
beat("Nuestra opinión: es mucho contenido reservado a la edición cara, y entendemos a quien lo critica. Conviene saberlo antes de pagar, no después.",
     mus=("synthpop", 1), cert="INTERPRETACIÓN",
     shots=[S(None, "u:ULTIMATE_EDITION_GROTTI_CHEETAH_02", z=(1.0, 1.08)), S("entendemos", "u:ULTIMATE_EDITION_RIDEOUT_CUSTOMS_01", z=(1.0, 1.08)), S("Conviene saberlo", "g:editions", step=1)])

# ================================================================ 10 · MÚSICA
beat("La música. Rockstar anunció un álbum oficial con treinta y cuatro canciones originales, además de las emisoras de radio del juego. Aquí no suena ninguna: el audio oficial va silenciado, y toda la música de este vídeo es original de Sal y Asfalto.",
     section="10 · LA MÚSICA", chapter=(10, "LA MÚSICA"), mus=("seventies", 1), pre=0.6, cert="OFICIAL",
     shots=[S(None, "a:The_Album_Cover_Art_landscape", z=(1.0, 1.08)), S("treinta y cuatro", "a:The_Album_Cover_Art_landscape", z=(1.2, 1.3), f=(0.5, 0.35), label="34 CANCIONES ORIGINALES"),
            S("emisoras de radio", "e:518.0"), S("Aquí no suena ninguna", "g:mute"), S("toda la música", "g:mute", step=1)],
     sfx=[(0.0, "tune", 0.45)])

# ================================================================ LO QUE FALTA
beat("Y lo que Rockstar todavía no ha enseñado: el modo online. Cuando se lo preguntaron en aquella entrevista, prefirió no hablar de él. Y, de momento, no hay versión anunciada para PC.",
     section="LO QUE FALTA POR SABER", mus=("mystery", 1), pre=0.5, cert="OFICIAL",
     shots=[S(None, "s:Vice_City_08", z=(1.0, 1.1)), S("el modo online", "g:unknown", step=0), S("versión anunciada para PC", "g:unknown", step=1)],
     sfx=[("w:el modo online", "pop", 0.4), ("w:para PC", "pop", 0.4)])

# ================================================================ CIERRE
beat("Y eso es todo lo que Rockstar ha enseñado. Lo que no te vamos a contar es la historia: esa te toca descubrirla a ti, mando en mano.",
     section="CIERRE", mus=("synthwave", 2), pre=0.5, cert=None,
     shots=[S(None, "k:cover", st=15.6), S("Lo que no te vamos", "s:Vice_City_27", z=(1.0, 1.08)), S("la historia", "a:Jason_and_Lucia_Beach_landscape", z=(1.0, 1.1)),
            S("mando en mano", "s:Vice_City_11", z=(1.0, 1.08))])
beat("Cuéntanos en los comentarios qué es lo primero que vas a hacer en Leonida: ¿baloncesto, paracaídas o pescar en los Cayos? Y si este vídeo te ha servido, suscríbete a Sal y Asfalto. Seguimos toda la semana, siempre sin spoilers.",
     mus=("synthwave", 2), hold=0.4,
     shots=[S(None, "e:1128.0", z=(1.0, 1.06)), S("baloncesto", "e:1033.6"), S("paracaídas", "e:1134.6"), S("pescar en los Cayos", "s:Jason_Duval_03", z=(1.1, 1.2)),
            S("suscríbete", "g:subscribe")],
     sfx=[("w:suscríbete", "pop", 0.45)])
beat("", dur=20.0, mus=("synthwave", 1), shots=[S(None, "g:end")], trans="fade")

# ---------------------------------------------------------------- música original por capítulo
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
        y = audio.compose(sg["style"], dur, energy=en, seed=2600 + 13 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

VIDEO = dict(id="gl", folder="GTA6_VIDEO_LANZAMIENTO", file="VIDEO_FINAL",
             title="GTA 6: todo lo que Rockstar ha enseñado antes del lanzamiento (sin spoilers)",
             format="Largo (16:9) · guía con material oficial", music="synthwave", music_fn=music_fn, voice="host", beats=B,
             overlay=R.overlay, grade=None, music_gain=0.42, max_tries=5, qa_metric="fonetica", qa_thr=0.995, trans=("cut", 0.0),
             final_codec="av1", target_mb=94, av1_preset=8,
             names=dict(narr_wav="recursos/narracion_original.flac", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="recursos/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.thumbnail(c)
