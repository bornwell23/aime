import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.service_name = os.getenv('SERVICE_NAME', 'ui')
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
        return f"[{self.service_name.upper()}] {message}"

    def error(self, message):
        self.logger.error(self._format_message(message))

    def warn(self, message):
        self.logger.warning(self._format_message(message))

    def warning(self, message):
        self.logger.warning(self._format_message(message))

    def info(self, message):
        self.logger.info(self._format_message(message))

    def debug(self, message):
        self.logger.debug(self._format_message(message))

# Create a singleton instance
logger = Logger()
