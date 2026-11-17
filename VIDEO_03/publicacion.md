# VIDEO_03 — GTA 6 para PC y Android: la verdad (y la estafa que está robando cuentas)

**Estado real:** TERMINADO · listo para publicar  
**Fase:** Pre-lanzamiento (útil también durante los 30 días posteriores)  
**Formato:** Largo (16:9) · **Duración:** 3:32 · **Música:** estilo «tension» original · **Voz:** narradora + copiloto

## A. Estrategia y posicionamiento

- **Título principal (SEO):** GTA 6 para PC y Android: la verdad (y la estafa que está robando cuentas)
- **Títulos alternativos:**
  1. NO descargues “GTA 6 PC gratis”: así funciona el malware que roba tus cuentas
  2. GTA 6 APK y GTA 6 PC: por qué son falsos y qué hacer si ya lo instalaste
  3. La descarga más peligrosa de noviembre: anatomía de la estafa de GTA 6
- **Palabra clave principal:** gta 6 pc descargar
- **Palabras clave secundarias:** gta 6 apk, gta 6 android, gta 6 gratis, gta 6 malware, gta 6 estafa, gta 6 para pc
- **Intención de búsqueda:** Navegacional riesgosa → la convertimos en protección (servicio público).
- **Público:** Jugadores sin PS5/Series que buscan alternativas, sobre todo en Latinoamérica; padres y familiares.
- **Duración:** 3:32
- **Por qué hacer clic:** Ocupa una búsqueda masiva dominada por contenido engañoso con información verificada por empresas de seguridad (ESET, Cynet) y pasos de recuperación útiles.

## B-C. Guion, voz y subtítulos

- Guion completo con marcas de tiempo y notas visuales: `guion.txt`
- Texto de narración: `narracion.txt` · marcas por frase: `marcas_de_tiempo.csv`
- Audio de narración: `narracion.wav` (24 kHz, original) y `narracion.mp3` (procesada, 48 kHz)
- Subtítulos: `subtitulos.srt` (súbelos como subtítulos en español en YouTube Studio)

## D-F. Recursos visuales, animación y montaje

- Vídeo final: `GTA6_PC_Android_estafa_malware_investigacion.mp4` · H.264 High, AAC 192 kbps 48 kHz, 30 fps, sonoridad −14 LUFS
- Hoja de contactos (un fotograma cada 5 s): `recursos/hoja_de_contactos.jpg`
- Música original del vídeo: `recursos/musica_original.mp3`
- Código fuente de todas las escenas: `engine/videos/v03.py` (re-renderizable)

## Descripción para YouTube (copiar y pegar)

```
No existe GTA 6 para PC (sin fecha anunciada), ni para Android ni para iPhone. Los archivos que lo prometen son malware: ESET detectó “gta6_installer.exe” con el infostealer Vidar y Cynet otra variante con WARDEN. En este video: cómo funciona el anzuelo, qué roba y qué hacer si ya lo ejecutaste.

CAPÍTULOS
0:00 Gancho
0:17 Introducción
0:29 1 · la verdad corta
0:50 1b · por qué funciona
1:09 2 · anatomía del anzuelo
1:34 3 · lo que pide
1:49 4 · lo que se lleva
2:10 5 · variantes
2:29 6 · si ya lo ejecutaste
2:56 7 · regla de los 5 segundos
3:11 Despedida

FUENTES
• Help Net Security (13 nov. 2026): falsa descarga de GTA 6 que roba credenciales de Steam y monederos
• Security Boulevard (nov. 2026): “GTA 6 download” como búsqueda peligrosa
• Shattered.io: ESET y Vidar en gta6_installer.exe
• Neowin: estafas de descarga gratuita
• Take-Two: sin fecha para PC

ℹ️ Transparencia: narración con voz sintética (modelo Chatterbox de Resemble AI, licencia MIT, con marca de agua inaudible) y animaciones originales de Sal y Asfalto. Este video NO contiene imágenes, música ni material de Rockstar Games. GTA y Grand Theft Auto son marcas de Take-Two Interactive; canal independiente, sin relación con Rockstar Games.

#GTA6 #GTAVI #Leonida
```

## Etiquetas

gta 6 pc, gta 6 pc descargar, gta 6 apk, gta 6 android, gta 6 gratis, gta 6 descargar, gta 6 malware, gta 6 estafa, gta 6 virus, seguridad gamer, infostealer, gta 6, sal y asfalto

## Comentario fijado recomendado

📌 Si ya ejecutaste un “instalador de GTA 6”: 1) desconecta y analiza el equipo, 2) cambia contraseñas desde OTRO dispositivo (empieza por el correo), 3) cierra sesiones y activa 2FA. Comparte esto con quien lo necesite 🛡️

## Divulgación de IA (YouTube Studio → Detalles → Contenido alterado)

**Casilla “contenido alterado o sintético”: NO.** Todo el material visual es animación/infografía claramente no realista y la voz sintética no imita a ninguna persona real ni presenta hechos inventados como reales. Según los ejemplos de YouTube, esto no exige la etiqueta. Por transparencia, la descripción lo declara igualmente.

## Fuentes de investigación

- Help Net Security (13 nov. 2026): falsa descarga de GTA 6 que roba credenciales de Steam y monederos
- Security Boulevard (nov. 2026): “GTA 6 download” como búsqueda peligrosa
- Shattered.io: ESET y Vidar en gta6_installer.exe
- Neowin: estafas de descarga gratuita
- Take-Two: sin fecha para PC

## Recursos utilizados y licencias

- Música y efectos: compuestos y sintetizados por código para este video (engine/audio.py) · obra original, sin muestras de terceros.
- Voz: Chatterbox Multilingual de Resemble AI (licencia MIT) con referencia de una locutora anónima del corpus abierto OpenSLR SLR72 (Google, CC BY-SA 4.0; atribución: Guevara-Rukoz et al., LREC 2020). Ver engine/voces/README.md.
- Verificación y sincronización de la voz: reconocedor Parakeet TDT v3 de NVIDIA (CC-BY-4.0), usado solo como herramienta; no aparece en el video.
- Tipografías: Google Fonts con licencia SIL OFL 1.1 o Apache 2.0 (Anton, Inter, JetBrains Mono y las específicas del video).
- Gráficos: dibujados por código con Skia (BSD) · iconos propios (rutas SVG originales en engine/gfx.py).
- Codificación: FFmpeg (libx264 / AAC).
- Fuentes: Share Tech Mono, VT323 (OFL). Interfaces (buscador, diálogos) genéricas e inventadas: no imitan ninguna marca.

## Auditoría de calidad

| Comprobación | Resultado |
|---|---|
| ¿Contenido original? | Sí |
| ¿Aporta valor? | Sí: prevención y pasos de recuperación |
| ¿Guion distinto a los demás? | Sí: investigación con dos voces |
| ¿Imágenes adecuadas y autorizadas? | Sí: interfaces genéricas inventadas |
| ¿Voz con calidad profesional? | Buena: voz femenina expresiva (Chatterbox Multilingual), leída por frases y párrafos cortos; cada toma verificada con reconocimiento de voz (ver recursos/control_de_voz.csv). Es una voz sintética: grabar con voz humana mejora autenticidad (ver README). |
| ¿Montaje con buen ritmo? | Sí |
| ¿Título honesto? | Sí: el vídeo explica que no existe versión PC/Android |
| ¿Miniatura corresponde? | Sí |
| ¿Información sin verificar? | Datos de malware atribuidos a ESET/Cynet (REPORTADO) |
| ¿Riesgo de copyright? | No |
| ¿Declarar contenido sintético? | No |
| ¿Problema de monetización? | Bajo (contenido educativo de seguridad) |

**Riesgos y notas:** Tema sensible pero educativo: no muestra cómo crear malware, solo cómo reconocerlo. Sin enlaces a sitios maliciosos. Revisa la política de YouTube sobre engaños: no aplica (contenido de prevención).
