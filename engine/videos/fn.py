"""VIDEO_LARGO_5 — «Todos los finales de GTA 6 explicados (y cómo conseguir el bueno)». CON SPOILERS (se avisa en el título y al empezar).

Fuente de imagen: TheGamingRevolution, «GTA 6 - ALL 9 Endings Story Explained» (21/11/2026, 1440p), que a su vez reúne partidas de
Sirloin, meloo, BabyZoneGaming y Ben-Gun (créditos en la descripción, no en pantalla). Se usa recortado (sin marcas de agua ni
subtítulos) y se evitan sus tramos que no son de GTA 6 (Red Dead Redemption 2, un recorte de periódico, una escena de GTA IV).
Datos: lo que se ve en esas escenas y la explicación transcrita de ese vídeo. Rockstar no ha dicho cuál es el final oficial, y la
versión «Jason libre y Lucía presa» no aparece en ninguna partida publicada: se menciona solo como rumor sin pruebas.
"""
import os
import numpy as np
import audio
from videos import dc_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
F = "B0b5JhrGUJQ"
def X(t, **k): return S(None, f"x:{F}@{t}", z=(1.0, 1.05), **k)
def XA(anchor, t, **k): return S(anchor, f"x:{F}@{t}", z=(1.0, 1.05), **k)

# ================================================================ APERTURA
beat("Aviso: en este vídeo te cuento todo el final de GTA 6. Si todavía no lo has terminado, guárdalo para después. ¿Sigues aquí? Perfecto. Porque GTA 6 no tiene un final: tiene siete, y un par de variantes. Y lo que hiciste durante toda la partida decide cuál ves.",
     pre=0.3, id="o01", mus=("tension", 2),
     shots=[S(None, "g:cover", kicker="AVISO: SPOILERS", lines=["TODOS LOS FINALES", "DE GTA 6"], sub="Y cómo conseguir el bueno"),
            XA("¿Sigues aquí?", 312.0), XA("tiene siete", 344.0), XA("lo que hiciste", 628.0)],
     sfx=[(0.0, "riser", 0.35), ("w:siete", "stamp", 0.5)])
beat("Vamos a verlos todos, del más trágico al más feliz. Y al final, te explico qué tienes que hacer para conseguir el mejor de todos.",
     id="o02", mus=("tension", 1),
     shots=[X(256.0), XA("al más feliz", 644.0)], sfx=[])

# ================================================================ 1. EL ÚLTIMO GOLPE
beat("Todo empieza en la última misión. Jason y Lucía ya no se fían de nadie: les prometieron un indulto y los traicionaron. Su única carta es un disco duro con pruebas que alguien muy poderoso no puede permitirse perder.",
     id="c1a", chapter=(1, "EL ÚLTIMO GOLPE"), mus=("tension", 2),
     shots=[X(120.0), XA("les prometieron", 104.0), XA("Su única carta", 128.0)], sfx=[("w:disco duro", "stamp", 0.4)])
beat("Así que se abren paso a tiros por una torre, llegan al despacho y se llevan el disco. Y aquí llega la primera gran decisión, aunque no lo parezca: cómo salir de ese edificio.",
     id="c1b", mus=("tension", 3),
     shots=[X(136.0), XA("llegan al despacho", 144.0), XA("cómo salir", 150.0)], sfx=[("w:a tiros", "impact", 0.35)])

# ================================================================ 2. EL ASCENSOR
beat("Si bajan en el ascensor hasta el final, la policía los está esperando cuando se abren las puertas. Y pasa en un segundo: disparan a Jason, Lucía agarra un arma y responde… y muere a su lado. Sin despedidas, sin música épica. Se acabó.",
     id="c2a", chapter=(2, "EL ASCENSOR"), mus=("storm", 2),
     shots=[X(158.0), XA("disparan a Jason", 166.0), XA("Sin despedidas", 172.0)], sfx=[("w:disparan", "impact", 0.5)])
beat("Hay una segunda versión de esa misma emboscada. Jason muere, pero a Lucía la arrestan y, con el tiempo, sale libre. Conduce hasta Liberty City para ver a su hijo… y cuando está a punto de llegar, da la vuelta.",
     id="c2b", mus=("storm", 1),
     shots=[X(176.0), XA("Conduce hasta Liberty City", 184.0), XA("da la vuelta", 196.0)], sfx=[("w:da la vuelta", "whoosh", 0.4)])
beat("Vuelve a Vice City, a la cafetería de siempre… y al crimen. Es un final pequeño y muy triste: Lucía se convence de que, si se acerca a su hijo, tarde o temprano también le hará daño.",
     id="c2c", mus=("storm", 1),
     shots=[X(200.0), XA("Es un final pequeño", 224.0)], sfx=[])

# ================================================================ 3. EL PANTANO
beat("El tercer final es el castigo por fiarte de quien no debías. Si en la torre perdonas a Mendes y aceptas trabajar con él, cuando salen del ascensor él está esperando. Los esposa delante de la policía y les dice que el arresto es solo teatro.",
     id="c3a", chapter=(3, "EL PANTANO"), mus=("mystery", 2),
     shots=[X(208.0), XA("cuando salen del ascensor", 248.0), XA("es solo teatro", 252.0)], sfx=[("w:castigo", "stamp", 0.4)])
beat("Pero el coche no va hacia ninguna comisaría: va hacia el pantano. Jason y Lucía se miran y lo entienden a la vez. El juego no enseña lo que pasa… pero después de los créditos vemos sus calaveras en el agua, y un caimán acercándose.",
     id="c3b", mus=("mystery", 3),
     shots=[X(256.0), XA("se miran", 272.0), XA("después de los créditos", 262.0)], sfx=[("w:caimán", "heartbeat", 0.5)])

# ================================================================ LLAMADA A MITAD
beat("Antes de seguir con los finales del puente: si este vídeo te está sirviendo, dale like y suscríbete a Sal y Asfalto. Así sabemos que quieres más historias de GTA 6 contadas a fondo.",
     id="cta", cta=True, mus=("tension", 1),
     shots=[X(288.0), XA("dale like", 296.0)], sfx=[("w:dale like", "ding", 0.45), ("w:suscríbete", "pop", 0.45)])

# ================================================================ 4. EL PUENTE
beat("Si consiguen bajar de la torre por la grúa, van a casa de Cal para huir en barco. Pero Cal ve que llegan y les hace un gesto para que se vayan, sin decir nada: la policía ya está allí. Así que escapan hacia el aeródromo… y los encierran en un puente.",
     id="c4a", chapter=(4, "EL PUENTE"), mus=("tension", 2),
     shots=[X(232.0), XA("Pero Cal", 288.6), XA("y los encierran", 304.0)], sfx=[("w:puente", "stamp", 0.4)])
beat("Ahí Lucía le recuerda a Jason que el trato era para ella. Él puede darle el disco y una oportunidad de quedar libre… pero nadie promete que él vaya con ella. Y aquí elegimos.",
     id="c4b", mus=("tension", 2),
     shots=[X(312.0), XA("Él puede darle", 320.0), XA("Y aquí elegimos", 328.0)], sfx=[])
beat("Si no se rinden, llega el final de Bonnie y Clyde. Lucía se queda con Jason, intentan atravesar el control con el coche, y la policía los acribilla juntos. Su hijo se queda con la familia de Lucía.",
     id="c4c", mus=("storm", 3),
     shots=[X(336.0), XA("intentan atravesar", 352.0), XA("Su hijo", 368.0)], sfx=[("w:acribilla", "impact", 0.5)])
beat("Es el final más trágico, pero también el más romántico: eligen no separarse. Y cobra otro sentido cuando sabes que tienen un hijo, y que Lucía llega a pensar que él estará mejor sin ellos.",
     id="c4d", mus=("storm", 1),
     shots=[X(376.0), XA("eligen no separarse", 384.0)], sfx=[])
beat("Si en cambio intentan saltar al agua y sale mal, también mueren los dos, pero sin ningún romanticismo: los abaten como a dos fugitivos más, con Jason todavía con un arma en la mano. Y ojo: con esa misma elección, en otra partida, a Jason simplemente lo arrestan. Lo que cambia es cómo jugaste antes.",
     id="c4e", mus=("storm", 2),
     shots=[X(392.0), XA("con Jason todavía", 400.0), XA("Lo que cambia", 384.4)], sfx=[])

# ================================================================ 5. LA CÁRCEL
beat("Si el salto sale bien, se acercan a la barandilla, se dan la mano, cuentan hasta tres… y Jason deja que Lucía salte sola. Mientras la policía lo detiene a él, Lucía escapa nadando.",
     id="c5a", chapter=(5, "LA CÁRCEL"), mus=("nature", 2),
     shots=[X(404.0), XA("Lucía salte sola", 412.0), XA("Lucía escapa", 478.0)], sfx=[("w:salte sola", "whoosh", 0.45)])
beat("Lucía firma el trato y va a Liberty City a buscar a su hijo. Jason entra en prisión. Y el juego empieza a saltar entre las dos vidas: él, peleando en el comedor de la cárcel; los años pasando, con barba y el pelo largo.",
     id="c5b", mus=("nature", 1),
     shots=[X(424.0), XA("Jason entra en prisión", 432.0), XA("los años pasando", 440.0)], sfx=[])
beat("Hasta que Lucía lleva a su hijo a visitarlo, y padre e hijo ponen la mano contra el cristal. Jason se sacrificó para que ellos tuvieran una vida… y esto es lo más cerca que puede estar de ellos.",
     id="c5c", mus=("nature", 1),
     shots=[X(448.0), XA("ponen la mano", 456.0)], sfx=[])

# ================================================================ 6. EL REENCUENTRO
beat("Y llegamos al mejor final: el reencuentro familiar. Al principio parece el de la cárcel: Lucía salta, a Jason lo detienen… Pero un día, en la cafetería, a Lucía le llega un mensaje de Abe: la inversión ha dado dinero.",
     id="c6a", chapter=(6, "EL REENCUENTRO"), mus=("tropical", 2),
     shots=[X(540.0), XA("Pero un día", 588.0), XA("la inversión", 600.0)], sfx=[("w:mensaje", "ding", 0.45)])
beat("Se reúnen con unos señores de traje, y poco después llega otro mensaje: «Ya está». De su cuenta salen dos millones y medio de dólares… y Jason sale de la cárcel.",
     id="c6b", mus=("tropical", 2),
     shots=[X(594.0), XA("Ya está", 604.0), XA("y Jason sale", 616.0)], sfx=[("w:Ya está", "stamp", 0.45)])
beat("Lucía lo espera en la puerta de la misma prisión donde él la recogió al principio del juego. Esta vez es ella quien viene a buscarlo, con su hijo. Jason le da la mano, los tres se suben al coche… y se van juntos a Liberty City.",
     id="c6c", mus=("tropical", 3),
     shots=[X(620.0), XA("Jason le da la mano", 628.0), XA("y se van juntos", 644.0)], sfx=[])

# ================================================================ 7. CÓMO CONSEGUIRLO
beat("¿Cómo se consigue? Según las partidas que ya se han publicado, hacen falta tres cosas antes de la última misión.",
     id="c7a", chapter=(7, "CÓMO CONSEGUIRLO"), mus=("synthwave", 2),
     shots=[S(None, "g:list", title="EL FINAL FELIZ", subt="Lo que piden las partidas publicadas",
              items=["2 millones en el ahorro familiar", "Perfil criminal bajo", "Perdonar al policía"], st=[3.2, 7.0, 11.0])],
     sfx=[])
beat("Una: tener al menos dos millones de dólares en la cuenta de ahorros familiar de Jason y Lucía. Dos: llevar un perfil criminal bajo, o sea, no convertir cada golpe en una masacre. Y tres: perdonar al policía cuando el juego te da esa opción.",
     id="c7b", mus=("synthwave", 2),
     shots=[S(None, "g:list", title="EL FINAL FELIZ", subt="Lo que piden las partidas publicadas",
              items=["2 millones en el ahorro familiar", "Perfil criminal bajo", "Perdonar al policía"], st=[0.2, 5.6, 10.6])],
     sfx=[("w:Una", "ding", 0.4), ("w:Dos", "ding", 0.4), ("w:tres", "ding", 0.4)])
beat("Y un detalle: perdonar a Mendes no es lo mismo que dejar que él te saque de ahí. Lo primero puede ayudarte. Lo segundo, ya viste a dónde lleva.",
     id="c7c", mus=("synthwave", 1),
     shots=[X(260.0)], sfx=[])

# ================================================================ 8. DESPUÉS DE LOS CRÉDITOS
beat("Esos ahorros cuentan incluso si todo sale mal. Si tienes los dos millones pero mueren en el ascensor o en el puente, hay una escena dos años después: Abe aparece en casa de la familia que está criando a su hijo y les entrega el dinero.",
     id="c8a", chapter=(8, "DESPUÉS DE LOS CRÉDITOS"), mus=("mystery", 2),
     shots=[X(692.0), XA("hay una escena", 700.0), XA("les entrega el dinero", 714.0)], sfx=[])
beat("Y queda un misterio. En los finales del puente, Cal abre por fin el archivo que estaba esperando, dice que no se lo puede creer… y la pantalla se va a negro. Nunca vemos qué hay dentro.",
     id="c8b", mus=("mystery", 2),
     shots=[X(722.0), XA("dice que no se lo puede creer", 734.0), XA("Nunca vemos", 740.0)], sfx=[("w:a negro", "stamp", 0.4)])
beat("También se habla de un final en el que Jason sale libre y Lucía acaba presa. Pero hasta ahora nadie ha enseñado una partida con ese final, así que, por ahora, es solo un rumor.",
     id="c8c", mus=("mystery", 1),
     shots=[X(684.0), XA("nadie ha enseñado", 748.0 - 3.0)], sfx=[])

# ================================================================ CIERRE
beat("Rockstar no ha dicho cuál de todos es el oficial. Pero si alguna vez volvemos a ver a Jason y Lucía, muchos apuestan por el reencuentro en Liberty City.",
     id="r01", mus=("tropical", 1),
     shots=[S(None, "g:quote", q="Rockstar no ha dicho cuál es el final oficial.", who="LOS FINALES DE GTA 6"), XA("muchos apuestan", 650.0)], sfx=[])
beat("Y tú, ¿qué final conseguiste? ¿Y cuál crees que se merecían? Escríbelo en los comentarios. Si quieres más GTA 6 contado a fondo, suscríbete a Sal y Asfalto. Nos vemos en el próximo vídeo.",
     id="r02", mus=("tropical", 1), hold=0.6,
     shots=[S(None, "g:quote", q="¿Qué final conseguiste tú? ¿Cuál se merecían?", who="ESCRÍBELO EN LOS COMENTARIOS"), S("suscríbete", "g:subscribe")], sfx=[("w:suscríbete", "pop", 0.45)])
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
        y = audio.compose(sg["style"], dur, energy=en, seed=8700 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "VIDEO_LARGO_5_GTA6_FINALES"
for _d in ("trabajo", "trabajo/audio"):
    os.makedirs(os.path.join(_ROOT, FOLDER, _d), exist_ok=True)
VIDEO = dict(id="fn", folder=FOLDER, file="VIDEO_FINAL", res_dir="trabajo", theme="finales", credit=False,
             title="Todos los finales de GTA 6 explicados (y cómo conseguir el bueno)",
             format="Largo (16:9, 1920×1080, 30 fps) · escenas reales del juego", music="tension", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.30, duck=0.22, duck_release=0.9, sfx_gain=0.5,
             expr_pick=dict(seeds=2, confs=[(0.6, 0.4), (0.7, 0.45)]),   # 4 tomas por frase: la más animada (voice_expr.py)
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="trabajo/audio/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    """Fotograma real del final del puente (recortado) + «TODOS LOS FINALES» y aviso de spoilers."""
    import skia
    from gfx import draw_text, rect
    Wt, Ht = 1280, 720; base = os.path.join(_ROOT, FOLDER, "trabajo")
    R._bg(c, os.path.join(base, "miniatura_fondo.png"), 0, 0, Wt, Ht, crop=(0.0, 0.0, 1.0, 1.0))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, Ht), (0, Ht - 330)], [skia.Color(10, 4, 6, 245), skia.Color(10, 4, 6, 0)]))
    c.drawRect(skia.Rect.MakeXYWH(0, Ht - 330, Wt, 330), g)
    rect(c, 40, 36, 300, 64, "#FF5A5F", 1, r=12); draw_text(c, "SPOILERS", 190, 84, "anton", 48, "#FFFFFF", 1, align="center", tracking=4)
    draw_text(c, "TODOS LOS FINALES", Wt / 2, Ht - 140, "anton", 112, "#FFFFFF", 1, align="center", tracking=3)
    draw_text(c, "DE GTA 6", Wt / 2, Ht - 40, "anton", 92, "#FF5A5F", 1, align="center", tracking=4)
