# Ders 4 - Goruntu aritmetigi ve canli filigran (watermark)
# Once numpy toplama ile cv2.add farkini gosteriyor,
# sonra kamera goruntusunun uzerine yari saydam filigran basiyor.
# Calistirma (kok dizinden): python ders04.py

import os

import cv2
import numpy as np

# ---------- aritmetik tuzagi ----------
# tek pikselli iki "resim". uint8 = 0-255 arasi sayi (piksel tipi)
a = np.uint8([[250]])
b = np.uint8([[20]])

print("=" * 55)
print(" ARİTMETİK TUZAĞI")
print("=" * 55)
# numpy ile 250+20 = 14 cikiyor. 255'i gecince basa donuyor (270 - 256 = 14)
print("  NumPy   : 250 + 20 = " + str(int((a + b)[0][0])).rjust(3)
      + "   <- TAŞTI, başa döndü!")
# cv2.add ise 255'te durduruyor (doyma). resim parlatirken beyazlar siyaha donmuyor
print("  cv2.add : 250 + 20 = " + str(int(cv2.add(a, b)[0][0])).rjust(3)
      + "   <- DOYDU, 255'te kaldı")
print("\n  Kural: Görüntü aritmetiğinde cv2.add / cv2.subtract kullanın.\n")


# filigran katmani: siyah zemin + alt serit + yazilar
# siyah kisimlar addWeighted'da kareyi degistirmiyor, sadece yazilar gorunuyor
def filigran_uret(genislik, yukseklik):
    kat = np.zeros((yukseklik, genislik, 3), dtype=np.uint8)  # simsiyah resim

    # en alta 46 px yuksekliginde koyu serit (-1 = ici dolu)
    cv2.rectangle(kat, (0, yukseklik - 46), (genislik, yukseklik),
                  (40, 20, 10), -1)
    # putText turkce karakter basamiyor, o yuzden i/o kullandim
    # konum yazinin sol ALT kosesi
    cv2.putText(kat, "IYC Tech Workshop  |  Bilgisayarli Goru",
                (12, yukseklik - 16), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 220, 120), 2)
    # sag ustte isim. genislik - 230 yazinca resim boyutu degisse de sagda kaliyor
    cv2.putText(kat, "Furkan Demirci", (genislik - 230, 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (120, 220, 255), 2)
    cv2.line(kat, (genislik - 232, 44), (genislik - 40, 44),
             (120, 220, 255), 2)  # ismin alt cizgisi
    return kat


def canli_filigran(kaynak=0):
    # 0 = bilgisayarin kamerasi. acilmazsa video dosyasini deniyor
    kap = cv2.VideoCapture(kaynak)
    if not kap.isOpened():
        print("[!] Kamera açılamadı. Video dosyası deneniyor...")
        kap = cv2.VideoCapture("video/ornek.mp4")
        if not kap.isOpened():
            print("[!] Görüntü kaynağı bulunamadı.")
            return

    # ilk kareyi sadece boyutu ogrenmek icin okuyorum
    ok, kare = kap.read()
    if not ok:
        print("[!] Kare okunamadı.")
        kap.release()
        return

    kare = cv2.resize(kare, (640, 480))
    h, w = kare.shape[:2]
    filigran = filigran_uret(w, h)  # bir kere uretiliyor, her karede tekrar degil

    saydamlik = 0.65  # filigranin ne kadar belirgin oldugu (0-1)
    parlaklik = 0     # -100 ile +100 arasi

    print("""
    ------------------------------------------------------
     KONTROLLER
       + / -   : filigran saydamlığı
       w / s   : parlaklık artır / azalt  (cv2.add)
       k       : kareyi 'ciktilar/' klasörüne kaydet
       q       : çık
    ------------------------------------------------------
    """)

    sayac = 0
    while True:
        ok, kare = kap.read()
        if not ok:
            # video bittiyse basa sar
            kap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # filigranla ayni boyutta olmasi lazim yoksa addWeighted hata veriyor
        kare = cv2.resize(kare, (w, h))
        if kaynak == 0:
            kare = cv2.flip(kare, 1)  # kamerada ayna gibi gorunsun diye

        # parlaklik: her pikseli ayni sayi olan bir resim yapip cv2.add / subtract
        if parlaklik != 0:
            sabit = np.full(kare.shape, abs(parlaklik), dtype=np.uint8)
            kare = cv2.add(kare, sabit) if parlaklik > 0 \
                else cv2.subtract(kare, sabit)

        # sonuc = kare * 1.0 + filigran * saydamlik + 0
        sonuc = cv2.addWeighted(kare, 1.0, filigran, saydamlik, 0)

        # sol ustte anlik degerler (.2f = 2 ondalik, +d = isaretli sayi)
        cv2.putText(sonuc, "saydamlik=" + format(saydamlik, ".2f")
                    + "  parlaklik=" + format(parlaklik, "+d"),
                    (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

        cv2.imshow("Ders 4 - Canli Filigran", sonuc)

        # tus kontrolu. min/max ile degerlerin sinir disina cikmasini engelliyorum
        tus = cv2.waitKey(1) & 0xFF
        if tus == ord("q"):
            break
        elif tus in (ord("+"), ord("=")):  # = da olsun, shift'e basmadan calissin
            saydamlik = min(1.0, saydamlik + 0.05)
        elif tus == ord("-"):
            saydamlik = max(0.0, saydamlik - 0.05)
        elif tus == ord("w"):
            parlaklik = min(100, parlaklik + 5)
        elif tus == ord("s"):
            parlaklik = max(-100, parlaklik - 5)
        elif tus == ord("k"):
            os.makedirs("ciktilar", exist_ok=True)  # klasor yoksa olusturuyor
            ad = "ciktilar/filigranli_" + str(sayac).zfill(3) + ".jpg"  # 000, 001...
            cv2.imwrite(ad, sonuc)
            print("  [✓] Kaydedildi: " + ad)
            sayac += 1

    kap.release()  # kamerayi birakmazsam mesgul kaliyor
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    canli_filigran(0)
