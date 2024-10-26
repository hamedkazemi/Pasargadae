import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                              QVBoxLayout, QWidget, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsBlurEffect

class BlurredWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create and apply blur effect
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(20)  # Increased blur radius
        self.setGraphicsEffect(self.blur_effect)
        
        # Style for blurred background
        self.setStyleSheet("""
            BlurredWidget {
                background-color: rgba(40, 40, 40, 80);
                border-radius: 15px;
            }
        """)

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Transparent Hello World")
        self.setGeometry(100, 100, 400, 200)
        self.setMinimumSize(400, 200)
        
        # Make window frameless and stay on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Enable transparency
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create main container
        self.container = QWidget()
        self.setCentralWidget(self.container)
        
        # Create blurred background
        self.blurred_bg = BlurredWidget(self.container)
        
        # Create layout
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Create close button
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 150);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 200);
            }
        """)
        
        # Create and style the label
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        # Add widgets to content layout
        content_layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        
        # Add content to main layout
        layout.addWidget(content)
        
        # Set up shadow effect for the window
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Make blurred background follow window size
        self.blurred_bg.setGeometry(self.container.rect())

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
