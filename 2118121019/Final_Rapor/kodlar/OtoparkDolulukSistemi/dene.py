from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# YOLO modelini yükle
model = YOLO('best.pt')

# Nesne tespiti yap
results = model('2012-10-11_07_36_48.jpg')

# Görüntüyü yükle
image = plt.imread('2012-10-11_07_36_48.jpg')

# Görüntüyü göster
plt.figure(figsize=(10, 10))
plt.imshow(image)

# Tespit sonuçlarını işle
for det in results[0].boxes:
    xmin, ymin, xmax, ymax = det.xyxy[0].tolist()
    conf = det.conf.item()
    cls = det.cls.item()
    
    # Kırmızı kutu çiz
    rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=2, edgecolor='r', facecolor='none')
    
    # Kırmızı kutuyu görüntüye ekle
    plt.gca().add_patch(rect)
    
    # Sınıf etiketini ve güven değerini yazdır
    plt.text(xmin, ymin - 5, f'{1},{conf:.2f}', fontsize=8, color='b')

# Eksenleri kapat
plt.axis('off')

# Görüntüyü göster
plt.show()
