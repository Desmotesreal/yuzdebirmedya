"""Seslendirme + müzik karışımı (sidechain ducking, -14 LUFS).

Kullanım: python3 tools/mix.py <vo.mp3> <music.wav> <out.wav> <toplam_sure_sn> [vo_gecikme_sn=0.3]
"""
import subprocess, sys

vo, music, out, dur = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
off = int(float(sys.argv[5] if len(sys.argv) > 5 else 0.3) * 1000)
fc = (f"[0:a]adelay={off}|{off},aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,"
      f"acompressor=threshold=-20dB:ratio=3:attack=5:release=120,volume=1.6,apad=whole_dur={dur},asplit=2[v][sc];"
      f"[1:a]volume=0.38[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[md];"
      f"[v][md]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vo, "-i", music, "-filter_complex", fc,
                "-ar", "48000", "-t", str(dur), out], check=True)
print("mix ok", out)
