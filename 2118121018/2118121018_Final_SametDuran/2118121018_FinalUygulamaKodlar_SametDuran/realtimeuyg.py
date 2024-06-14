import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import QProcess, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
import subprocess

class RealTimeSTTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Real Time STT')
        self.showMaximized()

        icon = QIcon('icon.jpg')  # Icon dosyanızın adını ve yolunu buraya girin

        # Pencere simgesini ayarla
        self.setWindowIcon(icon)

        font=QFont()
        font.setPointSize(16)

        # Başlatma ve Durdurma düğmelerini oluştur
        self.startButton = QPushButton('Başlat', self)
        self.startButton.setFont(font)
        self.startButton.clicked.connect(self.startProcess)
        self.startButton.setFixedWidth(200)
        self.startButton.setStyleSheet('''
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

        self.stopButton = QPushButton('Durdur', self)
        self.stopButton.setFont(font)
        self.stopButton.clicked.connect(self.stopProcess)
        self.stopButton.setEnabled(False)  # Başlangıçta devre dışı bırak
        self.stopButton.setFixedWidth(200)
        self.stopButton.setStyleSheet('''
            QPushButton {
                background-color: red;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: lightgray;  
                color: gray;  
            }
            QPushButton:hover {
                background-color: maroon;
            }
        ''')

        self.mainButton = QPushButton('Ana sayfa', self)
        self.mainButton.setFont(font)
        self.mainButton.clicked.connect(self.mainProcess)
        self.mainButton.setEnabled(True)
        self.mainButton.setFixedWidth(200)
        self.mainButton.setStyleSheet('''
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
        self.ciktiLabel=QLabel("Konuşma Çıktısı:")
        self.ciktiLabel.setFont(font)
        
        # Çıktıları göstermek için metin alanı oluştur
        self.outputTextEdit = QTextEdit(self)
        self.outputTextEdit.setFont(font)
        self.outputTextEdit.setReadOnly(True)
        #self.outputTextEdit.setFixedWidth(600)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.mainButton)


        # Düğmeleri ve metin alanını düzenlemek için düzen oluştur
        layout = QVBoxLayout()
        layout.addLayout(buttonLayout)
        #layout.addWidget(self.startButton)
        #layout.addWidget(self.stopButton)
        #layout.addWidget(self.mainButton)
        layout.addWidget(self.ciktiLabel)
        layout.addWidget(self.outputTextEdit)

        self.setLayout(layout)

    @pyqtSlot()
    def startProcess(self):
        # Yürütülecek betik dosyası
        script_path = 'realtimestt2.py'

        # QProcess kullanarak betiği başlat
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.onReadyRead)
        self.process.start('python', [script_path])

        # Durdurma düğmesini etkinleştir
        self.stopButton.setEnabled(True)
        self.startButton.setEnabled(False)  # Başlatma düğmesini devre dışı bırak
        self.mainButton.setEnabled(False)
    @pyqtSlot()
    def stopProcess(self):
        # Eğer işlem çalışıyorsa, işlemi sonlandır
        if self.process.state() == QProcess.Running:
            self.process.terminate()  # KeyboardInterrupt gönder
            self.process.kill()
            
            text = self.outputTextEdit.toPlainText()
            with open('realtimestt.txt', 'a', encoding='utf-8') as file:
                file.write(text + "\n")

        # Durdurma düğmesini devre dışı bırak, başlatma düğmesini etkinleştir
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.mainButton.setEnabled(True)

    @pyqtSlot()
    def onReadyRead(self):
        # QProcess çıktısını al ve metin alanında göster
        self.outputTextEdit.clear()
        data = self.process.readAllStandardOutput().data().decode('windows-1254')
        self.outputTextEdit.append(data)
    
    @pyqtSlot()
    def mainProcess(self):
        try:
            self.close()
            subprocess.Popen(['python', 'main.py'])
        except FileNotFoundError:
            print("main.py bulunamadı!")

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RealTimeSTTApp()
    window.show()
    sys.exit(app.exec_())
