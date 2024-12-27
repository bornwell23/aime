import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, service_name=None):
        """
        Initialize a logger with configurable service name and log level
        
        Args:
            service_name (str, optional): Name of the service. Defaults to None.
        """
        self.service_name = service_name or os.getenv('SERVICE_NAME', 'unspecified-service')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Configure logging
        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        )
        
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(self.log_level)

    def _format_message(self, message):
        """
        Format log message with service name
        
        Args:
            message (str): Original log message
        
        Returns:
            str: Formatted log message
        """
        return f"[{self.service_name.upper()}] {message}"

    def error(self, message):
        """Log an error message"""
        self.logger.error(self._format_message(message))

    def warn(self, message):
        """Log a warning message"""
        self.logger.warning(self._format_message(message))

    def warning(self, message):
        """Log a warning message (alias for warn)"""
        self.logger.warning(self._format_message(message))

    def info(self, message):
        """Log an informational message"""
        self.logger.info(self._format_message(message))

    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(self._format_message(message))

    def update_log_level(self, log_level):
        """Update the log level"""
        self.log_level = log_level.upper()
        self.logger.setLevel(self.log_level)
    
    def update_name(self, service_name):
        """Update the service name"""
        self.service_name = service_name
        self.logger = logging.getLogger(self.service_name)


# Create a base logger that can be imported and customized
logger = Logger()
