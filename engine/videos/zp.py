"""SHORT_4 — «Hice zapping en la tele de GTA 6» (9:16). Short independiente, solo GTA 6.

Formato: zapping. Cada canal es una emisión real de la tele del juego, grabada en partida (Video Pump, licencia CC BY 4.0, crédito en
la descripción): el dibujo animado de Weazel (un caimán, un flamenco y un manatí ante el club «Delights»), el anuncio de Big Ball
Burger de la marca Marbles, el abogado «1-9-9-9 BRAD-LAW», Hank's Waffles «Est. 1984» y un western. Solo se cuenta lo que se ve.
Ningún medio consultado recoge estos anuncios. Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
TV = (0.0, 0.03, 1.0, 0.97)
def ST(anchor, ch): return S(anchor, "g:static", ch=ch, nocap=False)
def CH(anchor, vid, t, top, **k): return S(anchor, f"c:{vid}@{t}", crop=k.pop("crop", TV), top=top, **k)

beat("Me puse a hacer zapping en la tele de GTA 6. Y esto es lo que dan.", pre=0.15, exag=0.7, id="s1",
     shots=[CH(None, "vpWestern", 19.5, "LA TELE DE GTA 6"), ST("Y esto", "CH 01")],
     sfx=[(0.0, "riser", 0.3), ("w:zapping", "pop", 0.4)])
beat("Canal uno: un dibujo animado con un caimán, un flamenco y un manatí, aparcando delante de un club de dudosa reputación.", exag=0.7, id="s2",
     shots=[CH(None, "vpWeazel", 9.6, "CANAL 1 · DIBUJOS"), CH("aparcando", "vpWeazel", 3.6, "CANAL 1 · DIBUJOS"),
            CH("de dudosa", "vpWeazel", 6.8, "«DANCERS WANTED»")],
     sfx=[("w:Canal uno", "pop", 0.35)])
beat("Canal dos: un anuncio en el que las hamburguesas se fabrican como canicas. Se llaman Big Ball Burger.", exag=0.7, id="s3",
     shots=[ST(None, "CH 02"), CH("un anuncio", "vpBurger", 3.4, "CANAL 2 · ANUNCIO"), CH("como canicas", "vpBurger", 12.4, "CANAL 2 · ANUNCIO"),
            CH("Se llaman", "vpBurger", 21.6, "BIG BALL BURGER")],
     sfx=[("w:Canal dos", "pop", 0.35)])
beat("Canal tres: un abogado que te busca si sufriste un accidente, y te pide que llames a Brad Law.", exag=0.7, id="s4",
     shots=[ST(None, "CH 03"), CH("un abogado", "vpBradlaw", 11.6, "CANAL 3 · ANUNCIO"), CH("y te pide", "vpBradlaw", 18.4, "1-9-9-9 BRAD-LAW")],
     sfx=[("w:Canal tres", "pop", 0.35), ("w:Brad Law", "ding", 0.4)])
beat("Canal cuatro: el restaurante de Hank, abierto desde mil novecientos ochenta y cuatro. El dueño presume de familia, mientras un empleado está en el baño, bajo un cartel que dice que la familia es para siempre.", exag=0.7, id="s5",
     shots=[ST(None, "CH 04"), CH("el restaurante", "vpWaffles", 24.6, "CANAL 4 · ANUNCIO"), CH("El dueño", "vpWaffles", 0.6, "HANK'S WAFFLES"),
            CH("mientras un empleado", "vpWaffles", 12.6, "«FAMILY... FOREVER»")],
     sfx=[("w:Canal cuatro", "pop", 0.35), ("w:baño", "pop", 0.3)])
beat("Y canal cinco: una película del oeste, con vaqueros, tiroteos… y un vaquero abrazándose con un puma.", exag=0.7, id="s6",
     shots=[ST(None, "CH 05"), CH("una película", "vpWestern", 1.0, "CANAL 5 · WESTERN"), CH("tiroteos", "vpWestern", 15.0, "CANAL 5 · WESTERN"),
            CH("y un vaquero", "vpWestern", 43.6, "CANAL 5 · WESTERN")],
     sfx=[("w:Canal cinco", "pop", 0.35), ("w:tiroteos", "impact", 0.35)])
beat("Todo esto, en una tele que puedes no encender nunca. ¿Qué canal dejarías puesto?", exag=0.65, hold=1.4, id="s7",
     shots=[S(None, "g:sq", lines=["¿QUÉ CANAL", "DEJARÍAS?"], sub="Emisiones reales de la tele de GTA 6", hl=[1])],
     sfx=[(0.0, "pop", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("synthwave", total + 1.0, energy=[(0.0, 2), (beats_tl[2]["start"], 2), (beats_tl[6]["start"], 1)], seed=8460)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "zp", "SHORT_4_GTA6_ZAPPING", "synthwave", "tv", "GTA 6 · ZAPPING"
TITLE = "Hice zapping en la tele de GTA 6"

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.makedirs(os.path.join(_ROOT, FOLDER, "trabajo"), exist_ok=True)
VIDEO = dict(id=VID, folder=FOLDER, file="SHORT_FINAL", res_dir="trabajo", theme=THEME, header=HEADER, credit=False,
             title=TITLE, format="Short (9:16, 1080×1920, 30 fps)", music=MOOD, music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55, size=(1080, 1920),
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav="trabajo/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="trabajo/PORTADA.png"))
THUMB_MARK = None
