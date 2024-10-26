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
        elif pos in QRect(QPoint(bottom_left.x()+5, bottom_left.y()-5), 
                         QPoint(bottom_right.x()-5, bottom_right.y())):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.value = 2
        
        # Right resize
        elif pos in QRect(QPoint(top_right.x()-5, top_right.y()+5), 
                         QPoint(bottom_right.x(), bottom_right.y()-5)):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.value = 3
        
        # Left resize
        elif pos in QRect(QPoint(top_left.x(), top_left.y()+5), 
                         QPoint(bottom_left.x()+5, bottom_left.y()-5)):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.value = 4
        
        # Top-right resize
        elif pos in QRect(QPoint(top_right.x()-5, top_right.y()), 
                         QPoint(top_right.x(), top_right.y()+5)):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.value = 5
        
        # Bottom-left resize
        elif pos in QRect(QPoint(bottom_left.x(), bottom_left.y()-5), 
                         QPoint(bottom_left.x()+5, bottom_left.y())):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.value = 6
        
        # Top-left resize
        elif pos in QRect(QPoint(top_left.x(), top_left.y()), 
                         QPoint(top_left.x()+5, top_left.y()+5)):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.value = 7
        
        # Bottom-right resize
        elif pos in QRect(QPoint(bottom_right.x()-5, bottom_right.y()-5), 
                         QPoint(bottom_right.x(), bottom_right.y())):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.value = 8
        
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def resizing(self, ori, event, geo, value):
        current_pos = event.globalPosition().toPoint() - ori
        
        if value == 1:  # Top resize
            height = geo.height() - current_pos.y()
            y = geo.y() + current_pos.y()
            if height > self.minimumHeight():
                self.setGeometry(geo.x(), y, geo.width(), height)
        
        elif value == 2:  # Bottom resize
            height = geo.height() + current_pos.y()
            self.resize(geo.width(), height)
        
        elif value == 3:  # Right resize
            width = geo.width() + current_pos.x()
            self.resize(width, geo.height())
        
        elif value == 4:  # Left resize
            width = geo.width() - current_pos.x()
            x = geo.x() + current_pos.x()
            if width > self.minimumWidth():
                self.setGeometry(x, geo.y(), width, geo.height())
        
        elif value == 5:  # Top-right resize
            width = geo.width() + current_pos.x()
            height = geo.height() - current_pos.y()
            y = geo.y() + current_pos.y()
            if height > self.minimumHeight():
                self.setGeometry(geo.x(), y, width, height)
        
        elif value == 6:  # Bottom-left resize
