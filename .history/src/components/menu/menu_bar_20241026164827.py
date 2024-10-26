from PyQt6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_menus()
    
    def setup_menus(self):
        # Tasks menu
        tasks_menu = self.addMenu("Tasks")
        tasks_menu.addAction("Add URL")
        tasks_menu.addAction("Start All")
        tasks_menu.addAction("Stop All")
        
        # File menu
        file_menu = self.addMenu("File")
        file_menu.addAction("Exit")
        
        # Downloads menu
        self.addMenu("Downloads")
        
        # View menu
        self.addMenu("View")
        
        # Help menu
        self.addMenu("Help")
