# Görüntü İşleme Workshop

**OpenCV ile Bilgisayarlı Görü Uygulamaları — Veriyi İşle, Geleceği Kodla** workshop'unda (İYC Tech Workshop Serisi, eğitmen: Ali Çetinkaya) yazdığım kodlar.

## Kurulum

Python 3.12+ ve [uv](https://github.com/astral-sh/uv) gerekiyor.

```bash
git clone https://github.com/mfd-cs/goruntu-isleme-workshop.git
cd goruntu-isleme-workshop
uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

Kodlar **kök dizinden** çalıştırılır:

```bash
python ders04.py
```

## Klasör yapısı

```
goruntu-isleme-workshop/
├── ilk-kurulum.py      # kurulum testi
├── ders01.py           # görsel okuma
├── ders02.py           # resim / kamera / video fonksiyonları
├── ders03.py           # ROI, döndürme, dijital zoom
├── ders04.py           # görüntü aritmetiği + canlı filigran
├── ders05.py           # Canny kenar bulma + video kaydı
├── resim/              # örnek görseller
├── video/              # örnek videolar (repoya eklenmiyor)
└── requirements.txt
```

---

## ilk-kurulum.py — Kurulum testi
Kütüphane sürümlerini yazdırır, siyah bir tuvale daire ve yazı çizip gösterir. Kurulum doğru mu diye kontrol etmek için.

## ders01.py — Görsel okuma
- `cv2.imread` ile resim okur. Dosya yoksa `None` döner; o durumda kod kendi yedek görselini çizer.
- `shape` ile boyut bilgisini yazdırır (yükseklik, genişlik, kanal).
- `cv2.rectangle`, `cv2.circle` ile çizim.

## ders02.py — Resim, kamera ve video
- Kod fonksiyonlara bölündü: `resim_alma()`, `kamera_alma()`, `video_alma()`.
- Kamera ve video aynı döngüyle okunur (`VideoCapture` → `read` → `imshow`).
- Çıkmak için `q`.

## ders03.py — ROI, döndürme, dijital zoom
Tek bir resim üzerinde 4 işlem yapıp 2×2 panelde gösterir:
1. **ROI seçimi:** resmin bir parçasını dilimleme ile alma (`gorsel[y1:y2, x1:x2]`)
2. **Sadece ROI'yi bulanıklaştırma:** yüz/plaka kapatma mantığı
3. **Döndürme:** `getRotationMatrix2D` + `warpAffine`
4. **Dijital zoom:** ortadan kırpıp eski boyuta büyütme

Kapatmak için herhangi bir tuş.

## ders04.py — Görüntü aritmetiği ve canlı filigran
- **Aritmetik tuzağı:** NumPy ile `250 + 20 = 14` (taşma), `cv2.add` ile `255` (doyma). Görüntüde toplama/çıkarma için `cv2.add` / `cv2.subtract` kullanılmalı.
- Kamera görüntüsünün üzerine `cv2.addWeighted` ile yarı saydam filigran basar.

| Tuş | İşlev |
|---|---|
| `+` / `-` | filigran saydamlığı |
| `w` / `s` | parlaklık artır / azalt |
| `k` | kareyi `ciktilar/` klasörüne kaydet |
| `q` | çık |

## ders05.py — Kenar bulma ve video kaydı
- Her karede: gri → Gaussian bulanıklaştırma → **Canny** kenar bulma → kenarları yeşile boyayıp görüntünün üstüne bindirme.
- İşlenmiş görüntüyü `VideoWriter` ile 10 saniye boyunca `ciktilar/islenmis_video.mp4` dosyasına kaydeder.
- Terminalde ilerleme çubuğu gösterir. Erken bitirmek için `q`.

---

## Notlar
- Kamera açılmazsa kodlar `video/ornek.mp4` dosyasını dener.
- `cv2.putText` Türkçe karakter basamadığı için ekrandaki yazılar Türkçe karaktersiz.
- Mac'te kamera izni: Sistem Ayarları → Gizlilik ve Güvenlik → Kamera → Terminal / VS Code.
