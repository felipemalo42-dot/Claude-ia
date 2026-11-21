"""Prepara los clips de gameplay de terceros (catálogo videos/gp_clips.json) para el montaje de gp.

Uso:  python3 clips_externos.py            → comprueba qué clips hay y prepara los nuevos
      python3 clips_externos.py ID [ID…]   → solo esos
      python3 clips_externos.py --hq [--plan] → extrae a 1080p, de la copia 4K de Internet Archive, solo los tramos que usa gp
                                             (con --plan usa la duración real de cada plano; sin él, una estimación de 7 s)

Por cada clip presente en GTA6_VIDEO_LANZAMIENTO/clips_externos/ (ID.mp4, .mkv, .webm o .mov):
  1. ficha técnica (resolución, fotogramas por segundo, duración) y aviso si el ID no está en el catálogo;
  2. cortes de escena en dos pasadas (umbral 0,22 y 0,10), en el mismo formato que usa gl_render.cuts_for;
  3. hojas de contacto (un fotograma cada 10 s, con su minuto) para elegir los planos de cada frase del guion.
Los clips no se suben al repositorio (pesan demasiado); el crédito de cada uno va en pantalla y en FUENTES_Y_ENLACES.txt.
"""
import glob, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from videos import gl_render as R

STEP = float(os.environ.get("XSTEP", 12))   # segundos entre fotogramas de la hoja de contacto
COLS, TW, TH = 8, 240, 135

def probe(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:format=duration",
                        "-of", "json", p], capture_output=True, text=True, check=True)
    j = json.loads(o.stdout); st = j["streams"][0]; n, d = st["r_frame_rate"].split("/")
    return dict(w=st["width"], h=st["height"], fps=round(int(n) / int(d), 2), dur=float(j["format"]["duration"]))

def scene_cuts(p, thr):
    """Instantes de corte de escena (scdet sobre una copia reducida, para que sea rápido en vídeos de horas)."""
    o = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-an", "-vf", f"fps=10,scale=320:-2,select='gt(scene,{thr})',metadata=print:file=-",
                        "-f", "null", "-"], capture_output=True, text=True)
    return [float(l.split("pts_time:")[1]) for l in o.stdout.splitlines() if "pts_time:" in l]

def sheets(vid, p, dur, out):
    os.makedirs(out, exist_ok=True)
    tmp = f"{out}/_f"; os.makedirs(tmp, exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", p, "-an", "-vf", f"fps=1/{STEP},scale={TW}:{TH}:force_original_aspect_ratio=decrease,pad={TW + 4}:{TH + 4}:(ow-iw)/2:(oh-ih)/2", f"{tmp}/%05d.jpg"], check=True)
    fr = sorted(glob.glob(f"{tmp}/*.jpg")); per = COLS * 6; ft = ImageFont.load_default()
    for s in range(0, len(fr), per):
        chunk = fr[s:s + per]; rows = (len(chunk) + COLS - 1) // COLS
        im = Image.new("RGB", (COLS * TW, rows * TH), (20, 20, 20)); dr = ImageDraw.Draw(im)
        for i, f in enumerate(chunk):
            x, y = (i % COLS) * TW, (i // COLS) * TH; im.paste(Image.open(f).resize((TW, TH)), (x, y))
            t = (s + i) * STEP; lab = f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{int(t % 60):02d}"
            dr.rectangle([x, y, x + 52, y + 12], fill=(0, 0, 0)); dr.text((x + 3, y + 1), lab, fill=(255, 220, 60), font=ft)
        im.save(f"{out}/{vid}_{s // per:03d}.jpg", quality=80)
    for f in fr: os.remove(f)
    os.rmdir(tmp)

def main(ids):
    os.makedirs(f"{R.SCR}/cuts", exist_ok=True); os.makedirs(f"{R.SCR}/cuts2", exist_ok=True)
    present = {os.path.splitext(os.path.basename(p))[0]: p for p in glob.glob(f"{R.XDIR}/*") if p.rsplit(".", 1)[-1] in ("mp4", "mkv", "webm", "mov")}
    for vid in sorted(set(present) - set(R.XCAT)): print(f"[aviso] {vid}: no está en el catálogo (sin licencia ni autor comprobados): no se usará")
    todo = ids or sorted(present)
    for vid in R.XCAT:
        if vid not in present: print(f"[falta] {vid}  {R.XCAT[vid]['autor']} · {R.XCAT[vid]['titulo'][:60]}")
    for vid in todo:
        if vid not in present or vid not in R.XCAT: continue
        p = present[vid]; m = probe(p)
        print(f"[ok] {vid}  {m['w']}x{m['h']} {m['fps']} fps {m['dur'] / 60:.1f} min  ({R.XCAT[vid]['autor']})")
        for d, thr in (("cuts", 0.22), ("cuts2", 0.10)):
            f = f"{R.SCR}/{d}/{vid}.txt"
            if not os.path.exists(f): open(f, "w").write(" ".join(f"{x:.3f}" for x in scene_cuts(p, thr)))
        out = f"{R.SCR}/xsheets/{vid}"
        if not glob.glob(f"{out}/*.jpg"): sheets(vid, p, m["dur"], out)

# ---------------------------------------------------------------- tramos en alta calidad
NET = ["-http_proxy", os.environ.get("HTTPS_PROXY", ""), "-ca_file", "/root/.ccr/ca-bundle.crt", "-tls_verify", "1"] if os.environ.get("HTTPS_PROXY") else []
def hq_url(vid):
    m = R.XCAT[vid]
    if "archive.org/details/" in m.get("copia", ""):
        ident = m["copia"].rsplit("/", 1)[1]; return f"https://archive.org/download/{ident}/{vid}.webm"
    return None

def hq(plan=False):
    import importlib, concurrent.futures as cf
    M = importlib.import_module("videos.gp")
    need = {}
    if plan:
        import build
        ctx = build.Ctx(M.VIDEO, json.load(open(f"{build.ROOT}/{M.VIDEO['folder']}/recursos/timeline.json")), 1920, 1080)
        shots = R.table(ctx)["shots"]
    else:
        shots = [dict(sh, t0=0.0, t1=7.0) for b in M.B for sh in b.get("shots", [])]
    for sh in shots:
        if not sh["src"].startswith("x:"): continue
        vid = sh["src"][2:].split("@")[0]
        path, loc, Ls = R.src_window(dict(sh))
        if probe(path)["h"] >= 1080 or not hq_url(vid): continue      # la copia local ya es HD
        k = (vid, round(loc, 3)); need[k] = max(need.get(k, 0.0), min(Ls, sh["t1"] - sh["t0"]) + 0.4)
    os.makedirs(R.XHQ, exist_ok=True)
    def one(item):
        (vid, loc), L = item; out = f"{R.XHQ}/{vid}_{loc:.3f}.mp4"
        if os.path.exists(out) and probe(out)["dur"] >= L - 0.05: return None
        tmp = out + ".part.mp4"
        r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *NET, "-ss", f"{loc:.3f}", "-i", hq_url(vid), "-t", f"{L:.3f}", "-an",
                            "-vf", "scale=1920:1080:force_original_aspect_ratio=increase:flags=bicubic,crop=1920:1080,fps=30",
                            "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], capture_output=True, text=True)
        if r.returncode or not os.path.exists(tmp): return f"{vid}@{loc}: {r.stderr.strip()[-200:]}"
        os.replace(tmp, out); return None
    items = sorted(need.items()); errs = []
    with cf.ThreadPoolExecutor(3) as ex:
        for i, e in enumerate(ex.map(one, items)):
            if e: errs.append(e); print("[error]", e, flush=True)
            if i % 10 == 0: print(f"  {i + 1}/{len(items)}", flush=True)
    print(f"tramos HQ: {len(items)} · errores: {len(errs)}")

if __name__ == "__main__":
    if "--hq" in sys.argv: hq("--plan" in sys.argv)
    else: main(sys.argv[1:])
