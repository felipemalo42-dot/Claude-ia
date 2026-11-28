"""VIDEO_LARGO_6 — «Niko Bellic está en GTA 6 (y no es el único): los viejos protagonistas escondidos». Spoilers solo al final (se avisa).

Fuentes de imagen (créditos en la descripción, no en pantalla): Puzzle Knows (el pódcast con Wade y la escena de Niko, con los subtítulos
del propio juego), Nostix Gaming (el velero y el tono «Wind Chimes»; se recortan sus rótulos y se evitan sus insertos de GTA 5) e IGN
(el sombrero de Arthur Morgan y los guiños a Dexter). Lo que se cuenta es lo que dicen los subtítulos del juego en esas partidas; lo que
afirman los jugadores (el barco de Michael, el tono) se cuenta como suyo, no como algo confirmado por Rockstar.
"""
import os
import numpy as np
import audio
from videos import dc_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
P, N, H, D = "a8fK-RLK4qM", "I1cHE-udf-Y", "HAIx2b9ThL8", "mlnfgO4G0n0"
def X(v, t, **k): return S(None, f"x:{v}@{t}", **{"z": (1.0, 1.05), **k})
def XA(anchor, v, t, **k): return S(anchor, f"x:{v}@{t}", **{"z": (1.0, 1.05), **k})
def Q(anchor, q, who): return S(anchor, "g:quote", q=q, who=who)

# ================================================================ APERTURA
beat("En GTA 6 aparece Niko Bellic. Sí: el de GTA 4. Y no es un parecido ni una teoría: el juego dice su nombre. Pero no es el único que vuelve. Michael, Franklin, Trevor… y hasta Arthur Morgan dejan huella en Leonida. Hoy te los enseño todos, con partidas reales.",
     pre=0.3, id="o01", mus=("tension", 2),
     shots=[S(None, "g:cover", kicker="SPOILERS SOLO AL FINAL", lines=["NIKO BELLIC", "ESTÁ EN GTA 6"], sub="Y no es el único que vuelve"),
            XA("Sí: el de GTA 4", P, 464.3), Q("Y no es un parecido", "«Niko Bellic, my brother!»", "SUBTÍTULOS DE GTA 6"), XA("Michael, Franklin", P, 92.0), XA("Arthur Morgan", H, 100.5)],
     sfx=[(0.0, "riser", 0.35), ("w:Niko", "stamp", 0.5)])
beat("Vamos de menos a más. Primero, las pistas que puedes encontrar tú mismo. Y al final, la escena de Niko, que tiene spoilers de la historia: te avisaré antes, para que decidas si la ves. Y quédate hasta el final, porque lo de Niko no es un simple guiño: es una escena entera.",
     id="o02", mus=("tension", 1),
     shots=[S(None, "g:list", title="DE MENOS A MÁS", subt="Así va el vídeo", items=["Pistas que puedes encontrar tú", "La escena de Niko (con spoilers)"], st=[1.8, 4.6]),
            XA("Y quédate hasta el final", P, 272.0)], sfx=[])

# ================================================================ 1. EL PÓDCAST DE WADE
beat("Empezamos por GTA 5. En la radio de GTA 6 hay un pódcast de crímenes reales. Quien lo presenta lleva tiempo investigando un caso de Los Santos, y tiene su gracia: entre episodio y episodio se queja de sus audiciones fallidas y de las facturas que no puede pagar. Y en esta entrega acaba sentándose a hablar con alguien que conocemos muy bien: Wade.",
     id="c1a", chapter=(1, "EL PÓDCAST DE WADE"), mus=("mystery", 2),
     shots=[X(P, 18.0), XA("se queja de sus audiciones", P, 143.0), XA("alguien que conocemos", P, 33.0)], sfx=[("w:Wade", "stamp", 0.4)])
beat("Wade era el amigo inseparable de Trevor en GTA 5: un chico ingenuo, con rastas, que lo seguía a todas partes. Llegó a Los Santos buscando a su primo Floyd… y Trevor acabó instalándose en casa de Floyd, con las consecuencias que ya conoces.",
     id="c1b", mus=("mystery", 1),
     shots=[S(None, "g:quote", q="Wade Hebert: el amigo inseparable de Trevor en GTA 5.", who="GTA 5 (2013)")], sfx=[])
beat("El pódcast cuenta que, al principio, sospechaba de él: que Wade podía ser un genio criminal. Pero cuando por fin le enseñó la fotografía que había encontrado en una taquilla, Wade dejó de disimular. En esa foto aparecen tres hombres sentados a la mesa de un restaurante.",
     id="c1c", mus=("mystery", 2),
     shots=[X(P, 76.0)], sfx=[])
beat("Y suelta esto: «¡Ese de ahí es mi mejor amigo! Es todo un caballero». No dice cómo se llama. Pero de los otros dos, sí: «El de atrás es Michael De Santa. Y ese jovencito es Franklin Clinton, lo que llaman un granuja de la calle».",
     id="c1d", mus=("mystery", 2),
     shots=[X(P, 92.0)], sfx=[("w:Michael De Santa", "ding", 0.4), ("w:Franklin Clinton", "ding", 0.4)])
beat("El nombre que no se atreve a decir, el de su mejor amigo, es el de Trevor. Que ni siquiera se atreva a pronunciarlo es, conociéndolo, lo más Trevor posible. Y Wade insiste en que ninguno de ellos pudo matar a Floyd y Deborah. Si jugaste GTA 5, sabes perfectamente quién fue. Y el pódcast tampoco se lo traga: «Wade parecía asustado cuando hablaba de sus tres amigos. ¿Y por qué levantaba la voz? ¿Sería que la foto era, en realidad, de tres criminales peligrosos?».",
     id="c1e", mus=("mystery", 2),
     shots=[X(P, 112.5), Q("Si jugaste GTA 5", "Floyd y Deborah murieron en GTA 5… a manos de Trevor.", "GTA 5 (2013)"), XA("Y el pódcast tampoco", P, 124.0)], sfx=[])
beat("El pódcast termina con más preguntas que respuestas: ¿qué quería decir Wade con eso de robar todos esos bancos? ¿Cómo acabaron los tres en la misma mesa de restaurante? Y la gran pregunta: ¿dónde sigue la investigación? Para GTA 6, lo que pasó en Los Santos fue real… y sigue sin resolverse.",
     id="c1f", mus=("mystery", 2),
     shots=[X(P, 151.0), XA("Para GTA 6", P, 164.0)], sfx=[])
beat("Eso sí: de momento, nadie ha enseñado una partida en la que Michael, Franklin o Trevor aparezcan en persona. Solo se habla de ellos.",
     id="c1g", mus=("mystery", 1),
     shots=[Q(None, "Michael, Franklin y Trevor: se habla de ellos, pero nadie los ha visto en persona.", "LO QUE SE SABE")], sfx=[])

# ================================================================ 2. ¿EL BARCO DE MICHAEL?
beat("Pero algunos jugadores creen haber encontrado algo más. Este velero está varado en tierra, en Leonida… y es casi idéntico al barco de Michael en GTA 5: el que su hijo Jimmy intentó vender, y que acabó remolcado por la autopista mientras Michael y Franklin lo perseguían.",
     id="c2a", chapter=(2, "¿EL BARCO DE MICHAEL?"), mus=("tropical", 2),
     shots=[X(N, 24.0), XA("es casi idéntico", N, 88.0), Q("el que su hijo Jimmy", "Jimmy intenta vender el barco de Michael… y acaba remolcado por la autopista.", "GTA 5 (2013)")], sfx=[])
beat("En GTA 5, ese barco era el orgullo de Michael. En una de las primeras misiones, Jimmy se lo intenta vender a unos tipos que se lo llevan por la autopista, y Franklin acaba saltando al barco en marcha para recuperarlo. Aquí se puede subir a bordo. Y en la pantalla de navegación, el jugador que lo encontró asegura que hay un guiño a GTA 5. Rockstar no ha dicho nada, así que tómatelo como lo que es: un parecido muy sospechoso.",
     id="c2b", mus=("tropical", 2),
     shots=[X(N, 93.0), Q("En una de las primeras misiones", "Franklin salta al barco en plena autopista para recuperarlo.", "GTA 5 (2013)"),
            XA("Aquí se puede subir a bordo", N, 67.5), XA("en la pantalla de navegación", N, 80.0), XA("Rockstar no ha dicho nada", N, 33.0)], sfx=[])
beat("Y el mismo jugador encontró otra cosa en el móvil de Jason: un tono de llamada que se llama «Wind Chimes». Según él, es el mismo tono que sonaba en el móvil de Michael. Si te pasaste GTA 5 con ese sonido en el bolsillo, dinos en los comentarios si lo reconoces.",
     id="c2c", mus=("tropical", 1),
     shots=[X(N, 105.0), XA("Wind Chimes", N, 113.0), Q("Si te pasaste GTA 5", "«Wind Chimes»: según el jugador que lo encontró, el tono del móvil de Michael en GTA 5.", "DÍNOSLO EN LOS COMENTARIOS")],
     sfx=[("w:Wind Chimes", "ding", 0.4)])

# ================================================================ 3. EL SOMBRERO DE ARTHUR
beat("De Red Dead Redemption 2, de dos mil dieciocho, también hay un recuerdo. Arthur Morgan, su protagonista, nunca se quitaba su sombrero de vaquero… y en GTA 6 puedes llevarte uno igual. Bueno, uno que se le parece muchísimo. A partir del capítulo dos, en una casa azul con una bandera de Estados Unidos muy alta, al noroeste de la casa de Jason y Lucía, hay una venta de garaje.",
     id="c3a", chapter=(3, "EL SOMBRERO DE ARTHUR"), mus=("nature", 2),
     shots=[X(H, 0.0), XA("en una casa azul", H, 8.0), XA("al noroeste", H, 40.0)], sfx=[])
beat("Es la única casa de la calle con mercadillo, así que no tiene pérdida. En una de las mesas está el «sombrero vaquero auténtico», de cuero marrón, por treinta y cinco dólares. Le falta el desgaste… pero es el de Arthur. Lleva dinero en efectivo, y si vas antes del capítulo dos, solo encontrarás una casa normal.",
     id="c3b", mus=("nature", 2),
     shots=[X(H, 64.0), XA("En una de las mesas", H, 72.0), XA("por treinta y cinco dólares", H, 13.0), XA("Le falta el desgaste", H, 96.0)],
     sfx=[("w:treinta y cinco", "ding", 0.4)])

# ================================================================ 4. DEXTER EN VICE CITY
beat("Y hay un protagonista que ni siquiera es de Rockstar: Dexter Morgan, el forense de la policía de Miami que, en la serie, es un asesino de asesinos. Tiene sentido: la serie pasa en Miami, la ciudad en la que se inspira Vice City. En Vice City hay un edificio de apartamentos que se parece muchísimo al suyo… y se llama Trinity Apartments.",
     id="c4a", chapter=(4, "DEXTER EN VICE CITY"), mus=("synthwave", 2),
     shots=[X(D, 0.0), XA("En Vice City hay un edificio", D, 32.0), XA("Trinity Apartments", D, 55.0)], sfx=[("w:Trinity", "stamp", 0.4)])
beat("En la serie, Trinity era el asesino de la cuarta temporada, uno de sus peores enemigos. Y la cosa no acaba ahí: en el canal de al lado hay un barco igual que el suyo, el «Slice of Life», en el que se deshacía de los cuerpos, y en la azotea, sus herramientas: un cuchillo, cinta, una jeringuilla, una bolsa de plástico y cuerda. Hasta el aparato de aire acondicionado del apartamento está en su sitio: en la serie, ahí es donde Dexter escondía sus recuerdos de cada víctima.",
     id="c4b", mus=("synthwave", 2),
     shots=[X(D, 40.0), XA("en el canal de al lado", D, 67.0), XA("en la azotea", D, 86.0)], sfx=[])
beat("Y en Key Lento hay una casa que esconde algo peor: una habitación forrada de plástico, como las que preparaba Dexter. Eso sí, primero tendrás que vértelas con el hombre armado que vive allí. Dentro hay armas, un chaleco antibalas… y hasta un lanzacohetes escondido en la bañera.",
     id="c4c", mus=("synthwave", 1),
     shots=[X(D, 96.0), XA("una habitación forrada", D, 158.5), XA("primero tendrás que", D, 114.0), XA("Dentro hay armas", D, 125.5), XA("y hasta un lanzacohetes", D, 130.5)], sfx=[])

# ================================================================ LLAMADA A MITAD
beat("Si te está gustando este repaso, dale like y suscríbete a Sal y Asfalto: así sabemos que quieres más secretos de GTA 6. Y ahora, sí: el plato fuerte.",
     id="cta", cta=True, mus=("tropical", 1),
     shots=[X(D, 120.0), XA("dale like", H, 30.5)], sfx=[("w:dale like", "ding", 0.45), ("w:suscríbete", "pop", 0.45)])

# ================================================================ 5. NIKO BELLIC
beat("Antes de Niko, un poco de contexto: Rockstar ya lo había hecho. En GTA 5, en su primera escena, Trevor mata a Johnny Klebitz, el protagonista de un episodio de GTA 4. Y Packie McReary, de GTA 4, podía unirse a tus atracos en Los Santos. Los personajes de un juego siguen vivos en el siguiente.",
     id="c5p", chapter=(5, "NIKO BELLIC"), mus=("tension", 1),
     shots=[Q(None, "GTA 5: en su primera escena, Trevor mata a Johnny Klebitz, protagonista de un episodio de GTA 4.", "ROCKSTAR YA LO HIZO"),
            Q("Y Packie McReary", "Packie McReary, de GTA 4, podía unirse a los atracos de GTA 5.", "ROCKSTAR YA LO HIZO")], sfx=[])
beat("Último aviso: a partir de aquí hay spoilers de la historia de GTA 6. Si no quieres saber nada, este es el momento de irte… aunque te vas a perder lo mejor.",
     id="c5a", mus=("tension", 1),
     shots=[S(None, "g:cover", kicker="ÚLTIMO AVISO", lines=["SPOILERS", "DE LA HISTORIA"], sub="La escena de Niko Bellic")], sfx=[("w:spoilers", "stamp", 0.45)])
beat("Para entender la escena: Giorgio Gallo es un mafioso de Vice City con el que Jason y Lucía acaban trabajando. Y en esta misión está eufórico: por fin tiene un disco duro que lo va a sacar de todos sus problemas. Hasta les dice a Jason y Lucía que ya no van a necesitar nuevas identidades.",
     id="c5b", mus=("tension", 2),
     shots=[X(P, 277.6), XA("Hasta les dice", P, 290.15)], sfx=[("w:disco duro", "stamp", 0.4)])
beat("«Se acabaron los problemas, se acabaron los albaneses. ¡Gigi ha vuelto!». Y justo entonces, alguien entra en la sala. Giorgio se da la vuelta, sonríe… y lo saluda así: «¡Niko Bellic, hermano mío!». Lo dice en voz alta, y así aparece en los subtítulos del juego: Niko Bellic.",
     id="c5c", mus=("tension", 2),
     shots=[X(P, 296.0), XA("alguien entra", P, 303.4), XA("Giorgio se da la vuelta", P, 306.5), XA("Niko Bellic, hermano", P, 330.7),
            # el subtítulo del juego («Niko Bellic, my brother!», sobre negro): ampliado y sin el subtítulo propio encima
            XA("Niko Bellic.", P, 325.6, nosub=True, z=(1.3, 1.38), f=(0.5, 0.91))], sfx=[("w:Niko Bellic", "impact", 0.5)])
beat("Es él. Mayor, con barba, una cadena de oro… y la misma mirada. En GTA 4, Niko era un veterano de guerra de Europa del Este que llegaba a Liberty City porque su primo Roman le había prometido mansiones, coches y chicas. La realidad era un piso cutre y un montón de deudas. Y su historia terminaba con una decisión que le costaba la vida a Roman… o a Kate. Casi veinte años después, aquel hombre que quería dejar atrás la violencia aparece en Vice City… y no viene de visita.",
     id="c5d", mus=("storm", 2),
     shots=[X(P, 337.66), Q("En GTA 4", "GTA 4 (2008): Niko Bellic, veterano de guerra de Europa del Este, llega a Liberty City buscando una vida mejor.", "EL PROTAGONISTA DE GTA 4"),
            Q("Y su historia terminaba", "Al final de GTA 4, según lo que elijas, muere Roman… o muere Kate.", "GTA 4 (2008)"),
            XA("aquel hombre", P, 380.0), XA("y no viene de visita", P, 353.0)], sfx=[])
beat("«Solo hay una razón por la que vendría hasta aquí», le dice. Giorgio la ha liado: hay dos mil millones de dólares en juego, se han perdido demasiados envíos… y los cárteles ya han decidido trabajar con otro: un tal Olaf. Giorgio no se lo puede creer: «¿Olaf? ¡Fui al colegio con Olaf!». Y Niko le recuerda lo que está en juego: el siguiente envío ya ha salido, y media Europa va a comprarle la droga a otro.",
     id="c5e", mus=("storm", 2),
     shots=[X(P, 343.85), XA("hay dos mil millones", P, 350.45), XA("se han perdido demasiados envíos", P, 360.5), XA("y los cárteles", P, 364.9),
            XA("Giorgio no se lo puede", P, 356.05), XA("¡Fui al colegio", P, 370.15), XA("Y Niko le recuerda", P, 362.55), XA("el siguiente envío", P, 384.1)],
     sfx=[("w:dos mil millones", "stamp", 0.45)])
beat("Giorgio suplica: «¡Niko, por favor! Tengo un plan, te lo prometo». Pero Niko ni se inmuta. «Giorgio, intentamos limpiar tu desastre… y tú te lo traes a casa». Le apunta, le deja suplicar… y al final le concede una última oportunidad: «No hace falta que te diga lo que pasará después».",
     id="c5f", mus=("storm", 3),
     shots=[X(P, 418.0), XA("Pero Niko ni", P, 433.25), XA("Giorgio, intentamos", P, 425.7), XA("Le apunta", P, 443.6), XA("una última oportunidad", P, 449.0),
            XA("No hace falta", P, 452.7)], sfx=[("w:apunta", "impact", 0.4)])
beat("Y se va. Ni una palabra más. Giorgio se queda en el suelo, temblando… y Jason y Lucía, en medio de un lío que acaba de hacerse mucho más grande. Ahora les toca arreglarlo: recuperar la droga de una base de los guardacostas… y detener un barco con veinte mil contenedores rumbo a Europa.",
     id="c5g", mus=("storm", 1),
     shots=[X(P, 458.0), XA("Giorgio se queda", P, 474.0), XA("y Jason y Lucía", P, 476.85), XA("Ahora les toca arreglarlo", P, 484.25), XA("y detener un barco", P, 488.9)], sfx=[])
beat("Esta escena deja algo claro: GTA 4, GTA 5 y GTA 6 comparten el mismo mundo. Y Liberty City sigue ahí: en uno de los finales del juego, en la autopista se ve un cartel hacia Alderney, uno de los barrios de GTA 4. Niko sigue vivo… y más peligroso que nunca.",
     id="c5h", mus=("tension", 1),
     shots=[Q(None, "GTA 4, GTA 5 y GTA 6: el mismo mundo.", "ESTA ESCENA LO CONFIRMA"), XA("Y Liberty City sigue ahí", "B0b5JhrGUJQ", 422.9), XA("Niko sigue vivo", P, 469.5)], sfx=[("w:Alderney", "ding", 0.4)])

beat("Repasemos: Wade y su pódcast sobre Michael, Franklin y Trevor; el velero que parece el de Michael y su tono de móvil; el sombrero de Arthur; el apartamento de Dexter… y Niko Bellic, en persona.",
     id="r0a", mus=("tropical", 1),
     shots=[S(None, "g:list", title="LOS QUE VUELVEN", subt="Todo lo que se ha encontrado",
              items=["El pódcast de Wade", "El velero y el tono de Michael", "El sombrero de Arthur", "El apartamento de Dexter", "Niko Bellic, en persona"], st=[0.8, 3.6, 6.4, 8.0, 10.0])], sfx=[])
beat("Y si te quedas con ganas de más guiños, en el canal tienes Shorts con otros secretos de GTA 6: las gorras de Mario y Luigi, el barco fantasma del faro… y el portal a la Vice City de PlayStation 2, la de Tommy Vercetti.",
     id="r00", mus=("tropical", 1),
     shots=[S(None, "g:list", title="MÁS GUIÑOS EN EL CANAL", subt="Shorts de Sal y Asfalto",
              items=["Las gorras de Mario y Luigi", "El barco fantasma del faro", "El portal a la Vice City de PS2"], st=[3.6, 6.4, 8.8])], sfx=[])

# ================================================================ CIERRE
beat("Lo que más me gusta de estos guiños es que premian a los que llevamos años jugando: un nombre en un pódcast, un barco en un jardín, un sombrero en un mercadillo… y, de repente, Niko. Y tú, ¿a quién te gustaría ver volver? ¿A Trevor, a CJ, a Tommy Vercetti? Escríbelo en los comentarios. Y si quieres saber cómo termina la historia de Jason y Lucía, tienes nuestro vídeo con todos los finales. Suscríbete a Sal y Asfalto, y nos vemos en el próximo.",
     id="r01", mus=("tropical", 1), hold=0.6,
     shots=[Q(None, "¿A quién te gustaría ver volver?", "ESCRÍBELO EN LOS COMENTARIOS"), S("Suscríbete", "g:subscribe")], sfx=[("w:Suscríbete", "pop", 0.45)])
beat("", dur=20.0, mus=("tropical", 1), id="end", shots=[S(None, "g:end")], trans="fade")

def music_fn(total, beats_tl):
    segs = []
    for b, bd in zip(B, beats_tl):
        st, lv = b.get("mus", ("tension", 1))
        if segs and segs[-1]["style"] == st: segs[-1]["en"].append((bd["start"] - segs[-1]["t0"], lv))
        else: segs.append(dict(style=st, t0=bd["start"], en=[(0.0, lv)]))
    n = int(total * audio.SR); out = np.zeros((n, 2)); xf = 1.2
    for i, sg in enumerate(segs):
        t1 = segs[i + 1]["t0"] if i + 1 < len(segs) else total
        a0 = max(0.0, sg["t0"] - (xf / 2 if i else 0)); dur = (t1 - a0) + (xf / 2 if i + 1 < len(segs) else 0)
        en = [(max(0.0, tt + (sg["t0"] - a0)), lv) for tt, lv in sg["en"]]
        y = audio.compose(sg["style"], dur, energy=en, seed=9100 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "VIDEO_LARGO_6_GTA6_VIEJOS_PROTAGONISTAS"
for _d in ("trabajo", "trabajo/audio"):
    os.makedirs(os.path.join(_ROOT, FOLDER, _d), exist_ok=True)
VIDEO = dict(id="vc", folder=FOLDER, file="VIDEO_FINAL", res_dir="trabajo", theme="retro", credit=False,
             title="Niko Bellic está en GTA 6 (y no es el único)",
             format="Largo (16:9, 1920×1080, 30 fps) · escenas reales del juego", music="tension", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.30, duck=0.22, duck_release=0.9, sfx_gain=0.5,
             expr_pick=dict(seeds=2, confs=[(0.6, 0.4), (0.7, 0.45)]),   # 4 tomas por frase: la más animada (voice_expr.py)
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="trabajo/audio/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    """Fotograma real de Niko (recortado) + «NIKO ESTÁ EN GTA 6»."""
    import skia
    from gfx import draw_text, rect
    Wt, Ht = 1280, 720; base = os.path.join(_ROOT, FOLDER, "trabajo")
    R._bg(c, os.path.join(base, "miniatura_fondo.png"), 0, 0, Wt, Ht)
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, Ht), (0, Ht - 340)], [skia.Color(8, 6, 14, 245), skia.Color(8, 6, 14, 0)]))
    c.drawRect(skia.Rect.MakeXYWH(0, Ht - 340, Wt, 340), g)
    rect(c, 40, 36, 380, 64, "#F2C14E", 1, r=12); draw_text(c, "VUELVE DE GTA 4", 230, 84, "anton", 44, "#14101E", 1, align="center", tracking=3)
    draw_text(c, "NIKO BELLIC", Wt / 2, Ht - 140, "anton", 124, "#FFFFFF", 1, align="center", tracking=3)
    draw_text(c, "ESTÁ EN GTA 6", Wt / 2, Ht - 40, "anton", 92, "#F2C14E", 1, align="center", tracking=4)
