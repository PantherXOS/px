import sys
import syslog
import logging
from os import environ


logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))


class Logger:
    def __init__(self, context, application='px'):
        self.context = context
        self.name = application
        self.log = logging.getLogger(self.name)

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)
        # syslog.syslog(syslog.LOG_INFO, message)

    def warning(self, message):
        self.log.warning(message)
        syslog.syslog(syslog.LOG_WARNING, message)

    def error(self, message):
        self.log.error(message)
        syslog.syslog(syslog.LOG_ERR, message)