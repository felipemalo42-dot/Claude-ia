"""SHORT_6 — «Reseña: el tour de buceo de GTA 6 (una estrella)» (9:16). Short independiente, solo GTA 6. CON SPOILERS (misión).

Formato: reseña de una estrella. Partida real (Video Pump, «GTA 6 Treasure Dive Gone Wrong», CC BY 4.0) de la misión del tour de
buceo del primer capítulo. Frases citadas: las que salen en los subtítulos del vídeo. Lo de la tapadera (permiso revocado y la
despedida de soltero), según las guías (VGC, games.gg). Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
DV = (0.04, 0.13, 0.88, 0.75)   # sin los subtítulos, el título y el logo que la edición de Video Pump lleva incrustados
def D(anchor, t, top, **k): return S(anchor, f"c:vpDive@{t}", crop=k.pop("crop", DV), top=top, **k)

beat("Reseña de un tour de buceo en GTA 6. Nota: una estrella.", pre=0.15, exag=0.7, id="s1",
     shots=[D(None, 38.5, "TOUR DE BUCEO · GTA 6"), S("Nota", "g:review", kicker="RESEÑA · CON SPOILERS", title="TOUR DE BUCEO EN GTA 6", stars=1, sub="Misión del primer capítulo")],
     sfx=[(0.0, "riser", 0.3), ("w:una estrella", "stamp", 0.45)])
beat("Para empezar, el capitán bromea con que ha hecho un agujero en el barco.", exag=0.7, id="s2",
     shots=[D(None, 4.2, "EL CAPITÁN", say="I just put a hole in the boat.")],
     sfx=[("w:agujero", "impact", 0.35)])
beat("Luego le pregunta al guía quién es. Respuesta: «Nadie. Solo el guía de buceo». Es Jason.", exag=0.7, id="s3",
     shots=[D(None, 6.6, "EL CAPITÁN"), D("Respuesta", 8.6, "EL GUÍA", say="Nobody, bud. Just the dive guide."), D("Es Jason", 10.6, "ES JASON")],
     sfx=[("w:Es Jason", "pop", 0.4)])
beat("Y es que el tour es una tapadera: según las guías, al capitán le quitaron el permiso para buscar tesoros, y usa una despedida de soltero como excusa.", exag=0.7, id="s4",
     shots=[D(None, 13.6, "LA TAPADERA"), D("y usa una despedida", 27.4, "LA DESPEDIDA DE SOLTERO")],
     sfx=[("w:tapadera", "pop", 0.35)])
beat("Bajo el agua, el guía deja solos a los turistas y se va directo a por el oro. Doblones españoles, dicen a bordo.", exag=0.7, id="s5",
     shots=[D(None, 44.0, "BAJO EL AGUA"), D("se va directo", 63.0, "+ GOLD DOUBLOONS"), D("Doblones", 88.6, "DOBLONES ESPAÑOLES", say="I think these might be Spanish doubloons.")],
     sfx=[("w:oro", "ding", 0.45)])
beat("¿Resultado? Los turistas no terminan el tour, y se despiden como «hermanos de buceo». ¿Tú le darías más de una estrella?", exag=0.65, hold=1.4, id="s6",
     shots=[D(None, 92.0, "NI LA MITAD DEL TOUR", say="We didn't even get to finish the tour."), D("y se despiden", 108.4, "«DIVE BROS»"),
            S("¿Tú le darías", "g:review", kicker="TU NOTA", title="¿MÁS DE UNA ESTRELLA?", stars=1, sub="Te leo en los comentarios")],
     sfx=[("w:hermanos", "pop", 0.4)])

def music_fn(total, beats_tl):
    y = audio.compose("tropical", total + 1.0, energy=[(0.0, 2), (beats_tl[2]["start"], 1), (beats_tl[4]["start"], 2)], seed=8480)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "tb", "SHORT_6_GTA6_TOUR_DE_BUCEO", "tropical", "playa", "GTA 6 · RESEÑA"
TITLE = "Reseña: el tour de buceo de GTA 6 (spoiler)"

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
