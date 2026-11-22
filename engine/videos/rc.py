"""SHORT_5 — «El consejo de GTA 6 cuando robas un avión de combate» (9:16). Short independiente, solo GTA 6.

Partida real de la guía de IGN «GTA 6: You Can Steal a Fighter Jet in Chapter 1 (But Probably Shouldn't)» (20/11/2026, 4K).
Lo nuevo: el consejo que el juego muestra al despegar («Flying at a lower altitude can reduce your chance of being spotted by law
enforcement.», 2:41-2:47); ninguna web consultada lo menciona para GTA 6. Además: cinco estrellas al subir al blindado, el salto
sobre la valla que el juego marca como «Stunt Jump failed» (1:38) y el derribo («la policía de la diversión», en palabras de la
guía). Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
JET = "4HCd052lpnA"

beat("Si robas un avión de combate en GTA 6, el juego te da este consejo.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"v:{JET}@131.0@0.38", prueba="ROBAR UN CAZA", lado="acusacion"),
            S("este consejo", f"c:{JET}@161.2", crop=(0.0, 0.22, 0.42, 0.44), top="CONSEJO DEL JUEGO")],
     sfx=[(0.0, "riser", 0.3), ("w:este consejo", "ding", 0.4)])
beat("«Volar a menos altura puede reducir la probabilidad de que la policía te vea».", exag=0.7, id="s2",
     shots=[], sfx=[("w:menos altura", "whoosh", 0.3)])
beat("Pero llegar hasta el avión es otra historia. En cuanto subes a un blindado del ejército, cinco estrellas de golpe.", exag=0.7, id="s3",
     shots=[S(None, f"v:{JET}@60.2@0.48"), S("En cuanto subes", f"v:{JET}@73.4@0.55"),
            S("cinco estrellas", f"v:{JET}@82.6@0.5", prueba="5 ESTRELLAS", lado="acusacion")],
     sfx=[("w:cinco estrellas", "alarm", 0.3)])
beat("Para entrar en la base hay un salto sobre la valla. Este jugador lo hizo, y el juego lo marcó como salto acrobático fallido.", exag=0.7, id="s4",
     shots=[S(None, f"v:{JET}@87.6@0.5"), S("Este jugador lo hizo", f"c:{JET}@92.2", top="EL SALTO SOBRE LA VALLA"),
            S("salto acrobático fallido", f"c:{JET}@97.4", crop=(0.5, 0.2, 1.0, 0.62), top="«STUNT JUMP FAILED»")],
     sfx=[("w:salto sobre", "whoosh", 0.35), ("w:fallido", "pop", 0.4)])
beat("Y cuando por fin despegas, la libertad dura unos segundos, hasta que te derriba lo que una guía llamó «la policía de la diversión».", exag=0.7, id="s5",
     shots=[S(None, f"v:{JET}@167.8@0.45")],
     sfx=[("w:despegas", "whoosh", 0.4), ("w:derriba", "impact", 0.5)])
beat("¿Tú habrías volado más bajo? Te leo en los comentarios.", exag=0.65, hold=1.4, id="s6",
     shots=[S(None, "g:sq", lines=["¿HABRÍAS VOLADO", "MÁS BAJO?"], sub="Más GTA 6 con partidas reales · sin spoilers", hl=[1])],
     sfx=[(0.0, "pop", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("tension", total + 1.0, energy=[(0.0, 2), (beats_tl[2]["start"], 3), (beats_tl[5]["start"], 1)], seed=8440)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD = "rc", "SHORT_5_GTA6_VUELA_BAJO", "tension"
TITLE = "El consejo de GTA 6 cuando robas un avión de combate"

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
