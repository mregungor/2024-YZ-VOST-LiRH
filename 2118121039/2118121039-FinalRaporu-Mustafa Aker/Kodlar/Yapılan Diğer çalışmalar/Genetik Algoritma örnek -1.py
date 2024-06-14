import numpy as np
import pandas as pd

class GenetikAlgoritma:
    def __init__(self, n, m, k, u, h):
        self.n = n  # Hemşire sayısı
        self.m = m  # Gün sayısı
        self.k = k  # Vardiya sayısı
        self.u = u  # Uzman hemşire sayısı
        self.h = h  # Gece nöbetine kalmayacak hemşire sayısı
        self.populasyon_boyutu = 50  # Popülasyon boyutu
        self.maksimum_nesil = 100  # Maksimum nesil sayısı
        self.mutasyon_orani = 0.1 # Mutasyon oranı
        self.populasyon = self.populasyon_olustur()

    def amac_fonksiyonu(self, X):
        fmin = 0
        for i in range(self.n):
            for d in range(self.m):
                fmin += 8 * X[i*self.m + d] + 16 * X[self.n*self.m + i*self.m + d]
        return fmin

    def kisitlar(self, X):
        kisitlar = []
        # Aynı gün ya gece ya gündüz vardiyasında çalışılmalı ya da izinli olunmalıdır
        for i in range(self.n):
            for d in range(self.m):
                kisitlar.append(X[i*self.m + d] + X[self.n*self.m + i*self.m + d] <= 1)
         # Kisit 1: Her hemşirenin bir günde en fazla bir vardiya yapması
        for i in range(self.n):
            for d in range(self.m):
                kisitlar.append(X[i*self.m + d] + X[self.n*self.m + i*self.m + d] <= 1)
        
        # Kisit 2: Uzman hemşirelerin her gün en az bir vardiya yapması
        for d in range(self.m):
            uzman_toplam = 0
            for i in range(self.u):
                uzman_toplam += X[self.n*self.m + i*self.m + d]
            kisitlar.append(uzman_toplam >= 1)
        
        # Kisit 3: Gece nöbetine kalmayacak hemşirelerin her gün gece vardiyası yapmaması
        for d in range(self.m):
            gece_toplam = 0
            for i in range(self.h):
                gece_toplam += X[self.n*self.m + self.u*self.m + i*self.m + d]
            kisitlar.append(gece_toplam == 0)
        
        # Kisit 4: Gündüz vardiyasında çalışan bir hemşirenin gece vardiyasında çalışmaması
        for i in range(self.n):
            for d in range(self.m):
                kisitlar.append(X[i*self.m + d] + X[self.n*self.m + i*self.m + d] <= 1) 


        # Kisit 5: Akşam nöbetinde iki kişi çalışır
        for d in range(self.m):
            aksam_toplam = 0
            for i in range(self.n):
                aksam_toplam += X[self.n*self.m + i*self.m + d]
            kisitlar.append(aksam_toplam == 2)
        
        # Kisit 6: Her hemşire nöbetçi olmadığı gün 8 saat çalışır. Haftada 40 saat, ayda 160 saat çalışma zorunluluğu
        saat = 40 if self.n == 5 else 160
        for i in range(self.n):
            toplam_saat = 0
            for d in range(self.m):
                toplam_saat += 8 * (1 - X[i*self.m + d]) + 16 * X[self.n*self.m + i*self.m + d]
            kisitlar.append(toplam_saat == saat)
        
        # Kisit 7: Akşam nöbeti tutanlara ertesi gün görev verilmez
        for i in range(self.n):
            for d in range(self.m - 1):
                kisitlar.append(X[self.n*self.m + i*self.m + d] + X[i*self.m + d + 1] == 0)
        
        # Kisit 8: Hemşire aynı gün içinde yalnızca bir vardiyada çalışabilir ya da izinlidir
        for i in range(self.n):
            for d in range(self.m):
                kisitlar.append(X[i*self.m + d] + X[self.n*self.m + i*self.m + d] <= 1)
        
        # Kisit 9: Akşam vardiyasında nöbet tutan iki kişiden birinin uzman olması
        for d in range(self.m):
            uzman_var = 0
            for i in range(self.u):
                uzman_var += X[self.n*self.m + i*self.m + d]
            kisitlar.append(uzman_var >= 1)
        
        # Kisit 10: Sabah vardiyasında çalışan hemşire akşam vardiyasında çalışmayacak
        for i in range(self.n):
            for d in range(self.m):
                kisitlar.append(X[i*self.m + d] + X[self.n*self.m + i*self.m + d] <= 1)
        
        # Kisit 11:Uzman hemşireler gece vardiyasında en az bir kişi olmalı
        for d in range(self.m):
            uzman_toplam = 0
            for i in range(self.u):
                uzman_toplam += X[self.n*self.m + i*self.m + d]
            kisitlar.append(uzman_toplam >= 1)
        
        # Kisit 12:Gece nöbetine kalmayacak hemşireler
        for d in range(self.m):
            gece_toplam = 0
            for i in range(self.h):
                gece_toplam += X[self.n*self.m + self.u*self.m + i*self.m + d]
            kisitlar.append(gece_toplam == 0)
        
        #Kisit 13:Gece nöbetinde iki kişi çalışır (kısıtlı olanlar hariç)
        for d in range(self.m):
            aksam_toplam = 0
            for i in range(self.n):
                aksam_toplam += X[self.n*self.m + i*self.m + d]
            kisitlar.append(aksam_toplam == 2)
               # Kisit 14: Ayda en az 160 saat çalışmalı
        saat = 160
        for i in range(self.n):
            toplam_saat = 0
            for d in range(self.m):
                toplam_saat += 8 * X[i*self.m + d] + 16 * X[self.n*self.m + i*self.m + d]
            kisitlar.append(toplam_saat >= saat)
        
        # Kisit 15:Gece nöbet tutan ertesi gün gündüz çalışmaz
        for i in range(self.n):
            for d in range(self.m - 1):
                kisitlar.append(X[self.n*self.m + i*self.m + d] + X[i*self.m + d + 1] == 0)
        
        return kisitlar

    def populasyon_olustur(self):
        populasyon = []
        for _ in range(self.populasyon_boyutu):
            birey = self.baslangic_bireyi_olustur()
            while not self.kisitlari_saglar(birey):
                birey = self.baslangic_bireyi_olustur()
            populasyon.append(birey)
        return np.array(populasyon)

    def baslangic_bireyi_olustur(self):
        return np.random.randint(2, size=(self.n * self.m * 2))

    def kisitlari_saglar(self, birey):
        kisitlar = self.kisitlar(birey)
        return all(kisitlar)

    def uygunluk_hesapla(self):
        uygunluk_degerleri = []
        for birey in self.populasyon:
            if self.kisitlari_saglar(birey):
                uygunluk_degerleri.append(self.amac_fonksiyonu(birey))
            else:
                uygunluk_degerleri.append(float('inf'))  # Kısıtları sağlamayan bireylere sonsuz uygunluk değeri atanır
        return uygunluk_degerleri

    def sec(self, uygunluk_degerleri):
        secilenler = []
        for _ in range(self.populasyon_boyutu):
            indeks1 = np.random.randint(len(uygunluk_degerleri))
            indeks2 = np.random.randint(len(uygunluk_degerleri))
            secilen = indeks1 if uygunluk_degerleri[indeks1] < uygunluk_degerleri[indeks2] else indeks2
            secilenler.append(secilen)
        return secilenler

    def caprazla(self, ebeveyn1, ebeveyn2):
        nokta1 = np.random.randint(len(ebeveyn1))
        nokta2 = np.random.randint(len(ebeveyn1))
        min_nokta = min(nokta1, nokta2)
        max_nokta = max(nokta1, nokta2)
        cocuk1 = np.concatenate((ebeveyn1[:min_nokta], ebeveyn2[min_nokta:max_nokta], ebeveyn1[max_nokta:]))
        cocuk2 = np.concatenate((ebeveyn2[:min_nokta], ebeveyn1[min_nokta:max_nokta], ebeveyn2[max_nokta:]))
        return cocuk1, cocuk2

    def mutasyon(self, birey):
        for i in range(len(birey)):
            if np.random.rand() < self.mutasyon_orani:
                birey[i] = 1 - birey[i]
        return birey

    def optimize_et(self):
        for nesil in range(self.maksimum_nesil):
            uygunluk_degerleri = self.uygunluk_hesapla()
            yeni_populasyon = []
            for _ in range(self.populasyon_boyutu // 2):
                secilenler = self.sec(uygunluk_degerleri)
                ebeveyn1, ebeveyn2 = self.populasyon[secilenler[0]], self.populasyon[secilenler[1]]
                cocuk1, cocuk2 = self.caprazla(ebeveyn1, ebeveyn2)
                cocuk1 = self.mutasyon(cocuk1)
                cocuk2 = self.mutasyon(cocuk2)
                yeni_populasyon.append(cocuk1)
                yeni_populasyon.append(cocuk2)
            self.populasyon = np.array(yeni_populasyon)
            if nesil % 10 == 0:
                print("Nesil {}: En iyi çözüm: {}".format(nesil, min(uygunluk_degerleri)))
        en_iyi_birey = self.populasyon[np.argmin(uygunluk_degerleri)]
        en_iyi_cozum = self.amac_fonksiyonu(en_iyi_birey)
        print("En iyi çözüm:", en_iyi_cozum)
        return en_iyi_cozum, en_iyi_birey

    def matris_olustur(self, birey):
        matris = np.zeros((self.n, self.m, self.k))
        for i in range(self.n):
            for d in range(self.m):
                matris[i, d, 0] = birey[i*self.m + d]
                matris[i, d, 1] = birey[self.n*self.m + i*self.m + d]
        return matris

# Parametreler
n = 14  # Hemşire sayısı
m = 28  # Gün sayısı
k = 2  # Vardiya sayısı
u = 9  # Uzman hemşirelerin sayısı
h = 3  # Gece nöbetine kalmayacak hemşirelerin sayısı

# Genetik Algoritma'nın kullanılması
genetik_algoritma = GenetikAlgoritma(n, m, k, u, h)
en_iyi_cozum, en_iyi_birey = genetik_algoritma.optimize_et()
matris = genetik_algoritma.matris_olustur(en_iyi_birey)

# Şubat 2015 takvimine göre düzenleme ve çıktı
gunduz_vardiya = ["08`16", "izinli"]
gece_vardiya = ["16`08"]

print("01.02.2015 Pazar'dan başlayan 28 günlük hemşire nöbet çizelgesi:\n")

days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]
dates = [f"{str(i+1).zfill(2)}.02.2015" for i in range(28)]

hafta_sayisi = 4

# Haftalık çizelge oluştur
for week in range(hafta_sayisi):
    print(f"Hafta {week+1}:\n")
    data = {"Hemşireler": [f"Hemşire {i+1}" for i in range(n)]}
    for d in range(week*7, (week+1)*7):
        data[dates[d]] = []
        for i in range(n):
            if matris[i, d, 0] == 1:
                data[dates[d]].append(gunduz_vardiya[0])
            elif matris[i, d, 1] == 1:
                data[dates[d]].append(gece_vardiya[0])
            else:
                data[dates[d]].append(gunduz_vardiya[1])

    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    print("\n" + "="*50 + "\n")
     
       
