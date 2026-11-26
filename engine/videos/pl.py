"""VIDEO_LARGO_6 — «La policía de GTA 6: qué significa cada estrella (y cómo escapar siempre)». Sin spoilers de la historia.

Fuente de imagen: Cynic, «How GTA 6's Wanted System Actually Works» (24/11/2026, 4K), partida real con los iconos de búsqueda,
el mapa de zonas calientes, la leyenda del juego («Appearance recognized», «Recorded by CCTV»…), un robo con cámaras, alarma y caja
fuerte, y huidas por la azotea y en coche. Datos: lo que se ve en esa partida y su explicación transcrita (sus consejos se cuentan
como consejos, no como reglas oficiales de Rockstar). Créditos en la descripción, no en pantalla.
"""
import os
import numpy as np
import audio
from videos import dc_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
P = "rK6MXJpcaIA"
def X(t, **k): return S(None, f"x:{P}@{t}", z=(1.0, 1.05), **k)
def XA(anchor, t, **k): return S(anchor, f"x:{P}@{t}", z=(1.0, 1.05), **k)

# ================================================================ APERTURA
beat("En GTA 6, la policía ya no te olvida solo porque te escondas detrás de un edificio. Las estrellas cambian de color, de forma… y cada detalle te dice qué sabe la policía de ti. Si aprendes a leerlas, escapas siempre.",
     pre=0.3, id="o01", mus=("tension", 2),
     shots=[X(18.0), XA("Las estrellas", 66.0), S("Si aprendes", "g:cover", kicker="GUÍA SIN SPOILERS", lines=["LA POLICÍA", "DE GTA 6"], sub="Qué significa cada estrella y cómo escapar")],
     sfx=[(0.0, "riser", 0.35), ("w:escapas", "stamp", 0.5)])
beat("En este vídeo te explico qué significa cada estrella, cada icono, y los trucos para hacer un robo limpio y desaparecer. Todo con partidas reales.",
     id="o02", mus=("tension", 1),
     shots=[X(112.0), XA("un robo limpio", 420.0)], sfx=[])

# ================================================================ 1. SEIS ESTRELLAS
beat("Lo primero: ahora hay hasta seis estrellas. Cuantas más tengas, más agentes vienen… y mejor armados: chalecos antibalas, cascos, fusiles de asalto, equipos especiales y helicópteros.",
     id="c1a", chapter=(1, "SEIS ESTRELLAS"), mus=("tension", 2),
     shots=[X(4.0), XA("más agentes", 32.0), XA("helicópteros", 832.0)], sfx=[("w:seis estrellas", "stamp", 0.45)])

# ================================================================ 2. LOS COLORES
beat("Pero lo importante no es cuántas estrellas tienes, sino cómo se ven. Si son grises, la policía ya viene en camino: alguien denunció un delito. Ese es el mejor momento para irte, antes de que lleguen.",
     id="c2a", chapter=(2, "CÓMO LEER LAS ESTRELLAS"), mus=("tension", 2),
     shots=[X(62.0), XA("Si son grises", 64.0), XA("el mejor momento", 8.0)], sfx=[("w:grises", "ding", 0.4)])
beat("Si las estrellas están huecas, con el borde blanco, la policía llegó pero no sabe quién es el sospechoso. Puedes pasar a su lado y no te reconocerán, si no llamas la atención.",
     id="c2b", mus=("tension", 2),
     shots=[X(78.0), XA("Puedes pasar a su lado", 16.0)], sfx=[])
beat("Si son blancas y sólidas, te persiguen y te están viendo. Y si se ven blancas pero apagadas, siguen buscándote… pero te perdieron de vista. Es tu oportunidad.",
     id="c2c", mus=("tension", 3),
     shots=[X(96.0), XA("apagadas", 100.0), XA("Es tu oportunidad", 128.0)], sfx=[("w:oportunidad", "whoosh", 0.4)])
beat("Y luego están las rojas. Cuando la policía te pierde, marca en el mapa una zona caliente en rojo, donde te siguen buscando. Si estás justo en tu última ubicación conocida, las estrellas se ponen rojas y sólidas. Si estás dentro de la zona pero más lejos, se ven huecas con el borde rojo.",
     id="c2d", mus=("tension", 2),
     shots=[X(160.0), XA("Si estás justo", 208.0), XA("Si estás dentro de la zona", 176.0)], sfx=[("w:rojas", "stamp", 0.45)])
beat("Fíjate también en el minimapa. Cuando denuncian un delito, aparece un círculo azul oscuro donde pasó, y otro más claro alrededor: si estás dentro, te pueden ver como sospechoso. Cuando la policía ya tiene tu descripción, el círculo se vuelve rojo.",
     id="c2f", mus=("tension", 2),
     shots=[X(884.0), XA("Cuando la policía", 896.0)], sfx=[("w:rojo", "stamp", 0.4)])
beat("Un truco: si ves que esas estrellas rojas parpadean en blanco, un agente está a punto de reconocerte. Sal de ahí.",
     id="c2e", mus=("tension", 3),
     shots=[X(192.0)], sfx=[("w:Sal de ahí", "alarm", 0.35)])

# ================================================================ 3. LOS ICONOS
beat("Al lado de las estrellas aparecen iconos con lo que la policía sabe de ti. El juego tiene siete: tu cara, tu ropa, tu vehículo, un arma a la vista, tu pareja reconocida, y si te grabó una cámara de seguridad… o una cámara conectada a la nube.",
     id="c3a", chapter=(3, "LO QUE SABEN DE TI"), mus=("synthwave", 2),
     shots=[X(316.0), XA("El juego tiene siete", 320.0)], sfx=[("w:siete", "ding", 0.45)])
beat("Y cada pista se puede borrar. Si conocen tu cara, ponte o quítate un sombrero, unas gafas, una máscara, o cámbiate el peinado. Si conocen tu ropa, cámbiate: puedes llevar otra en el maletero.",
     id="c3b", mus=("synthwave", 2),
     shots=[X(336.0), XA("cámbiate", 352.0)], sfx=[])
beat("Si conocen tu vehículo, píntalo en un taller o simplemente roba otro donde no te vean. Y si abandonas tu coche, mira lo que pasa: la policía lo encuentra, acordona la zona… y se lo lleva al depósito.",
     id="c3c", mus=("synthwave", 2),
     shots=[X(368.0), XA("Y si abandonas", 384.0), XA("se lo lleva", 512.0)], sfx=[])

# ================================================================ LLAMADA A MITAD
beat("Por cierto: si esta guía te está ayudando, dale like y suscríbete a Sal y Asfalto. Así sabemos que quieres más guías de GTA 6 con partidas reales.",
     id="cta", cta=True, mus=("tropical", 1),
     shots=[X(288.0), XA("dale like", 304.0)], sfx=[("w:dale like", "ding", 0.45), ("w:suscríbete", "pop", 0.45)])

# ================================================================ 4. EL ROBO LIMPIO
beat("Ahora, lo bueno: cómo robar una tienda sin que te atrapen. Antes de entrar, mantén pulsados los dos sticks para concentrarte: el juego te marca si hay cámaras dentro.",
     id="c4a", chapter=(4, "EL ROBO LIMPIO"), mus=("tension", 2),
     shots=[X(412.0), XA("el juego te marca", 448.0)], sfx=[("w:cámaras", "ding", 0.4)])
beat("Si vas con tu pareja, uno controla a la gente mientras el otro va a la trastienda, destruye la grabación de las cámaras y desactiva la alarma. Así nadie da tu descripción.",
     id="c4b", mus=("tension", 3),
     shots=[X(432.0), XA("va a la trastienda", 528.0), XA("destruye la grabación", 576.0)], sfx=[("w:alarma", "alarm", 0.3)])
beat("Para la caja fuerte tienes tres opciones: amenazar al cajero para que te dé el código, buscar una nota con el código escondida en la tienda… o volarla con un explosivo, haciendo algo de ruido.",
     id="c4c", mus=("tension", 2),
     shots=[X(544.0), XA("buscar una nota", 560.0), XA("volarla", 1088.0)], sfx=[("w:explosivo", "impact", 0.45)])
beat("Hazlo así y puedes volver al rato y sentarte al lado de un coche patrulla sin que nadie sepa que fuiste tú. Pero ojo: si la cámara estaba conectada a la nube, tu ropa ya la tienen, aunque destruyas la grabación del local.",
     id="c4d", mus=("tension", 1),
     shots=[X(592.0), XA("Pero ojo", 464.0)], sfx=[])
beat("Y un consejo más: roba con pistola, no con un fusil. Un arma grande llama mucho más la atención. Si te buscan por el fusil, guárdalo en el maletero de cualquier coche, o suéltalo desde la rueda de armas. Si lo compraste, no lo pierdes: vuelve a tu arsenal.",
     id="c4e", mus=("tension", 2),
     shots=[X(600.0), XA("guárdalo en el maletero", 1072.0), XA("o suéltalo", 640.0)], sfx=[])

# ================================================================ 5. JOYERÍAS
beat("Antes de un golpe grande, mira el mapa: cada tienda te dice cuánto podrías sacar y cuánta seguridad tiene. Y revisa la salida: algunos sitios tienen un portón de hierro que se abre con un botón, y con el coche no lo vas a atravesar.",
     id="c5p", chapter=(5, "JOYERÍAS Y BANDAS"), mus=("tension", 2),
     shots=[X(1056.0), XA("Y revisa la salida", 1040.0)], sfx=[])
beat("En una joyería, impón el control desde el primer segundo: noquea al guardia y haz que el otro suelte el arma. Noquéalos, no dispares: hace ruido y la gente entra en pánico. Y si solo puedes elegir una cosa, ve a por la caja fuerte: es lo que más vale.",
     id="c5j", mus=("tension", 3),
     shots=[X(992.0), XA("Noquéalos", 1008.0), XA("ve a por la caja fuerte", 1090.0)], sfx=[("w:noquea", "impact", 0.4)])
beat("Vigila también a la gente: si alguien sale corriendo por la puerta, es un testigo, y la policía llegará antes.",
     id="c5w", mus=("tension", 2),
     shots=[X(1024.0)], sfx=[])
beat("¿Y si asaltas el escondite de una banda? Aunque oigas que llega la policía, no te asustes: primero montan un perímetro, te dan órdenes para que salgas y te avisan antes de entrar. Y aun dentro, no van a por ti hasta que te ven… o hasta que les disparas.",
     id="c5g", mus=("storm", 2),
     shots=[X(1152.0), XA("primero montan un perímetro", 1168.0), XA("hasta que te ven", 1200.0)], sfx=[])

# ================================================================ 6. LA HUIDA
beat("¿Y si todo sale mal? Lo primero: no te pares a pelear. El sistema está hecho para frenarte, y cada segundo que te quedas llegan más refuerzos con más potencia de fuego.",
     id="c5a", chapter=(6, "LA HUIDA"), mus=("storm", 3),
     shots=[X(960.0), XA("El sistema está hecho", 896.0)], sfx=[("w:refuerzos", "alarm", 0.35)])
beat("Si te persiguen en coche, dispara a las ruedas. Y si hay un helicóptero, dispárale: se retira o pierde de vista. Además, los helicópteros tienen que irse a repostar… y ese es tu momento.",
     id="c5b", mus=("storm", 3),
     shots=[X(912.0), XA("si hay un helicóptero", 832.0), XA("ese es tu momento", 816.0)], sfx=[])
beat("Si te reconocen a ti y a tu pareja, sepárense: puedes darle la bolsa del botín o un arma. Luego te escribe para quedar o para venderlo; si lo vende ella, ganas un poco menos, pero te ahorras el viaje.",
     id="c5c", mus=("storm", 2),
     shots=[X(704.0), XA("sepárense", 720.0), XA("Luego te escribe", 736.0)], sfx=[])
beat("Y si pierdes al helicóptero de vista, concéntrate: el juego te marca de dónde viene el ruido de las aspas. Escóndete, cámbiate de ropa, vuelve más tarde… y nadie sabrá que fuiste tú.",
     id="c5d", mus=("storm", 2),
     shots=[X(784.0), XA("Escóndete", 800.0), XA("y nadie sabrá", 864.0)], sfx=[])

# ================================================================ CIERRE
beat("En resumen: mira el color de las estrellas, borra cada pista que tengan de ti, y nunca te quedes a pelear si puedes desaparecer.",
     id="r01", mus=("tropical", 1),
     shots=[S(None, "g:list", title="PARA ESCAPAR SIEMPRE", subt="Resumen de la guía",
              items=["Mira el color de las estrellas", "Borra cada pista", "Desaparece, no pelees"], st=[0.6, 2.6, 4.8])], sfx=[])
beat("¿Cuál es tu mejor huida en GTA 6? Cuéntamela en los comentarios. Y si quieres más guías con partidas reales, suscríbete a Sal y Asfalto. Nos vemos en el próximo vídeo.",
     id="r02", mus=("tropical", 1), hold=0.6,
     shots=[X(1120.0), XA("suscríbete", 1104.0), S("Nos vemos", "g:subscribe")], sfx=[("w:suscríbete", "pop", 0.45)])
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
        y = audio.compose(sg["style"], dur, energy=en, seed=8800 + 17 * i, key_shift=0)
        L = len(y); s = int(a0 * audio.SR)
        fi = int((xf if i else 0.05) * audio.SR); y[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.2
        fo = int(xf * audio.SR)
        if i + 1 < len(segs) and L > fo: y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.2
        e = min(n, s + L); out[s:e] += y[: e - s]
    return out / (np.abs(out).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "VIDEO_LARGO_6_GTA6_POLICIA"
for _d in ("trabajo", "trabajo/audio"):
    os.makedirs(os.path.join(_ROOT, FOLDER, _d), exist_ok=True)
VIDEO = dict(id="pl", folder=FOLDER, file="VIDEO_FINAL", res_dir="trabajo", theme="policia", credit=False,
             title="La policía de GTA 6: qué significa cada estrella (y cómo escapar siempre)",
             format="Largo (16:9, 1920×1080, 30 fps) · partida real", music="tension", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.30, duck=0.22, duck_release=0.9, sfx_gain=0.5,
             expr_pick=dict(seeds=2, confs=[(0.6, 0.4), (0.7, 0.45)]),   # 4 tomas por frase: la más animada (voice_expr.py)
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/audio/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", size=(1920, 1080),
             names=dict(narr_wav="trabajo/audio/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="MINIATURA.png"))
THUMB_MARK = None

def thumbnail(c):
    """Fotograma real (huida con la policía) + seis estrellas y «LA POLICÍA DE GTA 6»."""
    import skia
    from gfx import draw_text, rect
    Wt, Ht = 1280, 720; base = os.path.join(_ROOT, FOLDER, "trabajo")
    R._bg(c, os.path.join(base, "miniatura_fondo.png"), 0, 0, Wt, Ht)
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([(0, Ht), (0, Ht - 330)], [skia.Color(4, 8, 18, 245), skia.Color(4, 8, 18, 0)]))
    c.drawRect(skia.Rect.MakeXYWH(0, Ht - 330, Wt, 330), g)
    from videos.ds_render import star
    for k in range(6): star(c, 380 + k * 104, 110, 44, "#FFFFFF" if k < 4 else "#E5484D", 1)
    draw_text(c, "LA POLICÍA", Wt / 2, Ht - 140, "anton", 116, "#FFFFFF", 1, align="center", tracking=3)
    draw_text(c, "DE GTA 6", Wt / 2, Ht - 40, "anton", 92, "#4DA3FF", 1, align="center", tracking=4)
