# 显示每秒增加1的app
import sys
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

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

    window = CounterWindow()
    window.show()

    sys.exit(app.exec())
