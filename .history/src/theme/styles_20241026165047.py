from .colors import Colors

class Styles:
    WINDOW = f"""
        QMainWindow {{
            background-color: {Colors.BACKGROUND};
            color: {Colors.TEXT_PRIMARY};
        }}
    """
    
    MENU = f"""
        QMenuBar {{
            background-color: {Colors.SURFACE};
            color: {Colors.TEXT_PRIMARY};
            padding: 2px;
            border-bottom: 1px solid #3A3B3E;
        }}
        QMenuBar::item:selected {{
            background-color: {Colors.PRIMARY};
            border-radius: 4px;
        }}
        QMenu {{
            background-color: {Colors.SURFACE};
            color: {Colors.TEXT_PRIMARY};
            border: 1px solid #3A3B3E;
            border-radius: 4px;
            padding: 5px;
        }}
        QMenu::item:selected {{
            background-color: {Colors.PRIMARY};
            border-radius: 2px;
        }}
    """
    
    TOOLBAR = f"""
        QToolBar {{
            background-color: {Colors.SURFACE};
            border-bottom: 1px solid #3A3B3E;
            padding: 5px;
            spacing: 5px;
        }}
        QToolButton {{
            background-color: transparent;
            color: {Colors.TEXT_PRIMARY};
            border: none;
            border-radius: 4px;
            padding: 5px;
        }}
        QToolButton:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
        QToolButton:pressed {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
    """
    
    TREE = f"""
        QTreeWidget {{
            background-color: {Colors.SURFACE};
            border: none;
            border-radius: 8px;
            padding: 5px;
        }}
        QTreeWidget::item {{
            padding: 5px;
            border-radius: 4px;
        }}
        QTreeWidget::item:selected {{
            background: {Colors.GRADIENT_PRIMARY};
        }}
        QTreeWidget::item:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}
    """
    
    SEARCH = f"""
        QLineEdit {{
            background-color: {Colors.SURFACE};
            color: {Colors.TEXT_PRIMARY};
            border: 1px solid #3A3B3E;
            border-radius: 20px;
            padding: 8px 15px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border: 2px solid {Colors.PRIMARY};
        }}
    """
    
    TABLE = f"""
        QTableWidget {{
            background-color: {Colors.SURFACE};
            border: none;
            border-radius: 8px;
            gridline-color: #3A3B3E;
            color: {Colors.TEXT_PRIMARY};
        }}
        QTableWidget::item {{
            padding: 5px;
            border-radius: 4px;
        }}
        QTableWidget::item:selected {{
            background: rgba(33, 150, 243, 0.2);
            color: {Colors.TEXT_PRIMARY};
        }}
        QHeaderView::section {{
            background-color: {Colors.SURFACE};
            color: {Colors.TEXT_SECONDARY};
            padding: 5px;
            border: none;
        }}
    """
    
    PROGRESS = f"""
        QProgressBar {{
            border: none;
            background-color: rgba(255, 255, 255, 0.1);
            height: 4px;
            border-radius: 2px;
        }}
        QProgressBar::chunk {{
            background: {Colors.GRADIENT_PRIMARY};
            border-radius: 2px;
        }}
    """
    
    DISK_SPACE = f"""
        QWidget#diskSpace {{
            background-color: {Colors.SURFACE};
            border-radius: 8px;
            padding: 10px;
        }}
        QLabel#diskTitle {{
            color: {Colors.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: bold;
        }}
        QLabel#diskPath {{
            color: {Colors.TEXT_SECONDARY};
            font-size: 12px;
        }}
        QPushButton#diskCleaner {{
            background: {Colors.GRADIENT_PRIMARY};
            color: {Colors.TEXT_PRIMARY};
            border: none;
            border-radius: 15px;
            padding: 8px 15px;
            font-weight: bold;
        }}
        QPushButton#diskCleaner:hover {{
            background: {Colors.GRADIENT_HOVER};
        }}
    """
