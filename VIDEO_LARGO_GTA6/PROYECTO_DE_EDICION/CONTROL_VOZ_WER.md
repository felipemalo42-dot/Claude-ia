# Control de la voz: guion frente a narración final (WER) — GTA 6 te está vigilando: del testigo a las 6 estrellas y el perfil criminal que no se borra

Audio comprobado: `PROYECTO_DE_EDICION/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1711 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 1 |
| **WER final** | **0.058%** (coincidencia 99.942%) |
| WER solo con Parakeet TDT v3 | 1.344% (23 errores) |
| WER solo con Whisper small | 2.864% (49 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.058% (1 errores en 1711 palabras, 36 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 0 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 0 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 20.4 dB · percentil 5 7.7 dB · mínimo -2.7 dB (1114 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **CUMPLE**.

## Diferencias que quedan (frase a frase)

- 334.9 s · «No siempre sale bien: chocar con uno de esos aviones, o destrozar el tren de aterrizaje contra las escaleras de embarque, termina la prueba antes de tiempo.» → Parakeet: «No siempre sale bien chocar con uno de sus aviones o destrozar el tren de aterrizaje contra las escaleras de embarque termina la prueba antes de tiempo.» · Whisper: «No siempre sale bien chocar con uno de sus aviones o destrozar el tren de aterrizaje contra las escaleras de embarque termina la prueba antes de tiempo.» · sustitución: «esos» → «sus / sus»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 7.56 s · «caza» = «casa» | «caza» = «casa»
- 413.65 s · «caza» = «casa» | «caza» = «casa»
- 640.66 s · «rozaste» = «rosaste»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 114.68 s · «vuelve en» = «vuelven»
- 172.91 s · «mejor es» = «mejores»
- 183.92 s · «ayuda» = «ayuda a»
- 203.32 s · «marca a» = «marca»
- 371.23 s · «ganartela» = «ganarte la»
- 376.37 s · «ganarsela» = «ganarse la» | «ganarsela» = «ganarse la»
- 399.37 s · «apunta a» = «apunta»
- 470.39 s · «deja a» = «deja»
- 479.71 s · «mata» = «mata a»
- 490.31 s · «ataca a» = «ataca» | «hasta a» = «hasta» | «hasta a» = «hasta»
- 509.32 s · «afecta a» = «afecta»
- 528.89 s · «en curtido» = «encurtido» | «en curtido» = «encurtido»

## Términos clave

Todos los nombres propios, cifras y términos de GTA del guion los reconoce al menos un reconocedor.

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.4 | 17.18 | 45 | 2 | 2 | 0 |  |
| 16.96 | 33.7 | 49 | 0 | 1 | 0 |  |
| 37.27 | 56.12 | 54 | 0 | 0 | 0 |  |
| 56.59 | 75.99 | 53 | 0 | 1 | 0 |  |
| 75.95 | 94.22 | 46 | 0 | 1 | 0 |  |
| 94.12 | 114.51 | 53 | 0 | 0 | 0 |  |
| 114.48 | 131.74 | 50 | 0 | 0 | 0 |  |
| 131.44 | 149.76 | 45 | 0 | 0 | 0 |  |
| 149.67 | 170.06 | 55 | 0 | 0 | 0 |  |
| 169.99 | 188.02 | 49 | 2 | 0 | 0 |  |
| 187.88 | 203.49 | 45 | 0 | 1 | 0 |  |
| 203.12 | 222.97 | 59 | 0 | 1 | 0 |  |
| 222.72 | 243.08 | 54 | 0 | 3 | 0 |  |
| 242.96 | 261.45 | 45 | 0 | 2 | 0 |  |
| 261.84 | 282.02 | 62 | 0 | 0 | 0 |  |
| 281.84 | 297.75 | 44 | 2 | 0 | 0 |  |
| 297.68 | 315.19 | 37 | 2 | 0 | 0 |  |
| 315.17 | 334.75 | 53 | 0 | 0 | 0 |  |
| 334.7 | 352.59 | 45 | 2 | 1 | 1 | sustitución: «esos» → «sus / sus» |
| 352.55 | 371.36 | 56 | 0 | 0 | 0 |  |
| 371.03 | 386.42 | 30 | 0 | 0 | 0 |  |
| 386.61 | 399.32 | 33 | 0 | 0 | 0 |  |
| 399.17 | 418.67 | 51 | 0 | 2 | 0 |  |
| 418.57 | 436.46 | 43 | 0 | 0 | 0 |  |
| 436.13 | 447.27 | 27 | 0 | 0 | 0 |  |
| 450.12 | 470.54 | 48 | 0 | 0 | 0 |  |
| 470.19 | 490.26 | 52 | 1 | 0 | 0 |  |
| 490.11 | 509.2 | 53 | 0 | 2 | 0 |  |
| 509.12 | 529.05 | 51 | 3 | 0 | 0 |  |
| 528.69 | 547.53 | 53 | 2 | 0 | 0 |  |
| 547.27 | 566.57 | 44 | 0 | 1 | 0 |  |
| 566.43 | 581.11 | 33 | 0 | 0 | 0 |  |
| 580.54 | 600.18 | 61 | 0 | 0 | 0 |  |
| 599.92 | 618.5 | 48 | 1 | 0 | 0 |  |
| 620.25 | 639.85 | 46 | 0 | 0 | 0 |  |
| 639.82 | 657.61 | 39 | 2 | 0 | 0 |  |
