"""SHORT_9 — «GTA 6 no tiene primera persona… pero hay un truco» (9:16). Short independiente, solo GTA 6.

Partida real de IGN («GTA 6 First-Person Mode Glitch: Here's how to do it!», 20/11/2026; recorte limpio sin sus rótulos). Pasos
según IGN (vídeo y guía «How to Play GTA 6 in First-Person (It's a Glitch!)»): cambiar en los ajustes del mando el botón del panel
táctil o Vista de Mapa a Cámara, entrar en un coche, sacar el teléfono y guardarlo pulsando sin parar el botón de cámara. Se mantiene
al morir y se va al cargar la partida o salir del juego. No es un modo oficial. Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=1.0, cfg=0.3)   # voz más expresiva (parámetros de Chatterbox para habla animada)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
F = "igFP"
def N(anchor, n, name): return S(anchor, "g:sq", lines=[n, name], hl=[0], y=760)

beat("GTA 6 no tiene modo en primera persona… ¡pero hay un truco para jugar así!", pre=0.1, id="s1",
     shots=[S(None, f"c:{F}@0.36", top="PRIMERA PERSONA EN GTA 6"), S("¡pero hay un truco", f"c:{F}@16.8", top="¡CON UN TRUCO!")], sfx=[(0.0, "riser", 0.35), ("w:truco", "stamp", 0.45)])
beat("Paso uno: en los ajustes del mando, cambia el botón del panel táctil, o el botón Vista, de Mapa a Cámara.", id="s2",
     shots=[N(None, "1", "AJUSTES DEL MANDO"), S("panel táctil", f"c:{F}@4.32", top="PASO 1 · AJUSTES"),
            S("de Mapa a Cámara", f"c:{F}@6.02", crop=(0.55, 0.45, 1.0, 0.68), top="MAPA → CÁMARA")],
     sfx=[("w:Paso uno", "ding", 0.45)])
beat("Paso dos: súbete a un coche y saca el teléfono.", id="s3",
     shots=[N(None, "2", "EL TELÉFONO"), S("súbete", f"c:{F}@8.9", top="PASO 2 · EL TELÉFONO")], sfx=[("w:Paso dos", "ding", 0.45)])
beat("Paso tres, el difícil: guarda el teléfono mientras pulsas el botón de cámara sin parar. ¡Puede costar varios intentos!", id="s4",
     shots=[N(None, "3", "GUARDA EL TELÉFONO"), S("mientras pulsas", f"c:{F}@11.66", top="PASO 3 · SIN PARAR")], sfx=[("w:Paso tres", "ding", 0.45)])
beat("Cuando entra, te quedas en primera persona… ¡aunque mueras! Solo se quita al cargar la partida o al salir del juego.", id="s5",
     shots=[S(None, f"c:{F}@18.8", top="¡DENTRO!"), S("¡aunque mueras", f"c:{F}@22.9", top="AUNQUE MUERAS"),
            S("Solo se quita", f"c:{F}@23.88", top="SE QUITA AL CARGAR O SALIR")],
     sfx=[("w:aunque mueras", "impact", 0.4)])
beat("No es un modo oficial, así que tiene fallos. Pero se ve increíble.", id="s6",
     shots=[S(None, f"c:{F}@27.93", top="NO ES OFICIAL")], sfx=[("w:increíble", "whoosh", 0.35)])
beat("Suscríbete para más trucos de GTA 6, ¡y dale like si lo vas a probar!", hold=1.6, id="s7",
     shots=[S(None, "g:sub", lines=["Más trucos de GTA 6", "con partidas reales"])], sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("electro", total + 1.0, energy=[(0.0, 2), (beats_tl[1]["start"], 3), (beats_tl[6]["start"], 1)], seed=8530)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "fp", "SHORT_9_GTA6_PRIMERA_PERSONA", "electro", "arcade", "GTA 6 · TRUCO"
TITLE = "GTA 6 no tiene primera persona… pero hay un truco"

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
