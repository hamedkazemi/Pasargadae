from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QSize, Qt
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class CategoryTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name, icon=None, is_dark=True):
        super().__init__(parent, [name])
        if icon:
            self.setIcon(0, IconProvider.get_icon(icon, is_dark))
        
        # Set text alignment
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Set item height
        self.setSizeHint(0, QSize(0, 32))

class CategoryTree(QTreeWidget):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.setHeaderHidden(True)
        self.setStyleSheet(Styles.get_styles()["TREE"])
        self.setIconSize(QSize(20, 20))
        self.setIndentation(20)  # Space for expand/collapse icons
        self.setup_tree()
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
    
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
        
        self.clear()
        
        for category in categories:
            name, icon, subcategories = category
            item = CategoryTreeItem(None, name, icon, self._is_dark)
            
            for sub in subcategories:
                sub_name, sub_icon = sub
                sub_item = CategoryTreeItem(item, sub_name, sub_icon, self._is_dark)
            
            self.addTopLevelItem(item)
            
            # Expand Categories by default
            if name == "Categories":
                item.setExpanded(True)
        
        # Expand Downloads by default
        self.topLevelItem(1).setExpanded(True)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.setStyleSheet(Styles.get_styles(is_dark)["TREE"])
        
        def update_item_icons(item):
            for i in range(item.childCount()):
                child = item.child(i)
                icon_name = child.data(0, Qt.ItemDataRole.UserRole)
                if icon_name:
                    child.setIcon(0, IconProvider.get_icon(icon_name, is_dark))
                update_item_icons(child)
        
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            icon_name = item.data(0, Qt.ItemDataRole.UserRole)
            if icon_name:
                item.setIcon(0, IconProvider.get_icon(icon_name, is_dark))
            update_item_icons(item)
    
    def mouseMoveEvent(self, event):
        """Override to ensure hover effect covers the entire row"""
        super().mouseMoveEvent(event)
        item = self.itemAt(event.pos())
        if item:
            item.setSelected(True)
        else:
            self.clearSelection()
    
    def leaveEvent(self, event):
        """Clear selection when mouse leaves the widget"""
        super().leaveEvent(event)
        self.clearSelection()
