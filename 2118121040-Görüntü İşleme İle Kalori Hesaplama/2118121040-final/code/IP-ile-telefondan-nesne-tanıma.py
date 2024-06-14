# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:45:45 2024

@author: Melisa
"""


import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture("http://10.200.26.20:8080/video")

model = YOLO("yolov8n.pt")

while True:
    ret, img = cap.read()
    
    if not ret:
        break
    
    result = model(img, show=True)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
