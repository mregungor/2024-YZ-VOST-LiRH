"""
Tobs80 tarafından oluşturulmuştur.
"""

import random
import numpy as np
import math
import prettytable as prettytable
from prettytable import DEFAULT

# Her dönemdeki dersleri içeren listeler
sınıf_1 = ["	Reading Skills 2", "  Atatürk İlkeleri ve İnkılap Tarihi 2", "  Fizik 2",  " 	Ayrık Matematik", "	 Matematik 2", " Temel Elektronik", "Algoritma ve Programlama 2	"]
sınıf_2 = ["Nesne Tabanlı Programlama", "Veri Bilimine Giriş", "Algoritma Analizi", "Olasılık ve İstatistik", "	Bilgisayar Ağlarına Giriş", "Writing Skills 2", "Boş"]
sınıf_3 = ["Veri Madenciliği", "Simülasyon ve Modelleme", "	Mikro Denetleyiciler", "	Yapay Zeka", "	Veri Odaklı Sistem Tasarımı", "Latex İle Rapor Hazırlama", "Boş"]
# Öğretmenler ve dersleri ile ilgili sözlükler
ogretmenler_1inci = {"Reading Skills 2":"	Öğr. Gör. İSMAİL KARABULUT", "Atatürk İlkeleri ve İnkılap Tarihi 2": "Öğr. Gör. Halil Ölmez", "Fizik 2":"Doç. Dr. ÖMER SEVGİLİ", "	Ayrık Matematik":"Öğr. Gör. ALİ GÖKHAN ERTAŞ", "	Matematik 2":"Öğr. Gör. ALİ GÖKHAN ERTAŞ", "	Temel Elektronik":"Dr. Öğr. Üyesi VEDAT KAVALCI", "Algoritma ve Programlama 2":"Dr. Öğr. Üyesi HÜSEYİN COŞKUN"}

ogretmenler_2ncı = { "Nesne Tabanlı Programlama": " Dr. Öğr. Üyesi ZEKERİYA KATILMIŞ",  " Veri Bilimine Giriş": " Dr. Öğr. Üyesi ZEKERİYA KATILMIŞ",  " Algoritma Analizi": "Dr. Öğr. Üyesi AHMET GÜVEN","Olasılık ve İstatistik": "Dr. Öğr. Üyesi AHMET GÜVEN","Bilgisayar Ağlarına Giriş": "Dr. Öğr. Üyesi VEDAT KAVALCI","Writing Skills 2": "Öğr. Gör. İSMAİL KARABULUT","Boş": ""
}


ogretmenler_3nci = { "Veri Madenciliği": "Dr. Öğr. Üyesi AHMET GÜVEN", "Simülasyon ve Modelleme": "Dr. Öğr. Üyesi AHMET BAŞTUĞ", "Mikro Denetleyiciler": "Dr. Öğr. Üyesi AHMET BAŞTUĞ",
    "Yapay Zeka": "Dr. Öğr. Üyesi EMRE GÜNGÖR", "Veri Odaklı Sistem Tasarımı": "Dr. Öğr. Üyesi EMRE GÜNGÖR", "Latex İle Rapor Hazırlama": "Dr. Öğr. Üyesi EMRE GÜNGÖR", "Boş": ""
}


gunler = {0:  " Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe", 4: "Cuma"}
# Popülasyon boyutunu belirleme
populasyon = 8
# Ders sayısı
ders_sayisi = len(sınıf_1)
# Popülasyon boyutuna göre vektörlerin başlatılması
Populasyonlar = [0] * populasyon
Uygunluk_degeri = [0] * populasyon
# Mutasyon için değiştirilecek öznelerin sayısı
mutasyona_uğrayacaklar = 4
# Mutasyon olasılığı
mutasyon_olasılığı = 0.3
# Maksimum nesil sayısı
maksimum_nesil = 100

# Saatleri düzenli ve güzel görünmesi için bir fonksiyon
def zamanyazdır(zaman, birey, ogretmenler):
    tablo = prettytable.PrettyTable()
    tablo.field_names = [ "Pazartesi" , "Salı", "Çarşamba", "Perşembe", "Cuma" ]
    for gün in range(7):
        dersler = ["  ",  "   ",  "  ",  "   ",  "   "]
        ogretmenler_listesi = ["  ",  "  ",  "  ",  "  ",  "  "]
        for x in range(5):
            dersler[x] = zaman[birey][x][gün]
            ogretmenler_listesi[x] = ogretmenler.get(dersler[x])
        tablo.add_row(dersler)
        tablo.add_row(ogretmenler_listesi)
        
        tablo.add_row(["   ",  "  ",  "  ",  "  ",  "  "])

    tablo.header = (True)
    tablo.horizontal_char =  '—'
    tablo.junction_char = ' '
    tablo.add_column("Ders Saati", ["7:00 - 9:00" ,  "  ", " ", "9:00 - 11:00", " ", " ", "11:00 - 12:00 ", " ", " ", "12:00 - 13:00 ",
                                     " ", " ", "13:00 - 14:00 ", " ", " ", "14:00 - 16:00 ", " ", " ", "16:00 - 18:00 ", " ", " "])
    print(tablo)

# En iyi çözümden en kötüsüne doğru özneleri sıralayan fonksiyon
def bubbleSort(liste1, liste2):
    for i in range(len(liste1)-1,0,-1):
        for j in range(i):
            if liste1[j]>liste1[j+1]:
                temp = liste1[j]
                temp2 = liste2[j]
                liste1[j] = liste1[j+1]
                liste2[j] = liste2[j+1]
                liste1[j+1] = temp
                liste2[j+1] = temp2
    return (liste1,liste2)

# Başlangıç horaryosunu oluşturan fonksiyon
def populasyonuBaşlat(zaman_init, dersler):
    for birey in range(populasyon):
        for gün in range(5):
            zaman_init[birey][gün] = random.sample(dersler, len(dersler))
    return zaman_init

def uygunluk_degeri_hesapla(zaman_1inci, zaman_2ncı, zaman_3nci, birey):
    çakışmalar = 0
    for günler in range(5):
        for ders in range(ders_sayisi):
            ogretmen_5inci = ogretmenler_1inci.get(zaman_1inci[birey][günler][ders])
            ogretmen_6ncı = ogretmenler_2ncı.get(zaman_2ncı[birey][günler][ders])
            ogretmen_7nci = ogretmenler_3nci.get(zaman_3nci[birey][günler][ders])
            if (ogretmen_5inci == ogretmen_6ncı or ogretmen_5inci == ogretmen_7nci) and ogretmen_5inci != "Boş":
                çakışmalar += 1
            if (ogretmen_6ncı == ogretmen_7nci) and ogretmen_6ncı != "Boş":
                çakışmalar += 1
    return (çakışmalar)

def mutasyon(zaman, dersler):
    for gün in range(5):
        if random.uniform(0, 1) <= mutasyon_olasılığı:
            zaman[gün] = random.sample(dersler, len(dersler))
    return zaman

def değişim(zaman, populasyonlar, mutasyon_dersleri):
    yeni_populasyon = zaman
    yeni_populasyon[0] = zaman[populasyonlar[0]]
    yeni_populasyon[1] = zaman[populasyonlar[1]]
    for bireyler in range(2, len(populasyonlar) - 1, 2):
        kesme_noktası = math.floor(random.uniform(0, 5.9))

        ebeveyn1 = zaman[populasyonlar[bireyler]]
        ebeveyn2 = zaman[populasyonlar[bireyler + 1]]

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
        for mutasyonlar in range(1, mutasyona_uğrayacaklar):
            yeni_populasyon[-mutasyonlar] = mutasyon(yeni_populasyon[-mutasyonlar], mutasyon_dersleri)
    return (yeni_populasyon)

# zaman başlangıcı (boyutlar)
zaman_1inci = [["0" for i in range(5)] for j in range(populasyon)]
zaman_2ncı = zaman_1inci
zaman_3nci = zaman_1inci

# Her özne için derslerle yüklenme ve bunları daha kolay işlemek için NP dizisine dönüştürme
zaman_1inci = populasyonuBaşlat(zaman_1inci, sınıf_1)
zaman1 = np.array(zaman_1inci)
zaman_2ncı = populasyonuBaşlat(zaman_2ncı, sınıf_2)
zaman2 = np.array(zaman_2ncı)
zaman_3nci = populasyonuBaşlat(zaman_3nci, sınıf_3)
zaman3 = np.array(zaman_3nci)


# Nesil sayacı
nesil_sayacı = 0
while nesil_sayacı < maksimum_nesil:
    if nesil_sayacı % 10 == 0:
        print("Nesil: ", nesil_sayacı)

    for birey in range(populasyon):
        Uygunluk_degeri[birey] = uygunluk_degeri_hesapla(zaman1, zaman2, zaman3, birey - 1)
        Populasyonlar[birey] = birey
        if Uygunluk_degeri[birey] == 0:
            print("Çözüm bulundu, birey:", birey, "\n")
            print("Nesil: ", nesil_sayacı)
            print("1. sınıf ders programı\n")
            zamanyazdır(zaman1, birey, ogretmenler_1inci)
            print("2. sınıf ders programı\n")
            zamanyazdır(zaman2, birey, ogretmenler_2ncı)
            print("3. sınıf ders programı\n")
            zamanyazdır(zaman3, birey, ogretmenler_3nci)
            nesil_sayacı = maksimum_nesil 
            break

    Uygunluk_degeri, Populasyonlar = bubbleSort(Uygunluk_degeri, Populasyonlar)
    zaman1 = değişim(zaman1, Populasyonlar, sınıf_1)
    zaman2 = değişim(zaman2, Populasyonlar, sınıf_2)
    zaman3 = değişim(zaman3, Populasyonlar, sınıf_3)
    nesil_sayacı += 1
zamanyazdır(zaman1.copy(), birey, ogretmenler_1inci.copy())
zamanyazdır(zaman2.copy(), birey, ogretmenler_2ncı.copy())
zamanyazdır(zaman3.copy(), birey, ogretmenler_3nci.copy())



# Tekrar :)
