# Auditoría final — VIDEO_LARGO_GTA6 y SHORT_PROMOCIONAL_GTA6

Comprobaciones hechas sobre los archivos finales (ver CONTROL_DE_CALIDAD.md y CONTROL_VOZ_WER.md).

## Vídeo largo

| Requisito | Estado | Dato |
|---|---|---|
| Dura al menos 10 minutos | ✅ | 679 s |
| Idea nueva para el canal | ✅ | Matriz de temas en INVESTIGACION_Y_CONCEPTO.md: la policía y el perfil criminal no se habían tratado |
| Gameplay reciente (posterior al lanzamiento) | ✅ | Partidas publicadas el 19 y el 20/11/2026 (7 vídeos) |
| No recicla material de vídeos anteriores | ✅ | ninguna fuente repetida |
| Narrativa clara | ✅ | Gancho → introducción → 7 capítulos (del testigo a la etiqueta permanente) → resumen y preguntas |
| Imagen fluida, 30 fps constantes | ✅ | 30/1 (media 30/1) · 1 duración(es) de fotograma distinta(s) · repetidos o congelados por el montaje: 0 · saltos atrás: 0 |
| Sin congelados ni saltos | ✅ | 125 de 125 |
| Tirones que ya trae la grabación original | ℹ️ | 43 de 8886 fotogramas de gameplay repiten imagen en el propio original (el juego o la captura); comprobado contra los originales en archive.org. El montaje y la conversión no añaden ninguno |
| Negro en pantalla | ✅ | 1 (0.0-0.6 s): solo la entrada antes de la primera palabra |
| Correspondencia audio ↔ guion ≥ 99,8 % | ✅ | WER 0.058% sobre el audio final: 1 palabra(s) distinta(s) de 1711 (detalle en CONTROL_VOZ_WER.md) |
| Uniones entre tomas (bloques de ~20 s) | ✅ | WER 0.058% (1 errores en 1711 palabras, 36 bloques): ningún error nuevo en las uniones (las diferencias son las mismas de la comprobación frase a frase) |
| Nombres propios, cifras y términos de GTA | ✅ | términos clave que no reconoce ningún reconocedor: 0 (lista en CONTROL_VOZ_WER.md) |
| Voz sin cortes bruscos, sílabas perdidas ni solapes | ✅ | tomas que terminan de golpe: 0 · solapes: 0 |
| La música no tapa la voz | ✅ | voz por encima de música + efectos mientras hay voz: mediana 20.4 dB · percentil 5 7.7 dB · mínimo -2.7 dB (1114 ventanas de 0,5 s) (objetivo: percentil 5 ≥ 6 dB) |
| Subtítulos iguales al guion | ✅ | diferencias: 0 |
| La imagen corresponde a lo que se narra | ✅ | Cada plano anclado a la palabra que lo motiva (registro_de_planos.csv) |
| Resolución y códec | ✅ | H264 High · 1920×1080 · yuv420p |

## Short promocional

| Requisito | Estado | Dato |
|---|---|---|
| Gancho en los primeros segundos | ✅ | «Si ves este mensaje en GTA 6, ya es demasiado tarde» sobre el mensaje real |
| Se entiende sin ver el vídeo largo | ✅ | Contexto propio: qué es la sexta estrella y qué la hace distinta |
| Deja curiosidad (no resuelve) | ✅ | Termina en la pregunta sobre el perfil criminal |
| Usa fragmentos del vídeo largo | ✅ | Misma partida de IGN y mismos momentos (recortes verticales 4K) |
| Vertical 1080×1920 | ✅ | H264 High · 1080×1920 · yuv420p · 30/1 (media 30/1) · 1 duración(es) de fotograma distinta(s) |
| Duración 35-60 s | ✅ | 43.7 s |
| Audio ↔ guion | ✅ | WER 0.0% |
| Voz sin cortes bruscos ni solapes | ✅ | tomas que terminan de golpe: 0 · solapes: 0 · términos clave sin reconocer: 0 |
| La música no tapa la voz | ✅ | voz por encima de música + efectos mientras hay voz: mediana 19.9 dB · percentil 5 10.1 dB · mínimo 2.6 dB (68 ventanas de 0,5 s) (objetivo: percentil 5 ≥ 6 dB) |
| Imagen fluida | ✅ | repetidos o congelados por el montaje: 0 · saltos atrás: 0 · repetidos en la grabación original: 4 |
| Subtítulos iguales al guion | ✅ | diferencias: 0 |
| Llamada a la acción | ✅ | Verbal («tienes el enlace justo aquí abajo»), rótulo «VIDEO RELACIONADO» con flecha y miniatura del vídeo largo; comentario fijado y descripción |
| «Vídeo relacionado» configurado | ⚠️ | Preparado: se activa al subir el Short en YouTube Studio (pasos en CONFIGURACION_VIDEO_RELACIONADO.txt). Requiere acceso al canal |

