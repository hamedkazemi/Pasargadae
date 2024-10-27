import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Logger._initialized:
            # Create logs directory if it doesn't exist
            log_dir = os.path.expanduser("~/.pasargadae/logs")
            os.makedirs(log_dir, exist_ok=True)
            
            # Set up file handler
            log_file = os.path.join(log_dir, f"pasargadae_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s'
            ))
            
            # Set up console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s'
            ))
            
            # Configure root logger
            self.logger = logging.getLogger('pasargadae')
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
            Logger._initialized = True
    
    @classmethod
    def debug(cls, message):
        cls().logger.debug(message)
    
    @classmethod
    def info(cls, message):
        cls().logger.info(message)
    
    @classmethod
    def warning(cls, message):
        cls().logger.warning(message)
    
    @classmethod
    def error(cls, message):
        cls().logger.error(message)
    
    @classmethod
    def critical(cls, message):
        cls().logger.critical(message)
    
    @classmethod
    def exception(cls, message):
        cls().logger.exception(message)
