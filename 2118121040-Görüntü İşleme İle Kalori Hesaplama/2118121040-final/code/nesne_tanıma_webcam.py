# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 23:45:29 2024

@author: Melisa
"""

from ultralytics import YOLO
import cv2
import cvzone
import math

# Check the camera index (0 for default webcam)
# If 0 is not the correct index for your camera, try 1 or other indices

cap = cv2.VideoCapture(0)

model=YOLO("yolov8n.pt")
  
cap.set(3, 720)
cap.set(4, 620)


classNames=["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
             "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
              "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
              "backpack", "umbrella", "handbag","tie", "suitcase", "frisbee", "skis", "sqowboard",
              "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
              "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
              "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
              "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet",
              "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone" "microwave",
              "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush",]

while True:
   success, img = cap.read()
   results=model(img, stream=True)
   for r in results:
       boxes=r.boxes
       for box in boxes:
          x1,y1,x2,y2= box.xyxy[0]
          x1,y1,x2,y2= int(x1),int(y1),int(x2),int(y2)
          # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
          
          w,h=x2-x1,y2-y1
          
          cvzone.cornerRect(img, (x1,y1,w,h))
          
          conf=math.ceil((box.conf[0]*100))/100
          print(conf)
          
          cls=int(box.cls[0])
          cvzone.putTextRect(img,f'{classNames[cls]} {conf}',(max(0,x1),max(35,y1)))
   
   cv2.imshow("Image", img)
        
        # Exit the loop if 'q' is pressed
   if cv2.waitKey(1) & 0xFF == ord('q'):
     break

    # Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()