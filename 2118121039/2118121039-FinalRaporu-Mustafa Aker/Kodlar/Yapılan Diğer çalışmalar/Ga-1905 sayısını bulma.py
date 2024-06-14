import random
# Parametreler
populasyon_boyutu = 10
mutasyon_orani = 0.5
nesil_sayisi = 1000
# Hedef sayı
hedef_sayi = 1905

# Başlangıç popülasyonu oluşturma
def birey_olustur(uzunluk):
    return [random.randint(0, 9) for _ in range(uzunluk)]

# Uygunluk (fitness) hesaplama
def uygunluk_hesapla(birey):
    uygunluk = 0
    for i in range(len(birey)):
        uygunluk += abs(birey[i] - int(str(hedef_sayi)[i]))
    return uygunluk

# Çaprazlama
def caprazlama(ebeveyn1, ebeveyn2):
    caprazlama_noktasi = random.randint(1, len(ebeveyn1) - 1)
    cocuk1 = ebeveyn1[:caprazlama_noktasi] + ebeveyn2[caprazlama_noktasi:]
    cocuk2 = ebeveyn2[:caprazlama_noktasi] + ebeveyn1[caprazlama_noktasi:]
    return cocuk1, cocuk2

# Mutasyon
def mutasyon(birey, mutasyon_orani):
    for i in range(len(birey)):
        if random.random() < mutasyon_orani:
            birey[i] = random.randint(0, 9)
    return birey

# Genetik algoritma
def genetik_algoritma(populasyon_boyutu, mutasyon_orani, nesil_sayisi):
    populasyon = [birey_olustur(len(str(hedef_sayi))) for _ in range(populasyon_boyutu)]

    for nesil in range(nesil_sayisi):
        populasyon = sorted(populasyon, key=lambda x: uygunluk_hesapla(x))
        en_iyi_birey = populasyon[0]
        print(f"Nesil {nesil + 1} - En İyi Birey: {''.join(map(str, en_iyi_birey))}, Uygunluk: {uygunluk_hesapla(en_iyi_birey)}")

        if uygunluk_hesapla(en_iyi_birey) == 0:
            print("Hedef sayı bulundu:", ''.join(map(str, en_iyi_birey)))
            return en_iyi_birey

        yeni_nesil = []

        for _ in range(populasyon_boyutu // 2):
            ebeveyn1 = random.choice(populasyon)
            ebeveyn2 = random.choice(populasyon)
            cocuk1, cocuk2 = caprazlama(ebeveyn1, ebeveyn2)
            cocuk1 = mutasyon(cocuk1, mutasyon_orani)
            cocuk2 = mutasyon(cocuk2, mutasyon_orani)
            yeni_nesil.extend([cocuk1, cocuk2])

        populasyon = yeni_nesil

    print("Belirli nesil sayısına ulaşıldı ancak hedef sayı bulunamadı.")
    en_iyi_birey = min(populasyon, key=lambda x: uygunluk_hesapla(x))
    print("En yakın sayı:", ''.join(map(str, en_iyi_birey)))
    return en_iyi_birey



# Genetik algoritma çalıştırma
genetik_algoritma(populasyon_boyutu, mutasyon_orani, nesil_sayisi)
