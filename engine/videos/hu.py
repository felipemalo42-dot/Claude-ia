"""SHORT_13 — «El hombre del búnker y el huracán» (9:16). Solo GTA 6.

Partida real: Lootward, «You Can Actually Unlock HURRICANE Weather in GTA 6» (23/11/2026, 4K). Se ve: las defensas del búnker
de Freddie, su pódcast, la cámara, el aviso «A HURRICANE WARNING IS IN EFFECT», el dinero que te da y el huracán al salir.
No se afirma que el clima quede desbloqueado para siempre (solo lo dice quien lo subió). Sin crédito en pantalla."""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)   # la voz de siempre (las rondas de repetición usan estos ajustes)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)
U = "mMBdAMjCEnE"

beat("En GTA 6 hay un tipo que vive en un búnker esperando el apocalipsis… ¡y tiene razón!", id="s1", pre=0.1,
     shots=[S(None, f"c:{U}@772.0", top="¿EL APOCALIPSIS?"), S("en un búnker", f"c:{U}@178.0", top="EL BÚNKER")],
     sfx=[(0.0, "riser", 0.35), ("w:tiene razón", "impact", 0.5)])
beat("Se llama Freddie, y su casa está protegida con minas y drones.", id="s2",
     shots=[S(None, f"c:{U}@124.0", top="FREDDIE"), S("minas y drones", f"c:{U}@60.0", top="MINAS Y DRONES")],
     sfx=[("w:drones", "alarm", 0.35)])
beat("Si logras atravesar sus defensas, no se enfada… ¡te invita a su pódcast!", id="s3",
     shots=[S(None, f"c:{U}@140.0", top="LAS DEFENSAS"), S("te invita", f"c:{U}@605.0", top="SU PÓDCAST")],
     sfx=[("w:pódcast", "pop", 0.45)])
beat("Pero entonces su cámara ve algo afuera, y salta una alerta: ¡huracán!", id="s4",
     shots=[S(None, f"c:{U}@692.0", top="LA CÁMARA"), S("salta una alerta", f"c:{U}@713.0", top="¡ALERTA!")],
     sfx=[("w:huracán", "alarm", 0.45)])
beat("Freddie se encierra, te da dinero y te dice que lo gastes rápido…", id="s5",
     shots=[S(None, f"c:{U}@728.0", top="SE ENCIERRA"), S("te da dinero", f"c:{U}@742.0", top="GÁSTALO RÁPIDO")],
     sfx=[("w:dinero", "coin", 0.45)])
beat("…porque al salir, el huracán ya está aquí.", id="s6",
     shots=[S(None, f"c:{U}@752.0", top="AL SALIR…"), S("ya está aquí", f"c:{U}@781.0", top="EL HURACÁN")],
     sfx=[("w:huracán", "whoosh", 0.5)])
beat("¿Te quedarías en el búnker? Suscríbete para más secretos de GTA 6, ¡y dale like si sobreviviste!", id="s7", hold=1.6,
     shots=[S(None, "g:sub", lines=["Más secretos de GTA 6", "con partidas reales"])],
     sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("storm", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[-1]["start"], 1)], seed=8640)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "hu", "SHORT_13_GTA6_HURACAN_SECRETO", "storm", "tormenta", "GTA 6 · ALERTA"
TITLE = "La misión secreta del huracán en GTA 6"

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
