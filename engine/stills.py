"""Renderiza fotogramas sueltos para revisión: python stills.py v01 12.5 40 80 ..."""
import sys, json, importlib, os, skia
sys.path.insert(0, os.path.dirname(__file__))
import build, gfx
vid = sys.argv[1]; times = [float(x) for x in sys.argv[2:]]
mod = importlib.import_module(f"videos.{vid}"); V = mod.VIDEO
outdir = os.path.join(build.ROOT, V["folder"]); tl = json.load(open(f"{outdir}/recursos/timeline.json"))
W, H = V.get("size", (1920, 1080)); ctx = build.Ctx(V, tl, W, H)
groups = build.group_scenes(V, tl); infos = [build.SceneInfo(g) for g in groups]
os.makedirs("/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad/stills", exist_ok=True)
for gt in times:
    gi = max(i for i, g in enumerate(groups) if g["start"] <= gt)
    s = gfx.new_surface(W, H); c = s.getCanvas(); c.clear(skia.ColorBLACK)
    groups[gi]["fn"](c, gt - groups[gi]["start"], infos[gi], ctx)
    if V.get("overlay"): V["overlay"](c, gt, ctx)
    p = f"/tmp/claude-0/-home-user-Claude-ia/2692e1fb-2c8d-5e01-9751-d8741cc42ebb/scratchpad/stills/{vid}_{gt:07.2f}.png"
    s.makeImageSnapshot().save(p, skia.kPNG); print(p)
