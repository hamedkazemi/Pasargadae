from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                                    QLabel, QFrame)
from PyQt6.QtCore import Qt
from src.components.menu.menu_bar import MenuBar
from src.components.toolbar.action_toolbar import ActionToolbar
from src.components.navigation.category_tree import CategoryTree
from src.components.navigation.disk_space import DiskSpace
from src.components.downloads.download_table import DownloadTable
from src.components.downloads.search_bar import SearchBar
from src.components.theme.theme_switcher import ThemeSwitcher
from src.theme.styles import Styles
from src.theme.colors import Colors

class SpeedTestWidget(QFrame):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        speed_label = QLabel("Speed Test:")
        download_label = QLabel("↓ 10.55 MB/s")
        upload_label = QLabel("↑ 6.30 MB/s")
        
        colors = Colors.Dark if self._is_dark else Colors.Light
        style = f"""
            QLabel {{
                color: {colors.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """
        
        for label in [speed_label, download_label, upload_label]:
            label.setStyleSheet(style)
        
        layout.addWidget(speed_label)
        layout.addWidget(download_label)
        layout.addWidget(upload_label)
        layout.addStretch()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Internet Download Manager")
        self.setMinimumSize(1200, 800)
        self._is_dark = True
        self.setup_ui()
        self.apply_theme()
        
        # Remove window frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def setup_ui(self):
        # Create central widget with proper styling
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        
        # Main vertical layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Set menu bar
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
        
        # Add theme switcher to menu bar
        self.theme_switcher = ThemeSwitcher(self)
        self.theme_switcher.themeChanged.connect(self.on_theme_changed)
        menu_bar.setCornerWidget(self.theme_switcher)
        
        # Add toolbar
        self.toolbar = ActionToolbar(self)
        self.main_layout.addWidget(self.toolbar)
        
        # Content layout
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(15)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        
        # Setup navigation panel
        self.nav_panel = QWidget()
        nav_layout = QVBoxLayout(self.nav_panel)
        nav_layout.setSpacing(15)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        self.category_tree = CategoryTree()
        self.disk_space = DiskSpace()
        nav_layout.addWidget(self.category_tree)
        nav_layout.addWidget(self.disk_space)
        
        # Setup download panel
        self.download_panel = QWidget()
        self.download_layout = QVBoxLayout(self.download_panel)
        self.download_layout.setSpacing(15)
        self.download_layout.setContentsMargins(0, 0, 0, 0)
        self.search_bar = SearchBar()
        self.download_table = DownloadTable()
        self.speed_test = SpeedTestWidget(self._is_dark)
        self.download_layout.addWidget(self.search_bar)
        self.download_layout.addWidget(self.download_table)
        self.download_layout.addWidget(self.speed_test)
        
        # Add panels to content layout
        self.content_layout.addWidget(self.nav_panel, 1)
        self.content_layout.addWidget(self.download_panel, 4)
        
        # Add content layout to main layout
        self.main_layout.addLayout(self.content_layout)
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()
        
        # Update speed test widget
        self.speed_test.setParent(None)
        self.speed_test = SpeedTestWidget(self._is_dark)
        self.download_layout.addWidget(self.speed_test)
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.menuBar().setStyleSheet(styles["MENU"])
        self.toolbar.setStyleSheet(styles["TOOLBAR"])
        self.category_tree.setStyleSheet(styles["TREE"])
        self.search_bar.setStyleSheet(styles["SEARCH"])
        self.download_table.setStyleSheet(styles["TABLE"])
        self.disk_space.setStyleSheet(styles["DISK_SPACE"])
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()