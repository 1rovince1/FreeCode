import logging
import logging.config
import os
import sys

def setup_logging(LOG_DIR="logs", LOG_FILE="app.log"):
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILEPATH = os.path.join(LOG_DIR, LOG_FILE)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console_formatter": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s"
            },
            "file_formatter": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s"
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "console_formatter",
                "stream": sys.stdout
            },
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "file_formatter",
                "filename": LOG_FILEPATH,
                "maxBytes": 10*1024*1024,
                "backupCount": 5,
                "encoding": "utf-8"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console_handler", "file_handler"]
        }
    }

    logging.config.dictConfig(logging_config)
