"""SHORT_14 — «El auto de Paul Walker en GTA 6» (9:16). Solo GTA 6.

Partida real: IGN, «GTA 6: How to Get Paul Walker's Eclipse (The Fast and the Furious)» (22/11/2026, 4K). Se ve: el Eclipse
verde (Penumbra FF), la matrícula, el mapa de Vespucci, la puerta lateral, el portón, el cristal, el panel de alarma, el taller de
Moses con el registro y la ficha de prestaciones. Sin imágenes de la película. Sin crédito en pantalla."""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)   # la voz de siempre (las rondas de repetición usan estos ajustes)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)
E = "JPnJPuH4N6Q"

beat("¡El auto de Brian O'Conner, de Rápido y Furioso, está en GTA 6!", id="s1", pre=0.1,
     shots=[S(None, f"c:{E}@126.4", top="RÁPIDO Y FURIOSO"), S("está en GTA 6", f"c:{E}@19.0", top="EN GTA 6")],
     sfx=[(0.0, "riser", 0.35), ("w:GTA 6", "impact", 0.5)])
beat("Es el Eclipse verde de la primera película; aquí se llama Penumbra {FF|efe efe}. Y mira la matrícula: otro guiño a la peli.", id="s2",
     shots=[S(None, f"c:{E}@6.0", top="PENUMBRA FF"), S("Y mira la matrícula", f"c:{E}@27.4", crop=(0.42, 0.42, 1.0, 0.95), top="MATRÍCULA: «HAD YOU»")],
     sfx=[("w:matrícula", "stamp", 0.4)])
beat("Está en un garaje de Vespucci.", id="s3",
     shots=[S(None, f"c:{E}@36.0", top="VESPUCCI")],
     sfx=[("w:Vespucci", "ding", 0.45)])
beat("Entras por la puerta lateral, abres el portón, rompes el cristal… ¡y le haces el puente!", id="s4",
     shots=[S(None, f"c:{E}@74.0", top="LA PUERTA LATERAL"), S("abres el portón", f"c:{E}@88.0", top="EL PORTÓN"), S("rompes el cristal", f"c:{E}@58.0", top="EL CRISTAL"), S("le haces el puente", f"c:{E}@62.0", top="¡EL PUENTE!")],
     sfx=[("w:cristal", "impact", 0.4)])
beat("Si no quieres a la policía detrás, desactiva antes la alarma.", id="s5",
     shots=[S(None, f"c:{E}@79.0", top="LA ALARMA")],
     sfx=[])
beat("Luego llévaselo a Moses para registrarlo. ¡Si es tu primer auto, te sale gratis!", id="s6",
     shots=[S(None, f"c:{E}@107.0", top="MOSES"), S("Si es tu primer", f"c:{E}@115.0", top="¡GRATIS!")],
     sfx=[("w:gratis", "coin", 0.5)])
beat("Es rapidísimo, pero frágil: mejor no lo choques.", id="s7",
     shots=[S(None, f"c:{E}@146.0", top="RAPIDÍSIMO"), S("pero frágil", f"c:{E}@156.0", top="PERO FRÁGIL")],
     sfx=[])
beat("¿Vas a ir por él? Suscríbete para más secretos de GTA 6, ¡y dale like en honor a Paul Walker!", id="s8", hold=1.6,
     shots=[S(None, "g:sub", lines=["Más secretos de GTA 6", "con partidas reales"])],
     sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("synthpop", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[-1]["start"], 1)], seed=8650)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "ec", "SHORT_14_GTA6_AUTO_PAUL_WALKER", "synthpop", "racing", "GTA 6 · AUTOS"
TITLE = "El auto de Paul Walker está en GTA 6"

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
