import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsBlurEffect

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
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
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
        
        # Add widgets to layout
        layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        
        # Set window background
        central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 100);
                border-radius: 10px;
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
