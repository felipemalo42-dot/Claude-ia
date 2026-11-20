# Control de la voz: guion frente a narración final (WER) — Si ves este mensaje en GTA 6, ya es demasiado tarde

Audio comprobado: `../VIDEO_LARGO_GTA6/PROYECTO_DE_EDICION/short_promocional/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 105 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 0 |
| **WER final** | **0.000%** (coincidencia 100.000%) |
| WER solo con Parakeet TDT v3 | 0.000% (0 errores) |
| WER solo con Whisper small | 4.762% (5 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.000% (0 errores en 105 palabras, 3 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 19.9 dB · percentil 5 10.1 dB · mínimo 2.6 dB (68 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 4.0 s · «caza» = «casa» | «caza» = «casa»

Uniones o separaciones de palabras (la separación entre palabras no se oye): ninguna.

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.2 | 18.98 | 50 | 0 | 1 | 0 |  |
| 18.74 | 37.81 | 49 | 0 | 1 | 0 |  |
| 37.8 | 41.09 | 6 | 0 | 0 | 0 |  |
