import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import time
import vlc
import sys, webbrowser, datetime

# Dlib'in yüz özelliklerini tespit edici yükleniyor
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# Göz açıklık oranını hesaplayan fonksiyon
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Ağız açıklık oranını hesaplayan fonksiyon
def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[13], mouth[19]) # 52-56
    B = dist.euclidean(mouth[14], mouth[18]) # 50-58
    C = dist.euclidean(mouth[15], mouth[17]) # 51-57
    D = dist.euclidean(mouth[12], mouth[16]) # 48-54
    MAR = (A + B + C) / (2.0 * D)
    return MAR

# Kamera kalibrasyonu için varsayılan değerler
kamera_matrisi = np.array([[640, 0, 320],
                            [0, 640, 240],
                            [0, 0, 1]], dtype="double")

bozulma_katsayilari = np.zeros((4, 1)) # Varsayılan olarak bozulma katsayıları sıfır kabul edilir

# Baş pozisyonunu tahmin etmek için kullanılacak 3D model noktaları
model_noktalari = np.array([
    (0.0, 0.0, 0.0),             # Burun ucu
    (0.0, -330.0, -65.0),        # Çene
    (-225.0, 170.0, -135.0),     # Sol göz sol köşesi
    (225.0, 170.0, -135.0),      # Sağ göz sağ köşesi
    (-150.0, -150.0, -125.0),    # Sol ağız köşesi
    (150.0, -150.0, -125.0)      # Sağ ağız köşesi
])

# Baş pozisyonunu tahmin eden fonksiyon
def bas_pozisyonu(landmarks):
    image_points = np.array([
        landmarks[30],     # Burun ucu
        landmarks[8],      # Çene
        landmarks[45],     # Sol göz sol köşesi
        landmarks[36],     # Sağ göz sağ köşesi
        landmarks[54],     # Sol ağız köşesi
        landmarks[48]      # Sağ ağız köşesi
    ], dtype="double")
    # solvePnP fonksiyonunu çağırarak baş pozisyonunu tahmin et
    _, rotation_vector, translation_vector = cv2.solvePnP(model_noktalari, image_points, kamera_matrisi, bozulma_katsayilari)

    # Euler açılarına dönüştür
    euler_acilari = cv2.Rodrigues(rotation_vector)[0]
    return euler_acilari
def process_image(goruntu):
    griTon = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
    yuzler = detector(griTon)
    for yuz in yuzler:
        landmarks2 = predictor(griTon, yuz)
        sol_goz = np.array([(landmarks2.part(n).x, landmarks2.part(n).y) for n in range(36, 42)])
        sag_goz = np.array([(landmarks2.part(n).x, landmarks2.part(n).y) for n in range(42, 48)])
        sol_goz_ear = eye_aspect_ratio(sol_goz)
        sag_goz_ear = eye_aspect_ratio(sag_goz)
        return (sol_goz_ear + sag_goz_ear) / 2
    return 0

# Kamera başlatılıyor
kamera = cv2.VideoCapture(0)
focus_player = vlc.MediaPlayer('focus.mp3')
break_player = vlc.MediaPlayer('take_a_break.mp3')

# Kullanıcıdan EAR için veri toplamak
def collect_eye_data():
    input("Gözlerinizi açık tutun ve 'enter' tuşuna basın.")
    time.sleep(1)
    _, acik_goruntu = kamera.read()
    acik_ear = process_image(acik_goruntu)

    time.sleep(3)

    input("Gözlerinizi kapalı tutun ve 'enter' tuşuna basın.")
    time.sleep(1)
    _, kapali_goruntu = kamera.read()
    kapali_ear = process_image(kapali_goruntu)

    print(f"Kapali: {kapali_ear}")
    print(f"Acik: {acik_ear}")
    ozel_esik_degeri = (acik_ear + kapali_ear) / 2
    print(f"Özel Eşik Değeri: {ozel_esik_degeri}")

    time.sleep(5)
    return ozel_esik_degeri

# Ağız bölgesini döndüren fonksiyon
def get_mouth_shape(landmarks):
    return np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(48, 68)])
#uyuklama kontrolü
def check(euler_acilari):
    pitch = euler_acilari[0, 0] * (180 / np.pi)
    # Başın aşağı eğilme derecesi (pitch) ile uyuklama
    if pitch < 10:
        return "Uyuklama tespit edildi!"
    else:
        return "Uyuklama tespit edilmedi."

esneme_sayaci = 0
esneme_esik_degeri = 0.5
ozel_esik_degeri = collect_eye_data()
kapali_sayac = 0
kapali_zaman = 1
counter = 0
goz_durumu = ""
ana = ozel_esik_degeri * 2
# 'landmarks' nesnesi, Dlib tarafından tespit edilen yüz özelliklerini içerir.
# Örneğin, 'predictor(griTon, yuz)' fonksiyonu ile elde edilir.


# Ana döngü
while True:
    _, goruntu = kamera.read()
    griTon = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
    yuzler = detector(griTon)
    for yuz in yuzler:
        landmarkss = predictor(griTon, yuz)
        mouth = get_mouth_shape(landmarkss)
        mar = mouth_aspect_ratio(mouth)
        landmarks = np.array([(p.x, p.y) for p in predictor(griTon, yuz).parts()])
        euler_acilari = bas_pozisyonu(landmarks)
        #print(landmarks)
        print(landmarkss)

        if check(euler_acilari):
            cv2.putText(goruntu, "UYUKLAMA TESPIT EDILDI!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        mouth_points = get_mouth_shape(landmarkss)
        # Ağız bölgesindeki nokta sayısını kontrol et
        print("Ağız bölgesindeki nokta sayısı:", len(mouth_points))

        # Eğer MAR eşik değerinden büyükse esneme olarak kabul et#if mouth > esneme_esik_degeri:
        if mar > esneme_esik_degeri:
            esneme_sayaci += 1
            cv2.putText(goruntu, "Esneme!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            esneme_sayaci = 0

        ear = process_image(goruntu)
        # Gözler %40'dan daha az açıksa
        if ear <= (0.4 * ana):
            print(f"%40 Değeri: {(0.3 * ana)}")
            goz_durumu = "Cok yorgunsunuz"
            kapali_sayac += 1
            break_player.play()
            if kapali_sayac >= 7:
                kapali_sayac = 0
                #webbrowser.open("https://www.google.com/maps/search/hotels+or+motels+near+me")
        # Gözler %60'dan daha fazla açıksa
        elif (ozel_esik_degeri < ear >= (ana * 0.6)):
            print(f"%60 Değeri: {(ana * 0.6)}")
            goz_durumu = "Odaklanin"
            counter += 1
            if counter >= 3:
                counter = 0
                focus_player.play()  # Focus sesini çal

        # Gözler normal açıklıktaysa
        else:
            kapali_sayac = 0  # Sayacı sıfırla
            counter = 0  # Counter'ı sıfırla
        uyuklama_mesaji = check(euler_acilari)
        cv2.putText(goruntu, uyuklama_mesaji, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(goruntu, f"Mesaj: {goz_durumu}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Orijinal", goruntu)

    if cv2.waitKey(1) == ord("q"):
        break

kamera.release()
cv2.destroyAllWindows()
