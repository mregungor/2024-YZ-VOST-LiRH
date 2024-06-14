from urllib.request import urlopen
from bs4 import BeautifulSoup
import string


#metin kazıma
source = urlopen("https://www.egitimsistem.com/da-vincinin-sifresi-kitabinin-ozeti-14314h.htm#:~:text=Da%20Vinci'nin%20%C5%9Eifresi%20Kitap,esrarengiz%20bir%20cinayete%20kurban%20gitmi%C5%9Ftir.&text=Kap%C4%B1%20%C3%A7ald%C4%B1%20ve%20Te%C4%9Fmen%20Collet,kendisinin%20onunla%20birlikte%20gelmesini%20istedi.").read()
soup = BeautifulSoup(source, "lxml")
print(set([text.parent.name for text in soup.find_all(text=True)]))

#HTML belgesinden metin içeriğini çekmek.
text = ""

for paragraph in soup.find_all("span"):
    text += paragraph.text
    
for paragraph in soup.find_all("p"):
    text += paragraph.text
    
print(text)

#karekter küçültme
def corpus_lower(corpus):
    corpus = corpus.lower()
    return corpus

text = corpus_lower(text)
print(text)

#noktalama kaldırma
def remove_punctuation(text):
    no_punc = [words for words in text if words not in string.punctuation]
    word_wo_punc = "".join(no_punc)
    return word_wo_punc

text = remove_punctuation(text)
print(text)

#numeric ifade kaldır
def remove_numeric(corpus):
    output = ''.join(words for words in corpus if not words.isdigit())
    return output

text = remove_numeric(text)
text = text.replace("°c","")
print(text)

#Şimdi de elimizdeki text’i işlemlere alabilmek adına parçalara ayırıyoruz. Bunu da split() modülü ile gerçekleştiriyoruz
text = text.split()
text

#tr stopwordler için kod 
source = urlopen("https://github.com/stopwords-iso/stopwords-tr/blob/master/stopwords-tr.txt").read()
soup = BeautifulSoup(source, "lxml")
print(set([text.parent.name for text in soup.find_all(text=True)]))

#stopwords kaldırma
stopwords = ''

for paragraph in soup.find_all("tr"):
    stopwords += paragraph.text
    
stopwords = stopwords.split()
stopwords

#texten stopwords silme
filtered_text = []

for word in text:
    if word not in stopwords:
        filtered_text.append(word)

filtered_text


#wordcloud oluşturma 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image

sentence = []

for i in filtered_text:
    sentence.append(i)
    
text_ = " ".join(map(str, sentence)) 

wordcloud = WordCloud(width = 3000, 
                      height = 3000, 
                      max_font_size = 300, 
                      colormap = "twilight_shifted").generate(text_)

plt.figure(figsize = (20,17))
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.show()

#Bu şablonu buraya alarak bunun üzerine kelime bulutu oluşturacağım.
movie_mask = np.array(Image.open("monalisa.jpg"))
movie_mask

#Ek olarak yapmamız gereken tek şey mask parametresine oluşturduğumuz movie_mask değişkenini atamak.
wordcloud = WordCloud(width = 3000, 
                      height = 3000, 
                      max_font_size = 300, 
                      mask = movie_mask, 
                      colormap = "twilight_shifted").generate(text_)

plt.figure(figsize = (20,17))
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.show()

#Şimdi ise kelimeleri modele alabilmek için tekrar bir split etme işlemi uygularak tokenize ediyoruz
corpus = []

for cumle in filtered_text:
    corpus.append(cumle.split())
    
corpus

#w2w model kurma . Skip-gram algoritmasına göre kuruldu. 
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

model = Word2Vec(corpus, vector_size = 150, window = 2, min_count = 1, sg = 1)
model

#modelde bulunan kelimeler
vocab = list(model.wv.index_to_key)
print(vocab)

#Modelimizi kurduk. Şimdi modelin içerisinden satanlar kelimesinin vektör yapısını inceleyelim.
vector = model.wv['satanlar']
print(vector)

#Şimdi de sırası ile satanlar,kelimelerine en yakın 10 kelimeyi listeyerek modelimizin sonuçlarını inceleyelim.
model.wv.most_similar("satanlar")



def closestwords_tsneplot(model, word):
    # Belirtilen kelimenin en yakın kelimelerini bulma
    close_words = model.wv.most_similar(word)
    
    # Ana kelimeyi ve en yakın kelimeleri bir listeye ekleme
    words = [word] + [w for w, _ in close_words]
    
    # Bu kelimelerin vektörlerini alma
    vectors = [model.wv[w] for w in words]
    
    # Vektörleri numpy dizisine dönüştürme
    vectors = np.array(vectors)
    
    # t-SNE uygulama
    tsne_model = TSNE(perplexity=min(30, len(words)-1), n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(vectors)
    
    # x ve y eksenlerini alma
    x = [value[0] for value in new_values]
    y = [value[1] for value in new_values]
    
    # Grafik oluşturma
    plt.figure(figsize=(16, 16)) 
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(words[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()

# closestwords_tsneplot fonksiyonunu çağırma
closestwords_tsneplot(model, "yüz")

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

# Kullanıcıdan metni al
user_text = input("Lütfen metni girin: ")

# Metni vektörlere dönüştürme
vectors = text_to_vectors(user_text)

# Her kelimenin vektörünü gösterme
for word, vector in vectors.items():
    print(f"{word}: {vector}")




##baslıyor    
import spacy
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Doğrudan yükleme yolu
spacy.cli.download("en_core_web_md")

# Modeli yükle
nlp = spacy.load("en_core_web_md")

# Kullanıcıdan metni al
user_text = input("Lütfen metni girin: ")

# Metni vektörlere dönüştürme
doc = nlp(user_text)
vectors = {token.text: token.vector for token in doc if not token.is_stop and not token.is_punct}

# Vektörleri WordCloud ile görselleştirme
word_freq = {word: vector.mean() for word, vector in vectors.items()}
wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_freq)

# Görüntüyü gösterme
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
##bitti

##baslıyor
import spacy
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

print("********")
# SpaCy modelini yükle
nlp = spacy.load("en_core_web_md")

# Kullanıcıdan metni al
user_text = input("Lütfen metni girin: ")

# Metnin boş olup olmadığını kontrol et
if not user_text.strip():
    raise ValueError("Metin boş olamaz. Lütfen geçerli bir metin girin.")

# Metni vektörlere dönüştürme
doc = nlp(user_text)
vectors = {token.text: token.vector for token in doc if not token.is_stop and not token.is_punct}

# Kelime vektörlerinin boş olup olmadığını kontrol et
if not vectors:
    raise ValueError("Geçerli vektörler bulunamadı. Lütfen daha fazla kelime içeren bir metin girin.")

# Vektörleri iki boyuta indirge
words = list(vectors.keys())
word_vectors = list(vectors.values())

# Vektörlerin boyutunu kontrol et
if len(word_vectors) == 0 or len(word_vectors[0]) == 0:
    raise ValueError("Vektörler doğru bir şekilde alınamadı. Lütfen geçerli bir metin girin.")

# PCA kullanarak iki boyuta indirge
pca = PCA(n_components=2)
pca_result = pca.fit_transform(word_vectors)

# Görselleştirme
plt.figure(figsize=(10, 5))
plt.scatter(pca_result[:, 0], pca_result[:, 1], c='blue')

# Kelime etiketlerini ekleme
for i, word in enumerate(words):
    plt.annotate(word, (pca_result[i, 0], pca_result[i, 1]))

plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Word Vectors PCA Visualization")
plt.show()
##bitti
print("********")
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Unsplash API anahtarınızı buraya ekleyin
access_key = "_i5AeVSLj0W-Fp0DEQg5XIZUBionPUbw4XU1iuSlz3s"  # Buraya aldığınız Unsplash API anahtarını ekleyin
search_url = "https://api.unsplash.com/search/photos"

# Kullanıcıdan metni al
user_text = input("Lütfen metni girin: ")

# Metni kelimelere böl
words = user_text.split()

# Görselleri indirme ve gösterme fonksiyonu
def fetch_and_display_images(words):
    plt.figure(figsize=(15, 10))
    for i, word in enumerate(words):
        try:
            # API sorgusu yap
            params = {"query": word, "client_id": access_key}
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
                plt.subplot(1, len(words), i + 1)
                plt.imshow(image)
                plt.title(word)
                plt.axis("off")
            else:
                print(f"{word} için görsel bulunamadı.")
        except Exception as e:
            print(f"Hata oluştu: {e}")
    
    plt.show()

# Görselleri indir ve göster
fetch_and_display_images(words)






