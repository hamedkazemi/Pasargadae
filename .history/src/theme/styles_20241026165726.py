from .colors import Colors

class Styles:
    @staticmethod
    def get_styles(is_dark=True):
        colors = Colors.Dark if is_dark else Colors.Light
        
        return {
            "WINDOW": f"""
                QMainWindow {{
                    background-color: {colors.BACKGROUND};
                    color: {colors.TEXT_PRIMARY};
                }}
            """,
            
            "MENU": f"""
                QMenuBar {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_PRIMARY};
                    padding: 2px;
                    border-bottom: 1px solid {colors.SURFACE};
                }}
                QMenuBar::item:selected {{
                    background-color: {colors.PRIMARY};
                    border-radius: 4px;
                }}
                QMenu {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_PRIMARY};
                    border: 1px solid {colors.SURFACE};
                    border-radius: 4px;
                    padding: 5px;
                }}
                QMenu::item:selected {{
                    background-color: {colors.PRIMARY};
                    border-radius: 2px;
                }}
            """,
            
            "TOOLBAR": f"""
                QToolBar {{
                    background-color: {colors.SURFACE};
                    border-bottom: 1px solid {colors.SURFACE};
                    padding: 5px;
                    spacing: 5px;
                }}
                QToolButton {{
                    background-color: transparent;
                    color: {colors.TEXT_PRIMARY};
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }}
                QToolButton:hover {{
                    background-color: rgba(128, 128, 128, 0.1);
                }}
            """,
            
            "TREE": f"""
                QTreeWidget {{
                    background-color: {colors.SURFACE};
                    border: none;
                    border-radius: 8px;
                    padding: 5px;
                    color: {colors.TEXT_PRIMARY};
                }}
                QTreeWidget::item {{
                    padding: 5px;
                    border-radius: 4px;
                }}
                QTreeWidget::item:selected {{
                    background: {colors.GRADIENT_PRIMARY};
                }}
                QTreeWidget::item:hover {{
                    background-color: rgba(128, 128, 128, 0.1);
                }}
            """,
            
            "SEARCH": f"""
                QLineEdit {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_PRIMARY};
                    border: 1px solid {colors.SURFACE};
                    border-radius: 20px;
                    padding: 8px 15px;
                    font-size: 14px;
                }}
                QLineEdit:focus {{
                    border: 2px solid {colors.PRIMARY};
                }}
            """,
            
            "TABLE": f"""
                QTableWidget {{
                    background-color: {colors.SURFACE};
                    border: none;
                    border-radius: 8px;
                    gridline-color: {colors.SURFACE};
                    color: {colors.TEXT_PRIMARY};
                }}
                QTableWidget::item {{
                    padding: 5px;
                    border-radius: 4px;
                }}
                QTableWidget::item:selected {{
                    background: rgba(33, 150, 243, 0.2);
                    color: {colors.TEXT_PRIMARY};
                }}
                QHeaderView::section {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_SECONDARY};
                    padding: 5px;
                    border: none;
                }}
            """,
            
            "PROGRESS": f"""
                QProgressBar {{
                    border: none;
                    background-color: rgba(128, 128, 128, 0.1);
                    height: 4px;
                    border-radius: 2px;
                }}
                QProgressBar::chunk {{
                    background: {colors.GRADIENT_PRIMARY};
                    border-radius: 2px;
                }}
            """,
            
            "DISK_SPACE": f"""
                QWidget#diskSpace {{
                    background-color: {colors.SURFACE};
                    border-radius: 8px;
                    padding: 10px;
                }}
                QLabel#diskTitle {{
                    color: {colors.TEXT_PRIMARY};
                    font-size: 14px;
                    font-weight: bold;
                }}
                QLabel#diskPath {{
                    color: {colors.TEXT_SECONDARY};
                    font-size: 12px;
                }}
                QPushButton#diskCleaner {{
                    background: {colors.GRADIENT_PRIMARY};
                    color: {colors.TEXT_PRIMARY};
                    border: none;
                    border-radius: 15px;
                    padding: 8px 15px;
                    font-weight: bold;
                }}
                QPushButton#diskCleaner:hover {{
                    background: {colors.GRADIENT_HOVER};
                }}
            """
        }
