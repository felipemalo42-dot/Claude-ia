"""SHORT_8 — «3 cosas GRATIS al empezar GTA 6» (9:16). Short independiente, solo GTA 6.

Guías reales de IGN: el lanzacohetes Hauners H-AT en la caravana con búnker junto al campo de tiro Griffin (con sus cuatro cohetes y
el aviso de guardar antes de disparar), la pista de Southwind con aviones y helicóptero sin policía (y las cuatro estrellas si vuelas
sobre la base militar) y la fábrica al este de Hamlet con un botín de unos 7.000 dólares que se repone al alejarte y volver.
Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=1.0, cfg=0.3)   # voz más expresiva (parámetros de Chatterbox para habla animada)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
R1, PL, PV, MO = "igRocket", "QBMZ1ZXlflk", "igPlaneV", "NKq2GOBaJV8"
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)

beat("Tres cosas gratis que puedes conseguir al empezar GTA 6. ¡Y la tercera te llena los bolsillos!", pre=0.1, id="s1",
     shots=[S(None, f"c:{R1}@45.6", top="3 COSAS GRATIS"), S("la tercera", f"c:{MO}@37.0", top="¿DINERO INFINITO?")],
     sfx=[(0.0, "riser", 0.35), ("w:bolsillos", "coin", 0.5)])
beat("Uno: un lanzacohetes. Está en una caravana llena de antenas, en un depósito de coches junto al campo de tiro Griffin. Abres la trampilla del búnker… ¡y ahí está, con cuatro cohetes!", id="s2",
     shots=[N(None, "1", "LANZACOHETES"), S("Está en una caravana", f"c:{R1}@23.6", top="LA CARAVANA"), S("en un depósito", f"c:{R1}@19.2", top="EL DEPÓSITO"),
            S("Abres la trampilla", f"c:{R1}@27.6", top="EL BÚNKER"), S("y ahí está", f"c:{R1}@31.0", top="HAUNERS H-AT")],
     sfx=[("w:Uno", "ding", 0.45), ("w:cuatro cohetes", "impact", 0.45)])
beat("Ojo: no puedes comprar más munición, así que guarda la partida antes de disparar.", id="s3",
     shots=[S(None, f"c:{R1}@40.6", top="GUARDA ANTES DE DISPARAR")], sfx=[("w:Ojo", "pop", 0.4)])
beat("Dos: un avión. En una pista de Southwind, al suroeste de Key Lento, hay aviones y un helicóptero, sin policía. Eso sí: no vueles sobre la base militar de al lado, ¡o te caen cuatro estrellas!", id="s4",
     shots=[N(None, "2", "UN AVIÓN"), S("En una pista", f"c:{PL}@38.6", top="SOUTHWIND"), S("sin policía", f"c:{PV}@4.0", top="GRATIS Y SIN POLICÍA"),
            S("no vueles", f"c:{PL}@46.0", top="CUIDADO CON LA BASE")],
     sfx=[("w:Dos", "ding", 0.45), ("w:cuatro estrellas", "alarm", 0.35)])
beat("Y tres: dinero que se repone. En una fábrica al este de Hamlet hay un botín de unos siete mil dólares. Te alejas un poco, vuelves… ¡y está otra vez! Eso sí: puede que lo arreglen pronto.", id="s5",
     shots=[N(None, "3", "DINERO"), S("En una fábrica", f"c:{MO}@17.0", top="LA FÁBRICA"), S("siete mil", f"c:{MO}@41.0", top="UNOS 7.000 $"),
            S("Te alejas", f"c:{MO}@47.0", top="TE ALEJAS…"), S("y está otra vez", f"c:{MO}@54.6", top="…Y VUELVE A ESTAR")],
     sfx=[("w:Y tres", "ding", 0.45), ("w:siete mil", "coin", 0.5)])
beat("¿Cuál vas a probar primero? Suscríbete para más trucos de GTA 6, ¡y dale like para que llegue a más gente!", hold=1.6, id="s6",
     shots=[S(None, "g:sub", lines=["Más trucos de GTA 6", "con partidas reales"])], sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("dembow", total + 1.0, energy=[(0.0, 3), (beats_tl[5]["start"], 2)], seed=8520)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "gr", "SHORT_8_GTA6_3_COSAS_GRATIS", "dembow", "combate", "GTA 6 · TRUCOS"
TITLE = "3 cosas GRATIS al empezar GTA 6"

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.makedirs(os.path.join(_ROOT, FOLDER, "trabajo"), exist_ok=True)
VIDEO = dict(id=VID, folder=FOLDER, file="SHORT_FINAL", res_dir="trabajo", theme=THEME, header=HEADER, credit=False,
             title=TITLE, format="Short (9:16, 1080×1920, 30 fps)", music=MOOD, music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.36, duck=0.24, duck_release=0.9, sfx_gain=0.6, size=(1080, 1920),
             tempo=1.15, pause_mul=0.65,   # voz de Shorts: más ritmo (estiramiento con timbre intacto) y pausas más cortas
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav="trabajo/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="trabajo/PORTADA.png"))
THUMB_MARK = None
