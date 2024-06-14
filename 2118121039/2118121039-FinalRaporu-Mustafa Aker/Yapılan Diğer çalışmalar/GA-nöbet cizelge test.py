import numpy as np
from datetime import datetime, timedelta

class GenetikAlgoritma:
    def __init__(self, n, m, k, u, h):
        self.n = n  # Hemşire sayısı
        self.m = m  # Gün sayısı
        self.k = k  # Vardiya sayısı
        self.u = u  # Uzman hemşire sayısı
        self.h = h  # Gece nöbetine kalmayacak hemşire sayısı
        self.populasyon_boyutu = 100 # Popülasyon boyutu
        self.maksimum_nesil = 200  # Maksimum nesil sayısı
        self.mutasyon_orani = 1.5 # Mutasyon oranı
        self.populasyon = self.populasyon_olustur()

    def amac_fonksiyonu(self, X):
        """
        Amaç fonksiyonu: Çalışma sürelerinin minimizasyonu
        """
        fmin = 0
        for i in range(self.n):
            for d in range(self.m):
                fmin += 8 * X[i*self.m + d] + 16* X[self.n*self.m + i*self.m + d]
        return fmin

    def kisitlar(self, X):
        """
        Kısıtlar
        """
        kisitlar = []
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
        return kisitlar

    def populasyon_olustur(self):
        """
        Başlangıç populasyonunu oluştur
        """
        return np.random.randint(2, size=(self.populasyon_boyutu, self.n*(self.m*2)))

    def uygunluk_hesapla(self):
        """
        Popülasyon için uygunluk değerlerini hesapla
        """
        uygunluk_degerleri = []
        for birey in self.populasyon:
            uygunluk_degerleri.append(self.amac_fonksiyonu(birey))
        return uygunluk_degerleri

    def sec(self, uygunluk_degerleri):
        """
        Seçim işlemi
        """
        ters_uygunluk = np.max(uygunluk_degerleri) - uygunluk_degerleri + 1
        return np.random.choice(range(len(self.populasyon)), size=self.populasyon_boyutu, 
                                replace=True, p=(ters_uygunluk / np.sum(ters_uygunluk)))

    def caprazla(self, ebeveyn1, ebeveyn2):
        """
        Çaprazlama işlemi
        """
        nokta = np.random.randint(len(ebeveyn1))
        cocuk1 = np.concatenate((ebeveyn1[:nokta], ebeveyn2[nokta:]))
        cocuk2 = np.concatenate((ebeveyn2[:nokta], ebeveyn1[nokta:]))
        return cocuk1, cocuk2

    def mutasyon(self, birey):
        """
        Mutasyon işlemi
        """
        for i in range(len(birey)):
            if np.random.rand() < self.mutasyon_orani:
                birey[i] = 1 - birey[i]
        return birey

    def optimize_et(self):
        """
        Genetik algoritmayı çalıştır ve en iyi çözümü bul
        """
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

        uygunluk_degerleri = self.uygunluk_hesapla() # Tekrar hesaplamak gerekebilir
        en_iyi_birey = self.populasyon[np.argmin(uygunluk_degerleri)]
        en_iyi_cozum = self.amac_fonksiyonu(en_iyi_birey)
        print("En iyi çözüm:", en_iyi_cozum)
        return en_iyi_cozum, en_iyi_birey

    def hemshire_cizelgesi(self, birey):
        """
        Hemşire çizelgesini tablo olarak oluştur
        """
        gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        simdi = datetime.now()
        haftanin_gunleri = [(simdi + timedelta(days=i)).strftime('%Y-%m-%d %A') for i in range(self.m)]
        tablo = np.zeros((self.n, self.m, 2), dtype=int)  # 2: gündüz ve gece vardiyası

        for i in range(self.n):
            for d in range(self.m):
                tablo[i, d, 0] = birey[i*self.m + d]
                tablo[i, d, 1] = birey[self.n*self.m + i*self.m + d]

        print("Hemşire Çizelgesi (Gündüz: 1, Gece: 2):")
        for d in range(self.m):
            print("\nTarih:", haftanin_gunleri[d])
            for i in range(self.n):
                vardiya = "Gündüz" if tablo[i, d, 0] == 1 else ("Gece" if tablo[i, d, 1] == 1 else "Yok")
                print(f"Hemşire {i+1}: {vardiya}")
        return tablo

# Parametreler
n = 5 # Hemşire sayısı
m = 7   # Gün sayısı
k = 2   # Vardiya sayısı
u = 1   # Uzman hemşirelerin sayısı
h = 3   # Gece nöbetine kalmayacak hemşirelerin sayısı

# Genetik Algoritma'nın kullanılması
genetik_algoritma = GenetikAlgoritma(n, m, k, u, h)
en_iyi_cozum, en_iyi_birey = genetik_algoritma.optimize_et()
genetik_algoritma.hemshire_cizelgesi(en_iyi_birey)
