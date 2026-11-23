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
- Hedef kitle: **LGS ve YKS'ye hazırlanan öğrenciler** (YouTube'da tutan kitle bu; bkz. adım 2b).
- Görsel dil: koyu sinematik zemin, kinetik tipografi (Inter Display 800–900), bokeh + ışık sızıntısı + film grain,
  her videoda **tek vurgu rengi** (gold / cyan / ember / violet; kırmızı sadece kayıp/uyarı), swoosh/impact/riser ses tasarımı.
- Yapı: **kanca (0–2 sn)** → simülasyon/veri ya da güçlü tek fikir → yüzleşme → CTA (**kaydet / arkadaşına gönder**;
  "yorumlara yaz" kullanma: 2–22 Kasım'daki 18 Reel'de 0 yorum geldi).
- Süre hedefi **24–26 sn** (üst sınır 35). 8–10 cümle. Her cümlenin ekranda karşılığı olur; sayılar **söylendiği anda** ekrana gelir.

## Her sabahki adımlar
0. **Hazırlık**: Bu depo klonlu değilse `add_repo` (owner `Desmotesreal`, repo `yuzdebirmedya`, access `push`) ile ekle ve
   `git clone https://github.com/Desmotesreal/yuzdebirmedya ~/yuzdebirmedya`. `ffmpeg`, `/usr/bin/google-chrome`,
   python `playwright`, `scipy`, `numpy`, `PIL` ve Inter fontu (`fc-list | grep Inter`) olmalı.
1. **Tarih**: Bugünün tarihini (Europe/Istanbul) al. `posts.json` oku: aynı konuyu/kancayı son 30 günde tekrar etme.
   **Çift paylaşım kontrolü**: Metricool `getScheduledPosts` (brandId 7823005, bugün 00:00–23:59, Europe/Istanbul) —
   bugüne zaten planlı bir Reel/Short varsa yenisini üretme; sadece adım 10 (istatistik) ve 12 (rapor) yap.
2b. **Konu/kanca seçimi: YouTube önceliklidir** (24 Kasım 2026 kararı; konu seçmeden ve plan kullanmadan ÖNCE; analiz yayını asla durdurmaz):
   **Neden:** Aynı videolar Instagram'da format ne olursa olsun 130–160 izlenme bandında kalıyor (bu fark gürültüdür),
   YouTube'da ise 13 Kasım'dan beri Short başına 1,3K–6,6K izleniyor. Bu yüzden format kararı **yalnızca YouTube
   izlenmesine** göre verilir. Instagram sayıları raporlanır ama format sıralamak ya da konu seçmek için **kullanılmaz**.
   **Veri:** Metricool `getAnalyticsDataByMetrics` (brandId 7823005, bugün−14 gün 00:00 → bugün 23:59, `+03:00`):
   - YouTube kanal toplamı `YTEV01,YTEV02,YTEV05` (abone, günlük izlenme, kazanılan abone). Video bazlı YouTube listeleri
     (`YTVP…`, `YTVV…`) boş dönüyor; onlara güvenme.
   - Video bazlı YouTube izlenmesi `insights.md`'deki en son **"YouTube video bazlı"** nottadır (kanal sayfasından elle
     alınır). Yeni not yoksa aşağıdaki karışımı aynen uygula.
   - IG Reels `IGRE01,IGRE03,IGRE23,IGRE11,IGRE12,IGRE21,IGRE24` yalnızca rapor için.
   **Haftalık karışım (Pazartesi–Pazar, çarşamba hariç 6 yayın günü), zorunlu:**
   - **3 video LGS.** YouTube'da en iyi giden konu (17 Kasım hata defteri 6,6K, 14 Kasım ara tatil 3,6K). Her LGS videosu
     son 3 LGS videosundan **farklı bir açı** kullanır: somut çalışma yöntemi (hata defteri gibi), "günde X soru = Y deneme"
     hesabı, ders bazlı (paragraf, yeni nesil matematik, fen, inkılap), deneme analizi/net artırma, 8. sınıf günlük düzeni
     (uyku, telefon) LGS'ye bağlanarak.
   - **1 video YKS/TYT** (YouTube'da ortalama 1,7K).
   - **2 video okul gündemi**: karne, okula dönüş, tatil, deneme haftası, özel gün gibi öğrencinin o haftaki gerçeği +
     somut sayı (19 Kasım karne 2,8K, 22 Kasım tatilin son akşamı 2,3K).
   - **Öğrenciye dönük olmayan genel motivasyon/alışkanlık videosu yok** (kitap, erteleme, telefon, pazartesi videoları
     YouTube'da 7–110 izlenmede kaldı). `plan/<tarih>.json` bu karışıma uymuyorsa planı **kullanma** (dosyayı silme) →
     adım 3'ten yeni içerik üret.
   Bu haftaki yayınlanmış + planlı videoları türe göre say. Kalan yayın günü sayısı ≤ eksik LGS kotası ise bugün **zorunlu LGS**.
   Aynı sınavı üst üste iki yayın gününde kullanma (kota zorunlu kılmadıkça). Sınav tarihlerini her seferinde ÖSYM/MEB
   kaynağından doğrula. Gündem (özel gün, tatil) LGS/YKS videosuna kanca olarak eklenebilir; tür yine LGS/YKS sayılır.
   **Süre 24–26 sn** (mümkünse): ~8–10 kısa cümle, ses ≈ 22–24 sn. Ses 24,5 sn'yi aşarsa metni kısalt ve TTS'i bir kez yeniden üret.
   Haftalık sayımı (LGS x/3 · YKS x/1 · okul gündemi x/2) ve YouTube kanal özetini adım 10'daki `insights.md` notuna ve rapora ekle.
2. **Plan var mı?** (2b izin veriyorsa) `plan/<YYYY-MM-DD>.json` varsa → `ELEVEN_API_KEY=... python3 tools/run_plan.py <tarih> --no-render`,
   `~/work/<tarih>/sheet.png`'ye **bak** (yazı taşması / çakışma yoksa) → `python3 tools/run_plan.py <tarih>` (render + yükleme) → adım 8.
   Plan yoksa adım 3'ten devam: **yeni içerik üret**.
3. **Gündem + fikir** (WebSearch, Türkçe): bugünün/haftanın Türkiye gündemi — sınav tarihleri (ÖSYM/MEB), özel günler,
   mevsim/ay başı-sonu, büyük spor olayları, viral konular. Gündemi **kanca** olarak kullan, motivasyon mesajına bağla.
   Siyaset, trajedi, kişiler hakkında iddia **yok**. Uygun gündem yoksa `IDEAS.md` havuzundan, 2b karışımına uyan bir fikir seç.
   Format karışımı adım 2b'deki haftalık karışımdır (LGS 3 · YKS/TYT 1 · okul gündemi 2). Simülasyon/veri ("günde X = Y"),
   kinetik tipografi ve "ya … olsaydı" senaryosu birer **anlatım biçimidir**; konu her zaman öğrenciye dönük kalır.
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
   YouTube başlığı: sınav videolarında sınav adı + gün sayısıyla başla ("LGS'ye N gün: <somut kazanç>"); en çok izlenen
   iki Short bu kalıpta. LGS videolarında etiketlere `lgs`, `lgs 2027`, `8. sınıf` ekle.
   **Aylık kota bitince: elle paylaşım modu** (Umut'un kararı, 24 Kasım 2026: ücretli plana geçilmeyecek, kota bitince
   Umut kendisi paylaşacak). Video her yayın günü yine **üretilir** (adım 1–8 aynen); yalnızca bu adım değişir:
   - Her gün önce Metricool'a planlamayı **bir kez** dene. Gönderi kabul edildiyse (yanıtta gönderi id'si var ve `media`
     metricool adresine dönmüş) normal akış.
   - Metricool aylık gönderi sınırı / plan hatası döndürürse **elle paylaşım moduna** geç. Tekrar deneme, metni değiştirip
     yeniden gönderme, başka bir yoldan yüklemeye çalışma. Bu bir hata değildir, beklenen durumdur.
   - Elle modda rapor (adım 12) ilk satırda **"BUGÜN ELLE PAYLAŞ"** yazar ve sırayla verir: (1) video indirme linki
     (`VIDEO_URL`; ertesi sabahki üretimde silinir, **aynı gün** indirilmeli), (2) YouTube Shorts başlığı, (3) açıklama +
     hashtagler tek blok hâlinde (Instagram Reel ve YouTube için aynı metin), (4) önerilen saat 07:00–09:00.
   - `posts.json` kaydına `"manual": true` ve `"metricool_ids": []` yaz. Haftalık karışım sayımında bu video da sayılır.
   - Ayın 1'inde kota yenilenir; her gün önce Metricool denendiği için normal akışa kendiliğinden dönülür.
   - Ertesi gün adım 1'de dünkü Metricool gönderisinin durumuna bak (`getScheduledPosts`, `providers[].status`):
     `PUBLISHED` değilse raporun başında uyar.
10. **İstatistik** (her gün kısa, pazar günleri detaylı): Metricool `getAnalyticsAvailableMetrics` (instagram/reels,
    youtube) → son 7 günün izlenme/erişim/kaydetme/paylaşım değerlerini çek; `insights.md`'ye tarihli kısa not düş
    (hangi format/kanca iyi gitti, ne değişecek). YouTube kanal izlenmesini ve abone sayısını da yaz (`YTEV01,YTEV02,YTEV05`).
    Format karışımını Instagram verisine göre **değiştirme**: karışım 2b'de sabittir ve yalnızca `insights.md`'ye yeni bir
    "YouTube video bazlı" not düşüldüğünde güncellenir.
11. **Kayıt**: `posts.json`'a ekle `{date, topic, format, hook, script, caption, yt_title, video_url, metricool_ids}` →
    `git add -A && git commit -m "<tarih> reels" && git push origin main` (yalnızca main; videolar main'e girmez).
12. **Rapor**: Son mesajda Türkçe 3–5 satır: konu, kanca, planlanan saat, Metricool linkleri, varsa sorun.
    Elle paylaşım modunda rapor adım 9'daki "BUGÜN ELLE PAYLAŞ" biçimiyle başlar (link, başlık, açıklama, saat).
    ElevenLabs kredisi 3.000'in altına düştüyse ya da bir adım başarısızsa bunu açıkça yaz. (Kredi `GET /v1/user/subscription`
    ile okunur; anahtarda `user_read` izni yoksa 401 döner → "kredi okunamadı" yaz, adımı atla.)

## Hata durumları
- TTS hata (402/401): anahtar/plan sorunu → rapor et, o gün dünkü değil **yedek plan**: `plan/` altında kullanılmamış bir
  plan varsa onu sessiz şablonla değil, yine seslendirmeli üretmeye çalış; olmazsa rapor et, paylaşım yapma.
- Metricool hata: hatayı olduğu gibi raporla, metni değiştirip tekrar deneme döngüsüne girme (en fazla 1 tekrar).
  Aylık gönderi sınırı hatası bunun dışındadır: tekrar deneme, adım 9'daki elle paylaşım moduna geç.
- Asla: gizli anahtarı depoya yazma, telifli müzik/görsel/söz kullanma, gerçek kişiler adına söz uydurma.
