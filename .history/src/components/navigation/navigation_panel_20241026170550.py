from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .category_tree import CategoryTree
from .disk_space import DiskSpace

class NavigationPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.category_tree = CategoryTree()
        self.disk_space = DiskSpace()
        
        layout.addWidget(self.category_tree)
        layout.addWidget(self.disk_space)
    
    def apply_theme(self, styles):
        self.category_tree.setStyleSheet(styles["TREE"])
        self.disk_space.setStyleSheet(styles["DISK_SPACE"])
