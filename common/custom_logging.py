import logging
from dotenv import load_dotenv
import os


load_dotenv()

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))
