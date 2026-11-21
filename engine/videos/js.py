"""SHORT_3 — «En GTA 6, si te matan, te cobran el hospital» (9:16, 1080×1920).

Sale del vídeo largo «GTA 6 a juicio»: la factura del hospital (Video Pump), la basura que sube el Focus (guía de IGN), el caza
del primer capítulo (guía de IGN) y la pregunta del juicio. Vídeo completo en el canal.
"""
import os
import numpy as np
import audio
from videos import ds_render as R

B = []
def beat(vo="", **k): B.append(dict(vo=vo, scene=(R.scene if not B else None), **k))
def S(anchor, src, **k): return dict(anchor=anchor, src=src, **k)
HOS, CAS, JET, TAN = "vpHospital1", "3UiRmXUIE9k", "4HCd052lpnA", "-UuHA1h-Cf8"

beat("Si te matan en GTA 6, te cobran el hospital.", pre=0.15, exag=0.7, id="s1",
     shots=[S(None, f"c:{HOS}@6.6", top="PARTIDA REAL · VIDEO PUMP")], sfx=[(0.0, "riser", 0.3), ("w:hospital", "coin", 0.4)])
beat("Este jugador recibe un disparo, muere, y despierta junto a la carretera con un cargo de mil ciento noventa y un dólares.", exag=0.7, id="s2",
     shots=[S(None, f"c:{HOS}@0.0"), S("muere", f"c:{HOS}@2.5"), S("despierta", f"c:{HOS}@10.4"), S("con un cargo", f"c:{HOS}@13.45", crop=(0.55, 0.05, 1.0, 0.6), top="EL CARGO, EN LA ESQUINA")],
     sfx=[("w:muere", "impact", 0.35), ("w:mil ciento", "coin", 0.45)])
beat("Pero si sacas la basura, el juego te premia: la barra de Focus sube un tres por ciento.", exag=0.7, id="s3",
     shots=[S(None, f"v:{CAS}@79.0@0.5", prueba="+3 % FOCUS", lado="defensa"), S("la barra", f"v:{CAS}@86.0@0.5")],
     sfx=[("w:tres por", "ding", 0.4)])
beat("Y en el primer capítulo ya puedes robar un avión de combate.", exag=0.7, id="s4",
     shots=[S(None, f"v:{JET}@134.0@0.55", prueba="ROBO DE UN CAZA", lado="acusacion"), S("un avión", f"v:{JET}@163.0@0.42")],
     sfx=[("w:robar", "whoosh", 0.35)])
beat("Entonces, ¿GTA 6 es un juego de crímenes o un simulador de vida? Por eso hicimos un juicio, con pruebas reales.", exag=0.65, id="s5",
     shots=[S(None, f"v:{JET}@142.0@0.55", prueba="¿CRÍMENES?", lado="acusacion"), S("o un simulador", f"v:{CAS}@89.6@0.5", prueba="¿VIDA?", lado="defensa"),
            S("Por eso hicimos", "g:sq", lines=["GTA 6", "A JUICIO"], sub="Con pruebas reales", hl=[1])],
     sfx=[(0.0, "whoosh", 0.35), ("w:juicio", "stamp", 0.5)])
beat("El veredicto lo pones tú. El video completo está en el canal.", exag=0.65, hold=1.6, id="s6",
     shots=[S(None, "g:scta", thumb=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "VIDEO_LARGO_3_GTA6_A_JUICIO", "MINIATURA.png"),
              sub="Acusación, defensa y testigos", cues=["en el canal"])],
     sfx=[(0.0, "pop", 0.45), ("w:en el canal", "ding", 0.45)])

def music_fn(total, beats_tl):
    y = audio.compose("noir", total + 1.0, energy=[(0.0, 2), (beats_tl[2]["start"], 1), (beats_tl[4]["start"], 2)], seed=6207)
    n = int(total * audio.SR); y = y[:n]; fo = int(1.2 * audio.SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y / (np.abs(y).max() + 1e-9) * 0.8

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDER = "SHORT_3_GTA6_A_JUICIO"
os.makedirs(os.path.join(_ROOT, FOLDER, "trabajo"), exist_ok=True)
VIDEO = dict(id="js", folder=FOLDER, file="SHORT_FINAL", res_dir="trabajo", theme="juicio", header="GTA 6 A JUICIO",
             title="En GTA 6, si te matan, te cobran el hospital",
             format="Short (9:16, 1080×1920, 30 fps)", music="noir", music_fn=music_fn,
             voice="host", beats=B, overlay=R.overlay, grade=None, music_gain=0.34, duck=0.24, duck_release=0.9, sfx_gain=0.55, size=(1080, 1920),
             max_tries=6, qa_metric="wer", qa_thr=1.0, drone_clean=True, trim_tail="energia", stems="trabajo/pistas", trans=("cut", 0.0),
             final_codec="h264_hq", crf=18, x264_tune="film", thumb_size=(1080, 1920),
             names=dict(narr_wav="trabajo/narracion_original.wav", narr_mp3="trabajo/NARRACION.mp3", srt="SUBTITULOS.srt",
                        script="trabajo/guion_con_tiempos.txt", thumb="trabajo/PORTADA.png"))
THUMB_MARK = None
