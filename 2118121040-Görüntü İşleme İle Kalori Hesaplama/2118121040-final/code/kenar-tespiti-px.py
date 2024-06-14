# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 20:45:47 2024

@author: Melisa
"""
import cv2
import numpy as np

# Resmi yükle
image = cv2.imread(r'C:/Users/Melisa/Desktop/boyut-bulma-verisi/avakado-15.jpg')

# Resmin boyutlarını belirle
new_width = int(image.shape[1] * 0.20)  # Dörtte bir boyutuna küçült
new_height = int(image.shape[0] * 0.20)

# Resmi yeni boyutlara dönüştür
resized_image = cv2.resize(image, (new_width, new_height))

# Gri tonlamaya dönüştürme
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Gürültüyü azaltmak için bulanıklaştırma uygula
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Kenar tespiti
edges = cv2.Canny(blurred, 50, 150)

# Kapalı bölgeleri doldurma
filled_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)))

# Konturları bulma
contours, _ = cv2.findContours(filled_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# En büyük konturu seçme
largest_contour = max(contours, key=cv2.contourArea)

# Konturun etrafına bir dikdörtgen çizme
x, y, w, h = cv2.boundingRect(largest_contour)

# Dikdörtgenin boyutlarına göre bir eşik değeri belirleme
threshold = 0  # Dikdörtgen boyutlarının yüzde 10'u kadar ek bir pay bırak

# Yeni dikdörtgen koordinatlarını hesaplama
w_new = min(resized_image.shape[1] - 1, x + w + int(w * threshold)) - x
h_new = min(resized_image.shape[0] - 1, y + h + int(h * threshold)) - y

# Yeni dikdörtgeni çizme
cv2.rectangle(resized_image, (x, y), (x + w_new, y + h_new), (0, 255, 0), 2)

# Dikdörtgenin genişliğini ve uzunluğunu piksel olarak hesaplama
genislik = w_new
uzunluk = h_new

# Genişlik ve uzunluğu dikdörtgenin yanına ve üstüne yazdırma
cv2.putText(resized_image, f"G: {genislik} px (Ust)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
cv2.putText(resized_image, f"U: {uzunluk} px (Yan)", (x + w_new + 10, y + h_new // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Sonucu gösterme
cv2.imshow("Bounding Box", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
