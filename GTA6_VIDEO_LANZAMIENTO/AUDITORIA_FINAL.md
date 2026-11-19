# GTA6_VIDEO_LANZAMIENTO: auditoría final

**Vídeo:** *GTA 6 ya se juega: qué dicen de su jugabilidad quienes ya lo han jugado* · `VIDEO_FINAL.mp4` · revisado el 19/11/2026 sobre el archivo final.

## Datos técnicos medidos

| Comprobación | Resultado |
|---|---|
| Duración | **11:05** (665,1 s), incluida la pantalla final de 20 s |
| Vídeo | AV1 10 bits, 1920 × 1080, 30 fps, 19952 fotogramas |
| Audio | AAC, 48 kHz, 2 canales |
| Tamaño | 92,1 MB (límite de GitHub: 100 MB) |
| Sonoridad integrada | −14,2 LUFS (objetivo de YouTube: −14) |
| Narración | 1694 palabras, voz C (la misma del canal) |
| Coincidencia guion ↔ voz | **99,66 %** global (26 sonidos distintos de 7662); 51 de 60 tomas ≥ 99,5 % |
| Sincronía imagen ↔ palabra | **154 de 154 cortes (100 %)** a ≤ 0,10 s del inicio de su palabra |
| Planos | 192 (media 3,4 s por plano) |

**Detalle de la medición de la voz:**
- Hay 9 tomas por debajo del 99,5 % (la más baja, 95,6 %).
- En todas, la diferencia es un nombre en inglés que el reconocedor escribe de otra forma: «UroGamer», «Gameyspot», «Y Gene» (IGN), «Take 2», «Kik». No es un error de la voz.
- Se corrigió un error real de pronunciación («Games» se leía con jota) y esas tomas se volvieron a generar.
- Detalle toma por toma, con las dos transcripciones: `recursos/control_de_voz.csv`.

**Cómo se mide la sincronía:**
- Cada plano está anclado a la palabra que lo motiva, y el corte se hace 2 fotogramas antes del inicio de esa palabra.
- Los 154 cortes con ancla caen a menos de 0,10 s de su palabra.
- Las partes del render se unen sin perder fotogramas: un fotograma menos que el máximo teórico, recortado al final para ajustarse a la duración exacta del audio.
- Registro plano a plano: `recursos/registro_de_planos.csv`.

**Límite honesto:** no puedo escuchar el audio. Antes de publicar, mira el vídeo completo (11 minutos).

---

## Control de calidad (lista del encargo)

| Comprobación | Resultado |
|---|---|
| ¿Dura más de 10 minutos? | **Sí**: 11:05 (10:45 de contenido más 20 s de pantalla final). |
| ¿Es posterior al lanzamiento? | **Sí**. Todo el guion sale de información publicada desde el 18/11/2026:<br>- reseñas de quien jugó la versión final;<br>- Digital Foundry;<br>- primeros jugadores de Nueva Zelanda;<br>- récord de audiencia y primeras quejas.<br>Lo único anterior está rotulado como tal (las 80 horas y el tamaño del mapa, ambos de Rockstar). |
| ¿Información falsa? | **No**. Cada dato lleva la fuente en pantalla y en `FUENTES_Y_ENLACES.txt`.<br>Las quejas de jugadores se presentan como «sin confirmar por Rockstar».<br>Las cifras que varían según el medio (reseñas en Metacritic, espectadores) se dan como «más de», con el rango en pantalla. |
| ¿Imágenes auténticas o rotuladas? | **Sí**. 130 planos son material oficial de Rockstar. Los gráficos propios (mapa, perfil, carreras de drones) llevan el rótulo «Representación» o «Sin imagen oficial». No hay imágenes generadas por IA. |
| ¿Lo visual corresponde a la narración? | **Sí**. 154 de 154 cortes están sincronizados con su palabra. Cada medio citado aparece en pantalla cuando se le nombra, y cada actividad o mecánica, con su plano. |
| ¿Spoilers? | **Solo en el capítulo 4 (3:45-4:46).** Lleva:<br>- un cartel de aviso con el minuto para saltarlo;<br>- un rótulo rojo permanente;<br>- el aviso en la descripción.<br>Son escenas de misión del Extended Look oficial (atraco e infiltración), sin rehenes, cuerpos ni diálogos de trama. Título y miniatura sin spoilers. |
| ¿Derechos y permisos suficientes? | **Para uso no comercial, sí**: la política de Rockstar y la página «Download and share». **Para monetizar, no.** Ver `REGISTRO_DE_PERMISOS.txt`. |
| ¿Música sin licencia? | **No**. El audio oficial va silenciado; la música es original. |
| ¿Subtítulos sincronizados? | **Sí**. Subtítulos dinámicos incrustados palabra a palabra, y `SUBTITULOS.srt` con los tiempos reales de la voz. |
| ¿Buen ritmo? | **Sí**:<br>- un plano nuevo cada 3,4 s de media;<br>- los planos de vídeo de más de 4,6 s cambian de encuadre;<br>- 16 capítulos;<br>- una pregunta a la audiencia;<br>- avisos y rótulos de actividad. |
| ¿Aportación original suficiente (contenido reutilizado)? | **Sí**:<br>- guion propio de 1.694 palabras;<br>- análisis y comparación de medios;<br>- gráficos propios;<br>- ningún vídeo oficial completo: el plano oficial más largo dura 6,7 s;<br>- música original.<br>Aun así, el vídeo se basa en material ajeno: por eso **no se monetiza**. |
| ¿Se promete monetización? | **No**. Hay que publicarlo con los anuncios desactivados. |
| ¿Clips de streamers? | **No se usan**. Este entorno no llega a YouTube ni a Twitch, el control de permisos bloqueó la descarga y no hay permiso escrito. Plantilla para pedirlo: `00_INFORMES/PLANTILLA_PERMISO_STREAMERS.md`. |

## Antes de publicar
1. Mira el vídeo completo, sobre todo los nombres en inglés (1:12-1:35, medios; 6:48-7:24, Digital Foundry).
2. Abre 3 o 4 enlaces de `FUENTES_Y_ENLACES.txt` y comprueba que las notas no han cambiado: Metacritic puede subir o bajar con nuevas reseñas.
3. En YouTube Studio:
   - **monetización desactivada**;
   - **contenido alterado o sintético: Sí**;
   - sube `SUBTITULOS.srt`;
   - pega `DESCRIPCION_YOUTUBE.txt`, con capítulos y aviso de spoiler;
   - fija el comentario de `PUBLICACION_YOUTUBE.md`;
   - configura la pantalla final.
4. Formato: `VIDEO_FINAL.mp4` está en **AV1**, que YouTube acepta. Si tu reproductor no lo abre, usa VLC o un navegador.
