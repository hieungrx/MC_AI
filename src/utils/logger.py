import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name="AI_MC", log_file="logs/app.log", level=logging.INFO, max_bytes=10485760, backup_count=5):
    """
    Sets up a logger with both console and rotating file handlers.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    # Log message format
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler
    try:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Failed to set up rotating file handler for logging: {e}")

    return logger

# Create a default system logger
logger = setup_logger()
