import cv2 # OpenCV lib
import numpy as np #artik adini np yaptik

YOL = "resim/renk2.gif"

gorsel = cv2.imread(YOL)

if gorsel is None:
	print("Gorsel Dosyasi Bos.")
	gorsel = np.zeros((300, 400, 3),dtype=np.uint8)
	cv2.rectangle(gorsel, (50, 50), (350, 250), (0, 165, 255), -1)#turuncu
	cv2.circle(gorsel, (200, 150), 60, (255, 0, 0))#mavi

#resmin kunyesini elde etme

yukseklik, genislik, kanal = gorsel.shape

print("Gorselin Boyutlari", gorsel.shape)
print("Gorselin Yuksekligi", yukseklik)
print("Gorselin Genisligi", genislik)
print("Gorselin Kanal", kanal)

cv2.imshow("1. Gorsel", gorsel)
cv2.waitKey(0)
cv2.destroyAllWindows()
