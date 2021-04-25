import logging
import os
import pwd
import subprocess

log = logging.getLogger(__name__)


def prompt_yes_no(question):
    '''Inline user command line prompt'''
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def get_user():
    '''Returns username and a bool whether user is root or not'''
    username = pwd.getpwuid( os.getuid() )[ 0 ]
    is_root = False

    if username == 'root':
        is_root = True

    return username, is_root


def runner(arguments):
    '''Command Runner'''
    res = subprocess.run(arguments, capture_output=True)
    if res.stderr:
        log.error(res.stderr)