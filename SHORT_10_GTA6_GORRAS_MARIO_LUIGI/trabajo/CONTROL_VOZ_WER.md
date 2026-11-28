# Control de la voz: guion frente a narración final (WER) — Las gorras de Mario y Luigi en GTA 6

Audio comprobado: `trabajo/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 111 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 1 |
| **WER final** | **0.901%** (coincidencia 99.099%) |
| WER solo con Parakeet TDT v3 | 2.703% (3 errores) |
| WER solo con Whisper small | 5.405% (6 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.000% (0 errores en 111 palabras, 3 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 18.2 dB · percentil 5 1.5 dB · mínimo -2.5 dB (76 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **NO CUMPLE**.

## Diferencias que quedan (frase a frase)

- 22.3 s · «¡y salta, como en Mario!» → Parakeet: «Y salta como armario.» · Whisper: «y salta a Cuman Mario.» · sustitución: «en» → «— / cuman»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción): ninguno.

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 29.79 s · «a las» = «alas»
- 32.56 s · «te la» = «tela» | «te la» = «tela»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.15 | 15.41 | 37 | 1 | 1 | 0 |  |
| 15.24 | 32.42 | 41 | 0 | 0 | 0 |  |
| 32.36 | 44.86 | 33 | 0 | 0 | 0 |  |
