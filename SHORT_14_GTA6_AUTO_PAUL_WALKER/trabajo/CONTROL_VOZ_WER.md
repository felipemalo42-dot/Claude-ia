# Control de la voz: guion frente a narración final (WER) — El auto de Paul Walker está en GTA 6

Audio comprobado: `trabajo/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 111 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 2 |
| **WER final** | **1.802%** (coincidencia 98.198%) |
| WER solo con Parakeet TDT v3 | 4.505% (5 errores) |
| WER solo con Whisper small | 9.009% (10 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 2.703% (3 errores en 111 palabras, 3 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 17.1 dB · percentil 5 1.6 dB · mínimo 0.1 dB (76 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **NO CUMPLE**.

## Diferencias que quedan (frase a frase)

- 5.33 s · «Es el Eclipse verde de la primera película; aquí se llama Penumbra FF.» → Parakeet: «Es el eclipse verde de la primera película. Aquí se llama penumbra FF.» · Whisper: «Es el eclipse verde de la primera película. Aquí se llama penumbra FF.» · sustitución: «ff» → «efe / efe» | inserción: «» → «efe / efe»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 13.31 s · «garaje» = «garage»

Uniones o separaciones de palabras (la separación entre palabras no se oye): ninguna.

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.15 | 20.65 | 53 | 3 | 3 | 3 | sustitución: «ff» → «efe / efe» | inserción: «» → «efe / efe» | inserción: «» → «y / y» |
| 20.16 | 38.11 | 43 | 0 | 5 | 0 |  |
| 37.93 | 44.36 | 15 | 2 | 0 | 0 |  |
