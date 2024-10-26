from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import pyqtSignal, QObject

class DownloadContextMenuSignals(QObject):
    openFile = pyqtSignal(int)
    openWith = pyqtSignal(int)
    openFolder = pyqtSignal(int)
    moveRename = pyqtSignal(int)
    redownload = pyqtSignal(int)
    resumeDownload = pyqtSignal(int)
    stopDownload = pyqtSignal(int)
    refreshAddress = pyqtSignal(int)
    addToQueue = pyqtSignal(int)
    deleteFromQueue = pyqtSignal(int)
    showProperties = pyqtSignal(int)

class DownloadContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = DownloadContextMenuSignals()
        self.download_id = None
        self.setup_menu()
    
    def setup_menu(self):
        # File operations
        self.addAction("Open", lambda: self.signals.openFile.emit(self.download_id))
        self.addAction("Open With", lambda: self.signals.openWith.emit(self.download_id))
        self.addAction("Open Folder", lambda: self.signals.openFolder.emit(self.download_id))
        self.addSeparator()
        
        # File management
        self.addAction("Move/Rename", lambda: self.signals.moveRename.emit(self.download_id))
        self.addAction("Redownload", lambda: self.signals.redownload.emit(self.download_id))
        self.addSeparator()
        
        # Download control
        self.addAction("Resume Download", lambda: self.signals.resumeDownload.emit(self.download_id))
        self.addAction("Stop Download", lambda: self.signals.stopDownload.emit(self.download_id))
        self.addAction("Refresh Download Address", lambda: self.signals.refreshAddress.emit(self.download_id))
        self.addSeparator()
        
        # Queue operations
        self.addAction("Add to queue", lambda: self.signals.addToQueue.emit(self.download_id))
        self.addAction("Delete from Queue", lambda: self.signals.deleteFromQueue.emit(self.download_id))
        self.addSeparator()
        
        # Properties
        self.addAction("Properties", lambda: self.signals.showProperties.emit(self.download_id))
    
    def show_for_download(self, download_id, pos):
        """Show the context menu for a specific download"""
        self.download_id = download_id
        self.exec(pos)
