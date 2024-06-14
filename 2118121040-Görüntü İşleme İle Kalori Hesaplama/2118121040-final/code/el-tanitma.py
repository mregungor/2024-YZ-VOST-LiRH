# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 18:50:20 2024

@author: Melisa
"""

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def distance(lm1, lm2):
    return ((lm1.x - lm2.x) ** 2) + ((lm1.y - lm2.y) ** 2) ** 0.5

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_tracking_confidence=0.5,
    min_detection_confidence=0.5,
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Kamera okunamıyor!")
            break
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)     

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())
                # Eldeki ilk ve orta parmak arasındaki mesafeyi hesapla
                dist = distance(hand_landmarks.landmark[0], hand_landmarks.landmark[12])
                dist2 = distance(hand_landmarks.landmark[3], hand_landmarks.landmark[17])
                # Mesafeyi ekrana yazdır
                cv2.putText(image, f"Uzunluk: {dist:.2f} piksel", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                cv2.putText(image, f"Genislik: {dist2:.2f} piksel", (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Result", image)
        if cv2.waitKey(5) & 0xFF == 27:  # ESC tuşuna basıldığında döngüden çık
            break

cap.release()
cv2.destroyAllWindows()

