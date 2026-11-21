# Control de la voz: guion frente a narración final (WER) — Llevamos GTA 6 a juicio: ¿juego de crímenes o simulador de vida?

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1715 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 7 |
| **WER final** | **0.408%** (coincidencia 99.592%) |
| WER solo con Parakeet TDT v3 | 1.691% (29 errores) |
| WER solo con Whisper small | 5.073% (87 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.058% (1 errores en 1715 palabras, 37 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 2 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 20.4 dB · percentil 5 9.2 dB · mínimo -1.9 dB (1083 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **NO CUMPLE**.

## Diferencias que quedan (frase a frase)

- 268.17 s · «GTA 6 te premia por sacar la basura.» → Parakeet: «GTA VIST premia por sacar la basura.» · Whisper: «Jeteaséis este premio por sacar la basura.» · sustitución: «seis» → «— / jeteaseis» | sustitución: «te» → «vist / este»
- 273.39 s · «Karl McKittrick, un granjero con el brazo roto, necesita un piloto para fumigar sus cultivos, y ese piloto eres tú.» → Parakeet: «Carl McGitrick, un granjero con el brazo roto, necesita un piloto para fumigar sus cultivos, y ese piloto eres tú.» · Whisper: «Carl McKeithrick, un granjero con el brazo roto, necesita un piloto para fumigar sus cultivos y ese piloto eres tú.» · sustitución: «mckittrick» → «mcgitrick / mckeithrick»
- 472.58 s · «Según la prensa que recogió la entrevista, eso no significa que el juego castigue a quien prefiere el caos.» → Parakeet: «Según la prensa que recogió la entrevista, eso no significa que el juego casgue a quien prefiere el caos.» · Whisper: «Según la prensa que recogió la entrevista, eso no significa que el juego castilla quien prefiere el caos.» · sustitución: «castigue» → «casgue / —»
- 528.69 s · «GTA 6 te premia por arreglar la casa, por cuidar de tu pareja y hasta por sacar la basura.» → Parakeet: «Y te a seis te premia por arreglar la casa, por cuidar de tu pareja y hasta por sacar la basura.» · Whisper: «Jete a seis te premie por arreglar la casa por cuidar de tu pareja y hasta por sacar la basura.» · sustitución: «gta» → «a / a» | inserción: «» → «te / jete»
- 561.9 s · «Que en GTA puedas elegir entre el caos y la vida tranquila no es nuevo: en GTA 5 también podías jugar al golf, al tenis o hacer yoga.» → Parakeet: «Que en GTA puedir entre el caos y la vida tranquila no es nuevo, en GTA V también podrías jugar al golf, al tenis o hacer yoga.» · Whisper: «¿Qué inquieta puedes elegir entre el caos y la vida tranquila? No es nuevo. En GTA V también podías jugar al Golf, al Tennis o hacer Yoga.» · sustitución: «puedas» → «— / puedes»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 165.78 s · «caza» = «casa» | «caza» = «casa»
- 312.34 s · «ciervo» = «siervo» | «ciervo» = «siervo»
- 361.9 s · «objecion» = «objesion» | «interrumpe» = «interumpe»
- 485.54 s · «mapa» = «mapa191»
- 561.9 s · «tenis» = «tennis»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 6.15 s · «dejalo» = «deja lo»
- 145.97 s · «ya» = «y ya» | «felicita» = «felicita a»
- 308.74 s · «oyes» = «hoy es»
- 513.82 s · «alegato» = «al legato»
- 527.26 s · «alegato» = «al legato»

## Términos clave


- 268.17 s · «seis» en «GTA 6 te premia por sacar la basura.»
- 528.69 s · «gta» en «GTA 6 te premia por arreglar la casa, por cuidar de tu pareja y hasta por sacar la basura.»

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 19.76 | 50 | 0 | 0 | 0 |  |
| 19.55 | 37.05 | 57 | 1 | 0 | 0 |  |
| 36.7 | 52.23 | 39 | 0 | 0 | 0 |  |
| 52.1 | 68.05 | 47 | 1 | 2 | 0 |  |
| 67.64 | 87.36 | 47 | 0 | 3 | 0 |  |
| 86.97 | 98.78 | 32 | 0 | 4 | 0 |  |
| 99.25 | 119.23 | 61 | 2 | 2 | 0 |  |
| 119.18 | 133.07 | 41 | 0 | 0 | 0 |  |
| 133.02 | 152.42 | 55 | 0 | 0 | 0 |  |
| 152.81 | 172.56 | 50 | 0 | 0 | 0 |  |
| 172.41 | 186.78 | 36 | 1 | 2 | 0 |  |
| 186.85 | 202.1 | 44 | 0 | 0 | 0 |  |
| 201.94 | 220.58 | 44 | 0 | 0 | 0 |  |
| 220.42 | 239.12 | 55 | 0 | 0 | 0 |  |
| 239.08 | 252.92 | 45 | 0 | 0 | 0 |  |
| 252.88 | 270.98 | 56 | 0 | 2 | 0 |  |
| 270.96 | 285.34 | 37 | 0 | 1 | 0 |  |
| 285.2 | 303.3 | 47 | 0 | 0 | 0 |  |
| 303.16 | 320.49 | 52 | 0 | 4 | 0 |  |
| 320.43 | 335.66 | 44 | 0 | 1 | 0 |  |
| 335.51 | 353.51 | 53 | 0 | 0 | 0 |  |
| 353.27 | 368.16 | 35 | 0 | 0 | 0 |  |
| 368.18 | 386.8 | 51 | 0 | 0 | 0 |  |
| 386.65 | 404.06 | 49 | 1 | 3 | 1 | sustitución: «seis» → «cinco / gtss» |
| 403.69 | 423.56 | 55 | 2 | 0 | 0 |  |
| 423.45 | 442.08 | 48 | 0 | 2 | 0 |  |
| 441.99 | 458.16 | 45 | 0 | 1 | 0 |  |
| 457.65 | 472.33 | 41 | 0 | 0 | 0 |  |
| 472.38 | 485.48 | 34 | 0 | 1 | 0 |  |
| 485.34 | 498.87 | 42 | 2 | 2 | 0 |  |
| 498.62 | 515.63 | 42 | 1 | 0 | 0 |  |
| 515.38 | 534.42 | 59 | 0 | 7 | 0 |  |
| 534.15 | 552.72 | 54 | 0 | 0 | 0 |  |
| 552.54 | 571.41 | 50 | 0 | 4 | 0 |  |
| 571.26 | 588.89 | 56 | 0 | 0 | 0 |  |
| 588.87 | 607.21 | 58 | 0 | 1 | 0 |  |
| 606.97 | 609.83 | 4 | 0 | 0 | 0 |  |
