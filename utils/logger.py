"""
Application-wide logger configuration.
"""

import logging
import os
from pathlib import Path

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
# Create the logs directory if it doesn't exist.
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "job-alert.log"

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("job-alert")
