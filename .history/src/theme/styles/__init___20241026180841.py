from src.theme.colors import Colors
from .window import get_window_styles
from .menu import get_menu_styles
from .toolbar import get_toolbar_styles
from .tree import get_tree_styles
from .table import get_table_styles
from .progress import get_progress_styles
from .disk_space import get_disk_space_styles
from .search import get_search_styles

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
