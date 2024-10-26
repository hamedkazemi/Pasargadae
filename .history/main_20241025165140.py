import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Qt, QRect, QPoint, QTimer
from PySide6.QtGui import QColor, QScreen, QPixmap, QPainter, QImage

class CriticalError(Exception):
    """Custom exception for critical application errors"""
    pass

def show_error_and_exit(error_message):
    """Display error message and exit application"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle("Critical Error")
    error_box.setText(error_message)
    error_box.exec()
    sys.exit(1)

def show_warning(message):
    """Display warning message without exiting"""
    warning_box = QMessageBox()
    warning_box.setIcon(QMessageBox.Warning)
    warning_box.setWindowTitle("Warning")
    warning_box.setText(message)
    warning_box.exec()

class FastBlur:
    @staticmethod
    def blur(image, radius):
        if radius < 1:
            return image
        if image is None:
            return None

        try:
            # Create working image
            tmp = QImage(image)
            
            # Horizontal blur
            h = image.height()
            w = image.width()
            
            for y in range(h):
                line = []
                for x in range(w):
                    pixel = image.pixel(x, y)
                    line.append(QColor(pixel))
                
                for x in range(w):
                    r = g = b = a = 0
                    for ix in range(max(x - radius, 0), min(x + radius + 1, w)):
                        color = line[ix]
                        r += color.red()
                        g += color.green()
                        b += color.blue()
                        a += color.alpha()
                    
                    count = min(x + radius + 1, w) - max(x - radius, 0)
                    tmp.setPixelColor(x, y, QColor(r//count, g//count, b//count, a//count))
            
            # Vertical blur
            for x in range(w):
                line = []
                for y in range(h):
                    pixel = tmp.pixel(x, y)
                    line.append(QColor(pixel))
                
                for y in range(h):
                    r = g = b = a = 0
                    for iy in range(max(y - radius, 0), min(y + radius + 1, h)):
                        color = line[iy]
                        r += color.red()
                        g += color.green()
                        b += color.blue()
                        a += color.alpha()
                    
                    count = min(y + radius + 1, h) - max(y - radius, 0)
                    tmp.setPixelColor(x, y, QColor(r//count, g//count, b//count, a//count))
            
            return tmp
        except Exception:
            return None

class TransparentWindow(QMainWindow):
    def __init__(self):
        try:
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
            
            # Add widgets to layout
            layout.addWidget(self.close_button, alignment=Qt.AlignRight)
            layout.addWidget(self.label, alignment=Qt.AlignCenter)
            
            # Background properties
            self.background = None
            self.blur_radius = 10
            self._updating_background = False
            
            # Setup update timer
            self._update_timer = QTimer(self)
            self._update_timer.setSingleShot(True)
            self._update_timer.timeout.connect(self._perform_background_update)
            
        except Exception as e:
            raise CriticalError(f"Failed to initialize window: {str(e)}")

    def _perform_screen_capture(self):
        """Perform the actual screen capture"""
        try:
            screen = QApplication.primaryScreen()
            if not screen:
                return None
                
            window_rect = self.geometry()
            desktop = QApplication.primaryScreen().virtualGeometry()
            
            # Ensure capture coordinates are within screen bounds
            x = max(0, min(window_rect.x(), desktop.width() - window_rect.width()))
            y = max(0, min(window_rect.y(), desktop.height() - window_rect.height()))
            w = min(window_rect.width(), desktop.width() - x)
            h = min(window_rect.height(), desktop.height() - y)
            
            # Capture the screen area
            screen_pixmap = screen.grabWindow(
                0,  # Window ID 0 means entire screen
                x, y, w, h
            )
            
            return screen_pixmap
        except Exception as e:
            show_warning(f"Screen capture failed: {str(e)}")
            return None

    def _perform_background_update(self):
        """Perform the actual background update"""
        if self._updating_background:
            return
            
        try:
            self._updating_background = True
            
            # Temporarily hide window
            was_visible = self.isVisible()
            if was_visible:
                self.setAttribute(Qt.WA_WState_Hidden, True)
                self.setAttribute(Qt.WA_WState_Visible, False)
            
            # Process events to ensure window state is updated
            QApplication.processEvents()
            
            # Capture screen
            screen_pixmap = self._perform_screen_capture()
            
            # Restore window visibility
            if was_visible:
                self.setAttribute(Qt.WA_WState_Hidden, False)
                self.setAttribute(Qt.WA_WState_Visible, True)
            
            if not screen_pixmap or screen_pixmap.isNull():
                return
            
            # Convert to image and apply blur
            screen_image = screen_pixmap.toImage()
            blurred_image = FastBlur.blur(screen_image, self.blur_radius)
            
            if not blurred_image:
                return
            
            # Update background
            self.background = QPixmap.fromImage(blurred_image)
            self.update()
            
        except Exception as e:
            show_warning(f"Background update failed: {str(e)}")
        finally:
            self._updating_background = False

    def updateBackground(self):
        """Schedule a background update"""
        if not self._updating_background:
            self._update_timer.start(100)  # 100ms delay before update

    def paintEvent(self, event):
        if self.background:
            try:
                painter = QPainter(self)
                painter.drawPixmap(0, 0, self.background)
                painter.fillRect(self.rect(), QColor(40, 40, 40, 80))
            except Exception as e:
                show_warning(f"Paint operation failed: {str(e)}")

    def moveEvent(self, event):
        super().moveEvent(event)
        self.updateBackground()

    def showEvent(self, event):
        super().showEvent(event)
        self.updateBackground()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            new_pos = self.pos() + event.globalPosition().toPoint() - self.dragPos
            self.move(new_pos)
            self.dragPos = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = TransparentWindow()
        window.show()
        sys.exit(app.exec())
    except CriticalError as e:
        show_error_and_exit(str(e))
    except Exception as e:
        show_error_and_exit(f"Unexpected error: {str(e)}")
