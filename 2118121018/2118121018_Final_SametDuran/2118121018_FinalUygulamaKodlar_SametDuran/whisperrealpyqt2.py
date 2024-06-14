import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFont
import subprocess
import threading
import queue

class WhisperLiveApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Whisper Real Time")
        self.showMaximized()

        self.is_running = False
        self.process = None
        self.output_queue = queue.Queue()
        icon = QIcon('icon.jpg')
        self.setWindowIcon(icon)

        font = QFont()
        font.setPointSize(16)

        self.start_button = QtWidgets.QPushButton("Başlat")
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.start_whisper)
        self.start_button.setFixedWidth(200)
        self.start_button.setStyleSheet('''
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

        self.stop_button = QtWidgets.QPushButton("Durdur")
        self.stop_button.setFont(font)
        self.stop_button.clicked.connect(self.stop_whisper)
        self.stop_button.setEnabled(False)
        self.stop_button.setFixedWidth(200)
        self.stop_button.setStyleSheet('''
            QPushButton {
                background-color: red;
                color: white;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: lightgray;  /* Devre dışı olduğunda farklı bir arka plan rengi */
                color: gray;  /* Devre dışı olduğunda farklı bir metin rengi */
            }
            QPushButton:hover {
                background-color: maroon;
            }
        ''')

        self.main_Button = QtWidgets.QPushButton("Ana sayfa")
        self.main_Button.setFont(font)
        self.main_Button.clicked.connect(self.main_whisper)
        self.main_Button.setFixedWidth(200)
        self.main_Button.setStyleSheet('''
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
        

        self.status_label = QtWidgets.QLabel("")
        self.status_label.setStyleSheet("color: darkturquoise")
        self.status_label.setFont(font)

        self.cikti_label = QtWidgets.QLabel("Konuşma Çıktısı:")
        self.cikti_label.setFont(font)

        self.terminal_output = QtWidgets.QTextEdit()
        self.terminal_output.setFont(font)
        self.terminal_output.setReadOnly(True)
        #self.terminal_output.setFixedWidth(600) 
        button_layout=QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.main_Button)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(button_layout)
        #layout.addWidget(self.start_button)
        #layout.addWidget(self.stop_button)
        #layout.addWidget(self.main_Button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.cikti_label)
        layout.addWidget(self.terminal_output)

        self.setLayout(layout)

    def start_whisper(self):
        if not self.is_running:
            self.process = subprocess.Popen(["python", "whisperreal2.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
            self.is_running = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText("Whisper Real Time başlatılıyor...")
            self.read_process_output_thread()
            self.main_Button.setEnabled(False)

            QTimer.singleShot(10000, self.change_status_label)

    def change_status_label(self):
        # status_label metnini değiştir
        self.status_label.setText("Whisper Real Time başlatıldı.")
        self.status_label.setStyleSheet("color: green")

    def read_process_output_thread(self):
        def enqueue_output(out, queue):
            for line in iter(out.readline, ''):
                queue.put(line)
            out.close()

        thread = threading.Thread(target=enqueue_output, args=(self.process.stdout, self.output_queue))
        thread.daemon = True
        thread.start()

        self.process_output_queue()

    def process_output_queue(self):
        last_line = None
        while not self.output_queue.empty():
            last_line = self.output_queue.get_nowait()

        if last_line:
            self.terminal_output.insertPlainText(last_line)

        self.terminal_output.moveCursor(QtGui.QTextCursor.End)

        if self.is_running:
            QtCore.QTimer.singleShot(5, self.process_output_queue)

    def stop_whisper(self):
        if self.is_running and self.process:
            self.process.terminate()
            self.is_running = False
            self.process = None
            self.status_label.setText("Whisper Real Time durduruldu.")
            self.status_label.setStyleSheet("color: red")

            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.main_Button.setEnabled(True)

    def main_whisper(self):
        try:
            self.close()
            subprocess.Popen(['python', 'main.py'])
        except FileNotFoundError:
            print("main.py bulunamadı!")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WhisperLiveApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
