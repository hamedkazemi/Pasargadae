from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.components.navigation.category_tree import CategoryTree
from src.components.navigation.disk_space import DiskSpace
from src.theme.styles import Styles

class NavigationPanel(QWidget):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Add category tree
        self.category_tree = CategoryTree(self._is_dark)
        layout.addWidget(self.category_tree)
        
        # Add disk space widget
        self.disk_space = DiskSpace(self._is_dark)
        layout.addWidget(self.disk_space)
        
        self.setFixedWidth(250)
    
    def update_theme(self, is_dark):
        """Update theme for all child widgets"""
        self._is_dark = is_dark
        self.category_tree.update_theme(is_dark)
        self.disk_space.update_theme(is_dark)
