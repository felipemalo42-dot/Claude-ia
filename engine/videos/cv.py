"""VIDEO_LARGO_4 — «GTA 5 vs GTA 6: 8 asaltos con partidas reales»

Formato: un combate por asaltos. En cada asalto, la MISMA situación en los dos juegos, con partidas reales de cada uno,
y un resultado razonado (incluidos asaltos que gana GTA 5 y empates). No se comparan gráficos: el material de GTA 5 viene
de versiones distintas (2013 en consola y la edición mejorada de PC), y así se dice en el vídeo.

Fuentes de imagen (créditos en pantalla y en la descripción):
- GTA 5: Kotaku «How To Get A Tank And Fighter Jet In GTA 5» (2013) · The Escapist «How to steal a fighter jet in GTA V»
  (2013) · LOCAL GAMING «GTA 5: Enhanced in RTX 5090 - Franklin & Chop» (2025, 4K)
- GTA 6: Sirloin «The Military Base in GTA 6 - First Look» · GameV (tanque y seis estrellas) · guías de IGN (caza, casa)
  · Video Pump (factura del hospital) · toaster (habitantes) · Yamatum O (Vice City, menú turista/local)
Datos: GTA Wiki (factura del hospital en GTA 5, hasta 5000 $ según el dinero que lleves) · Rockstar 2022 (modo de 60
imágenes por segundo de GTA 5 en PS5 y Xbox Series) · Rockstar vía TweakTown (GTA 6 a 30) · guías de Kotaku y The Escapist
(transcritas) · PC Gamer (seis estrellas) · Rockstar vía GamesRadar (interacciones más allá de Red Dead Redemption 2).
Sin spoilers de la historia de GTA 6.
"""
import os
import numpy as np
import audio
from videos import dc_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def X(vid, t): return f"x:{vid}@{t}"

K5 = "IG2hfrBVjh4"    # Kotaku (2013) · GTA 5: Fort Zancudo, tanque Rhino y caza
E5 = "Q5XgKNEnbP4"    # The Escapist (2013) · GTA 5: robar un caza (de noche, «wasted», Vinewood)
L5 = "V99Ng_VTBUs"    # LOCAL GAMING (2025) · GTA 5 Enhanced 4K: Los Santos, el barrio de Franklin, el centro
B6 = "nqmpDCbz3lA"    # Sirloin · GTA 6: la base militar (llegada, valla, blindado)
TAN = "-UuHA1h-Cf8"   # GameV · GTA 6: tanque contra seis estrellas
JET = "4HCd052lpnA"   # IGN · GTA 6: robar un caza en el capítulo 1
CAS = "3UiRmXUIE9k"   # IGN · GTA 6: la casa (corazón de la relación, basura y Focus)
HOS = "vpHospital1"   # Video Pump · GTA 6: la factura del hospital
TOA = "cEDUO1zjB5c"   # toaster · GTA 6: encuentros con los habitantes (4K, subtítulos incrustados abajo)
THA = "gvlY1gVmSKM"   # Yamatum O · GTA 6: Vice City, playa, menú turista/local, gimnasio
TOACAP = dict(z=(1.40, 1.44), f=(0.5, 0.0))
V5 = dict(prueba="GTA V", lado="gta5")
V6 = dict(prueba="GTA VI", lado="gta6")

# ================================================================ APERTURA
beat("Trece años separan a GTA 5 de GTA 6. Y la pregunta que todo el mundo se hace es la misma: ¿de verdad ha cambiado tanto? Para responderla, hemos puesto a los dos juegos frente a frente, en las mismas situaciones, con partidas reales. Ocho asaltos. Y al final, el marcador.",
     mus=("synthwave", 2), pre=0.3, id="o01",
     shots=[S(None, X(L5, 5.0), z=(1.0, 1.05), **V5), S("de GTA 6", X(THA, 212.0), z=(1.0, 1.05), **V6),
            S("frente a frente", X(K5, 52.0), z=(1.0, 1.05), **V5), S("con partidas reales", X(TAN, 150.0), z=(1.0, 1.05), **V6),
            S("Ocho asaltos", "g:cover", kicker="SAL Y ASFALTO PRESENTA", lines=["GTA 5", "VS GTA 6"], sub="Ocho asaltos con partidas reales")],
     sfx=[(0.0, "riser", 0.35), ("w:Ocho asaltos", "stamp", 0.5)])
beat("Las reglas del combate. Todas las imágenes son partidas reales de jugadores y medios, con su crédito en pantalla. Las de GTA 5 vienen de versiones distintas, de dos mil trece y de la edición mejorada para PC, así que aquí no vamos a comparar gráficos: vamos a comparar lo que puedes hacer. Y no hay spoilers de la historia de GTA 6.",
     mus=("synthwave", 1), pre=0.4, id="o02",
     shots=[S(None, "g:creators", title="LAS REGLAS", subt="Partidas reales de los dos juegos · créditos en pantalla",
              rows=[("GTA 5", "Kotaku y The Escapist (2013) · LOCAL GAMING (PC)"), ("GTA 6", "GameV, IGN, Sirloin, toaster, Yamatum O, Video Pump"),
                    ("Sin spoilers", "Solo cosas que puedes hacer por tu cuenta")],
              foot="No comparamos gráficos: las versiones de GTA 5 son distintas"),
            S("no vamos a comparar", X(L5, 150.0), z=(1.0, 1.05), **V5)],
     sfx=[(0.1, "paper", 0.4)])
beat("En la esquina izquierda, el veterano: Grand Theft Auto 5, publicado en dos mil trece, con Los Santos como escenario. En la esquina derecha, el aspirante: Grand Theft Auto 6, a la venta desde el diecinueve de noviembre, en Vice City y el estado de Leonida. Que empiece el combate.",
     mus=("synthwave", 2), id="o03",
     shots=[S(None, X(L5, 160.0), z=(1.0, 1.06), **V5), S("En la esquina derecha", X(THA, 225.0), z=(1.0, 1.06), **V6),
            S("Que empiece", "g:cargo", kicker="EL COMBATE", txt="GTA V CONTRA GTA VI", lado="gta6")],
     sfx=[("w:Que empiece", "stamp", 0.5)])

# ================================================================ 1 · LA CIUDAD
beat("Primer asalto: la ciudad. GTA 5 se juega en Los Santos, la versión de Rockstar de Los Ángeles: rascacielos, autopistas y barrios como el de Franklin, uno de sus protagonistas, donde la gente vive su día en la calle. Franklin, además, tiene un perro, Chop, que lo acompaña por el barrio.",
     chapter=(1, "LA CIUDAD"), mus=("synthwave", 1), pre=1.4, id="c01",
     shots=[S(None, X(L5, 8.0), z=(1.0, 1.06), **V5), S("rascacielos", X(L5, 180.0), z=(1.0, 1.05)), S("barrios como", X(L5, 45.0), z=(1.0, 1.05)),
            S("donde la gente", X(L5, 70.0), z=(1.0, 1.05)), S("tiene un perro", X(L5, 92.0), z=(1.0, 1.06))],
     sfx=[(0.0, "whoosh", 0.35)])
beat("GTA 6 vuelve a Vice City, la versión de Miami, dentro de un estado inventado, Leonida, inspirado en Florida: playas llenas de gente, avenidas con palmeras y edificios de colores. Y en la playa hay hasta un gimnasio al aire libre, donde la gente entrena al atardecer, y el jugador puede estrecharle la mano a un habitante que no suelta las pesas.",
     mus=("tropical", 1), id="c02",
     shots=[S(None, X(THA, 605.0), z=(1.0, 1.05), **V6), S("playas", X(THA, 640.0), z=(1.0, 1.05)), S("avenidas", X(THA, 232.0), z=(1.0, 1.05)), S("hasta un gimnasio", X(THA, 1245.0), z=(1.0, 1.05))])
beat("Los dos mapas tienen su estilo, y aquí no hay trampa posible: depende de lo que te guste. Y los dos salen de la ciudad: GTA 5 tiene campo, desierto y montaña, y GTA 6 tiene, por ejemplo, los cayos de Leonida. Hay quien prefiere el asfalto de Los Ángeles, y quien prefiere el sol de Miami. Primer asalto: empate.",
     mus=("tropical", 1), id="c03",
     shots=[S(None, X(L5, 310.0), z=(1.0, 1.05), **V5), S("el sol de Miami", X(THA, 660.0), z=(1.0, 1.05), **V6),
            S("Primer asalto", "g:ronda", n=1, tema="LA CIUDAD", gana="empate", razon="Los Ángeles contra Miami: cuestión de gustos", score=(0, 0))],
     sfx=[("w:Primer asalto", "stamp", 0.45)])

# ================================================================ 2 · LA POLICÍA
beat("Segundo asalto: la policía. En GTA 5, el nivel de búsqueda máximo era de cinco estrellas, y cuando la policía te perdía de vista, las estrellas parpadeaban mientras te buscaban, hasta apagarse. En GTA 6, hay una sexta. Y si nadie te ha identificado, las estrellas aparecen vacías: la policía sabe que hubo un delito, pero no sabe quién fue.",
     chapter=(2, "LA POLICÍA"), mus=("tension", 2), pre=1.4, id="p01",
     shots=[S(None, X(K5, 56.0), z=(1.0, 1.05), **V5), S("En GTA 6", X(TAN, 160.0), z=(1.0, 1.05), **V6),
            S("una sexta", X(TAN, 172.0), z=(1.0, 1.06), big="6 ESTRELLAS"), S("si nadie te ha identificado", X(TAN, 176.0), z=(1.0, 1.05))],
     sfx=[("w:una sexta", "alarm", 0.3)])
beat("Y la diferencia no es solo de número. Como ya te explicamos en el canal, en GTA 6 la policía necesita que alguien te vea o que salte una alarma. Y según PC Gamer, con seis estrellas ya no puedes bajar el nivel: la única salida es morir.",
     mus=("tension", 2), id="p02", cert="PRENSA",
     shots=[S(None, X(TAN, 182.0), z=(1.0, 1.05), **V6), S("según PC Gamer", X(TAN, 205.0), z=(1.0, 1.05)), S("la única salida", X(TAN, 240.5), z=(1.0, 1.04))])
beat("Y hay más. Según Newsweek, el juego te enseña lo que la policía sabe de ti: tu cara, tu ropa, tu auto o tu arma. Y además de testigos y alarmas, también cuentan las cámaras.",
     mus=("tension", 1), id="p025", cert="PRENSA",
     shots=[S(None, "g:list", title="LO QUE SABE LA POLICÍA", subt="GTA 6 · según Newsweek", items=["Tu cara", "Tu ropa", "Tu auto", "Tu arma"],
              cues=["tu cara", "tu ropa", "tu auto", "tu arma"]),
            S("también cuentan las cámaras", X(B6, 470.0), z=(1.0, 1.05), **V6)],
     sfx=[("w:tu cara", "pop", 0.3), ("w:tu arma", "pop", 0.3)])
beat("Esta persecución real lo demuestra: un tanque contra seis estrellas, puentes, helicópteros, y al final, la pantalla de muerte. Segundo asalto para GTA 6: más estrellas, y una policía que se fija en quién te ha visto.",
     mus=("tension", 1), id="p03", cert="PARTIDA",
     shots=[S(None, X(TAN, 216.0), z=(1.0, 1.05), **V6), S("helicópteros", X(TAN, 226.0), z=(1.0, 1.06)), S("la pantalla de muerte", X(TAN, 246.6), z=(1.0, 1.03)),
            S("Segundo asalto", "g:ronda", n=2, tema="LA POLICÍA", gana="gta6", razon="Una sexta estrella y testigos que te delatan", score=(0, 1))],
     sfx=[("w:Segundo asalto", "stamp", 0.45)])

# ================================================================ 3 · EL CAZA
beat("Tercer asalto: robar un avión de combate. Es casi una tradición de la saga, y los dos juegos la cumplen. En GTA 5, el lugar es Fort Zancudo, la base militar del oeste del mapa.",
     chapter=(3, "EL CAZA"), mus=("tension", 2), pre=1.4, id="j01", cert="GUIA",
     shots=[S(None, X(K5, 22.0), z=(1.0, 1.04), **V5), S("En GTA 5", X(K5, 36.0), z=(1.0, 1.05)), S("la base militar", X(K5, 64.0), z=(1.0, 1.05))],
     sfx=[(0.0, "whoosh", 0.35)])
beat("Una guía en vídeo de dos mil trece lo hace con una partida de solo dos horas: entra en la base, se sube a un caza y despega mientras le lanzan misiles. Otra guía de la misma época avisaba de que la base, tanques incluidos, se pone en alerta en cuanto entras, de que está rodeada por una valla alta, y de que su autor murió muchas veces antes de conseguirlo. Su receta: un auto rápido, embestir la puerta, ir directo a los hangares, subirse al primer caza y despegar cuanto antes.",
     mus=("tension", 2), id="j02", cert="GUIA",
     shots=[S(None, X(K5, 72.0), z=(1.0, 1.05), **V5), S("y despega", X(K5, 84.0), z=(1.0, 1.06)), S("Otra guía", X(E5, 5.0), z=(1.0, 1.05), **V5),
            S("una valla alta", X(E5, 40.0), z=(1.0, 1.05)), S("murió muchas veces", X(E5, 44.0), z=(1.0, 1.04)), S("Su receta", X(E5, 93.0), z=(1.0, 1.05)), S("ir directo a los hangares", X(E5, 106.0), z=(1.0, 1.05))],
     sfx=[("w:murió", "impact", 0.4)])
beat("En GTA 6, el caza está en una base aérea, al oeste de la casa de Jason. Según otra guía, la forma de entrar es llegar en lancha, robar un blindado del ejército y saltar la valla. Y al subir al blindado, el juego te pone cinco estrellas de golpe. La propia guía recomienda guardar la partida antes y llevar objetos de curación, porque morir es casi seguro.",
     mus=("tension", 2), id="j03", cert="GUIA",
     shots=[S(None, X(B6, 352.0), z=(1.0, 1.05), **V6), S("robar un blindado", X(B6, 414.0), z=(1.0, 1.05)), S("cinco estrellas", X(JET, 108.0), z=(1.0, 1.06), big="5 ESTRELLAS DE GOLPE"), S("La propia guía", X(B6, 430.0), z=(1.0, 1.05))],
     sfx=[("w:cinco estrellas", "alarm", 0.3)])
beat("Después, encender el avión lleva su tiempo, y la libertad dura poco. En los dos juegos se puede, en los dos es un caos, y en los dos acaba mal. Tercer asalto: empate.",
     mus=("tension", 1), id="j04", cert="GUIA",
     shots=[S(None, X(JET, 162.3), z=(1.0, 1.06), **V6), S("En los dos juegos", X(E5, 136.0), z=(1.0, 1.05), **V5),
            S("Tercer asalto", "g:ronda", n=3, tema="EL CAZA", gana="empate", razon="Los dos te dejan robarlo… y los dos te derriban", score=(0, 1))],
     sfx=[("w:Tercer asalto", "stamp", 0.45)])

# ================================================================ 4 · EL TANQUE
beat("Cuarto asalto: el tanque. En la misma base de GTA 5, la guía de dos mil trece entra con el coche, y la alarma no salta al instante. Entonces encuentra un tanque casi por suerte, se sube, y sale a la carretera disparando.",
     chapter=(4, "EL TANQUE"), mus=("tension", 2), pre=1.4, id="t01", cert="GUIA",
     shots=[S(None, X(K5, 36.0), z=(1.0, 1.05), **V5), S("Entonces encuentra", X(K5, 44.0), z=(1.0, 1.05)), S("se sube", X(K5, 49.0), z=(1.0, 1.06)), S("sale a la carretera", X(K5, 58.0), z=(1.0, 1.05))],
     sfx=[("w:disparando", "impact", 0.4)])
beat("En GTA 6, este jugador se lanza en paracaídas sobre una base militar, se sube a un tanque, y aguanta una persecución de seis estrellas por toda la ciudad, hasta una pista de aterrizaje donde un avión acaba envuelto en llamas.",
     mus=("tension", 3), id="t02", cert="PARTIDA",
     shots=[S(None, X(TAN, 140.0), z=(1.0, 1.05), **V6), S("por toda la ciudad", X(TAN, 194.0), z=(1.0, 1.05)), S("una pista", X(TAN, 287.0), z=(1.0, 1.05)),
            S("envuelto en llamas", X(TAN, 305.5), z=(1.0, 1.08))],
     sfx=[("w:llamas", "impact", 0.45)])
beat("Eso sí, en GTA 6 subirse a un tanque no da seis estrellas por sí solo: según las guías, la sexta llega cuando causas una destrucción masiva. La idea es la misma, pero la persecución de GTA 6 tiene un nivel más de policía detrás. Cuarto asalto para GTA 6.",
     mus=("tension", 1), id="t03",
     shots=[S(None, X(TAN, 296.0), z=(1.0, 1.05), **V6),
            S("Cuarto asalto", "g:ronda", n=4, tema="EL TANQUE", gana="gta6", razon="La misma idea, con una estrella más detrás", score=(0, 2))],
     sfx=[("w:Cuarto asalto", "stamp", 0.45)])

# ================================================================ 5 · LA GENTE
beat("Quinto asalto: la gente. En GTA 5, las calles de Los Santos están llenas de peatones que reaccionan a lo que haces, pero no hay un menú para elegir cómo hablarles. Las conversaciones con desconocidos estaban escritas para ocasiones concretas, como los encuentros de la serie de misiones de desconocidos y locos.",
     chapter=(5, "LA GENTE"), mus=("synthwave", 1), pre=1.4, id="g01",
     shots=[S(None, X(L5, 56.0), z=(1.0, 1.05), **V5), S("que reaccionan", X(L5, 82.0), z=(1.0, 1.05)), S("pero no hay", X(L5, 100.0), z=(1.0, 1.05)), S("Las conversaciones", X(L5, 110.0), z=(1.0, 1.05))])
beat("En GTA 6 sí lo hay. Al acercarte a alguien, aparecen dos opciones, calmar o provocar, y una etiqueta que te dice si esa persona es turista o local.",
     mus=("synthwave", 1), id="g02", cert="OBSERVADO",
     shots=[S(None, X(THA, 694.0), z=(1.0, 1.04), **V6), S("una etiqueta", X(THA, 709.0), card=True, card_zoom=(0.78, 0.80, 1.0, 1.0), zoom_at=0.35),
            S("o local", X(THA, 1262.0), card=True, card_zoom=(0.78, 0.80, 1.0, 1.0), zoom_at=0.3)],
     sfx=[("w:una etiqueta", "pop", 0.35)])
beat("Y las respuestas son de todo tipo: «No me hables». «Aléjate de mí».",
     mus=("synthwave", 1), id="g03", cert="OBSERVADO",
     shots=[S(None, X(TOA, 4.0), **TOACAP, **V6), S("«No me", X(TOA, 8.0), **TOACAP, say="Don't talk to me."), S("«Aléjate", X(TOA, 12.5), **TOACAP, say="Get away from me.")])
beat("Y a veces es la gente la que viene a ti. Este desconocido quiere la bolsa del jugador, y en pantalla aparecen dos opciones: entregársela o negarse. El jugador se niega, empieza una pelea, y alrededor alguien grita: «¡Que alguien llame a la policía!».",
     mus=("tension", 1), id="g035", cert="OBSERVADO",
     shots=[S(None, X(TOA, 18.0), **TOACAP, **V6), S("dos opciones", X(TOA, 24.0), **TOACAP, say="Give bag / Decline"), S("El jugador se niega", X(TOA, 28.0), **TOACAP),
            S("alguien grita", X(TOA, 38.5), **TOACAP, say="Someone call the cops!")],
     sfx=[("w:pelea", "impact", 0.35)])
beat("Según Rockstar, GTA 6 lleva las interacciones con los personajes más lejos que Red Dead Redemption 2. Quinto asalto, sin discusión, para GTA 6.",
     mus=("synthwave", 1), id="g04",
     shots=[S(None, "g:quote", q="GTA 6 lleva las interacciones con los personajes de su mundo más lejos que Red Dead Redemption 2.", who="SEGÚN ROCKSTAR · DECLARACIONES RECOGIDAS POR LA PRENSA", tag="ROCKSTAR"),
            S("Quinto asalto", "g:ronda", n=5, tema="LA GENTE", gana="gta6", razon="Calmar, provocar, turista o local: un menú que GTA 5 no tenía", score=(0, 3))],
     sfx=[("w:Quinto asalto", "stamp", 0.45)])

# ================================================================ 6 · MORIR
beat("Sexto asalto: morir. En los dos juegos, cuando te matan, aparece el mensaje de muerte: en GTA 5, sobre una imagen en gris; en GTA 6, sobre una imagen en rojo.",
     chapter=(6, "MORIR"), mus=("noir", 1), pre=1.4, id="m01",
     shots=[S(None, X(E5, 47.0), z=(1.0, 1.04), **V5), S("en GTA 6, sobre", X(TAN, 247.0), z=(1.0, 1.03), **V6)],
     sfx=[("w:mensaje de muerte", "impact", 0.4)])
beat("En GTA 5, despertabas en el hospital y te cobraban la factura: según la wiki de GTA, depende del dinero que lleves encima, y llega hasta cinco mil dólares.",
     mus=("noir", 1), id="m02", cert="PRENSA",
     shots=[S(None, X(E5, 52.0), z=(1.0, 1.04), **V5), S("según la wiki", "g:list", title="EL HOSPITAL EN GTA 5", subt="Según la GTA Wiki",
              items=["Despiertas en el hospital", "La factura depende de tu dinero", "Máximo: 5.000 dólares"], cues=["despertabas", "depende del dinero", "cinco mil"])],
     sfx=[("w:cinco mil", "coin", 0.45)])
beat("En GTA 6, este jugador recibe un disparo, despierta junto a la carretera, y en la esquina de la pantalla aparece el cargo: mil ciento noventa y un dólares de hospital.",
     mus=("noir", 1), id="m03", cert="PARTIDA",
     shots=[S(None, X(HOS, 6.3), card=True, **V6), S("en la esquina", X(HOS, 13.45), card=True, card_zoom=(0.84, 0.17, 1.0, 0.47), zoom_at=0.3)],
     sfx=[("w:mil ciento", "coin", 0.45)])
beat("Pero no es una comparación justa: en GTA 5 la cifra depende de lo que lleves, y en GTA 6 solo tenemos este caso. Así que el sexto asalto queda en empate.",
     mus=("noir", 1), id="m04",
     shots=[S(None, X(HOS, 0.0), card=True, **V6), S("Así que", "g:ronda", n=6, tema="MORIR", gana="empate", razon="Cifras que no se pueden comparar todavía", score=(0, 3))],
     sfx=[("w:empate", "stamp", 0.45)])

# ================================================================ 7 · LOS PODERES
beat("Séptimo asalto: los poderes. En GTA 5, cada uno de sus tres protagonistas tenía una habilidad especial. Michael ralentizaba el tiempo en los tiroteos, Franklin lo hacía al volante, y Trevor entraba en un estado de furia.",
     chapter=(7, "LOS PODERES"), mus=("synthwave", 2), pre=1.4, id="h01", cert="GUIA",
     shots=[S(None, X(L5, 600.0), z=(1.0, 1.05), **V5), S("Michael", "g:list", title="TRES PROTAGONISTAS, TRES PODERES", subt="GTA 5",
              items=["Michael · cámara lenta en los tiroteos", "Franklin · cámara lenta al volante", "Trevor · modo furia"], cues=["Michael", "Franklin", "Trevor"])],
     sfx=[("w:Michael", "pop", 0.3), ("w:Franklin", "pop", 0.3), ("w:Trevor", "pop", 0.3)])
beat("Tanto, que una de aquellas guías recomendaba cambiar a Franklin para robar el caza: su habilidad hacía más fácil cruzar la entrada de la base. Y en GTA 5 podías cambiar de protagonista casi en cualquier momento, con la cámara alejándose sobre el mapa.",
     mus=("synthwave", 2), id="h02", cert="GUIA",
     shots=[S(None, X(E5, 80.0), z=(1.0, 1.05), **V5), S("cruzar la entrada", X(E5, 96.0), z=(1.0, 1.06)), S("podías cambiar", X(L5, 620.0), z=(1.0, 1.05), **V5)])
beat("En GTA 6, Jason y Lucía comparten el mismo sistema, el Focus, una barra que, por ejemplo, sube un tres por ciento si tiras las latas vacías a la basura. Y GTA 6 también te deja cambiar entre los dos protagonistas, sin pantalla de carga.",
     mus=("tropical", 1), id="h03", cert="GUIA",
     shots=[S(None, X(CAS, 79.0), z=(1.0, 1.05), **V6), S("sube un tres", X(CAS, 86.0), z=(1.0, 1.06), big="+3 % FOCUS"), S("cambiar entre los dos", X(CAS, 28.3), z=(1.0, 1.05))],
     sfx=[("w:tres por ciento", "ding", 0.4)])
beat("Y en lo que mostró Rockstar antes del lanzamiento, el Focus también sirve en los tiroteos: el tiempo se ralentiza y se marcan los puntos débiles del enemigo. Algo que recuerda mucho a la habilidad de Michael. Pero es la misma barra para los dos protagonistas.",
     mus=("synthwave", 1), id="h035", cert="ROCKSTAR",
     shots=[S(None, X(B6, 440.0), z=(1.0, 1.05), **V6), S("Algo que recuerda", X(L5, 680.0), z=(1.0, 1.05), **V5), S("Pero es la misma", X(CAS, 82.0), z=(1.0, 1.05), **V6)])
beat("Tres poderes distintos contra un mismo sistema para los dos. Séptimo asalto para GTA 5.",
     mus=("synthwave", 2), id="h04",
     shots=[S(None, X(L5, 640.0), z=(1.0, 1.05), **V5),
            S("Séptimo asalto", "g:ronda", n=7, tema="LOS PODERES", gana="gta5", razon="Tres protagonistas, tres habilidades distintas", score=(1, 3))],
     sfx=[("w:Séptimo asalto", "stamp", 0.45)])

# ================================================================ 8 · LA FLUIDEZ
beat("Octavo y último asalto: la fluidez. En PlayStation 5 y Xbox Series, GTA 5 tiene un modo de rendimiento a sesenta imágenes por segundo, que Rockstar anunció en dos mil veintidós. Es un juego que salió en PlayStation 3 y Xbox 360, y que ha llegado a tres generaciones de consolas.",
     chapter=(8, "LA FLUIDEZ"), mus=("synthwave", 1), pre=1.4, id="f01", cert="PRENSA",
     shots=[S(None, X(L5, 660.0), z=(1.0, 1.05), **V5), S("sesenta imágenes", "g:cover", kicker="GTA 5 EN PS5 Y XBOX SERIES", lines=["60", "IMÁGENES/S"], sub="Modo rendimiento · Rockstar, 2022"), S("Es un juego", X(L5, 700.0), z=(1.0, 1.05), **V5)],
     sfx=[("w:sesenta", "pop", 0.4)])
beat("GTA 6, según Rockstar, funciona a treinta, y su equipo técnico aún no tenía claro si habrá un modo de sesenta. Ojo: este vídeo va a treinta imágenes por segundo, así que aquí no lo vas a notar. Pero con el mando en la mano, se nota. Octavo asalto para GTA 5.",
     mus=("synthwave", 1), id="f02", cert="PRENSA",
     shots=[S(None, "g:cover", kicker="GTA 6 · SEGÚN ROCKSTAR", lines=["30", "IMÁGENES/S"], sub="Sin un modo de 60 confirmado"),
            S("Ojo", X(THA, 245.0), z=(1.0, 1.05), **V6), S("con el mando", X(L5, 690.0), z=(1.0, 1.05), **V5),
            S("Octavo asalto", "g:ronda", n=8, tema="LA FLUIDEZ", gana="gta5", razon="60 imágenes por segundo contra 30", score=(2, 3))],
     sfx=[("w:Octavo asalto", "stamp", 0.45)])

# ================================================================ VEREDICTO
beat("Fin del combate. Repasemos el marcador. Para GTA 5: los poderes y la fluidez. Para GTA 6: la policía, el tanque y la gente. Y quedan en empate la ciudad, el caza y morir.",
     mus=("noir", 2), pre=0.8, id="r01",
     shots=[S(None, "g:marcador", title="EL MARCADOR", names=("GTA V", "GTA VI"), colors=(R.G5, R.G6),
              acu=["Los poderes", "La fluidez"], **{"def": ["La policía", "El tanque", "La gente"]},
              cues=["los poderes", "la fluidez", "la policía", "el tanque", "la gente"])],
     sfx=[("w:los poderes", "pop", 0.3), ("w:la fluidez", "pop", 0.3), ("w:la policía", "pop", 0.3), ("w:el tanque", "pop", 0.3), ("w:la gente", "pop", 0.3)])
beat("Resultado: tres asaltos para GTA 6, dos para GTA 5 y tres empates. GTA 6 gana, pero a los puntos, y no por paliza. Trece años después, el veterano todavía da guerra. Lo que deja claro este combate es que GTA 6 no gana por fuerza bruta, sino por los detalles: una policía que necesita testigos, un menú para hablar con la gente, y una persecución que no se acaba hasta que caes. Y GTA 5 sigue ganando en lo que mejor hacía: tres personajes con su propio poder, y un juego que va como la seda.",
     mus=("noir", 2), id="r02",
     shots=[S(None, "g:cover", kicker="RESULTADO FINAL", lines=["GTA 6 GANA", "A LOS PUNTOS"], sub="3 asaltos para GTA 6 · 2 para GTA 5 · 3 empates"),
            S("Trece años después", X(L5, 12.0), z=(1.0, 1.05), **V5), S("Lo que deja claro", X(TAN, 300.0), z=(1.0, 1.05), **V6), S("Y GTA 5 sigue", X(L5, 330.0), z=(1.0, 1.05), **V5)],
     sfx=[(0.0, "stamp", 0.5)])
beat("¿Y tú? ¿Cuál es tu marcador? Escribe en los comentarios qué asalto le darías a cada uno. Y si quieres ver a GTA 6 en un juicio de verdad, tienes ese video en el canal.",
     mus=("tropical", 1), pre=0.6, id="r03",
     shots=[S(None, "g:veredicto", title="TU MARCADOR", subt="¿Quién gana cada asalto?", opts=[("GTA V", "el veterano", R.G5), ("GTA VI", "el aspirante", R.G6)],
              cues=["tu marcador", "a cada uno"], foot="ESCRÍBELO EN LOS COMENTARIOS")],
     sfx=[("w:comentarios", "pop", 0.4)])
beat("Y si quieres más GTA 6 contado de otra forma, suscríbete a Sal y Asfalto. Nos vemos en el próximo combate.",
     mus=("tropical", 1), hold=0.6, id="r04",
     shots=[S(None, X(THA, 700.0), z=(1.0, 1.05), **V6), S("suscríbete", "g:subscribe")],
     sfx=[("w:suscríbete", "pop", 0.45)])
beat("", dur=20.0, mus=("tropical", 1), id="end", shots=[S(None, "g:end")], trans="fade")

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
        y = audio.compose(sg["style"], dur, energy=en, seed=8400 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "VIDEO_LARGO_4_GTA5_VS_GTA6"
for _d in ("trabajo", "trabajo/audio"):
    os.makedirs(os.path.join(_ROOT, FOLDER, _d), exist_ok=True)

VIDEO = dict(id="cv", folder=FOLDER, file="VIDEO_FINAL", res_dir="trabajo", theme="combate",
             title="GTA 5 vs GTA 6: 8 asaltos con partidas reales",
             format="Largo (16:9, 1920×1080, 30 fps) · gameplay real de los dos juegos", music="synthwave", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55,
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="trabajo/audio/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.thumb_combate(c)
