"""SHORT_4 — «GTA 6 te lo avisa: con seis estrellas, escapar es imposible» (9:16). Short independiente, solo GTA 6.

Partida real (GameV, «Can a TANK Survive a 6-STAR Police Chase in GTA 6?», 18/11/2026, 4K). Lo nuevo: el texto literal que el
juego muestra al llegar a seis estrellas («You now have a 6-star wanted level. Escape is impossible, and the cops won't give up
until you're hunted down.», en pantalla de 1:24 a 1:28) y el aviso del rastreador militar del tanque («This vehicle has a military
tracker installed. Cops will always be able to locate it.»). Ninguna web consultada cita el mensaje de seis estrellas palabra por
palabra. Desenlace real: pantalla de muerte en mitad de un puente (4:04). Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
TAN = "-UuHA1h-Cf8"

beat("Cuando llegas a seis estrellas en GTA 6, el juego te muestra este mensaje.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"v:{TAN}@146.0@0.5", prueba="6 ESTRELLAS", lado="acusacion"),
            S("este mensaje", f"c:{TAN}@83.4", crop=(0.0, 0.22, 0.40, 0.50), top="MENSAJE DEL JUEGO")],
     sfx=[(0.0, "riser", 0.3), ("w:este mensaje", "alarm", 0.35)])
beat("«Ahora tienes seis estrellas. Escapar es imposible, y la policía no se rendirá hasta darte caza».", exag=0.7, id="s2",
     shots=[S("y la policía", f"v:{TAN}@89.0@0.5")],
     sfx=[("w:imposible", "stamp", 0.45)])
beat("Pero este jugador ya iba avisado. Al robar el tanque, el juego le había dicho otra cosa: lleva un rastreador militar, y la policía siempre sabrá dónde está.", exag=0.7, id="s3",
     shots=[S(None, f"v:{TAN}@2.0@0.5"), S("Al robar el tanque", f"v:{TAN}@15.5@0.5"),
            S("lleva un rastreador", f"c:{TAN}@28.2", crop=(0.0, 0.17, 0.40, 0.42), top="AVISO DEL JUEGO")],
     sfx=[("w:rastreador", "pop", 0.4)])
beat("Aun así, lo intentó: puentes, helicópteros, y el ejército detrás, sin descanso.", exag=0.7, id="s4",
     shots=[S(None, f"v:{TAN}@120.0@0.5"), S("puentes", f"v:{TAN}@170.0@0.5"), S("helicópteros", f"v:{TAN}@205.0@0.5"),
            S("y el ejército", f"v:{TAN}@228.5@0.5")],
     sfx=[("w:helicópteros", "whoosh", 0.35)])
beat("¿Y el mensaje? Tenía razón. En mitad de un puente, se acabó.", exag=0.7, id="s5",
     shots=[S(None, f"v:{TAN}@233.6@0.5"), S("En mitad de un puente", f"v:{TAN}@238.6@0.5"), S("se acabó", f"v:{TAN}@243.4@0.5")],
     sfx=[("w:se acabó", "impact", 0.5)])
beat("¿Tú habrías llegado más lejos? Te leo en los comentarios.", exag=0.65, hold=1.4, id="s6",
     shots=[S(None, "g:sq", lines=["¿HABRÍAS LLEGADO", "MÁS LEJOS?"], sub="Más GTA 6 con partidas reales · sin spoilers", hl=[1])],
     sfx=[(0.0, "pop", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("tension", total + 1.0, energy=[(0.0, 2), (beats_tl[3]["start"], 3), (beats_tl[5]["start"], 1)], seed=8430)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD = "tk", "SHORT_4_GTA6_ESCAPAR_ES_IMPOSIBLE", "tension"
TITLE = "GTA 6 te lo avisa: con seis estrellas, escapar es imposible"

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
