'''This is primarily to update the channels file location'''
import os
from shutil import copyfile
from .config import CHANNELS_FILE_LEGACY, CHANNELS_FILE


def migrate_channels_file():
    '''This should only be used on root users'''
    if os.path.isfile(CHANNELS_FILE_LEGACY):
        if not os.path.isfile(CHANNELS_FILE):
            copyfile(CHANNELS_FILE_LEGACY, CHANNELS_FILE)
