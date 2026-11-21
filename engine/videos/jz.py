"""VIDEO_LARGO_3 — «Llevamos GTA 6 a juicio: ¿juego de crímenes o simulador de vida?»

Formato nuevo (no lo hace ningún canal): un juicio con acusación, defensa, testigos y alegatos. Las «pruebas» son partidas
reales publicadas tras el lanzamiento (19/11/2026) y las declaraciones, citas verificadas con su fuente en pantalla:
- Policía de Atlanta (X, 17/11/2026) · sheriff de Miami-Dade (PC Gamer, sept. 2026) · documento filtrado en China (sin confirmar)
- Rockstar: comunicado sobre funciones retiradas (Shacknews, recogido por IGN Daily Fix 19/11) · Rob Nelson a The Guardian
- Guías de IGN (casa, misiones secundarias, caza, fuente de Capri) · partidas de GameV (tanque) y Video Pump (factura del hospital)
Sin spoilers de la historia: solo actividades libres.

Planos: S(ancla, fuente, **opciones). fuente = x:<ID>@<segundo del original> · g:<gráfico> (videos/dc_render.py)
"""
import os
import numpy as np
import audio
from videos import dc_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def X(vid, t): return f"x:{vid}@{t}"

TAN = "-UuHA1h-Cf8"   # GameV · «Can a TANK Survive a 6-STAR Police Chase in GTA 6?» (PS5 Pro, 4K)
JET = "4HCd052lpnA"   # IGN · «GTA 6: You Can Steal a Fighter Jet in Chapter 1 (But Probably Shouldn't)»
CAS = "3UiRmXUIE9k"   # IGN · «GTA 6: Fix Your Safehouse FIRST!»
MIS = "xnNu7YybiCM"   # IGN · «7 Optional Missions in GTA 6 You Won't Want to Miss»
FUE = "R9r9ew12GcA"   # IGN · Short de la fuente de Capri (vertical)
HOS = "vpHospital1"   # Video Pump · «Wasted in GTA 6, Then a $1,191 Hospital Bill» (solo la imagen de juego)

# ================================================================ APERTURA
beat("Dos días antes del lanzamiento de GTA 6, la policía de Atlanta publicó un aviso para los jugadores: «Déjalo en el juego. No lo traigas a nuestras calles». Y recordaba que conducir borracho o de forma temeraria, robar autos y la violencia tienen consecuencias reales.",
     mus=("noir", 2), pre=0.3, id="j01", cert="PRENSA",
     shots=[S(None, X(TAN, 292.0), z=(1.0, 1.06)),
            S("«Déjalo", "g:quote", q="Déjalo en el juego. No lo traigas a nuestras calles.", who="POLICÍA DE ATLANTA · 17/11/2026", tag="PRENSA",
              sub="«GTA no es un lugar real, pero Atlanta sí»")],
     sfx=[(0.0, "riser", 0.35), ("w:«Déjalo", "stamp", 0.45)])
beat("En Miami fueron más lejos. La sheriff del condado se opuso a que la ciudad se disfrazara de Vice City para promocionar el juego, porque, según ella, Grand Theft Auto es una saga construida alrededor del crimen.",
     mus=("noir", 2), id="j02", cert="PRENSA",
     shots=[S(None, X(TAN, 118.0), z=(1.0, 1.06)),
            S("para promocionar", X(TAN, 168.0), z=(1.05, 1.0)),
            S("Grand Theft Auto", X(TAN, 304.5), z=(1.0, 1.08))],
     sfx=[("w:Grand Theft", "impact", 0.4)])
beat("Así que hoy vamos a hacer algo distinto: sentar a GTA 6 en el banquillo. ¿Es un juego de crímenes, o un simulador de vida? Las pruebas son partidas reales, y el veredicto lo pones tú.",
     mus=("noir", 2), id="j03",
     shots=[S(None, "g:cover", kicker="SAL Y ASFALTO PRESENTA", lines=["GTA 6", "A JUICIO"], sub="¿Juego de crímenes o simulador de vida?"),
            S("¿Es un juego", X(TAN, 20.0), z=(1.0, 1.05), big="¿CRÍMENES?", big_col=R.RED),
            S("simulador de vida", X(CAS, 68.0), z=(1.0, 1.05), big="¿O VIDA?", big_col=R.BLUE),
            S("Las pruebas", X(JET, 104.0), z=(1.0, 1.06))],
     sfx=[("w:banquillo", "stamp", 0.5), ("w:¿Es un", "whoosh", 0.35), ("w:simulador", "whoosh", 0.35)])
beat("Antes de empezar, estas son las reglas del juicio. Todo lo que vas a ver son partidas reales, grabadas por jugadores en los primeros días después del lanzamiento. Lo que dijeron Rockstar y la prensa aparece en pantalla con su fuente, y cada cita está traducida del inglés.",
     mus=("noir", 1), pre=0.4, id="j04",
     shots=[S(None, "g:sting"),
            S("Todo lo que", "g:creators", title="LAS PRUEBAS", subt="Partidas reales publicadas tras el lanzamiento (19/11/2026)",
              rows=[("GameV", "Un tanque contra seis estrellas"), ("IGN", "Guías: casa, misiones, caza, fuente"), ("Video Pump", "La factura del hospital")],
              foot="Créditos de cada plano en pantalla y en la descripción"),
            S("Lo que dijeron", X(TAN, 125.0), z=(1.0, 1.05))],
     sfx=[(0.0, "logo", 0.5), ("w:Todo lo que", "paper", 0.4)])
beat("Y no hay spoilers de la historia: solo cosas que puedes hacer por tu cuenta, cuando el juego te deja libre. Se abre la sesión.",
     mus=("noir", 1), id="j05",
     shots=[S(None, X(MIS, 160.0), z=(1.0, 1.05)), S("Se abre", "g:cargo", kicker="SE ABRE LA SESIÓN", txt="EL ESTADO DE VICE CITY CONTRA GTA 6", lado="defensa")],
     sfx=[("w:Se abre", "stamp", 0.5)])
beat("El acusado: Grand Theft Auto 6, de Rockstar Games, a la venta desde el diecinueve de noviembre en PlayStation 5 y Xbox Series. El cargo: que, en el fondo, es un simulador de crímenes.",
     mus=("noir", 2), id="j06",
     shots=[S(None, X(TAN, 300.5), z=(1.0, 1.05)), S("El cargo", "g:cargo", kicker="EL CARGO", txt="SER UN SIMULADOR DE CRÍMENES", lado="acusacion")],
     sfx=[("w:El cargo", "stamp", 0.5)])

# ================================================================ SESIÓN 1 · LA ACUSACIÓN
beat("La acusación quiere demostrar que GTA 6 sigue siendo, ante todo, un juego de crímenes. Y empieza con su prueba más grande.",
     chapter=(1, "LA ACUSACIÓN"), mus=("tension", 2), pre=1.4, id="a01", cert="PARTIDA",
     shots=[S(None, X(TAN, 128.0), z=(1.0, 1.05)), S("su prueba", X(TAN, 1.0), z=(1.0, 1.04))],
     sfx=[(0.0, "impact", 0.4)])
beat("Primera prueba. Un jugador se lanza en paracaídas sobre una base militar, se sube a un tanque y sale a la carretera como si nada.",
     mus=("tension", 2), id="a02", cert="PARTIDA",
     shots=[S(None, X(TAN, 4.0), z=(1.0, 1.06), prueba="PRUEBA A", lado="acusacion"),
            S("se sube", X(TAN, 17.0), z=(1.0, 1.05)),
            S("sale a la carretera", X(TAN, 27.0), z=(1.0, 1.05))],
     sfx=[("w:Primera prueba", "stamp", 0.5)])
beat("Lo que viene después es una persecución de seis estrellas: puentes, autopistas, helicópteros, y una pista de aterrizaje donde un avión acaba envuelto en llamas. Y nada de esto es una misión: es lo que el juego te deja hacer en su mundo abierto, cuando quieras. Al final, el tanque no aguanta, y la partida termina en la pantalla de muerte.",
     mus=("tension", 3), id="a03", cert="PARTIDA",
     shots=[S(None, X(TAN, 140.0), z=(1.0, 1.05)),
            S("puentes", X(TAN, 172.0), z=(1.0, 1.06)),
            S("helicópteros", X(TAN, 203.0), z=(1.0, 1.06)),
            S("una pista", X(TAN, 287.0), z=(1.0, 1.05)),
            S("envuelto en llamas", X(TAN, 305.5), z=(1.0, 1.08)),
            S("Y nada de esto", X(TAN, 214.0), z=(1.0, 1.05)),
            S("Al final, el tanque", X(TAN, 240.5), z=(1.0, 1.06)),
            S("pantalla de muerte", X(TAN, 246.6), z=(1.0, 1.03))],
     sfx=[("w:helicópteros", "whoosh", 0.35), ("w:llamas", "impact", 0.45)])
beat("Segunda prueba. Una guía en vídeo explica, paso a paso, cómo robar un avión de combate en el primer capítulo del juego.",
     mus=("tension", 2), id="a04", cert="GUIA",
     shots=[S(None, X(JET, 62.0), z=(1.0, 1.05), prueba="PRUEBA B", lado="acusacion"), S("cómo robar", X(JET, 134.0), z=(1.0, 1.06))],
     sfx=[("w:Segunda prueba", "stamp", 0.5)])
beat("El método es llegar en lancha hasta la base aérea, robar un blindado del ejército y saltar la valla. Al subir al vehículo, el juego te pone cinco estrellas de golpe, y el ejército te manda de todo, incluidos tanques.",
     mus=("tension", 2), id="a05", cert="GUIA",
     shots=[S(None, X(JET, 70.0), z=(1.0, 1.05)), S("saltar la valla", X(JET, 84.0), z=(1.0, 1.05)),
            S("cinco estrellas", X(JET, 108.0), z=(1.0, 1.06), big="5 ESTRELLAS DE GOLPE")],
     sfx=[("w:cinco estrellas", "alarm", 0.3)])
beat("Ya en la base, encender el avión lleva su tiempo, y mientras tanto te disparan sin parar. Pero cuando por fin despegas, la guía te felicita: ya eres piloto… aunque sea por poco tiempo.",
     mus=("tension", 2), id="a055", cert="GUIA",
     shots=[S(None, X(JET, 162.3), z=(1.0, 1.06))],   # de noche: el caza en la pista, el despegue y la explosión, sin cortes
     sfx=[("w:despegas", "whoosh", 0.4), ("w:poco tiempo", "impact", 0.35)])
beat("Y la propia guía avisa de cómo termina. Recomienda llevar objetos de curación y guardar la partida, porque tendrás unos momentos de libertad antes de que te derribe, en sus palabras, «la policía de la diversión». Lo recomienda incluso desde el título: puedes robar un caza… aunque probablemente no deberías.",
     mus=("tension", 2), id="a06", cert="GUIA",
     shots=[S(None, X(JET, 140.0), z=(1.0, 1.05)), S("antes de que", X(JET, 148.0), z=(1.0, 1.06)),
            S("puedes robar", "g:quote", q="Puedes robar un avión de combate en el capítulo 1 (aunque probablemente no deberías)", who="TÍTULO DE LA GUÍA DE IGN · 20/11/2026", tag="GUIA")],
     sfx=[("w:puedes robar", "paper", 0.4)])
beat("Tercera prueba. La declaración de la sheriff de Miami-Dade, recogida por PC Gamer: «Grand Theft Auto es una saga de videojuegos construida alrededor de la actividad criminal».",
     mus=("noir", 2), id="a07",
     shots=[S(None, "g:quote", q="Grand Theft Auto es una saga de videojuegos construida alrededor de la actividad criminal.", who="SHERIFF DE MIAMI-DADE · SEGÚN PC GAMER", tag="PRENSA",
              sub="Se opuso a que Miami-Dade se convirtiera en Vice City para promocionar el juego", sub_at=4.0, col=R.RED)],
     sfx=[(0.1, "stamp", 0.5)])
beat("Y la cuarta prueba es la más curiosa. En China circula un documento filtrado, que nadie ha confirmado, con reglas para quien quiera transmitir el juego en directo.",
     mus=("noir", 2), id="a08",
     shots=[S(None, X(TAN, 222.0), z=(1.0, 1.05), prueba="PRUEBA D", lado="acusacion"), S("con reglas", X(TAN, 112.0), z=(1.0, 1.05))],
     sfx=[("w:cuarta prueba", "stamp", 0.5), ("w:con reglas", "paper", 0.4)])
beat("Según ese documento, en pantalla no se podría robar autos, ni atacar a la policía o a los peatones. Ni siquiera mostrar sangre roja. En un foro, un jugador lo resumió así: con esas reglas, GTA 6 sería un simulador de paisajes.",
     mus=("noir", 2), id="a09",
     shots=[S(None, "g:list", title="DOCUMENTO FILTRADO", subt="Reglas para transmitir GTA 6 en China · sin confirmar", cert="FILTRADO",
              items=["Nada de robar autos", "Nada de atacar a la policía", "Nada de atacar a los peatones", "Nada de sangre roja"],
              cues=["robar autos", "a la policía", "peatones", "sangre roja"])],
     sfx=[("w:robar", "pop", 0.35), ("w:policía", "pop", 0.35), ("w:peatones", "pop", 0.35), ("w:sangre", "pop", 0.35)])
beat("La pregunta de la acusación es simple: si le quitas los crímenes a GTA 6, ¿qué queda? La defensa tiene una respuesta.",
     mus=("noir", 1), id="a10",
     shots=[S(None, X(TAN, 236.0), z=(1.0, 1.05)), S("La defensa", "g:cargo", kicker="TURNO DE LA DEFENSA", txt="¿QUÉ QUEDA SIN CRÍMENES?", lado="defensa")],
     sfx=[("w:La defensa", "stamp", 0.5)])

# ================================================================ SESIÓN 2 · LA DEFENSA
beat("Prueba uno: la casa. La primera casa de Jason se la alquila a Brian, y es un desastre. Otra guía explica cómo arreglarla.",
     chapter=(2, "LA DEFENSA"), mus=("tropical", 1), pre=1.4, id="d01", cert="GUIA",
     shots=[S(None, X(CAS, 37.0), z=(1.0, 1.05), prueba="PRUEBA 1", lado="defensa"), S("es un desastre", X(CAS, 61.0), z=(1.0, 1.05)),
            S("Otra guía", X(CAS, 63.5), z=(1.0, 1.05))],
     sfx=[("w:Prueba uno", "stamp", 0.5)])
beat("Hay que reparar la pared del dormitorio y elegir el color de la pintura, clavar las tejas sueltas del techo, arreglar la baranda del gimnasio de la terraza y cambiar los escalones podridos de la entrada.",
     mus=("tropical", 1), id="d02", cert="GUIA",
     shots=[S(None, X(CAS, 43.0), z=(1.0, 1.05)), S("el color", X(CAS, 52.0), z=(1.0, 1.05)),
            S("clavar las tejas", X(CAS, 66.5), z=(1.0, 1.05)), S("arreglar la baranda", X(CAS, 94.0), z=(1.0, 1.05)),
            S("cambiar los escalones", X(CAS, 105.0), z=(1.0, 1.05))],
     sfx=[("w:pared", "brush", 0.3), ("w:tejas", "hit", 0.25), ("w:baranda", "hit", 0.25)])
beat("Además, en el dormitorio puedes dormir para que pase el tiempo y guardar tu dinero escondido. Y la recompensa por arreglar la casa no es dinero: según la guía, hace feliz a Lucía y mejora la relación entre los dos, con un corazón en pantalla. Eso sí, hay que hacerlo antes de ir a buscar a Lucía: en cuanto sales, las reparaciones pendientes se bloquean.",
     mus=("tropical", 1), id="d03", cert="GUIA",
     shots=[S(None, X(CAS, 112.0), z=(1.0, 1.05)), S("la recompensa", "g:list", title="LA RECOMPENSA", subt="Según la guía de IGN",
              items=["No es dinero", "Lucía, más feliz", "Mejora la relación (corazón en pantalla)"], cues=["no es dinero", "feliz a Lucía", "un corazón"])],
     sfx=[("w:corazón", "chime", 0.45)])
beat("Prueba dos, la favorita de la defensa. Después de tomarte una cerveza, si tiras las latas vacías al contenedor, la barra de Focus sube un tres por ciento. GTA 6 te premia por sacar la basura.",
     mus=("tropical", 2), id="d04", cert="GUIA",
     shots=[S(None, X(CAS, 79.0), z=(1.0, 1.05), prueba="PRUEBA 2", lado="defensa"), S("si tiras", X(CAS, 85.0), z=(1.0, 1.06)),
            S("tres por ciento", X(CAS, 89.0), z=(1.0, 1.06), big="+3 % DE FOCUS"),
            S("GTA 6 te premia", X(CAS, 116.5), z=(1.0, 1.05))],
     sfx=[("w:Prueba dos", "stamp", 0.5), ("w:tres por", "coin", 0.4)])
beat("Prueba tres: las misiones secundarias. Karl McKittrick, un granjero con el brazo roto, necesita un piloto para fumigar sus cultivos, y ese piloto eres tú. Tienes que seguir su auto desde el aire y regar sus plantas. Según la guía, la primera vez parece un encargo aburrido, pero si vuelves cada vez que te necesita, la historia cambia por completo.",
     mus=("tropical", 2), id="d05", cert="GUIA",
     shots=[S(None, X(MIS, 150.0), z=(1.0, 1.05), prueba="PRUEBA 3", lado="defensa"), S("necesita un piloto", X(MIS, 157.0), z=(1.0, 1.05)),
            S("y ese piloto", X(MIS, 166.0), z=(1.0, 1.06))],
     sfx=[("w:Prueba tres", "stamp", 0.5)])
beat("Dodo Rising, un grupo que defiende a los animales, protesta contra un santuario de chimpancés cerca del aeropuerto, y te pide ayuda para salvarlos. Es solo el primero de varios encargos con ese grupo.",
     mus=("tropical", 2), id="d06", cert="GUIA",
     shots=[S(None, X(MIS, 270.0), z=(1.0, 1.05)), S("y te pide", X(MIS, 282.0), z=(1.0, 1.05))])
beat("Otra misión empieza de forma inquietante. Navegando por los pantanos, oyes unos aullidos espantosos. Si sigues el olor de un ciervo muerto, llegas a un tótem escondido entre la maleza… y te desmayas. Lo último que ves es un par de piernas.",
     mus=("noir", 1), id="d065", cert="GUIA",
     shots=[S(None, X(MIS, 62.5), z=(1.0, 1.05)), S("Si sigues el olor", X(MIS, 78.0), z=(1.0, 1.05)), S("llegas a un tótem", X(MIS, 88.0), z=(1.0, 1.08))],
     sfx=[("w:aullidos", "riser", 0.3), ("w:te desmayas", "impact", 0.35)])
beat("La historia podría acabar ahí, pero por la zona de Key Lento hay carteles que preguntan por una especie de Pie Grande de los pantanos. Si los lees, aparece un contacto nuevo en tu teléfono: Kirk, que te propone quedar de noche para buscarlo. Hay hasta un movimiento con una teoría conspirativa sobre las aguas residuales: primero lo oyes en las noticias de la radio, y el autor de la guía tardó ochenta horas en dar con sus miembros.",
     mus=("tropical", 1), id="d07", cert="GUIA",
     shots=[S(None, X(MIS, 100.0), z=(1.0, 1.05)), S("por la zona de Key Lento", X(MIS, 104.0), z=(1.0, 1.05)),
            S("hay carteles", X(MIS, 107.6), z=(1.0, 1.1)), S("aparece un contacto", X(MIS, 115.5), z=(1.0, 1.05)),
            S("Hay hasta un movimiento", X(MIS, 204.0), z=(1.0, 1.05)), S("y el autor de la guía", X(MIS, 216.0), z=(1.0, 1.05))])
beat("Prueba cuatro: esta fuente de Capri, la Fuente de la Eterna Juventud, al sureste del centro del pueblo. Según la guía, beber de ella te mejora todas las estadísticas al instante. Eso sí, el cartel avisa que bebes bajo tu propia responsabilidad.",
     mus=("tropical", 1), id="d08", cert="GUIA",
     shots=[S(None, X(FUE, 1.0), prueba="PRUEBA 4", lado="defensa", vtitle="LA FUENTE DE LA ETERNA JUVENTUD"),
            S("Eso sí", X(FUE, 17.0))],
     sfx=[("w:Prueba cuatro", "stamp", 0.5), ("w:al instante", "chime", 0.4)])
beat("¡Objeción!, interrumpe la acusación. No todas esas misiones son tan inocentes.",
     mus=("noir", 2), id="d09",
     shots=[S(None, "g:cargo", kicker="LA ACUSACIÓN INTERRUMPE", txt="¡OBJECIÓN!", lado="acusacion")],
     sfx=[(0.05, "stamp", 0.6), ("w:¡Objeción!", "impact", 0.4)])
beat("Un influencer de Ocean Beach te mete en las campañas de su propia criptomoneda, y de paso te enseña los desafíos de acrobacias del mundo abierto. Y una vieja amiga de Lucía la invita a hacer entregas para un negocio muy raro, que hasta la guía describe como una mala idea.",
     mus=("noir", 1), id="d10", cert="GUIA",
     shots=[S(None, X(MIS, 345.0), z=(1.0, 1.05)), S("su propia criptomoneda", X(MIS, 372.0), z=(1.0, 1.05)),
            S("Y una vieja amiga", X(MIS, 404.0), z=(1.0, 1.05)), S("un negocio", X(MIS, 432.0), z=(1.0, 1.05))])
beat("Objeción aceptada: en GTA 6, hasta las buenas acciones pueden tener trampa. Pero también hay historias más humanas, como la de Yago, un aspirante a piloto de carreras callejeras que, según la guía, esconde mucho más de lo que parece.",
     mus=("synthwave", 1), id="d11", cert="GUIA",
     shots=[S(None, X(MIS, 300.0), z=(1.0, 1.05)), S("como la de Yago", X(MIS, 318.0), z=(1.0, 1.05)), S("según la guía", X(MIS, 330.0), z=(1.0, 1.05))])
beat("Y hay misterios que la guía ni siquiera resuelve. Si ves un auto abandonado junto a un motel, con un rastro de ropa que se mete en el bosque, ve a mirar… si te atreves.",
     mus=("noir", 1), id="d115", cert="GUIA",
     shots=[S(None, X(MIS, 474.5), z=(1.0, 1.05)), S("un rastro de ropa", X(MIS, 480.0), z=(1.0, 1.06))],
     sfx=[("w:si te atreves", "riser", 0.3)])

# ================================================================ SESIÓN 3 · LOS TESTIGOS
beat("Llamamos a los testigos. El primero es la propia Rockstar.",
     chapter=(3, "LOS TESTIGOS"), mus=("noir", 1), pre=1.4, id="t01",
     shots=[S(None, X(JET, 120.0), z=(1.0, 1.05))], sfx=[(0.0, "stamp", 0.45)])
beat("GTA 6 ya no deja hacer algunas cosas que sí estaban en entregas anteriores, como contratar a trabajadoras sexuales. En un comunicado recogido por la prensa, Rockstar explicó por qué. Eso sí, los clubes de striptease siguen ahí, y Jason y Lucía pueden ir juntos, como pareja.",
     mus=("noir", 1), id="t02", cert="PRENSA",
     shots=[S(None, X(MIS, 440.0), z=(1.0, 1.05)), S("En un comunicado", X(MIS, 452.0), z=(1.0, 1.05))])
beat("«Todo lo que hemos incluido en GTA 6 está ahí para apoyar el espíritu de la historia que queríamos contar». Y añadió que muchas cosas de juegos anteriores no están, pero que todo lo que sí está es necesario para lo que querían que sintieras en la historia de Jason y Lucía: una pareja.",
     mus=("noir", 1), id="t03",
     shots=[S(None, "g:testigo", name="ROCKSTAR GAMES", role="Comunicado sobre las funciones que no están en GTA 6",
              q="Todo lo que hemos incluido en GTA 6 está ahí para apoyar el espíritu de la historia que queríamos contar.", fuente="SHACKNEWS · RECOGIDO POR IGN DAILY FIX, 19/11/2026")],
     sfx=[(0.1, "paper", 0.4)])
beat("Segundo testigo: Rob Nelson, uno de los responsables de Rockstar North. En una entrevista con The Guardian le preguntaron si GTA 6 es el primero de la saga que fomenta la empatía.",
     mus=("noir", 1), id="t04",
     shots=[S(None, "g:testigo", name="ROB NELSON", role="Codirector de Rockstar North",
              q="¿Es el primer GTA que fomenta la empatía? Yo diría que sí.", fuente="ENTREVISTA EN THE GUARDIAN · RECOGIDA POR LA PRENSA")],
     sfx=[(0.1, "paper", 0.4)])
beat("Su respuesta fue: «Yo diría que sí». Y añadió que el juego ofrece formas de fomentarla, para quien quiera usarlas. Según la prensa que recogió la entrevista, eso no significa que el juego castigue a quien prefiere el caos.",
     mus=("noir", 1), id="t05", cert="PRENSA",
     shots=[S("para quien quiera", X(MIS, 420.0), z=(1.0, 1.05))])   # hasta ahí sigue en pantalla la tarjeta del testigo
beat("Y el tercer testigo es el propio juego. Este jugador recibe un disparo y muere.",
     mus=("tension", 1), id="t06", cert="PARTIDA",
     shots=[S(None, "g:cargo", kicker="TERCER TESTIGO", txt="EL PROPIO JUEGO", lado="testigo"),
            S("Este jugador", X(HOS, 0.0), card=True, prueba="TESTIGO 3", lado="testigo")],
     sfx=[("w:muere", "impact", 0.4)])
beat("Cuando despierta, está junto a la carretera, y en la esquina de la pantalla aparece el cargo, justo debajo del aviso de que se actualizó el mapa: mil ciento noventa y un dólares de hospital.",
     mus=("tension", 1), id="t07", cert="PARTIDA",
     shots=[S(None, X(HOS, 6.2), card=True),
            S("aparece el cargo", X(HOS, 13.45), card=True, card_zoom=(0.84, 0.17, 1.0, 0.47), zoom_at=0.3),
            S("mil ciento", "g:cover", kicker="LA FACTURA DEL HOSPITAL", lines=["1.191", "DÓLARES"], sub="Partida real · Video Pump")],
     sfx=[("w:mil ciento", "coin", 0.45)])
beat("En GTA 6, hasta morir sale caro. Y hay otra consecuencia que ya te explicamos en este canal: el perfil criminal, que te va poniendo una etiqueta según cómo juegas, de Profesional hasta Irredimible. Y si llegas a Irredimible, ya no hay vuelta atrás.",
     mus=("tension", 1), id="t08",
     shots=[S(None, X(TAN, 224.0), z=(1.0, 1.04)),
            S("el perfil criminal", "g:list", title="EL PERFIL CRIMINAL", subt="Lo explicamos en el canal: «Qué pasa al llegar a 6 estrellas»",
              items=["Profesional", "Curtido", "Violento", "Psicópata", ("Irredimible", R.RED)],
              cues=["el perfil", "una etiqueta", "según cómo", "de Profesional", "Irredimible"])],
     sfx=[("w:Irredimible", "glitch", 0.4)])

# ================================================================ SESIÓN 4 · ALEGATOS FINALES
beat("Alegato final de la acusación: GTA 6 te deja robar un tanque y un avión de combate, y aguantar seis estrellas en una persecución. Sigue llamándose Grand Theft Auto, que en inglés es el nombre del delito de robar vehículos.",
     chapter=(4, "ALEGATOS FINALES"), mus=("tension", 2), pre=1.4, id="f01", cert="PARTIDA",
     shots=[S(None, X(TAN, 177.0), z=(1.0, 1.06)), S("un avión de combate", X(JET, 155.8), z=(1.0, 1.06)),
            S("Sigue llamándose", X(TAN, 309.0), z=(1.0, 1.05))],
     sfx=[(0.0, "stamp", 0.45)])
beat("Alegato final de la defensa: GTA 6 te premia por arreglar la casa, por cuidar de tu pareja y hasta por sacar la basura. Y casi nada de lo que has visto es obligatorio. La relación con Lucía, el Focus de la basura y las estadísticas de la fuente se ganan sin disparar ni una bala.",
     mus=("tropical", 1), id="f02", cert="GUIA",
     shots=[S(None, X(CAS, 28.3), z=(1.0, 1.05)), S("Y casi nada", X(MIS, 178.0), z=(1.0, 1.05)),
            S("se ganan sin disparar", "g:cover", kicker="ALEGATO DE LA DEFENSA", lines=["SIN DISPARAR", "NI UNA BALA"])],
     sfx=[(0.0, "stamp", 0.45)])
beat("Antes del veredicto, repasemos las pruebas. La acusación presentó un tanque, un avión de combate, a una sheriff y un documento filtrado. La defensa, una casa arreglada, unas latas en el contenedor, varias misiones secundarias y una fuente.",
     mus=("noir", 1), id="f025",
     shots=[S(None, "g:marcador", title="LAS PRUEBAS", acu=["A · Tanque y seis estrellas", "B · Robo de un caza", "C · La sheriff de Miami-Dade", "D · Documento de China"],
              **{"def": ["1 · Arreglar la casa", "2 · Sacar la basura", "3 · Misiones secundarias", "4 · La fuente de Capri"]},
              cues=["un tanque", "un avión", "una sheriff", "un documento", "una casa", "unas latas", "varias misiones", "una fuente"])],
     sfx=[("w:un tanque", "pop", 0.3), ("w:una casa", "pop", 0.3)])
beat("Nuestra conclusión no es un veredicto. Que en GTA puedas elegir entre el caos y la vida tranquila no es nuevo: en GTA 5 también podías jugar al golf, al tenis o hacer yoga.",
     mus=("noir", 1), id="f03",
     shots=[S(None, X(MIS, 190.0), z=(1.0, 1.05)),
            S("no es nuevo", "g:list", title="EN GTA 5 YA PODÍAS", subt="Elegir la vida tranquila no es nuevo",
              items=["Jugar al golf", "Jugar al tenis", "Hacer yoga"], cues=["golf", "tenis", "yoga"])])
beat("Lo nuevo es que ahora el juego toma nota: de tu relación con Lucía, de tu perfil criminal, y hasta de lo que haces con una lata vacía.",
     mus=("noir", 1), id="f04",
     shots=[S(None, X(TAN, 32.0), z=(1.0, 1.05)),
            S("de tu relación", "g:list", title="AHORA EL JUEGO TOMA NOTA", subt="Lo nuevo de GTA 6",
              items=["Tu relación con Lucía", "Tu perfil criminal", "Lo que haces con una lata vacía"], cues=["relación con Lucía", "perfil criminal", "lata vacía"])],
     sfx=[("w:lata vacía", "pop", 0.4)])

# ================================================================ VEREDICTO Y CIERRE
beat("Así que te toca a ti. ¿GTA 6 es culpable de ser un juego de crímenes, o es inocente, porque en el fondo es un simulador de vida?",
     mus=("noir", 2), pre=0.6, id="v01",
     shots=[S(None, "g:veredicto", title="TU VEREDICTO", subt="¿Juego de crímenes o simulador de vida?", cues=["culpable", "inocente"],
              foot="ESCRÍBELO EN LOS COMENTARIOS")],
     sfx=[("w:culpable", "stamp", 0.5), ("w:inocente", "stamp", 0.5)])
beat("Escribe tu veredicto en los comentarios: culpable o inocente, y qué prueba te convenció. En este juicio no hay respuesta correcta, solo buenos argumentos. Y si todavía no viste cómo te vigila la policía de GTA 6, tienes ese video en el canal.",
     mus=("noir", 1), id="v02", shots=[])
beat("Y si quieres más GTA 6 contado de otra forma, suscríbete a Sal y Asfalto. Se levanta la sesión.",
     mus=("noir", 1), hold=0.6, id="v03",
     shots=[S(None, X(MIS, 186.0), z=(1.0, 1.05)), S("suscríbete", "g:subscribe")],
     sfx=[("w:suscríbete", "pop", 0.45), ("w:Se levanta", "stamp", 0.5)])
beat("", dur=20.0, mus=("noir", 1), id="end", shots=[S(None, "g:end")], trans="fade")

# ---------------------------------------------------------------- música original por bloque (como en gx.py)
def music_fn(total, beats_tl):
    segs = []
    for b, bd in zip(B, beats_tl):
        st, lv = b.get("mus", ("noir", 1))
        if segs and segs[-1]["style"] == st: segs[-1]["en"].append((bd["start"] - segs[-1]["t0"], lv))
        else: segs.append(dict(style=st, t0=bd["start"], en=[(0.0, lv)]))
    n = int(total * audio.SR); out = np.zeros((n, 2)); xf = 1.2
    for i, sg in enumerate(segs):
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        a0 = max(0.0, sg["t0"] - (xf / 2 if i else 0)); dur = (t1 - a0) + (xf / 2 if i + 1 < len(segs) else 0)
        en = [(max(0.0, tt + (sg["t0"] - a0)), lv) for tt, lv in sg["en"]]
        y = audio.compose(sg["style"], dur, energy=en, seed=6200 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "VIDEO_LARGO_3_GTA6_A_JUICIO"
for _d in ("trabajo", "trabajo/audio"):
    os.makedirs(os.path.join(_ROOT, FOLDER, _d), exist_ok=True)

VIDEO = dict(id="jz", folder=FOLDER, file="VIDEO_FINAL", res_dir="trabajo", theme="juicio",
             title="Llevamos GTA 6 a juicio: ¿juego de crímenes o simulador de vida?",
             format="Largo (16:9, 1920×1080, 30 fps) · gameplay real posterior al lanzamiento", music="noir", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55,
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="trabajo/audio/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.thumb_juicio(c)
