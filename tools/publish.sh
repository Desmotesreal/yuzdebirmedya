#!/usr/bin/env bash
# Videoyu (ve kapağı) 'media' dalına yükler, herkese açık raw URL'leri yazdırır.
# 'media' dalı her seferinde sıfırdan (orphan) zorla gönderilir -> depo şişmez.
# Metricool gönderi oluşturulurken videoyu kendi sunucusuna kopyalar; sonraki gün dosyanın silinmesi sorun değil.
# Kullanım: tools/publish.sh <video.mp4> <hedef_ad.mp4> [kapak.jpg]
set -euo pipefail
SRC="$(readlink -f "$1")"; NAME="$2"; COVER="${3:+$(readlink -f "$3")}"
REPO_URL="https://github.com/Desmotesreal/yuzdebirmedya"
TMP=$(mktemp -d)
cd "$TMP"
git init -q -b media
git remote add origin "$REPO_URL"
mkdir -p reels && cp "$SRC" "reels/$NAME"
[ -n "$COVER" ] && cp "$COVER" "reels/${NAME%.mp4}.jpg"
git add -A
git -c user.name="Yuzde Bir Bot" -c user.email="bot@yuzdebir.local" commit -qm "media $NAME"
git push -q -f origin media 2>&1 | grep -v "push negotiation" || true
URL="https://raw.githubusercontent.com/Desmotesreal/yuzdebirmedya/media/reels/$NAME"
for i in 1 2 3 4 5 6; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -I "$URL") && [ "$code" = 200 ] && break; sleep 5
done
echo "VIDEO_URL=$URL"
[ -n "$COVER" ] && echo "COVER_URL=https://raw.githubusercontent.com/Desmotesreal/yuzdebirmedya/media/reels/${NAME%.mp4}.jpg"
rm -rf "$TMP"
