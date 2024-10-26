from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt, pyqtSignal
from qframelesswindow import StandardTitleBar
from src.components.menu.menu_bar import MenuBar
from src.components.theme.theme_switcher import ThemeSwitcher
from src.utils.icon_provider import IconProvider
from src.theme.styles import Styles
from src.theme.colors import Colors

class TitleBar(StandardTitleBar):
    theme_changed = pyqtSignal(bool)  # Signal for theme changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._is_dark = True
        self.setup_ui()
        self.apply_theme(self._is_dark)
    
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
        
        # Add custom widget to title bar (before the window controls)
        self.hBoxLayout.insertWidget(0, custom_widget, 1)
        
        # Move theme switcher to the right of window controls
        # First remove the existing buttons from their parent
        self.minBtn.setParent(None)
        self.maxBtn.setParent(None)
        self.closeBtn.setParent(None)
        
        # Create a new widget for the right side controls
        right_controls = QWidget(self)
        right_layout = QHBoxLayout(right_controls)
        right_layout.setContentsMargins(0, 0, 10, 0)
        right_layout.setSpacing(0)
        
        # Add the controls in the desired order
        right_layout.addWidget(self.theme_switcher)
        right_layout.addWidget(self.minBtn)
        right_layout.addWidget(self.maxBtn)
        right_layout.addWidget(self.closeBtn)
        
        # Add the right controls to the main layout
        self.hBoxLayout.addWidget(right_controls, 0, Qt.AlignmentFlag.AlignRight)

    def customize_buttons(self, is_dark):
        colors = Colors.Dark if is_dark else Colors.Light
        
        # Common button style
        button_style = f"""
            TitleBarButton {{
                border: none;
                border-radius: 12px;
                width: 24px;
                height: 24px;
                margin: 5px;
                qproperty-normalColor: {colors.ICON_COLOR};
                qproperty-normalBackgroundColor: transparent;
                qproperty-pressedColor: {colors.TEXT_PRIMARY};
            }}
        """

        # Minimize button
        self.minBtn.setStyleSheet(button_style + f"""
            TitleBarButton {{
                qproperty-hoverColor: {Colors.Dark.TEXT_PRIMARY if is_dark else Colors.Light.BACKGROUND};
                qproperty-hoverBackgroundColor: {colors.PRIMARY};
                qproperty-pressedBackgroundColor: {Colors.Dark.SURFACE_LIGHT if is_dark else Colors.Light.SURFACE_LIGHT};
            }}
        """)

        # Maximize button
        self.maxBtn.setStyleSheet(button_style + f"""
            TitleBarButton {{
                qproperty-hoverColor: {Colors.Dark.TEXT_PRIMARY if is_dark else Colors.Light.BACKGROUND};
                qproperty-hoverBackgroundColor: {colors.PRIMARY};
                qproperty-pressedBackgroundColor: {Colors.Dark.SURFACE_LIGHT if is_dark else Colors.Light.SURFACE_LIGHT};
            }}
        """)

        # Close button
        self.closeBtn.setStyleSheet(button_style + f"""
            TitleBarButton {{
                qproperty-hoverColor: {Colors.Dark.TEXT_PRIMARY};
                qproperty-hoverBackgroundColor: {Colors.Dark.ERROR if is_dark else Colors.Light.ERROR};
                qproperty-pressedBackgroundColor: {Colors.Dark.SURFACE_LIGHT if is_dark else Colors.Light.SURFACE_LIGHT};
            }}
        """)
    
    def update_logo(self):
        self.logo_label.setPixmap(IconProvider.get_icon("logo", self._is_dark).pixmap(24, 24))
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.update_logo()
        self.menu_bar.update_theme(is_dark)
        self.customize_buttons(is_dark)
        self.theme_changed.emit(is_dark)
    
    def apply_theme(self, is_dark):
        self._is_dark = is_dark
        styles = Styles.get_styles(is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.menu_bar.update_theme(is_dark)
        self.update_logo()
        self.customize_buttons(is_dark)
