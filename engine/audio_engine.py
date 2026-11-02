"""Videoyla senkron, tamamen sentezlenmiş ses tasarımı (telifsiz).
make(spec, out_wav). spec:
  dur, chords=[(t,[bas,n1,n2..])], bright_at, pulses=[(a,b,amp)], motif=[(t,midi)],
  events=[(tür, t, ...)] türler: impact(t,g,big) whoosh(t,d,up,g,pan) riser(t,d,g) tick(t,f,g)
  ticks(t0,t1,n,f0,f1,g) bell(t,midi,g) glitch(t,d,g) plinks(t0,step,n,g) err(t,g)
  heart(t0,t1,period,g) type(t0,t1,rate,g) pop(t,g) swish(t,g)
"""
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], "band", fs=SR, output="sos"), x)

def make(spec, out_path, seed=5):
    rng = np.random.default_rng(seed)
    DUR = spec["dur"]; N = int(SR * DUR); T = np.arange(N) / SR
    dry = np.zeros((N, 2)); send = np.zeros((N, 2))

    def put(sig, t0, gain=1.0, pan=0.0, rev=0.3):
        i0 = int(t0 * SR)
        if i0 >= N or i0 < 0: return
        sig = sig[: N - i0]
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        st = np.stack([sig * l, sig * r], 1) * gain
        dry[i0:i0 + len(sig)] += st; send[i0:i0 + len(sig)] += st * rev

    def pluck(m, d=.9, bright=1.0):
        u = tt(d); f = hz(m)
        s = sum(np.sin(2 * np.pi * f * h * u) * np.exp(-u * (3 + h * 2.5)) / h ** (1.3 / bright) for h in range(1, 6))
        return s * np.minimum(1, u / .004)
    def kick():
        u = tt(.45); f = 50 + 110 * np.exp(-u * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-u * 9)
    def whoosh(d=.7, peak=.55, up=True):
        u = tt(d); n = rng.standard_normal(len(u))
        bands = [(200, 500), (500, 1100), (1100, 2400), (2400, 5000), (5000, 10000)]
        pos = u / d * 4 if up else (1 - u / d) * 4
        out = sum(bp(n, a, b) * np.exp(-((pos - i) ** 2) / 1.2) for i, (a, b) in enumerate(bands))
        env = np.where(u < peak * d, (u / (peak * d)) ** 2, np.exp(-(u - peak * d) / (d * .18)))
        return out * env
    def riser(d):
        u = tt(d); n = rng.standard_normal(len(u)); p = u / d
        noise = hp(n, 800) * p ** 2.5
        f = 180 * (6 ** p); tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * p ** 3 * (1 + .5 * np.sin(2 * np.pi * (4 + 18 * p) * u))
        return noise * .5 + tone * .35
    def impact(big=False):
        d = 2.6 if big else 1.6; u = tt(d)
        f = 30 + 70 * np.exp(-u * 8)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-u * (1.6 if big else 2.6))
        crack = lp(rng.standard_normal(len(u)), 3500) * np.exp(-u * 28)
        tom = np.sin(2 * np.pi * 110 * u) * np.exp(-u * 10) * .5
        return sub * 1.1 + crack * .7 + tom
    def tick(f=2600):
        u = tt(.05)
        return np.sin(2 * np.pi * f * u) * np.exp(-u * 160) + hp(rng.standard_normal(len(u)), 4000) * np.exp(-u * 300) * .4
    def glitch(d=.25):
        u = tt(d); s = np.sign(np.sin(2 * np.pi * 80 * u)) * (rng.standard_normal(len(u)) > .3)
        return bp(s.astype(float), 300, 6000) * (np.floor(u * 40) % 2) * .5
    def bell(m):
        u = tt(2.2); f = hz(m)
        return (np.sin(2 * np.pi * f * u) + .5 * np.sin(2 * np.pi * f * 2.76 * u) * np.exp(-u * 3)) * np.exp(-u * 1.8)
    def heart():
        u = tt(.5)
        th = lambda d0: np.where(u >= d0, np.sin(2 * np.pi * 52 * (u - d0)) * np.exp(-(u - d0) * 14), 0)
        return th(0) + .7 * th(.16)
    def keyclick():
        u = tt(.03); return hp(rng.standard_normal(len(u)), 2500) * np.exp(-u * 260) * .6 + np.sin(2 * np.pi * 1800 * u) * np.exp(-u * 300) * .3
    def pop():
        u = tt(.25); f = 600 + 900 * (1 - np.exp(-u * 40))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-u * 18)
    def swish():
        u = tt(.25); return bp(rng.standard_normal(len(u)), 2000, 9000) * np.sin(np.pi * u / .25) ** 2 * .6

    # ---- pad + bas ----
    CH = spec.get("chords", [])
    pad = np.zeros(N); bass = np.zeros(N)
    for idx, (t0, notes) in enumerate(CH):
        t1 = CH[idx + 1][0] if idx + 1 < len(CH) else DUR
        a, b = int(max(0, t0 - .15) * SR), int(min(DUR, t1 + .5) * SR)
        u = T[a:b] - t0
        env = np.clip((u + .15) / .5, 0, 1) * np.clip((t1 + .5 - T[a:b]) / .6, 0, 1)
        for m in notes[1:]:
            for det in (-.07, 0, .07):
                f = hz(m + det)
                for h in range(1, 6): pad[a:b] += env * np.sin(2 * np.pi * f * h * u + h) / h * .03
        bass[a:b] += env * (np.sin(2 * np.pi * hz(notes[0]) * u) + .3 * np.sin(2 * np.pi * hz(notes[0]) * 2 * u)) * .16
    ba = spec.get("bright_at", DUR)
    mix = np.clip((T - ba) / .3, 0, 1)
    pad_f = lp(pad, spec.get("dark_cut", 900)) * (1 - mix) + lp(pad, 4200) * mix
    put(pad_f * (1 + .12 * np.sin(2 * np.pi * .25 * T)), 0, spec.get("pad_gain", .9), 0, .25)
    put(bass, 0, 1.0, 0, .05)

    def chord_at(t):
        c = CH[0][1] if CH else [45]
        for t0, n in CH:
            if t < t0 - 1e-6: break
            c = n
        return c
    for (za, zb, amp) in spec.get("pulses", []):
        b = za
        while b < zb: put(pluck(chord_at(b)[0] + 12, .22, .6) * .5, b, .35 * amp, 0, .05); b += .25
        b = za
        while b < zb: put(kick(), b, .55 * amp, 0, .02); b += .5
    for t0, m in spec.get("motif", []): put(pluck(m, 1.6, 1.4), t0, .22, rng.uniform(-.4, .4), .5)

    # ---- olaylar ----
    penta = [69, 72, 74, 76, 79, 81, 84, 86, 88, 91]
    for ev in spec.get("events", []):
        kd, t = ev[0], ev[1]; a = ev[2:]
        if kd == "impact": put(impact(a[1] if len(a) > 1 else False), t, a[0] if a else .9, 0, .55)
        elif kd == "whoosh":
            d, up, g, pan = (list(a) + [.6, True, .5, 0][len(a):])[:4]
            put(whoosh(d, .6 if up else .45, up), t, g, pan, .2)
        elif kd == "riser": put(riser(a[0]), t, a[1] if len(a) > 1 else .8, 0, .3)
        elif kd == "tick": put(tick(a[0] if a else 2600), t, a[1] if len(a) > 1 else .5, rng.uniform(-.3, .3), .1)
        elif kd == "ticks":
            t1, n, f0, f1, g = a
            for i in range(n):
                x = i / max(1, n - 1); put(tick(L(f0, f1, x)), L(t, t1, x), g, rng.uniform(-.4, .4), .12)
        elif kd == "tickcurve":   # (t0,t1,n,f0,f1,g, easing) tıklar easing eğrisine göre
            t1, n, f0, f1, g, ez = a
            last = 0
            for fr in range(int(t * 1000), int(t1 * 1000)):
                tm = fr / 1000; v = int(ez((tm - t) / (t1 - t)) * n)
                if v > last: last = v; put(tick(L(f0, f1, v / n)), tm, g, rng.uniform(-.4, .4), .12)
        elif kd == "bell": put(bell(a[0]), t, a[1] if len(a) > 1 else .25, rng.uniform(-.4, .4), .7)
        elif kd == "glitch": put(glitch(a[0] if a else .25), t, a[1] if len(a) > 1 else .5, 0, .2)
        elif kd == "plinks":
            step, n, g = a
            for i in range(n): put(pluck(penta[i % 10] + (12 if i > 19 else 0), .5, 1.3) * .5, t + i * step, g, -.6 + 1.2 * i / max(1, n), .6)
        elif kd == "err":
            u = tt(1.2); s = (np.sin(2 * np.pi * 220 * (1 - .15 * u / 1.2) * u) + np.sin(2 * np.pi * 233 * (1 - .15 * u / 1.2) * u)) * np.exp(-u * 1.5)
            put(lp(s, 2000), t, a[0] if a else .35, 0, .4)
        elif kd == "heart":
            t1, per, g = a; b = t
            while b < t1: put(heart(), b, g, 0, .1); b += per
        elif kd == "type":
            t1, rate, g = a; b = t; r2 = np.random.default_rng(int(t * 100))
            while b < t1: put(keyclick(), b, g * r2.uniform(.6, 1), r2.uniform(-.3, .3), .05); b += 1 / rate * r2.uniform(.6, 1.4)
        elif kd == "pop": put(pop(), t, a[0] if a else .4, 0, .3)
        elif kd == "swish": put(swish(), t, a[0] if a else .4, rng.uniform(-.5, .5), .2)

    # ---- reverb + master ----
    ir_t = tt(2.4)
    ir = np.stack([lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 2.6), 6000) for _ in range(2)], 1)
    wet = np.stack([fftconvolve(send[:, c], ir[:, c])[:N] for c in range(2)], 1)
    wet /= np.max(np.abs(wet)) + 1e-9
    out = dry + wet * np.max(np.abs(dry)) * .28
    out *= (np.clip(T / .2, 0, 1) * np.clip((DUR - T) / .6, 0, 1))[:, None]
    out = np.tanh(out / np.max(np.abs(out)) * 1.8) / np.tanh(1.8) * .95
    pcm = (out * 32767).astype(np.int16)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return out_path

def L(a, b, x): return a + (b - a) * x
def ioq(x): x = min(1, max(0, x)); return 2 * x * x if x < .5 else 1 - (-2 * x + 2) ** 2 / 2
def ioc(x): x = min(1, max(0, x)); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def oc(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
