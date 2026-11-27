# Control de la voz: guion frente a narración final (WER) — 3 cosas GRATIS al empezar GTA 6

Audio comprobado: `trabajo/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 157 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 0 |
| **WER final** | **0.000%** (coincidencia 100.000%) |
| WER solo con Parakeet TDT v3 | 0.637% (1 errores) |
| WER solo con Whisper small | 8.280% (13 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.637% (1 errores en 157 palabras, 3 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 17.3 dB · percentil 5 5.9 dB · mínimo -1.0 dB (93 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción): ninguno.

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 22.74 s · «suroeste» = «su roeste»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.15 | 16.01 | 49 | 0 | 2 | 0 |  |
| 15.85 | 34.83 | 56 | 1 | 9 | 1 | sustitución: «southwind» → «southwin / swim» |
| 34.66 | 52.44 | 52 | 1 | 1 | 0 |  |
