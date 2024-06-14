# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 17:33:23 2024

@author: Lenovo

"""

#%%
import cv2
import mediapipe as mp
import math
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

#%%
cap = cv2.VideoCapture("D:/motionCaptureRealtime/ip-atlama.mp4")
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()

        
        # Convert the feed from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Refer the section above how to make detections on feed
        results = holistic.process(image)
  
        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        height, width, _ = frame.shape
        """
        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                 mp_drawing.DrawingSpec(color=(120,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(120,256,121), thickness=1, circle_radius=1)
                                 )
        """
        

        
        # 2. Draw Right hand landmarks
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 3. Draw Left Hand landmarks
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 4. Draw Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        

        if results.pose_landmarks:
            left_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP.value]
            right_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP.value]
            
            # Sol kalça ve sağ kalça noktalarının ortalamasını alarak hip noktasını hesapla
            hip_x = (left_hip.x + right_hip.x) / 2
            hip_y = (left_hip.y + right_hip.y) / 2
            hip_z = (left_hip.z + right_hip.z) / 2
            
                    

            cv2.circle(image, (int(hip_x * width), int(hip_y * height)), 5, (0, 255, 0), -1)
            # Sol dudak, sağ dudak, sol omuz ve sağ omuz değerlerine göre neck hesaplanması
            mouth_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT.value] # Mouth right
            mouth_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT.value]  # Mouth left
            
            right_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value]  # Right shoulder
            left_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER.value]


            
            #Kafanın kordinatlarının hesaplanması
            eye_left = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE.value]
            eye_right = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE.value]
            nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE.value]
            
            eye_mid_x = (eye_left.x + eye_right.x)/2;
            eye_mid_y = (eye_left.y + eye_right.y)/2;
            eye_mid_z = (eye_left.z + eye_right.z)/2;
            
            #print(f"eye_mid: X={eye_mid_x}, Y={eye_mid_y}, Z={eye_mid_z}")
            cv2.circle(image, (int(eye_mid_x* width), int(eye_mid_y* height)), 5, (0, 255, 0), -1)

            
            
            # Mouth right ve left orta noktalarını hesapla
            mouth_mid_x = (mouth_right.x + mouth_left.x) / 2
            mouth_mid_y = (mouth_right.y + mouth_left.y) / 2
            mouth_mid_z = (mouth_right.z + mouth_left.z) / 2
            cv2.circle(image, (int(mouth_mid_x* width), int(mouth_mid_y* height)), 5, (0, 255, 0), -1)
            #dudakların orta noktasından gözlerin orta noktasına çizgi çiz.
            cv2.line(image, (int(nose.x * frame.shape[1]), int(nose.y * frame.shape[0])), 
             (int(eye_mid_x * frame.shape[1]), int(eye_mid_y * frame.shape[0])), 
             (0, 255, 0), 2)
            
            
            line_length = math.sqrt((eye_mid_x - nose.x)**2 + (eye_mid_y - nose.y)**2)
            #print("Çizginin Uzunluğu:", line_length)
            new_line_length = (2.5)*line_length
            
            head_x = eye_mid_x
            head_y = eye_mid_y - new_line_length 
            head_z = eye_mid_z

            cv2.circle(image, (int(head_x* width), int(head_y* height)), 5, (0, 255, 0), -1)
            

            
              
            # Right shoulder ve left shoulder orta noktalarını hesapla
            shoulder_mid_x = (right_shoulder.x + left_shoulder.x) / 2
            shoulder_mid_y = (right_shoulder.y + left_shoulder.y) / 2
            shoulder_mid_z = (right_shoulder.z + left_shoulder.z) / 2
            
            # Neck noktasını hesapla
            neck_x = (mouth_mid_x + shoulder_mid_x) / 2
            neck_y = (mouth_mid_y + shoulder_mid_y) / 2
            neck_z = (mouth_mid_z + shoulder_mid_z) / 2
            
 
            cv2.circle(image, (int(neck_x * width), int(neck_y * height)), 5, (0, 255, 0), -1)
            
            
            
            spine1_x = (right_shoulder.x + left_shoulder.x) / 2
            spine1_y = (right_shoulder.y + left_shoulder.y) / 2
            spine1_z = (right_shoulder.z + left_shoulder.z) / 2

            # Kalçaların orta noktalarını hesaplayalım
            hip_mid_x = (right_hip.x + left_hip.x) / 2
            hip_mid_y = (right_hip.y + left_hip.y) / 2
            hip_mid_z = (right_hip.z + left_hip.z) / 2
            

            distance_x = abs(shoulder_mid_x - hip_mid_x)
            distance_y = abs(shoulder_mid_y - hip_mid_y)
    
            # Orta noktalar arasında 3 eşit aralık oluşturalım
            spine2_x = shoulder_mid_x + distance_x / 3
            spine2_y = shoulder_mid_y + distance_y / 3
            spine2_z = shoulder_mid_y + distance_y / 3
            
    
            spine3_x = shoulder_mid_x + 2 * distance_x / 3
            spine3_y = shoulder_mid_y + 2 * distance_y / 3
            spine3_z = shoulder_mid_y + 2 * distance_y / 3
    
            # Yeni noktaları işaretleyelim
            cv2.circle(image, (int(spine1_x * width), int(spine1_y * height)), 5, (0, 0,255), -1)#red
            cv2.circle(image, (int(spine2_x * width), int(spine2_y * height)), 5, (255, 0, 255), -1)#pink
            cv2.circle(image, (int(spine3_x * width), int(spine3_y * height)), 5, (0, 255, 0), -1)
            
            # print(f"hip: X={hip_x}, Y={hip_y}, Z={hip_z}")
            # print(f"spine1: X={spine1_x}, Y={spine1_y}, Z={spine1_z}")
            # print(f"spine2: X={spine2_x}, Y={spine2_y}, Z={spine2_z}")
            # print(f"spine3: X={spine3_x}, Y={spine3_y}, Z={spine3_z}")
            # print(f"neck: X={neck_x}, Y={neck_y}, Z={neck_z}")
            # print(f"head: X={head_x}, Y={head_y}, Z={head_z}")

            hip = [hip_x, hip_y, hip_z]
            neck = [neck_x,neck_y,neck_z]
            head= [head_x,head_y,head_z]
            
            spine1 = [spine1_x, spine1_y, spine1_z]
            spine2 = [spine2_x, spine2_y, spine2_z]
            spine3 = [spine3_x, spine3_y, spine3_z]
            
            shoulder_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER.value]

            
            upperarm_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW.value]
            
            lowerarm_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST.value]
            shoulder_R = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value]
            upperarm_R = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW.value]
            lowerarm_R = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST.value]
             
            
            
            
            thigh_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP.value]
            shin_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE.value]
            foot_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE.value]
            toe_L = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX.value]
            
            thigh_R = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP.value]
            shin_R = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE.value]
            foot_R =results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE.value]
            toe_R = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX.value]
            
            if (results.left_hand_landmarks is not None) and (results.right_hand_landmarks is not None):
                print("girdi")
                hand_L = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST.value]
                
                
                
                hand_R = results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST.value]
                
                    #         h1 = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST.value]
                    #         print("Wrist", h1)
                    #         k1 = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP.value]
                    #         print("index_finger", k1)
                    #         index_finger_rotation = (h1.x - k1.x, h1.y - k1.y, h1.z - k1.z)
                    #         print("index_finger_rotation", index_finger_rotation)


                
                with open("landmark_coordinates.txt", "a") as f:
                    f.write(f"{hip_x:.6f} {hip_z:.6f} {hip_y:.6f} ")
                    f.write(f"{spine1_x:.6f} {spine1_z:.6f} {spine1_y:.6f} ")
                    f.write(f"{spine2_x:.6f} {spine2_z:.6f} {spine2_y:.6f} ")
                    f.write(f"{spine3_x:.6f} {spine3_z:.6f} {spine3_y:.6f} ")
                    

                    
                    f.write(f"{shoulder_L.x:.6f} {shoulder_L.z:.6f} {shoulder_L.y:.6f} ")
                    f.write(f"{upperarm_L.x:.6f} {upperarm_L.z:.6f} {upperarm_L.y:.6f} ")
                    f.write(f"{lowerarm_L.x:.6f} {lowerarm_L.z:.6f} {lowerarm_L.y:.6f} ")
                    
                    f.write(f"{hand_L.x:.6f} {hand_L.z:.6f} {hand_L.y:.6f} ")
                    
                    f.write(f"{neck_x:.6f} {neck_z:.6f} {neck_y:.6f} ")
                    f.write(f"{head_x:.6f} {head_z:.6f} {head_y:.6f} ")
                    
                    f.write(f"{shoulder_R.x:.6f} {shoulder_R.z:.6f} {shoulder_R.y:.6f} ")
                    f.write(f"{upperarm_R.x:.6f} {upperarm_R.z:.6f} {upperarm_R.y:.6f} ")
                    f.write(f"{lowerarm_R.x:.6f} {lowerarm_R.z:.6f} {lowerarm_R.y:.6f} ")
                    f.write(f"{hand_R.x:.6f} {hand_R.z:.6f} {hand_R.y:.6f} ")
                    
                    
                    
                    
                    f.write(f"{thigh_L.x:.6f} {thigh_L.z:.6f} {thigh_L.y:.6f} ")
                    f.write(f"{shin_L.x:.6f} {shin_L.z:.6f} {shin_L.y:.6f} ")
                    
                    f.write(f"{foot_L.x:.6f} {foot_L.z:.6f} {foot_L.y:.6f} ")
                    f.write(f"{toe_L.x:.6f} {toe_L.z:.6f} {toe_L.y:.6f} ")

                    
                    
                    f.write(f"{thigh_R.x:.6f} {thigh_R.y:.6f} {thigh_R.z:.6f} ")
                    f.write(f"{shin_R.x:.6f} {shin_R.y:.6f} {shin_R.z:.6f} ")
                    f.write(f"{foot_R.x:.6f} {foot_R.y:.6f} {foot_R.z:.6f} ")
                    f.write(f"{toe_R.x:.6f} {toe_R.y:.6f} {toe_R.z:.6f} ")
                    
                    
                    
                    #ROTATİON
                    
                    hip_rotation = (0,0,0)
                    
                    spine1_rotation = (hip_x + spine1_x , hip_y + spine1_y, hip_z + spine1_z)
                    spine2_rotation = (spine1_x + spine2_x, spine1_y + spine2_y, spine1_z + spine2_z)                    
                    spine3_rotation = (spine2_x + spine3_x, spine2_y + spine3_y, spine2_z + spine3_z)
                    
                    shoulder_L_rotation = (spine3_x + shoulder_L.x , spine3_y + shoulder_L.y, spine3_z + shoulder_L.z)
                    upperarm_L_rotation = (shoulder_L.x + upperarm_L.x, shoulder_L.y + upperarm_L.y, shoulder_L.z + upperarm_L.z)
                    lowerarm_L_rotation = (upperarm_L.x + lowerarm_L.x , upperarm_L.y + lowerarm_L.y, upperarm_L.z + lowerarm_L.z)
                    hand_L_rotation = (lowerarm_L.x + hand_L.x , lowerarm_L.y + hand_L.y, lowerarm_L.z + hand_L.z)
                    
                    
                    neck_rotation = (spine3_x + neck_x , spine3_y + neck_y, spine3_z + neck_z)
                    head_rotation = (neck_x + head_x, neck_y + head_y, neck_z + head_z)
                    
                    
                    shoulder_R_rotation = (spine3_x + shoulder_R.x , spine3_y + shoulder_R.y, spine3_z + shoulder_R.z)
                    upperarm_R_rotation = (shoulder_R.x + upperarm_R.x, shoulder_R.y + upperarm_R.y, shoulder_R.z + upperarm_R.z)
                    lowerarm_R_rotation = (upperarm_R.x + lowerarm_R.x , upperarm_R.y + lowerarm_R.y, upperarm_R.z + lowerarm_R.z)
                    hand_R_rotation = (lowerarm_R.x + hand_R.x , lowerarm_R.y + hand_R.y, lowerarm_R.z + hand_R.z)
                    
                    
                    thigh_L_rotation = (hip_x + thigh_L.x , hip_y + thigh_L.y , hip_z + thigh_L.z)
                    shin_L_rotation = (thigh_L.x + shin_L.x , thigh_L.y + shin_L.y , thigh_L.z + shin_L.z)
                    foot_L_rotation = (shin_L.x + foot_L.x , shin_L.y + foot_L.y, shin_L.z + foot_L.z)
                    toe_L_rotation = (foot_L.x + toe_L.x, foot_L.y + toe_L.y, foot_L.z + toe_L.z)
                    
                    
                    
                    thigh_R_rotation = (hip_x + thigh_R.x , hip_y + thigh_R.y , hip_z + thigh_R.z)
                    shin_R_rotation = (thigh_R.x + shin_R.x , thigh_R.y + shin_R.y , thigh_R.z + shin_R.z)
                    foot_R_rotation = (shin_R.x + foot_R.x , shin_R.y + foot_R.y, shin_R.z + foot_R.z)
                    toe_R_rotation = (foot_R.x + toe_R.x, foot_R.y + toe_R.y, foot_R.z + toe_R.z)
                    
                    with open("rotation_coordinates.txt", "a") as f:
                        
                        f.write(f"{hip_x:.6f} {hip_z:.6f} {hip_y:.6f} ")
                        f.write(f"{hip_rotation[0]:.6f} {hip_rotation[2]:.6f} {hip_rotation[1]:.6f} ")
                        
                        
                        
                        f.write(f"{spine1_x:.6f} {spine1_z:.6f} {spine1_y:.6f} ")
                        f.write(f"{spine1_rotation[0]:.6f} {spine1_rotation[2]:.6f} {spine1_rotation[1]:.6f} ")
                        
                        
                        
                        f.write(f"{spine2_rotation[0]:.6f} {spine2_rotation[2]:.6f} {spine2_rotation[1]:.6f} ")
                        f.write(f"{spine3_rotation[0]:.6f} {spine3_rotation[2]:.6f} {spine3_rotation[1]:.6f} ")
                        

                        
                        f.write(f"{shoulder_L.x:.6f} {shoulder_L.z:.6f} {shoulder_L.y:.6f} ")
                        f.write(f"{shoulder_L_rotation[0]:.6f} {shoulder_L_rotation[2]:.6f} {shoulder_L_rotation[1]:.6f} ")
                        
                        f.write(f"{upperarm_L_rotation[0]:.6f} {upperarm_L_rotation[2]:.6f} {upperarm_L_rotation[1]:.6f} ")
                        f.write(f"{lowerarm_L_rotation[0]:.6f} {lowerarm_L_rotation[2]:.6f} {lowerarm_L_rotation[1]:.6f} ")
                        f.write(f"{hand_L_rotation[0]:.6f} {hand_L_rotation[2]:.6f} {hand_L_rotation[1]:.6f} ")
                        
                        f.write(f"{neck_rotation[0]:.6f} {neck_rotation[2]:.6f} {neck_rotation[1]:.6f} ")
                        f.write(f"{head_rotation[0]:.6f} {head_rotation[2]:.6f} {head_rotation[1]:.6f} ")
                        
                        
                        f.write(f"{shoulder_R.x:.6f} {shoulder_R.z:.6f} {shoulder_R.y:.6f} ")
                        f.write(f"{shoulder_R_rotation[0]:.6f} {shoulder_R_rotation[2]:.6f} {shoulder_R_rotation[1]:.6f} ")
                        
                        f.write(f"{upperarm_R_rotation[0]:.6f} {upperarm_R_rotation[2]:.6f} {upperarm_R_rotation[1]:.6f} ")
                        f.write(f"{lowerarm_R_rotation[0]:.6f} {lowerarm_R_rotation[2]:.6f} {lowerarm_R_rotation[1]:.6f} ")
                        f.write(f"{hand_R_rotation[0]:.6f} {hand_R_rotation[2]:.6f} {hand_R_rotation[1]:.6f} ")
                        
                        
                        f.write(f"{thigh_L.x:.6f} {thigh_L.z:.6f} {thigh_L.y:.6f} ")
                        f.write(f"{thigh_L_rotation[0]:.6f} {thigh_L_rotation[2]:.6f} {thigh_L_rotation[1]:.6f} ")
                        
                        
                        
                        
                        f.write(f"{shin_L_rotation[0]:.6f} {shin_L_rotation[2]:.6f} {shin_L_rotation[1]:.6f} ")
                        f.write(f"{foot_L_rotation[0]:.6f} {foot_L_rotation[2]:.6f} {foot_L_rotation[1]:.6f} ")
                        f.write(f"{toe_L_rotation[0]:.6f} {toe_L_rotation[2]:.6f} {toe_L_rotation[1]:.6f} ")
                        
                        
                        
                        
                        f.write(f"{thigh_R.x:.6f} {thigh_R.z:.6f} {thigh_R.y:.6f} ")
                        f.write(f"{thigh_R_rotation[0]:.6f} {thigh_R_rotation[2]:.6f} {thigh_R_rotation[1]:.6f} ")
                        
                        f.write(f"{shin_R_rotation[0]:.6f} {shin_R_rotation[2]:.6f} {shin_R_rotation[1]:.6f} ")
                        f.write(f"{foot_R_rotation[0]:.6f} {foot_R_rotation[2]:.6f} {foot_R_rotation[1]:.6f} ")
                        f.write(f"{toe_R_rotation[0]:.6f} {toe_R_rotation[2]:.6f} {toe_R_rotation[1]:.6f} ")
                        
                
                    # if (results.left_hand_landmarks is not None) or (results.right_hand_landmarks is not None):                       
                    #     reference_point = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP.value]
                    #     point = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP.value]
                    #     icler_carpimi = (reference_point.x * point.x) + (reference_point.y * point.y)
                    #     vektor_uzunlugu_reference_point = math.sqrt(reference_point.x**2 + reference_point.y**2)
                    #     vektor_uzunlugu_point = math.sqrt(point.x**2 + point.y**2)
                    #     inner_product = (icler_carpimi/(vektor_uzunlugu_reference_point)*(vektor_uzunlugu_point))
                    #     theta = math.acos(inner_product)
                    #     theta_degrees = math.degrees(theta)
                    #     print("Açı (radyan):", theta)
                    #     print("Açı (derece):", theta_degrees)
                    #     start_point = (int(reference_point.x * frame.shape[1]), int(reference_point.y * frame.shape[0]))
                    #     end_point = (int(point.x * frame.shape[1]), int(point.y * frame.shape[0]))
                        
                    #     cv2.line(image, start_point, end_point, (0, 255, 0), 2)
                    #     cv2.putText(image, f"Angle: {theta_degrees:.2f} degrees", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
   
                    

        cv2.imshow('Holistic Model Detections', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

