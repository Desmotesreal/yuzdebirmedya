#!/usr/bin/env bash
# En yüksek kalitede paralel render + ses birleştirme.
# Kullanım: tools/render_parallel.sh <index.html> <sure_sn> <mix.wav> <cikti.mp4> [reels|long]
#  reels : 1080x1920, 2x süper örnekleme -> 1080x1920, 60 fps, CRF 16, maxrate 17M (+ 95 MB boyut koruması: GitHub 100 MB sınırı)
#  long  : 1920x1080, 2x -> 3840x2160 (4K60), CRF 16, maxrate 50M
set -euo pipefail
HTML="$1"; DUR="$2"; AUDIO="$3"; OUTF="$4"; MODE="${5:-reels}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N=$(nproc); [ "$N" -lt 1 ] && N=1
if [ "$MODE" = long ]; then export SIZE=1920x1080 SCALE=2 OUT= MAXRATE=50M; else export SIZE=1080x1920 SCALE=2 OUT=1080x1920 MAXRATE=17M; fi
export FPS=60 CRF=16
TMP=$(mktemp -d)
pids=()
for i in $(seq 0 $((N-1))); do
  t0=$(python3 -c "print(round($DUR*$i/$N*60)/60)"); t1=$(python3 -c "print(round($DUR*($i+1)/$N*60)/60)")
  python3 "$ROOT/engine/render.py" chunk "$HTML" "$t0" "$t1" "$TMP/c$i.mp4" > "$TMP/c$i.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
for i in $(seq 0 $((N-1))); do grep -q "^done" "$TMP/c$i.log" || { cat "$TMP/c$i.log"; exit 1; }; echo "file '$TMP/c$i.mp4'"; done > "$TMP/list.txt"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -i "$AUDIO" -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$OUTF"
rm -rf "$TMP"
# Boyut koruması (reels): publish.sh GitHub'a yükler, 100 MB üstü reddedilir -> 95 MB altına yeniden kodla
LIMIT=95000000
if [ "$MODE" = reels ] && [ "$(stat -c %s "$OUTF")" -gt "$LIMIT" ]; then
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUTF")
  KB=$(python3 -c "print(int($LIMIT*8/$D/1000*0.93-330))")
  echo "Boyut > 95 MB -> ${KB}k ile 2 geçişli yeniden kodlama"
  T2=$(mktemp -d)
  ffmpeg -y -loglevel error -i "$OUTF" -c:v libx264 -preset slow -b:v ${KB}k -maxrate ${KB}k -bufsize $((KB*2))k -pass 1 -passlogfile "$T2/p" -g 60 -pix_fmt yuv420p -an -f mp4 /dev/null
  ffmpeg -y -loglevel error -i "$OUTF" -map 0 -c:v libx264 -preset slow -b:v ${KB}k -maxrate ${KB}k -bufsize $((KB*2))k -pass 2 -passlogfile "$T2/p" \
    -profile:v high -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -g 60 -c:a copy -movflags +faststart "$T2/o.mp4"
  mv "$T2/o.mp4" "$OUTF"; rm -rf "$T2"
fi
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size -of compact "$OUTF"
echo "RENDER_OK $OUTF"
