# -*- coding: utf-8 -*-
"""
Created on Sat May 11 21:14:13 2024

@author: Melisa
"""

import cv2
from ultralytics import YOLO

model = YOLO(r'C:\Users\Melisa\Desktop\egitilmis-model-ile-boyut-bulma\yolo-test\model\best.pt')
cap = cv2.VideoCapture(r'C:/Users/Melisa/Desktop/Data-1/elma-5.jpg')

while cap.isOpened():
    ret, img = cap.read()
    if ret:
        img = cv2.resize(img, (640, 480))
        results = model(img, stream=True)

        try:
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    
                    # Kutu boyutlarını hesapla
                    genislik = x2 - x1
                    yukseklik = y2 - y1
                    
                    # Yazılacak metni oluştur
                    boyut_metni = f"{genislik}x{yukseklik} px"
                    
                    # Metni yazacağımız pozisyonu belirle
                    text_x = x1
                    text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20 # Kenardan taşma kontrolü
                    
                    # Metni resme yazdır
                    cv2.putText(img, boyut_metni, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
                    
                 
                 
            cv2.imshow('img', img)
            a = cv2.waitKey()
            if a == ord('q'):
                break

        except cv2.error:
            print("Error")

cap.release()
cv2.destroyAllWindows()
