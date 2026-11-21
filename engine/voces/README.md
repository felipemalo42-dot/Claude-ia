# Voces de referencia

El modelo de voz (**Chatterbox Multilingual** de Resemble AI, licencia MIT) genera la narración imitando el timbre de un audio de referencia de unos 10–15 segundos. Estos son los archivos de referencia que usa el canal:

| Archivo | Rol | Origen | Licencia |
|---|---|---|---|
| `narradora_ref.wav` | Narradora (voz principal) | Grabaciones de una locutora voluntaria del corpus **"Crowdsourced high-quality Colombian Spanish speech data set"** (Google, OpenSLR SLR72, archivos `cof_03034_*`), creado específicamente para construir sistemas de síntesis de voz | **CC BY-SA 4.0**. Atribución: *Guevara-Rukoz et al., "Crowdsourcing Latin American Spanish for Low-Resource Text-to-Speech", LREC 2020*. Este archivo derivado se comparte bajo la misma licencia. |
| `copiloto_ref.wav` | Copiloto (preguntas en el video 03) | Generado con la voz sintética M1 de Supertonic 3. No pertenece a ninguna persona real | OpenRAIL-M (pesos del modelo) |

## Uso responsable
- La locutora del corpus es anónima. El conjunto de datos se publicó, con su consentimiento, para que cualquiera construyera voces sintéticas, incluso con fines comerciales, bajo CC BY-SA 4.0. **No se imita a ninguna persona conocida.**
- Chatterbox incrusta en todo lo que genera una **marca de agua inaudible (Perth)** que identifica el audio como sintético.
- Si cambias de voz, conserva aquí la fuente y la licencia de la nueva referencia. Nunca uses grabaciones de personas reales sin su permiso expreso.

## Cambiar de voz
1. Sustituye `narradora_ref.wav` por otra referencia: unos 12 s de voz limpia, sin música y a 24 kHz.
2. Ejecuta `python build.py vXX` para cada video. Las tomas se guardan en caché según texto, voz y semilla, así que solo se regenera lo que cambia.
