# -*- coding: utf-8 -*-
"""
Created on Sun May 19 13:49:05 2024

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
cap.set(3, 1280)  # Genişlik
cap.set(4, 1080)  # Yükseklik
mp_drawing_styles = mp.solutions.drawing_styles

def main():
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    hand_landmark_drawing_spec = mp_drawing.DrawingSpec(color=(121, 22, 6), thickness=5, circle_radius=0)
    hand_connection_drawing_spec = mp_drawing.DrawingSpec(color=(250, 44, 90), thickness=15, circle_radius=15)

    right_distance = None
    left_distance = None

    while cap.isOpened():
        (ret, image) = cap.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (image_height, image_width, _) = image.shape

        results_hand = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results_hand.multi_hand_landmarks:
            for (idx, hand_landmarks) in enumerate(results_hand.multi_hand_landmarks):
                color = (0xFF, 0, 0)

                if idx == 0:  # Sağ el
                    x1, y1 = int(hand_landmarks.landmark[8].x * image_width), int(hand_landmarks.landmark[8].y * image_height)
                    x2, y2 = int(hand_landmarks.landmark[5].x * image_width), int(hand_landmarks.landmark[5].y * image_height)
                    cv2.circle(image, (x1, y1), 10, (255, 0, 128), cv2.FILLED)
                    cv2.circle(image, (x2, y2), 10, (255, 0, 128), cv2.FILLED)
                    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 128), 3)
                    right_distance2 = math.hypot(x2 - x1, y2 - y1)

                    x3, y3 = int(hand_landmarks.landmark[4].x * image_width), int(hand_landmarks.landmark[4].y * image_height)
                    x4, y4 = int(hand_landmarks.landmark[2].x * image_width), int(hand_landmarks.landmark[2].y * image_height)
                    cv2.circle(image, (x3, y3), 10, (255, 0, 128), cv2.FILLED)
                    cv2.circle(image, (x4, y4), 10, (255, 0, 128), cv2.FILLED)
                    cv2.line(image, (x3, y3), (x4, y4), (255, 0, 128), 3)
                    right_distance1 = math.hypot(x4 - x3, y2 - y4)

                    # Metni başparmak ucuna yazdır
                    text_x = x3
                    text_y = y3 - 20
                    cv2.putText(image, "{:.2f}".format(float(right_distance1 * 0.46 / right_distance2)), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)

                elif idx == 1:  # Sol el
                    x1, y1 = int(hand_landmarks.landmark[8].x * image_width), int(hand_landmarks.landmark[8].y * image_height)
                    x2, y2 = int(hand_landmarks.landmark[5].x * image_width), int(hand_landmarks.landmark[5].y * image_height)
                    cv2.circle(image, (x1, y1), 10, (255, 0, 128), cv2.FILLED)
                    cv2.circle(image, (x2, y2), 10, (255, 0, 128), cv2.FILLED)
                    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 128), 3)
                    right_distance2 = math.hypot(x2 - x1, y2 - y1)  # İşaret parmak boyu

                    x3, y3 = int(hand_landmarks.landmark[4].x * image_width), int(hand_landmarks.landmark[4].y * image_height)
                    x4, y4 = int(hand_landmarks.landmark[2].x * image_width), int(hand_landmarks.landmark[2].y * image_height)
                    cv2.circle(image, (x3, y3), 10, (255, 0, 128), cv2.FILLED)
                    cv2.circle(image, (x4, y4), 10, (255, 0, 128), cv2.FILLED)
                    cv2.line(image, (x3, y3), (x4, y4), (255, 0, 128), 3)
                    right_distance1 = math.hypot(x4 - x3, y2 - y4)  # Baş parmak boyu

                    # Metni başparmak ucuna yazdır
                    text_x = x3
                    text_y = y3 - 20
                    cv2.putText(image, "{:.2f}".format(float(right_distance1 * 0.46 / right_distance2)), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 2)

            for (idx, hand_landmarks) in enumerate(results_hand.multi_hand_landmarks):
                color = (0xFF, 0, 0)

                center_coordinates1 = (hand_landmarks.landmark[drawSpecific.HandLandmark.THUMB_TIP].x * image_width,
                                       hand_landmarks.landmark[drawSpecific.HandLandmark.THUMB_TIP].y * image_height)
                center_coordinates2 = (hand_landmarks.landmark[drawSpecific.HandLandmark.INDEX_FINGER_TIP].x * image_width,
                                       hand_landmarks.landmark[drawSpecific.HandLandmark.INDEX_FINGER_TIP].y * image_height)
                center_coordinates3 = (hand_landmarks.landmark[drawSpecific.HandLandmark.MIDDLE_FINGER_TIP].x * image_width,
                                       hand_landmarks.landmark[drawSpecific.HandLandmark.MIDDLE_FINGER_TIP].y * image_height)
                center_coordinates4 = (hand_landmarks.landmark[drawSpecific.HandLandmark.RING_FINGER_TIP].x * image_width,
                                       hand_landmarks.landmark[drawSpecific.HandLandmark.RING_FINGER_TIP].y * image_height)
                center_coordinates5 = (hand_landmarks.landmark[drawSpecific.HandLandmark.PINKY_TIP].x * image_width,
                                       hand_landmarks.landmark[drawSpecific.HandLandmark.PINKY_TIP].y * image_height)

                cv2.circle(image, (int(center_coordinates1[0]), int(center_coordinates1[1])), 15, color, 5)
                cv2.circle(image, (int(center_coordinates2[0]), int(center_coordinates2[1])), 15, color, 5)
                cv2.circle(image, (int(center_coordinates3[0]), int(center_coordinates3[1])), 15, color, 5)
                cv2.circle(image, (int(center_coordinates4[0]), int(center_coordinates4[1])), 15, color, 5)
                cv2.circle(image, (int(center_coordinates5[0]), int(center_coordinates5[1])), 15, color, 5)

                # mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=hand_landmarks,
                #     connections=handConnection,
                #     landmark_drawing_spec=hand_landmark_drawing_spec,
                #     connection_drawing_spec=hand_connection_drawing_spec
                # )

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    hands.close()
    cap.release()

main()
