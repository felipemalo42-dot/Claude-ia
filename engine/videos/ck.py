"""SHORT_11 — «El barco fantasma de GTA 6» (9:16). Solo GTA 6.

Partida real: IGN, «GTA 6: How to Get the Cursed Knife | Ghost Ship Lighthouse Easter Egg» (24/11/2026, 4K). Todo lo que se
cuenta se ve: el faro de noche, los dos fantasmas y el empujón, la foto, el libro en la chimenea, el buceo entre la niebla, el bote
hundido con el cuchillo verde y el barco fantasma con los binoculares. Sin crédito en pantalla (va en la descripción)."""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)   # la voz de siempre (las rondas de repetición usan estos ajustes)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)
K = "IqKb-yJGroE"

beat("A medianoche, en un faro de GTA 6, pasa algo que no deberías ver.", id="s1", pre=0.1,
     shots=[S(None, f"c:{K}@12.2", top="MEDIANOCHE"), S("pasa algo", f"c:{K}@3.6", top="EL FARO")],
     sfx=[(0.0, "riser", 0.35), ("w:no deberías", "heartbeat", 0.45)])
beat("Sube hasta arriba: dos fantasmas discuten… ¡y uno empuja al otro al vacío!", id="s2",
     shots=[S(None, f"c:{K}@37.0", top="SUBE HASTA ARRIBA"), S("dos fantasmas", f"c:{K}@45.0", top="DOS FANTASMAS"), S("y uno empuja", f"c:{K}@50.6", top="¡AL VACÍO!")],
     sfx=[("w:empuja", "impact", 0.5)])
beat("Abajo te espera una foto. Es la primera pista.", id="s3",
     shots=[S(None, f"c:{K}@57.0", top="LA FOTO")],
     sfx=[("w:pista", "stamp", 0.4)])
beat("Te lleva a una casa en un islote. En la chimenea, un libro.", id="s4",
     shots=[S(None, f"c:{K}@66.0", top="EL ISLOTE"), S("En la chimenea", f"c:{K}@75.0", top="EL LIBRO")],
     sfx=[])
beat("Después, con equipo de buceo, nadas mar adentro… hasta que todo se llena de niebla.", id="s5",
     shots=[S(None, f"c:{K}@92.0", top="EQUIPO DE BUCEO"), S("hasta que", f"c:{K}@107.0", top="LA NIEBLA")],
     sfx=[("w:niebla", "whoosh", 0.4)])
beat("Ahí abajo hay un bote hundido. Y dentro, un cuchillo verde: ¡el cuchillo maldito!", id="s6",
     shots=[S(None, f"c:{K}@121.6", top="EL BOTE HUNDIDO"), S("un cuchillo verde", f"c:{K}@128.0", top="EL CUCHILLO MALDITO")],
     sfx=[("w:maldito", "impact", 0.5)])
beat("Vuelve al faro, mira con binoculares… y ahí está: ¡el barco fantasma!", id="s7",
     shots=[S(None, f"c:{K}@139.0", top="VUELVE AL FARO"), S("y ahí está", f"c:{K}@143.0", top="EL BARCO FANTASMA")],
     sfx=[("w:barco fantasma", "heartbeat", 0.5)])
beat("¿Irías de noche? Suscríbete para más secretos de GTA 6, ¡y dale like si te dio escalofríos!", id="s8", hold=1.6,
     shots=[S(None, f"c:{K}@150.0", top="¿IRÍAS DE NOCHE?"), S("Suscríbete", "g:sub", lines=["Más secretos de GTA 6", "con partidas reales"])],
     sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("tension", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[-1]["start"], 1)], seed=8620)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "ck", "SHORT_11_GTA6_BARCO_FANTASMA", "tension", "fantasma", "GTA 6 · MISTERIO"
TITLE = "El barco fantasma de GTA 6"

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
