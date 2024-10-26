from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from src.components.menu.menu_bar import MenuBar
from src.components.theme.theme_switcher import ThemeSwitcher
from src.components.window.window_controls import WindowControls
from src.utils.icon_provider import IconProvider

class TitleBar(QWidget):
    theme_changed = pyqtSignal(bool)  # Signal for theme changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._is_dark = True
        self._is_dragging = False
        self._drag_start_pos = None
        self.setup_ui()
        
        # Enable mouse tracking for window dragging
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(10)
        
        # Logo and title
        self.logo_label = QLabel()
        self.update_logo()
        
        title_label = QLabel("Pasargadae")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding-right: 20px;
            }
        """)
        
        # Menu bar
        self.menu_bar = MenuBar(self.parent)
        
        # Theme switcher
        self.theme_switcher = ThemeSwitcher(self.parent)
        self.theme_switcher.themeChanged.connect(self.on_theme_changed)
        
        # Window controls
        self.window_controls = WindowControls(self.parent)
        self.window_controls.setFixedHeight(self.height())
        self.window_controls.minimizeClicked.connect(self.parent.showMinimized)
        self.window_controls.closeClicked.connect(self.parent.close)
        
        # Add widgets to layout
        layout.addWidget(self.logo_label)
        layout.addWidget(title_label)
        layout.addWidget(self.menu_bar)
        layout.addStretch()
        layout.addWidget(self.theme_switcher)
        layout.addWidget(self.window_controls)
    
    def update_logo(self):
        self.logo_label.setPixmap(IconProvider.get_icon("logo", self._is_dark).pixmap(24, 24))
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.update_logo()
        self.window_controls.update_theme(is_dark)
        self.theme_changed.emit(is_dark)
    
    def apply_theme(self, styles, is_dark=True):
        self._is_dark = is_dark
        self.menu_bar.setStyleSheet(styles["MENU"])
        self.window_controls.update_theme(is_dark)
        self.update_logo()
    
    def is_draggable_area(self, pos):
        """Check if the given position is in a draggable area"""
        for widget in [self.window_controls, self.theme_switcher, self.menu_bar]:
            if widget.isVisible():
                widget_pos = widget.mapFrom(self, pos)
                if widget.rect().contains(widget_pos):
                    return False
        return True
    
    def mousePressEvent(self, event):
        """Handle window dragging"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_draggable_area(event.pos()):
            self._is_dragging = True
            self._drag_start_pos = event.globalPosition().toPoint()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle end of window dragging"""
        if event.button() == Qt.MouseButton.LeftButton and self._is_dragging:
            self._is_dragging = False
            self._drag_start_pos = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if self._is_dragging and self._drag_start_pos is not None:
            current_pos = event.globalPosition().toPoint()
            diff = current_pos - self._drag_start_pos
            new_pos = self.parent.pos() + diff
            self.parent.move(new_pos)
            self._drag_start_pos = current_pos
            event.accept()
    
    def leaveEvent(self, event):
        """Reset cursor when mouse leaves the title bar"""
        if not self._is_dragging:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
