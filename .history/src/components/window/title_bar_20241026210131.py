from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt, pyqtSignal
from qframelesswindow import StandardTitleBar
from src.components.menu.menu_bar import MenuBar
from src.components.theme.theme_switcher import ThemeSwitcher
from src.utils.icon_provider import IconProvider
from src.theme.styles import Styles

class TitleBar(StandardTitleBar):
    theme_changed = pyqtSignal(bool)  # Signal for theme changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._is_dark = True
        self.setup_ui()
        self.apply_theme(self._is_dark)
        self.customize_buttons()
    
    def setup_ui(self):
        # Create custom layout
        custom_widget = QWidget(self)
        layout = QHBoxLayout(custom_widget)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(10)
        
        # Logo and title
        self.logo_label = QLabel()
        self.update_logo()
        
        # Menu bar
        self.menu_bar = MenuBar(self.parent)
        
        # Theme switcher
        self.theme_switcher = ThemeSwitcher(self.parent)
        self.theme_switcher.themeChanged.connect(self.on_theme_changed)
        
        # Add widgets to layout
        layout.addWidget(self.logo_label)
        layout.addWidget(self.menu_bar)
        layout.addStretch()
        layout.addWidget(self.theme_switcher)
        
        # Add custom widget to title bar
        self.hBoxLayout.insertWidget(0, custom_widget, 1)

    def customize_buttons(self):
        # Common button style
        button_style = """
            TitleBarButton {
                border: none;
                border-radius: 12px;
                width: 24px;
                height: 24px;
                margin: 5px;
                qproperty-normalColor: white;
                qproperty-normalBackgroundColor: transparent;
                qproperty-hoverColor: white;
                qproperty-pressedColor: white;
            }
        """

        # Minimize button
        self.minBtn.setStyleSheet(button_style + """
            TitleBarButton {
                qproperty-hoverBackgroundColor: rgb(0, 100, 182);
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)

        # Maximize button
        self.maxBtn.setStyleSheet(button_style + """
            TitleBarButton {
                qproperty-hoverBackgroundColor: rgb(0, 100, 182);
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)

        # Close button
        self.closeBtn.setStyleSheet(button_style + """
            TitleBarButton {
                qproperty-hoverBackgroundColor: rgb(232, 17, 35);
                qproperty-pressedBackgroundColor: rgb(241, 112, 122);
            }
        """)
    
    def update_logo(self):
        self.logo_label.setPixmap(IconProvider.get_icon("logo", self._is_dark).pixmap(24, 24))
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.update_logo()
        self.menu_bar.update_theme(is_dark)
        self.theme_changed.emit(is_dark)
    
    def apply_theme(self, is_dark):
        self._is_dark = is_dark
        styles = Styles.get_styles(is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.menu_bar.update_theme(is_dark)
        self.update_logo()
