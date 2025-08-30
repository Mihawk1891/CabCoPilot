from loguru import logger
import os

# Configure a sane default log format
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL,
           format="<level>{level: <8}</level> | <cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | "
                  "<green>{name}</green>:<yellow>{function}</yellow>:<magenta>{line}</magenta> - "
                  "<level>{message}</level>")
