from .colors import Colors

class Styles:
    @staticmethod
    def get_styles(is_dark=True):
        colors = Colors.Dark if is_dark else Colors.Light
        
        # Common scrollbar style
        scrollbar_style = f"""
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {colors.TEXT_SECONDARY};
                min-height: 30px;
                border-radius: 4px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors.PRIMARY};
            }}
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: transparent;
                height: 8px;
                margin: 0;
            }}
            QScrollBar::handle:horizontal {{
                background: {colors.TEXT_SECONDARY};
                min-width: 30px;
                border-radius: 4px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {colors.PRIMARY};
            }}
            QScrollBar::add-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """
        
        return {
            "WINDOW": f"""
                QMainWindow {{
                    background-color: {colors.BACKGROUND};
                    color: {colors.TEXT_PRIMARY};
                    border-radius: 10px;
                }}
                QWidget#centralWidget {{
                    background-color: {colors.BACKGROUND};
                    border-radius: 10px;
                }}
                QLabel {{
                    color: {colors.TEXT_PRIMARY};
                }}
                {scrollbar_style}
            """,
            
            "MENU": f"""
                QMenuBar {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_PRIMARY};
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    padding: 2px 10px;
                    spacing: 5px;
                }}
                QMenuBar::item {{
                    padding: 5px 10px;
                    border-radius: 4px;
                }}
                QMenuBar::item:selected {{
                    background-color: rgba(128, 128, 128, 0.1);
                }}
                QMenu {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_PRIMARY};
                    border: 1px solid {colors.SURFACE_LIGHT};
                    border-radius: 4px;
                    padding: 5px;
                }}
                QMenu::item {{
                    padding: 5px 30px 5px 20px;
                    border-radius: 4px;
                }}
                QMenu::item:selected {{
                    background-color: rgba(128, 128, 128, 0.1);
                }}
                {scrollbar_style}
            """,
            
            "TOOLBAR": f"""
                QToolBar {{
                    background-color: {colors.SURFACE};
                    border: none;
                    padding: 5px;
                    spacing: 5px;
                }}
                QToolButton {{
                    background-color: transparent;
                    color: {colors.TEXT_PRIMARY};
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                    icon-size: 20px;
                }}
                QToolButton:hover {{
                    background-color: rgba(128, 128, 128, 0.1);
                }}
                QToolButton:pressed {{
                    background-color: rgba(128, 128, 128, 0.15);
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
                    padding: 4px;
                    border-radius: 4px;
                    color: {colors.TEXT_PRIMARY};
                }}
                QTreeWidget::item:selected {{
                    background: rgba(128, 128, 128, 0.1);
                }}
                QTreeWidget::item:hover {{
                    background: rgba(128, 128, 128, 0.05);
                }}
                QTreeWidget::branch {{
                    background: transparent;
                }}
                {scrollbar_style}
            """,
            
            "SEARCH": f"""
                QLineEdit {{
                    background-color: {colors.SURFACE_LIGHT};
                    color: {colors.TEXT_PRIMARY};
                    border: none;
                    border-radius: 20px;
                    padding: 8px 35px;
                    font-size: 13px;
                }}
                QLineEdit:focus {{
                    background-color: {colors.SURFACE};
                    border: 1px solid rgba(128, 128, 128, 0.1);
                }}
            """,
            
            "TABLE": f"""
                QTableWidget {{
                    background-color: {colors.SURFACE};
                    border: none;
                    border-radius: 8px;
                    gridline-color: transparent;
                    color: {colors.TEXT_PRIMARY};
                }}
                QTableWidget::item {{
                    padding: 8px;
                    border-radius: 4px;
                    color: {colors.TEXT_PRIMARY};
                }}
                QTableWidget::item:selected {{
                    background: rgba(128, 128, 128, 0.05);
                }}
                QHeaderView::section {{
                    background-color: {colors.SURFACE};
                    color: {colors.TEXT_SECONDARY};
                    padding: 8px;
                    border: none;
                    font-size: 12px;
                }}
                QTableWidget QCheckBox {{
                    padding: 6px;
                }}
                QTableWidget QProgressBar {{
                    border: none;
                    background-color: rgba(128, 128, 128, 0.1);
                    height: 4px;
                    border-radius: 2px;
                }}
                QTableWidget QProgressBar::chunk {{
                    background: {colors.GRADIENT_PRIMARY};
                    border-radius: 2px;
                }}
                {scrollbar_style}
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
                    padding: 15px;
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
                    color: white;
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
