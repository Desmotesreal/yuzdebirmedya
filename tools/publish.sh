#!/usr/bin/env bash
# Videoyu (ve kapağı) 'media' dalına yükler, herkese açık raw URL'leri yazdırır.
# 'media' dalı her seferinde sıfırdan (orphan) zorla gönderilir -> depo şişmez.
# Metricool gönderi oluşturulurken videoyu kendi sunucusuna kopyalar; sonraki gün dosyanın silinmesi sorun değil.
# Kullanım: tools/publish.sh <video.mp4> <hedef_ad.mp4> [kapak.jpg]
set -euo pipefail
SRC="$(readlink -f "$1")"; NAME="$2"; COVER="${3:+$(readlink -f "$3")}"
# GitHub 100 MB üstü dosyayı reddeder -> önceden durdur (render_parallel.sh zaten ~95 MB altına indirir)
SZ=$(stat -c %s "$SRC")
if [ "$SZ" -gt 99000000 ]; then echo "HATA: $NAME $((SZ/1000000)) MB; GitHub sınırı 100 MB. Önce küçült (render_parallel.sh boyut korumasıyla yeniden çalıştır)." >&2; exit 1; fi
REPO_URL="https://github.com/Desmotesreal/yuzdebirmedya"
TMP=$(mktemp -d)
cd "$TMP"
git init -q -b media
git remote add origin "$REPO_URL"
mkdir -p reels && cp "$SRC" "reels/$NAME"
[ -n "$COVER" ] && cp "$COVER" "reels/${NAME%.mp4}.jpg"
git add -A
git -c user.name="Yuzde Bir Bot" -c user.email="bot@yuzdebir.local" commit -qm "media $NAME"
if ! git push -q -f origin media 2> "$TMP.err"; then
  grep -v "push negotiation" "$TMP.err" >&2; rm -rf "$TMP" "$TMP.err"; echo "HATA: media dalına push başarısız" >&2; exit 1
fi
rm -f "$TMP.err"
URL="https://raw.githubusercontent.com/Desmotesreal/yuzdebirmedya/media/reels/$NAME"
ok=0
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -I "$URL" || true); [ "$code" = 200 ] && { ok=1; break; }; sleep 5
done
[ "$ok" = 1 ] || { echo "HATA: $URL 200 dönmedi (son kod: $code)" >&2; rm -rf "$TMP"; exit 1; }
echo "VIDEO_URL=$URL"
[ -n "$COVER" ] && echo "COVER_URL=https://raw.githubusercontent.com/Desmotesreal/yuzdebirmedya/media/reels/${NAME%.mp4}.jpg"
rm -rf "$TMP"
