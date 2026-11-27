# Control de la voz: guion frente a narración final (WER) — Todos los finales de GTA 6 explicados (y cómo conseguir el bueno)

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1118 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 0 |
| **WER final** | **0.000%** (coincidencia 100.000%) |
| WER solo con Parakeet TDT v3 | 1.163% (13 errores) |
| WER solo con Whisper small | 4.293% (48 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.179% (2 errores en 1118 palabras, 21 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 22.2 dB · percentil 5 10.8 dB · mínimo -3.8 dB (655 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 14.2 s · «ves» = «vez» | «ves» = «vez»
- 93.47 s · «mendes» = «mendez»
- 244.92 s · «abe» = «ave» | «abe» = «ave»
- 281.46 s · «ahorros» = «aoros»
- 308.12 s · «ascensor» = «asensor»
- 313.26 s · «abe» = «ave» | «abe» = «ave»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 135.1 s · «cal ve» = «calve» | «cal ve» = «calve»
- 146.75 s · «recuerda» = «recuerda a»
- 223.56 s · «padre e» = «padre» | «hijo» = «y hijo»
- 251.29 s · «llega» = «llega a»
- 319.59 s · «cal abre» = «calabre» | «cal abre» = «calabre»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 18.34 | 49 | 0 | 0 | 0 |  |
| 18.2 | 34.13 | 47 | 0 | 1 | 0 |  |
| 34.05 | 51.48 | 51 | 0 | 1 | 0 |  |
| 51.43 | 68.19 | 52 | 1 | 2 | 0 |  |
| 68.11 | 84.49 | 51 | 0 | 1 | 0 |  |
| 84.07 | 104.45 | 64 | 0 | 3 | 0 |  |
| 104.35 | 118.6 | 45 | 1 | 0 | 0 |  |
| 118.47 | 134.87 | 52 | 0 | 1 | 0 |  |
| 134.9 | 150.41 | 46 | 1 | 4 | 1 | sustitución: «le» → «la / la» |
| 150.39 | 168.4 | 51 | 0 | 2 | 0 |  |
| 167.87 | 182.11 | 44 | 0 | 0 | 0 |  |
| 182.19 | 200.36 | 55 | 0 | 2 | 0 |  |
| 200.32 | 216.42 | 52 | 0 | 2 | 0 |  |
| 216.03 | 236.15 | 66 | 0 | 0 | 0 |  |
| 236.05 | 255.94 | 55 | 0 | 0 | 0 |  |
| 255.89 | 276.24 | 66 | 0 | 1 | 0 |  |
| 276.0 | 296.1 | 62 | 1 | 1 | 0 |  |
| 296.0 | 313.61 | 57 | 0 | 2 | 0 |  |
| 313.06 | 333.6 | 71 | 1 | 1 | 1 | inserción: «» → «despues / pues» |
| 333.59 | 353.48 | 53 | 0 | 0 | 0 |  |
| 352.95 | 365.91 | 29 | 2 | 0 | 0 |  |
