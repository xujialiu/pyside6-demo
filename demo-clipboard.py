from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QClipboard
import sys

class ClipboardDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.label = QLabel("剪切板内容将显示在这里", self)
        self.button = QPushButton("显示剪切板内容", self)
        self.button.clicked.connect(self.show_clipboard_content)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle("剪切板示例")

    def show_clipboard_content(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        self.label.setText(clipboard_text)

def main():
    app = QApplication(sys.argv)
    demo = ClipboardDemo()
    demo.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
