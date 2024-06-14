import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib
from datetime import datetime

from plaka_tespit_alg import plaka_konum_don
from alg2_plaka_tanima import plakaTani

veriler = os.listdir("veriseti")

isim = veriler[8]

img=cv2.imread("veriseti/"+isim)
img=cv2.resize(img,(500,500))

plaka=plaka_konum_don(img) # img'de konumu dondurecek x,y,w,h
plakaImg,plakaKarakter = plakaTani(img,plaka)



print("arabanin plakasi: ",plakaKarakter)

def plakaCiktisiniKaydet(plakaKarakter, dosya_adi):
    now = datetime.now()  # Anlık zamanı al
    saat_str = now.strftime("%d-%m-%Y / %H:%M:%S")  # Saat bilgisini belirli bir formata dönüştür
    plaka_metni = ''.join(plakaKarakter) + ' ' + saat_str + '\n'  # Plaka karakterleri ve saat bilgisini birleştir
    with open(dosya_adi, 'a') as file:  # 'a' modu dosyayı açar ve ekleme yapar
        file.write(plaka_metni)

# Kullanım örneği:
plakaCiktisiniKaydet(plakaKarakter, 'plaka_ciktisi.txt')
plt.imshow(img)
plt.show()
