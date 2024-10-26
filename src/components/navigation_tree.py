from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

class NavigationTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setup_tree()
    
    def setup_tree(self):
        # Create main items
        home = QTreeWidgetItem(self, ["Home"])
        downloads = QTreeWidgetItem(self, ["Downloads"])
        scheduler = QTreeWidgetItem(self, ["Scheduler"])
        settings = QTreeWidgetItem(self, ["Settings"])
        browser = QTreeWidgetItem(self, ["Browser Integration"])
        categories = QTreeWidgetItem(self, ["Categories"])
        reports = QTreeWidgetItem(self, ["Reports"])
        help_item = QTreeWidgetItem(self, ["Help"])
        
        # Expand downloads by default
        downloads.setExpanded(True)
        self.setCurrentItem(downloads)
