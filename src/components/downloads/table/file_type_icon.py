from PyQt6.QtWidgets import QTableWidgetItem
from src.utils.icon_provider import IconProvider

class FileTypeIcon(QTableWidgetItem):
    def __init__(self, file_type, is_dark=True):
        super().__init__()
        self.file_type = file_type
        icon_map = {
            'image': 'image',
            'music': 'music',
            'video': 'video',
            'document': 'document',
            'program': 'options',
            'archive': 'document'
        }
        icon_name = icon_map.get(file_type, 'document')
        self.setIcon(IconProvider.get_icon(icon_name, is_dark))
