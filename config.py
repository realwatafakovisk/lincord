import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = '!'

DATABASE_URL = os.getenv('DATABASE_URL')

LINCORD_CMD_CHANNEL = 'lincord-cmd'
SETUP_CHANNEL_NAME = 'lincord-setup'

COLORS = {
    'SUCCESS': 0x00ff00,
    'ERROR': 0xff0000,
    'INFO': 0x0099ff,
    'WARNING': 0xff9900
}

ACTIVATED_SERVERS = set()
LOCKED_SERVERS = set()

DATA_DIR = 'data'
COGS_DIR = 'cogs'
APT_PACKAGES_DIR = 'apt-packages'
