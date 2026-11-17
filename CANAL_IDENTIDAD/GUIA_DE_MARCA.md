# Identidad del canal

## 1. Cinco nombres posibles
| Nombre | Idea | Pros | Contras |
|---|---|---|---|
| **Caimán Neón** ✅ | El animal emblema de Florida/Leonida y la estética nocturna de Vice City | Mascota reconocible, funciona en miniaturas pequeñas, no depende de marcas de Rockstar y sirve para otros mundos abiertos | "Caimán" no es la especie exacta (es aligátor), algo que convertimos en guiño (V08) |
| Brújula Neón | Exploración y guías | Promete orientación | Más genérico; no tiene una mascota clara |
| Medianoche Tropical | Lanzamiento a medianoche y trópico | Evocador | Largo y difícil de recordar como @usuario |
| Ruta Seis | Carretera + "VI" | Corto | Demasiado ligado a GTA VI; envejece mal y recuerda a canales de noticias |
| Expediente Sur | Investigación | Encaja con el tono riguroso | Frío; no transmite entretenimiento |

**Elegido: Caimán Neón.**
- Es corto (2 palabras, 11 letras) y se pronuncia igual en toda Hispanoamérica.
- Tiene una **mascota dibujable**: el caimán de tubo de neón, que funciona como logotipo, sello de lacre, marca de agua y sintonía.
- **No usa marcas de Rockstar** ("GTA", "Vice City", "Leonida"), así que puede crecer más allá de GTA VI sin cambiar de nombre.
- Antes de crear el canal, **comprueba si están libres el @usuario `@caimanneon` y los perfiles en redes**. No se pudo verificar desde este entorno.

## 2. Descripción del canal ("Acerca de")
> **Caimán Neón: GTA VI en español, sin humo.**
> Guías, mapas, análisis y misterios de Grand Theft Auto VI para Latinoamérica y España. Nuestra regla: cada dato lleva su etiqueta.
> 🟢 OFICIAL: lo confirmó Rockstar, Take-Two o la tienda.
> 🟡 DEDUCCIÓN: lo inferimos nosotros o la comunidad, y lo decimos.
> 🩷 RUMOR: nadie lo ha confirmado.
> Sin filtraciones, sin imágenes falsas y sin "descargas gratis". Animaciones y música originales.
> Nuevos videos martes, jueves y sábados, y Shorts casi a diario.
> *Canal independiente, sin relación con Rockstar Games ni Take-Two Interactive.*

## 3. Logotipo y recursos (esta carpeta)
| Archivo | Uso |
|---|---|
| `logo_horizontal_transparente.png` (2600×640) | Cabeceras, documentos, colaboraciones |
| `logo_horizontal_fondo.png` | Redes sociales y presentaciones |
| `avatar_800x800.png` | Foto de perfil de YouTube (se ve circular). Solo el caimán, legible a 98 px |
| `banner_2560x1440.png` | Banner de YouTube. Logo, eslogan y semáforo dentro de la zona segura de 1546×423 |
| `marca_de_agua_150x150.png` | Marca de agua de YouTube (Studio → Personalización → Imagen de marca) |
| `paleta.png`, `tipografia.png` | Referencia visual |

El logotipo es un **caimán de perfil dibujado como tubo de neón** (verde Caimán) con el **ojo en rosa Flamenco** y pupila rasgada. Lleva el wordmark "CAIMÁN" en hueso y "NEÓN" en verde con brillo. Es dibujo vectorial original: el código está en `engine/brand.py`.

## 4. Paleta
| Nombre | Hex | Uso |
|---|---|---|
| Noche | `#0B0F1E` | Fondos de marca |
| Pantano | `#10302A` | Degradados y profundidad |
| **Caimán** | `#2BFF88` | Color principal; etiqueta **OFICIAL** |
| **Sol** | `#FFC83D` | Acentos; etiqueta **DEDUCCIÓN** |
| **Flamenco** | `#FF4FA0` | Acentos; etiqueta **RUMOR** |
| Laguna | `#27D7F2` | Información secundaria, fuentes |
| Hueso | `#F3EFE4` | Texto sobre oscuro |

La paleta evita a propósito el degradado rosa-naranja-violeta de la identidad de GTA VI. Nuestro verde neón es el diferenciador.

## 5. Tipografía (todas OFL o Apache 2.0, aptas para uso comercial)
- **Anton:** titulares y miniaturas.
- **Inter:** texto y subtítulos.
- **JetBrains Mono:** datos, etiquetas y fuentes.
- **Cada formato tiene su tipografía de acento:**
  - Barlow Condensed: kit de lanzamiento.
  - Bebas Neue: Shorts informativos.
  - Share Tech Mono: investigación.
  - DM Serif Display: mapas.
  - Special Elite: expedientes.
  - Bungee: Shorts de juego.
  - Abril Fatface + Caveat: guía de campo.
  - Syne: misterios.

## 6. Sistema de miniaturas
1. **Un solo punto focal** que se entienda a 160 px de ancho (en el móvil).
2. **Máximo 4 palabras grandes.** El resto del texto, pequeño o ninguno.
3. **Composición distinta por formato**, no una plantilla única:
   - Reloj de paletas (V01).
   - Globo (V02).
   - Botón trampa (V03).
   - Mapa 3D (V04).
   - Expediente (V05).
   - Pantalla dividida (V06).
   - Tanques (V07).
   - Lámina naturalista (V08).
   - Sobres (V09/V10).
4. **Constante de marca:** el verde Caimán o el caimán aparece en algún lugar. Siempre alto contraste.
5. **Prohibido:**
   - Logotipos o arte de Rockstar.
   - Capturas falsas o imágenes de IA que imiten el juego.
   - Flechas o reacciones engañosas.
   - Prometer en la miniatura algo que el vídeo no muestra.
6. **Formato:** PNG de 1280×720. Cada vídeo trae la suya en `VIDEO_XX/miniatura.png`.

## 7. Personalidad de la narración
- **El Narrador (voz principal):**
  - Cercano, directo y con humor seco ("prepárate para ser el narrador oficial de la sala").
  - Tutea, usa frases cortas y verbos activos. Nunca grita ni exagera ("BRUTAL", "INCREÍBLE").
  - Dice en voz alta cuando algo es deducción.
  - Español latinoamericano neutro: "video", "computadora" o "PC", "ustedes".
- **La Analista (segunda voz):**
  - Calmada y precisa. Aparece en los formatos de investigación (V03), expediente (V05) y guía de campo (V08).
- **Tono de marca:** "el amigo que sabe y no te vende humo". El rigor es la diferencia frente a los canales de rumores.
- **Identidad sonora:**
  - Sintonía de 3 notas en campana FM más una "mordida" de caimán (cortinilla de 2,4 s).
  - Cada formato tiene su propio estilo musical original.

## 8. Fórmulas recurrentes que construyen marca
- El **semáforo de certeza** en pantalla y en voz.
- **Fuentes visibles** en pantalla (chip "FUENTE · …").
- **Marcador de aciertos y fallos**: el canal vuelve a sus deducciones y rinde cuentas (V09 → V10). Es lo que hace que la audiencia vuelva.
