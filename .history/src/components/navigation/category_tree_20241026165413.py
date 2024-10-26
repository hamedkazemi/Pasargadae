from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtGui import QIcon
from src.theme.styles import Styles

class CategoryTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setStyleSheet(Styles.TREE)
        self.setup_tree()
    
    def setup_tree(self):
        categories = [
            ("Home", "home", []),
            ("Downloads", "downloads", []),
            ("Categories", None, [
                ("Musics", "music"),
                ("Compressed", "compressed"),
                ("Videos", "video"),
                ("Programs", "program"),
                ("Documents", "document"),
                ("APKs", "apk"),
                ("Images", "image")
            ]),
            ("Unfinished", "queue", []),
            ("Finished", "downloads", [])
        ]
        
        for category in categories:
            name, icon, subcategories = category
            item = QTreeWidgetItem([name])
            if icon:
                item.setIcon(0, QIcon(f"src/assets/icons/{icon}.svg"))
            
            for sub in subcategories:
                sub_name, sub_icon = sub
                sub_item = QTreeWidgetItem([sub_name])
                if sub_icon:
                    sub_item.setIcon(0, QIcon(f"src/assets/icons/{sub_icon}.svg"))
                item.addChild(sub_item)
            
            self.addTopLevelItem(item)
        
        # Expand Downloads by default
        self.topLevelItem(1).setExpanded(True)
