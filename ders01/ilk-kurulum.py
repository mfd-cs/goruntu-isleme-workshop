import sys
import cv2
import numpy as np
import matplotlib
import PIL

print("=" * 60)
print("2026 GÖRÜNTÜ İŞLEME WORKSHOP - ORTAM KURULUMU BAŞARILI!")
print("=" * 60)

# Sürüm Bilgileri
print("Python Sürümü      :", sys.version.split()[0])
print("OpenCV Sürümü      :", cv2.__version__)
print("NumPy Sürümü       :", np.__version__)
print("Matplotlib Sürümü  :", matplotlib.__version__)
print("Pillow (PIL) Sürümü:", PIL.__version__)

print("-" * 60)
# @danismanliogrenme Sosyal Medya & Workshop Bilgileri
print("Takip ve İçerikler için:")
print("YouTube   : @danismanliogrenme (youtube.com/@danismanliogrenme)")
print("Instagram : @danismanliogrenme (instagram.com/danismanliogrenme)")
print("=" * 60)

# Görsel Oluşturma ve Test (300x400 Piksel RGB Tuval)
img = np.zeros((300, 400, 3), dtype=np.uint8)

# Tuval üzerine test metni ve daire ekleme
cv2.circle(img, (200, 150), 60, (0, 255, 0), -1)  # Yeşil Daire
cv2.putText(
    img,
    "@danismanliogrenme 2026",
    (50, 260),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2,
)

# Pencerede Gösterme
cv2.imshow("Goruntu isleme Workshop @2026", img)
print("\n💡 Ekrana test penceresi açıldı. Kapatmak için pencere seçiliyken bir tuşa basın...")

cv2.waitKey(0)
cv2.destroyAllWindows()