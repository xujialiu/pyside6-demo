import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import wave
import pyaudio
import threading


class SamplePlayer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

        self.file = "test.mp3"

        self.paused = True
        self.playing = False

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.pause_btn = QPushButton("Pause", self)
        self.pause_btn.clicked.connect(self.pause)
        layout.addWidget(self.pause_btn)

        self.play_btn = QPushButton("Play", self)
        self.play_btn.clicked.connect(self.play)
        layout.addWidget(self.play_btn)

        self.setWindowTitle("Sample Player")
        self.setGeometry(100, 100, 300, 200)

    def start_playing(self):
        p = pyaudio.PyAudio()
        with wave.open(self.file, "rb") as wf:
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )

            data = wf.readframes(wf.getnframes())
            data_len = len(data)
            chunk_size = 1024
            i = 0

            while self.playing and i < data_len:
                if not self.paused:
                    stream.write(data[i : i + chunk_size])
                    i += chunk_size

        self.playing = False
        stream.close()
        p.terminate()

    def pause(self):
        self.paused = True

    def play(self):
        if not self.playing:
            self.playing = True
            threading.Thread(target=self.start_playing, daemon=True).start()
        self.paused = False

    def stop(self):
        self.playing = False

    def closeEvent(self, event):
        self.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    player = SamplePlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
