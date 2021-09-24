import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('config.env'), override=True)


class Config:

    debug = bool(os.getenv('debug', False))

    if debug:
        host = 'localhost'
        port = 80
    else:
        host = '0.0.0.0'
        port = 7777
