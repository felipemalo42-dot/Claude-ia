# Control de la voz: guion frente a narración final (WER) — El portal a la Vice City de PS2 en GTA 6

Audio comprobado: `trabajo/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 139 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 1 |
| **WER final** | **0.719%** (coincidencia 99.281%) |
| WER solo con Parakeet TDT v3 | 2.878% (4 errores) |
| WER solo con Whisper small | 10.072% (14 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 1.439% (2 errores en 139 palabras, 3 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 17.5 dB · percentil 5 5.0 dB · mínimo -5.1 dB (89 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **NO CUMPLE**.

## Diferencias que quedan (frase a frase)

- 29.26 s · ««Reactor 2».» → Parakeet: «Lector dos.» · Whisper: «L'Actor 2» · sustitución: «reactor» → «lector / actor»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción): ninguno.

Uniones o separaciones de palabras (la separación entre palabras no se oye): ninguna.

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.15 | 20.26 | 57 | 2 | 2 | 0 |  |
| 20.19 | 39.13 | 55 | 2 | 2 | 2 | sustitución: «reactor» → «actor / actor» | inserción: «» → «el / la» |
| 38.95 | 50.9 | 27 | 1 | 2 | 0 |  |
