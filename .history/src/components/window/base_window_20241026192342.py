from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QCursor

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.press_control = 0
        self.value = 0
        self.installEventFilter(self)
        
        # Set minimum size
        self.setMinimumSize(800, 600)
    
    def eventFilter(self, obj, event):
        # Hover move event
        if event.type() == QEvent.Type.HoverMove:
            if self.press_control == 0:
                self.pos_control(event)
        
        # Mouse press event
        elif event.type() == QEvent.Type.MouseButtonPress:
            self.press_control = 1
            self.origin = self.mapToGlobal(event.position().toPoint())
            self.ori_geo = self.geometry()
        
        # Mouse release event
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.press_control = 0
            self.pos_control(event)
        
        # Mouse move event
        elif event.type() == QEvent.Type.MouseMove:
            if self.cursor().shape() != Qt.CursorShape.ArrowCursor:
                self.resizing(self.origin, event, self.ori_geo, self.value)
        
        return super().eventFilter(obj, event)
    
    def pos_control(self, event):
        rect = self.rect()
        top_left = rect.topLeft()
        top_right = rect.topRight()
        bottom_left = rect.bottomLeft()
        bottom_right = rect.bottomRight()
        pos = event.position().toPoint()
        
        # Top resize
        if pos in QRect(QPoint(top_left.x()+5, top_left.y()), 
                       QPoint(top_right.x()-5, top_right.y()+5)):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.value = 1
        
        # Bottom resize
