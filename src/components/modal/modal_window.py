from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QEventLoop, pyqtSignal, QPoint
from qframelesswindow import FramelessWindow, StandardTitleBar
from src.theme.colors import Colors
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider
from src.components.window.window_controls import WindowControls

class ModalTitleBar(StandardTitleBar):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._is_dark = True
        self.setup_ui()
        self.apply_theme(self._is_dark)
        #self._drag_pos = None
    
    def setup_ui(self):
        # Create custom layout
        custom_widget = QWidget(self)
        layout = QHBoxLayout(custom_widget)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(10)
        
        # Logo and title
        self.logo_label = QLabel()        

        # Add widgets to layout
        layout.addWidget(self.logo_label)
        layout.addStretch()
        
        # Add custom widget to title bar (before the window controls)
        self.hBoxLayout.insertWidget(0, custom_widget, 1)
        
        # Create a new widget for the right side controls
        right_controls = QWidget(self)
        right_layout = QHBoxLayout(right_controls)
        right_layout.setContentsMargins(0, 0, 10, 0)
        right_layout.setSpacing(0)
        
        # Add the controls in the desired order
        right_layout.addWidget(self.minBtn)
        #right_layout.addWidget(self.maxBtn)
        self.maxBtn.hide()
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
        self.customize_buttons(is_dark)
        self.theme_changed.emit(is_dark)
    
    def apply_theme(self, is_dark):
        self._is_dark = is_dark
        styles = Styles.get_styles(is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.update_logo()
        self.customize_buttons(is_dark)

class ModalWindow(FramelessWindow):
    finished = pyqtSignal()  # Signal emitted when the modal is closed
    
    def __init__(self, parent=None, title="", width=400, height=300):
        super().__init__(parent=parent)
        self._is_dark = True
        self._title = title
        self._result = 0
        self._parent = parent  # Store parent just for positioning
        
        # Set window flags to make it a proper modal
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  # Clean up on close
        
        self.title_bar = ModalTitleBar(self)
        self.title_bar.setTitle(title)
        self.setTitleBar(self.title_bar)
        
        # Set size
        self.setFixedSize(width, height)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.main_layout.addWidget(self.title_bar)
        
        # Create container widget with border radius
        self.content_container = QWidget()
        self.content_container.setObjectName("modalContainer")
        container_layout = QVBoxLayout(self.content_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        
        # Action buttons area
        self.action_area = QWidget()
        self.action_layout = QHBoxLayout(self.action_area)
        self.action_layout.setContentsMargins(15, 10, 15, 15)
        self.action_layout.addStretch()
        
        # Add all sections to container
        container_layout.addWidget(self.content_area)
        container_layout.addWidget(self.action_area)
        
        # Add container to main layout
        self.main_layout.addWidget(self.content_container)
        
        self.update_style()
    
    def add_action_button(self, text, callback, primary=False):
        """Add an action button to the modal"""
        from PyQt6.QtWidgets import QPushButton
        button = QPushButton(text)
        button.setFixedHeight(32)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        if primary:
            button.setObjectName("primaryButton")
        else:
            button.setObjectName("secondaryButton")
        self.action_layout.addWidget(button)
        return button
    
    def set_content(self, widget):
        """Set the main content widget of the modal"""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())): 
            self.content_layout.itemAt(i).widget().setParent(None)
        self.content_layout.addWidget(widget)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.title_bar.update_theme(is_dark)
        self.update_style()
    
    def update_style(self):
        base_style = f"""
            QWidget#modalContainer {{
                background-color: {"#15161A" if self._is_dark else "#FFFFFF"};
                border-radius: 10px;
                border: 1px solid {"#26272B" if self._is_dark else "#E0E0E0"};
            }}
            
            QLabel {{
                color: {"#FFFFFF" if self._is_dark else "#212121"};
            }}
            
            QPushButton {{
                border-radius: 4px;
                padding: 5px 15px;
            }}
            
            QPushButton#primaryButton {{
                background-color: {"#2196F3" if self._is_dark else "#1976D2"};
                color: white;
                border: none;
            }}
            
            QPushButton#primaryButton:hover {{
                background-color: {"#1976D2" if self._is_dark else "#1565C0"};
            }}
            
            QPushButton#secondaryButton {{
                background-color: transparent;
                color: {"#FFFFFF" if self._is_dark else "#212121"};
                border: 1px solid {"#26272B" if self._is_dark else "#E0E0E0"};
            }}
            
            QPushButton#secondaryButton:hover {{
                background-color: {"rgba(255, 255, 255, 0.1)" if self._is_dark else "rgba(0, 0, 0, 0.05)"};
            }}
            
            #modalSeparator {{
                background-color: {"#26272B" if self._is_dark else "#E0E0E0"};
                height: 1px;
            }}
        """
        
        self.setStyleSheet(base_style)
    
    def showEvent(self, event):
        """Center the modal on screen when shown"""
        super().showEvent(event)
        if self._parent:
            parent_geo = self._parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - self.width()) // 2
            y = parent_geo.y() + (parent_geo.height() - self.height()) // 2
            self.move(x, y)
    
    def closeEvent(self, event):
        """Handle window close event"""
        super().closeEvent(event)
        self.finished.emit()
    
    def exec(self):
        """Show the modal window and wait for it to close"""
        self.show()
        # Create event loop
        loop = QEventLoop()
        self.finished.connect(loop.quit)
        loop.exec()
        return self._result
    
    def done(self, result):
        """Close the modal with a result"""
        self._result = result
        self.close()
