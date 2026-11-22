import cv2  # OpenCV lib
import numpy as np  # artik adini np yaptik


def resim_alma():
    YOL = "resim/renk.gif"
    gorsel = cv2.imread(YOL)

    if gorsel is None:
        print("Gorsel Dosyasi Bos.")
        gorsel = np.zeros((300, 400, 3), dtype=np.uint8)
        cv2.rectangle(gorsel, (50, 50), (350, 250), (0, 165, 255), -1)  # turuncu
        cv2.circle(gorsel, (200, 150), 60, (255, 0, 0))  # mavi

    # resmin kunyesini elde etme
    yukseklik, genislik, kanal = gorsel.shape
    print("Gorselin Boyutlari", gorsel.shape)
    print("Gorselin Yuksekligi", yukseklik)
    print("Gorselin Genisligi", genislik)
    print("Gorselin Kanal", kanal)

    cv2.imshow("1. Gorsel", gorsel)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def video_alma():
    print("Video fonk basladi")
    YOL = "video/ornek.mp4"
    video = cv2.VideoCapture(YOL)
    if not video.isOpened():
        print("Video Acilamadi:", YOL)
        return

    fps = video.get(cv2.CAP_PROP_FPS)
    bekleme = int(1000 / fps) if fps > 0 else 25  # videoyu gercek hizinda oynat

    while True:
        ok, kare = video.read()
        if not ok:  # video bitti
            break
        kare = cv2.resize(kare, (400, 300))
        cv2.imshow("Video Oynatiliyor", kare)

        if cv2.waitKey(bekleme) & 0xFF == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()


def kamera_alma():
    print("Kamera fonk basladi")
    kamera = cv2.VideoCapture(0)  # sabit cam 0, port port artiyor
    if not kamera.isOpened():
        print("Kamera Calismadi")
        return

    while True:
        ok, kare = kamera.read()
        if not ok:
            break
        kare = cv2.resize(kare, (400, 300))
        kare = cv2.flip(kare, 1)
        cv2.imshow("Kamera Calisiyor", kare)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    kamera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Goruntu Isleme Workshop ---> Resim Video Kamera Uygulamasi")
    resim_alma()
    video_alma()
    kamera_alma()
