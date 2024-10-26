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
        
        # Install event filter for resize handling
        self.installEventFilter(self)
    
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
                self.resizing(event)
        
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
            self.resize_area = "top"
        
        # Bottom resize
        elif pos in QRect(QPoint(bottom_left.x()+5, bottom_left.y()-5),
                         QPoint(bottom_right.x()-5, bottom_right.y())):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.resize_area = "bottom"
        
        # Right resize
        elif pos in QRect(QPoint(top_right.x()-5, top_right.y()+5),
                         QPoint(bottom_right.x(), bottom_right.y()-5)):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.resize_area = "right"
        
        # Left resize
        elif pos in QRect(QPoint(top_left.x(), top_left.y()+5),
                         QPoint(bottom_left.x()+5, bottom_left.y()-5)):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.resize_area = "left"
        
        # Top-right resize
        elif pos in QRect(QPoint(top_right.x()-5, top_right.y()),
                         QPoint(top_right.x(), top_right.y()+5)):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.resize_area = "top_right"
        
        # Bottom-left resize
        elif pos in QRect(QPoint(bottom_left.x(), bottom_left.y()-5),
                         QPoint(bottom_left.x()+5, bottom_left.y())):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.resize_area = "bottom_left"
        
        # Top-left resize
        elif pos in QRect(QPoint(top_left.x(), top_left.y()),
                         QPoint(top_left.x()+5, top_left.y()+5)):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.resize_area = "top_left"
        
        # Bottom-right resize
        elif pos in QRect(QPoint(bottom_right.x()-5, bottom_right.y()-5),
                         QPoint(bottom_right.x(), bottom_right.y())):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.resize_area = "bottom_right"
        
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.resize_area = None
    
    def resizing(self, event):
        if not hasattr(self, 'resize_area') or not self.resize_area:
            return
        
        pos = event.globalPosition().toPoint()
        geo = self.geometry()
        
        if self.resize_area == "top":
            diff = pos.y() - self.origin.y()
            new_height = self.ori_geo.height() - diff
            new_y = self.ori_geo.y() + diff
            if new_height > self.minimumHeight():
                self.setGeometry(geo.x(), new_y, geo.width(), new_height)
        
        elif self.resize_area == "bottom":
            diff = pos.y() - self.origin.y()
            new_height = self.ori_geo.height() + diff
            if new_height > self.minimumHeight():
                self.resize(geo.width(), new_height)
        
        elif self.resize_area == "right":
            diff = pos.x() - self.origin.x()
            new_width = self.ori_geo.width() + diff
            if new_width > self.minimumWidth():
                self.resize(new_width, geo.height())
        
        elif self.resize_area == "left":
            diff = pos.x() - self.origin.x()
            new_width = self.ori_geo.width() - diff
            new_x = self.ori_geo.x() + diff
            if new_width > self.minimumWidth():
                self.setGeometry(new_x, geo.y(), new_width, geo.height())
        
        elif self.resize_area == "top_right":
            x_diff = pos.x() - self.origin.x()
            y_diff = pos.y() - self.origin.y()
            new_width = self.ori_geo.width() + x_diff
            new_height = self.ori_geo.height() - y_diff
            new_y = self.ori_geo.y() + y_diff
            if new_height > self.minimumHeight() and new_width > self.minimumWidth():
                self.setGeometry(geo.x(), new_y, new_width, new_height)
        
        elif self.resize_area == "bottom_left":
            x_diff = pos.x() - self.origin.x()
            y_diff = pos.y() - self.origin.y()
            new_width = self.ori_geo.width() - x_diff
            new_height = self.ori_geo.height() + y_diff
            new_x = self.ori_geo.x() + x_diff
            if new_width > self.minimumWidth():
                self.setGeometry(new_x, geo.y(), new_width, new_height)
        
        elif self.resize_area == "top_left":
            x_diff = pos.x() - self.origin.x()
            y_diff = pos.y() - self.origin.y()
            new_width = self.ori_geo.width() - x_diff
            new_height = self.ori_geo.height() - y_diff
            new_x = self.ori_geo.x() + x_diff
            new_y = self.ori_geo.y() + y_diff
            if new_height > self.minimumHeight() and new_width > self.minimumWidth():
                self.setGeometry(new_x, new_y, new_width, new_height)
        
        elif self.resize_area == "bottom_right":
            x_diff = pos.x() - self.origin.x()
            y_diff = pos.y() - self.origin.y()
            new_width = self.ori_geo.width() + x_diff
            new_height = self.ori_geo.height() + y_diff
            self.resize(new_width, new_height)
