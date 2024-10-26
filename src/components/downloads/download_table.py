from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal
from src.theme.styles import Styles
from .table.header_checkbox import HeaderCheckBox
from .table.row_checkbox import RowCheckBox
from .table.file_type_icon import FileTypeIcon
from .table.context_menu import DownloadContextMenu
from .table.header_context_menu import HeaderContextMenu
from .table.table_actions import TableActions
from .table.table_data_handler import TableDataHandler

class DownloadTable(QTableWidget):
    sortingChanged = pyqtSignal(int, Qt.SortOrder)  # column, order
    
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.actions = TableActions()
        self.data_handler = TableDataHandler()
        self.context_menu = DownloadContextMenu(self)
        self.header_context_menu = HeaderContextMenu(self)
        self.setup_ui()
        self.setup_context_menus()
        self.setup_sorting()
        self.load_data()
        self.connect_signals()
    
    def setup_ui(self):
        headers = ["", "", "Name", "Size", "Status", "Time Left", 
                  "Last Modified", "Speed"]
        
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Customize header
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setDefaultSectionSize(150)
        header.setStretchLastSection(True)
        
        # Set column widths
        self.setColumnWidth(0, 40)  # Checkbox
        self.setColumnWidth(1, 30)  # Icon
        
        # Add header checkbox
        self.header_checkbox = HeaderCheckBox(self._is_dark)
        self.header_checkbox.stateChanged.connect(self.toggle_all_checkboxes)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setHorizontalHeaderWidget(0, self.header_checkbox)
        
        self.setStyleSheet(Styles.get_styles(self._is_dark)["TABLE"])
    
    def setup_sorting(self):
        header = self.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.sectionClicked.connect(self.handle_sort)
        self.setSortingEnabled(True)
        
        # Initialize sort state
        self._current_sort_column = -1
        self._current_sort_order = Qt.SortOrder.AscendingOrder
    
    def handle_sort(self, logical_index):
        if logical_index in [0, 1]:  # Skip checkbox and icon columns
            return
        
        header = self.horizontalHeader()
        
        # Update sort order
        if self._current_sort_column == logical_index:
            # Toggle sort order if clicking the same column
            self._current_sort_order = (Qt.SortOrder.DescendingOrder 
                if self._current_sort_order == Qt.SortOrder.AscendingOrder 
                else Qt.SortOrder.AscendingOrder)
        else:
            # First click on new column, start with ascending
            self._current_sort_order = Qt.SortOrder.AscendingOrder
            self._current_sort_column = logical_index
        
        # Set the sort indicator before sorting
        header.setSortIndicator(logical_index, self._current_sort_order)
        
        # Perform the sort
        self.sortItems(logical_index, self._current_sort_order)
        
        # Emit the sorting changed signal
        self.sortingChanged.emit(logical_index, self._current_sort_order)
    
    def handle_search(self, search_text):
        """Filter table rows based on search text"""
        # Store current sort state
        sort_column = self._current_sort_column
        sort_order = self._current_sort_order
        
        # Temporarily disable sorting
        self.setSortingEnabled(False)
        
        # Get filtered downloads and update table
        filtered_downloads = self.data_handler.filter_downloads(search_text)
        self.populate_table(filtered_downloads)
        
        # Restore sorting
        self.setSortingEnabled(True)
        if sort_column >= 0:
            self.sortItems(sort_column, sort_order)
    
    def populate_table(self, downloads):
        """Populate table with the given downloads"""
        self.setRowCount(len(downloads))
        for row, download in enumerate(downloads):
            items = self.data_handler.create_table_items(download, self._is_dark)
            
            # Set items in table
            self.setItem(row, 0, items['id'])
            self.setCellWidget(row, 0, items['checkbox'])
            self.setItem(row, 1, items['icon'])
            self.setItem(row, 2, items['name'])
            self.setItem(row, 3, items['size'])
            
            if isinstance(items['status'], QTableWidgetItem):
                self.setItem(row, 4, items['status'])
            else:
                self.setCellWidget(row, 4, items['status'])
            
            self.setItem(row, 5, items['time_left'])
            self.setItem(row, 6, items['modified'])
            self.setItem(row, 7, items['speed'])
    
    def setup_context_menus(self):
        # Download context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Header context menu
        header = self.horizontalHeader()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_header_context_menu)
    
    def show_context_menu(self, pos):
        row = self.rowAt(pos.y())
        if row >= 0:
            download_id = self.item(row, 0).data(Qt.ItemDataRole.UserRole)
            self.context_menu.show_for_download(download_id, self.mapToGlobal(pos))
    
    def show_header_context_menu(self, pos):
        self.header_context_menu.show_menu(self.horizontalHeader().mapToGlobal(pos))
    
    def connect_signals(self):
        # Connect context menu signals to handlers
        self.context_menu.signals.openFile.connect(self.actions.handle_open_file)
        self.context_menu.signals.openWith.connect(self.actions.handle_open_with)
        self.context_menu.signals.openFolder.connect(self.actions.handle_open_folder)
        self.context_menu.signals.moveRename.connect(self.actions.handle_move_rename)
        self.context_menu.signals.redownload.connect(self.actions.handle_redownload)
        self.context_menu.signals.resumeDownload.connect(self.actions.handle_resume_download)
        self.context_menu.signals.stopDownload.connect(self.actions.handle_stop_download)
        self.context_menu.signals.refreshAddress.connect(self.actions.handle_refresh_address)
        self.context_menu.signals.addToQueue.connect(self.actions.handle_add_to_queue)
        self.context_menu.signals.deleteFromQueue.connect(self.actions.handle_delete_from_queue)
        self.context_menu.signals.showProperties.connect(self.actions.handle_show_properties)
        
        # Connect header context menu signals
        self.header_context_menu.signals.columnVisibilityChanged.connect(
            self.toggle_column_visibility)
    
    def toggle_column_visibility(self, column, visible):
        self.setColumnHidden(column, not visible)
    
    def setHorizontalHeaderWidget(self, column, widget):
        self.horizontalHeader().setMinimumSectionSize(widget.sizeHint().width())
        self.setCellWidget(0, column, widget)
    
    def toggle_all_checkboxes(self, checked):
        for row in range(self.rowCount()):
            checkbox = self.cellWidget(row, 0)
            if checkbox and isinstance(checkbox, RowCheckBox):
                checkbox.setChecked(checked)
    
    def load_data(self):
        downloads = self.data_handler.load_data()
        self.populate_table(downloads)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.header_checkbox.update_style()
        self.setStyleSheet(Styles.get_styles(self._is_dark)["TABLE"])
        
        for row in range(self.rowCount()):
            # Update checkbox
            checkbox = self.cellWidget(row, 0)
            if isinstance(checkbox, RowCheckBox):
                checkbox.update_style()
            
            # Update file type icon
            icon_item = self.item(row, 1)
            if isinstance(icon_item, FileTypeIcon):
                self.setItem(row, 1, FileTypeIcon(icon_item.file_type, is_dark))
