# Ders 3 - ROI secimi, dondurme ve dijital zoom
# Bir resim uzerinde 4 islem yapip hepsini tek pencerede 2x2 panel olarak gosteriyor.
# Calistirma (kok dizinden): python ders03.py

import cv2
import numpy as np


# resim bulunamazsa kullanilacak yedek gorsel (izgara + dikdortgen + daire)
def test_gorseli():
    g = np.full((360, 480, 3), 25, dtype=np.uint8)  # 480x360 koyu gri zemin
    # 40 pikselde bir dikey ve yatay cizgi -> izgara
    for i in range(0, 480, 40):
        cv2.line(g, (i, 0), (i, 360), (60, 60, 60), 1)
    for i in range(0, 360, 40):
        cv2.line(g, (0, i), (480, i), (60, 60, 60), 1)
    cv2.rectangle(g, (140, 100), (340, 260), (0, 140, 255), -1)  # turuncu, -1 = ici dolu
    cv2.circle(g, (240, 180), 55, (230, 60, 60), -1)              # ortada mavi daire
    cv2.putText(g, "ROI", (196, 192), cv2.FONT_HERSHEY_SIMPLEX,
                1.1, (255, 255, 255), 3)
    return g


# resmi oku, yoksa yedek gorseli kullan (imread hata vermiyor, None donuyor)
gorsel = cv2.imread("resim/ornek.jpg")
if gorsel is None:
    gorsel = test_gorseli()
gorsel = cv2.resize(gorsel, (480, 360))  # resize (genislik, yukseklik) aliyor
h, w = gorsel.shape[:2]                  # shape ise (yukseklik, genislik) veriyor, ters!

# ---------- 1) ROI (ilgi alani) ----------
# ROI = resmin sadece bir parcasi. numpy dilimleme ile aliniyor: [y1:y2, x1:x2]
# dikkat: once y (satir) sonra x (sutun)
x1, y1, x2, y2 = 120, 80, 360, 280
roi = gorsel[y1:y2, x1:x2]

# ROI'yi gostermek icin kopya uzerine yesil cerceve ciziyorum
# (copy yapmazsam orijinal resim de degisiyor)
roi_gosterim = gorsel.copy()
cv2.rectangle(roi_gosterim, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.putText(roi_gosterim, "ROI", (x1, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

print("Orijinal boyut :", gorsel.shape)
print("ROI boyutu     :", roi.shape)   # 200 x 240 cikmali

# ---------- 2) sadece ROI'yi bulaniklastirma ----------
# resmin tamami degil sadece secilen alan bulaniklasiyor (yuz/plaka kapatma mantigi)
# (51, 51) bulaniklik penceresi, tek sayi olmak zorunda, buyudukce daha bulanik
roi_islenmis = gorsel.copy()
roi_islenmis[y1:y2, x1:x2] = cv2.GaussianBlur(
    roi_islenmis[y1:y2, x1:x2], (51, 51), 0)

# ---------- 3) dondurme ----------
merkez = (w // 2, h // 2)  # resmin ortasi etrafinda donecek
ACI = 30                   # derece, pozitif = saat yonunun tersi
OLCEK = 1.0                # 1.0 = boyut ayni kalsin

# once donusum matrisi hesaplaniyor, sonra warpAffine ile resme uygulaniyor
M = cv2.getRotationMatrix2D(merkez, ACI, OLCEK)
dondurulmus = cv2.warpAffine(gorsel, M, (w, h),
                             borderValue=(20, 20, 20))  # kosede bos kalan yerlerin rengi
cv2.putText(dondurulmus, str(ACI) + " derece", (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)


# ---------- 4) dijital zoom ----------
# ortadan kucuk bir parca kesip tekrar eski boyuta buyutuyor
# kat=2 ise genislik ve yuksekligin yarisi kadar parca aliniyor
def dijital_zoom(kare, kat=2.0):
    yuk, gen = kare.shape[:2]
    yeni_g, yeni_y = int(gen / kat), int(yuk / kat)
    x0 = (gen - yeni_g) // 2   # kesilecek parcanin sol ust kosesi (ortalamak icin)
    y0 = (yuk - yeni_y) // 2
    kirpik = kare[y0:y0 + yeni_y, x0:x0 + yeni_g]
    # INTER_LINEAR = buyuturken pikseller arasini yumusak dolduruyor
    return cv2.resize(kirpik, (gen, yuk), interpolation=cv2.INTER_LINEAR)


zoomlu = dijital_zoom(gorsel, 2.0)
cv2.putText(zoomlu, "2x dijital zoom", (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

# ---------- 4 resmi birlestirme ----------
# hstack = yan yana, vstack = alt alta (boyutlari ayni olmali)
ust = np.hstack([roi_gosterim, roi_islenmis])
alt = np.hstack([dondurulmus, zoomlu])
panel = np.vstack([ust, alt])

# her parcanin altina baslik. w ve h ekleyerek diger kutulara kaydiriyorum
for metin, konum in [("1. ROI secimi", (10, h - 12)),
                     ("2. Sadece ROI bulanik", (w + 10, h - 12)),
                     ("3. Dondurme", (10, 2 * h - 12)),
                     ("4. Dijital zoom", (w + 10, 2 * h - 12))]:
    cv2.putText(panel, metin, konum, cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 2)

cv2.imshow("Ders 3 - ROI, Dondurme, Zoom", panel)
print("\n[i] Kapatmak için herhangi bir tuşa basın.")
cv2.waitKey(0)           # 0 = tusa basilana kadar bekle
cv2.destroyAllWindows()
cv2.waitKey(1)           # mac'te pencere kapanmayinca bunu ekledim
