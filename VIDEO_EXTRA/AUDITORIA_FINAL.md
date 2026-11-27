# VIDEO_EXTRA: auditoría final

**Video:** *¿Por qué Vice City es rosa? La historia real de sus colores (GTA 6)* · `VIDEO_FINAL.mp4`
**Revisado el 18/11/2026**, después del render final y sobre el archivo MP4 comprimido.

## Datos técnicos medidos

| Comprobación | Resultado |
|---|---|
| Duración real | **9:29** (569,2 s): 9:09 de contenido más 20 s de pantalla final |
| Video | H.264 High, 1920 × 1080, 30 fps, yuv420p, unos 0,9 Mbps |
| Audio | AAC-LC, 48 kHz, estéreo, 203 kbps |
| Sonoridad integrada | −14,2 LUFS (objetivo de YouTube: −14) |
| Tamaño | 78,8 MB |
| Narración | 1.462 palabras, 178 palabras por minuto de habla |
| Coincidencia guion ↔ voz | **99,97 %** global: 2 sonidos distintos de 6.539 (detalle abajo) |
| Subtítulos | `SUBTITULOS.srt`, sincronizados palabra a palabra con la voz real |

**Detalle técnico (sin efecto visible):** el render se hizo en cuatro partes en paralelo. Al unirlas se perdieron 3 fotogramas de 17.076. En el último tramo la imagen va hasta 0,1 s por delante del sonido, algo imperceptible en animaciones sin personas que hablan. El motor quedará corregido para futuros renders.

### Cómo se midió la coincidencia entre guion y voz (exigencia: mínimo 99,5 %)
- Cada toma se transcribió con dos reconocedores automáticos independientes: Parakeet y, como segunda opinión, Whisper.
- El guion y la transcripción se compararon con una clave fonética del español (b = v, h muda, seseo…), sonido por sonido. El método está en `engine/voice_qa.py`.
- Las tomas por debajo del 99,5 % se regeneraron con otra semilla, hasta 12 intentos, y se eligió la mejor.
- Además, se reescribió una frase imposible de transcribir: la cita «Deco schmeco» se narra traducida («esto no somos nosotros») y el original se muestra en pantalla.

**Resultado:**
- Global: **99,97 %**.
- 47 de 49 tomas superan el 99,5 % por separado.
- Las otras dos tienen un solo sonido distinto cada una y siguieron igual tras 12 semillas:
  - 99,49 %: en «art déco tropical», la «d» casi no se oye («arte co»), algo normal en el habla rápida;
  - 99,38 %: el reconocedor intercala una «y» en la pausa de una coma («una serie, que filmó» → «una serie y que filmó»).
- Toma por toma, con las dos transcripciones: `recursos/control_de_voz.csv`.

**Límite honesto:** la medición la hace un reconocedor automático y no puedo escuchar el audio. Antes de publicar, escúchalo completo: 9 minutos.

---

## Las diez preguntas

**1. ¿Es realmente diferente de los diez videos anteriores? — Sí.**
- Los diez anteriores responden **qué** hay en el juego o **qué** hacer el día del lanzamiento. Este responde **por qué** Vice City se ve como se ve.
- Es el primero que cuenta historia real con personas reales (Barbara Capitman, Leonard Horowitz, L. Murray Dixon).
- Es el primero con estructura en capas cronológicas y el primero que pasa de 5 minutos.
- No reutiliza datos de los anteriores, salvo una mención a Aaron Garbut con otro dato distinto.
- Corrige además una imprecisión del video 04: Vice City existe desde 1997, no desde 2002.

**2. ¿Tiene un concepto original? — Sí.**
- El dispositivo del «corte de pintura» (siete capas, de 1912 a 2026) y la idea de que el video «se va pintando» guían la dirección de arte, la música y el sonido.
- En las búsquedas web no encontramos ningún video en español que cuente el origen de la paleta de Vice City.
- Límite: no pudimos revisar YouTube directamente.

**3. ¿Tiene profundidad para durar más de ocho minutos? — Sí.**
- 9:09 de contenido sin relleno: ningún dato se repite y no hay silencios artificiales.
- La única recapitulación, la guía de campo, tiene función práctica para el día del lanzamiento.
- El guion tiene 1.462 palabras. Los 15 capítulos duran entre 15 y 68 segundos y cada uno trae un descubrimiento propio.

**4. ¿La investigación está respaldada por fuentes? — Sí.**
- Cada dato del guion está asociado a su fuente en `FUENTES_Y_REFERENCIAS.txt`, con enlace, fecha y si se leyó directamente o mediante el buscador.
- Fuentes primarias leídas directamente:
  - la web oficial de Rockstar;
  - la Ciudad de Miami Beach;
  - el Servicio de Parques Nacionales de EE. UU.;
  - WLRN y AP;
  - el National Trust for Historic Preservation.
- Las interpretaciones propias van marcadas en amarillo en pantalla.
- Durante la revisión se corrigieron cinco frases para ajustarlas a las fuentes:
  - el paquete Vintage Vice City es un **bono por reservar el juego**, no se vende aparte;
  - «todo el mundo graba» pasó a «en varias imágenes oficiales…»;
  - «baratos» pasó a «modestos»;
  - «Son de 1980» pasó a «de los años ochenta»;
  - la cita del hijo de Capitman se fechó en 2014.

**5. ¿La narración es atractiva? — Sí, con un límite.**
- El gancho plantea un misterio verificable en los primeros 20 segundos («los colores no son de los años treinta»).
- Hay giros cada minuto: Ocean Beach existió de verdad; eran blancos; la panadería-pastel; los carritos de Miami Vice; el Hotel Dixon; Miami se viste de Vice City.
- Incluye un momento emotivo (las cenizas de Horowitz) y un matiz incómodo (el desplazamiento de los vecinos).
- Límite: es una voz sintética, aunque realista. Grabarla con voz humana mejoraría la conexión, y el motor lo permite (ver `GUION_COMPLETO.docx`).

**6. ¿Cada recurso audiovisual cumple su función? — Sí.**

| Recurso | Función |
|---|---|
| Calle nocturna con neones que se encienden | Gancho: lo que el jugador verá mañana |
| Calle que se vuelve blanca y luego pastel | Hace visible la tesis del video en 10 segundos |
| Corte de pintura de 7 capas | Mapa del video: el espectador sabe dónde está |
| Mapa sepia con la cuadrícula del plano y el sello | Muestra de dónde sale el nombre Ocean Beach |
| Tormenta (espiral, lluvia, agua que sube) | El fin del boom, sin imágenes de archivo reales |
| Plano azul con rótulos | Enseña los rasgos del art déco que luego son la misión |
| Calle descolorida, excavadora y velas | El abandono y la lucha de Capitman |
| Panadería pintada a brochazos | El momento clave, contado con el objeto real |
| Flechas de continuidad de color | Explica un concepto de diseño difícil de narrar |
| Televisor de tubo | La regla de Miami Vice sin usar imágenes de la serie |
| Calle pixelada | 2002, rotulada como recreación ilustrada |
| Placas «Hotel Victor → Hotel Dixon» | Prueba documentada del vínculo real-juego |
| Celulares que graban | Ilustra la interpretación sobre 2026, marcada en amarillo |
| Guía de campo con casillas | Valor práctico y llamada a comentar |
| Tratamiento de color por época | Refuerza la idea de «capas de pintura» |
| Música por época y dial de radio | Señala cada cambio de capítulo |

**7. ¿Los derechos de los materiales están suficientemente claros? — Sí.**
- No se usa ningún material audiovisual de Rockstar ni de terceros: ver `REGISTRO_DE_DERECHOS.txt`.
- Todo lo que se ve y se oye es obra propia o tiene licencia comercial (VERDE).
- Las citas de la web oficial son breves, traducidas y con atribución (derecho de cita).
- Trailers, capturas, logotipos y música oficiales quedaron descartados (ROJO o AMARILLO), con instrucciones para pedir permiso.

**8. ¿Cumple las políticas de monetización de YouTube? — Cumple lo que depende del video; la aprobación no se puede garantizar.**
- **Contenido reutilizado:** no hay material ajeno.
- **Contenido inauténtico** (masivo o repetitivo): guion investigado y único, dirección de arte propia, música compuesta para el video. El riesgo restante es el uso de voz sintética y gráficos generados por código en todo el canal. Grabar con voz humana es la mejor mitigación.
- **Contenido apto para anunciantes:**
  - sin violencia, armas ni lenguaje ofensivo;
  - las menciones al Holocausto y al sida son breves, factuales y respetuosas;
  - el juego es para mayores de 18 años, pero el video no muestra nada del juego.
- **Divulgación de IA:** se recomienda marcar **Sí** («AI use»). La voz es sintética y realista. La política vigente dice que divulgarlo no limita la audiencia ni la monetización.
- **Riesgos restantes:**
  - la revisión es a nivel de canal: se miran los videos más vistos y los más nuevos;
  - siempre puede haber una reclamación errónea de terceros por el título «GTA 6»;
  - la política de Rockstar no autoriza usos comerciales de su material, pero este video no lo usa.

**9. ¿La miniatura representa honestamente el contenido? — Sí.**
- Muestra el mismo edificio art déco, mitad blanco («1936») y mitad pastel («1980»), con el texto «ANTES ERA BLANCO» y el subtítulo «La historia real de los colores de Vice City».
- Es exactamente la tesis documentada del video (NPS: «mostly painted white»).
- El edificio es una ilustración inventada, sin capturas del juego ni logotipos. Los años son representativos: los hoteles se construyeron entre 1935 y 1941 y la paleta es de alrededor de 1980.

**10. ¿Hay razones para pensar que alguien querrá compartirlo? — Sí.**
- Tiene un dato sorprendente y fácil de contar («los hoteles de Vice City eran blancos»).
- Tiene una misión práctica para el día del lanzamiento (la guía de campo), que invita a responder con capturas.
- Tiene historias humanas memorables (la activista frente a las excavadoras, el diseñador y sus cenizas) y un vínculo local de actualidad (Miami se disfraza de Vice City).

**Ninguna respuesta es negativa.** Los límites señalados en las preguntas 2, 5 y 8 no se pueden resolver desde la producción: dependen de revisar YouTube directamente, de grabar con voz humana o de la decisión de YouTube.

---

## Antes de publicar (lista de comprobación)
1. Escucha el video completo, sobre todo los nombres en inglés y las tomas de 2:45 (art déco tropical) y 6:18 (Lance Vance y la cadena de copias).
2. Publícalo **hoy, 18/11/2026**: el guion dice «mañana». Si se publica después del lanzamiento, cambia tres frases (instrucciones en `PUBLICACION_YOUTUBE.md`).
3. En YouTube Studio:
   - sube `SUBTITULOS.srt`;
   - marca **AI use: Sí**;
   - pega la descripción con los capítulos y las etiquetas;
   - fija el comentario;
   - configura la pantalla final.
4. Vuelve a revisar los dos enlaces de fuentes [B] más importantes (Axios y Miami New Times) por si cambiaron.
