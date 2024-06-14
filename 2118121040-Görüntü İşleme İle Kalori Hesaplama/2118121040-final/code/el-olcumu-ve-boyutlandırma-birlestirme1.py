# -*- coding: utf-8 -*-
"""
Created on Sat May 18 10:25:42 2024

@author: Melisa
"""

import cv2
import cvzone
import mediapipe as mp
import numpy as np
import math
from ultralytics import YOLO

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand_connections = [(4, 4), (8, 8), (12, 12), (16, 16), (20, 20)]

# YOLO modelini başlat
model = YOLO(r'C:\Users\Melisa\Desktop\egitilmis-model-ile-boyut-bulma\yolo-test\model\best.pt')
cap = cv2.VideoCapture(0)

def main():
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    hand_landmark_drawing_spec = mp_drawing.DrawingSpec(color=(121, 22, 6), thickness=5, circle_radius=0)
    hand_connection_drawing_spec = mp_drawing.DrawingSpec(color=(250, 44, 90), thickness=15, circle_radius=15)

    while cap.isOpened():
        ret, img = cap.read()

        if not ret:
            break

        img = cv2.resize(img, (640, 480))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results_hand = hands.process(img_rgb)
        results = model(img, stream=True)

        # Nesne tanıma ve kutu çizme işlemleri
        try:
            for r in results:
                boxes = r.boxes
                names = r.names
                for box in boxes:
                    variable = names[int(box.cls)]
                    confidence = box.conf[0] * 100  # Güven oranını yüzde olarak hesapla
                    
                    if confidence > 40: 
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                        # Kutu boyutlarını hesapla
                        genislik = x2 - x1
                        yukseklik = y2 - y1

                        # Metni resme yazdır
                        boyut_metni = f"{genislik}x{yukseklik} px"
                        cv2.putText(img, f"{genislik}px, {yukseklik}px, {confidence:.2f}%", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                        cvzone.putTextRect(img, variable, (x1, y2 + 20), scale=0.8, thickness=2, colorR=(255, 0, 255))

                        print(f'Class: {variable}, Confidence: {confidence:.2f}%')

                        with open("names_file1.txt", "a") as isimler_dosyasi:
                            isimler_dosyasi.write(f"{genislik} px genislik, {yukseklik} px yukseklik, {variable},oran:{confidence:.2f}%\n")

        except cv2.error as e:
            print(f"OpenCV error: {e}")

        # El takibi işlemleri
        if results_hand.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results_hand.multi_hand_landmarks):
                if idx == 0:  # Sağ el
                    x1, y1 = int(hand_landmarks.landmark[8].x * img.shape[1]), int(hand_landmarks.landmark[8].y * img.shape[0])
                    x2, y2 = int(hand_landmarks.landmark[5].x * img.shape[1]), int(hand_landmarks.landmark[5].y * img.shape[0])
                    cv2.circle(img, (x1, y1), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.circle(img, (x2, y2), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 128), 3)
                    right_distance2 = math.hypot(x2 - x1, y2 - y1)

                    x3, y3 = int(hand_landmarks.landmark[8].x * img.shape[1]), int(hand_landmarks.landmark[8].y * img.shape[0])
                    x4, y4 = int(hand_landmarks.landmark[6].x * img.shape[1]), int(hand_landmarks.landmark[6].y * img.shape[0])
                    cv2.circle(img, (x3, y3), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.circle(img, (x4, y4), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.line(img, (x3, y3), (x4, y4), (255, 0, 128), 3)
                    right_distance1 = math.hypot(x4 - x3, y2 - y4)

                    # Metnin başlama noktasını ayarla
                    text_x = x1 + 30
                    text_y = y1
                    cv2.putText(img, "{:.2f}".format(float(right_distance1 / right_distance2)), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)

                elif idx == 1:  # Sol el
                    x1, y1 = int(hand_landmarks.landmark[8].x * img.shape[1]), int(hand_landmarks.landmark[8].y * img.shape[0])
                    x2, y2 = int(hand_landmarks.landmark[5].x * img.shape[1]), int(hand_landmarks.landmark[5].y * img.shape[0])
                    cv2.circle(img, (x1, y1), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.circle(img, (x2, y2), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 128), 3)
                    left_distance2 = math.hypot(x2 - x1, y2 - y1)

                    x3, y3 = int(hand_landmarks.landmark[8].x * img.shape[1]), int(hand_landmarks.landmark[8].y * img.shape[0])
                    x4, y4 = int(hand_landmarks.landmark[6].x * img.shape[1]), int(hand_landmarks.landmark[6].y * img.shape[0])
                    cv2.circle(img, (x3, y3), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.circle(img, (x4, y4), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.line(img, (x3, y3), (x4, y4), (255, 0, 128), 3)
                    left_distance1 = math.hypot(x4 - x3, y2 - y4)

                    # Metnin başlama noktasını ayarla
                    text_x = x1 + 30
                    text_y = y1
                    cv2.putText(img, "{:.2f}".format(float(left_distance1 / left_distance2)), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)

                # Tüm parmak uçlarına daire çizme işlemi
                for i in range(5):
                    landmark = hand_landmarks.landmark[mp_hands.HandLandmark(i * 4 + 4)]
                    center_coordinates = (int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]))
                    cv2.circle(img, center_coordinates, 15, (0, 0, 255), 5)

        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


