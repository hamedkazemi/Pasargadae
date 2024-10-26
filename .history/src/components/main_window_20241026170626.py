from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from src.components.window.title_bar import TitleBar
from src.components.toolbar.action_toolbar import ActionToolbar
from src.components.navigation.navigation_panel import NavigationPanel
from src.components.downloads.download_panel import DownloadPanel
from src.theme.styles import Styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Internet Download Manager")
        self.setMinimumSize(1200, 800)
        self._is_dark = True
        
        # Remove window frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        # Create central widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar with menu and theme switcher
        self.title_bar = TitleBar(self)
        self.title_bar.theme_changed.connect(self.on_theme_changed)
        self.setMenuBar(self.title_bar.menu_bar)
        
        # Toolbar
        self.toolbar = ActionToolbar(self)
        self.main_layout.addWidget(self.toolbar)
        
        # Content layout
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(15)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        
        # Navigation and download panels
        self.nav_panel = NavigationPanel()
        self.download_panel = DownloadPanel(self._is_dark)
        
        self.content_layout.addWidget(self.nav_panel, 1)
        self.content_layout.addWidget(self.download_panel, 4)
        
        # Add content layout to main layout
        self.main_layout.addLayout(self.content_layout)
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.title_bar.apply_theme(styles)
        self.toolbar.setStyleSheet(styles["TOOLBAR"])
        self.nav_panel.apply_theme(styles)
        self.download_panel.apply_theme(styles, self._is_dark)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()
