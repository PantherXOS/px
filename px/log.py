import getpass
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
from platform import system

opsys = system()

ROOT_LOG_DIR = '/var/log/px.log'
USER_LOG_DIR = user_data_dir("px") + '/px.log'

log = logging.getLogger('px')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
formatter_cli = logging.Formatter('%(levelname)s: %(message)s')

log.setLevel(logging.DEBUG)

if opsys == 'Linux':
    from appdirs import user_data_dir
    import syslog

    current_user = getpass.getuser()
    logdir = ROOT_LOG_DIR
    if current_user != 'root':
        # For users we log to HOME since there's no access to `/var/log`
        logdir = USER_LOG_DIR

    fh = RotatingFileHandler(logdir, maxBytes=10000, backupCount=1)
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
