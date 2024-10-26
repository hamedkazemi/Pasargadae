from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from .menu.menu_bar import MenuBar
from .toolbar.action_toolbar import ActionToolbar
from .navigation.category_tree import CategoryTree
from .navigation.disk_space import DiskSpace
from .downloads.download_table import DownloadTable
from .downloads.search_bar import SearchBar
from ..theme.styles import Styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Internet Download Manager")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(Styles.WINDOW)
        
        # Set menu bar
        self.setMenuBar(MenuBar(self))
        
        # Add toolbar
        self.addToolBar(ActionToolbar(self))
        
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
        nav_layout.addWidget(CategoryTree())
        nav_layout.addWidget(DiskSpace())
        
        # Setup download panel
        download_panel = QWidget()
        download_layout = QVBoxLayout(download_panel)
        download_layout.setSpacing(15)
        download_layout.setContentsMargins(0, 0, 0, 0)
        download_layout.addWidget(SearchBar())
        download_layout.addWidget(DownloadTable())
        
        # Add panels to main layout
        main_layout.addWidget(nav_panel, 1)
        main_layout.addWidget(download_panel, 4)
