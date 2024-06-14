import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import whisper
import subprocess

class WhisperApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Whisper Transkripsiyon")
        window_width = 500
        window_height = 500

        icon = QIcon('icon.jpg')
        self.setWindowIcon(icon)

        font = QFont()
        font.setPointSize(16)

        # Ekranın genişliği ve yüksekliğini al
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()

        # Pencereyi ekranın ortasına yerleştir
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        self.label = QLabel("Ses dosyanızı buraya sürükleyip bırakın", self)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed gray;")
        self.label.setAcceptDrops(True)

        self.model_selector = QComboBox(self)
        self.model_selector.addItems(["tiny", "base", "small"])
        self.model_selector.setFont(font)

        self.button = QPushButton("Transkripti Oluştur", self)
        self.button.setFont(font)
        self.button.clicked.connect(self.transcribe_audio)
        self.button.setEnabled(False)
        self.button.setStyleSheet('''
            QPushButton {
                background-color: green;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: lightgray;  
                color: gray;  
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        ''')

        self.Mainbutton = QPushButton("Ana Sayfa", self)
        self.Mainbutton.setFont(font)
        self.Mainbutton.clicked.connect(self.main_whisper)
        self.Mainbutton.setStyleSheet('''
            QPushButton {
                background-color: gray;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: lightgray;  
                color: gray;  
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        ''')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.model_selector)
        layout.addWidget(self.button)
        layout.addWidget(self.Mainbutton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setAcceptDrops(True)
        self.audio_file_path = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): #Bu satır, sürüklenen öğenin bir veya daha fazla URL içerip içermediğini kontrol eder. Bu, sürüklenen öğenin bir dosya olduğunun bir göstergesidir.
            event.acceptProposedAction() #Eğer sürüklenen öğe URL içeriyorsa, bu işlem kabul edilir ve sürükle-bırak işlemi devam eder. Bu, kullanıcının dosyayı pencereye bırakmasına izin verir.

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile() and url.toLocalFile().endswith(('.mp3', '.wav', '.m4a', '.MP3')): #Her URL'nin yerel bir dosya olup olmadığını ve dosya uzantısını kontorl eder
                self.audio_file_path = url.toLocalFile()
                self.label.setText(f"Seçilen dosya: {self.audio_file_path}")
                self.button.setEnabled(True)
                break

    def transcribe_audio(self):
        if self.audio_file_path:
            self.Mainbutton.setEnabled(False)
            self.label.setText("Transkript oluşturuluyor...")
            QApplication.processEvents() #GUI'nin güncellenmesini sağlar, böylece kullanıcı işlemin başladığını hemen görür.

            selected_model = self.model_selector.currentText() #Kullanıcının seçtiği Whisper modelini alır
            model = whisper.load_model(selected_model)
            result = model.transcribe(self.audio_file_path)
            transcription_text = result["text"]

            output_file_path = "output.txt"
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(transcription_text)

            self.label.setText(f"Transkript başarıyla '{output_file_path}' dosyasına kaydedildi.")
            self.Mainbutton.setEnabled(True)
        else:
            self.label.setText("Lütfen geçerli bir ses dosyası sürükleyin ve bırakın.")

    def main_whisper(self):
        try:
            self.close()
            subprocess.Popen(['python', 'main.py'])
        except FileNotFoundError:
            print("main.py bulunamadı!")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WhisperApp()
    main_window.show()
    sys.exit(app.exec_())
