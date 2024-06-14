# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:38:43 2024

@author: Melisa
"""

import cv2

# Resmi yükle
image = cv2.imread(r"C:/Users/Melisa/Desktop/Data-1/domates-10.jpg")

# Resmin yeni boyutlarını hesapla
new_width = int(image.shape[1] * 0.20)
new_height = int(image.shape[0] * 0.20)

# Resmi yeni boyutlara dönüştür
resized_image = cv2.resize(image, (new_width, new_height))

# Gri tonlama
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Kenar tespiti
edges = cv2.Canny(gray, 50, 150)

# Konturları bul
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# En dış çizim bulunuyor
external_contour = max(contours, key=cv2.contourArea)

# Alanı hesapla ve yazdır
area = cv2.contourArea(external_contour)
print(f"Dış Çizime Göre Alan: {area} piksel kare")

# Alanı resme yazdır
text = f"{area} px"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_thickness = 1
text_color = (0, 0, 255)  # Kırmızı renk (BGR formatında)
text_position = (10, 30)   # Sol üst köşe
cv2.putText(resized_image, text, text_position, font, font_scale, text_color, font_thickness)

# Sonuçları görselleştir
cv2.drawContours(resized_image, [external_contour], -1, (0, 255, 0), 2)
cv2.imshow("Round Objects", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

