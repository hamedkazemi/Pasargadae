from .colors import Colors
from .styles import (
    get_window_styles,
    get_menu_styles,
    get_toolbar_styles,
    get_tree_styles,
    get_table_styles,
    get_progress_styles,
    get_disk_space_styles,
    get_search_styles
)

class Styles:
    @staticmethod
    def get_styles(is_dark=True):
        colors = Colors.Dark if is_dark else Colors.Light
        
        return {
            "WINDOW": get_window_styles(colors),
            "MENU": get_menu_styles(colors),
            "TOOLBAR": get_toolbar_styles(colors),
            "TREE": get_tree_styles(colors),
            "TABLE": get_table_styles(colors),
            "PROGRESS": get_progress_styles(colors),
            "DISK_SPACE": get_disk_space_styles(colors),
            "SEARCH": get_search_styles(colors)
        }
