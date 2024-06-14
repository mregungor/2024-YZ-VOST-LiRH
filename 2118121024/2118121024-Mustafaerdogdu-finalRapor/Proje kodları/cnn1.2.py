import tensorflow
from tensorflow.keras.utils import Sequence

# VGG16 önceden eğitilmiş model
conv_base =  tensorflow.keras.applications.VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(224, 224, 3)
                  )

# 'block5_conv1'e kadar (dahil) katmanları dondur
for layer in conv_base.layers:
    if layer.name in ['block5_conv1']:  # 'block5_conv1'e kadar ve dahil olmak üzere dondur
        layer.trainable = True
        break  # İstenen katmanları dondurduktan sonra döngüden çık
    else:
        layer.trainable = False
conv_base.summary()

print("conv_base.layers:")
for layer in conv_base.layers:
    layer_output = layer.output
    print(layer.name, layer_output.shape)

# Son modeli oluştur
model = tensorflow.keras.models.Sequential()
model.add(conv_base)

# Düzleştir ve yoğun katmanlar ekle
model.add(tensorflow.keras.layers.Flatten())
model.add(tensorflow.keras.layers.Dense(256, activation='relu'))
model.add(tensorflow.keras.layers.Dense(6, activation='softmax'))

# Modeli derle
model.compile(loss='binary_crossentropy',
              optimizer=tensorflow.keras.optimizers.RMSprop(learning_rate=1e-5),
              metrics=['acc'])

# Model özeti
model.summary()


class PyDataset(Sequence):
    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size

    def __len__(self):
        return len(self.data) // self.batch_size

    def __getitem__(self, idx):
        batch_data = self.data[idx * self.batch_size: (idx + 1) * self.batch_size]
        return batch_data, None  # Etiketler için None döndürüyoruz çünkü bu sadece bir örnek

    def on_epoch_end(self):
        pass  # Opsiyonel olarak epoch sonunda yapılacak işlemler burada yapılabilir
        

        
        
        
# Defining the directories that data are in.
EGITIM_YOLU = 'veriler/EGİTİM'
GECERLEME_YOLU = 'veriler/GECERLEME'
TEST_YOLU = 'veriler/TEST'

# We need to apply data augmentation methods to prevent overfitting.
train_datagen = tensorflow.keras.preprocessing.image.ImageDataGenerator(
      rescale=1./255, # piksel değerleri 0-255'den 0-1 arasına getiriliyor.
      rotation_range=40, # Görüntüleri rastgele döndürür.
      width_shift_range=0.2,# Görüntüleri yatay olarak kaydırır.
      height_shift_range=0.2,# Görüntüleri dikey olarak kaydırır.
      shear_range=0.2,# Görüntüleri eğri hale getirir.
      zoom_range=0.2,# Görüntüleri yakınlaştırır veya uzaklaştırır.
      horizontal_flip=True, # Görüntüleri yatay olarak çevirir.
      fill_mode='nearest'# Dönüştürme sırasında boşlukları en yakın piksel değeri ile doldurur.
      )


train_generator = train_datagen.flow_from_directory(
        EGITIM_YOLU,
        target_size=(224, 224),
        batch_size=20,
        )

# To validate the training process, we do not need augmented images.
validation_datagen = tensorflow.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255
        )

validation_generator = validation_datagen.flow_from_directory(
        GECERLEME_YOLU,
        target_size=(224, 224),
        batch_size=20,
        )

# Training the model.
EGITIM_TAKIP = model.fit(
      train_generator,
      steps_per_epoch=5,
      epochs=7,
      validation_data=validation_generator,
      validation_steps=1)


# Saving the trained model to working directory.
model.save('my_model.h5')
model.save('my_model.keras')
model.save('manzara_tf_model.h5')



# To test the trained model, we do not need augmented i mages.
test_datagen = tensorflow.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255
        )

test_generator = test_datagen.flow_from_directory(
        TEST_YOLU,
        target_size=(224, 224),
        batch_size=10,
        )

# Printing the test results.
test_loss, test_acc = model.evaluate(test_generator, steps=20)
print('test acc:', test_acc)