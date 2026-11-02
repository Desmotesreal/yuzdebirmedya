"""Hazır plan dosyasından (plan/<tarih>.json) videoyu baştan sona üretir ve yükler.

Kullanım: ELEVEN_API_KEY=... python3 tools/run_plan.py <YYYY-MM-DD> [--no-render]
Adımlar: script.txt -> tts.py -> warp.py (şablon + müzik) -> mix.py -> stills (sheet.png) -> render_parallel.sh -> publish.sh
Çıktı (son satırlar): VIDEO_URL=..., COVER_MS=..., DUR=...
"""
import json, os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
date = sys.argv[1]
P = json.load(open(os.path.join(ROOT, "plan", f"{date}.json"), encoding="utf-8"))
wd = os.path.join(os.path.expanduser("~"), "work", date); os.makedirs(wd, exist_ok=True)
run = lambda *a, **k: subprocess.run(list(a), check=True, **k)

open(os.path.join(wd, "script.txt"), "w", encoding="utf-8").write("\n".join(P["script"]) + "\n")
run("python3", os.path.join(ROOT, "tools/tts.py"), wd)
json.dump({"offset": 0.3, "tail": 1.3, "orig_dur": P["orig_dur"], "cues": P["cues"]}, open(os.path.join(wd, "cues.json"), "w"))
run("python3", os.path.join(ROOT, "tools/warp.py"), os.path.join(ROOT, "templates", P["template"]), wd, os.path.join(wd, "cues.json"))
W = json.load(open(os.path.join(wd, "warp.json"))); dur = W["dur"]; A = W["anchors"]
def o2n(o):
    for (n0, a), (n1, b) in zip(A, A[1:]):
        if o <= b: return n0 + (n1 - n0) * (o - a) / (b - a) if b > a else n0
    return A[-1][0]
run("python3", os.path.join(ROOT, "tools/mix.py"), os.path.join(wd, "vo.mp3"), os.path.join(wd, "music.wav"), os.path.join(wd, "mix.wav"), str(dur), "0.3")
env = dict(os.environ, SIZE="1080x1920", SCALE="1", FPS="30")
ts = ",".join(str(round(dur * i / 12, 2)) for i in range(1, 12))
run("python3", os.path.join(ROOT, "engine/render.py"), "stills", os.path.join(wd, "index.html"), ts, env=env)
print("STILLS", os.path.join(wd, "sheet.png"))
if "--no-render" in sys.argv: sys.exit(0)
out = os.path.join(wd, f"reel_{date}.mp4")
run(os.path.join(ROOT, "tools/render_parallel.sh"), os.path.join(wd, "index.html"), str(dur), os.path.join(wd, "mix.wav"), out, "reels")
r = subprocess.run([os.path.join(ROOT, "tools/publish.sh"), out, f"{date}.mp4"], check=True, capture_output=True, text=True)
print(r.stdout)
print(f"COVER_MS={int(o2n(P.get('cover_orig', 1.0)) * 1000)}")
print(f"DUR={dur}")
