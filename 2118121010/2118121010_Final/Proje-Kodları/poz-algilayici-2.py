# -*- coding: utf-8 -*-
"""
Created on Sat May 18 07:29:44 2024

@author: Lenovo
"""

import cv2
from cvzone.PoseModule import PoseDetector
 
cap = cv2.VideoCapture('D:/motionCaptureRealtime/ip-atlama.mp4')
 
detector = PoseDetector()
posList = []
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)
 
    if bboxInfo:
        lmString = ''
        print(len(lmList))
        print(len(lmList[0]))
        for lm in lmList:
            lmString += f'{lm[0]},{img.shape[0] - lm[1]},{lm[2]},'
        posList.append(lmString)
 
    print(len(posList))
 
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('s'):
        with open("AnimationFile.txt", 'w') as f:
            f.writelines(["%s\n" % item for item in posList])
            
            
            
            
cap.release()
cv2.destroyAllWindows()            
            
        