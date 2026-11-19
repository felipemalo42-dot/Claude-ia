# GTA6_VIDEO_LANZAMIENTO: auditoría final (versión 2)

**Vídeo:** *GTA 6 ya se juega: qué dicen de su jugabilidad quienes ya lo han jugado* · `VIDEO_FINAL.mp4` · revisado el 19/11/2026 sobre el archivo final.

**Qué cambia respecto a la versión 1:**
- Las imágenes ahora son **gameplay grabado y publicado tras el lanzamiento**: 134 planos, 393 s, el 57 % del vídeo. Antes eran el Extended Look y el tráiler.
- No queda ni un plano del Extended Look ni de los tráileres.
- La narración dice que el juego **ya se ha lanzado en todo el mundo**.
- El capítulo de spoilers enseña misiones que no salen en ningún tráiler.
- Aparece el **mapa del propio juego**.

## Datos técnicos medidos

| Comprobación | Resultado |
|---|---|
| Duración | **11:32** (692,2 s), incluida la pantalla final de 20 s |
| Vídeo | AV1 10 bits, 1920 × 1080, 30 fps, 20 767 fotogramas |
| Audio | AAC, 48 kHz, 2 canales |
| Tamaño | 92,9 MB (límite de GitHub: 100 MB) |
| Sonoridad integrada | −14,2 LUFS (objetivo de YouTube: −14) |
| Narración | 1792 palabras, voz C (la misma del canal) |
| Coincidencia guion ↔ voz | **99,65 %** global (28 sonidos distintos de 8021); 52 de 63 tomas ≥ 99,5 % |
| Sincronía imagen ↔ palabra | **165 de 165 cortes (100 %)** a ≤ 0,10 s del inicio de su palabra |
| Planos | 203 (media 3,3 s por plano) |
| Origen de las imágenes | Gameplay de terceros: 134 planos (393 s) · material oficial de Rockstar: 11 planos (25 s) · el resto, gráficos propios |

**Detalle de la medición de la voz:**
- Hay 11 tomas por debajo del 99,5 % (la más baja, 95,6 %).
- En todas, la diferencia es un nombre o una cifra que el reconocedor escribe de otra forma: «Y Gene»/«Ajene» (IGN), «GaSpot», «UroGamer», «metacrítica», «Take 2», «Kik», «Swims Charts», «P S5». No es un error de la voz.
- Se corrigió un error real: «Just Like Paradise» se leía con jota. Ahora se pronuncia «Yast Laik Páradais», y esa toma se volvió a generar.
- Detalle toma por toma, con las dos transcripciones: `recursos/control_de_voz.csv`.

**Cómo se mide la sincronía:**
- Cada plano está anclado a la palabra que lo motiva, y el corte se hace 2 fotogramas antes del inicio de esa palabra.
- Los 165 cortes con ancla caen a menos de 0,10 s de su palabra.
- Registro plano a plano: `recursos/registro_de_planos.csv`.

**Límite honesto:** no puedo escuchar el audio. Antes de publicar, mira el vídeo completo (11 minutos y medio).

---

## Control de calidad

| Comprobación | Resultado |
|---|---|
| ¿Dura más de 10 minutos? | **Sí**: 11:32 (11:12 de contenido más 20 s de pantalla final). |
| ¿Es posterior al lanzamiento? | **Sí, guion e imágenes**.<br>- **Guion:** sale de lo publicado desde el 18/11/2026: reseñas, Digital Foundry, primeros jugadores, récord de audiencia y primeras quejas.<br>- **Imágenes:** gameplay publicado el 18 y el 19/11.<br>- Lo único anterior al lanzamiento está rotulado como tal: las 80 horas y el tamaño del mapa, ambos dichos por Rockstar. |
| ¿Nada del Extended Look ni de los tráileres? | **Ningún plano.** Lo comprueba el registro: el material oficial que queda son 6 capturas, 1 ilustración y 3 vídeos de personaje. |
| ¿La imagen se ajusta a cada opinión? | **Sí**. Ejemplos:<br>- las frases de IGN van sobre el análisis en vídeo de IGN;<br>- la conducción, sobre persecuciones y derrapes;<br>- la policía, sobre la persecución de seis estrellas y el menú para cambiar de gorra y gafas;<br>- el rendimiento, sobre IGN en Series X, Series S y la comparativa PS5 Pro frente a Series S;<br>- las «físicas raras», sobre clips de directos;<br>- el buceo, sobre el buceo;<br>- el tamaño de Leonida, sobre el mapa del juego. |
| ¿Spoilers? | **Solo en el capítulo 4 (3:53-5:04).** Lleva:<br>- un cartel de aviso con el minuto para saltarlo;<br>- un rótulo rojo permanente;<br>- el aviso en la descripción.<br>Muestra un asalto a un banco, la primera misión («Just Like Paradise») y la misión del alquiler de Brian. Ninguna sale en los tráileres ni en el Extended Look: este se revisó entero, con un fotograma cada 8 s. El título y la miniatura no tienen spoilers. |
| ¿Contenido delicado? | Revisado plano a plano. Fuera quedan:<br>- los planos con cuerpos, sangre o desnudos;<br>- la cámara de los creadores (Swiss001 va encuadrado para dejarla fuera);<br>- los fragmentos de otros juegos que IGN intercala en su análisis (Red Dead Redemption 2, GTA IV, GTA V, Cyberpunk 2077 y GTA: San Andreas). |
| ¿Información falsa? | **No**. Cada dato lleva la fuente en pantalla y en `FUENTES_Y_ENLACES.txt`.<br>Lo que se cuenta de las misiones sale de los textos del propio juego, visibles en los vídeos («Collect Brian's rent», «Lose the cops»…).<br>Las quejas de jugadores se presentan como «sin confirmar por Rockstar». |
| ¿Créditos? | **En cada plano** (autor, título del vídeo y minuto) y en un gráfico al principio. Los 10 enlaces están en la descripción. |
| ¿Derechos y permisos? | **El gameplay de terceros no tiene licencia.** Se usa como cita breve, con crédito y sin monetizar, por decisión del canal. El plano ajeno más largo dura 7,5 s. Riesgos y qué hacer si alguien reclama: `REGISTRO_DE_PERMISOS.txt`. |
| ¿Música sin licencia? | **No**. Todo el audio original va silenciado; la música es propia. |
| ¿Subtítulos sincronizados? | **Sí**. Subtítulos dinámicos incrustados palabra a palabra, y `SUBTITULOS.srt` con los tiempos reales de la voz. |
| ¿Buen ritmo? | **Sí**:<br>- un plano nuevo cada 3,3 s de media;<br>- 16 capítulos;<br>- una pregunta a la audiencia;<br>- rótulos de actividad y de mapa. |
| ¿Aportación original suficiente? | **Sí**:<br>- guion propio de 1.792 palabras;<br>- análisis y comparación de medios;<br>- gráficos propios;<br>- ningún vídeo ajeno completo: solo fragmentos de 1 a 7,5 s, cada uno ligado a una frase.<br>Aun así, el vídeo se basa en material ajeno: por eso **no se monetiza**. |
| ¿Se promete monetización? | **No**. Hay que publicarlo con los anuncios desactivados. |

## Antes de publicar
1. Mira el vídeo completo, sobre todo:
   - los nombres en inglés (1:17-1:38, medios; 7:13-8:11, Digital Foundry);
   - el capítulo de spoilers (3:53-5:04).
2. Abre 3 o 4 enlaces de `FUENTES_Y_ENLACES.txt` y comprueba que las notas no han cambiado: Metacritic puede subir o bajar con nuevas reseñas.
3. En YouTube Studio:
   - **monetización desactivada**;
   - **contenido alterado o sintético: Sí**;
   - sube `SUBTITULOS.srt`;
   - pega `DESCRIPCION_YOUTUBE.txt` (4.656 caracteres, con capítulos, aviso de spoiler y créditos);
   - fija el comentario de `PUBLICACION_YOUTUBE.md`;
   - configura la pantalla final.
4. Si llega una reclamación de Content ID (IGN o Rockstar), no la dispute. Si un autor pide quitar su clip, sustituye sus planos (ver `REGISTRO_DE_PERMISOS.txt`).
5. Formato: `VIDEO_FINAL.mp4` está en **AV1**, que YouTube acepta. Si tu reproductor no lo abre, usa VLC o un navegador.
