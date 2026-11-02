# Yüzde Bir — günlük Reels/Shorts hattı

Bu depo, **@yuzdebir.tr** (Instagram) ve **Yüzde Bir** (YouTube) hesaplarının tam otomatik içerik hattıdır.
Her sabah çalışan görev bu dosyayı baştan sona okuyup adımları uygular. Hesap sahibi: Umut (Türkçe konuşur).

## Sabitler
| Ne | Değer |
|---|---|
| Metricool brand/blogId | `7823005` (zaman dilimi `Europe/Istanbul`) |
| Instagram | `yuzdebir.tr` |
| YouTube kanal | `UCuuIjGsjz_os2tGTUZVb7kw` |
| Depo | `Desmotesreal/yuzdebirmedya` (herkese açık, **asla gizli bilgi koyma**) |
| Ses | ElevenLabs, ses `J17lijyP1BHYcM7ld0Rg` (Adam, Türkçe), model `eleven_v4`, `language_code=tr` |
| ElevenLabs anahtarı | Sadece görev talimatında; `ELEVEN_API_KEY` ortam değişkeni olarak kullan, dosyaya/depoya yazma |
| Paylaşım günleri | **Çarşamba hariç** her gün **07:00** (Europe/Istanbul) — Instagram Reel + YouTube Short (tek gönderi) |
| Format | 1080×1920, **60 fps**, 2x süper örnekleme, CRF 16, AAC 320k, -14 LUFS |

## Marka
- İsim: **Yüzde Bir (%1)** — "Her gün %1 daha iyi." Motivasyon hesabı, haber hesabı değil.
- Görsel dil: koyu sinematik zemin, kinetik tipografi (Inter Display 800–900), bokeh + ışık sızıntısı + film grain,
  her videoda **tek vurgu rengi** (gold / cyan / ember / violet; kırmızı sadece kayıp/uyarı), swoosh/impact/riser ses tasarımı.
- Yapı: **kanca (0–2 sn)** → simülasyon/veri ya da güçlü tek fikir → yüzleşme → CTA (kaydet / yorumlara yaz).
- Süre 22–35 sn. 9–12 cümle. Her cümlenin ekranda karşılığı olur; sayılar **söylendiği anda** ekrana gelir.

## Her sabahki adımlar
0. **Hazırlık**: Bu depo klonlu değilse `add_repo` (owner `Desmotesreal`, repo `yuzdebirmedya`, access `push`) ile ekle ve
   `git clone https://github.com/Desmotesreal/yuzdebirmedya ~/yuzdebirmedya`. `ffmpeg`, `/usr/bin/google-chrome`,
   python `playwright`, `scipy`, `numpy`, `PIL` ve Inter fontu (`fc-list | grep Inter`) olmalı.
1. **Tarih**: Bugünün tarihini (Europe/Istanbul) al. `posts.json` oku: aynı konuyu/kancayı son 30 günde tekrar etme.
   **Çift paylaşım kontrolü**: Metricool `getScheduledPosts` (brandId 7823005, bugün 00:00–23:59, Europe/Istanbul) —
   bugüne zaten planlı bir Reel/Short varsa yenisini üretme; sadece adım 10 (istatistik) ve 12 (rapor) yap.
2. **Plan var mı?** `plan/<YYYY-MM-DD>.json` varsa → `ELEVEN_API_KEY=... python3 tools/run_plan.py <tarih> --no-render`,
   `~/work/<tarih>/sheet.png`'ye **bak** (yazı taşması / çakışma yoksa) → `python3 tools/run_plan.py <tarih>` (render + yükleme) → adım 8.
   Plan yoksa adım 3'ten devam: **yeni içerik üret**.
3. **Gündem + fikir** (WebSearch, Türkçe): bugünün/haftanın Türkiye gündemi — sınav tarihleri (ÖSYM/MEB), özel günler,
   mevsim/ay başı-sonu, büyük spor olayları, viral konular. Gündemi **kanca** olarak kullan, motivasyon mesajına bağla.
   Siyaset, trajedi, kişiler hakkında iddia **yok**. Uygun gündem yoksa `IDEAS.md` havuzundan seç.
   Format karışımı: gündem kancalı (haftada 2–3), simülasyon/veri ("günde X = yılda Y"), kinetik tipografi (özgün söz),
   "ya … olsaydı" senaryosu. Haftalık istatistiklere göre iyi gideni artır (adım 10).
4. **Rakamlar**: Her sayıyı python ile hesapla; tarihli bilgiyi (ör. sınav tarihi) kaynağıyla doğrula, kaynağı açıklamaya yaz.
5. **Seslendirme metni** `~/work/<tarih>/script.txt` — her satır bir cümle. KURALLAR:
   - **Kesme işareti yok** ("Ocakta", "Aralıkta", "Mertin"), yoksa ses duraksar. `tools/tts.py` kesme görürse durur.
   - **Ekli sayılar yazıyla**: "iki bin yirmi yediye", "yüzde seksen dördü", "on iki kitap". Yüzde işareti yerine "yüzde".
   - Kısa, konuşma dilinde cümleler. İlk cümle merak uyandıran kanca. Son cümle CTA.
   Sonra: `ELEVEN_API_KEY=... python3 tools/tts.py ~/work/<tarih>` → `vo.mp3` + `timing.json` (cümle ve kelime zamanları).
6. **Görsel** `~/work/<tarih>/index.html` — **HER VİDEO YENİ TASARIM** (YouTube "tekrarlayan içerik" riskine karşı):
   `designs.json`'u oku; son 30 günde kullanılan **ana görsel fikri, yerleşim ve vurgu rengini tekrar etme**.
   Her gün farklı bir ana metafor seç (ör. kum saati, yol/harita, merdiven, pil, nabız grafiği, takvim yırtılması, kitap
   rafı, termometre, şehir silüeti dolumu, satranç, damla damla dolan bardak, fitil/mum, yörünge, bar yarışı, sayaç
   kilidi…), sahne geçişlerini ve tipografi düzenini de çeşitlendir. `templates/` sadece **kod/teknik örneği**dir,
   kompozisyonları kopyalanmaz. Tasarımı bitirince `designs.json`'a {date, metafor, yerlesim, vurgu, gecisler} ekle. Motor: `engine/engine.js` (`boot({dur,scene(t),...})`, `split`, `charsIn`, `slam`, `maskLine`,
   `fadeBlock`, `sweep`, `ENG.mid` canvas, `pulse`, `k`, `E` easing'leri). Zamanları **doğrudan timing.json'dan** al
   (videoda ses `offset=0.3` sn gecikmeli başlar: ekran zamanı = 0.3 + cümle/kelime başlangıcı — HTML'de `const O=.3` tanımlayıp
   **her** zamanı `O+<timing.json değeri>` diye yaz; elle çıkarılmış zaman yazma, sahneler kayar). `dur` = 0.3 + ses süresi + 1.3.
   Engine yolu: `<script src="file:///home/.../yuzdebirmedya/engine/engine.js">` gibi **mutlak yol** kullan (CSS için de).
   Güvenli alan: önemli yazıları y=300–1500 arasında tut (Instagram arayüzü üst/altı kapatır). Uzun kelimede h1 ≤ 220px.
   Kontrol: `SIZE=1080x1920 SCALE=1 FPS=30 python3 engine/render.py stills index.html t1,t2,...` → `sheet.png`'ye **bak**,
   taşma/çakışma varsa düzelt (en fazla 2 tur).
   Alternatif: bir şablonu olduğu gibi kullanacaksan `tools/warp.py` (cues.json: [cümle_no, oran, şablon_zamanı]).
7. **Müzik** `~/work/<tarih>/audio.py`: şablonlardaki `audio.py` gibi `audio_engine.make(spec, 'music.wav')`
   (chords / pulses / motif / events — impact, whoosh, riser, ticks, bell…) olayları sahne zamanlarına hizala.
   `python3 tools/mix.py vo.mp3 music.wav mix.wav <dur> 0.3`.
8. **Render + yükleme**: `tools/render_parallel.sh index.html <dur> mix.wav reel_<tarih>.mp4 reels` (2 çekirdekte 40 sn video ≈ 38 dk;
   süre videonun uzunluğuyla doğru orantılı → 35 sn'yi aşma). Çıktı **95 MB'ı geçerse script otomatik yeniden kodlar**
   (GitHub 100 MB üstünü reddeder). `publish.sh` push ya da URL kontrolü başarısız olursa **hata koduyla çıkar** — VIDEO_URL
   satırı yoksa Metricool'a gönderme, raporla. →
   `tools/publish.sh reel_<tarih>.mp4 <tarih>.mp4` → `VIDEO_URL=...`. Kapak karesi: kanca yazısının tam göründüğü an (ms).
   Render hata verirse bir kez `FPS=30 SCALE=1` ile tekrar dene.
9. **Metricool'a planla** (07:00 Europe/Istanbul; saat geçtiyse şimdi+15 dk). **TEK gönderi** (ücretsiz planda ayda 20
   yayın sınırı var; iki ağı tek gönderide birleştir): `providers=[{"network":"instagram"},{"network":"youtube"}]`,
   `media=[VIDEO_URL]`, `autoPublish=true`, `videoCoverMilliseconds=<kapak ms>`, `text`=açıklama + hashtagler,
   `instagramData={"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}`,
   `youtubeData={"title":"... #shorts" (≤100 karakter),"type":"short","privacy":"public","tags":[...],"category":"EDUCATION",
   "madeForKids":false,"isAiGeneratedContent":false}`. Kapak yüzünden reddedilirse kapak alanını çıkarıp bir kez tekrar dene.
   Yanıttaki `media` metricool adresine dönmeli. Ayın kaçıncı yayını olduğunu `posts.json`'dan say; 18'i geçtiyse raporda uyar.
   Açıklama: 2–3 cümle (kanca + değer + CTA), sonra 6–8 Türkçe hashtag.
10. **İstatistik** (her gün kısa, pazar günleri detaylı): Metricool `getAnalyticsAvailableMetrics` (instagram/reels,
    youtube) → son 7 günün izlenme/erişim/kaydetme/paylaşım değerlerini çek; `insights.md`'ye tarihli kısa not düş
    (hangi format/kanca iyi gitti, ne değişecek). Format karışımını buna göre kaydır.
11. **Kayıt**: `posts.json`'a ekle `{date, topic, format, hook, script, caption, yt_title, video_url, metricool_ids}` →
    `git add -A && git commit -m "<tarih> reels" && git push origin main` (yalnızca main; videolar main'e girmez).
12. **Rapor**: Son mesajda Türkçe 3–5 satır: konu, kanca, planlanan saat, Metricool linkleri, varsa sorun.
    ElevenLabs kredisi 3.000'in altına düştüyse ya da bir adım başarısızsa bunu açıkça yaz. (Kredi `GET /v1/user/subscription`
    ile okunur; anahtarda `user_read` izni yoksa 401 döner → "kredi okunamadı" yaz, adımı atla.)

## Hata durumları
- TTS hata (402/401): anahtar/plan sorunu → rapor et, o gün dünkü değil **yedek plan**: `plan/` altında kullanılmamış bir
  plan varsa onu sessiz şablonla değil, yine seslendirmeli üretmeye çalış; olmazsa rapor et, paylaşım yapma.
- Metricool hata: hatayı olduğu gibi raporla, metni değiştirip tekrar deneme döngüsüne girme (en fazla 1 tekrar).
- Asla: gizli anahtarı depoya yazma, telifli müzik/görsel/söz kullanma, gerçek kişiler adına söz uydurma.
