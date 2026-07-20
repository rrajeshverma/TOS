import logging
from pathlib import Path

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "tos.log"

LOG_LEVEL = logging.INFO

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | " "%(name)s | %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

ROTATING_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

BACKUP_COUNT = 5
