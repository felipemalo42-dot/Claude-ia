# PROYECTO_DE_EDICION — VIDEO_LARGO_GTA6 y su Short

Todo lo necesario para revisar o rehacer el montaje.

| Archivo | Qué es |
|---|---|
| `registro_de_planos.csv` | Cada plano: inicio, fin, palabra que lo motiva, desfase, vídeo y segundo exacto del original, encuadre, transición y rótulo |
| `VIDEO_LARGO_GTA6.edl` | Lista de edición CMX3600 (30 fps) para DaVinci Resolve, Premiere o Final Cut, con el código de tiempo del original |
| `descargar_material.sh` | Vuelve a crear los tramos de gameplay (1080p, 30 fps, sin fotogramas duplicados) desde las copias públicas |
| `recursos/timeline.json` | Tiempos de cada bloque, frase y palabra de la narración, y de cada toma de voz |
| `audio/narracion_original.flac` | Narración completa sin mezclar (FLAC sin pérdidas, 44,1 kHz): la que se comprobó con el WER |
| `audio/pistas/` | Voz, música y efectos por separado (FLAC), a la ganancia de la mezcla |
| `CONTROL_VOZ_WER.md`, `control_voz_wer.csv` | Comprobación guion ↔ audio final (WER) |
| `CONTROL_DE_CALIDAD.md` | Formato, fluidez (fotograma a fotograma frente al original), orden de reproducción, negro, sonoridad, subtítulos y sincronía |
| `AUDITORIA_FINAL.md` | Listas de comprobación del encargo (vídeo largo y Short) con los datos medidos |
| `INVESTIGACION_Y_CONCEPTO.md` | Investigación, matriz de temas ya usados y los 15 conceptos evaluados |
| `recursos/iconos_hud/` | Iconos reales del HUD recortados de fotogramas 4K |
| `short_promocional/` | Lo mismo para el Short: tiempos, narración sin mezclar (FLAC), pistas, control de voz (WER) y de calidad |

## Rehacer el vídeo

```
cd engine
python mezzanine.py            # tramos de gameplay (ver descargar_material.sh)
python mezzanine.py --short    # recortes verticales 4K del Short
python build.py gx --jobs 4     # voz (con control WER), mezcla, vídeo, subtítulos y miniatura
python wer_final.py gx          # verificación final guion ↔ audio
python build.py gs --jobs 4     # el Short
python wer_final.py gs
python gx_qa.py gx; python gx_qa.py gs   # control de calidad del vídeo final
python gx_package.py todo       # documentos
python gx_package.py auditoria  # AUDITORIA_FINAL.md
```

La voz pasa por `engine/voice_fix.py` al montarse (quita el zumbido grave que la síntesis añade a veces tras una frase, sin cambiar los tiempos).

El guion y los planos están en `engine/videos/gx.py` (largo) y `engine/videos/gs.py` (Short); el montaje en `gx_render.py` y `gs_render.py`.
