from PyQt6.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt6.QtCore import Qt, QSize, QByteArray
from PyQt6.QtSvg import QSvgRenderer
from src.theme.colors import Colors

class IconProvider:
    @staticmethod
    def get_icon(name: str, is_dark: bool = True) -> QIcon:
        # Get color from theme
        colors = Colors.Dark if is_dark else Colors.Light
        color = QColor(colors.ICON_COLOR)
        
        # Read the SVG file
        with open(f"src/assets/icons/{name}.svg", 'r') as f:
            svg_content = f.read()
        
        # Replace the currentColor with our desired color
        svg_content = svg_content.replace('currentColor', color.name())
        
        # Convert string to QByteArray
        svg_bytes = QByteArray(svg_content.encode())
        
        # Create icon from modified SVG
        colored_icon = QIcon()
        sizes = [(16, 16), (24, 24), (32, 32)]
        
        # Create SVG renderer
        renderer = QSvgRenderer(svg_bytes)
        
        for size in sizes:
            pixmap = QPixmap(*size)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            
            # Render SVG with the correct color
            renderer.render(painter)
            painter.end()
            
            colored_icon.addPixmap(pixmap)
        
        return colored_icon
