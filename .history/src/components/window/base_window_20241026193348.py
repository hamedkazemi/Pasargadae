from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, QPoint, QRect, QEvent
from PyQt6.QtGui import QCursor

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.press_control = 0
        self._drag_pos = None
        self.resize(1200, 800)
        
        # Enable mouse tracking
        self.setMouseTracking(True)
        
        # Install event filter for resize handling
        self.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        # Mouse press event
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                self.press_control = 1
                self.origin = event.globalPosition().toPoint()
                self.ori_geo = self.geometry()
        
        # Mouse release event
        elif event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                self.press_control = 0
                self.setCursor(Qt.CursorShape.ArrowCursor)
        
        # Mouse move event
        elif event.type() == QEvent.Type.MouseMove:
            if not self.isMaximized():
                self.handle_resize(event)
        
        return super().eventFilter(obj, event)
    
    def handle_resize(self, event):
        pos = event.position().toPoint()
        rect = self.rect()
        
        # Define resize areas
        border = 5
        top = pos.y() <= border
        bottom = pos.y() >= rect.height() - border
        left = pos.x() <= border
        right = pos.x() >= rect.width() - border
        
        # Set appropriate cursor and store resize direction
        if top and left:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.resize_area = "top_left"
        elif top and right:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.resize_area = "top_right"
        elif bottom and left:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.resize_area = "bottom_left"
        elif bottom and right:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.resize_area = "bottom_right"
        elif top:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.resize_area = "top"
        elif bottom:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.resize_area = "bottom"
        elif left:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.resize_area = "left"
        elif right:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.resize_area = "right"
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.resize_area = None
        
        # Handle resizing if mouse is pressed
        if event.buttons() & Qt.MouseButton.LeftButton and hasattr(self, 'resize_area') and self.resize_area:
            global_pos = event.globalPosition().toPoint()
            diff = global_pos - self.origin
            new_geometry = self.ori_geo
            
            if self.resize_area == "top_left":
                if self.minimumWidth() <= new_geometry.width() - diff.x() and \
                   self.minimumHeight() <= new_geometry.height() - diff.y():
                    new_geometry.setTopLeft(new_geometry.topLeft() + diff)
            
            elif self.resize_area == "top_right":
                if self.minimumWidth() <= new_geometry.width() + diff.x() and \
                   self.minimumHeight() <= new_geometry.height() - diff.y():
                    new_geometry.setTopRight(new_geometry.topRight() + diff)
            
            elif self.resize_area == "bottom_left":
                if self.minimumWidth() <= new_geometry.width() - diff.x() and \
                   self.minimumHeight() <= new_geometry.height() + diff.y():
                    new_geometry.setBottomLeft(new_geometry.bottomLeft() + diff)
            
            elif self.resize_area == "bottom_right":
                if self.minimumWidth() <= new_geometry.width() + diff.x() and \
                   self.minimumHeight() <= new_geometry.height() + diff.y():
                    new_geometry.setBottomRight(new_geometry.bottomRight() + diff)
            
            elif self.resize_area == "top":
                if self.minimumHeight() <= new_geometry.height() - diff.y():
                    new_geometry.setTop(new_geometry.top() + diff.y())
            
            elif self.resize_area == "bottom":
                if self.minimumHeight() <= new_geometry.height() + diff.y():
                    new_geometry.setBottom(new_geometry.bottom() + diff.y())
            
            elif self.resize_area == "left":
                if self.minimumWidth() <= new_geometry.width() - diff.x():
                    new_geometry.setLeft(new_geometry.left() + diff.x())
            
            elif self.resize_area == "right":
                if self.minimumWidth() <= new_geometry.width() + diff.x():
                    new_geometry.setRight(new_geometry.right() + diff.x())
            
            self.setGeometry(new_geometry)
