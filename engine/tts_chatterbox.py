"""Síntesis por lotes con Chatterbox Multilingual (Resemble AI, licencia MIT) — voz con expresividad humana.

Se ejecuta en su propio entorno de Python (PyTorch), separado del motor de render:
    <venv>/bin/python tts_chatterbox.py trabajos.json --threads 2
`trabajos.json` = lista de {"text", "seed", "out", "ref", "exaggeration", "cfg", "temperature"}.
Cada audio se escribe en `out` (WAV 24 kHz). Si `out` ya existe, se omite (caché).

Chatterbox añade una marca de agua inaudible (Perth) a todo lo que genera: identifica el audio como sintético.
Modelo: https://huggingface.co/ResembleAI/chatterbox (t3_mtl23ls_v2.safetensors, s3gen.pt, ve.pt, conds.pt, grapheme_mtl_merged_expanded_v1.json)
Variable de entorno CHATTERBOX_DIR = carpeta con esos archivos.
"""
import argparse, json, os, sys, time

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("jobs"); ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args()
    jobs = [j for j in json.load(open(a.jobs, encoding="utf-8")) if not os.path.exists(j["out"])]
    if not jobs: print("nada que generar", flush=True); return
    import torch, numpy as np, soundfile as sf
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    torch.set_num_threads(a.threads)
    d = os.environ.get("CHATTERBOX_DIR")
    m = ChatterboxMultilingualTTS.from_local(d, "cpu")
    last_ref = None; t0 = time.time(); done_s = 0.0
    for i, j in enumerate(jobs):
        torch.manual_seed(int(j["seed"]))
        if j["ref"] != last_ref:
            m.prepare_conditionals(j["ref"], exaggeration=float(j.get("exaggeration", 0.6))); last_ref = j["ref"]
        with torch.inference_mode():
            wav = m.generate(j["text"], language_id="es", audio_prompt_path=None,
                             exaggeration=float(j.get("exaggeration", 0.6)), cfg_weight=float(j.get("cfg", 0.4)),
                             temperature=float(j.get("temperature", 0.8)))
        x = wav.squeeze().detach().cpu().numpy().astype("float32")
        tmp = j["out"] + ".tmp.wav"; sf.write(tmp, x, m.sr, subtype="FLOAT"); os.replace(tmp, j["out"])
        done_s += len(x) / m.sr
        print(f"[{i + 1}/{len(jobs)}] {len(x) / m.sr:.1f}s · acumulado {done_s / 60:.1f} min de voz en {(time.time() - t0) / 60:.1f} min", flush=True)

if __name__ == "__main__":
    main()
