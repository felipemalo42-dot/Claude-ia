"""VIDEO_LARGO_GTA6 — «GTA 6 te está vigilando»: del testigo a las 6 estrellas y el perfil que no se borra.

Concepto (elegido entre 15, ver PROYECTO_DE_EDICION/INVESTIGACION_Y_CONCEPTO.md): seguir un delito en Vice City de
principio a fin con partidas reales grabadas por jugadores tras el lanzamiento (19/11/2026): el testigo, lo que sabe la
policía, una huida real de 5 estrellas, la escalada hasta la sexta estrella y el perfil criminal que no se borra.
Reglas: solo gameplay real posterior al lanzamiento (nada de tráileres, Extended Look, filtraciones ni recreaciones);
lo que Rockstar explicó antes del lanzamiento se dice «según Rockstar»; los mensajes del juego se muestran tal cual
(en inglés) con su traducción; sin escenas de misiones ni detalles de la historia.

Planos: S(ancla, fuente, **opciones) — el corte cae en la palabra `ancla` del beat (LEAD = 2 fotogramas antes).
  fuente = x:<ID>@<segundo> (gameplay del catálogo videos/gp_clips.json) · g:<gráfico propio>
"""
import os
import numpy as np
import audio
from videos import gx_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)

# gameplay (copias públicas en Internet Archive; créditos en pantalla y en FUENTES_Y_GAMEPLAYS.txt)
SIX = "Om4W6tYMF-0"      # IGN · «You Have to Become a Complete Psychopath to Get A 6 Star Wanted Level in GTA 6» (19/11/2026)
SAT = "gJyMGHxCKHU"      # GTAsatara · «GTA VI Police Investigation» (19/11/2026)
MIK = "ey0qks0aQ-c"      # MikeTheGoon · «GTA 6 - Ocean Beach Shootout + Five Star Escape» (19/11/2026), 4K HDR
ROP = "qbhJRtgCx30"      # IGN · guía de ropa y conjuntos (20/11/2026)
OPS = "eD5ndr0OMM0"      # IGN · «What Are Illegal Operations?» (19/11/2026)
FOC = "JHRVSzM2O2M"      # IGN · Short del modo Focus (20/11/2026), vertical
DET = "uMYUjOLOOVQ"      # IGN · Short de detalles (20/11/2026), vertical
def X(vid, t): return f"x:{vid}@{t}"
HUD = (0.965, 0.06, 3.0, 0.55)     # zoom a las estrellas (arriba a la derecha)
MSG = (0.125, 0.33, 2.5, 0.5)      # zoom a los mensajes del juego (arriba a la izquierda)
MSGBOX = (0.012, 0.258, 0.25, 0.372)    # recuadro de un mensaje de 3 líneas en la imagen original (0-1)
MSGBOX4 = (0.012, 0.258, 0.237, 0.40)   # mensaje de 4 líneas
HUDBOX = (0.862, 0.012, 0.992, 0.098)   # estrellas e iconos en la imagen original (0-1)

# ================================================================ GANCHO
beat("Este mensaje aparece en GTA 6 cuando ya es demasiado tarde. «Ahora tienes un nivel de búsqueda de 6 estrellas. Escapar es imposible, y la policía no se rendirá hasta darte caza».",
     section="GANCHO", mus=("tension", 2), pre=0.35, exag=0.62, id="gancho1", seed_off=1,
     shots=[S(None, X(SIX, 355.6), z=(1.0, 1.06)),
            S("«Ahora", X(SIX, 362.25), gamemsg="MENSAJE DEL JUEGO (EN INGLÉS)"),
            S("Escapar es imposible", X(SIX, 297.6), z=(1.0, 1.08)),
            S("y la policía no se rendirá", X(SIX, 392.5), z=(1.0, 1.06))],
     sfx=[(0.0, "riser", 0.35), ("w:«Ahora", "alarm", 0.30), ("w:Escapar", "hit", 0.35)])
beat("Y en esa misma prueba, el juego lanzó otro aviso todavía más serio: Lucía estaba a punto de quedar marcada para siempre.",
     mus=("tension", 2), exag=0.62, id="gancho2",
     shots=[S(None, X(SIX, 397.2), z=(1.0, 1.05)),
            S("Lucía estaba", "g:msgcard", en="Warning: Lucia is nearing irredeemable. Avoid extreme violence to prevent a lasting impact.")],
     sfx=[("w:otro aviso", "heartbeat", 0.45), ("w:Lucía estaba", "hit", 0.35)])
beat("Hoy seguimos un delito en Vice City desde el primer disparo hasta ese punto sin retorno. Qué ve un testigo, qué sabe la policía, cómo se pierde una persecución… y qué es lo único que el juego no te perdona.",
     mus=("tension", 2), exag=0.62, hold=0.2, id="gancho3",
     shots=[S(None, X(MIK, 24.2), z=(1.0, 1.06)),
            S("el primer disparo", X(SIX, 255.6), z=(1.0, 1.06)),
            S("ese punto sin retorno", X(SIX, 248.3), tr=("flash", 0.18)),
            S("Qué ve un testigo", X(SAT, 205.6), zoom=HUD, z0=2.2, tr=("whip", 0.22)),
            S("qué sabe la policía", X(SIX, 263.8), tr=("whip", 0.22)),
            S("cómo se pierde", X(MIK, 785.0), tr=("whip", 0.22)),
            S("lo único que el juego", "g:ladder", hi=4, title="PERFIL CRIMINAL", reveal=[0.0, 0.05, 0.1, 0.15, 0.2], lock=0.9, tr=("zoom", 0.25))],
     sfx=[("w:el primer disparo", "impact", 0.35), ("w:ese punto", "whoosh", 0.35), ("w:Qué ve", "whoosh", 0.3), ("w:qué sabe", "whoosh", 0.3),
          ("w:cómo se pierde", "whoosh", 0.3), ("w:no te perdona", "stamp", 0.45)])
beat("", dur=2.4, mus=("tension", 1), sfx=[(0.0, "logo", 0.9)], id="sting",
     shots=[S(None, "g:sting")], trans="flash")

# ================================================================ INTRODUCCIÓN
beat("Todo lo que vas a ver son partidas reales, grabadas por jugadores en los primeros días después del lanzamiento. Vamos a separar lo que se ve en pantalla de lo que Rockstar contó antes de que saliera el juego.",
     section="INTRODUCCIÓN", mus=("synthwave", 1), pre=1.0, id="intro1",
     # entra ya en la pausa tras la cortinilla (dt): sin segundo en negro; material tras el cambio de cámara del original (29,87 s)
     shots=[S(None, X(MIK, 29.9), z=(1.0, 1.05), dt=-0.972),
            S("grabadas por jugadores", "g:creators"),
            S("Vamos a separar", "g:legend", cues=["lo que se ve", "lo que Rockstar"])],
     sfx=[("w:grabadas", "pop", 0.35), ("w:lo que se ve", "pop", 0.4), ("w:lo que Rockstar", "pop", 0.4)])
beat("Y una promesa: cero spoilers de la historia. Solo cómo funciona el juego por dentro.",
     mus=("synthwave", 1), id="intro2",
     shots=[S(None, "g:nospoil"), S("Solo cómo funciona", X(SAT, 252.0), z=(1.0, 1.06))],
     sfx=[("w:cero spoilers", "stamp", 0.45)])
beat("Quédate hasta el final, porque vas a ver cómo alguien terminó la historia con más de 300 enemigos muertos… y el juego todavía lo considera un profesional.",
     mus=("synthwave", 1), hold=0.2, id="intro3",
     shots=[S(None, X(MIK, 430.0), z=(1.0, 1.06)), S("más de 300", "g:teaser", cues=["y el juego"])],
     sfx=[("w:más de 300", "tick", 0.45), ("w:un profesional", "ding", 0.35)])

# ================================================================ 1 · EL TESTIGO
beat("Primera regla: sin testigos, no hay estrellas. Según Rockstar, la policía solo se entera de un delito si alguien lo ve, o si salta una alarma.",
     section="1 · EL TESTIGO", chapter=(1, "EL TESTIGO"), mus=("tension", 1), pre=1.6, id="c1a",
     cert="ROCKSTAR",
     shots=[S(None, X(SAT, 82.3), z=(1.0, 1.08)),
            S("Según Rockstar", "g:witness", cues=["alguien lo ve", "salta una alarma"])],
     sfx=[(0.0, "whoosh", 0.35), ("w:alguien lo ve", "pop", 0.4), ("w:salta una alarma", "alarm", 0.25)])
beat("Mira esta partida. Un tiroteo en un patio privado, escondido detrás de una cerca. Arriba a la derecha aparecen dos estrellas, pero vacías por dentro. Y el juego muestra este mensaje: «La policía no te ha identificado. Mantén un perfil bajo para no llamar la atención».",
     mus=("tension", 1), id="c1b", seed_off=1,
     cert="PARTIDA",
     shots=[S(None, X(SAT, 64.6), z=(1.0, 1.06)),
            S("Un tiroteo", X(SAT, 120.9), z=(1.04, 1.1)),
            S("escondido detrás", X(SAT, 70.4), z=(1.0, 1.06)),
            S("Arriba a la derecha", X(SAT, 196.0), zoom=HUD, hl_src=HUDBOX, hl_at=0.6),
            S("Y el juego muestra", X(SAT, 183.5), zoom=MSG, z0=2.5, hl_src=MSGBOX, hl_at=0.3),
            S("«La policía no te ha", "g:msgcard", en="You weren't identified by the cops. ☆ Keep a low profile to avoid any attention.")],
     sfx=[("w:Un tiroteo", "impact", 0.3), ("w:Arriba", "pop", 0.4), ("w:este mensaje", "pop", 0.4)])
beat("Eso es una estrella hueca: la policía sabe que algo pasó, pero no sabe quién fue.",
     mus=("tension", 1), id="c1c",
     cert="PARTIDA", shots=[S(None, "g:hollow", cues=["la policía sabe", "pero no sabe"])], sfx=[(0.0, "pop", 0.4)])
beat("¿Y qué hace el jugador? Lo más inteligente: recoge lo que necesita, sale caminando sin prisa y se aleja. Sin correr, sin disparar, sin llamar la atención. Un par de minutos después, las estrellas se apagan solas.",
     mus=("tension", 1), id="c1d",
     cert="PARTIDA",
     shots=[S(None, X(SAT, 166.6), z=(1.0, 1.05)),
            S("sale caminando", X(SAT, 223.0), z=(1.0, 1.05)),
            S("Sin correr", X(SAT, 262.0), z=(1.0, 1.06)),
            S("Un par de minutos", X(SAT, 336.0), zoom=HUD, sync=("se apagan", 339.6, 0.25), hl_src=HUDBOX, hl_at=0.5)],
     sfx=[("w:se apagan", "pop", 0.35)])
beat("Pero mira lo que pasa cuando vuelve en su auto hacia la zona, un rato después. Aparece una estrella roja con dos iconos: una silueta y un auto. El juego no explica por qué, pero esos iconos tienen un significado muy concreto.",
     mus=("tension", 1), id="c1d2",
     cert="PARTIDA",
     shots=[S(None, X(SAT, 586.0), z=(1.0, 1.05)),
            S("Aparece una estrella", X(SAT, 604.0), zoom=HUD, sync=("Aparece una estrella", 608.1, 0.35), hl_src=HUDBOX, hl_at=0.8),
            S("El juego no explica", X(SAT, 646.2), z=(1.0, 1.06))],
     sfx=[("w:estrella roja", "alarm", 0.25)])
beat("Ojo, porque el lugar del crimen tiene memoria. Según las guías publicadas estos días, una mancha de sangre puede seguir en el mismo sitio varios días después, dentro del juego. Y si hay muchos disparos en una zona con gente, es fácil que algún vecino llame a la policía.",
     mus=("tension", 1), id="c1e",
     cert="GUIAS",
     shots=[S(None, X(SAT, 700.0), z=(1.0, 1.06)),
            S("una mancha de sangre", X(DET, 9.8), vtitle="LA SANGRE SE QUEDA DÍAS EN EL MISMO SITIO", nocut=True),
            S("Y si hay muchos disparos", X(OPS, 48.3), z=(1.0, 1.06)),
            S("algún vecino llame", X(MIK, 242.2), z=(1.0, 1.05))],
     sfx=[("w:mancha", "pop", 0.35), ("w:muchos disparos", "impact", 0.25)])

# ================================================================ 2 · LO QUE SABE LA POLICÍA
beat("Ahora, el siguiente paso. Cuando la policía sí te identifica, las estrellas se llenan, y debajo aparecen unos iconos rojos.",
     section="2 · LO QUE SABE LA POLICÍA", chapter=(2, "LO QUE SABE LA POLICÍA"), mus=("electro", 1), pre=1.6, id="c2a",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 256.5), z=(1.0, 1.06)),
            S("las estrellas se llenan", X(SIX, 47.9), tr=("zoom", 0.2))],
     sfx=[("w:se llenan", "pop", 0.4), ("w:iconos rojos", "pop", 0.4)])
beat("En las partidas de estos días se ven cuatro: una percha, una silueta, un auto y una pistola. Según Rockstar, la policía puede saber cómo eres, qué ropa llevas, qué vehículo usas y si Jason y Lucía van juntos.",
     mus=("electro", 1), id="c2b",
     shots=[S(None, "g:icons", step=0, cert="PARTIDA", cues=["una percha", "una silueta", "un auto", "una pistola"]),
            S("Según Rockstar", "g:icons", step=1, cert="ROCKSTAR", cues=["cómo eres", "qué ropa", "qué vehículo", "si Jason"])],
     sfx=[("w:una percha", "pop", 0.35), ("w:una silueta", "pop", 0.35), ("w:un auto", "pop", 0.35), ("w:una pistola", "pop", 0.35), ("w:si Jason", "ding", 0.3)])
beat("Funciona como una ficha policial en directo. Y lo mejor es que puedes ir borrando datos de esa ficha.",
     mus=("electro", 1), id="c2c",
     shots=[S(None, "g:ficha", cues=["ir borrando"])], sfx=[(0.0, "paper", 0.45), ("w:ir borrando", "snap", 0.4)])
beat("Cuando tienes estrellas, se envía un aviso a todas las patrullas con tu descripción y con la ropa que llevas puesta. Por eso, cambiarte de ropa te ayuda a perderlos.",
     mus=("electro", 1), id="c2d",
     cert="GUIAS",
     shots=[S(None, X(SIX, 278.8), zoom=(0.95, 0.07, 2.6, 0.5), hl_src=HUDBOX, hl_at=0.7),
            S("con la ropa que llevas", X(ROP, 108.3), z=(1.0, 1.06)),
            S("Por eso, cambiarte", X(ROP, 100.5), z=(1.0, 1.06))],
     sfx=[("w:todas las patrullas", "alarm", 0.2)])
beat("No hace falta volver a casa: puedes guardar hasta 5 conjuntos en tu vehículo personal y cambiarte ahí mismo. Y si no te da tiempo, quitarte la gorra o los lentes de sol también enfría un poco la búsqueda.",
     mus=("electro", 1), id="c2e",
     cert="GUIAS",
     shots=[S(None, X(ROP, 94.3), z=(1.0, 1.05)),
            S("hasta 5 conjuntos", X(ROP, 134.5), z=(1.0, 1.06), label="HASTA 5 CONJUNTOS"),
            S("quitarte la gorra", X(ROP, 145.3), z=(1.0, 1.06)),
            S("enfría un poco", X(MIK, 160.0), z=(1.0, 1.05))],
     sfx=[("w:5 conjuntos", "pop", 0.4)])
beat("Otra herramienta es el modo Focus. Mientras manejas, marca a los policías en azul, para que sepas por dónde no pasar.",
     mus=("electro", 1), id="c2f",
     cert="GUIAS",
     shots=[S(None, X(FOC, 0.6), vtitle="EL MODO FOCUS"),
            S("Mientras manejas", X(FOC, 18.0), vtitle="POLICÍAS EN AZUL MIENTRAS MANEJAS"),
            S("para que sepas", X(SAT, 620.5), z=(1.0, 1.05))],
     sfx=[(0.0, "whoosh", 0.35), ("w:en azul", "pop", 0.4)])
beat("Y una pista que dio Rockstar antes del lanzamiento: con 3 estrellas o más en la ciudad, escapar en un auto normal es casi imposible. Lo mejor es dejarlo y huir a pie, por callejones y por encima de las cercas.",
     mus=("electro", 2), id="c2g",
     cert="ROCKSTAR",
     shots=[S(None, X(MIK, 545.0), z=(1.0, 1.05)),
            S("escapar en un auto", X(MIK, 545.0), cont=True, z=(1.1, 1.16), f=(0.5, 0.55)),
            S("Lo mejor es dejarlo", X(MIK, 698.5), z=(1.0, 1.06)),
            S("por callejones", X(MIK, 250.0), z=(1.0, 1.05)),
            S("por encima de las cercas", X(MIK, 354.2), z=(1.0, 1.06))],
     sfx=[("w:casi imposible", "hit", 0.3)])
beat("¿De verdad funciona? Vamos a comprobarlo con una huida real.",
     mus=("electro", 2), hold=0.2, id="c2h",
     shots=[S(None, X(MIK, 733.5), z=(1.0, 1.06)),
            S("una huida real", X(MIK, 797.0), big=["UNA HUIDA", "REAL"], tr=("whip", 0.22))],
     sfx=[("w:una huida real", "riser", 0.4)])

# ================================================================ 3 · UNA HUIDA REAL
beat("Esta partida empieza en calma: un paseo en bicicleta junto a la playa de Vice City.",
     section="3 · UNA HUIDA REAL", chapter=(3, "UNA HUIDA REAL"), mus=("trap26", 1), pre=1.6, id="c3a",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 18.6), z=(1.0, 1.05)), S("un paseo en bicicleta", X(MIK, 45.2), z=(1.0, 1.05))],
     sfx=[(0.0, "whoosh", 0.35)])
beat("Hasta que el jugador empieza a saquear los autos estacionados en la avenida. Llega una patrulla, y en segundos la calle se convierte en un tiroteo.",
     mus=("trap26", 2), id="c3b",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 91.5), z=(1.0, 1.06)),
            S("los autos estacionados", X(MIK, 114.0), z=(1.0, 1.06)),
            S("Llega una patrulla", X(MIK, 181.0), z=(1.0, 1.05)),
            S("se convierte en un tiroteo", X(MIK, 176.3), z=(1.04, 1.1), tr=("flash", 0.15))],
     sfx=[("w:Llega una patrulla", "alarm", 0.3), ("w:tiroteo", "impact", 0.35)])
beat("La búsqueda sube sin parar. Se refugia en un hotel, sube hasta el bar de la azotea y resiste desde arriba.",
     mus=("trap26", 2), id="c3c",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 252.0), zoom=HUD, hl_src=HUDBOX, hl_at=0.5),
            S("Se refugia en un hotel", X(MIK, 375.2), z=(1.0, 1.06)),
            S("sube hasta el bar", X(MIK, 379.4), z=(1.0, 1.08)),
            S("resiste desde arriba", X(MIK, 426.0), z=(1.0, 1.06))],
     sfx=[("w:sube sin parar", "riser", 0.3), ("w:la azotea", "pop", 0.35)])
beat("Cuando baja, toma una camioneta y escapa por la avenida. Pero en el aire ya lo espera un helicóptero. Entonces se sube a un vehículo militar y sigue huyendo.",
     mus=("trap26", 2), id="c3d",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 528.6), z=(1.0, 1.05)),
            S("y escapa por la avenida", X(MIK, 533.6), z=(1.0, 1.05)),
            S("un helicóptero", X(MIK, 585.6), z=(1.0, 1.06)),
            S("un vehículo militar", X(MIK, 638.2), z=(1.0, 1.05)),
            S("y sigue huyendo", X(MIK, 651.0), z=(1.0, 1.05))],
     sfx=[("w:un helicóptero", "whoosh", 0.35), ("w:vehículo militar", "hit", 0.35)])
beat("Y aquí viene la clave. No se queda en un vehículo que todo el mundo está buscando. Lo abandona y escapa a pie: callejones, patios, arbustos… hasta la orilla del mar, entre los bañistas.",
     mus=("trap26", 2), id="c3e",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 666.0), z=(1.0, 1.05)),
            S("Lo abandona", X(MIK, 692.8), z=(1.0, 1.06)),
            S("callejones", X(MIK, 719.0), z=(1.0, 1.05)),
            S("hasta la orilla del mar", X(MIK, 779.0), z=(1.0, 1.05)),
            S("entre los bañistas", X(MIK, 787.6), z=(1.0, 1.06))],
     sfx=[("w:Y aquí viene la clave", "riser", 0.3), ("w:callejones", "whoosh", 0.25), ("w:patios", "whoosh", 0.25), ("w:arbustos", "whoosh", 0.25)])
beat("Desde que llegó la primera patrulla han pasado más de 10 minutos de partida. Y ya lejos del tiroteo, las estrellas se vuelven rojas, y el juego avisa: «La policía te está buscando y tiene tu descripción».",
     mus=("trap26", 1), id="c3f",
     cert="PARTIDA",
     shots=[S(None, X(MIK, 803.0), z=(1.0, 1.05), timer="+10 MIN"),
            S("las estrellas se vuelven rojas", X(MIK, 829.0), zoom=HUD, sync=("rojas", 833.3, 0.1), hl_src=HUDBOX, hl_at=0.6),
            S("y el juego avisa", X(MIK, 834.0), zoom=MSG, sync=("avisa", 835.6, 0.2), hl_src=MSGBOX, hl_at=0.6, gamemsg="MENSAJE DEL JUEGO (EN INGLÉS)")],
     sfx=[(0.0, "tick", 0.4), ("w:rojas", "alarm", 0.25)])
beat("Fíjate en la diferencia. Escapar de la persecución no es lo mismo que perder la búsqueda. Las estrellas rojas siguen ahí: ya no te ven, pero siguen buscando a alguien que se parezca a ti.",
     mus=("trap26", 1), id="c3g",
     shots=[S(None, "g:split", cues=["Escapar de la persecución", "no es lo mismo", "perder la búsqueda"]), S("Las estrellas rojas siguen", X(MIK, 846.0), cont=True, zoom=HUD, cert="PARTIDA"),
            S("que se parezca a ti", X(MIK, 852.5), z=(1.0, 1.08), cert="PARTIDA")],
     sfx=[("w:no es lo mismo", "pop", 0.4)])
beat("Por eso las estrellas cambian de color: huecas cuando no saben quién eres, blancas mientras te persiguen y rojas cuando te pierden de vista, pero siguen buscándote.",
     mus=("trap26", 1), hold=0.2, id="c3h",
     cert="PARTIDA", shots=[S(None, "g:stars", cues=["huecas", "blancas", "rojas"]), S("pero siguen buscándote", X(MIK, 746.0), z=(1.0, 1.06))],
     sfx=[("w:huecas", "pop", 0.35), ("w:blancas", "pop", 0.35), ("w:rojas", "pop", 0.35)])

# ================================================================ 4 · DE UNA A CINCO ESTRELLAS
beat("Ahora, la escalada. ¿Qué hace falta para subir de nivel?",
     section="4 · DE UNA A CINCO ESTRELLAS", chapter=(4, "DE UNA A CINCO ESTRELLAS"), mus=("electro", 2), pre=1.6, id="c4a",
     shots=[S(None, "g:meter", lvl=0, title="LA ESCALADA", note="¿QUÉ HACE FALTA?", note_at=0.6)], sfx=[(0.0, "riser", 0.35)])
beat("En otra partida, el jugador se mete en el aeropuerto internacional de Vice City, atraviesa las barreras y se sube a un avión de carga. Antes de llegar a la pista ya tiene 4 estrellas, sin haber matado a nadie.",
     mus=("electro", 2), id="c4b",
     cert="PARTIDA",
     shots=[S(None, X(SIX, 128.3), z=(1.0, 1.06)),
            S("atraviesa las barreras", X(SIX, 135.4), z=(1.0, 1.06)),
            S("se sube a un avión de carga", X(SIX, 142.2), z=(1.0, 1.05)),
            S("Antes de llegar a la pista", X(SIX, 144.93), z=(1.0, 1.05)),
            S("ya tiene 4 estrellas", X(SIX, 145.0), cont=True, zoom=HUD, z0=1.6, hl_src=HUDBOX, hl_at=0.3),
            S("sin haber matado", X(SIX, 148.3), z=(1.0, 1.05), dt=-0.12)],
     sfx=[("w:las barreras", "hit", 0.35), ("w:4 estrellas", "pop", 0.45)])
beat("Y en cuanto despega, aparecen aviones de combate a su lado para interceptarlo.",
     mus=("electro", 2), id="c4c",
     cert="PARTIDA",
     shots=[S(None, X(SIX, 148.3), cont=True, z=(1.0, 1.05)), S("aviones de combate", X(SIX, 174.0), z=(1.0, 1.08))],
     sfx=[("w:aviones de combate", "whoosh", 0.4)])
beat("No siempre sale bien: chocar con uno de esos aviones, o destrozar el tren de aterrizaje contra las escaleras de embarque, termina la prueba antes de tiempo.",
     mus=("electro", 2), id="c4c2",
     cert="GUIAS",
     shots=[S(None, X(SIX, 181.0), z=(1.0, 1.05)),
            S("chocar con uno", X(SIX, 187.5)),
            S("o destrozar el tren", X(SIX, 192.0), z=(1.0, 1.06))],
     sfx=[("w:chocar", "impact", 0.4)])
beat("Con 5 estrellas llega todo lo demás: vehículos blindados, todoterrenos, helicópteros y, como en los juegos anteriores, tanques.",
     mus=("electro", 2), id="c4d",
     cert="GUIAS",
     shots=[S(None, X(SIX, 266.0), z=(1.0, 1.05)),
            S("vehículos blindados", X(SIX, 260.0), z=(1.0, 1.06)),
            S("todoterrenos", X(SIX, 294.0), z=(1.0, 1.06)),
            S("helicópteros", X(MIK, 592.0), z=(1.0, 1.05)),
            S("tanques", "g:meter", lvl=5, title="CON 5 ESTRELLAS", note="+ TANQUES", note_at=0.2, cert="PRENSA", sub="Dato de PC Gamer (18/11/2026)")],
     sfx=[("w:vehículos blindados", "hit", 0.3), ("w:todoterrenos", "hit", 0.3), ("w:helicópteros", "hit", 0.3), ("w:tanques", "stamp", 0.4)])
beat("Pero hay dos datos que muchos jugadores no conocen. El primero: en la historia principal nunca vas a pasar de 5 estrellas. Las misiones más intensas te llevan hasta ahí, y nada más.",
     mus=("electro", 1), id="c4e",
     cert="GUIAS",
     shots=[S(None, X(SIX, 270.0), z=(1.0, 1.05)),
            S("El primero", "g:meter", lvl=5, lock6=True, title="HISTORIA PRINCIPAL", note="MÁXIMO: 5 ESTRELLAS", cues=["nunca vas a pasar"]),
            S("Las misiones más intensas", X(SIX, 236.2), z=(1.0, 1.06))],
     sfx=[("w:nunca vas a pasar", "stamp", 0.45)])
beat("El segundo: al terminar la historia se desbloquea un truco que sube tu nivel de búsqueda al instante… pero se queda en 5. La sexta estrella siempre tienes que ganártela tú.",
     mus=("electro", 1), hold=0.2, id="c4f",
     cert="GUIAS",
     shots=[S(None, "g:meter", lvl=5, lock6=True, title="EL TRUCO DE BÚSQUEDA", note="TAMBIÉN SE QUEDA EN 5", cues=["se queda en 5"]),
            S("La sexta estrella", X(SIX, 330.3), z=(1.0, 1.06))],
     sfx=[("w:se queda en 5", "stamp", 0.45), ("w:La sexta estrella", "riser", 0.35)])

# ================================================================ 5 · LA SEXTA ESTRELLA
beat("Y ganársela cuesta. Robar un avión no basta. Para la sexta hace falta destrucción masiva y muchísimas bajas, sobre todo de policías.",
     section="5 · LA SEXTA ESTRELLA", chapter=(5, "LA SEXTA ESTRELLA"), mus=("tension", 2), pre=1.6, id="c5a",
     cert="GUIAS",
     shots=[S(None, X(SIX, 200.0), z=(1.0, 1.05)),
            S("Robar un avión no basta", X(SIX, 208.0), z=(1.0, 1.05)),
            S("destrucción masiva", X(SIX, 320.6), z=(1.0, 1.06)),
            S("sobre todo de policías", X(SIX, 283.5), z=(1.0, 1.05))],
     sfx=[("w:destrucción", "impact", 0.4)])
beat("En las pruebas publicadas estos días, unos la consiguieron tras 5 o 10 minutos de caos en la playa. Otros, robando un tanque en una base militar y destruyendo otros tanques y vehículos.",
     mus=("tension", 2), id="c5b",
     cert="PRENSA",
     shots=[S(None, X(SIX, 336.5), z=(1.0, 1.05), cert="GUIAS"),
            S("Otros, robando un tanque", "g:quote", q="Robamos un tanque en una base militar y destruimos otros tanques y vehículos", who="PC Gamer · guía de las 6 estrellas (18/11/2026)")],
     sfx=[("w:tanque", "hit", 0.35)])
beat("Y no es fácil sobrevivir: la policía apunta a las ruedas, te rodea, y la pantalla de muerte aparece una y otra vez.",
     mus=("tension", 2), id="c5c",
     cert="GUIAS",
     shots=[S(None, X(MIK, 595.5), z=(1.0, 1.05)),
            S("te rodea", X(SIX, 342.7), z=(1.0, 1.05)),
            S("la pantalla de muerte", X(SIX, 384.25)),
            S("una y otra vez", X(SIX, 189.3), tr=("flash", 0.15))],
     sfx=[("w:pantalla de muerte", "impact", 0.4), ("w:una y otra", "impact", 0.35)])
beat("Hasta que, por fin, aparece este mensaje: «Ahora tienes un nivel de búsqueda de 6 estrellas. Escapar es imposible, y la policía no se rendirá hasta darte caza».",
     mus=("tension", 2), id="c5d",
     cert="PARTIDA",
     shots=[S(None, X(SIX, 444.0), z=(1.0, 1.04), sync=("este mensaje", 446.35, 0.0)),
            S("«Ahora tienes", "g:msgcard", en="You now have a 6-star wanted level. Escape is impossible, and the cops won't give up until you're hunted down."),
            S("Escapar es imposible", X(SIX, 327.0)),
            S("no se rendirá", X(SIX, 369.85), z=(1.0, 1.05))],
     sfx=[("w:este mensaje", "alarm", 0.3), ("w:Escapar", "hit", 0.35)])
beat("No es una exageración. Con 6 estrellas ya no hay forma de bajar el nivel de búsqueda. Puedes correr, pero no esconderte. La única salida es morir.",
     mus=("tension", 1), id="c5e",
     cert="GUIAS",
     shots=[S(None, X(SIX, 352.0), z=(1.0, 1.05)),
            S("Con 6 estrellas", X(SIX, 344.3), z=(1.0, 1.05)),
            S("Puedes correr", X(SIX, 306.6), z=(1.0, 1.06)),
            S("La única salida es morir", X(SIX, 302.7), tr=("flash", 0.15))],
     sfx=[("w:morir", "impact", 0.45)])
beat("Y ya hay quien propone un reto: ver quién aguanta más tiempo vivo con 6 estrellas. Por eso, el consejo es muy simple: guarda la partida antes de intentarlo.",
     mus=("tension", 1), id="c5f",
     cert="GUIAS", shots=[S(None, "g:record"), S("guarda la partida", "g:save")],
     sfx=[(0.0, "tick", 0.4), ("w:guarda la partida", "ding", 0.4)])
beat("Porque al morir, las estrellas se reinician. Pero hay algo que no se reinicia.",
     mus=("tension", 1), hold=0.5, music_stop=2.0, id="c5g",
     shots=[S(None, "g:meter", lvl=6, reset=True, title="AL MORIR", note="LAS ESTRELLAS VUELVEN A CERO", cues=["se reinician"]),
            S("Pero hay algo", "g:ladder", hi=4, title="¿QUÉ NO SE REINICIA?", reveal=[9, 9, 9, 9, 0.2], tr=("dip", 0.35))],
     sfx=[("w:Pero hay algo", "heartbeat", 0.5)])

# ================================================================ 6 · EL PERFIL CRIMINAL
beat("Se llama perfil criminal, y trabaja en segundo plano todo el tiempo, aunque no tengas ni una sola estrella.",
     section="6 · EL PERFIL CRIMINAL", chapter=(6, "EL PERFIL CRIMINAL"), mus=("mystery", 1), pre=1.6, id="c6a",
     cert="PRENSA",
     shots=[S(None, "g:ladder", title="PERFIL CRIMINAL", sub="Funciona aunque no tengas estrellas"),
            S("aunque no tengas", X(SAT, 434.0), z=(1.0, 1.05), cert="PARTIDA")],
     sfx=[(0.0, "whoosh", 0.35)])
beat("Tiene 5 niveles: Profesional, Curtido, Violento, Psicópata e Irredimible. Y Jason y Lucía tienen cada uno el suyo.",
     mus=("mystery", 1), id="c6b",
     cert="PRENSA",
     shots=[S(None, "g:ladder", title="5 NIVELES", cues=["Profesional", "Curtido", "Violento", "Psicópata", "Irredimible"], reveal_cues=True),
            S("Y Jason y Lucía", "g:ladder", mode="duo", title="UNO PARA CADA UNO", duo_at=0.3, reveal=[0, 0, 0, 0, 0])],
     sfx=[("w:Profesional", "pop", 0.3), ("w:Curtido", "pop", 0.3), ("w:Violento", "pop", 0.3), ("w:Psicópata", "pop", 0.3), ("w:Irredimible", "pop", 0.35)])
beat("¿De qué depende? Casi por completo, de a cuánta gente matas. Profesional es el que no deja rastro: usa la violencia justa, deja a sus enemigos fuera de combate en lugar de matarlos y procura pasar desapercibido.",
     mus=("mystery", 1), id="c6c", seed_off=1,
     cert="PRENSA",
     shots=[S(None, X(MIK, 436.5), z=(1.0, 1.06)),
            S("Profesional es", "g:ladder", hi=0, reveal=[0, 0, 0, 0, 0], notes={0: "Violencia justa · fuera de combate · sin ser visto"}, note_at={0: 0.4}),
            S("procura pasar desapercibido", X(SAT, 656.0), z=(1.0, 1.06))],
     sfx=[("w:Profesional es", "pop", 0.35)])
beat("Curtido mata enemigos sin pensarlo mucho, y no le importa que lo vean. Violento ignora las opciones no letales y dispara también a policías y civiles.",
     mus=("mystery", 1), id="c6c2",
     cert="PRENSA",
     shots=[S(None, "g:ladder", hi=1, reveal=[0, 0, 0, 0, 0], notes={1: "Mata enemigos · no le importa que lo vean"}, note_at={1: 0.3}),
            S("Violento ignora", "g:ladder", hi=2, reveal=[0, 0, 0, 0, 0], notes={2: "Sin opciones no letales · policías y civiles"}, note_at={2: 0.3})],
     sfx=[(0.0, "pop", 0.3), ("w:Violento", "pop", 0.3)])
beat("Y Psicópata mata a muchos policías, ataca a civiles indefensos y hasta a mascotas y animales domésticos. Eso sí: cazar no cuenta.",
     mus=("mystery", 1), id="c6d",
     cert="PRENSA",
     shots=[S(None, "g:ladder", hi=3, reveal=[0, 0, 0, 0, 0], notes={3: "Muchos policías · civiles indefensos · mascotas"}, note_at={3: 0.3}),
            S("Eso sí: cazar no cuenta", "g:ladder", hi=3, reveal=[0, 0, 0, 0, 0], notes={3: "LA CAZA NO CUENTA"}, note_at={3: 0.1})],
     sfx=[(0.0, "pop", 0.3), ("w:cazar no cuenta", "stamp", 0.4)])
beat("El propio juego te lo advierte con sus consejos. Uno dice: «La conducta extremadamente violenta te acercará al perfil de Psicópata».",
     mus=("mystery", 1), id="c6e",
     cert="PARTIDA",
     shots=[S(None, X(ROP, 155.1), zoom=MSG, z0=1.0, hl_src=MSGBOX, hl_at=0.8, gamemsg="CONSEJO DEL JUEGO (EN INGLÉS)"),
            S("«La conducta", "g:msgcard", en="Extremely violent behavior will contribute toward a psycho criminal profile.")],
     sfx=[("w:Uno dice", "pop", 0.4)])
beat("Y otro aclara algo que cambia la forma de jugar: «Tener un nivel de búsqueda no afecta a tu perfil criminal, pero sí cómo decidas tratar a la policía».",
     mus=("mystery", 1), id="c6f",
     cert="PARTIDA",
     shots=[S(None, X(ROP, 160.4), zoom=MSG, z0=1.0, hl_src=MSGBOX4, hl_at=0.8, gamemsg="CONSEJO DEL JUEGO (EN INGLÉS)"),
            S("«Tener un nivel", "g:msgcard", en="Getting a wanted level doesn't affect your criminal profile, but how you choose to deal with the cops will.")],
     sfx=[("w:cambia la forma", "pop", 0.4)])
beat("Aquí entra otra vez el modo Focus. Al apuntar, marca puntos amarillos para herir o desarmar, y puntos rojos para matar, como la cabeza o el corazón.",
     mus=("mystery", 2), id="c6g",
     cert="GUIAS",
     shots=[S(None, X(FOC, 26.0), vtitle="MODO FOCUS AL APUNTAR"),
            S("puntos rojos", X(FOC, 30.6), cont=True, vtitle="AMARILLO: HERIR · ROJO: MATAR")],
     sfx=[("w:puntos amarillos", "pop", 0.35), ("w:puntos rojos", "pop", 0.35)])
beat("Cada nivel tiene su recompensa. En Profesional y en Curtido, dejar a alguien fuera de combate o tener un buen gesto con la gente te recarga el Focus. En Violento y en Psicópata, lo recargan los disparos a la cabeza.",
     mus=("mystery", 2), id="c6h",
     cert="PRENSA", shots=[S(None, "g:bonus", cues=["En Profesional", "En Violento"]), S("los disparos a la cabeza", X(SIX, 459.5), z=(1.0, 1.06), cert="PARTIDA")],
     sfx=[("w:En Profesional", "pop", 0.35), ("w:En Violento", "pop", 0.35)])
beat("Pero hay un precio: siendo Psicópata, ya no puedes rendirte ante la policía.",
     mus=("mystery", 2), hold=0.2, id="c6i",
     cert="PRENSA", shots=[S(None, "g:ladder", hi=3, reveal=[0, 0, 0, 0, 0], cues=["no puedes rendirte"], nosurrender_cue=True)],
     sfx=[("w:no puedes rendirte", "stamp", 0.45)])

# ================================================================ 7 · LA ETIQUETA QUE NO SE BORRA
beat("Y llegamos al último nivel. Si pasas demasiado tiempo como Psicópata, te conviertes en Irredimible.",
     section="7 · LA ETIQUETA QUE NO SE BORRA", chapter=(7, "LA ETIQUETA QUE NO SE BORRA"), mus=("tension", 1), pre=1.6, id="c7a",
     cert="PRENSA", shots=[S(None, "g:ladder", hi=[3, 4], reveal=[0, 0, 0, 0, 0], cues=["Irredimible"], crack_cue=True)],
     sfx=[("w:Irredimible", "glitch", 0.4)])
beat("Entre los otros cuatro niveles puedes subir y bajar durante toda la partida. Pero este es permanente.",
     mus=("tension", 1), id="c7b",
     cert="PRENSA", shots=[S(None, "g:ladder", hi=[0, 1, 2, 3], reveal=[0, 0, 0, 0, 0], cues=["permanente"], lock_cue=True)],
     sfx=[("w:permanente", "stamp", 0.5)])
beat("Por suerte, el juego avisa antes. Este mensaje apareció en plena prueba de las 6 estrellas: «Atención: Lucía está cerca de volverse Irredimible. Evita la violencia extrema para no causar un efecto duradero».",
     mus=("tension", 2), id="c7c", seed_off=1,
     cert="PARTIDA",
     shots=[S(None, X(SIX, 408.1), z=(1.0, 1.05)),
            S("Este mensaje apareció", X(SIX, 412.4), z=(1.0, 1.05)),
            S("«Atención", X(SIX, 403.1), gamemsg="MENSAJE DEL JUEGO (EN INGLÉS)"),
            S("Evita la violencia", "g:msgcard", en="Warning: Lucia is nearing irredeemable. Avoid extreme violence to prevent a lasting impact.")],
     sfx=[("w:«Atención", "alarm", 0.3)])
beat("¿Qué efecto? Rockstar solo ha dicho que ser Irredimible tendrá un impacto duradero en Jason y Lucía. Las guías hablan de consecuencias en la historia y en cómo te trata la gente, pero los detalles todavía no están claros.",
     mus=("tension", 1), id="c7d",
     cert="ROCKSTAR",
     shots=[S(None, "g:quote", q="Ser irredimible tendrá un impacto duradero en Jason y Lucía", who="Rockstar Games, citado por PC Gamer"),
            S("Las guías hablan", X(SAT, 438.0), z=(1.0, 1.05), cert="GUIAS"),
            S("pero los detalles", X(SAT, 714.0), z=(1.0, 1.05), cert="GUIAS")],
     sfx=[(0.0, "paper", 0.4)])
beat("Lo que sí está claro es que no se puede deshacer. Si llegas ahí, tu única opción es cargar una partida guardada de antes.",
     mus=("tension", 1), id="c7e",
     cert="PRENSA",
     shots=[S(None, "g:ladder", hi=4, reveal=[0, 0, 0, 0, 0], lock=0.1),
            S("cargar una partida", "g:save", txt="CARGA UNA PARTIDA ANTERIOR", sub="La única forma de volver atrás")],
     sfx=[("w:cargar una partida", "ding", 0.35)])
beat("Y si crees que para quedarte en Profesional hay que ser un santo, mira esto. Un redactor terminó la historia en Profesional… con {321|trescientos veintiún} enemigos muertos. La diferencia es que a otros 461 los dejó fuera de combate.",
     mus=("synthwave", 1), id="c7f",
     cert="PRENSA",
     shots=[S(None, X(SIX, 455.0), z=(1.0, 1.05)),
            S("Un redactor", "g:stats", cues=["con 321", "a otros 461"])],
     sfx=[("w:con 321", "tick", 0.45), ("w:461", "ding", 0.4)])
beat("Y en su contador de animales: 98. Según él, casi todos pájaros, que no se apartan de ningún vehículo.",
     mus=("synthwave", 1), hold=0.2, id="c7g",
     cert="PRENSA", shots=[S(None, "g:stats", step=1)], sfx=[(0.0, "pop", 0.35), ("w:pájaros", "bird", 0.4)])

# ================================================================ CIERRE
beat("Resumiendo: sin testigos, no hay estrellas. Si te identifican, cámbiate de ropa y deja el auto. Escapar de la persecución no es perder la búsqueda. La sexta estrella solo se apaga muriendo. Y quien de verdad te juzga no es la policía: es tu perfil criminal.",
     section="RESUMEN Y CIERRE", mus=("synthwave", 2), pre=1.6, id="cierre1",
     shots=[S(None, "g:recap", cues=["sin testigos", "Si te identifican", "Escapar de la persecución", "La sexta estrella", "Y quien de verdad"])],
     sfx=[("w:sin testigos", "pop", 0.3), ("w:Si te identifican", "pop", 0.3), ("w:Escapar de la", "pop", 0.3), ("w:La sexta", "pop", 0.3), ("w:Y quien", "pop", 0.3)])
beat("¿Y tú? ¿Juegas en Profesional, o ya rozaste el Irredimible? ¿Cuánto aguantaste con 6 estrellas? Cuéntanoslo en los comentarios.",
     mus=("synthwave", 2), id="cierre2",
     shots=[S(None, "g:poll", cues=["¿Juegas", "¿Cuánto"])],
     sfx=[("w:¿Juegas", "pop", 0.35), ("w:¿Cuánto", "pop", 0.35)])
beat("Y si quieres seguir descubriendo los secretos de Vice City, suscríbete a Sal y Asfalto. Nos vemos en el próximo.",
     mus=("synthwave", 2), hold=0.4, id="cierre3",
     shots=[S(None, X(SIX, 388.2), z=(1.0, 1.06)), S("suscríbete", "g:subscribe")], sfx=[("w:suscríbete", "pop", 0.45)])
beat("", dur=20.0, mus=("synthwave", 1), id="end",
     shots=[S(None, "g:end")], trans="fade")

# ---------------------------------------------------------------- música original por capítulo (como en gl.py)
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
        y = audio.compose(sg["style"], dur, energy=en, seed=4100 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for _d in ("PROYECTO_DE_EDICION/recursos", "PROYECTO_DE_EDICION/audio"):
    os.makedirs(os.path.join(_ROOT, "VIDEO_LARGO_GTA6", _d), exist_ok=True)

VIDEO = dict(id="gx", folder="VIDEO_LARGO_GTA6", file="VIDEO_FINAL", res_dir="PROYECTO_DE_EDICION/recursos",
             title="GTA 6 te está vigilando: del testigo a las 6 estrellas y el perfil criminal que no se borra",
             format="Largo (16:9, 1920×1080, 30 fps) · gameplay real posterior al lanzamiento", music="synthwave", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55,
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="PROYECTO_DE_EDICION/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="PROYECTO_DE_EDICION/audio/narracion_original.wav", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="PROYECTO_DE_EDICION/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.thumbnail(c)
