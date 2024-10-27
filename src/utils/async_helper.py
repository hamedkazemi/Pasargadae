import asyncio
from functools import partial
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from src.utils.logger import Logger

class AsyncHelper(QObject):
    """Helper class to run async functions in Qt's event loop."""
    
    finished = pyqtSignal(object)
    error = pyqtSignal(Exception)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._loop = None
        self._task = None
        self._timer = None
    
    def run_async(self, coro):
        """Run an async coroutine in Qt's event loop."""
        Logger.debug(f"Running async coroutine: {coro.__qualname__}")
        
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            Logger.debug("Created new event loop")
        
        async def _wrapped_coro():
            try:
                Logger.debug("Starting coroutine execution")
                result = await coro
                Logger.debug(f"Coroutine completed with result: {result}")
                self.finished.emit(result)
            except Exception as e:
                Logger.exception("Coroutine failed with error")
                self.error.emit(e)
        
        self._task = self._loop.create_task(_wrapped_coro())
        Logger.debug("Created async task")
        
        if self._timer is not None:
            self._timer.stop()
        
        def _process_events():
            if not self._loop.is_running():
                Logger.debug("Processing events in event loop")
                self._loop.run_until_complete(self._task)
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(_process_events)
        self._timer.start(10)  # Process every 10ms
        Logger.debug("Started event processing timer")
        
        return self._task
    
    def __del__(self):
        if self._timer is not None:
            self._timer.stop()
        if self._loop is not None:
            self._loop.close()
