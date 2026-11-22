# Control de la voz: guion frente a narración final (WER) — GTA 5 vs GTA 6: 8 asaltos con partidas reales

Audio comprobado: `trabajo/audio/narracion_original.wav` (narración final, la misma que lleva el vídeo). Método en `engine/wer_final.py` y `engine/voice_qa.py`.

| Medida | Resultado |
|---|---|
| Palabras del guion | 1642 |
| Errores (por frase; una palabra es error si la fallan los dos reconocedores) | 5 |
| **WER final** | **0.305%** (coincidencia 99.695%) |
| WER solo con Parakeet TDT v3 | 2.192% (36 errores) |
| WER solo con Whisper small | 6.577% (108 errores) |
| WER en bloques de ~20 s (uniones entre tomas) | 0.061% (1 errores en 1642 palabras, 35 bloques) |
| Términos clave no reconocidos por ningún reconocedor | 3 |
| Tomas solapadas | 0 |
| Tomas que terminan de golpe con voz | 1 |
| Voz frente a música y efectos | voz por encima de música + efectos mientras hay voz: mediana 20.7 dB · percentil 5 9.4 dB · mínimo -0.3 dB (1055 ventanas de 0,5 s) |

Objetivo del encargo: WER ≤ 0,2 % (coincidencia ≥ 99,8 %). Resultado: **NO CUMPLE**.

## Diferencias que quedan (frase a frase)

- 26.38 s · «Las de GTA 5 vienen de versiones distintas, de dos mil trece y de la edición mejorada para PC, así que aquí no vamos a comparar gráficos: vamos a comparar lo que puedes hacer.» → Parakeet: «Las de G vienen de versiones distintas, de 2013 y de la edición mejorada para PC, así que aquí no vamos a comparar gráficos, vamos a comparar lo que puedes hacer.» · Whisper: «Las dajetas 5 vienen de reacciones distintas, de 2013 y de la edición mejorada para PC, así que aquí no vamos a comparar gráficos, vamos a comparar lo que puedes hacer.» · sustitución: «gta» → «— / dajetas»
- 125.21 s · «En GTA 5, el nivel de búsqueda máximo era de cinco estrellas, y cuando la policía te perdía de vista, las estrellas parpadeaban mientras te buscaban, hasta apagarse.» → Parakeet: «En GT5, el nivel de búsqueda máximo era de cinco estrellas y cuando la policía te perdía de vista, las estrelladeaban mientras te buscaban hasta apagarse.» · Whisper: «Ejete a 5, el nivel de búsqueda máximo era de 5 estrellas, y cuando la policía te perlía de vista, las estrellas parpadeaban mientras te buscaban hasta pagarse.» · sustitución: «gta» → «— / a»
- 429.47 s · «Tanto, que una de aquellas guías recomendaba cambiar a Franklin para robar el caza: su habilidad hacía más fácil cruzar la entrada de la base.» → Parakeet: «Tanto que una de aquellas recomendaba cambiar a Flanken para robar el caza. Su habilidad sea más fácil cruzar la entrada de la base.» · Whisper: «tanto que una de aquellas guías recomendaba cambiar a Franking para robar el casa. Su habilidad hacia más fácil cruzar la entrada de la base.» · sustitución: «franklin» → «flanken / franking»
- 538.03 s · «Y quedan en empate la ciudad, el caza y morir.» → Parakeet: «y que han en empate la ciudad el caza morir.» · Whisper: «y que en el empate de la ciudad el casa y morir.» · sustitución: «quedan» → «han / que»
- 541.28 s · «Resultado: tres asaltos para GTA 6, dos para GTA 5 y tres empates.» → Parakeet: «Resultado tres asaltos para GTA V, dos para GTA V y tres empates.» · Whisper: «Resultado 3 asaldos para JT6, 2 para JT5 y 3 empates.» · sustitución: «seis» → «cinco / jt6»

## Igualdades que no cuentan como error

Homófonos del español latinoamericano (misma pronunciación, otra ortografía en la transcripción):
- 194.2 s · «zancudo» = «sankudo» | «zancudo» = «sankudo»
- 200.36 s · «caza» = «casa»
- 222.5 s · «caza» = «casa» | «caza» = «casa»
- 230.02 s · «caza» = «casa» | «caza» = «casa»
- 394.05 s · «y» = «y1»
- 429.47 s · «caza» = «casa»
- 538.03 s · «caza» = «casa»

Uniones o separaciones de palabras (la separación entre palabras no se oye):
- 9.57 s · «con partidas» = «compartidas»
- 210.68 s · «pone en» = «ponen»
- 222.5 s · «embestir» = «en vestir» | «embestir» = «en vestir» | «ir» = «y ir»
- 447.03 s · «y lucia» = «ilusia»
- 509.69 s · «funciona a» = «funciona» | «funciona a» = «funciona»
- 530.59 s · «gta» = «gt a5»
- 576.39 s · «asalto» = «a salto»
- 580.55 s · «a gta» = «agta6»

## Términos clave


- 26.38 s · «gta» en «Las de GTA 5 vienen de versiones distintas, de dos mil trece y de la edición mejorada para PC, así que aquí no vamos a comparar gráficos: vamos a comparar lo que puedes hacer.»
- 125.21 s · «gta» en «En GTA 5, el nivel de búsqueda máximo era de cinco estrellas, y cuando la policía te perdía de vista, las estrellas parpadeaban mientras te buscaban, hasta apagarse.»
- 541.28 s · «seis» en «Resultado: tres asaltos para GTA 6, dos para GTA 5 y tres empates.»

## Bloques de ~20 s

| Desde | Hasta | Palabras | Errores Parakeet | Errores Whisper | Errores (mejor) | Detalle |
|---|---|---|---|---|---|---|
| 0.35 | 18.85 | 51 | 0 | 4 | 0 |  |
| 19.21 | 39.07 | 63 | 1 | 3 | 1 | sustitución: «versiones» → «version / reacciones» |
| 39.0 | 57.15 | 50 | 0 | 3 | 0 |  |
| 58.5 | 78.55 | 51 | 1 | 4 | 0 |  |
| 78.56 | 91.44 | 30 | 0 | 0 | 0 |  |
| 91.43 | 108.8 | 57 | 0 | 4 | 0 |  |
| 108.23 | 125.33 | 39 | 0 | 1 | 0 |  |
| 125.01 | 144.94 | 56 | 0 | 1 | 0 |  |
| 144.94 | 161.34 | 51 | 1 | 1 | 0 |  |
| 161.12 | 179.92 | 51 | 0 | 0 | 0 |  |
| 179.84 | 200.3 | 53 | 0 | 0 | 0 |  |
| 200.16 | 210.63 | 32 | 1 | 0 | 0 |  |
| 210.48 | 229.85 | 60 | 0 | 0 | 0 |  |
| 229.82 | 246.48 | 50 | 0 | 0 | 0 |  |
| 246.42 | 266.12 | 51 | 1 | 2 | 0 |  |
| 267.38 | 281.2 | 43 | 0 | 0 | 0 |  |
| 281.06 | 294.25 | 41 | 2 | 2 | 0 |  |
| 294.21 | 313.36 | 54 | 4 | 1 | 0 |  |
| 313.11 | 331.98 | 54 | 0 | 0 | 0 |  |
| 331.87 | 346.84 | 47 | 0 | 0 | 0 |  |
| 346.58 | 359.49 | 33 | 0 | 1 | 0 |  |
| 359.34 | 375.16 | 27 | 2 | 1 | 0 |  |
| 375.22 | 394.0 | 57 | 1 | 1 | 0 |  |
| 393.85 | 412.38 | 55 | 0 | 0 | 0 |  |
| 412.18 | 429.14 | 45 | 0 | 1 | 0 |  |
| 429.27 | 446.85 | 44 | 1 | 0 | 0 |  |
| 446.83 | 462.4 | 45 | 0 | 4 | 0 |  |
| 462.37 | 479.84 | 46 | 1 | 2 | 0 |  |
| 479.81 | 491.4 | 21 | 0 | 3 | 0 |  |
| 491.17 | 509.64 | 46 | 1 | 1 | 0 |  |
| 509.49 | 528.87 | 55 | 0 | 2 | 0 |  |
| 528.55 | 546.42 | 44 | 0 | 2 | 0 |  |
| 545.96 | 564.65 | 60 | 2 | 1 | 0 |  |
| 564.63 | 580.49 | 41 | 0 | 1 | 0 |  |
| 580.35 | 594.42 | 39 | 0 | 0 | 0 |  |
