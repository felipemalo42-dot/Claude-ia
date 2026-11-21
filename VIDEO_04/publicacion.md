# VIDEO_04 — El mapa de GTA 6 explicado: las 6 regiones de Leonida y los lugares reales que las inspiran

**Estado real:** TERMINADO · listo para publicar  
**Fase:** Pre-lanzamiento (actualizar con comentario fijado tras jugar)  
**Formato:** Largo (16:9) · **Duración:** 3:40 · **Música:** estilo «tropical» original · **Voz:** narradora

## A. Estrategia y posicionamiento

- **Título principal (SEO):** El mapa de GTA 6 explicado: las 6 regiones de Leonida y los lugares reales que las inspiran
- **Títulos alternativos:**
  1. Leonida región por región: lo que Rockstar confirmó del mapa de GTA 6 (y lo que no)
  2. Mapa de GTA 6: Vice City, Grassrivers, Ambrosia y más… sobre la Florida real
  3. Viajamos por Leonida antes del lanzamiento: 6 regiones, 6 pistas reales
- **Palabra clave principal:** mapa gta 6
- **Palabras clave secundarias:** leonida gta 6, regiones gta 6, vice city gta 6, grassrivers, port gellhorn, ambrosia gta 6, mount kalaga, leonida keys
- **Intención de búsqueda:** Exploración y curiosidad pre-lanzamiento.
- **Público:** Fans que quieren entender el mundo antes de jugar; interesados en Florida/Miami.
- **Duración:** 3:40
- **Por qué hacer clic:** Combina datos oficiales con inspiraciones reales, marcando qué es deducción; animación 3D original que evita los mapas falsos que circulan.

## B-C. Guion, voz y subtítulos

- Guion completo con marcas de tiempo y notas visuales: `guion.txt`
- Texto de narración: `narracion.txt` · marcas por frase: `marcas_de_tiempo.csv`
- Audio de narración: `narracion.wav` (24 kHz, original) y `narracion.mp3` (procesada, 48 kHz)
- Subtítulos: `subtitulos.srt` (súbelos como subtítulos en español en YouTube Studio)

## D-F. Recursos visuales, animación y montaje

- Vídeo final: `GTA6_mapa_Leonida_6_regiones_lugares_reales.mp4` · H.264 High, AAC 192 kbps 48 kHz, 30 fps, sonoridad −14 LUFS
- Hoja de contactos (un fotograma cada 5 s): `recursos/hoja_de_contactos.jpg`
- Música original del vídeo: `recursos/musica_original.mp3`
- Código fuente de todas las escenas: `engine/videos/v04.py` (re-renderizable)

## Descripción para YouTube (copiar y pegar)

```
Rockstar no ha publicado un mapa completo de Leonida. Con lo oficial (6 regiones, Mount Kalaga en la frontera norte, Ambrosia en el corazón del estado, el mapa “el doble que el de GTA 5” según Aaron Garbut en Game Informer) y la geografía real de Florida, recorremos Mount Kalaga, Port Gellhorn, Ambrosia, Grassrivers, Vice City y Leonida Keys.

⚠️ El mapa que ves es la FLORIDA REAL (Natural Earth), no el mapa del juego.

CAPÍTULOS
0:00 Gancho
0:16 Introducción
0:36 Tamaño
0:54 Parada 1 · Mount Kalaga
1:19 Parada 2 · Port Gellhorn
1:43 Parada 3 · Ambrosia
2:07 Parada 4 · Grassrivers
2:27 Parada 5 · Vice City
2:45 Parada 6 · Leonida Keys
3:00 Lo que no sabemos
3:19 Despedida

FUENTES
• Web oficial de Rockstar (regiones y descripciones), vía GTA BOOM / The Games Wiki / guías que la citan
• Game Informer n.º 382 (Aaron Garbut: mapa el doble que GTA V; +170 especies)
• Clewiston, “America's Sweetest Town” (dato real)
• Britton Hill, ≈105 m, punto más alto de Florida (dato real)

ℹ️ Transparencia: narración con voz sintética (modelo Chatterbox de Resemble AI, licencia MIT, con marca de agua inaudible) y animaciones originales de Sal y Asfalto. Este video NO contiene imágenes, música ni material de Rockstar Games. GTA y Grand Theft Auto son marcas de Take-Two Interactive; canal independiente, sin relación con Rockstar Games.

#GTA6 #GTAVI #Leonida
```

## Etiquetas

mapa gta 6, gta 6 mapa, leonida, vice city, grassrivers, port gellhorn, ambrosia, mount kalaga, leonida keys, gta 6 florida, gta 6 regiones, gta 6, sal y asfalto

## Comentario fijado recomendado

📌 Marcador de deducciones: el jueves volvemos a este mapa con el juego y marcamos aciertos ✅ y fallos ❌. ¿A qué región vas primero?

## Divulgación de IA (YouTube Studio → Detalles → Contenido alterado)

**Casilla “contenido alterado o sintético”: NO.** Todo el material visual es animación/infografía claramente no realista y la voz sintética no imita a ninguna persona real ni presenta hechos inventados como reales. Según los ejemplos de YouTube, esto no exige la etiqueta. Por transparencia, la descripción lo declara igualmente.

## Fuentes de investigación

- Web oficial de Rockstar (regiones y descripciones), vía GTA BOOM / The Games Wiki / guías que la citan
- Game Informer n.º 382 (Aaron Garbut: mapa el doble que GTA V; +170 especies)
- Clewiston, “America's Sweetest Town” (dato real)
- Britton Hill, ≈105 m, punto más alto de Florida (dato real)

## Recursos utilizados y licencias

- Música y efectos: compuestos y sintetizados por código para este video (engine/audio.py) · obra original, sin muestras de terceros.
- Voz: Chatterbox Multilingual de Resemble AI (licencia MIT) con referencia de una locutora anónima del corpus abierto OpenSLR SLR72 (Google, CC BY-SA 4.0; atribución: Guevara-Rukoz et al., LREC 2020). Ver engine/voces/README.md.
- Verificación y sincronización de la voz: reconocedor Parakeet TDT v3 de NVIDIA (CC-BY-4.0), usado solo como herramienta; no aparece en el video.
- Tipografías: Google Fonts con licencia SIL OFL 1.1 o Apache 2.0 (Anton, Inter, JetBrains Mono y las específicas del video).
- Gráficos: dibujados por código con Skia (BSD) · iconos propios (rutas SVG originales en engine/gfx.py).
- Codificación: FFmpeg (libx264 / AAC).
- Geografía: Natural Earth 1:50m (dominio público).
- Fuentes: DM Serif Display (OFL).

## Auditoría de calidad

| Comprobación | Resultado |
|---|---|
| ¿Contenido original? | Sí |
| ¿Aporta valor? | Sí: guía geográfica con certeza etiquetada |
| ¿Guion distinto a los demás? | Sí: viaje de norte a sur en 3D |
| ¿Imágenes adecuadas y autorizadas? | Sí: Natural Earth + dibujo propio; aviso permanente de que no es el mapa oficial |
| ¿Voz con calidad profesional? | Buena: voz femenina expresiva (Chatterbox Multilingual), leída por frases y párrafos cortos; cada toma verificada con reconocimiento de voz (ver recursos/control_de_voz.csv). Es una voz sintética: grabar con voz humana mejora autenticidad (ver README). |
| ¿Montaje con buen ritmo? | Sí: cámara 3D continua |
| ¿Título honesto? | Sí |
| ¿Miniatura corresponde? | Sí |
| ¿Información sin verificar? | Ubicaciones deducidas marcadas en amarillo |
| ¿Riesgo de copyright? | No |
| ¿Declarar contenido sintético? | No |
| ¿Problema de monetización? | Bajo |

**Riesgos y notas:** Las ubicaciones de Port Gellhorn y Grassrivers son deducciones (se dice en voz alta y en pantalla). Sin uso de mapas oficiales.
