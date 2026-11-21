"""SHORT_2 — «Así reacciona un habitante de GTA 6 cuando invades su espacio» (9:16, 1080×1920).

Sale del vídeo largo «Planeta Vice City»: los mismos encuentros reales (partida de toaster, 4K), en recorte vertical con el
encuadre que deja fuera los subtítulos incrustados del original. Gancho → tres reacciones → pregunta → vídeo completo en el canal.
Planos: v:<ID>@<segundo>@<centro x> (recorte vertical) · c:<ID>@<segundo> (tarjeta 16:9) · g:<gráfico>
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
TOA = "cEDUO1zjB5c"
TOP = dict(z=(1.38, 1.42), fy=0.0)      # deja fuera los subtítulos incrustados (73-86 % de la altura)

beat("Así reacciona un habitante de GTA 6 si alguien invade su espacio.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"v:{TOA}@15.4@0.62", **TOP)], sfx=[(0.0, "riser", 0.3)])
beat("Primero, te lo dice claro: «No me hables». «Aléjate de mí».", exag=0.7, id="s2",
     shots=[S(None, f"v:{TOA}@6.5@0.62", **TOP), S("«No me", f"v:{TOA}@9.0@0.62", say="Don't talk to me.", **TOP),
            S("«Aléjate", f"v:{TOA}@12.5@0.62", say="Get away from me.", **TOP)],
     sfx=[("w:«No me", "pop", 0.35), ("w:«Aléjate", "pop", 0.35)])
beat("Si lo tocas, la cosa se pone seria: «¿Quién te dio permiso para tocarme?».", exag=0.7, id="s3",
     shots=[S(None, f"v:{TOA}@168.0@0.55", **TOP), S("«¿Quién", f"v:{TOA}@178.0@0.55", say="Who said you could touch me?", **TOP)],
     sfx=[("w:seria", "hit", 0.35)])
beat("Y a veces, el que ataca es él. Este te exige la bolsa. Si te niegas, empieza la pelea, y se oye un grito: «¡Que alguien llame a la policía!».", exag=0.7, id="s4",
     shots=[S(None, f"v:{TOA}@20.2@0.45", **TOP), S("te exige", f"v:{TOA}@24.0@0.45", say="Give bag / Decline", **TOP),
            S("empieza la pelea", f"v:{TOA}@30.0@0.45", **TOP), S("se oye un grito", f"v:{TOA}@37.0@0.45", say="Someone call the cops!", **TOP)],
     sfx=[("w:pelea", "impact", 0.4)])
beat("Lo estudiamos como a un animal salvaje en Planeta Vice City: el documental de los humanos de GTA 6.", exag=0.65, id="s5",
     shots=[S(None, f"v:{TOA}@186.0@0.55", **TOP),
            S("en Planeta", "g:sq", lines=["PLANETA", "VICE CITY"], sub="El documental de los humanos de GTA 6", hl=[1])],
     sfx=[(0.0, "whoosh", 0.35)])
beat("Lo tienes completo en el canal.", exag=0.65, hold=1.6, id="s6",
     shots=[S(None, "g:scta", thumb=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_2_PLANETA_VICE_CITY", "MINIATURA.png"),
              sub="Un documental con partidas reales", cues=["en el canal"])],
     sfx=[(0.0, "pop", 0.45), ("w:en el canal", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("nature", total + 1.0, energy=[(0.0, 1), (beats_tl[3]["start"], 2), (beats_tl[4]["start"], 1)], seed=7307)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "SHORT_2_PLANETA_VICE_CITY"
os.makedirs(os.path.join(_ROOT, FOLDER, "trabajo"), exist_ok=True)
VIDEO = dict(id="ps", folder=FOLDER, file="SHORT_FINAL", res_dir="trabajo", theme="planeta", header="PLANETA VICE CITY",
             title="Así reacciona un habitante de GTA 6 cuando invades su espacio",
             format="Short (9:16, 1080×1920, 30 fps)", music="nature", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55, size=(1080, 1920),
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav="trabajo/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="trabajo/PORTADA.png"))
THUMB_MARK = None
