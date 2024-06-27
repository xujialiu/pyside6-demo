import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QThread, Signal, Slot, QMutex, QWaitCondition, Qt


class CounterThread(QThread):
    update_label = Signal(int)

    def __init__(self):
        super().__init__()
        self.count = 0
        self._running = True
        self._paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def run(self):
        while self._running:
            self.mutex.lock()
            if self._paused:
                self.condition.wait(self.mutex)
            self.mutex.unlock()
            self.count += 1
            self.update_label.emit(self.count)
            self.sleep(1)

    def stop(self):
        self._running = False
        self.resume()  # Ensure the thread is not paused when stopping

    def pause(self):
        self.mutex.lock()
        self._paused = True
        self.mutex.unlock()

    def resume(self):
        self.mutex.lock()
        self._paused = False
        self.condition.wakeAll()
        self.mutex.unlock()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread Demo")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("0", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_thread)

        self.pause_resume_button = QPushButton("Pause/Resume", self)
        self.pause_resume_button.clicked.connect(self.pause_resume_thread)
        self.pause_resume_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_resume_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.counter_thread = CounterThread()
        self.counter_thread.update_label.connect(self.update_label)

    @Slot()
    def start_thread(self):
        if not self.counter_thread.isRunning():
            self.counter_thread.start()
            self.start_button.setEnabled(False)
            self.pause_resume_button.setEnabled(True)

    @Slot()
    def pause_resume_thread(self):
        if self.counter_thread._paused:
            self.counter_thread.resume()
            self.pause_resume_button.setText("Pause")
        else:
            self.counter_thread.pause()
            self.pause_resume_button.setText("Resume")

    @Slot(int)
    def update_label(self, count):
        self.label.setText(str(count))

    def closeEvent(self, event):
        if self.counter_thread.isRunning():
            self.counter_thread.stop()
            self.counter_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
