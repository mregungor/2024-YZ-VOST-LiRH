from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import os

def veriCekme(root):
    dikdortgen_kose_noktalari = []
    ids = []
    for space in root.findall('.//space'):
        ids.append(space.get('id'))
        occupied = int(space.get('occupied'))
        points = space.findall('.//contour/point')
        koordinatlar = [(float(point.get('x')), float(point.get('y'))) for point in points]
        if occupied == 1:
            dikdortgen_kose_noktalari.append(koordinatlar)
        else:
            dikdortgen_kose_noktalari.append(None)
    return dikdortgen_kose_noktalari, ids

def dikdortgenYapma(image, dikdortgen_kose_noktalari, ids, det_kose_noktalari):
    plt.imshow(image)
    for det_koordinatlar, koordinatlar, id in zip(det_kose_noktalari, dikdortgen_kose_noktalari, ids):
        if det_koordinatlar:
            points = np.array(det_koordinatlar)
            points = np.concatenate([points, [points[0]]])
            plt.plot(points[:, 0], points[:, 1], color='red', linewidth=2)
        else:
            points = np.array(koordinatlar)
            points = np.concatenate([points, [points[0]]])
            plt.plot(points[:, 0], points[:, 1], color='green', linewidth=2)
        
        x_center = np.mean(points[:, 0])
        y_center = np.mean(points[:, 1])
        plt.text(x_center, y_center, 1"", fontsize=7, color='black', ha='center')

# YOLO modelini yükle
model = YOLO('best.pt')

# Klasördeki her bir resmi işle
image_folder = "C:/Users/faruk/Desktop/YeniEgitim/egit"
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')][:10]

for image_file in image_files:
    # Görüntüyü yükle
    image_path = os.path.join(image_folder, image_file)
    image = plt.imread(image_path)

    # Nesne tespiti yap
    results = model(image_path)

    # Tespit sonuçlarını işle
    det_kose_noktalari = []
    for det in results[0].boxes:
        xmin, ymin, xmax, ymax = det.xyxy[0].tolist()
        if xmin == 0 and ymin == 0 and xmax == 0 and ymax == 0:
            det_kose_noktalari.append(None)
        else:
            det_kose_noktalari.append([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])

    # XML dosyasını yükle
    xml_file = image_file.replace('.jpg', '.xml')
    xml_path = os.path.join(image_folder, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Veriyi al
    dikdortgen_kose_noktalari, ids = veriCekme(root)

    # Dikdörtgenleri çiz
    dikdortgenYapma(image, dikdortgen_kose_noktalari, ids, det_kose_noktalari)

    plt.axis('off')
    plt.show()
