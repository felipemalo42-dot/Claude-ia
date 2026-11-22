"""SHORT_6 — «¿Turista o local? GTA 6 te lo dice antes de hablar» (9:16). Short independiente, solo GTA 6.

Partida real (Yamatum O, «พาเที่ยวเมือง Vice City | GTA 6», 19/11/2026). Lo nuevo: la etiqueta que el menú de interacción pone a
cada persona («TOURIST» en la playa, 11:31-11:52; «LOCAL» en el gimnasio de la playa al atardecer, 20:46-21:08); ninguna web
consultada la menciona. Se ve también el orden de las opciones en las dos escenas: primero GREET/TAUNT, después DEFUSE/PROVOKE.
Lo de provocar y calmar, según las guías (gtaboom, dotesports). Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
THA = "gvlY1gVmSKM"
MENU = (0.60, 0.52, 1.0, 1.0)

beat("En GTA 6, antes de hablar con alguien, el juego te dice si es turista… o local.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"c:{THA}@686.0", crop=(0.15, 0.1, 1.0, 1.0), top="PARTIDA REAL · GTA 6"),
            S("turista", f"c:{THA}@696.0", crop=(0.4, 0.3, 1.0, 1.0), top="TOURIST · TURISTA"),
            S("o local", f"c:{THA}@1248.4", crop=(0.3, 0.25, 1.0, 1.0), top="LOCAL")],
     sfx=[(0.0, "riser", 0.3), ("w:turista", "pop", 0.4), ("w:local", "pop", 0.4)])
beat("Esta mujer, en la playa: turista. Este hombre, en el gimnasio de la playa al atardecer: local.", exag=0.7, id="s2",
     shots=[S(None, f"c:{THA}@701.0", crop=(0.25, 0.15, 1.0, 1.0), top="TURISTA"),
            S("Este hombre", f"c:{THA}@1250.5", crop=(0.25, 0.15, 1.0, 1.0), top="LOCAL")],
     sfx=[("w:Este hombre", "whoosh", 0.3)])
beat("Y las opciones cambian: primero, saludar o burlarte; después, calmar o provocar.", exag=0.7, id="s3",
     shots=[S(None, f"c:{THA}@690.9", crop=MENU, top="SALUDAR · BURLARTE"),
            S("después", f"c:{THA}@1253.8", crop=MENU, top="CALMAR · PROVOCAR")],
     sfx=[("w:saludar", "pop", 0.35), ("w:calmar", "pop", 0.35)])
beat("Según las guías, provocar puede acabar en pelea, y calmar sirve cuando alguien ya está enfadado.", exag=0.7, id="s4",
     shots=[S(None, f"c:{THA}@705.5", crop=(0.25, 0.15, 1.0, 1.0), top="SEGÚN LAS GUÍAS")],
     sfx=[("w:pelea", "impact", 0.3)])
beat("¿Y la etiqueta, para qué sirve? No hemos encontrado ninguna explicación oficial.", exag=0.7, id="s5",
     shots=[S(None, f"c:{THA}@1264.6", crop=MENU, top="¿PARA QUÉ SIRVE?")],
     sfx=[("w:explicación", "ding", 0.35)])
beat("¿Tú qué crees que cambia? Te leo en los comentarios.", exag=0.65, hold=1.4, id="s6",
     shots=[S(None, "g:sq", lines=["¿TURISTA", "O LOCAL?"], sub="Más GTA 6 con partidas reales · sin spoilers", hl=[1])],
     sfx=[(0.0, "pop", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("tropical", total + 1.0, energy=[(0.0, 2), (beats_tl[2]["start"], 1), (beats_tl[4]["start"], 2)], seed=8450)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD = "tl", "SHORT_6_GTA6_TURISTA_O_LOCAL", "tropical"
TITLE = "¿Turista o local? GTA 6 te lo dice antes de hablar"

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.makedirs(os.path.join(_ROOT, FOLDER, "trabajo"), exist_ok=True)
VIDEO = dict(id=VID, folder=FOLDER, file="SHORT_FINAL", res_dir="trabajo", theme="combate", header="GTA 6 · PARTIDA REAL", credit=False,
             title=TITLE, format="Short (9:16, 1080×1920, 30 fps)", music=MOOD, music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55, size=(1080, 1920),
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav="trabajo/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="trabajo/PORTADA.png"))
THUMB_MARK = None
