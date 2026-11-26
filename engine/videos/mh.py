"""SHORT_10 — «¿Mario y Luigi en GTA 6?» (9:16). Solo GTA 6.

Partida real: IGN, «GTA 6 - How to Get the Mario and Luigi Hat Easter Egg» (23/11/2026, 4K). Todo lo que se cuenta se ve:
las ruinas junto al río, el dinero y la pipa, el bloque que aparece flotando, el salto debajo y las dos gorras con la J y la L.
Sin crédito en pantalla (va en la descripción)."""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=0.6, cfg=0.4)   # la voz de siempre (las rondas de repetición usan estos ajustes)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)
H = "GByO53W1-fI"

beat("¿Mario y Luigi… en GTA 6? ¡Pues sí! Y el truco para encontrarlos es rarísimo.", id="s1", pre=0.1,
     shots=[S(None, f"c:{H}@73.8", top="¿MARIO Y LUIGI?"), S("el truco", f"c:{H}@53.6", top="UN TRUCO RARÍSIMO")],
     sfx=[(0.0, "riser", 0.35), ("w:rarísimo", "pop", 0.45)])
beat("Primero, ve a unas ruinas junto a un río, lejos de la ciudad.", id="s2",
     shots=[S(None, f"c:{H}@15.6", top="PASO 1 · LAS RUINAS"), S("junto a un río", f"c:{H}@6.0", top="JUNTO AL RÍO")],
     sfx=[("w:Primero", "ding", 0.45)])
beat("Adentro hay algo de dinero… y una pipa. ¡Úsala!", id="s3",
     shots=[S(None, f"c:{H}@27.0", top="PASO 2 · ADENTRO"), S("Úsala", f"c:{H}@40.0", top="LA PIPA")],
     sfx=[("w:Úsala", "whoosh", 0.4)])
beat("Y de repente, sobre las ruinas, aparece un bloque flotando en el aire.", id="s4",
     shots=[S(None, f"c:{H}@45.0", top="PASO 3 · EL BLOQUE")],
     sfx=[("w:bloque", "stamp", 0.4)])
beat("Súbete justo debajo… ¡y salta, como en Mario!", id="s5",
     shots=[S(None, f"c:{H}@50.6", top="SALTA DEBAJO")],
     sfx=[("w:salta", "pop", 0.5)])
beat("¡Pum! Salen dos gorras: una con la {J|jota} y otra con la {L|ele}. ¡Igualitas a las de Mario y Luigi!", id="s6",
     shots=[S(None, f"c:{H}@62.4", top="¡PUM!"), S("una con la", f"c:{H}@79.6", top="LA J Y LA L")],
     sfx=[("w:Pum", "impact", 0.5), ("w:Igualitas", "coin", 0.5)])
beat("Una te la pones al momento; la de tu pareja, en el armario.", id="s7",
     shots=[S(None, f"c:{H}@83.0", top="PARA LOS DOS")],
     sfx=[])
beat("¿Qué otro guiño crees que esconde Rockstar? Suscríbete para más secretos de GTA 6, ¡y dale like si te gustó!", id="s8", hold=1.6,
     shots=[S(None, "g:sub", lines=["Más secretos de GTA 6", "con partidas reales"])],
     sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("chip", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[-1]["start"], 1)], seed=8610)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "mh", "SHORT_10_GTA6_GORRAS_MARIO_LUIGI", "chip", "retro", "GTA 6 · EASTER EGG"
TITLE = "Las gorras de Mario y Luigi en GTA 6"

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
