from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyle
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class CategoryTreeItem(QTreeWidgetItem):
    def __init__(self, parent, name, icon=None, is_dark=True):
        super().__init__(parent, [name])
        self._is_dark = is_dark
        self.icon_name = icon
        
        if icon:
            self.setIcon(0, IconProvider.get_icon(icon, is_dark))
        
        # Store the icon name for theme updates
        self.setData(0, Qt.ItemDataRole.UserRole, icon)
        
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
        self.setIndentation(20)
        self.setup_tree()
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
        # Connect item expansion signal
        self.itemExpanded.connect(self.update_branch_icon)
        self.itemCollapsed.connect(self.update_branch_icon)
    
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
            
            # Set branch icons if has children
            if subcategories:
                self.update_branch_icon(item)
            
            # Expand Categories by default
            if name == "Categories":
                item.setExpanded(True)
        
        # Expand Downloads by default
        self.topLevelItem(1).setExpanded(True)
    
    def update_branch_icon(self, item):
        if item.childCount() > 0:
            is_expanded = item.isExpanded()
            icon = IconProvider.get_icon('chevron_down' if is_expanded else 'chevron_right', self._is_dark)
            item.setIcon(0, icon)
            if item.icon_name:  # If item has its own icon
                item.setIcon(0, IconProvider.get_icon(item.icon_name, self._is_dark))
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.setStyleSheet(Styles.get_styles(is_dark)["TREE"])
        
        def update_item_icons(item):
            icon_name = item.data(0, Qt.ItemDataRole.UserRole)
            if icon_name:
                item.setIcon(0, IconProvider.get_icon(icon_name, is_dark))
            if item.childCount() > 0:
                self.update_branch_icon(item)
            for i in range(item.childCount()):
                update_item_icons(item.child(i))
        
        for i in range(self.topLevelItemCount()):
            update_item_icons(self.topLevelItem(i))
    
    def drawRow(self, painter, options, index):
        """Override to ensure the entire row is highlighted"""
        options.showDecorationSelected = True
        super().drawRow(painter, options, index)
    
    def mousePressEvent(self, event):
        """Handle item expansion on click"""
        item = self.itemAt(event.pos())
        if item and item.childCount() > 0:
            if event.pos().x() < self.indentation():
                item.setExpanded(not item.isExpanded())
                return
        super().mousePressEvent(event)
