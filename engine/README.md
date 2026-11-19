# Motor de producción de Sal y Asfalto

Pipeline reproducible: **guion → voz → tiempos → música/SFX → animación → MP4 + SRT + miniatura**.
Cada vídeo es un módulo de Python (`videos/v01.py` … `videos/v10.py`) con dos partes:
- el **guion por bloques**: texto, escena, efectos de sonido sincronizados con palabras clave y energía musical;
- las **escenas**: funciones de dibujo con Skia, sincronizadas con el momento exacto en que la narradora dice cada palabra clave.

## Requisitos
```bash
pip install "sherpa-onnx>=2" skia-python numpy scipy soundfile pyloudnorm pillow
sudo apt-get install -y ffmpeg libegl1
# Voz principal: Chatterbox Multilingual (MIT), en un entorno aparte con PyTorch (~3,2 GB de modelo)
python3 -m venv cbenv && cbenv/bin/pip install chatterbox-tts "setuptools<81"
# descarga de https://huggingface.co/ResembleAI/chatterbox: ve.pt, conds.pt, s3gen.pt, t3_mtl23ls_v2.safetensors, grapheme_mtl_merged_expanded_v1.json, Cangjie5_TC.json
export CHATTERBOX_PY=$PWD/cbenv/bin/python CHATTERBOX_DIR=/ruta/al/modelo
# Voz alternativa ligera (VOICE_ENGINE=supertonic): Supertonic 3 (pesos OpenRAIL-M), ~130 MB
curl -L -O https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2
tar xjf sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2 && export SUPERTONIC_DIR=$PWD/sherpa-onnx-supertonic-3-tts-int8-2026-05-11
# Verificación y sincronización (CC-BY-4.0), ~490 MB
curl -L -O https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2
tar xjf sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2 && export ALIGN_ASR_DIR=$PWD/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8
```

## Uso
```bash
cd engine
python build.py v01                 # todo: audio, miniatura y vídeo
python build.py v01 --stage audio   # solo voz, música, mezcla, SRT y guion
python build.py v01 --stage video   # solo render (necesita la etapa de audio hecha)
python build.py v01 --master        # render de mayor calidad (CRF 17, hasta 12 Mbps) para subir a YouTube
python stills.py v01 12.5 40        # fotogramas sueltos para revisar
python brand.py ../CANAL_IDENTIDAD  # regenera logotipo, avatar, banner y marca de agua
python publish_meta.py              # regenera publicacion.md, descripción, etiquetas y hoja de contactos
```

**Nota sobre la calidad:** los MP4 entregados se codificaron con CRF 19 y un tope de bitrate para que cada archivo pese menos de 100 MB (límite de GitHub). Pesan entre 5 y 28 MB y se ven bien porque los gráficos planos comprimen muy bien. Si quieres el máximo margen de calidad para YouTube, vuelve a renderizar con `--master`.

## Sustituir la voz sintética por tu voz (recomendado para monetizar)
1. Abre `VIDEO_XX/guion.txt`. Cada bloque `## SECCIÓN` corresponde a uno o más *beats*, numerados en orden según la lista `B` del módulo.
2. Graba cada bloque de narración en un WAV: `VIDEO_XX/voz_humana/beat_00.wav`, `beat_01.wav`, … El número es la posición del beat en `B`; los beats sin narración no necesitan archivo.
3. Ejecuta `python build.py vXX`. El pipeline usa tu grabación, obtiene el tiempo exacto de cada palabra con reconocimiento de voz y vuelve a sincronizar animación, efectos, música (con *ducking*) y subtítulos.

## Arquitectura
| Archivo | Función |
|---|---|
| `tts.py` | Texto hablado (pronunciación de nombres en inglés, números a palabras), voz alternativa Supertonic 3, verificación de cada toma y tiempos por palabra con reconocimiento de voz |
| `tts_chatterbox.py` | Síntesis por lotes de la narradora con Chatterbox Multilingual (se ejecuta en su propio entorno de Python); referencias en `voces/` |
| `audio.py` | Sintetizador propio: osciladores, FM, filtros, reverberación por convolución, batería, 10 estilos musicales, 24 efectos de sonido, *ducking* y masterización a −14 LUFS |
| `gfx.py` | Utilidades de Skia: texto, formas, degradados, iconos (rutas SVG propias), cámara 3D en perspectiva y *easing* |
| `components.py` | Elementos de marca: semáforo de certeza, chips de fuente, cortinilla, pantalla final, subtítulos de Shorts y marca de agua |
| `brand.py` | Emblema (carretera sobre el mar), wordmark, señal vial, semáforo y recursos de identidad |
| `build.py` | Orquestación, transiciones (whip, glitch, iris, zoom, flash, wipe…), codificación H.264/AAC, SRT y guion con marcas de tiempo |
| `publish_meta.py` | Metadatos de publicación y auditoría de los 10 vídeos |
| `geo/` | Natural Earth (dominio público): países, estados y lagos |
| `fonts/` | Tipografías con licencia OFL o Apache 2.0 |

## Producción especial VIDEO_EXTRA (9:29)
```bash
cd engine
python build.py vx --stage audio            # voz verificada (métrica fonética, ver voice_qa.py), música por épocas, mezcla, SRT
python build.py vx --stage video --jobs 4   # render en 4 procesos paralelos (~19 min en 4 núcleos)
python vx_package.py                        # GUION_COMPLETO.docx, paquete de publicación, RECURSOS_VISUALES y limpieza
```
| Archivo | Función |
|---|---|
| `videos/vx.py` | Guion por bloques (con énfasis, ritmo y notas visuales), música por épocas y tratamiento de color por época |
| `videos/vx_lib.py` | Biblioteca visual: fachadas art déco genéricas, calle por época, corte de pintura, televisor, celulares, pixelado |
| `videos/vx_scenes.py` | Las 29 escenas y la miniatura |
| `voice_qa.py` | Control de calidad de la voz: dos reconocedores (Parakeet + Whisper) y comparación fonética guion ↔ voz |
| `vx_package.py` / `vx_docx.js` | Empaquetado final y guion en Word (docx-js) |

Opciones nuevas del motor:
- `--jobs N`: render en paralelo.
- En el módulo del video:
  - `music_fn`: música propia del video;
  - `grade`: corrección de color por época;
  - `qa_metric="fonetica"` y `qa_thr`: umbral de coincidencia de la voz;
  - `max_tries`: número de semillas;
  - `names`: nombres de los archivos de salida.
- Por bloque: `exag` y `cfg` (expresividad de la voz).

## GTA6_VIDEO_LANZAMIENTO (vídeo post lanzamiento con material oficial de Rockstar)
```bash
cd engine
python build.py gp --stage audio            # voz C verificada (fonética, ≥ 99,5 % por toma), música por capítulo, mezcla, SRT
python build.py gp --stage thumb            # miniatura (captura oficial, sin spoilers)
python build.py gp --stage video --jobs 4   # render en 4 procesos; segmentos H.264 en bruto unidos sin pérdida + AV1 final < 100 MB
python gp_package.py                        # registro de planos y sincronía, permisos con cifras reales, GUION_COMPLETO.docx, SEO, RECURSOS_VISUALES
```
| Archivo | Función |
|---|---|
| `videos/gp.py` | Guion por bloques (reseñas y datos posteriores al lanzamiento). Cada bloque lleva su lista de planos `S(ancla, fuente)`: el corte cae en la palabra «ancla». También fija qué misiones del Extended Look se muestran (con aviso de spoiler) |
| `videos/gl_render.py` | Montaje compartido: lector de vídeo (ffmpeg → Skia), ventanas por corte de escena, tramos prohibidos (`BAD`), Ken Burns, rótulos, aviso de spoiler, subtítulos dinámicos, gráficos y miniaturas |
| `videos/gl.py` | Borrador descartado (guía previa al lanzamiento). Se conserva sin renderizar |
| `gp_package.py` | `registro_de_planos.csv`, `sincronia.json`, cifras de uso en `REGISTRO_DE_PERMISOS.txt`, docx, descripción y recursos visuales |

Material de entrada (no incluido en el repositorio: se descarga de rockstargames.com/VI/media). Las rutas se fijan con estas variables de entorno:
- `GL_MEDIA`: carpeta con los ZIP descomprimidos y los MP4 oficiales;
- `GL_EL`: tramos del Extended Look en 1080p, sin audio (`r1…r5`, `m1`, `m3`, `m4`).
  Se extraen con `ffmpeg -ss T -i GTAVI_An_Extended_Look.mp4 -t D -an -vf scale=1920:1080 …`: los inicios y duraciones están en `EL_RANGES`.
- Cortes de escena: `ffmpeg … select='gt(scene,0.22)'` y `0.10`, guardados en `cuts/` y `cuts2/`.

Mejora general del motor: `--jobs N` ahora une los segmentos como H.264 en bruto (`cat`). Así no se pierde ningún fotograma entre partes, como pasaba con el `concat` de MP4.
Con `final_codec="av1"` y `target_mb`, el módulo comprime al final en AV1 de 10 bits con un tamaño objetivo.
