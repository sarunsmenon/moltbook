"""Logging helpers for Moltbook entry points."""

import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from config import Settings


def setup_logging(log_name_prefix: str = "workflow") -> Path:
    """Configure application logging and return the log file path."""
    Settings.create_directories()

    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    log_file = Settings.LOGS_DIR / f"{log_name_prefix}_{timestamp}.log"
    log_level_str = Settings.LOG_LEVEL if isinstance(Settings.LOG_LEVEL, str) else "INFO"

    logging.basicConfig(
        level=getattr(logging, log_level_str),
        format=Settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, mode='w'),
        ],
        force=True,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging to: {log_file}")
    return log_file
