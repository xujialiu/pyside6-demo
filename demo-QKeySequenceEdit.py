# 利用QKeySequence设置快捷键, 并用pynput监听全局快捷键
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QKeySequenceEdit
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import Qt
from pynput import keyboard

class HotkeyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.hotkey = None
        self.counter = 0
        self.listener = None

    def initUI(self):
        self.setWindowTitle("Hotkey Counter")
        
        self.layout = QVBoxLayout()
        
        # 定义label
        self.label = QLabel("0", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.label)
        
        # 定义keySequenceEdit
        self.keySequenceEdit = QKeySequenceEdit(self)
        self.layout.addWidget(self.keySequenceEdit)
        
        # 定义setHotkeyButton
        self.setHotkeyButton = QPushButton("Set Hotkey", self)
        self.setHotkeyButton.clicked.connect(self.setHotkey)    # 
        self.layout.addWidget(self.setHotkeyButton)
        
        self.setLayout(self.layout)
        
    def setHotkey(self):
        key_sequence = self.keySequenceEdit.keySequence().toString(QKeySequence.NativeText)
        if key_sequence:
            if self.listener:
                self.listener.stop()
            self.hotkey = self.parseHotkey(key_sequence)
            self.listener = keyboard.GlobalHotKeys({self.hotkey: self.incrementCounter})
            self.listener.start()
    
    def parseHotkey(self, key_sequence):
        key_map = {
            'Ctrl': '<ctrl>',
            'Alt': '<alt>',
            'Shift': '<shift>',
            'Meta': '<cmd>',
        }
        keys = key_sequence.split('+')
        parsed_keys = []
        for key in keys:
            key = key.strip()
            if key in key_map:
                parsed_keys.append(key_map[key])
            else:
                parsed_keys.append(key.lower())
        return '+'.join(parsed_keys)
    
    def incrementCounter(self):
        self.counter += 1
        self.label.setText(str(self.counter))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = HotkeyApp()
    demo.show()
    sys.exit(app.exec())
