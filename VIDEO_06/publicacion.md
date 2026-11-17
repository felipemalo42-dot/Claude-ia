# VIDEO_06 — GTA 6 vs GTA 5: 10 cambios confirmados, 1 que no cambió y 3 rumores

**Estado real:** TERMINADO · listo para publicar  
**Fase:** Pre-lanzamiento y primera semana  
**Formato:** Largo (16:9) · **Duración:** 3:37 · **Música:** estilo «dembow» original · **Voz:** narradora

## A. Estrategia y posicionamiento

- **Título principal (SEO):** GTA 6 vs GTA 5: 10 cambios confirmados, 1 que no cambió y 3 rumores
- **Títulos alternativos:**
  1. GTA 6 contra GTA 5: lo que de verdad cambia (sin humo)
  2. 13 años después: 10 diferencias confirmadas entre GTA 5 y GTA 6
  3. GTA 6 vs GTA 5: mapa, estrellas, protagonistas, precio y más
- **Palabra clave principal:** gta 6 vs gta 5
- **Palabras clave secundarias:** diferencias gta 5 gta 6, gta 6 estrellas, perfil criminal gta 6, gta 6 huracanes, gta 6 animales, gta 6 60 fps
- **Intención de búsqueda:** Comparativa.
- **Público:** Jugadores veteranos de GTA V que deciden cuánto cambia la experiencia.
- **Duración:** 3:37
- **Por qué hacer clic:** Formato rápido de rondas con fuentes; separa los 3 rumores más repetidos con etiqueta propia.

## B-C. Guion, voz y subtítulos

- Guion completo con marcas de tiempo y notas visuales: `guion.txt`
- Texto de narración: `narracion.txt` · marcas por frase: `marcas_de_tiempo.csv`
- Audio de narración: `narracion.wav` (24 kHz, original) y `narracion.mp3` (procesada, 48 kHz)
- Subtítulos: `subtitulos.srt` (súbelos como subtítulos en español en YouTube Studio)

## D-F. Recursos visuales, animación y montaje

- Vídeo final: `GTA6_vs_GTA5_10_cambios_confirmados.mp4` · H.264 High, AAC 192 kbps 48 kHz, 30 fps, sonoridad −14 LUFS
- Hoja de contactos (un fotograma cada 5 s): `recursos/hoja_de_contactos.jpg`
- Música original del vídeo: `recursos/musica_original.mp3`
- Código fuente de todas las escenas: `engine/videos/v06.py` (re-renderizable)

## Descripción para YouTube (copiar y pegar)

```
Diez cambios confirmados entre GTA 5 y GTA 6 (mapa, protagonistas, estrellas, Perfil Criminal, foco, clima, fauna, precio, online y plataformas), lo que no cambió (el idioma) y tres rumores señalados.

CAPÍTULOS
0:00 Gancho
0:11 Introducción
0:25 Ronda 1 · el mundo
0:40 Ronda 2 · protagonistas
1:01 Ronda 4 · perfil criminal
1:16 Ronda 5 · sistema de foco
1:30 Ronda 6 · clima
1:42 Ronda 7 · fauna
2:07 Ronda 9 · online
2:18 Ronda 10 · plataformas
2:33 Lo que no cambia
2:49 Rumores
3:17 Despedida

FUENTES
• Game Informer n.º 382 (mapa ×2, clima, +170 especies)
• Extended Look (Rockstar, agosto 2026) vía TechRadar / Red Bull
• Rob Nelson (Rockstar), vía prensa
• Hollywood Reporter (precio)
• FAQ de PlayStation / Take-Two (un jugador)
• TweakTown / RockstarINTEL (objetivo 30 fps)
• Historial de lanzamiento de GTA V (2013, PC en 2015)

ℹ️ Transparencia: narración con voz sintética (modelo Chatterbox de Resemble AI, licencia MIT, con marca de agua inaudible) y animaciones originales de Sal y Asfalto. Este video NO contiene imágenes, música ni material de Rockstar Games. GTA y Grand Theft Auto son marcas de Take-Two Interactive; canal independiente, sin relación con Rockstar Games.

#GTA6 #GTAVI #Leonida
```

## Etiquetas

gta 6 vs gta 5, gta 5 vs gta 6, diferencias gta 6, gta 6 cambios, gta 6 estrellas, perfil criminal, gta 6 huracanes, gta 6 animales, gta 6 precio, gta 6 60 fps, gta 6, sal y asfalto

## Comentario fijado recomendado

📌 ¿Cuál es el cambio más importante para ti? Después del jueves hacemos la comparación JUGANDO, con pruebas propias. 🎮

## Divulgación de IA (YouTube Studio → Detalles → Contenido alterado)

**Casilla “contenido alterado o sintético”: NO.** Todo el material visual es animación/infografía claramente no realista y la voz sintética no imita a ninguna persona real ni presenta hechos inventados como reales. Según los ejemplos de YouTube, esto no exige la etiqueta. Por transparencia, la descripción lo declara igualmente.

## Fuentes de investigación

- Game Informer n.º 382 (mapa ×2, clima, +170 especies)
- Extended Look (Rockstar, agosto 2026) vía TechRadar / Red Bull
- Rob Nelson (Rockstar), vía prensa
- Hollywood Reporter (precio)
- FAQ de PlayStation / Take-Two (un jugador)
- TweakTown / RockstarINTEL (objetivo 30 fps)
- Historial de lanzamiento de GTA V (2013, PC en 2015)

## Recursos utilizados y licencias

- Música y efectos: compuestos y sintetizados por código para este video (engine/audio.py) · obra original, sin muestras de terceros.
- Voz: Chatterbox Multilingual de Resemble AI (licencia MIT) con referencia de una locutora anónima del corpus abierto OpenSLR SLR72 (Google, CC BY-SA 4.0; atribución: Guevara-Rukoz et al., LREC 2020). Ver engine/voces/README.md.
- Verificación y sincronización de la voz: reconocedor Parakeet TDT v3 de NVIDIA (CC-BY-4.0), usado solo como herramienta; no aparece en el video.
- Tipografías: Google Fonts con licencia SIL OFL 1.1 o Apache 2.0 (Anton, Inter, JetBrains Mono y las específicas del video).
- Gráficos: dibujados por código con Skia (BSD) · iconos propios (rutas SVG originales en engine/gfx.py).
- Codificación: FFmpeg (libx264 / AAC).
- Fuentes: Anton (OFL).

## Auditoría de calidad

| Comprobación | Resultado |
|---|---|
| ¿Contenido original? | Sí |
| ¿Aporta valor? | Sí |
| ¿Guion distinto a los demás? | Sí: rondas tipo transmisión deportiva |
| ¿Imágenes adecuadas y autorizadas? | Sí: infografías propias |
| ¿Voz con calidad profesional? | Buena: voz femenina expresiva (Chatterbox Multilingual), leída por frases y párrafos cortos; cada toma verificada con reconocimiento de voz (ver recursos/control_de_voz.csv). Es una voz sintética: grabar con voz humana mejora autenticidad (ver README). |
| ¿Montaje con buen ritmo? | Sí: ritmo alto, música dembow original |
| ¿Título honesto? | Sí |
| ¿Miniatura corresponde? | Sí |
| ¿Información sin verificar? | 3 rumores rotulados como RUMOR |
| ¿Riesgo de copyright? | No |
| ¿Declarar contenido sintético? | No |
| ¿Problema de monetización? | Bajo |

**Riesgos y notas:** Datos de GTA V de conocimiento público. Ninguna imagen de GTA V/VI.
