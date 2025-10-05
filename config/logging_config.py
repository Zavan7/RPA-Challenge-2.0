import logging
from logging.handlers import RotatingFileHandler
import os

# Pasta de logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Arquivo de log
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Formato profissional
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(level=logging.INFO):
    """Configura logging para o projeto inteiro"""
    logging.basicConfig(
        level=level,  # DEBUG para dev / INFO para produção
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
        ]
    )
