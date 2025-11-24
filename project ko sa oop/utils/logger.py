import logging
import os
from utils.constants import LOG_LEVEL, LOG_FORMAT, LOG_FILE


def setup_logging(name):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    

    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if log_dir:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
  
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging(__name__)
