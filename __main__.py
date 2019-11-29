import logging

from mechadon.bot import MechaDon
from config import config

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    MechaDon(config)
