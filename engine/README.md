# Motor de producción de Caimán Neón

Pipeline reproducible: **guion → voz → tiempos → música/SFX → animación → MP4 + SRT + miniatura**.
Cada vídeo es un módulo de Python (`videos/v01.py` … `videos/v10.py`) con dos partes:
- el **guion por bloques**: texto, escena, efectos de sonido sincronizados con palabras clave y energía musical;
- las **escenas**: funciones de dibujo con Skia, sincronizadas con el momento en que el narrador dice cada palabra clave.

## Requisitos
```bash
pip install "sherpa-onnx<2" onnxruntime skia-python numpy scipy soundfile pyloudnorm espeakng-loader phonemizer-fork pillow
sudo apt-get install -y ffmpeg libegl1
# Voz (Apache 2.0): ~350 MB
curl -L -o k.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
tar xjf k.tar.bz2 && export KOKORO_DIR=$PWD/kokoro-multi-lang-v1_0
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
3. Ejecuta `python build.py vXX`. El pipeline usa tu grabación, recalcula los tiempos de cada frase (repartidos por número de caracteres dentro del bloque) y vuelve a sincronizar animación, efectos, música (con *ducking*) y subtítulos.

## Arquitectura
| Archivo | Función |
|---|---|
| `tts.py` | Kokoro-82M vía onnxruntime. Fonemización espeak-ng `es-419` (seseo y yeísmo latinoamericanos) y diccionario de pronunciación para nombres en inglés |
| `audio.py` | Sintetizador propio: osciladores, FM, filtros, reverberación por convolución, batería, 10 estilos musicales, 24 efectos de sonido, *ducking* y masterización a −14 LUFS |
| `gfx.py` | Utilidades de Skia: texto, formas, degradados, iconos (rutas SVG propias), cámara 3D en perspectiva y *easing* |
| `components.py` | Elementos de marca: semáforo de certeza, chips de fuente, cortinilla, pantalla final, subtítulos de Shorts y marca de agua |
| `brand.py` | Logotipo del caimán neón y recursos de identidad |
| `build.py` | Orquestación, transiciones (whip, glitch, iris, zoom, flash, wipe…), codificación H.264/AAC, SRT y guion con marcas de tiempo |
| `publish_meta.py` | Metadatos de publicación y auditoría de los 10 vídeos |
| `geo/` | Natural Earth (dominio público): países, estados y lagos |
| `fonts/` | Tipografías con licencia OFL o Apache 2.0 |
