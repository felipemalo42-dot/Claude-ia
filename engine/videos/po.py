"""SHORT_12 — «El portal a la Vice City de PS2» (9:16). Solo GTA 6.

Partida real: IGN, «GTA 6 - How to Find the PS2 Vice City Easter Egg» (25/11/2026, 4K); el secreto lo resolvió Memeio
(se le reconoce en la descripción). Se ve: la torre de radio, las subestaciones con sus letras y botones, el mensaje «U-235
REACTOR2», el salto sobre la central, el portal de rayos y la Vice City con aspecto de 2002. Sin crédito en pantalla."""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)   # la voz de siempre (las rondas de repetición usan estos ajustes)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)
P = "gNMTCbS8Ytg"

beat("En GTA 6 hay un portal… ¡a la Vice City de PlayStation 2!", id="s1", pre=0.1,
     shots=[S(None, f"c:{P}@470.4", top="UN PORTAL"), S("a la Vice City", f"c:{P}@478.0", top="VICE CITY · 2002")],
     sfx=[(0.0, "riser", 0.35), ("w:PlayStation", "impact", 0.5)])
beat("Pero abrirlo es el reto más difícil del juego. Primero, sube a la torre de radio de Key Lento y activa el interruptor.", id="s2",
     shots=[S(None, f"c:{P}@40.4", top="EL RETO"), S("activa el interruptor", f"c:{P}@48.2", top="LA TORRE DE RADIO")],
     sfx=[("w:Primero", "ding", 0.45)])
beat("Luego vienen doce subestaciones eléctricas. Sus letras, juntas, forman un truco de la Vice City original: el que adelantaba el tiempo.", id="s3",
     shots=[S(None, f"c:{P}@54.0", top="12 SUBESTACIONES"), S("Sus letras", f"c:{P}@91.0", top="LAS LETRAS"), S("un truco", "g:sq", lines=["LIFE IS", "PASSING ME BY"], hl=[1], y=700)],
     sfx=[("w:truco", "stamp", 0.45)])
beat("En cada una pulsas un botón, en el orden de ese truco. Sin viajar rápido, sin morir… y sin que te arresten.", id="s4",
     shots=[S(None, f"c:{P}@58.0", top="EN ORDEN"), S("Sin viajar rápido", f"c:{P}@71.5", top="SIN ATAJOS")],
     sfx=[])
beat("Si lo haces bien, te llega un mensaje: «Reactor 2».", id="s5",
     shots=[S(None, f"c:{P}@421.0", top="EL MENSAJE")],
     sfx=[("w:Reactor", "ding", 0.5)])
beat("Esa noche, en la central eléctrica, se abre un portal de rayos…", id="s6",
     shots=[S(None, f"c:{P}@452.0", top="LA CENTRAL"), S("se abre", f"c:{P}@466.0", top="EL PORTAL")],
     sfx=[("w:rayos", "impact", 0.45)])
beat("…y al cruzarlo, ¡todo se ve como en 2002!", id="s7",
     shots=[S(None, f"c:{P}@484.0", top="COMO EN 2002")],
     sfx=[("w:2002", "whoosh", 0.4)])
beat("Y vuelves con la camisa hawaiana de Tommy Vercetti.", id="s8",
     shots=[S(None, f"c:{P}@4.0", crop=(0.0, 0.0, 1.0, 0.80), top="LA CAMISA DE TOMMY")],
     sfx=[])
beat("¿Lo intentarías? Suscríbete para más secretos de GTA 6, ¡y dale like si jugaste la Vice City original!", id="s9", hold=1.6,
     shots=[S(None, f"c:{P}@501.0", top="¿LO INTENTARÍAS?"), S("Suscríbete", "g:sub", lines=["Más secretos de GTA 6", "con partidas reales"])],
     sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("synthwave", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[-1]["start"], 1)], seed=8630)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "po", "SHORT_12_GTA6_PORTAL_VICE_CITY_PS2", "synthwave", "neon", "GTA 6 · PORTAL"
TITLE = "El portal a la Vice City de PS2 en GTA 6"

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.makedirs(os.path.join(_ROOT, FOLDER, "trabajo"), exist_ok=True)
VIDEO = dict(id=VID, folder=FOLDER, file="SHORT_FINAL", res_dir="trabajo", theme=THEME, header=HEADER, credit=False,
             title=TITLE, format="Short (9:16, 1080×1920, 30 fps)", music=MOOD, music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.36, duck=0.24, duck_release=0.9, sfx_gain=0.6, size=(1080, 1920),
             pause_mul=0.9,   # pausas algo más cortas que en los vídeos largos, sin acelerar la voz
             expr_pick=dict(seeds=4, confs=[(0.6, 0.4), (0.7, 0.45)]),   # 8 tomas por frase: se elige la más animada (voice_expr.py)
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav="trabajo/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="trabajo/PORTADA.png"))
THUMB_MARK = None
