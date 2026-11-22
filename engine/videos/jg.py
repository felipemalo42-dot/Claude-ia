"""SHORT_5 — «GTA 6 tiene 4 videojuegos completos dentro» (9:16). Short independiente, solo GTA 6. Spoiler leve.

Formato: cuenta atrás 4 → 1, estética arcade. Street Trash III: Dezombifier (Video Pump, CC BY 4.0: Jason lo juega en el sofá con
Cal), Time Jackers, Tenebrae Lux y Bang! For Your Buck (IGN, «GTA 6: Playing Every Arcade and Console Game», 4K). Nombres
comprobados en pantalla (el título de la máquina es «BANG! FOR YOUR BUCK»; la descripción de IGN dice «Bank» por error) y géneros
según IGN y las guías (PowerPyx, Mobalytics, Kotaku). Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
IGN = "P-BbiYUPD-o"
VPG = (0.0, 0.12, 0.88, 0.75)   # sin los subtítulos y el logo que la edición de Video Pump lleva incrustados
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)

beat("GTA 6 tiene cuatro videojuegos completos dentro. Y no son minijuegos de relleno.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"c:vpGame@4.0", crop=VPG, top="UN JUEGO DENTRO DEL JUEGO"), S("Y no son", f"c:{IGN}@2563.0", top="CUATRO JUEGOS COMPLETOS")],
     sfx=[(0.0, "riser", 0.3), ("w:cuatro videojuegos", "stamp", 0.45)])
beat("Cuatro: Street Trash Tres. Un juego de zombis visto desde arriba, que Jason juega en el sofá con su amigo Cal.", exag=0.7, id="s2",
     shots=[N(None, "4", "STREET TRASH III"), S("Un juego de zombis", "c:vpGame@15.8", crop=VPG, top="STREET TRASH III: DEZOMBIFIER"),
            S("que Jason juega", "c:vpGame@25.2", crop=VPG, top="JASON Y CAL, EN EL SOFÁ")],
     sfx=[("w:Cuatro", "ding", 0.4)])
beat("Tres: Time Jackers. Un shooter cyberpunk, también visto desde arriba, y lleno de neones.", exag=0.7, id="s3",
     shots=[N(None, "3", "TIME JACKERS"), S("Un shooter", f"c:{IGN}@1213.0", top="TIME JACKERS"), S("y lleno de neones", f"c:{IGN}@1365.0", top="TIME JACKERS")],
     sfx=[("w:Tres", "ding", 0.4)])
beat("Dos: Tenebrae Lux. En blanco y negro, lento y misterioso: una parodia de los juegos de exploración más pretenciosos.", exag=0.7, id="s4",
     shots=[N(None, "2", "TENEBRAE LUX"), S("En blanco y negro", f"c:{IGN}@1965.0", top="TENEBRAE LUX"), S("una parodia", f"c:{IGN}@2189.0", top="TENEBRAE LUX")],
     sfx=[("w:Dos", "ding", 0.4)])
beat("Y uno: Bang For Your Buck. Una máquina recreativa de caza, que hay que buscar por el mapa.", exag=0.7, id="s5",
     shots=[N(None, "1", "BANG! FOR YOUR BUCK"), S("Una máquina", f"c:{IGN}@2490.0", top="BANG! FOR YOUR BUCK"), S("de caza", f"c:{IGN}@2567.0", top="BANG! FOR YOUR BUCK")],
     sfx=[("w:Y uno", "ding", 0.45)])
beat("¿Cuál jugarías primero? Te leo en los comentarios.", exag=0.65, hold=1.4, id="s6",
     shots=[S(None, "g:sq", lines=["¿CUÁL JUGARÍAS", "PRIMERO?"], sub="Juegos reales dentro de GTA 6", hl=[1])],
     sfx=[(0.0, "pop", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("tension", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[5]["start"], 1)], seed=8470)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "jg", "SHORT_5_GTA6_JUEGOS_DENTRO", "tension", "arcade", "GTA 6 · ARCADE"
TITLE = "GTA 6 tiene 4 videojuegos completos dentro"

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
