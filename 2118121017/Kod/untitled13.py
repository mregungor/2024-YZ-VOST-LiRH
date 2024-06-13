# -*- coding: utf-8 -*-
"""
Created on Sat May 25 17:08:16 2024

@author: user
"""

import cv2
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np

def load_images(option):
    global omuz_resmi, neck_image, image_right, image_left
    if option == 1:#beyaz
        omuz_resmi = cv2.imread("beyazdikdortgen2.PNG")
        neck_image = cv2.imread("BeyazBoyun3.PNG")
        image_right = cv2.imread('BeyazSag3.PNG')
        image_left = cv2.imread('BeyazSol2.PNG')
    elif option == 2:#mavi
        omuz_resmi = cv2.imread("dikdortgen.PNG")
        neck_image = cv2.imread("boyun5.PNG")
        image_right = cv2.imread('Sag.PNG')
        image_left = cv2.imread('Sol.PNG')
    elif option == 3:#yeşil
        omuz_resmi = cv2.imread("YesilDikdortgen.PNG")
        neck_image = cv2.imread("yesilBoyun5.PNG")
        image_right = cv2.imread('yesilSag.PNG')
        image_left = cv2.imread('yesilSol.PNG')

def on_image_click(option):
    load_images(option)
    root.destroy()

# tkinter penceresini oluştur
root = tk.Tk()

# Resimleri yükleyin
image1 = Image.open("beyazT.png")
image2 = Image.open("2.png")
image3 = Image.open("1.png")

# Resimleri Tkinter için uygun formata dönüştürün
tk_image1 = ImageTk.PhotoImage(image1)
tk_image2 = ImageTk.PhotoImage(image2)
tk_image3 = ImageTk.PhotoImage(image3)

# Resimleri etiketlere yerleştirin
label1 = tk.Label(root, image=tk_image1)
label1.grid(row=0, column=0)
label1.bind("<Button-1>", lambda event: on_image_click(1))

label2 = tk.Label(root, image=tk_image2)
label2.grid(row=0, column=1)
label2.bind("<Button-1>", lambda event: on_image_click(2))

label3 = tk.Label(root, image=tk_image3)
label3.grid(row=0, column=2)
label3.bind("<Button-1>", lambda event: on_image_click(3))

# Pencereyi göster
root.mainloop()

# Daha sonra seçilen resimlere göre işlem yapabilirsiniz.
# Mediapipe Pose modülünü yükle
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Kamera yakalayıcısını başlat
cap = cv2.VideoCapture(0)

def add_alpha_channel(image, alpha_value=255):
    """Add an alpha channel to the image with the given alpha value."""
    b, g, r = cv2.split(image)
    alpha = np.ones(b.shape, dtype=b.dtype) * alpha_value
    return cv2.merge([b, g, r, alpha])

def make_background_transparent(image, lower_bound, upper_bound):
    """Make the background transparent based on the color range."""
    b, g, r = cv2.split(image)
    alpha = np.ones(b.shape, dtype=b.dtype) * 255
    
    # Create a mask where the color is within the bounds
    mask = cv2.inRange(image, lower_bound, upper_bound)
    
    # Invert mask to get the foreground
    alpha[mask == 255] = 0
    
    return cv2.merge([b, g, r, alpha])

def detect_wrinkles(image):
    """Detect wrinkles in the image using edge detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

def combine_masks(alpha_mask, wrinkle_mask):
    """Combine alpha mask and wrinkle mask to exclude wrinkles from transparency."""
    combined_mask = np.where(wrinkle_mask == 255, 255, alpha_mask)
    return combined_mask

def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay img_overlay on top of img at (x, y) with alpha mask."""
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return img

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, None] / 255.0

    img_crop[:] = alpha * img_overlay_crop + (1 - alpha) * img_crop

    return img
# Define the color range for background to make transparent
lower_bound = np.array([0, 0, 0], dtype=np.uint8)  # adjust as needed
upper_bound = np.array([100, 100, 100], dtype=np.uint8)  # adjust as needed

def apply_combined_alpha(image, lower_bound, upper_bound):
    """Apply alpha channel to the image with wrinkle detection."""
    transparent_image = make_background_transparent(image, lower_bound, upper_bound)
    wrinkle_mask = detect_wrinkles(image)
    
    # Extract the alpha channel from transparent image
    b, g, r, alpha = cv2.split(transparent_image)
    
    # Combine the alpha mask with the wrinkle mask
    combined_alpha = combine_masks(alpha, wrinkle_mask)
    
    return cv2.merge([b, g, r, combined_alpha])

# Add alpha channel and make background transparent with wrinkle detection
omuz_resmi = apply_combined_alpha(omuz_resmi, lower_bound, upper_bound)
neck_image = cv2.resize(neck_image, (90, 90))
neck_image = apply_combined_alpha(neck_image, lower_bound, upper_bound)
image_right = cv2.resize(image_right, (90, 90))
image_right = apply_combined_alpha(image_right, lower_bound, upper_bound)
image_left = cv2.resize(image_left, (90, 90))
image_left = apply_combined_alpha(image_left, lower_bound, upper_bound)

# Save images with alpha channel (Optional)
cv2.imwrite("dikdortgen_alpha4.PNG", omuz_resmi)
cv2.imwrite("boyn5_alpha4.PNG", neck_image)
cv2.imwrite("sa_alpha4.PNG", image_right)
cv2.imwrite("so_alpha4.PNG", image_left)

# Resim dosyalarını alfa kanalıyla yükle
omuz_resmi = cv2.imread("dikdortgen_alpha4.PNG", cv2.IMREAD_UNCHANGED)
neck_image = cv2.imread("boyn5_alpha4.PNG", cv2.IMREAD_UNCHANGED)
image_right = cv2.imread('sa_alpha4.PNG', cv2.IMREAD_UNCHANGED)
image_left = cv2.imread('so_alpha4.PNG', cv2.IMREAD_UNCHANGED)

# Boyut uyumsuzluğu mesajını kontrol etmek için bir bayrak
size_mismatch_flag = False

while cap.isOpened():
    # Kameradan bir kare al
    ret, frame = cap.read()
    if not ret:
        break

    # Mediapipe ile pose tespiti yap
    results = pose.process(frame)

    # Sonuçları işle
    if results.pose_landmarks:
        # Sol omuz, sağ omuz, sol kalça ve sağ kalça noktalarının indislerini al
        left_shoulder = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame.shape[1]),
                         int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame.shape[0]))
        right_shoulder = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * frame.shape[1]),
                          int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame.shape[0]))
        left_hip = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * frame.shape[1]),
                    int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * frame.shape[0]))
        right_hip = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * frame.shape[1]),
                     int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * frame.shape[0]))

        # Noktaları işaretle
        cv2.circle(frame, left_shoulder, 5, (0, 255, 0), -1)
        cv2.circle(frame, right_shoulder, 5, (0, 255, 0), -1)
        cv2.circle(frame, left_hip, 5, (0, 255, 0), -1)
        cv2.circle(frame, right_hip, 5, (0, 255, 0), -1)

        # İşaretlenmiş noktaları içeren resmi kapsayan dikdörtgenin koordinatlarını hesapla
        x1 = min(left_shoulder[0], right_shoulder[0], left_hip[0], right_hip[0])
        y1 = min(left_shoulder[1], right_shoulder[1], left_hip[1], right_hip[1])
        x2 = max(left_shoulder[0], right_shoulder[0], left_hip[0], right_hip[0])
        y2 = max(left_shoulder[1], right_shoulder[1], left_hip[1], right_hip[1])

        # Omuz resminin boyutunu hedef bölgenin boyutlarına göre ayarlayın
        omuz_h = y2 - y1
        omuz_w = x2 - x1

        # Genişlik veya yükseklik sıfır ise atlayın
        if omuz_h > 0 and omuz_w > 0:
            resized_omuz_resmi = cv2.resize(omuz_resmi, (omuz_w, omuz_h))
            alpha_mask = resized_omuz_resmi[:, :, 3]
            resized_omuz_resmi = resized_omuz_resmi[:, :, :3]  # Remove alpha channel for blending
            frame = overlay_image_alpha(frame, resized_omuz_resmi, x1, y1, alpha_mask)

        # Boyun resmini ekle
        if neck_image is not None:
            # Boyun resmini işaretlenmiş omuzların ortasına yerleştir
            x_offset_neck = int((left_shoulder[0] + right_shoulder[0]) / 2) - neck_image.shape[1] // 2
            y_offset_neck = int((left_shoulder[1] + right_shoulder[1]) / 2) - neck_image.shape[0] // 2
            # Yerleştirme yaparken boyutları kontrol et
            if y_offset_neck >= 0 and y_offset_neck + neck_image.shape[0] <= frame.shape[0] and \
                    x_offset_neck >= 0 and x_offset_neck + neck_image.shape[1] <= frame.shape[1]:
                alpha_mask = neck_image[:, :, 3]
                neck_img_rgb = neck_image[:, :, :3]
                frame = overlay_image_alpha(frame, neck_img_rgb, x_offset_neck, y_offset_neck, alpha_mask)

        # Sağ omuz ve sol omuz resmini ekle
        if image_right is not None and image_left is not None:
            # Sağ omuz resmini işaretlenmiş sağ omuzun koordinatlarına yerleştir
            x_offset_right = right_shoulder[0] - image_right.shape[1] // 2
            y_offset_right = right_shoulder[1] - image_right.shape[0] // 2
            # Sol omuz resmini işaretlenmiş sol omuzun koordinatlarına yerleştir
            x_offset_left = left_shoulder[0] - image_left.shape[1] // 2
            y_offset_left = left_shoulder[1] - image_left.shape[0] // 2
            # Yerleştirme yaparken boyutları kontrol et
            if y_offset_right >= 0 and y_offset_right + image_right.shape[0] <= frame.shape[0] and \
                    x_offset_right >= 0 and x_offset_right + image_right.shape[1] <= frame.shape[1]:
                alpha_mask = image_right[:, :, 3]
                image_right_rgb = image_right[:, :, :3]
                frame = overlay_image_alpha(frame, image_right_rgb, x_offset_right, y_offset_right, alpha_mask)
            if y_offset_left >= 0 and y_offset_left + image_left.shape[0] <= frame.shape[0] and \
                    x_offset_left >= 0 and x_offset_left + image_left.shape[1] <= frame.shape[1]:
                alpha_mask = image_left[:, :, 3]
                image_left_rgb = image_left[:, :, :3]
                frame = overlay_image_alpha(frame, image_left_rgb, x_offset_left, y_offset_left, alpha_mask)

    # Sonuçları göster
    cv2.imshow('Pose Detection', frame)

    # Çıkış için 'q' tuşuna basılmasını bekle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()

