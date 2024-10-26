from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

class CategoryTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setup_tree()
    
    def setup_tree(self):
        categories = [
            ("All Downloads", []),
            ("Categories", [
                "Musics", "Compressed", "Videos", "Programs",
                "Documents", "APKs", "Images"
            ]),
            ("Unfinished", []),
            ("Finished", [])
        ]
        
        for category, subcategories in categories:
            item = QTreeWidgetItem(self, [category])
            for sub in subcategories:
                QTreeWidgetItem(item, [sub])
        
        self.topLevelItem(0).setExpanded(True)
