from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from .navigation_tree import NavigationTree
from .download_list import DownloadList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Manager")
        self.setMinimumSize(1000, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Add navigation tree and download list
        self.navigation_tree = NavigationTree()
        self.download_list = DownloadList()
        
        # Set layout
        main_layout.addWidget(self.navigation_tree, 1)
        main_layout.addWidget(self.download_list, 3)
