# Control de la voz: guion frente a narración final (WER) — GTA 6 no tiene primera persona… pero hay un truco

Audio comprobado: `trabajo/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 114 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 0 |
| **WER final** | **0.000%** (coincidencia 100.000%) |
| WER solo con Parakeet TDT v3 | 0.000% (0 errores) |
| WER solo con Whisper small | 7.018% (8 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.000% (0 errores en 114 palabras, 2 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 16.4 dB · percentil 5 6.0 dB · mínimo -4.4 dB (67 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción): ninguno.

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 4.73 s · «mapa a» = «mapa» | «mapa a» = «mapa»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.27 | 19.61 | 61 | 0 | 0 | 0 |  |
| 19.77 | 38.73 | 53 | 0 | 0 | 0 |  |
