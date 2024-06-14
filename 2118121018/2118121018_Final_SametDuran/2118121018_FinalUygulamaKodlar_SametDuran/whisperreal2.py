
import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform


def main():
    parser = argparse.ArgumentParser() # Bir ArgümanParser nesnesi oluşturur, bu, komut satırı argümanlarını işlemek için kullanılacak.
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=1,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=1,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args() # Komut satırı argümanlarını analiz eder ve bunları args adlı bir nesneye dönüştürür.

    # Kuyruktan bir kayıt alındığı son zaman.
    phrase_time = None # Bu, son ses parçasının zamanını tutmak için bir değişken tanımlar.

    # İş parçacığı kaydı geri aramasından veri aktarmak için güvenli iş parçacığı kuyruğu.
    data_queue = Queue() # Bu, ses verilerini geçici olarak depolamak için bir kuyruk oluşturur.

    # Konuşma sona erdiğinde algılayabilen güzel bir özelliği olduğu için Ses Tanıyıcı'yı sesimizi kaydetmek için kullanıyoruz.
    recorder = sr.Recognizer() #Bu, SpeechRecognition kütüphanesinden bir Tanıyıcı nesnesi oluşturur. Bu, sesi metne dönüştürmek için kullanılacak.
    recorder.energy_threshold = args.energy_threshold # Bu, mikrofonun ne kadar gürültü algılayacağını belirler. Bu, ses kaydının ne zaman başlayıp duracağını etkiler.

    # Kesinlikle bunu yapın; dinamik enerji telafisi, enerji eşiğini, SpeechRecognizer'ın kaydı asla durdurmadığı bir noktaya kadar önemli ölçüde düşürür.
    recorder.dynamic_energy_threshold = False # Bu, dinamik enerji eşiğini kapatır. Bu, enerji eşiğinin otomatik olarak ayarlanmasını engeller.

    # Important for linux users.
    # Yanlış Mikrofonun kullanılması nedeniyle uygulamanın kalıcı olarak kilitlenmesini ve çökmesini önler
    if 'linux' in platform: # Eğer işletim sistemi Linux ise bu kod bloğunu çalıştırır. Linux'a özgü bazı ayarları yapmak için kullanılır.
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=16000) # Bu, mikrofonu başlatır ve ses verilerini 16kHz örnekleme hızıyla alır.

    # Load / Download model
    model = args.model # Bu, kullanılacak modeli seçer.
    if args.model != "small" and not args.non_english:
        model = model + ".en"
    audio_model = whisper.load_model(model) # Bu, belirtilen modeli yükler.

    record_timeout = args.record_timeout # Bu, ses kaydının ne kadar süreyle devam edeceğini belirler.
    phrase_timeout = args.phrase_timeout

    transcription = [''] # Bu, metin transkripsiyonunu depolamak için bir liste oluşturur.

    with source: # Bu, mikrofon kaynağının bir kontekst içinde kullanılmasını sağlar.
        recorder.adjust_for_ambient_noise(source) # Bu, çevresel gürültüyü ölçer ve kaydın kalitesini artırmak için mikrofon ayarlarını buna göre ayarlar.

    def record_callback(_, audio:sr.AudioData) -> None: # Bu, ses verilerinin kaydedilmesi tamamlandığında çağrılacak bir geri çağrı işlevini tanımlar.
        """
        Kayıtlar bittiğinde ses verilerini almak için geri arama işlevi.
        ses: Kaydedilen baytları içeren bir AudioData.
        """
        # Ham baytları alın ve iş parçacığı güvenli kuyruğuna itin.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Bize ham ses baytlarını iletecek bir arka plan iş parçacığı oluşturun.
    # Bunu manuel olarak da yapabiliriz ancak SpeechRecognizer güzel bir yardımcıdır.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout) # Bu, arka planda sesi dinlemeyi başlatır.

    # Kullanıcıya başlamaya hazır olduğumuzu belirtin.
    print("Model loaded.\n")


    while True:
        try:
            now = datetime.utcnow()
            # Ham kayıtlı sesi kuyruktan alın.
            if not data_queue.empty():
                phrase_complete = False
                # Kayıtlar arasında yeterli süre geçtiyse cümlenin tamamlandığını düşünün.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                # Bu, kuyruktan yeni ses verilerini aldığımız son seferdir.
                phrase_time = now
                
                # Sıradaki ses verilerini birleştirin
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                
                # RAM içi arabelleği, geçici dosyaya ihtiyaç duymadan modelin doğrudan kullanabileceği bir şeye dönüştürün.
                # Verileri 16 bit genişliğinde tam sayılardan 32 bit genişliğinde kayan noktaya dönüştürün.
                # Ses akışı frekansını, PCM dalga boyuyla uyumlu varsayılan maksimum 32768hz'ye sabitleyin.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Transkripsiyonu okuyun.
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                output_file_path = "whisperreal.txt"
                with open("whisperreal.txt", "a", encoding="utf-8") as file:
                    file.write(text + "\n")




                # Kayıtlar arasında bir duraklama tespit edersek transkripsiyonumuza yeni bir öğe ekleyin.
                # Aksi takdirde mevcut olanı düzenleyin.
                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                # Güncellenen transkripsiyonu yeniden yazdırmak için konsolu temizleyin.
                os.system('cls' if os.name=='nt' else 'clear')
                for line in transcription:
                    print(line)
                # "Standart çıktıyı boşaltın."
                print('', end='', flush=True)

                # "Sonsuz döngüler işlemciler için zararlıdır, uyumalıdırlar."
                sleep(0.25)
        except KeyboardInterrupt:
            break



    print("\n\nTranscription:")
    for line in transcription:
        print(line)


if __name__ == "__main__": # Bu, programın doğrudan çalıştırılıp çalıştırılmadığını kontrol eder. Eğer doğrudan çalıştırılıyorsa, main() fonksiyonunu çağırır.
    main()