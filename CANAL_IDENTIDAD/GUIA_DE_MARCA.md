# Identidad del canal: SAL Y ASFALTO

> **Cambio de marca (17/11/2026):** el nombre anterior, *Caimán Neón*, se descartó porque **ya existe un canal de YouTube con ese nombre** (@CaimánNeón), que además publica contenido de GTA 6 con estética neón rosa y violeta. Para no confundir a la audiencia ni competir con su marca, se rediseñó todo: nombre, emblema, paleta, tipografía, cortinilla, pantalla final, rótulos, sintonía y sistema de miniaturas.

## 1. Cinco nombres candidatos
| Nombre | Idea | ¿Hay un canal de YouTube con ese nombre? |
|---|---|---|
| **Sal y Asfalto** ✅ | El mar (sal) y la calle (asfalto): la costa de Leonida y su vida criminal sobre ruedas | No se encontró en búsqueda web |
| Faro Sur | Una luz que guía entre tanto rumor | No se encontró en búsqueda web |
| Bitácora Sur | Diario de exploración con método | No se encontró en búsqueda web |
| Palmera Rota | Huracanes, trópico y caos | No se encontró en búsqueda web |
| Cuadrante Sur | Mapas y cuadrículas | No se encontró en búsqueda web |

> ⚠️ **Antes de crear el canal**, búscalo en YouTube y comprueba que estén libres el @usuario **`@SalYAsfalto`** y el nombre en Instagram y TikTok. Esa comprobación no se puede hacer desde este entorno: YouTube está bloqueado.

**Por qué Sal y Asfalto:**
- **Evoca Leonida sin usar marcas de Rockstar.** Mar, carreteras costeras y autos son el corazón de GTA VI, inspirado en Florida.
- **Tiene una imagen propia:** una carretera que cruza el mar hacia el sol, como las autopistas que unen islas. Funciona igual de bien en 98 px (avatar) que en un banner.
- **Sobrevive a GTA VI.** Sirve para cualquier juego de mundo abierto, de conducción o de crimen.
- **El semáforo de certeza se vuelve literal:** un canal "de carretera" que separa lo OFICIAL (verde), la DEDUCCIÓN (ámbar) y el RUMOR (rojo).
- **Es lo opuesto a la estética neón** que usan casi todos los canales de GTA 6 en español, así que destaca en la página de resultados.

## 2. Descripción del canal ("Acerca de")
> **Sal y Asfalto: GTA VI en español, sin humo.**
> Guías, mapas, análisis y misterios de Grand Theft Auto VI para Latinoamérica y España. Aquí manda el semáforo:
> 🟢 OFICIAL: lo confirmó Rockstar, Take-Two o la tienda.
> 🟡 DEDUCCIÓN: lo inferimos nosotros o la comunidad, y lo decimos.
> 🔴 RUMOR: nadie lo ha confirmado.
> Sin filtraciones, sin imágenes falsas y sin "descargas gratis". Animaciones y música originales.
> Nuevos videos martes, jueves y sábados, y Shorts casi a diario.
> *Canal independiente, sin relación con Rockstar Games ni Take-Two Interactive.*

## 3. Logotipo y recursos (esta carpeta)
| Archivo | Uso |
|---|---|
| `avatar_800x800.png` | Foto de perfil: el emblema (carretera sobre el mar, sol amarillo y línea de carril) |
| `banner_2560x1440.png` | Banner: carretera costera al atardecer y señal de autopista con el nombre, dentro de la zona segura de 1546×423 |
| `logo_horizontal_transparente.png` / `logo_horizontal_fondo.png` | Emblema + wordmark (2600×640) |
| `marca_de_agua_150x150.png` | Marca de agua de YouTube |
| `paleta.png`, `tipografia.png` | Referencias visuales |

**El emblema:** un círculo con borde blanco sal. Arriba, cielo claro con medio sol amarillo en el horizonte. Abajo, mar turquesa con olas y una carretera de asfalto en perspectiva que cruza el mar hasta el sol, con línea central amarilla discontinua.
**El wordmark:** "SAL Y ASFALTO" en Overpass Black. La "Y" va en amarillo de carril.
Todo es dibujo vectorial original (`engine/brand.py`).

## 4. Paleta
| Nombre | Hex | Uso |
|---|---|---|
| Asfalto | `#16181B` | Fondos de marca |
| Asfalto 2 | `#25282D` | Carretera, paneles |
| Sal | `#F3F0E9` | Texto, bordes de señal |
| **Amarillo carril** | `#FFC72C` | Color principal de acento (la "Y", llamadas a la acción) |
| Mar | `#13A8A0` → `#0B5E63` | Secundario, etiqueta REPORTADO |
| Señal | `#0B6B45` | Paneles tipo señal de autopista |
| Verde / Ámbar / Rojo | `#22C55E` / `#FFB000` / `#FF4A3D` | Semáforo de certeza: OFICIAL / DEDUCCIÓN / RUMOR |

**Se evitan** el neón rosa y violeta y el degradado rosa-naranja-violeta propio de GTA VI.

## 5. Tipografía (todas con licencia OFL o Apache 2.0)
- **Overpass Black / ExtraBold:** titulares, miniaturas y wordmark. Es una tipografía libre derivada del lenguaje de la señalización vial.
- **Overpass Mono:** datos, etiquetas y fuentes.
- **Inter:** texto largo.
- Cada formato conserva su tipografía de acento para diferenciar los videos entre sí: Barlow Condensed, Bebas Neue, Share Tech Mono, DM Serif Display, Special Elite, Bungee, Abril Fatface + Caveat, Syne.

## 6. Elementos animados de marca
- **Cortinilla (2,4 s):** viaje por la carretera costera hacia el sol. La imagen se cierra en el emblema y aparece la señal verde "SAL Y ASFALTO".
- **Sintonía:** un auto que pasa (efecto Doppler, de izquierda a derecha), una ola y un acorde de piano eléctrico. Sintetizada por código: es original.
- **Etiquetas de certeza:** semáforo en miniatura + rótulo en Overpass Mono.
- **Fuentes en pantalla:** chip negro con barra amarilla ("FUENTE · …").
- **Pantalla final:** escena costera con una señal "SIGUIENTE SALIDA", dos marcos "SALIDA 1 / SALIDA 2" para los elementos de YouTube, y el emblema con "SUSCRÍBETE".
- **Marca de agua:** el emblema, abajo a la derecha.

## 7. Sistema de miniaturas
1. **Un solo punto focal** y **un máximo de 4 palabras grandes** en Overpass Black. Sin brillos neón.
2. **Panel de señal vial** (verde con borde blanco) para el dato clave cuando ayuda: "00:00 LOCAL", "Y SUS LUGARES REALES", "10 CAMBIOS CONFIRMADOS".
3. **El emblema siempre aparece** en una esquina. Es la constante de marca.
4. **Composición distinta por formato**, no una plantilla única.
5. **Prohibido:**
   - Logotipos, arte o personajes de Rockstar.
   - Capturas falsas o imágenes de IA que imiten el juego.
   - Prometer en la miniatura algo que el video no muestra.
6. **Formato:** PNG de 1280×720 (`VIDEO_XX/miniatura.png`).

## 8. Personalidad de la narración
- **El Narrador:**
  - "El copiloto que conoce la ruta": cercano, directo y con humor seco.
  - Tutea, usa frases cortas y no exagera.
  - Dice en voz alta cuándo algo es deducción.
  - Español latinoamericano neutro.
- **La Analista:** calmada y precisa. Aparece en investigación (V03), expediente (V05) y guía de campo (V08).
- **Fórmula de presentación:** "Esto es Sal y Asfalto, y aquí manda el semáforo…"
- **Fórmulas recurrentes:**
  - Fuentes visibles en pantalla.
  - Semáforo de certeza.
  - Marcador de aciertos y fallos: el canal vuelve a sus deducciones y rinde cuentas (V09 → V10).
