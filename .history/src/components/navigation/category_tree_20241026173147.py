from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QSize
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class CategoryTree(QTreeWidget):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.setHeaderHidden(True)
        self.setStyleSheet(Styles.get_styles()["TREE"])
        self.setIconSize(QSize(20, 20))
        self.setup_tree()
    
    def setup_tree(self):
        categories = [
            ("Home", "home", []),
            ("Downloads", "downloads", []),
            ("Categories", None, [
                ("Musics", "music"),
                ("Compressed", "document"),
                ("Videos", "video"),
                ("Programs", "options"),
                ("Documents", "document"),
                ("APKs", "options"),
                ("Images", "image")
            ]),
            ("Unfinished", "queue", []),
            ("Finished", "downloads", [])
        ]
        
        self.clear()  # Clear existing items
        
        for category in categories:
            name, icon, subcategories = category
            item = QTreeWidgetItem([name])
            if icon:
                item.setIcon(0, IconProvider.get_icon(icon, self._is_dark))
            
            for sub in subcategories:
                sub_name, sub_icon = sub
                sub_item = QTreeWidgetItem([sub_name])
                if sub_icon:
                    sub_item.setIcon(0, IconProvider.get_icon(sub_icon, self._is_dark))
                item.addChild(sub_item)
            
            self.addTopLevelItem(item)
        
        # Expand Downloads by default
        self.topLevelItem(1).setExpanded(True)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.setup_tree()
