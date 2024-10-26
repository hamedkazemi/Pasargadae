from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qframelesswindow import FramelessMainWindow, StandardTitleBar
from src.components.window.title_bar import TitleBar
from PyQt6.QtCore import Qt
from src.components.toolbar.action_toolbar import ActionToolbar
from src.components.navigation.navigation_panel import NavigationPanel
from src.components.downloads.download_panel import DownloadPanel
from src.theme.styles import Styles

class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self._is_dark = True
        self.setWindowTitle("Pasargadae")
        self.setMinimumSize(1000, 600)
        self.setTitleBar(TitleBar(StandardTitleBar(self)))
        
        # Create main container
        self.container = QWidget()
        self.container.setObjectName("centralWidget")

        self.setCentralWidget(self.container)  # FramelessWindow uses setWidget instead of setCentralWidget
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout for container
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add custom title bar
        self.title_bar.theme_changed.connect(self.on_theme_changed)

        # Add toolbar
        self.toolbar = ActionToolbar(self._is_dark)
        
        # Create main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        # Add navigation panel
        self.navigation_panel = NavigationPanel(self._is_dark)
        content_layout.addWidget(self.navigation_panel)
        
        # Add download panel
        self.download_panel = DownloadPanel(self._is_dark)
        content_layout.addWidget(self.download_panel)
        
        # Add widgets to main layout
        layout.addWidget(self.title_bar)
        layout.addWidget(self.toolbar)
        layout.addLayout(content_layout)
        
        # Apply theme
        self.apply_theme(self._is_dark)
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme(is_dark)
    
    def apply_theme(self, is_dark):
        styles = Styles.get_styles(is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.toolbar.update_theme(is_dark)
        self.navigation_panel.update_theme(is_dark)
        self.download_panel.update_theme(is_dark)
