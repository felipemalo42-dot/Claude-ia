"""SHORT_PROMOCIONAL_GTA6 — Short (9:16) que lleva al vídeo largo «GTA 6 te está vigilando».

Sale del mejor momento del vídeo largo (el mensaje de las 6 estrellas y el aviso de «Irredimible»), reestructurado para
el formato corto: gancho → contexto → pregunta → se corta antes de resolver → llamada al vídeo largo.
Mismo material (partida real de IGN, guía de las 6 estrellas, 19/11/2026) en recortes verticales 4K o en tarjeta 16:9.
Planos: S(ancla, fuente) · v:<ID>@<segundo>@<centro x> (recorte vertical) · c:<ID>@<segundo> (tarjeta 16:9) · g:<gráfico>
"""
import os
import numpy as np
import audio
from videos import gs_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
SIX = "Om4W6tYMF-0"

beat("Si ves este mensaje en GTA 6, ya es demasiado tarde.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"c:{SIX}@362.25", crop=(0.0, 0.08, 0.94, 0.86), top="MENSAJE DEL JUEGO")],
     sfx=[(0.0, "alarm", 0.35), ("w:demasiado tarde", "hit", 0.4)])
beat("Aparece cuando llegas a 6 estrellas: escapar es imposible, y la policía no se rendirá hasta darte caza.", exag=0.7, id="s2",
     shots=[S(None, f"c:{SIX}@327.0", crop=(0.45, 0.0, 1.0, 0.62), top="LAS 6 ESTRELLAS"),
            S("escapar es imposible", f"v:{SIX}@355.6@0.42", z=(1.0, 1.06)),
            S("hasta darte caza", f"v:{SIX}@370.0@0.50", z=(1.0, 1.06))],
     sfx=[("w:6 estrellas", "pop", 0.45), ("w:escapar", "whoosh", 0.35)])
beat("No puedes esconderte, ni bajar el nivel de búsqueda. La única salida es morir.", exag=0.7, id="s3",
     shots=[S(None, f"v:{SIX}@373.75@0.50", z=(1.0, 1.06)),
            S("La única salida", f"c:{SIX}@384.0", crop=(0.1, 0.1, 0.9, 0.9))],
     sfx=[("w:morir", "impact", 0.5)])
beat("Pero ojo: morir no lo arregla todo. En esa misma prueba, el juego lanzó otro aviso: Lucía estaba cerca de volverse Irredimible.", exag=0.7, id="s4",
     shots=[S(None, f"v:{SIX}@397.2@0.52", z=(1.0, 1.06)),
            S("En esa misma prueba", f"c:{SIX}@412.4", crop=(0.1, 0.05, 0.9, 0.95)),
            S("Lucía estaba cerca", f"c:{SIX}@403.1", crop=(0.0, 0.16, 0.72, 0.84), top="AVISO DEL JUEGO")],
     sfx=[("w:no lo arregla", "heartbeat", 0.5), ("w:Irredimible", "glitch", 0.4)])
beat("Y eso, según Rockstar, tiene un impacto duradero. ¿Qué es el perfil criminal, y cómo evitas que te marque para siempre?", exag=0.7, id="s5",
     shots=[S(None, "g:sladder"), S("¿Qué es el perfil", "g:squestion")],
     sfx=[(0.0, "whoosh", 0.35), ("w:¿Qué es", "riser", 0.4)])
beat("Te lo explicamos paso a paso, con partidas reales, en nuestro video completo. Tienes el enlace justo aquí abajo.", exag=0.65, hold=1.6, id="s6",
     shots=[S(None, "g:scta", cues=["aquí abajo"])],
     sfx=[(0.0, "pop", 0.45), ("w:aquí abajo", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("tension", total + 1.0, energy=[(0.0, 2), (beats_tl[3]["start"], 1), (beats_tl[4]["start"], 2), (beats_tl[5]["start"], 1)], seed=5207)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = "../VIDEO_LARGO_GTA6/PROYECTO_DE_EDICION/short_promocional"
os.makedirs(os.path.join(_ROOT, "SHORT_PROMOCIONAL_GTA6", WORK), exist_ok=True)

VIDEO = dict(id="gs", folder="SHORT_PROMOCIONAL_GTA6", file="SHORT_FINAL", res_dir=WORK,
             title="Si ves este mensaje en GTA 6, ya es demasiado tarde",
             format="Short (9:16, 1080×1920, 30 fps) · promoción del vídeo largo", music="tension", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55, size=(1080, 1920),
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems=WORK + "/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav=WORK + "/narracion_original.wav", narr_mp3="NARRACION.mp3", srt="SUBTITULOS.srt",
                        script=WORK + "/guion_con_tiempos.txt", thumb="PORTADA.png"))
THUMB_MARK = None

def thumbnail(c):
    R.cover(c)
