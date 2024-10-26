import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsBlurEffect, QGraphicsOpacityEffect

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Transparent Hello World")
        self.setGeometry(100, 100, 400, 200)
        
        # Make window frameless and stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Enable transparency
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create and style the label
        self.label = QLabel("Hello, World!", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: rgba(40, 40, 40, 100);
                border-radius: 10px;
            }
        """)
        self.label.setGeometry(0, 0, 400, 200)
        
        # Add blur effect
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)
        self.label.setGraphicsEffect(blur)
        
        # Set window background to be fully transparent
        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec())
