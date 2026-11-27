# Control de la voz: guion frente a narración final (WER) — La policía de GTA 6: qué significa cada estrella (y cómo escapar siempre)

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1004 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 2 |
| **WER final** | **0.199%** (coincidencia 99.801%) |
| WER solo con Parakeet TDT v3 | 0.896% (9 errores) |
| WER solo con Whisper small | 3.884% (39 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.000% (0 errores en 1004 palabras, 20 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 1 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 21.9 dB · percentil 5 9.4 dB · mínimo -4.0 dB (610 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

- 0.55 s · «En GTA 6, la policía ya no te olvida solo porque te escondas detrás de un edificio.» → Parakeet: «En Geta Vis, la policía ya no te olvida solo porque te escondas detrás de un edificio.» · Whisper: «En Get A6, la policía ya no te olvida solo porque te escondas detrás de un edificio.» · sustitución: «seis» → «vis / a6»
- 257.7 s · «¿Y si asaltas el escondite de una banda?» → Parakeet: «Y si asaltas el esconite de una banda,» · Whisper: «y si asaltas el escognite de una banda» · sustitución: «escondite» → «esconite / escognite»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción): ninguno.

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 23.04 s · «con partidas» = «compartidas»
- 41.16 s · «alguien» = «a alguien»
- 88.45 s · «minimapa» = «mini mapa»
- 154.54 s · «con partidas» = «compartidas» | «con partidas» = «compartidas»
- 169.73 s · «controla a» = «controla»
- 245.56 s · «ve a» = «vea» | «ve a» = «vea»
- 260.02 s · «llega» = «llega a»
- 283.88 s · «dispara a» = «dispara» | «dispara a» = «dispara»
- 319.12 s · «borra» = «vor a»
- 331.2 s · «con partidas» = «compartidas» | «con partidas» = «compartidas»

## Términos clave


- 0.55 s · «seis» en «En GTA 6, la policía ya no te olvida solo porque te escondas detrás de un edificio.»

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 15.21 | 41 | 3 | 0 | 0 |  |
| 15.16 | 29.21 | 32 | 0 | 0 | 0 |  |
| 28.92 | 48.83 | 55 | 0 | 2 | 0 |  |
| 48.78 | 68.98 | 61 | 1 | 0 | 0 |  |
| 69.45 | 88.26 | 54 | 0 | 2 | 0 |  |
| 88.25 | 104.18 | 41 | 0 | 1 | 0 |  |
| 104.61 | 115.9 | 36 | 0 | 1 | 0 |  |
| 115.74 | 135.16 | 56 | 0 | 18 | 0 |  |
| 134.59 | 154.6 | 65 | 0 | 3 | 0 |  |
| 154.34 | 169.67 | 40 | 0 | 2 | 0 |  |
| 169.53 | 180.82 | 32 | 0 | 1 | 0 |  |
| 181.79 | 198.34 | 57 | 0 | 0 | 0 |  |
| 198.46 | 217.92 | 60 | 1 | 2 | 0 |  |
| 217.9 | 234.88 | 55 | 0 | 1 | 0 |  |
| 234.84 | 250.71 | 52 | 0 | 5 | 0 |  |
| 250.66 | 268.55 | 53 | 0 | 4 | 0 |  |
| 268.5 | 286.73 | 58 | 0 | 0 | 0 |  |
| 286.4 | 301.37 | 45 | 0 | 0 | 0 |  |
| 301.06 | 318.96 | 55 | 0 | 1 | 0 |  |
| 318.92 | 337.01 | 56 | 2 | 1 | 0 |  |
