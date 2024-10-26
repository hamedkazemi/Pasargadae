from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from src.components.menu.menu_bar import MenuBar
from src.components.toolbar.action_toolbar import ActionToolbar
from src.components.navigation.category_tree import CategoryTree
from src.components.navigation.disk_space import DiskSpace
from src.components.downloads.download_table import DownloadTable
from src.components.downloads.search_bar import SearchBar
from src.components.theme.theme_switcher import ThemeSwitcher
from src.theme.styles import Styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Internet Download Manager")
        self.setMinimumSize(1200, 800)
        self._is_dark = True
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        # Set menu bar
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
        
        # Add theme switcher to menu bar
        self.theme_switcher = ThemeSwitcher(self)
        self.theme_switcher.themeChanged.connect(self.on_theme_changed)
        menu_bar.setCornerWidget(self.theme_switcher)
        
        # Add toolbar
        self.toolbar = ActionToolbar(self)
        self.addToolBar(self.toolbar)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Setup navigation panel
        nav_panel = QWidget()
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setSpacing(15)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        self.category_tree = CategoryTree()
        self.disk_space = DiskSpace()
        nav_layout.addWidget(self.category_tree)
        nav_layout.addWidget(self.disk_space)
        
        # Setup download panel
        download_panel = QWidget()
        download_layout = QVBoxLayout(download_panel)
        download_layout.setSpacing(15)
        download_layout.setContentsMargins(0, 0, 0, 0)
        self.search_bar = SearchBar()
        self.download_table = DownloadTable()
        download_layout.addWidget(self.search_bar)
        download_layout.addWidget(self.download_table)
        
        # Add panels to main layout
        main_layout.addWidget(nav_panel, 1)
        main_layout.addWidget(download_panel, 4)
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.menuBar().setStyleSheet(styles["MENU"])
        self.toolbar.setStyleSheet(styles["TOOLBAR"])
        self.category_tree.setStyleSheet(styles["TREE"])
        self.search_bar.setStyleSheet(styles["SEARCH"])
        self.download_table.setStyleSheet(styles["TABLE"])
        self.disk_space.setStyleSheet(styles["DISK_SPACE"])
