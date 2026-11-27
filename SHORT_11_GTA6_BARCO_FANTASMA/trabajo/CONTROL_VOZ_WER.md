# Control de la voz: guion frente a narración final (WER) — El barco fantasma de GTA 6

Audio comprobado: `trabajo/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 107 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 1 |
| **WER final** | **0.935%** (coincidencia 99.065%) |
| WER solo con Parakeet TDT v3 | 4.673% (5 errores) |
| WER solo con Whisper small | 8.411% (9 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 1.869% (2 errores en 107 palabras, 3 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 18.2 dB · percentil 5 4.8 dB · mínimo -4.0 dB (77 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **NO CUMPLE**.

## Diferencias que quedan (frase a frase)

- 20.35 s · «Después, con equipo de buceo, nadas mar adentro… hasta que todo se llena de niebla.» → Parakeet: «Después, con equipo de buceo, nada asmar adentro, hasta que todo se llena de niebla.» · Whisper: «Después, con equipo de buceo, nada es mar adentro hasta que todo se llena de niebla.» · sustitución: «nadas» → «nada / es»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 5.23 s · «sube» = «suve»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 15.8 s · «lleva a» = «lleva» | «lleva a» = «lleva»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.15 | 20.24 | 49 | 2 | 2 | 2 | sustitución: «gta» → «a / a» | inserción: «» → «g / jet» |
| 20.15 | 40.39 | 41 | 1 | 2 | 0 |  |
| 40.35 | 47.12 | 17 | 0 | 2 | 0 |  |
