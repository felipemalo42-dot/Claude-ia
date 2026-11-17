# Sal y Asfalto: paquete de lanzamiento del canal de GTA VI (10 videos)

> **Nombre e identidad nuevos (17/11/2026):** el nombre anterior, *Caimán Neón*, ya estaba en uso en YouTube. Se rediseñó toda la marca y se volvieron a producir los 10 videos con la identidad nueva. Ver `CANAL_IDENTIDAD/GUIA_DE_MARCA.md`.

Canal hispanohablante dedicado a **Grand Theft Auto VI**, preparado para el lanzamiento del **jueves 19 de noviembre de 2026**.
Todo el material audiovisual es **original**: guiones, voces sintéticas con licencia comercial, música y efectos sintetizados por código, animaciones e infografías vectoriales, mapas de dominio público. **No hay imágenes, música ni recursos de Rockstar Games.**

## Por dónde empezar
1. `00_INFORMES/INFORME_INVESTIGACION.md`: demanda, tabla de palabras clave y hechos verificados, con su nivel de certeza.
2. `00_INFORMES/POLITICAS_Y_DERECHOS.md`: políticas de YouTube, Rockstar y Take-Two, divulgación de IA y riesgos de monetización.
3. `00_INFORMES/ESTRATEGIA_LANZAMIENTO.md`: calendario con horarios para México, Colombia, Argentina y España.
4. `CANAL_IDENTIDAD/`: nombre, logotipo, avatar, banner, marca de agua y guía de marca.
5. `VIDEO_01` … `VIDEO_10`: cada carpeta tiene su `publicacion.md` (paquete completo) y los archivos para subir.
6. `00_INFORMES/INVENTARIO.md`: lista completa de archivos.

## Estado real de producción

| # | Video | Formato | Duración | Estado | Publicación sugerida (UTC) |
|---|---|---|---|---|---|
| 01 | GTA 6: hora exacta, precio, peso e idioma (7 comprobaciones) | Largo 16:9 | 4:52 | ✅ **Terminado** | mar 17 · 20:00 |
| 02 | ¿A qué hora sale GTA 6 en tu país? | Short 9:16 | 0:45 | ✅ **Terminado** | mié 18 · 12:00 |
| 03 | GTA 6 para PC y Android: la estafa que roba cuentas | Largo | 3:32 | ✅ **Terminado** | mié 18 · 15:00 |
| 04 | El mapa de Leonida: 6 regiones y sus lugares reales | Largo | 3:40 | ✅ **Terminado** | mié 18 · 19:00 |
| 05 | Jason y Lucía: el expediente (sin spoilers) | Largo | 3:21 | ✅ **Terminado** | vie 20 · 18:00 |
| 06 | GTA 6 vs GTA 5: 10 cambios confirmados | Largo | 3:37 | ✅ **Terminado** | sáb 21 · 17:00 |
| 07 | GTA 6 pesa 210 GB: ¿te cabe? | Short | 0:48 | ✅ **Terminado** | mar 17 · 23:00 |
| 08 | Fauna de Leonida: guía de campo | Short | 0:40 | ✅ **Terminado** | jue 19 · 17:00 |
| 09 | 7 misterios que se resuelven el jueves | Largo | 3:03 | ✅ **Terminado** | mié 18 · 21:00 |
| 10 | Abrimos los 7 sobres: lo comprobamos jugando | Largo (post-lanzamiento) | estimada 8-10 min | 🟡 **Preproducción**: faltan capturas propias y veredictos. El MP4 incluido es un **animático rotulado "NO PUBLICAR"** | lun 23 · 19:00 |

**Especificaciones verificadas de todos los MP4:** H.264 High, 1920×1080 (Shorts 1080×1920), 30 fps, yuv420p, AAC 48 kHz estéreo ~200 kbps, sonoridad integrada entre −14,1 y −14,5 LUFS.

## Contenido de cada carpeta `VIDEO_XX`
| Archivo | Qué es |
|---|---|
| `*.mp4` | Video final |
| `miniatura.png` | 1280×720 |
| `guion.txt` | Guion completo con secciones, marcas de tiempo, voz y notas visuales |
| `narracion.txt` / `marcas_de_tiempo.csv` | Texto de narración y tiempos por frase |
| `narracion.wav` / `narracion.mp3` | Narración original (24 kHz) y procesada (48 kHz) |
| `subtitulos.srt` | Subtítulos en español |
| `descripcion_youtube.txt` / `etiquetas.txt` | Listos para copiar y pegar (con capítulos y fuentes) |
| `publicacion.md` | Títulos (principal y 3 alternativos), palabras clave, intención, público, comentario fijado, divulgación de IA, fuentes, licencias y **auditoría de calidad** |
| `recursos/` | Música original (MP3), hoja de contactos y línea de tiempo |

## Limitaciones honestas (y cómo resolverlas)
1. **Investigación:**
   - Google Trends, el autocompletado de YouTube, Reddit y las webs de Rockstar y YouTube Help están bloqueados en este entorno. Se pidió ampliar el acceso y el servicio lo rechazó.
   - La investigación se hizo con búsqueda web, citando prensa y fuentes secundarias. **No hay volúmenes de búsqueda inventados.**
   - **Antes de publicar, comprueba tres datos en tus propias fuentes:** la hora en el soporte de Rockstar, el precio en tu tienda y el tamaño en tu consola.
2. **Voz:**
   - Voz femenina expresiva generada con **Chatterbox Multilingual** (Resemble AI, licencia MIT), a partir de una referencia de una locutora anónima del corpus abierto OpenSLR SLR72 (Google, CC BY-SA 4.0). Lee frase a frase con entonación natural; la voz la elegiste tú entre cuatro candidatas (voz C). Chatterbox añade una marca de agua inaudible que identifica el audio como sintético.
   - Cada toma se comprueba con reconocimiento de voz y se repite si no coincide con el guion. El resultado de cada video está en `recursos/control_de_voz.csv`. Aun así, **no puedo escucharla**: revisa el resultado.
   - Revisa cada narración antes de publicar.
   - Para reducir el riesgo de "contenido inauténtico", lo más eficaz es **grabar la narración con tu voz**. El motor lo admite: ver `engine/README.md`.
3. **Imagen:**
   - No había un generador de imágenes con IA disponible. Todo está dibujado por código (motion graphics vectoriales, mapa 3D en perspectiva, globo 3D).
   - Esto además **evita el riesgo legal de las imágenes de IA que imitan el juego**, que Take-Two ya persigue.
4. **Duración:**
   - Los videos largos duran entre 3:03 y 4:52: densos y sin relleno.
   - **Sin anuncios intermedios** (YouTube exige 8 minutos o más).
   - Para videos más largos, la estructura está lista para ampliar los guiones y volver a renderizar.
5. **Calidad del MP4:** se codificó compacto (5-28 MB) para que entrara en GitHub. Para subir a YouTube con la máxima calidad: `python engine/build.py vXX --master`.
6. **El video 10** no puede terminarse sin jugar. No se ha simulado ninguna prueba ni ningún resultado.
7. **Nombre del canal:** la búsqueda web no encontró ningún canal llamado "Sal y Asfalto", pero YouTube no se puede consultar desde aquí. Comprueba que `@SalYAsfalto` esté libre antes de crear el canal.
8. **Monetización:** nadie puede garantizarla. Los riesgos y lo que se hizo para reducirlos están en `00_INFORMES/POLITICAS_Y_DERECHOS.md`.

## Reconstruir o modificar
El motor completo (voz, música, efectos, animación y montaje) está en `engine/` y regenera cualquier video desde su guion. Ver `engine/README.md`.
