import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Transparent Hello World")
        self.setGeometry(100, 100, 400, 200)
        
        # Make window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Enable transparency
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create and style the label
        label = QLabel("Hello, World!", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        label.setGeometry(0, 0, 400, 200)
        
        # Set window background with blur effect
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(40, 40, 40, 180);
                border-radius: 10px;
            }
        """)

    def mousePressEvent(self, event):
        # Allow window dragging
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        # Implement window dragging
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        # Close window on Escape key
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec())
