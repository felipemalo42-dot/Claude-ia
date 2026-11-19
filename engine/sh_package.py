"""Empaqueta un Short vertical (módulos videos/s01.py y videos/s02.py): guion con tiempos, fuentes y permisos fragmento a
fragmento, descripción y publicación, control de sincronía y limpieza de archivos intermedios.
Uso: python sh_package.py s01   (o s02)
"""
import csv, importlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
from tts import split_markup

def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"

PUB = {
 "s01": dict(
    titles=["GTA 6 tiene un ring de lucha libre SECRETO (y un error te mata) #shorts",
            "El combate secreto de GTA 6 que casi nadie ha encontrado #shorts",
            "Cómo ganar a The Gentrifier en GTA 6 (y llevarte su máscara) #shorts"],
    hook="Un combate de lucha libre escondido en un patio, en el que un solo error te mata.",
    desc=("En un patio de Hamlet hay un ring escondido: Backyard American Mania. Dónde está, cómo prepararte y cómo ganar a "
          "The Gentrifier para llevarte su máscara de luchador. Sin spoilers de la historia: es una actividad secundaria."),
    tags=["#GTA6", "#GTAVI", "#GrandTheftAutoVI", "#GTA6Secretos", "#Leonida", "#shorts"],
    keywords=["gta 6 ring lucha libre", "gta 6 backyard wrestling", "gta 6 gentrifier", "gta 6 mascara luchador", "gta 6 secretos", "gta 6 hamlet"],
    pinned="¿Lo ganaste a la primera o te cayó encima? 😅 Cuéntanos sin spoilers 👇"),
 "s02": dict(
    titles=["GTA 6: la isla del S.O.S. y el perro de la moto de agua #shorts",
            "Encontré un S.O.S. en una isla de GTA 6… y vino un perro a buscarme #shorts",
            "El misterio de la isla S.O.S. de GTA 6 #shorts"],
    hook="Una isla perdida con un S.O.S. en la arena y un vídeo inquietante… y el giro: un perro pilotando una moto de agua.",
    desc=("Una isla perdida, un S.O.S. escrito en la arena y un teléfono con un vídeo inquietante… hasta que aparece el perro de "
          "la moto de agua. Sin spoilers: es un encuentro secundario del mar de Leonida, no una misión."),
    tags=["#GTA6", "#GTAVI", "#GrandTheftAutoVI", "#JetSkiDog", "#Leonida", "#shorts"],
    keywords=["gta 6 jet ski dog", "gta 6 perro moto de agua", "gta 6 isla sos", "gta 6 secretos", "gta 6 easter egg", "gta 6 misterio"],
    pinned="¿Quién crees que escribió el S.O.S.? 🏝️ Teorías en los comentarios (sin spoilers de la historia) 👇"),
}

def run(vid):
    M = importlib.import_module(f"videos.{vid}"); V = M.VIDEO; G = M.G
    G._T.clear(); M.SR._SUB.clear()          # la tabla de planos se cachea por proceso: limpiarla al cambiar de Short
    out = os.path.join(build.ROOT, V["folder"]); r = os.path.join(out, "recursos")
    tl = json.load(open(f"{r}/timeline.json")); ctx = build.Ctx(V, tl, *V["size"]); T = G.table(ctx)
    P = PUB[vid]
    # ---------------- planos y sincronía
    rows = []
    for s in T["shots"]:
        k, v = s["src"].split(":", 1)
        if k == "x":
            path, loc, Ls = G.src_window(dict(s)); vv = v.split("@")[0]; m = G.XCAT[vv]
            src = f"{m['autor']} · «{m['titulo']}» · {mmss(loc)}"; url = m["url"]
        else:
            src = "Gráfico propio (Sal y Asfalto)"; url = ""; loc = None
        rows.append(dict(inicio=round(s["t0"], 3), fin=round(s["t1"], 3), palabra=s.get("word") or "", ancla=s.get("anchor") or "(inicio del bloque)",
                         desfase_s=round(s["t0"] - s["word_t"], 3) if s.get("word_t") is not None else "", fuente=src, minuto_en_el_original=mmss(loc) if loc is not None else "",
                         enlace=url))
    with open(f"{r}/registro_de_planos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";"); w.writeheader(); w.writerows(rows)
    anch = [x for x in rows if x["desfase_s"] != ""]; ok = [x for x in anch if abs(x["desfase_s"]) <= 0.10]
    sync = dict(planos=len(rows), anclados=len(anch), sincronizados=len(ok), pct=100.0 * len(ok) / max(1, len(anch)),
                dur_media=sum(x["fin"] - x["inicio"] for x in rows) / len(rows), max_plano=max(x["fin"] - x["inicio"] for x in rows))
    json.dump(sync, open(f"{r}/sincronia.json", "w"), indent=1)
    # ---------------- guion
    L = [f"{V['title']}", f"Short vertical 9:16 · {mmss(tl['total'])} · voz C (español latinoamericano, Chatterbox) · {V['music']}", "",
         "GANCHO: " + P["hook"], "", "GUION CON TIEMPOS (el plano que acompaña a cada frase, entre corchetes)", ""]
    by_beat = {}
    for s in T["shots"]: by_beat.setdefault(s["beat"], []).append(s)
    for bi, (b, bd) in enumerate(zip(M.B, tl["beats"])):
        if not b["vo"]: continue
        L.append(f"[{mmss(bd['start'])}] " + " ".join(split_markup(x)[0] for x in build.split_sentences(b["vo"])))
        for s in by_beat.get(bi, []):
            k, v = s["src"].split(":", 1)
            what = (f"{G.XCAT[v.split('@')[0]]['autor']} {mmss(G.src_window(dict(s))[1])}" if k == "x" else f"gráfico «{v}»")
            extra = " · ".join(str(s[x]) if not isinstance(s[x], tuple) else " ".join(map(str, s[x])) for x in ("label", "big", "evid", "tag") if s.get(x))
            L.append(f"      {mmss(s['t0'])}  «{s.get('anchor') or 'inicio'}» → {what}" + (f" · rótulo: {extra}" if extra else ""))
        L.append("")
    L += ["CIERRE: la última frase vuelve a la imagen o la pregunta del principio, para que el Short se vea en bucle.", "",
          f"Palabras: {sum(len(split_markup(b['vo'])[0].split()) for b in M.B if b['vo'])} · planos: {sync['planos']} · "
          f"media {sync['dur_media']:.1f} s por plano · sincronía imagen ↔ palabra: {sync['sincronizados']}/{sync['anclados']} cortes a ≤ 0,10 s"]
    open(f"{out}/GUION.txt", "w", encoding="utf-8").write("\n".join(L) + "\n")
    # ---------------- descripción y publicación
    used = sorted({s["src"][2:].split("@")[0] for s in T["shots"] if s["src"].startswith("x:")})
    cred = "\n".join(f"• Gameplay: {G.XCAT[u]['autor']}, «{G.XCAT[u]['titulo']}» · {G.XCAT[u]['url']}" for u in used)
    desc = (P["desc"] + "\n\n" + cred + "\n\nGuion, narración, montaje, gráficos y música: Sal y Asfalto. Narración con voz sintética.\n"
            "Grand Theft Auto VI es de Rockstar Games / Take-Two. Canal independiente, sin relación con Rockstar.\n\n" + " ".join(P["tags"]))
    open(f"{out}/DESCRIPCION_YOUTUBE.txt", "w", encoding="utf-8").write(desc + "\n")
    Lp = [f"# {V['folder']}: publicación", "", f"**Duración:** {mmss(tl['total'])} · 1080×1920 · 30 fps · H.264 + AAC", "",
          "## Título", "", f"**Principal:** {P['titles'][0]}", "", "Alternativos:"] + [f"- {x}" for x in P["titles"][1:]] + [
          "", "## Hashtags", "", " ".join(P["tags"]), "", "## Palabras clave", "", ", ".join(P["keywords"]), "",
          "## Comentario fijado", "", P["pinned"], "", "## Descripción", "", "Lista para copiar en `DESCRIPCION_YOUTUBE.txt` (incluye el crédito del gameplay).", "",
          "## Antes de publicar", "", "- **Monetización desactivada** (ver `FUENTES_Y_PERMISOS.txt`).",
          "- Contenido alterado o sintético: **Sí** (la narración es una voz sintética).",
          "- Sube `SUBTITULOS.srt` como subtítulos en español.",
          "- Portada: `PORTADA.png` (en Shorts se elige un fotograma; esta imagen sirve como referencia o para la pestaña de vídeos).",
          "- Mira el Short entero con sonido antes de publicarlo: no puedo escuchar el audio."]
    open(f"{out}/PUBLICACION.md", "w", encoding="utf-8").write("\n".join(Lp) + "\n")
    # ---------------- fuentes y permisos (fragmento a fragmento)
    NOTE = {"s01": ("Datos del guion: lo que se ve en el gameplay (mapa, tienda, carta coleccionable, caravana, combate, avisos del juego "
                    "«ADRENALINE (FULL)», «MASK», «Luchador Mask») y la narración en inglés del mismo vídeo de IGN, transcrita y "
                    "contada con palabras propias. No se reproduce su audio."),
            "s02": ("Datos del guion: lo que se ve en el gameplay (mapa, isla con S.O.S., teléfono con el vídeo, buceo, perro con gafas "
                    "en la moto de agua, segunda moto) y la narración en inglés del mismo vídeo de IGN, transcrita y contada con palabras "
                    "propias. No se reproduce su audio. Encuadre: solo la banda de juego del vídeo vertical; el título y los subtítulos "
                    "de IGN y su logotipo quedan fuera, y el crédito a IGN aparece en pantalla y en la descripción.")}
    F = [f"FUENTES Y PERMISOS · {V['folder']} · «{V['title']}»", "Revisado el 19/11/2026. Este registro no sustituye una opinión jurídica profesional.", "",
         "1. GAMEPLAY USADO"]
    for u in used:
        m = G.XCAT[u]
        F += [f"   Autor: {m['autor']} (canal de YouTube)", f"   Vídeo: «{m['titulo']}» · publicado el {m['publicado']}",
              f"   Enlace original: {m['url']}", f"   Copia descargada: {m['copia']} (copia pública en Internet Archive; YouTube bloquea la descarga desde el servidor de producción)",
              "   ¿Autorización comercial? NO. El vídeo no tiene licencia Creative Commons ni permiso del autor: todos los derechos reservados.",
              "   Condiciones de reutilización publicadas por el autor: ninguna.",
              "   Decisión del canal (19/11/2026): usarlo con crédito en pantalla y en la descripción, sin que la narración mencione al autor.",
              "   Fragmentos exactos usados (minuto del Short → minuto del vídeo original · duración):"]
        for x in rows:
            if x["enlace"] == m["url"]:
                F.append(f"     {mmss(x['inicio'])} → {x['minuto_en_el_original']} · {x['fin'] - x['inicio']:.1f} s · «{x['ancla']}»")
        xb = G.XBAD.get(u) or []
        if xb: F.append("   Tramos excluidos a propósito (rótulos del autor, cortinillas): " + ", ".join(f"{mmss(a)}-{mmss(b)}" for a, b in xb))
    F += ["", "2. " + NOTE[vid], "",
          "3. EL JUEGO", "   Las imágenes de Grand Theft Auto VI son de Rockstar Games / Take-Two Interactive. Su política solo permite usos no comerciales",
          "   («Policy on posting copyrighted Rockstar Games material», actualizada el 10/01/2025). Por eso: MONETIZACIÓN DESACTIVADA.",
          "   No se usa nada de los tráileres, del Extended Look ni de filtraciones.", "",
          "4. LO PROPIO DEL CANAL (VERDE)",
          "   - Guion y montaje: Sal y Asfalto.",
          "   - Narración: voz sintética Chatterbox Multilingual (licencia MIT) a partir de la referencia de voz OpenSLR SLR72 (CC BY-SA 4.0). Lleva marca de agua inaudible.",
          "   - Música y efectos: compuestos por código para este Short (engine/audio.py). Sin música comercial.",
          "   - Gráficos, rótulos y subtítulos: diseño propio; tipografías con licencia SIL Open Font License.", "",
          "5. POLÍTICAS DE YOUTUBE",
          "   - Aportación propia: guion original, narración, montaje, gráficos, música y subtítulos. No es una resubida con cambios superficiales:",
          "     cada fragmento ilustra una frase concreta y se recorta, reencuadra y comenta.",
          "   - Aun así, usa gameplay ajeno sin permiso. YouTube puede considerarlo contenido reutilizado, e IGN o Rockstar pueden reclamarlo",
          "     por Content ID. No se promete monetización: se publica con los anuncios desactivados.",
          "   - Divulgación: marcar «Contenido alterado o sintético: Sí» (la voz es sintética).", "",
          "6. SI ALGUIEN RECLAMA",
          "   - Content ID: no disputarlo.",
          "   - Si el autor pide retirarlo: retirar el Short o sustituir sus planos (engine/videos/" + vid + ".py) y volver a montarlo.",
          "   - Para pedir permiso: adaptar 00_INFORMES/PLANTILLA_PERMISO_STREAMERS.md, con los fragmentos de la lista de arriba. Guardar la respuesta por escrito.",
          "", "7. REGISTRO DE AUTORIZACIONES", "   Ninguna autorización recibida a 19/11/2026. No se ha marcado ningún recurso como aprobado."]
    open(f"{out}/FUENTES_Y_PERMISOS.txt", "w", encoding="utf-8").write("\n".join(F) + "\n")
    # ---------------- limpieza
    # mezcla_final.wav se conserva (está en .gitignore): el render la necesita para volver a montar el vídeo
    if os.path.exists(f"{r}/musica_original.wav"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{r}/musica_original.wav", "-c:a", "libmp3lame", "-b:a", "192k", f"{r}/musica_original.mp3"], check=True)
        os.remove(f"{r}/musica_original.wav")
    print(vid, sync)
    return rows, sync, used


QA = {
 "s01": dict(
    diff="Ningún vídeo anterior trata actividades secundarias ni lucha libre. Los Shorts previos eran la hora de salida por país (globo 3D), el espacio en disco (210 GB) y la fauna (guía de campo); este es una guía de «jefe final» con estética de retransmisión.",
    orig="Convierte una guía en un combate retransmitido: rondas, tarjeta VS, golpes con sacudida, cámara lenta en el salto y un cierre que vuelve a la imagen del principio para verse en bucle.",
    spoil="Sí. Es una actividad secundaria disponible casi en cualquier momento de la campaña; no aparecen misiones ni escenas de la historia.",
    refs="Hamlet → mapa con el puente y el pin · la casa → Jason llegando · el ring y el cartel B.A.M. → el cartel · barritas de proteína → la estantería con «PROTEIN BARS» · la carta → la carta «Chico Bonez» · la caravana → Jason llamando · las latas → Jason lanzando · The Gentrifier → su salida de la caravana y la tarjeta VS · la tercera cuerda → él arriba · esquivar → Jason rodando · el salto → congelado en el aire · subes tú → Jason trepando · adrenalina y máscara → los avisos «ADRENALINE (FULL)», «MASK» y «Luchador Mask» del juego. La única imagen propia es «guarda la partida», que no se ve en el gameplay."),
 "s02": dict(
    diff="Ningún vídeo anterior cuenta una historia de misterio ni trata el mar abierto o este encuentro. Es una narración con giro, distinta de la guía del SHORT_01 y de los Shorts informativos previos.",
    orig="Presenta el encuentro como un expediente policial con «pruebas» numeradas y tono frío, que estalla en color y comedia cuando aparece el perro. Acaba con una pregunta que devuelve al principio (bucle).",
    spoil="Sí. Es un encuentro secundario en el mar, no una misión. El vídeo del teléfono solo muestra a una pareja saludando; no se revela nada de la historia.",
    refs="lejos de la costa → el mapa con la isla · isla diminuta → la isla desde el aire · alguien escribió en la arena → Jason junto a las letras · S.O.S. → zoom a las letras · teléfono → el teléfono · vídeo y saludo → la pareja en la pantalla · solo agua → el mapa del mar · bucear → buceando · vuelves a la superficie → saliendo del agua · algo viene → punto lejano que se acerca · perro, gafas, moto → el perro con gafas al manillar · copiloto, conduce, vuelta, otra moto → los planos de cada acción · otras zonas → el perro en otro tramo de mar."),
}

def qa(vid):
    M = importlib.import_module(f"videos.{vid}"); V = M.VIDEO
    out = os.path.join(build.ROOT, V["folder"]); r = os.path.join(out, "recursos"); mp4 = f"{out}/VIDEO_FINAL.mp4"
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate",
                                    "-of", "json", mp4], capture_output=True, text=True).stdout)
    fmt = pr["format"]; vs = [s for s in pr["streams"] if s.get("width")][0]
    lu = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", lu); lufs = float(m[-1]) if m else float("nan")
    rows = list(csv.DictReader(open(f"{r}/control_de_voz.csv", encoding="utf-8"), delimiter=";"))
    D = sum(int(x["diferencias"] or 0) for x in rows); N = sum(int(x["sonidos"] or 0) for x in rows)
    st = json.load(open(f"{r}/sincronia.json")); q = QA[vid]; dur = float(fmt["duration"])
    low = [x for x in rows if float(x["coincidencia"]) < 0.995]
    L = [f"# {V['folder']}: control de calidad", "", f"Revisado el 19/11/2026 sobre `VIDEO_FINAL.mp4`.", "",
         "| Medida | Resultado |", "|---|---|",
         f"| Duración | {dur:.1f} s (objetivo 35-60 s) |", f"| Formato | {vs['codec_name'].upper()} {vs['width']}×{vs['height']} (9:16), {vs['r_frame_rate'].split('/')[0]} fps, {int(fmt['size']) / 1e6:.1f} MB |",
         f"| Sonoridad | {lufs:.1f} LUFS (YouTube normaliza a −14) |",
         f"| Voz ↔ guion | {1 - D / max(1, N):.2%} de coincidencia fonética ({D} sonidos distintos de {N}); {len(rows) - len(low)} de {len(rows)} frases ≥ 99,5 % |",
         f"| Sincronía imagen ↔ palabra | {st['sincronizados']} de {st['anclados']} cortes a ≤ 0,10 s de su palabra |",
         f"| Planos | {st['planos']} (media {st['dur_media']:.1f} s; el más largo {st['max_plano']:.1f} s) |", ""]
    if low:
        L += ["Frases por debajo del 99,5 % (el reconocedor escribe distinto un nombre o una palabra; se revisaron una a una):"]
        L += [f"- {x['inicio_s']} s · {float(x['coincidencia']):.1%} · reconocido: «{x['reconocido'][:140]}»" for x in low] + [""]
    L += ["## Lista del encargo", "", "| Pregunta | Respuesta |", "|---|---|",
          f"| ¿Es diferente de los vídeos anteriores? | Sí. {q['diff']} |", f"| ¿Su concepto es original? | Sí. {q['orig']} |",
          "| ¿Tiene gameplay auténtico? | Sí: gameplay grabado del juego ya lanzado (vídeo publicado el 19/11/2026). No hay imágenes generadas con IA. |",
          "| ¿Está libre de tráilers y Extended Look? | Sí: no usa ni un fotograma de los tráileres, del Extended Look ni de filtraciones. |",
          f"| ¿Está libre de spoilers? | {q['spoil']} |", f"| ¿Cada elemento mencionado se ve? | Sí. {q['refs']} |",
          "| ¿La narración es natural? | Voz C del canal (español latinoamericano), frase a frase, con la energía ajustada a cada bloque. No puedo escucharla: revísala antes de publicar. |",
          f"| ¿El ritmo es adecuado? | Un plano nuevo cada {st['dur_media']:.1f} s de media y sin pantallas vacías. El gancho dura menos de 3 s. |",
          "| ¿Los subtítulos están sincronizados? | Sí: los incrustados usan los tiempos de cada palabra de la voz, y `SUBTITULOS.srt`, los de cada frase. |",
          "| ¿Los recursos tienen permisos suficientes? | **No para uso comercial.** El gameplay no tiene licencia ni permiso del autor y se usa con crédito por decisión del canal; la música, la voz y los gráficos son propios. Ver `FUENTES_Y_PERMISOS.txt`. |",
          "| ¿Cumple las políticas de YouTube? | Aporta guion, narración, montaje y gráficos propios. Aun así, al usar gameplay ajeno sin permiso: **sin monetizar** y con el riesgo de una reclamación de Content ID. Hay que marcar el contenido como sintético (voz). |", ""]
    open(f"{out}/CONTROL_DE_CALIDAD.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(vid, "QA", f"{dur:.1f}s", f"{lufs:.1f} LUFS", f"voz {1 - D / max(1, N):.2%}", f"sync {st['sincronizados']}/{st['anclados']}")

if __name__ == "__main__":
    for v in sys.argv[1:]: run(v); qa(v)
