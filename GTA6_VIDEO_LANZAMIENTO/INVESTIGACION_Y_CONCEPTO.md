# GTA6_VIDEO_LANZAMIENTO: investigación y concepto (versión post lanzamiento)

> **Historial:** la primera versión de este vídeo, «Todo lo que Rockstar ha enseñado antes del lanzamiento», se descartó a petición del canal: hacía falta un vídeo **posterior al lanzamiento** y centrado en la **jugabilidad**. Su guion queda en `engine/videos/gl.py` como borrador sin publicar.

## 1. Estado del lanzamiento (comprobado el 18/11/2026, 19:00-21:00 UTC)

- **Desbloqueo:** GTA VI se desbloquea a medianoche, hora local de cada país. Nueva Zelanda fue la primera, a las 11:00 UTC del 18/11. Después llegaron Australia y Asia.
- **Reseñas:** se publicaron el 18/11, tras jugar la versión final. Metacritic 99, empatado con el récord histórico; OpenCritic 98-99.
- **Primeros análisis técnicos:** Digital Foundry midió Xbox Series X y Series S.
- **Rockstar:** no publicó material nuevo tras el lanzamiento (la página de medios no había cambiado).

## 2. ¿Se puede usar gameplay de streamers?

| Fuente | Disponible | Utilizable | Decisión |
|---|---|---|---|
| Directos y vídeos de streamers (YouTube, Twitch) | Sí, existen | Solo con permiso escrito de cada creador. Además, desde este entorno no se puede acceder a esas plataformas: el control de permisos bloqueó la descarga | **No se usan**. Plantilla para pedir permiso: `00_INFORMES/PLANTILLA_PERMISO_STREAMERS.md` |
| Gameplay con licencia Creative Commons | Sí (19/11/2026): 14 vídeos de YouTube con licencia CC BY (lista: `CLIPS_POSTLANZAMIENTO_CC.md`) | Sí, citando al autor | No se pudieron descargar: YouTube bloquea el servidor y no hay copia en Internet Archive |
| Gameplay posterior al lanzamiento con copia pública en Internet Archive (IGN y otros 4 creadores) | Sí | Sin licencia: cita breve con crédito y sin monetizar, por decisión del canal | **Base visual de la versión 2** |
| Filtraciones | — | No | Descartado |
| Gameplay oficial de Rockstar (Extended Look, 26 min de juego real) | Sí | Sí, sin fines comerciales y con comentario | Base visual de la versión 1; **no se usa en la versión 2** |
| Reseñas y crónicas del lanzamiento | Sí | Sí, como cita breve atribuida | **Base del guion** |

## 3. Concepto elegido

**«GTA 6 ya se juega: qué dicen de su jugabilidad quienes ya lo han jugado».**
- **Guion:** solo información posterior al lanzamiento. Lo dicen las reseñas (escritas tras jugar la versión final), la medición técnica y los primeros jugadores.
- **Imagen:** cada afirmación se ilustra con juego real del mismo tema. Por ejemplo, «GameSpot dice que los atracos son la joya» va sobre el atraco del Extended Look, con aviso de spoiler.

**Estructura:**
1. El veredicto: 99 en Metacritic y las frases de los medios.
2. Los primeros jugadores en Nueva Zelanda y el «truco de Nueva Zelanda».
3. El mundo y la gente de Leonida.
4. Qué hacer: las actividades que citan las reseñas.
5. Los atracos, con aviso de spoiler y el minuto para saltarlo.
6. La conducción y la policía.
7. El combate, la crítica más repetida.
8. El realismo del día a día.
9. El rendimiento: 30 fps sin modo a 60, y las medidas de Digital Foundry en Xbox y PlayStation.
10. La historia, sin spoilers.
11. El lanzamiento: mensaje de Sam Houser y bolsa.
12. Las primeras horas: récord de audiencia en directo y primeras quejas de jugadores (sin confirmar). Añadido el 19/11, tras el desbloqueo en Europa.
13. ¿Merece la pena?, con nuestra lectura en amarillo.

**Por qué funciona:**
- Responde a lo que más se busca el día del lanzamiento: «¿es bueno?», «¿cómo se juega?», «¿va a 60 fps?».
- Tiene datos verificables y frases citables.
- Incluye pegas reales (combate, 30 fps, arranque lento): da credibilidad.

## 4. Spoilers

- **Título y miniatura:** sin spoilers. La miniatura usa la captura oficial de Jason y Lucía huyendo en moto, con «¿Cómo se juega? · 99 Metacritic · Lo bueno y lo malo». No promete «sin spoilers» porque el capítulo 4 tiene escenas de misiones, con aviso.
- **Escenas de misiones:**
  - solo en el capítulo de los atracos;
  - antes, un cartel de aviso con el minuto para saltarlas;
  - durante, un rótulo rojo permanente de «SPOILER».
- **Historia:** solo lo que dicen las reseñas de forma general (arranque lento, historia de amor). Nada de tramas, giros ni finales.
- **Excluidos de las misiones:** rehenes, sangre, cuerpos y diálogos de trama (`recursos/tramos_excluidos.txt`).

## 5. Versión 2 (19/11/2026): gameplay posterior al lanzamiento

Petición del canal: mantener el guion y la estructura, pero **cambiar las imágenes por gameplay del juego ya lanzado**, sin planos del Extended Look ni de los tráileres.

- **De dónde sale el gameplay.** YouTube bloquea las descargas desde el servidor de producción («Sign in to confirm you're not a bot»), y no se esquivó. Pero muchos vídeos publicados tras el lanzamiento tienen una **copia pública en Internet Archive**, que sí permite descargarlos. Se usan 10:
  - IGN: análisis en vídeo, primera misión en PS5 Pro, misiones en Xbox Series S y X, comparativa PS5 Pro frente a Series S y buceo;
  - Lootward (persecución de seis estrellas), Sirloin1 (base militar y mapa), Swiss001 (aeropuerto y mapa) y RedArcade (momentos de directos).
- **Derechos.** No tienen licencia Creative Commons: se usan como cita breve, con el autor en pantalla en cada plano, enlaces en la descripción y el vídeo sin monetizar (`REGISTRO_DE_PERMISOS.txt`). Los 14 vídeos CC BY de `CLIPS_POSTLANZAMIENTO_CC.md` no tienen copia en el Archive.
- **Imagen ajustada a cada opinión.** Las frases de IGN van sobre el análisis de IGN, el rendimiento sobre IGN en Series X, Series S y PS5 Pro, la policía sobre la persecución de seis estrellas, las «físicas raras» sobre clips de directos, el buceo sobre el buceo, etc.
- **Spoilers (capítulo 4).** Se usan misiones que **no salen en ningún tráiler ni en el Extended Look** (comprobado revisando el Extended Look entero, con un fotograma cada 8 s):
  - el asalto a un banco del análisis de IGN;
  - la primera misión, «Just Like Paradise»: lancha, prismáticos, infiltración, tiroteo y huida en hidroavión;
  - el cobro del alquiler de Brian y el robo de un coche del depósito de la policía.
- **Revisión plano a plano.** Se descartaron los fragmentos de otros juegos que IGN intercala en su análisis (Red Dead Redemption 2, GTA IV, GTA V, Cyberpunk 2077 y GTA: San Andreas), la cámara de los creadores, y los planos con cuerpos, sangre o desnudos.
- **Lanzamiento mundial.** La narración dice que el juego ya se ha lanzado en todo el mundo.
- **Mapa.** El mapa oficial imprimible que anunció Rockstar aún no estaba publicado a las 10:45 UTC del 19/11. El vídeo enseña el **mapa del propio juego** (menú de pausa) en partidas de IGN y Swiss001.
- **Material oficial que queda.** Algunas capturas, ilustraciones y vídeos de personaje, sobre todo en el capítulo de la historia, para no hacer spoilers, y en las actividades sin gameplay disponible (golf, caza, aves).
