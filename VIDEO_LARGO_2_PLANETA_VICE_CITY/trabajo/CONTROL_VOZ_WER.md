# Control de la voz: guion frente a narración final (WER) — Planeta Vice City: el documental de los humanos de GTA 6

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1580 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 2 |
| **WER final** | **0.127%** (coincidencia 99.873%) |
| WER solo con Parakeet TDT v3 | 2.152% (34 errores) |
| WER solo con Whisper small | 3.987% (63 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.253% (4 errores en 1580 palabras, 34 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 2 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 20.9 dB · percentil 5 10.1 dB · mínimo -3.5 dB (1056 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

- 581.03 s · «¿Qué es lo más raro que has visto hacer a un habitante de Vice City?» → Parakeet: «que es lo más raro que has visto hacer a un habitante de Vaisity.» · Whisper: «que es lo más raro que has visto hacer a un habitante de Bicycy.» · omisión: «vice» → «— / —» | sustitución: «city» → «vaisity / bicycy»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 52.4 s · «ves» = «vez»
- 67.56 s · «habitat» = «abitat»
- 79.63 s · «hamacas» = «amacas»
- 184.12 s · «press» = «pres»
- 209.71 s · «pesas» = «pezas»
- 215.63 s · «membresia» = «membrecia»
- 377.39 s · «dejennos» = «dejenos» | «dejennos» = «dejenos»
- 433.89 s · «enzarzado» = «ensarzado» | «enzarzado» = «ensarzado»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 302.12 s · «clasifica a» = «clasifica»
- 354.81 s · «entregarsela» = «entregarse la»
- 372.95 s · «por que» = «porque»
- 471.99 s · «detiene en» = «detienen» | «detiene en» = «detienen»
- 498.33 s · «zoologico» = «sol logico»

## Términos clave


- 581.03 s · «vice» en «¿Qué es lo más raro que has visto hacer a un habitante de Vice City?»
- 581.03 s · «city» en «¿Qué es lo más raro que has visto hacer a un habitante de Vice City?»

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 18.81 | 58 | 1 | 0 | 0 |  |
| 19.17 | 35.3 | 50 | 0 | 1 | 0 |  |
| 35.07 | 52.26 | 50 | 0 | 0 | 0 |  |
| 52.2 | 71.41 | 47 | 0 | 2 | 0 |  |
| 71.12 | 91.3 | 50 | 1 | 0 | 0 |  |
| 91.43 | 111.8 | 58 | 0 | 0 | 0 |  |
| 111.75 | 130.9 | 48 | 0 | 2 | 0 |  |
| 131.57 | 150.03 | 54 | 0 | 2 | 0 |  |
| 150.79 | 166.68 | 50 | 0 | 2 | 0 |  |
| 166.32 | 184.07 | 46 | 0 | 3 | 0 |  |
| 183.92 | 202.1 | 48 | 1 | 1 | 1 | sustitución: «press» → «— / res» |
| 201.91 | 215.58 | 38 | 0 | 2 | 0 |  |
| 215.43 | 234.48 | 46 | 0 | 0 | 0 |  |
| 234.15 | 250.36 | 49 | 0 | 0 | 0 |  |
| 250.03 | 266.41 | 44 | 0 | 0 | 0 |  |
| 266.36 | 286.69 | 44 | 2 | 0 | 0 |  |
| 286.44 | 302.24 | 38 | 0 | 0 | 0 |  |
| 301.92 | 315.62 | 33 | 0 | 2 | 0 |  |
| 315.07 | 329.75 | 41 | 0 | 3 | 0 |  |
| 329.55 | 349.67 | 47 | 0 | 6 | 0 |  |
| 349.4 | 365.0 | 35 | 0 | 1 | 0 |  |
| 364.9 | 383.27 | 51 | 1 | 3 | 0 |  |
| 383.05 | 400.9 | 42 | 0 | 1 | 0 |  |
| 400.86 | 420.63 | 52 | 0 | 3 | 0 |  |
| 420.5 | 440.97 | 51 | 0 | 0 | 0 |  |
| 440.93 | 455.94 | 38 | 2 | 2 | 2 | sustitución: «otros» → «otro / otro» | sustitución: «quedan» → «queda / queda» |
| 455.9 | 475.77 | 53 | 0 | 0 | 0 |  |
| 475.63 | 493.43 | 44 | 1 | 0 | 0 |  |
| 493.3 | 510.06 | 45 | 2 | 3 | 1 | sustitución: «paradise» → «paradis / parodparadais» |
| 510.05 | 529.41 | 55 | 0 | 1 | 0 |  |
| 530.8 | 544.81 | 29 | 0 | 1 | 0 |  |
| 545.52 | 561.11 | 41 | 0 | 0 | 0 |  |
| 560.96 | 581.15 | 49 | 0 | 1 | 0 |  |
| 580.83 | 600.88 | 56 | 0 | 5 | 0 |  |
