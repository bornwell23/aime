#3rd party imports
import logging
import json
import os
from pythonjsonlogger import jsonlogger


def setup_logging():
    """
    Configure logging with JSON format and environment-based log level
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = os.getenv('LOG_FORMAT', 'json')

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))

    # JSON Formatter
    if log_format == 'json':
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s %(exc_info)s'
        )
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Global logger
logger = setup_logging()