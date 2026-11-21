# VIDEO_09 — 7 misterios de GTA 6 que se resuelven el jueves (y nuestras predicciones)

**Estado real:** TERMINADO · listo para publicar  
**Fase:** Pre-lanzamiento (publicar antes de la medianoche del 18/19)  
**Formato:** Largo (16:9) · **Duración:** 3:03 · **Música:** estilo «mystery» original · **Voz:** narradora

## A. Estrategia y posicionamiento

- **Título principal (SEO):** 7 misterios de GTA 6 que se resuelven el jueves (y nuestras predicciones)
- **Títulos alternativos:**
  1. Lo que todavía NO sabemos de GTA 6: 7 sobres sellados
  2. GTA 6: online, 60 fps, interiores… 7 preguntas sin respuesta
  3. Apostamos: 7 predicciones de GTA 6 antes del lanzamiento
- **Palabra clave principal:** gta 6 misterios
- **Palabras clave secundarias:** gta 6 online fecha, gta 6 60 fps, gta 6 interiores, gta 6 preguntas, gta 6 predicciones
- **Intención de búsqueda:** Curiosidad y conversación; puente a contenido post-lanzamiento.
- **Público:** Fans que siguen el lanzamiento y comentan.
- **Duración:** 3:03
- **Por qué hacer clic:** Formato de apuesta con medidor de confianza: invita a comentar y a volver para ver el resultado (VIDEO 10).

## B-C. Guion, voz y subtítulos

- Guion completo con marcas de tiempo y notas visuales: `guion.txt`
- Texto de narración: `narracion.txt` · marcas por frase: `marcas_de_tiempo.csv`
- Audio de narración: `narracion.wav` (24 kHz, original) y `narracion.mp3` (procesada, 48 kHz)
- Subtítulos: `subtitulos.srt` (súbelos como subtítulos en español en YouTube Studio)

## D-F. Recursos visuales, animación y montaje

- Vídeo final: `GTA6_7_misterios_que_se_resuelven_el_jueves.mp4` · H.264 High, AAC 192 kbps 48 kHz, 30 fps, sonoridad −14 LUFS
- Hoja de contactos (un fotograma cada 5 s): `recursos/hoja_de_contactos.jpg`
- Música original del vídeo: `recursos/musica_original.mp3`
- Código fuente de todas las escenas: `engine/videos/v09.py` (re-renderizable)

## Descripción para YouTube (copiar y pegar)

```
Siete preguntas que Rockstar no ha respondido, lo que sí sabemos y nuestras predicciones con un porcentaje de confianza. Las predicciones son opinión del canal (en amarillo), no información. El jueves los abrimos jugando.

CAPÍTULOS
0:00 Gancho
0:12 Reglas
0:25 Sobre 1
0:45 Sobre 2
1:04 Sobre 3
1:16 Sobre 4
1:34 Sobre 5
1:52 Sobre 6
2:08 Sobre 7
2:27 Cierre
2:43 Pantalla final

FUENTES
• FAQ de PlayStation / Take-Two (online)
• TweakTown / RockstarINTEL (30 fps)
• Rob Nelson (Rockstar), vía prensa (Perfil Criminal)
• Game Informer n.º 382 (huracanes, fauna, mapa ×2)
• Web oficial (6 regiones)

ℹ️ Transparencia: narración con voz sintética (modelo Chatterbox de Resemble AI, licencia MIT, con marca de agua inaudible) y animaciones originales de Sal y Asfalto. Este video NO contiene imágenes, música ni material de Rockstar Games. GTA y Grand Theft Auto son marcas de Take-Two Interactive; canal independiente, sin relación con Rockstar Games.

#GTA6 #GTAVI #Leonida
```

## Etiquetas

gta 6 misterios, gta 6 preguntas, gta 6 online, gta 6 60 fps, gta 6 predicciones, perfil criminal, gta 6 huracanes, gta 6, sal y asfalto

## Comentario fijado recomendado

📌 Deja tu predicción para el sobre que quieras (1-7). La más acertada se lleva este fijado después del lanzamiento 🔮

## Divulgación de IA (YouTube Studio → Detalles → Contenido alterado)

**Casilla “contenido alterado o sintético”: NO.** Todo el material visual es animación/infografía claramente no realista y la voz sintética no imita a ninguna persona real ni presenta hechos inventados como reales. Según los ejemplos de YouTube, esto no exige la etiqueta. Por transparencia, la descripción lo declara igualmente.

## Fuentes de investigación

- FAQ de PlayStation / Take-Two (online)
- TweakTown / RockstarINTEL (30 fps)
- Rob Nelson (Rockstar), vía prensa (Perfil Criminal)
- Game Informer n.º 382 (huracanes, fauna, mapa ×2)
- Web oficial (6 regiones)

## Recursos utilizados y licencias

- Música y efectos: compuestos y sintetizados por código para este video (engine/audio.py) · obra original, sin muestras de terceros.
- Voz: Chatterbox Multilingual de Resemble AI (licencia MIT) con referencia de una locutora anónima del corpus abierto OpenSLR SLR72 (Google, CC BY-SA 4.0; atribución: Guevara-Rukoz et al., LREC 2020). Ver engine/voces/README.md.
- Verificación y sincronización de la voz: reconocedor Parakeet TDT v3 de NVIDIA (CC-BY-4.0), usado solo como herramienta; no aparece en el video.
- Tipografías: Google Fonts con licencia SIL OFL 1.1 o Apache 2.0 (Anton, Inter, JetBrains Mono y las específicas del video).
- Gráficos: dibujados por código con Skia (BSD) · iconos propios (rutas SVG originales en engine/gfx.py).
- Codificación: FFmpeg (libx264 / AAC).
- Fuentes: Syne (OFL).

## Auditoría de calidad

| Comprobación | Resultado |
|---|---|
| ¿Contenido original? | Sí |
| ¿Aporta valor? | Sí: separa hechos de predicciones |
| ¿Guion distinto a los demás? | Sí: sobres sellados + medidores |
| ¿Imágenes adecuadas y autorizadas? | Sí |
| ¿Voz con calidad profesional? | Buena: voz femenina expresiva (Chatterbox Multilingual), leída por frases y párrafos cortos; cada toma verificada con reconocimiento de voz (ver recursos/control_de_voz.csv). Es una voz sintética: grabar con voz humana mejora autenticidad (ver README). |
| ¿Montaje con buen ritmo? | Sí |
| ¿Título honesto? | Sí |
| ¿Miniatura corresponde? | Sí |
| ¿Información sin verificar? | Predicciones = DEDUCCIÓN, dicho en voz y pantalla |
| ¿Riesgo de copyright? | No |
| ¿Declarar contenido sintético? | No |
| ¿Problema de monetización? | Bajo |

**Riesgos y notas:** Predicciones claramente rotuladas como DEDUCCIÓN en voz y pantalla.
