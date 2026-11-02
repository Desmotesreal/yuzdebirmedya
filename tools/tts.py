"""ElevenLabs seslendirme + cümle/kelime zamanlaması.

Kullanım:
  ELEVEN_API_KEY=... python3 tools/tts.py <workdir>
Girdi : <workdir>/script.txt  -> her satır BİR cümle (seslendirilecek metin, kurallara uygun yazılmış).
Çıktı : <workdir>/vo.mp3, <workdir>/timing.json
        timing.json = {"duration": s, "sentences":[{"i","text","start","end"}], "words":[{"w","start","end","s"}]}

Kurallar (PIPELINE.md): kesme işareti YOK (Ocakta, Aralıkta), ekli sayılar yazıyla
(iki bin yirmi yediye, yüzde seksen dördü). Düz sayılar rakamla yazılabilir ama yazıyla daha güvenli.
"""
import json, os, sys, base64, re, urllib.request

VOICE = os.environ.get("ELEVEN_VOICE", "J17lijyP1BHYcM7ld0Rg")   # Adam - Deep, Professional (Türkçe, İstanbul)
MODEL = os.environ.get("ELEVEN_MODEL", "eleven_v4")

def main(wd):
    key = os.environ["ELEVEN_API_KEY"]
    lines = [l.strip() for l in open(os.path.join(wd, "script.txt"), encoding="utf-8") if l.strip()]
    bad = [l for l in lines if "'" in l or "’" in l]
    if bad:
        sys.exit("HATA: kesme işareti var (seslendirmede duraksatır): " + " | ".join(bad))
    text = " ".join(lines)
    body = json.dumps({"text": text, "model_id": MODEL, "language_code": "tr"}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    open(os.path.join(wd, "vo.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    a = d.get("normalized_alignment") or d["alignment"]
    chars, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    full = "".join(chars)
    # cümle sınırları: metindeki karakter ofsetleri (alignment metni girdiyle aynı uzunlukta olmayabilir -> sırayla eşle)
    sents, pos = [], 0
    for i, l in enumerate(lines):
        j = full.find(l[:12], pos)
        if j < 0: j = pos
        k = j + len(l) - 1
        k = min(k, len(chars) - 1)
        sents.append({"i": i, "text": l, "start": round(st[j], 3), "end": round(en[k], 3)})
        pos = k + 1
    words, cur, ws = [], "", None
    si = 0
    for c, s, e in zip(chars, st, en):
        if c.strip() == "":
            if cur: words.append({"w": cur, "start": round(ws, 3), "end": round(pe, 3)}); cur = ""
            continue
        if not cur: ws = s
        cur += c; pe = e
    if cur: words.append({"w": cur, "start": round(ws, 3), "end": round(pe, 3)})
    for w in words:
        w["s"] = max([x["i"] for x in sents if x["start"] <= w["start"] + 1e-3] or [0])
    out = {"duration": round(en[-1], 3), "sentences": sents, "words": words}
    json.dump(out, open(os.path.join(wd, "timing.json"), "w"), ensure_ascii=False, indent=1)
    for x in sents: print(f'{x["start"]:6.2f}-{x["end"]:6.2f}  {x["text"]}')
    print("duration", out["duration"], "chars", len(text))

if __name__ == "__main__":
    main(sys.argv[1])
