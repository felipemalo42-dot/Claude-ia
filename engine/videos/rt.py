"""SHORT_7 — «El ritual secreto de GTA 6» (9:16). Short independiente, solo GTA 6. Con spoilers leves.

Partida real: IGN, «Have you found the pentagram in GTA 6?» (20/11/2026; recorte limpio sin sus rótulos). Todo lo que se cuenta
sale de ese vídeo: el pentagrama de Capri con sus notas, el «sacrificio» (dejar inconsciente a alguien y llevarlo), las luces y las
velas, la voz de la pareja desde otra habitación (con Lucía, una versión demoníaca de su madre; con Jason, Cal) y el cuerpo que ataca
y solo se frena con fuego. Sin crédito en pantalla (va en la descripción).
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
EX = dict(exag=1.0, cfg=0.3)   # voz más expresiva (parámetros de Chatterbox para habla animada)
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **{**EX, **k}))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
P = "igPenta"

beat("En GTA 6 hay un ritual secreto. Y si lo completas… pasa esto.", pre=0.1, id="s1",
     shots=[S(None, f"c:{P}@74.6", top="EL RITUAL SECRETO"), S("pasa esto", f"c:{P}@62.0", top="¿TE ATREVES?")],
     sfx=[(0.0, "riser", 0.35), ("w:pasa esto", "impact", 0.5)])
beat("En un edificio de Capri hay un pentagrama, con velas y unas notas. ¡Y a ese círculo le falta algo: un sacrificio!", id="s2",
     shots=[S(None, f"c:{P}@6.4", top="CAPRI"), S("con velas", f"c:{P}@20.6", top="EL PENTAGRAMA"), S("unas notas", f"c:{P}@0.2", top="LAS NOTAS"),
            S("un sacrificio", f"c:{P}@2.6", top="«SACRIFICE»")],
     sfx=[("w:sacrificio", "stamp", 0.45)])
beat("Así que dejas inconsciente a alguien… y lo llevas hasta allí.", id="s3",
     shots=[S(None, f"c:{P}@11.4", top="EL «SACRIFICIO»")], sfx=[("w:inconsciente", "impact", 0.35)])
beat("Se apagan las luces. Se encienden las velas. ¡Y oyes la voz de tu pareja en otra habitación!", id="s4",
     shots=[S(None, f"c:{P}@22.8", top="SE APAGAN LAS LUCES"), S("Y oyes", f"c:{P}@26.6", top="UNA VOZ")],
     sfx=[("w:velas", "whoosh", 0.35), ("w:otra habitación", "heartbeat", 0.45)])
beat("Pero no es ella. Si juegas con Lucía, aparece una versión demoníaca de su madre. ¡Y con Jason, es Cal!", id="s5",
     shots=[S(None, f"c:{P}@31.6", top="NO ES ELLA"), S("Si juegas con Lucía", f"c:{P}@41.4", top="CON LUCÍA"), S("Y con Jason", f"c:{P}@51.4", top="CON JASON")],
     sfx=[("w:demoníaca", "impact", 0.45)])
beat("Y cuando vuelves al pentagrama, el cuerpo que sacrificaste se levanta y te ataca. ¡Solo el fuego lo detiene!", id="s6",
     shots=[S(None, f"c:{P}@56.4", top="SE LEVANTA"), S("Solo el fuego", f"c:{P}@69.8", top="SOLO EL FUEGO")],
     sfx=[("w:te ataca", "impact", 0.45), ("w:fuego", "whoosh", 0.45)])
beat("¿Te atreverías? Suscríbete para más secretos de GTA 6, ¡y dale like si te dio miedo!", hold=1.6, id="s7",
     shots=[S(None, "g:sub", lines=["Más secretos de GTA 6", "con partidas reales"])], sfx=[(0.0, "pop", 0.45), ("w:dale like", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("mystery", total + 1.0, energy=[(0.0, 2), (beats_tl[3]["start"], 3), (beats_tl[6]["start"], 1)], seed=8510)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.0 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

VID, FOLDER, MOOD, THEME, HEADER = "rt", "SHORT_7_GTA6_RITUAL_SECRETO", "mystery", "terror", "GTA 6 · SECRETO"
TITLE = "El ritual secreto de GTA 6"

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
