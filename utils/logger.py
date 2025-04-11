"""
Custom logging module for the ParaBank automation framework.

Handles log configuration, file/console handlers, and formatted output for test execution.

@author: Raed Eleyan
@date: 04/07/2025
@contact: raedeleyan1@gmail.com
"""
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

class Logger:
    """Logger class to handle logging configuration and operations."""

    def __init__(self, name: str = None, log_level: int = logging.INFO):
        if name is None:
            if "__main__" in sys.argv[0]:
                script_path = sys.argv[0]
                script_name = os.path.splitext(os.path.basename(script_path))[0]
                name = script_name
            else:
                name = __name__
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.log_dir = Path('../logs')
        self._configure_handlers()

    def _configure_handlers(self) -> None:
        """Set up file and console handlers with formatters."""
        # Create logs directory if missing
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Timestamped log file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = self.log_dir / f"execution_{timestamp}.log"

        # Log formatting
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        """Log an info-level message."""
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log an error-level message."""
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Log a debug-level message."""
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """Log a warning-level message."""
        self.logger.warning(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)
