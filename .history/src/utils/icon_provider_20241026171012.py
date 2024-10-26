from PyQt6.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt6.QtCore import Qt, QSize
from src.theme.colors import Colors

class IconProvider:
    @staticmethod
    def get_icon(name: str, is_dark: bool = True) -> QIcon:
        # Convert hex color to QColor
        color_str = Colors.Dark.TEXT_PRIMARY if is_dark else Colors.Light.TEXT_PRIMARY
        color = QColor(color_str)
        
        # Create colored icon
        icon = QIcon(f"src/assets/icons/{name}.svg")
        sizes = [(16, 16), (24, 24), (32, 32)]
        colored_icon = QIcon()
        
        for size in sizes:
            pixmap = icon.pixmap(QSize(*size))
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(colored_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            
            # Set color
            painter.setPen(color)
            painter.setBrush(color)
            
            # Draw icon
            icon.paint(painter, 0, 0, pixmap.width(), pixmap.height())
            painter.end()
            
            colored_icon.addPixmap(colored_pixmap)
        
        return colored_icon
