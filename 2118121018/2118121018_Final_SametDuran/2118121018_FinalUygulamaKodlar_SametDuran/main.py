import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap
import subprocess

class FileOpenerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sesten Yazıya Çevirme')
        
        window_width = 500
        window_height = 350

        icon = QIcon('icon.jpg')  

        # Pencere simgesini ayarla
        self.setWindowIcon(icon)

        font = QFont()
        font.setPointSize(16)
        font2=QFont()
        font2.setPointSize(20)
        font2.setBold(True)

        # Ekranın genişliği ve yüksekliğini al
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()

        # Pencereyi ekranın ortasına yerleştir
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        sec_label=QLabel("Model Seçiniz:",self)
        sec_label.setFont(font2)
        sec_label.setGeometry(140, 20, 250, 40)
        sec_label.setStyleSheet("color: #cdad00")

        pixmap = QPixmap('icon.jpg')  # Eklenecek resmin dosya yolu
        resim_label = QLabel(self)
        resim_label.setPixmap(pixmap.scaledToWidth(70))  # Genişliği 400'e ölçekle
        resim_label.move(50, 10)  # Resmin konumunu ayarla

        # whisperrealpyqt.py dosyasını açacak buton
        btn_open_whisper = QPushButton('Whisper Real Time Uygulaması', self)
        btn_open_whisper.setFont(font)
        btn_open_whisper.clicked.connect(self.open_whisper)
        btn_open_whisper.setGeometry(50, 100, 400, 40)
        btn_open_whisper.setStyleSheet('''
            QPushButton {
                background-color: blue;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: navy;
            }
        ''')

        # realtimeuyg.py dosyasını açacak buton
        btn_open_realtime = QPushButton('RealtimeSTT Uygulaması', self)
        btn_open_realtime.setFont(font)
        btn_open_realtime.clicked.connect(self.open_realtime)
        btn_open_realtime.setGeometry(50, 175, 400, 40)
        btn_open_realtime.setStyleSheet('''
            QPushButton {
                background-color: red;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: maroon;
            }
        ''')

        btn_open_realtime = QPushButton('Whisper Uygulaması', self)
        btn_open_realtime.setFont(font)
        btn_open_realtime.clicked.connect(self.open_original)
        btn_open_realtime.setGeometry(50, 250, 400, 40)
        btn_open_realtime.setStyleSheet('''
            QPushButton {
                background-color: orange;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #B8860B;
            }
        ''')


    def open_whisper(self):
        try:
            self.close()
            subprocess.Popen(['python', 'whisperrealpyqt2.py'])
        except FileNotFoundError:
            print("whisperrealpyqt.py bulunamadı!")

    def open_realtime(self):
        try:
            self.close()
            subprocess.Popen(['python', 'realtimeuyg.py'])
        except FileNotFoundError:
            print("realtimeuyg.py bulunamadı!")

    def open_original(self):
        try:
            self.close()
            subprocess.Popen(['python', 'whisperoriginal2.py'])
        except FileNotFoundError:
            print("whisperoriginal2.py bulunamadı!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileOpenerApp()
    ex.show()
    sys.exit(app.exec_())
