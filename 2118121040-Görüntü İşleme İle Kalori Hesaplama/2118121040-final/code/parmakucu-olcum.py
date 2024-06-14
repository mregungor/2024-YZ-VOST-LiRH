# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:59:59 2024

@author: Melisa
"""

import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import math

mp_drawing = mp.solutions.drawing_utils
drawSpecific = mp.solutions.hands
mp_hands = mp.solutions.hands
handConnection = [(4, 4), (8, 8), (12, 12), (16, 16), (20, 20)]

cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Genişlik
cap.set(4, 1080) # Yükseklik
mp_drawing_styles = mp.solutions.drawing_styles

def main():
    hands = mp_hands.Hands(min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)
    hand_landmark_drawing_spec = mp_drawing.DrawingSpec(color=(121, 22,
            6), thickness=5, circle_radius=0)
    hand_connection_drawing_spec = mp_drawing.DrawingSpec(color=(250,
            44, 90), thickness=15, circle_radius=15)

    while cap.isOpened():
        ret, image = cap.read()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape

        results_hand = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        right_distance = None
        left_distance = None

        if results_hand.multi_hand_landmarks:
            for (idx, hand_landmarks) in enumerate(results_hand.multi_hand_landmarks):
                color = (0xFF, 0, 0)

                # Sağ elin uç parmaklarını al
                if idx == 0:
                    x1, y1 = int(hand_landmarks.landmark[8].x * image_width), int(hand_landmarks.landmark[8].y * image_height)
                    x2, y2 = int(hand_landmarks.landmark[7].x * image_width), int(hand_landmarks.landmark[7].y * image_height)
                    cv2.circle(image, (x1, y1), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.circle(image, (x2, y2), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 128), 3)
                    right_distance = math.hypot(x2 - x1, y2 - y1)
                    cv2.putText(image, str(int(right_distance)), (x1 + 30, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)
                # Sol elin uç parmaklarını al
                elif idx == 1:
                    x1, y1 = int(hand_landmarks.landmark[8].x * image_width), int(hand_landmarks.landmark[8].y * image_height)
                    x2, y2 = int(hand_landmarks.landmark[7].x * image_width), int(hand_landmarks.landmark[7].y * image_height)
                    cv2.circle(image, (x1, y1), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.circle(image, (x2, y2), 10, (255, 0, 128), cv2.FILLED) 
                    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 128), 3)
                    left_distance = math.hypot(x2 - x1, y2 - y1)
                    cv2.putText(image, str(int(left_distance)), (x1 + 30, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)


       

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    hands.close()
    cap.release()

main()
