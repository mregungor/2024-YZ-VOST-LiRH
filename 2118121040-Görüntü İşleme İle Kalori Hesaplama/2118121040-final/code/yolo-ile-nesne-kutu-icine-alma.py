# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:02:58 2024

@author: Melisa
"""


import cv2
from ultralytics import YOLO
import cvzone

model = YOLO(r'C:\Users\Melisa\Desktop\egitilmis-model-ile-boyut-bulma\yolo-test\model\best.pt')
#cap = cv2.VideoCapture(r'C:/Users/Melisa/Desktop/Data-1/cilek-1.jpg')
cap = cv2.VideoCapture(r'C:/Users/Melisa/Desktop/Data-1/elma-19.jpg')
#cap = cv2.VideoCapture(r'C:/Users/Melisa/Desktop/Data-1/armut-10.jpg')

while cap.isOpened():
    ret, img = cap.read()
    if ret:
        img = cv2.resize(img, (640, 480))
        results = model(img, stream=True)

        try:
            for r in results:
                boxes = r.boxes
                names = r.names
           
                ##print(names)
                #print(probabilities)
                for box in boxes:
                   
                    variable=names[int(box.cls)]
                    print(variable)
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cvzone.putTextRect(img,variable,(max(0,x1),max(35,y1)))

            cv2.imshow('img', img)
            a = cv2.waitKey()
            if a == ord('q'):
                break

        except cv2.error:
            print("An error occurred while processing the frame!")
            





cap.release()
cv2.destroyAllWindows()


