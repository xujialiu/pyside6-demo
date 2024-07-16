# 利用QProcess, 启动第2个app
import sys
import time
from PySide6.QtCore import QProcess, QTimer, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_process)

        self.pause_resume_button = QPushButton("Pause/Resume", self)
        self.pause_resume_button.setEnabled(False)
        self.pause_resume_button.clicked.connect(self.pause_resume_process)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_resume_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.process = None
        self.paused = False

    def start_process(self):
        if not self.process:
            self.process = QProcess(self)
            self.process.finished.connect(self.process_finished)
            self.process.start("python", ["-u", "demo-QTimer.py"])
            self.pause_resume_button.setEnabled(True)

    def pause_resume_process(self):
        if self.process:
            if not self.paused:
                self.process.kill()
                self.paused = True
            else:
                self.process.start("python", ["-u", "demo-QTimer.py"])
                self.paused = False

    def process_finished(self):
        self.process = None
        self.pause_resume_button.setEnabled(False)

class CounterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Counter Window")
        self.setGeometry(450, 100, 300, 200)

        self.label = QLabel("0", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counter)
        self.timer.start(1000)

    @Slot()
    def update_counter(self):
        self.counter += 1
        self.label.setText(str(self.counter))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    if len(sys.argv) > 1 and sys.argv[1] == "counter":
        counter_window = CounterWindow()
        counter_window.show()

    sys.exit(app.exec())