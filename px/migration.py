'''This is primarily to update the channels file location'''
import logging
import os
from shutil import copyfile

from .config import CHANNELS_FILE, CHANNELS_FILE_LEGACY

log = logging.getLogger(__name__)


def migrate_channels_file():
    '''This should only be used on root users'''
    if os.path.isfile(CHANNELS_FILE_LEGACY):
        if not os.path.isfile(CHANNELS_FILE):
            log.info('=> Copying channels file to new default location {}.'.format(CHANNELS_FILE))
            copyfile(CHANNELS_FILE_LEGACY, CHANNELS_FILE)
