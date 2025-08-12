import logging
import sys
from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    fmt = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

def load_env():
    load_dotenv()
