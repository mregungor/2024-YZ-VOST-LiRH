import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

def islem(img):
    yeni_boy = img.reshape((1600, 5, 5))
    orts = []
    for parca in yeni_boy:
        ort = np.mean(parca)
        orts.append(ort)
    orts = np.array(orts)
    orts = orts.reshape(1600,)
    return orts

path = "karakterseti/"
siniflar = os.listdir(path)
tek_batch = 0

urls = []
sinifs = []

print("Veriler okunuyor...")

for sinif in siniflar:
    resimler = os.listdir(path + sinif)
    for resim in resimler:
        urls.append(path + sinif + "/" + resim)
        sinifs.append(sinif)
        tek_batch += 1

df = pd.DataFrame({"adres": urls, "sinif": sinifs})

sinifs = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10,
          'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20,
          'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30,
          'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'arkaplan': 36}

index = list(sinifs.values())
siniflar = list(sinifs.keys())

df = df.sample(frac=1)

# Modeli yükleyelim
job = joblib.load('model.joblib')

for adres, sinif in df.values:
    image = cv2.imread(adres, 0)
    resim = cv2.resize(image, (200, 200))
    resim = resim / 255
    oznitelikler = islem(resim)

    # Tahmin yapalım
    sonuc = job.predict([oznitelikler])[0]
    print("Sonuc:", sonuc)

    ind = index.index(sonuc)
    sinif = siniflar[ind]
    plt.imshow(resim, cmap="gray")
    plt.title("Fotograftaki karakter: " + sinif)
    plt.show()
