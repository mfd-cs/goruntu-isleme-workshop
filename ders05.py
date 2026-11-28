# Ders 5 - Canny kenar bulma ve islenmis videoyu dosyaya kaydetme
# Kameradan gelen her karede kenarlari bulup yesil olarak ciziyor,
# sonucu 10 saniye boyunca mp4 dosyasina yaziyor.
# Calistirma (kok dizinden): python ders05.py

import os

import cv2
import numpy as np


# tek bir kareyi isleyen fonksiyon: kenarlari bul, yesile boya, ustune bindir
def islem_uygula(kare):
    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)  # kenar icin renk gerekmiyor, griye cevirdim
    gri = cv2.GaussianBlur(gri, (5, 5), 0)        # once hafif bulanik -> gurultu sahte kenar olmasin
    kenar = cv2.Canny(gri, 80, 160)               # 80 alt esik, 160 ust esik. sonuc: kenarlar beyaz

    # kare ile ayni boyutta siyah resim, sadece yesil kanala (1) kenarlari koyuyorum
    # BGR -> 0 mavi, 1 yesil, 2 kirmizi
    renkli_kenar = np.zeros_like(kare)
    renkli_kenar[:, :, 1] = kenar

    # orijinal %85 + yesil kenarlar %90
    return cv2.addWeighted(kare, 0.85, renkli_kenar, 0.9, 0)


def kaydet(kaynak=0, sure_sn=10, cikti="ciktilar/islenmis_video.mp4"):
    kap = cv2.VideoCapture(kaynak)
    if not kap.isOpened():
        print("[!] Kaynak açılamadı, video dosyası deneniyor...")
        kap = cv2.VideoCapture("video/ornek.mp4")
        if not kap.isOpened():
            print("[!] Hiçbir görüntü kaynağı bulunamadı.")
            return

    # kameraya boyutunu ve fps'ini soruyorum (kaydedici bunlari bilmek zorunda)
    genislik = int(kap.get(cv2.CAP_PROP_FRAME_WIDTH))
    yukseklik = int(kap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = kap.get(cv2.CAP_PROP_FPS)
    # bazi kameralar (mac'te oluyor) fps'i 0 donduruyor, o zaman 20 kabul ediyorum
    # fps yanlis olursa video hizli ya da agir cekim gibi oynuyor
    if not fps or fps <= 1:
        fps = 20.0

    os.makedirs(os.path.dirname(cikti), exist_ok=True)  # ciktilar/ klasoru yoksa olustur

    # VideoWriter = kareleri dosyaya yazan nesne
    # fourcc = video sikistirma formati, mp4v -> .mp4
    kodek = cv2.VideoWriter_fourcc(*"mp4v")
    yazici = cv2.VideoWriter(cikti, kodek, fps, (genislik, yukseklik))  # boyut kamerayla ayni olmali

    if not yazici.isOpened():
        print("[!] Yazıcı açılamadı. 'XVID' + .avi deneyin.")
        kap.release()
        return

    hedef_kare = int(fps * sure_sn)  # 20 fps x 10 sn = 200 kare
    print("\n    ------------------------------------------------------\n"
          + "     KAYIT BAŞLIYOR\n"
          + "       Çözünürlük : " + str(genislik) + " x " + str(yukseklik) + "\n"
          + "       FPS        : " + format(fps, ".1f") + "\n"
          + "       Süre       : ~" + str(sure_sn) + " sn  ("
          + str(hedef_kare) + " kare)\n"
          + "       Dosya      : " + cikti + "\n"
          + "       'q' ile erken bitirebilirsiniz.\n"
          + "    ------------------------------------------------------\n")

    sayac = 0
    # sonsuz dongu yerine hedef kare sayisina kadar donuyor
    while sayac < hedef_kare:
        ok, kare = kap.read()
        if not ok:
            break

        islenmis = islem_uygula(kare)

        # sag ustte kirmizi nokta + REC yazisi (kayit gorunumu)
        cv2.circle(islenmis, (genislik - 34, 30), 10, (0, 0, 255), -1)
        cv2.putText(islenmis, "REC", (genislik - 100, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        yazici.write(islenmis)  # kareyi videoya ekle
        sayac += 1

        # terminalde ilerleme cubugu. \r = satir basina don, ayni satira yaz
        oran = sayac / hedef_kare
        dolu = int(oran * 30)
        print("\r  [" + "#" * dolu + "." * (30 - dolu) + "] "
              + format(oran * 100, "5.1f") + "%",
              end="", flush=True)

        cv2.imshow("Kayit ediliyor... ('q' ile bitir)", islenmis)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # yaziciyi release etmezsem video dosyasi bozuk/acilmaz oluyor
    kap.release()
    yazici.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    boyut_mb = os.path.getsize(cikti) / (1024 * 1024)  # byte -> MB
    print("\n\n  [✓] Tamamlandı: " + cikti + "  ("
          + format(boyut_mb, ".2f") + " MB, " + str(sayac) + " kare)")


if __name__ == "__main__":
    kaydet(kaynak=0, sure_sn=10)
