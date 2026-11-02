"""Kullanım (varsayılan: 60 fps, 2x süper örnekleme, yüksek kalite):
  Reels/Shorts : SIZE=1080x1920 SCALE=2 OUT=1080x1920 MAXRATE=25M python3 render.py video ...
  Long (4K60)  : SIZE=1920x1080 SCALE=2 MAXRATE=50M python3 render.py video ...      -> 3840x2160

  python3 render.py stills <video.html> 1.0,2.5,...                 -> <dir>/still_<t>.png + sheet.png
  python3 render.py video  <video.html> <dur> <audio.wav> <out.mp4>
  python3 render.py chunk  <video.html> <t0> <t1> <out.mp4>          (sessiz parça; paralel render için)
Boyut: SIZE=1920x1080 ortam değişkeni (varsayılan 1080x1920).
"""
import sys, os, subprocess
from playwright.sync_api import sync_playwright

W, H = (int(x) for x in os.environ.get("SIZE", "1080x1920").split("x"))
FPS = int(os.environ.get("FPS", "60"))
# Kalite: SCALE=2 -> 2x çözünürlükte çiz (süper örnekleme). OUT=1080x1920 verilirse lanczos ile küçültülür,
# verilmezse yüksek çözünürlük korunur (ör. long video SIZE=1920x1080 SCALE=2 -> 4K).
SCALE = float(os.environ.get("SCALE", "2"))
OUT = os.environ.get("OUT", "")
CRF = os.environ.get("CRF", "16")
MAXRATE = os.environ.get("MAXRATE", "")

def open_page(p, html):
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                          args=["--force-color-profile=srgb", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
    pg.set_default_timeout(180000)
    pg.on("pageerror", lambda e: print("PAGE ERROR:", e))
    pg.goto("file://" + os.path.abspath(html))
    pg.wait_for_function("window.ready===true", timeout=30000)
    return b, pg

def enc(out, audio=None):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-"]
    if audio: cmd += ["-i", audio]
    vf = []
    if OUT: vf = ["-vf", f"scale={OUT.replace('x', ':')}:flags=lanczos"]
    cmd += vf + ["-c:v", "libx264", "-preset", "slow", "-crf", CRF, "-profile:v", "high", "-pix_fmt", "yuv420p",
                 "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-g", str(FPS)]
    if MAXRATE: cmd += ["-maxrate", MAXRATE, "-bufsize", str(int(MAXRATE.rstrip("M")) * 2) + "M"]
    cmd += (["-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest"] if audio else ["-an"])
    cmd += ["-movflags", "+faststart", out]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

if __name__ == "__main__":
    mode, html = sys.argv[1], sys.argv[2]
    d = os.path.dirname(os.path.abspath(html))
    with sync_playwright() as p:
        b, pg = open_page(p, html)
        if mode == "stills":
            ts = sys.argv[3].split(",")
            from PIL import Image
            tw, th = (480, 270) if W > H else (270, 480)
            ims = []
            for t in ts:
                pg.evaluate(f"window.seek({t})")
                path = f"{d}/still_{t}.png"; pg.screenshot(path=path)
                ims.append(Image.open(path).resize((tw, th)))
            cols = min(4 if W > H else 6, len(ims)); rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (tw * cols, th * rows))
            for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
            sheet.save(f"{d}/sheet.png")
        elif mode == "video":
            dur, audio, out = float(sys.argv[3]), sys.argv[4], sys.argv[5]
            ff = enc(out, audio)
            for i in range(int(FPS * dur)):
                pg.evaluate(f"window.seek({i / FPS})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=97))
            ff.stdin.close(); ff.wait(); print("done", out)
        elif mode == "chunk":
            t0, t1, out = float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
            ff = enc(out)
            for i in range(round(t0 * FPS), round(t1 * FPS)):
                pg.evaluate(f"window.seek({i / FPS})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=97))
            ff.stdin.close(); ff.wait(); print("done", out)
        b.close()
