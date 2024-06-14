"""
Tobs80 tarafından oluşturulmuştur.
"""

import random
import numpy as np
import math
import prettytable as prettytable
from prettytable import DEFAULT
# Her bir dönemdeki dersleri içeren listeler
dersler_5inci = ["Simülasyon", "Fizik IV", "Fizik V",
                  "Bilgisayar Bilimi", "Kompozisyon",
                    "Elektronik IV", "Boş"]
dersler_6ncı = ["Proje VI", "Elektronik V", "Mekanik VI", 
                "Mekanik VII", "Sistemler", "Ölçme", "Boş"]
dersler_7nci = ["Yenilenebilir Enerji", "Bilgisayar Bilimi IV",
                 "Mekatronik II", "Proje II", "Elektronik II",
                   "Mikroekonomi", "Boş"]
# Her dersin karşılık geldiği öğretim görevlileri ve haftanın günleri
ogretim_gorevlileri_5inci = {"Elektronik IV": "Grefa", "Kompozisyon": "R. Guachi",
                   "Simülasyon": "R. Guachi", "Fizik IV": "Oscullo",
                     "Bilgisayar Bilimi": "L. Guachi", "Fizik V": "Tirira",
                       "Boş": "Boş"}
ogretim_gorevlileri_6ncı = {"Proje VI": "Duchi", "Elektronik V": "Grefa",
                   "Mekanik VI": "Jacome", "Mekanik VII": "Jacome",
                     "Sistemler": "Velarde", "Ölçme": "Corrales",
                       "Boş": "Boş"}
ogretim_gorevlileri_7nci = {"Yenilenebilir Enerji": "Oscullo",
                   "Bilgisayar Bilimi IV": "Corrales",
                     "Mekatronik II": "Castro", "Proje II": "Duchi",
                       "Elektronik II": "Velarde", "Mikroekonomi": "Altamirano", "Boş": "Boş"}
haftanin_gunleri = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe", 4: "Cuma"}

# Popülasyon boyutunu belirtin
populasyon = 8
# Derslerin sayısı
ders_sayisi = len(dersler_5inci)
# Popülasyon boyutunu belirlemek için boş bir liste oluşturun
Populasyonlar = [0] * populasyon
Fitness_degeri = [0] * populasyon
# Mutasyona tabi tutulacak birey sayısı
mutasyona_uğrayanlar = 4
# Mutasyon olasılığı
mutasyon_olasılığı = 0.3
# Maksimum nesil sayısı
maksimum_nesil = 100

# Zaman tablosunu daha iyi anlaşılabilir ve düzenli bir şekilde yazdırmak için bir fonksiyon
def ders_programını_yazdır(program, birey, ogretim_gorevlileri):
    tablo = prettytable.PrettyTable()
    tablo.field_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
    for gun in range(7):
        dersler = [" ", " ", " ", " ", " "]
        ogretim_gorevlileri_listesi = [" ", " ", " ", " ", " "]
        for x in range(5):
            dersler[x] = program[birey][x][gun]
            ogretim_gorevlileri_listesi[x] = ogretim_gorevlileri.get(dersler[x])
        tablo.add_row(dersler)
        tablo.add_row(ogretim_gorevlileri_listesi)
        tablo.add_row([" ", " ", " ", " ", " "])

    tablo.header = True
    tablo.horizontal_char = '—'
    tablo.junction_char = ' '
    tablo.add_column("Ders Saati", ["7:00 - 9:00", " ", " ", "9:00 - 11:00", " ", " ", "11:00 - 12:00", " ", " ", "12:00 - 13:00",
                                     " ", " ", "13:00 - 14:00", " ", " ", "14:00 - 16:00", " ", " ", "16:00 - 18:00", " ", " "])
    print(tablo)

# En iyi ders programını bulmak için genetik algoritmayı kullan
def siralama_yap(birListe, birListe2):
    for numPasada in range(len(birListe) - 1, 0, -1):
        for i in range(numPasada):
            if birListe[i] > birListe[i + 1]:
                temp = birListe[i]
                temp2 = birListe2[i]
                birListe[i] = birListe[i + 1]
                birListe2[i] = birListe2[i + 1]
                birListe[i + 1] = temp
                birListe2[i + 1] = temp2

    return (birListe, birListe2)

# Başlangıç popülasyonunu oluştur
def PopulasyonuOlustur(Program_init, dersler):
    for birey in range(populasyon):
        for gun in range(5):
            Program_init[birey][gun] = random.sample(dersler, len(dersler))
    return Program_init

# Fitness fonksiyonu
def uygunluk_hesapla(Program_5, Program_6, Program_7, birey):
    çakışmalar = 0
    for günler in range(5):
        for ders in range(ders_sayisi):
            Ogretmen_5 = ogretim_gorevlileri_5inci.get(Program_5[birey][günler][ders])
            Ogretmen_6 = ogretim_gorevlileri_6ncı.get(Program_6[birey][günler][ders])
            Ogretmen_7 = ogretim_gorevlileri_7nci.get(Program_7[birey][günler][ders])
            if (Ogretmen_5 == Ogretmen_6 or Ogretmen_5 == Ogretmen_7 and Ogretmen_5 != "Boş"):
                çakışmalar += 1
            if (Ogretmen_6 == Ogretmen_7 and Ogretmen_6 != "Boş"):
                çakışmalar += 1
    return (çakışmalar)

# Mutasyon işlemi
def MutasyonaUgrat(program, dersler):
    for gün in range(5):
        if (random.uniform(0, 1) <= mutasyon_olasılığı):
            program[gün] = random.sample(dersler, len(dersler))
    return program

# Yeni nesil oluşturma işlemi
def YeniNesilOlustur(program, populasyonlar, dersler_mut):
    yeni_populasyon = program
    yeni_populasyon[0] = program[populasyonlar[0]]
    yeni_populasyon[1] = program[populasyonlar[1]]
    for bireyler in range(2, len(populasyonlar) - 1, 2):
        kesme_noktası = math.floor(random.uniform(0, 5.9))
        ebeveyn1 = program[populasyonlar[bireyler]]
        ebeveyn2 = program[populasyonlar[bireyler + 1]]
        çocuk1 = ebeveyn1
        çocuk2 = ebeveyn2
        if kesme_noktası == 5:
            çocuk1 = ebeveyn1
            çocuk2 = ebeveyn2
        else:
            gün_ = 0
            while gün_ <= kesme_noktası:
                çocuk1[gün_] = ebeveyn1[gün_]
                çocuk2[gün_] = ebeveyn2[gün_]
                gün_ += 1
            while gün_ < 5:
                çocuk2[gün_] = ebeveyn1[gün_]
                çocuk1[gün_] = ebeveyn2[gün_]
                gün_ += 1
        yeni_populasyon[bireyler] = çocuk1
        yeni_populasyon[bireyler + 1] = çocuk2
        for mutasyon in range(1, mutasyona_uğrayanlar):
            yeni_populasyon[-mutasyon] = MutasyonaUgrat(yeni_populasyon[-mutasyon], dersler_mut)
    return (yeni_populasyon)

# Haftalık ders programını oluşturma işlemi
Ders_Programı_5inci = [["0" for i in range(5)] for j in range(populasyon)]
Ders_Programı_6ncı = Ders_Programı_5inci
Ders_Programı_7nci = Ders_Programı_5inci

Ders_Programı_5inci = PopulasyonuOlustur(Ders_Programı_5inci, dersler_5inci)
Ders_Programı_5 = np.array(Ders_Programı_5inci)
Ders_Programı_6ncı = PopulasyonuOlustur(Ders_Programı_6ncı, dersler_6ncı)
Ders_Programı_6 = np.array(Ders_Programı_6ncı)
Ders_Programı_7ncı = PopulasyonuOlustur(Ders_Programı_7nci, dersler_7nci)
Ders_Programı_7 = np.array(Ders_Programı_7ncı)

nesil_sayacı = 0
while nesil_sayacı < maksimum_nesil:
    if nesil_sayacı % 10 == 0:
        print("Nesil: ", nesil_sayacı)
    for birey in range(populasyon):
        Fitness_degeri[birey] = uygunluk_hesapla(Ders_Programı_5, Ders_Programı_6, Ders_Programı_7, birey - 1)
        Populasyonlar[birey] = birey

        if (Fitness_degeri[birey] == 0):
            print("Çözüm bulundu, öğrenci: ", birey, "\n")
            print("Nesil: ", nesil_sayacı)
            print("5. Yarıyıl Ders Programı\n")
            ders_programını_yazdır(Ders_Programı_5, birey, ogretim_gorevlileri_5inci)
            print("6. Yarıyıl Ders Programı\n")
            ders_programını_yazdır(Ders_Programı_6, birey, ogretim_gorevlileri_6ncı)
            print("7. Yarıyıl Ders Programı\n")
            ders_programını_yazdır(Ders_Programı_7, birey, ogretim_gorevlileri_7nci)

            nesil_sayacı = maksimum_nesil
            break
    Fitness_degeri, Populasyonlar = siralama_yap(Fitness_degeri, Populasyonlar)
    Ders_Programı_5 = YeniNesilOlustur(Ders_Programı_5, Populasyonlar, dersler_5inci)
    Ders_Programı_6 = YeniNesilOlustur(Ders_Programı_6, Populasyonlar, dersler_6ncı)
    Ders_Programı_7 = YeniNesilOlustur(Ders_Programı_7, Populasyonlar, dersler_7nci)
    nesil_sayacı += 1
