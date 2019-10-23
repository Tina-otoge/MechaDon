import logging

from mechadon.bot import MechaDon
import config

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    MechaDon(config)
