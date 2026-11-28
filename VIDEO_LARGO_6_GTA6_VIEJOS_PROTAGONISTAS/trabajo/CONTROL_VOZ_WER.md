# Control de la voz: guion frente a narración final (WER) — Niko Bellic está en GTA 6 (y no es el único)

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1687 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 3 |
| **WER final** | **0.178%** (coincidencia 99.822%) |
| WER solo con Parakeet TDT v3 | 1.956% (33 errores) |
| WER solo con Whisper small | 4.327% (73 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.119% (2 errores en 1687 palabras, 33 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 22.0 dB · percentil 5 11.3 dB · mínimo -2.5 dB (1048 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

- 359.65 s · «Y Packie McReary, de GTA 4, podía unirse a tus atracos en Los Santos.» → Parakeet: «Ipakri, de GTA IV, podía unirse a tus atracos en los santos.» · Whisper: «Ypachima Kriri, de Gete 4, podía unirse a tus atracos en los santos.» · omisión: «y» → «— / —» | sustitución: «packie» → «— / ypachima» | sustitución: «mcreary» → «ipakri / kriri»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 24.92 s · «niko» = «nico» | «niko» = «nico»
- 31.28 s · «niko» = «nico» | «niko» = «nico»
- 319.39 s · «forrada» = «forada»
- 348.02 s · «niko» = «nico» | «niko» = «nico»
- 351.94 s · «klebitz» = «klevits» | «klebitz» = «clevitz»
- 406.17 s · «niko» = «nico»
- 417.85 s · «niko» = «nico»
- 459.7 s · «niko» = «nico» | «niko» = «nico»
- 468.78 s · «niko» = «nico» | «niko» = «nico»
- 472.85 s · «niko» = «nico»
- 520.43 s · «niko» = «nico»
- 549.67 s · «niko» = «nico» | «niko» = «nico»
- 564.3 s · «vercetti» = «versetti»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 101.98 s · «granuja» = «gran uja»
- 130.21 s · «por que» = «porque»
- 201.85 s · «tomatelo» = «tomate lo»
- 326.03 s · «vertelas» = «verte las»
- 408.33 s · «aparece en» = «aparecen» | «dice en» = «dicen» | «aparece en» = «aparecen»
- 446.0 s · «la» = «la ha» | «ha liado» = «aliado» | «ha liado» = «aliado» | «envios» = «en bios»
- 496.52 s · «detener» = «de tener»
- 520.43 s · «niko» = «ni co»
- 574.14 s · «asfalto» = «a asfalto»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 20.23 | 50 | 2 | 0 | 0 |  |
| 20.16 | 38.79 | 57 | 0 | 5 | 0 |  |
| 38.46 | 58.96 | 60 | 0 | 0 | 0 |  |
| 58.91 | 78.99 | 60 | 0 | 0 | 0 |  |
| 79.11 | 97.6 | 50 | 0 | 2 | 0 |  |
| 97.52 | 116.45 | 57 | 2 | 0 | 0 |  |
| 116.11 | 135.47 | 55 | 0 | 1 | 0 |  |
| 135.48 | 155.57 | 52 | 0 | 2 | 0 |  |
| 155.42 | 168.41 | 32 | 0 | 0 | 0 |  |
| 168.41 | 184.73 | 49 | 0 | 0 | 0 |  |
| 184.71 | 201.8 | 56 | 2 | 4 | 1 | sustitución: «lo» → «los / los» |
| 201.65 | 219.12 | 50 | 2 | 1 | 0 |  |
| 218.97 | 239.26 | 57 | 1 | 4 | 0 |  |
| 239.22 | 259.17 | 63 | 4 | 3 | 0 |  |
| 258.9 | 276.46 | 53 | 0 | 0 | 0 |  |
| 276.35 | 295.12 | 51 | 2 | 0 | 0 |  |
| 295.0 | 310.01 | 48 | 0 | 3 | 0 |  |
| 309.97 | 330.25 | 59 | 1 | 0 | 0 |  |
| 330.5 | 350.4 | 50 | 2 | 0 | 0 |  |
| 350.06 | 368.69 | 49 | 4 | 0 | 0 |  |
| 368.55 | 385.0 | 52 | 0 | 1 | 0 |  |
| 384.69 | 402.74 | 55 | 0 | 0 | 0 |  |
| 402.69 | 417.96 | 43 | 4 | 2 | 0 |  |
| 417.65 | 435.58 | 57 | 2 | 2 | 0 |  |
| 435.57 | 455.58 | 62 | 0 | 5 | 0 |  |
| 455.64 | 474.77 | 54 | 0 | 0 | 0 |  |
| 474.65 | 488.79 | 42 | 0 | 1 | 0 |  |
| 488.24 | 506.91 | 52 | 1 | 1 | 0 |  |
| 506.57 | 524.9 | 48 | 1 | 4 | 0 |  |
| 524.67 | 535.65 | 34 | 0 | 1 | 0 |  |
| 535.59 | 549.6 | 45 | 2 | 1 | 1 | sustitución: «vercetti» → «bracchetti / birchetti» |
| 549.47 | 568.57 | 55 | 2 | 2 | 0 |  |
| 568.02 | 578.34 | 30 | 0 | 1 | 0 |  |
