from PyQt6.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtSvg import QSvgRenderer
from io import BytesIO

class IconProvider:
    @staticmethod
    def get_icon(name: str, is_dark: bool = True) -> QIcon:
        # Use white for dark mode, dark gray for light mode
        color = QColor("#FFFFFF") if is_dark else QColor("#212121")
        
        # Read the SVG file
        with open(f"src/assets/icons/{name}.svg", 'r') as f:
            svg_content = f.read()
        
        # Replace the currentColor with our desired color
        svg_content = svg_content.replace('currentColor', color.name())
        
        # Create icon from modified SVG
        colored_icon = QIcon()
        sizes = [(16, 16), (24, 24), (32, 32)]
        
        # Create SVG renderer
        renderer = QSvgRenderer(BytesIO(svg_content.encode()))
        
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
