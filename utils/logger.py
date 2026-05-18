import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("teaching_agents")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Avoid duplicate handlers
if not logger.handlers:

    file_handler = logging.FileHandler("logs/app.log")

    error_handler = logging.FileHandler("logs/errors.log")

    error_handler.setLevel(logging.ERROR)

    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(error_handler)