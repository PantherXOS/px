import getpass
import logging
import os
from logging.handlers import RotatingFileHandler, SysLogHandler
from platform import system

from appdirs import user_data_dir

opsys = system()

ROOT_LOG = '/var/log/px.log'
USER_LOG_DIR = user_data_dir("px")
USER_LOG = USER_LOG_DIR + '/px.log'

log = logging.getLogger('px')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
formatter_cli = logging.Formatter('%(levelname)s: %(message)s')

log.setLevel(logging.DEBUG)

if opsys == 'Linux':
    import syslog

    current_user = getpass.getuser()
    log_file = ROOT_LOG
    if current_user != 'root':
        # For users we log to HOME since there's no access to `/var/log`
        log_file = USER_LOG
        # We create the folder if it does not exist.
        if not os.path.isdir(USER_LOG_DIR):
            os.makedirs(USER_LOG_DIR)

    fh = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # On Linux we engage syslog
    sh = SysLogHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(formatter)
    log.addHandler(sh)

# Default logging, on all systems
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter_cli)
log.addHandler(ch)
