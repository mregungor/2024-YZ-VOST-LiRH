import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from nltk.corpus import stopwords
import nltk
import re
import spacy
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

#spacy.cli.download("en_core_web_sm")

# NLTK'nin gerekli veri kaynaklarını indirin
nltk.download('punkt')
nltk.download('stopwords')

# İngilizce stopwords listesini tanımlayın
en_stopwords = set(stopwords.words('english'))

# SpaCy modelini yükleyin
nlp = spacy.load("en_core_web_sm")


# Metni temizleme fonksiyonunu tanımlayın
def metni_temizle(metin, stopwordler):
    metin = re.sub(r'\$\w*', '', metin)  # Para birimlerini temizle
    metin = re.sub(r'^RT[\s]+', '', metin)  # Retweet işaretlerini temizle
    metin = re.sub(r'https?:\/\/.*[\r\n]*', '', metin)  # URL'leri temizle
    metin = re.sub(r'#', '', metin)  # Hashtag işaretlerini temizle
    metin = re.sub(r':\(\)', '', metin)  # Emojileri temizle
    metin = re.sub(r'[.,!?;:•]', '', metin)  # Noktalama işaretlerini temizle
    
    metin = metin.lower()
    
    # SpaCy ile metni işlemle
    doc = nlp(metin)
    
    # Temizlenmiş kelimeleri saklayacak liste
    temizlenmis_kelimeler = []
    
    # Her kelimeyi kontrol et
    for token in doc:
        if token.text.lower() not in stopwordler and not token.is_punct:
            kelime_koku = token.lemma_  # Kelimenin kökünü al
            temizlenmis_kelimeler.append(kelime_koku)
            
    return ' '.join(temizlenmis_kelimeler)  # Kelimeleri birleştirip tek bir metin olarak döndür

# Kullanıcıdan cümle al
girilen_cumle = input("Lütfen bir cümle girin: ")

# Temizleme işlemini gerçekleştir
temizlenmis_cümle = metni_temizle(girilen_cumle, en_stopwords)

# Kelime vektörlerini oluşturma
def kelime_vektorleri_olustur(metin):
    doc = nlp(metin)
    kelime_vektorleri = [token.vector for token in doc if not token.is_punct and not token.is_stop]
    return kelime_vektorleri

kelime_vektorleri = kelime_vektorleri_olustur(temizlenmis_cümle)
print("promt Vektörü:")
for vektor in kelime_vektorleri:
    print(vektor)

def text_to_vectors(text, vector_size=100, window=5, min_count=1, sg=1):
    # Metni kelime düzeyinde tokenize etme
    tokens = word_tokenize(text.lower())  # Küçük harfe dönüştüre
    
    # Word2Vec modelini yaratma ve eğitme
    model = Word2Vec([tokens], vector_size=vector_size, window=window, min_count=min_count, sg=sg)
    
    # Kelimelerin vektörlerini alma
    word_vectors = {}
    for word in tokens:
        word_vectors[word] = model.wv[word]
    
    return word_vectors

access_key = "_i5AeVSLj0W-Fp0DEQg5XIZUBionPUbw4XU1iuSlz3s"  # Buraya aldığınız Unsplash API anahtarını ekleyin
search_url = "https://api.unsplash.com/search/photos"

# Görselleri indirme ve gösterme fonksiyonu
def fetch_and_display_images(kelime):
    plt.figure(figsize=(15, 10))
    try:
        # API sorgusu yap
        params = {"query": kelime, "client_id": access_key}
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        
        # İlk görseli al
        if "results" in search_results and len(search_results["results"]) > 0:
            image_url = search_results["results"][0]["urls"]["regular"]
            
            # Görseli indir
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image = Image.open(BytesIO(image_response.content))
            
            # Görseli göster
            plt.imshow(image)
            plt.title(kelime)
            plt.axis("off")
        else:
            print(f"{kelime} için görsel bulunamadı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        
    plt.show()
    #print("kelime:", kelime)
    # Metni vektörlere dönüştürme
    vectors = text_to_vectors(kelime)

    # Her kelimenin vektörünü gösterme
    #for word, vector in vectors.items():
        #print(f"{word}: {vector}")
# Görselleri indir ve göster
fetch_and_display_images(temizlenmis_cümle)

