# Control de la voz: guion frente a narración final (WER) — Todos los finales de GTA 6 explicados (y cómo conseguir el bueno)

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1758 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 0 |
| **WER final** | **0.000%** (coincidencia 100.000%) |
| WER solo con Parakeet TDT v3 | 0.910% (16 errores) |
| WER solo con Whisper small | 3.584% (63 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.114% (2 errores en 1758 palabras, 34 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 22.3 dB · percentil 5 10.0 dB · mínimo -3.2 dB (1060 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 14.2 s · «ves» = «vez» | «ves» = «vez»
- 154.89 s · «mendes» = «mendez»
- 311.4 s · «liberty» = «liberti»
- 367.42 s · «abe» = «ave» | «abe» = «ave»
- 375.91 s · «abe» = «ave»
- 460.2 s · «ascensor» = «asensor»
- 465.34 s · «abe» = «ave»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 88.95 s · «lleva a» = «lleva»
- 203.75 s · «cal ve» = «calve» | «cal ve» = «calve»
- 228.28 s · «y aqui» = «yaqui»
- 259.38 s · «eligen no» = «eligeno»
- 311.4 s · «buscar a» = «buscara»
- 335.0 s · «padre e» = «padre» | «padre e» = «padre» | «hijo» = «y hijo»
- 478.02 s · «cal abre» = «calabre» | «cal abre» = «calabre»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 18.34 | 49 | 0 | 0 | 0 |  |
| 18.2 | 34.68 | 47 | 0 | 3 | 0 |  |
| 34.59 | 53.03 | 56 | 0 | 1 | 0 |  |
| 53.1 | 70.01 | 48 | 0 | 0 | 0 |  |
| 69.89 | 88.8 | 56 | 0 | 4 | 0 |  |
| 88.75 | 106.23 | 46 | 0 | 0 | 0 |  |
| 106.19 | 123.15 | 48 | 0 | 1 | 0 |  |
| 123.11 | 143.26 | 59 | 0 | 0 | 0 |  |
| 142.93 | 161.23 | 62 | 3 | 1 | 0 |  |
| 161.09 | 177.18 | 45 | 0 | 4 | 0 |  |
| 176.97 | 194.43 | 53 | 0 | 0 | 0 |  |
| 194.31 | 214.65 | 64 | 0 | 3 | 0 |  |
| 215.2 | 230.63 | 49 | 0 | 4 | 0 |  |
| 230.52 | 247.09 | 45 | 0 | 2 | 0 |  |
| 247.6 | 263.91 | 47 | 0 | 2 | 0 |  |
| 263.9 | 281.92 | 58 | 0 | 0 | 0 |  |
| 282.93 | 300.35 | 42 | 1 | 2 | 1 | sustitución: «jason» → «jas / son» |
| 300.29 | 317.3 | 52 | 0 | 1 | 0 |  |
| 316.88 | 334.92 | 49 | 0 | 1 | 0 |  |
| 334.8 | 348.34 | 45 | 0 | 0 | 0 |  |
| 348.2 | 367.42 | 53 | 2 | 0 | 0 |  |
| 367.22 | 384.91 | 53 | 0 | 0 | 0 |  |
| 384.77 | 400.73 | 57 | 0 | 0 | 0 |  |
| 400.81 | 416.38 | 47 | 1 | 0 | 0 |  |
| 416.15 | 436.25 | 62 | 1 | 2 | 1 | omisión: «y» → «— / —» |
| 436.15 | 449.79 | 42 | 1 | 0 | 0 |  |
| 449.59 | 469.91 | 76 | 0 | 4 | 0 |  |
| 469.86 | 487.01 | 52 | 0 | 0 | 0 |  |
| 487.14 | 505.74 | 57 | 0 | 0 | 0 |  |
| 505.36 | 522.19 | 48 | 0 | 2 | 0 |  |
| 521.91 | 541.22 | 51 | 2 | 2 | 0 |  |
| 540.93 | 558.76 | 50 | 0 | 0 | 0 |  |
| 558.86 | 578.77 | 56 | 0 | 1 | 0 |  |
| 578.65 | 593.77 | 34 | 2 | 0 | 0 |  |
