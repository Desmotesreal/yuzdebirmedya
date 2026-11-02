"""Hazır bir şablon videoyu (templates/<ad>) seslendirmeye göre yeniden zamanlar.

Kullanım: python3 tools/warp.py <template_dir> <workdir> <cues.json>
cues.json:
  {"offset": 0.3,            # ses videonun başından kaç sn sonra başlar
   "tail": 1.2,              # son cümleden sonra kalan süre
   "orig_dur": 21,           # şablonun orijinal süresi (CONFIG.dur)
   "cues": [[cumle_no, oran, sablon_zamani], ...]}
   - cumle_no: timing.json'daki cümle indeksi
   - oran: 0 = cümle başı, 1 = cümle sonu (ör. kelime cümlenin ortasındaysa 0.5)
   - sablon_zamani: şablonda o anın (yazının/animasyonun) saniyesi
Çıktı: <workdir>/index.html (zaman-bükmeli), <workdir>/music.wav, <workdir>/warp.json ; süreyi yazdırır.
"""
import json, os, sys, re, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl, wd, cfile = sys.argv[1], sys.argv[2], sys.argv[3]
tpl = os.path.abspath(tpl); wd = os.path.abspath(wd)
C = json.load(open(cfile)); T = json.load(open(os.path.join(wd, "timing.json")))
off, S = C.get("offset", 0.3), T["sentences"]
A = [(0.0, 0.0)]
for si, fr, ot in C["cues"]:
    s = S[si]; A.append((round(off + s["start"] + fr * (s["end"] - s["start"]), 3), float(ot)))
new_dur = round(off + T["duration"] + C.get("tail", 1.2), 2)
A.append((new_dur, float(C["orig_dur"])))
A.sort()
for (n0, o0), (n1, o1) in zip(A, A[1:]):
    assert n1 > n0 and o1 >= o0, f"anchors monoton değil: {(n0,o0)} -> {(n1,o1)}"
json.dump({"anchors": A, "dur": new_dur}, open(os.path.join(wd, "warp.json"), "w"))

def o2n(o):
    for (n0, a), (n1, b) in zip(A, A[1:]):
        if o <= b: return n0 + (n1 - n0) * (o - a) / (b - a) if b > a else n0
    return A[-1][0]

# --- html
html = open(os.path.join(tpl, "index.html"), encoding="utf-8").read()
eng = "file://" + os.path.join(ROOT, "engine") + "/"
html = re.sub(r'(\.\./)+engine/', eng, html)
inj = ("<script>const WA=%s;function warp(t){for(let i=1;i<WA.length;i++){const[n0,a]=WA[i-1],[n1,b]=WA[i];"
       "if(t<=n1)return a+(b-a)*(t-n0)/(n1-n0)}return WA[WA.length-1][1]}"
       "const _seek=window.seek;window.seek=t=>_seek(warp(t));</script></body></html>") % json.dumps([[n, o] for n, o in A])
html = html.replace("</body></html>", inj)
open(os.path.join(wd, "index.html"), "w", encoding="utf-8").write(html)

# --- music: şablonun audio.py'sini, make() zamanlarını bükerek çalıştır
sys.path.insert(0, os.path.join(ROOT, "engine"))
import audio_engine
_make = audio_engine.make
T1 = {"ticks", "tickcurve", "heart", "type"}
def wmake(spec, _out, seed=5):
    sp = dict(spec); sp["dur"] = new_dur
    sp["bright_at"] = o2n(spec.get("bright_at", spec["dur"]))
    sp["chords"] = [(o2n(t), n) for t, n in spec.get("chords", [])]
    sp["pulses"] = [(o2n(a), o2n(b), g) for a, b, g in spec.get("pulses", [])]
    sp["motif"] = [(o2n(t), m) for t, m in spec.get("motif", [])]
    ev = []
    for e in spec.get("events", []):
        e = list(e); k = e[0]
        if k == "riser": e[1] = max(0, o2n(e[1] + e[2]) - e[2])
        else:
            if k in T1: e[2] = o2n(e[2])
            e[1] = o2n(e[1])
        ev.append(tuple(e))
    sp["events"] = ev
    return _make(sp, os.path.join(wd, "music.wav"), seed)
audio_engine.make = wmake
src = open(os.path.join(tpl, "audio.py"), encoding="utf-8").read()
src = re.sub(r"sys\.path\.insert\(0,[^)]*\)", "pass", src)
cwd = os.getcwd(); os.chdir(tpl)
try: exec(compile(src, "audio.py", "exec"), {"__name__": "__main__"})
finally: os.chdir(cwd)
print("DUR", new_dur)
