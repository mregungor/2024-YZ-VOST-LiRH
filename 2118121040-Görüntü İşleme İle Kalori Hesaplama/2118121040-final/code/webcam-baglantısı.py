# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:13:08 2024

@author: Melisa
"""

import cv2
 
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    
    if key == 27: # Esc key
        break
    
cap.release()
cv2.destroyAllWindows()
