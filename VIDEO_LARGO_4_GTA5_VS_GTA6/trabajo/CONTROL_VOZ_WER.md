# Control de la voz: guion frente a narración final (WER) — GTA 5 vs GTA 6: 8 asaltos con partidas reales

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1642 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 0 |
| **WER final** | **0.000%** (coincidencia 100.000%) |
| WER solo con Parakeet TDT v3 | 1.644% (27 errores) |
| WER solo con Whisper small | 5.664% (93 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.061% (1 errores en 1642 palabras, 36 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 20.8 dB · percentil 5 9.3 dB · mínimo -2.0 dB (1058 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

Ninguna: las dos transcripciones coinciden con el guion en todas las frases o al menos una de ellas lo hace.

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 195.3 s · «zancudo» = «sankudo»
- 201.26 s · «caza» = «casa»
- 223.41 s · «caza» = «casa» | «caza» = «casa»
- 230.92 s · «caza» = «casa» | «caza» = «casa»
- 430.21 s · «caza» = «casa»
- 537.61 s · «caza» = «casa»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 9.57 s · «con partidas» = «compartidas»
- 195.3 s · «zancudo» = «san kudo»
- 211.58 s · «pone en» = «ponen»
- 223.41 s · «embestir» = «en vestir» | «embestir» = «en vestir» | «ir» = «y ir»
- 374.24 s · «asalto» = «asalto o»
- 509.43 s · «funciona a» = «funciona» | «funciona a» = «funciona»
- 550.88 s · «todavia» = «todavia a»
- 583.91 s · «a gta» = «agta6»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 18.85 | 51 | 0 | 4 | 0 |  |
| 19.21 | 36.86 | 53 | 0 | 1 | 0 |  |
| 36.51 | 56.62 | 56 | 2 | 2 | 0 |  |
| 56.41 | 73.78 | 43 | 0 | 5 | 0 |  |
| 73.81 | 92.47 | 42 | 0 | 0 | 0 |  |
| 92.46 | 109.82 | 57 | 0 | 4 | 0 |  |
| 109.25 | 126.35 | 39 | 0 | 6 | 0 |  |
| 126.03 | 145.97 | 56 | 0 | 1 | 0 |  |
| 145.96 | 162.37 | 51 | 0 | 1 | 0 |  |
| 162.14 | 180.94 | 51 | 0 | 0 | 0 |  |
| 180.86 | 201.19 | 53 | 0 | 0 | 0 |  |
| 201.06 | 211.53 | 32 | 1 | 0 | 0 |  |
| 211.38 | 230.75 | 60 | 0 | 0 | 0 |  |
| 230.72 | 247.39 | 50 | 0 | 0 | 0 |  |
| 247.32 | 267.03 | 51 | 1 | 2 | 0 |  |
| 268.28 | 282.1 | 43 | 0 | 0 | 0 |  |
| 281.96 | 295.15 | 41 | 2 | 2 | 0 |  |
| 295.11 | 314.26 | 54 | 3 | 0 | 0 |  |
| 314.01 | 332.88 | 54 | 0 | 0 | 0 |  |
| 332.77 | 347.74 | 47 | 0 | 0 | 0 |  |
| 347.48 | 360.39 | 33 | 0 | 1 | 0 |  |
| 360.24 | 376.06 | 27 | 2 | 1 | 0 |  |
| 376.12 | 394.9 | 57 | 0 | 1 | 0 |  |
| 394.75 | 413.28 | 55 | 1 | 0 | 0 |  |
| 413.08 | 430.05 | 45 | 0 | 1 | 0 |  |
| 430.01 | 446.59 | 44 | 0 | 1 | 0 |  |
| 446.56 | 462.14 | 45 | 0 | 4 | 0 |  |
| 462.1 | 479.57 | 46 | 1 | 2 | 0 |  |
| 479.55 | 491.13 | 21 | 0 | 3 | 0 |  |
| 490.91 | 509.38 | 46 | 0 | 1 | 0 |  |
| 509.23 | 528.61 | 55 | 0 | 2 | 0 |  |
| 528.29 | 546.33 | 44 | 2 | 0 | 0 |  |
| 546.2 | 555.38 | 19 | 3 | 3 | 0 |  |
| 555.24 | 568.78 | 41 | 1 | 2 | 0 |  |
| 568.68 | 583.86 | 41 | 2 | 2 | 1 | sustitución: «asalto» → «— / sartor» |
| 583.71 | 597.78 | 39 | 0 | 0 | 0 |  |
