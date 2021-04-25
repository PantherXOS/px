import logging
import os
import sys

from .util import get_user, prompt_yes_no, runner

log = logging.getLogger(__name__)


class Guix:
    def __init__(self, unattended=False):
        username, is_root = get_user()
        self.username = username
        self.is_root = is_root
        self.unattended = unattended

    def update_check(self):
        '''Check for new updates'''
        if self.is_root:
            log.info("=> Checking for system updates ...")
        else:
            log.info("=> Checking for user application updates ...")
        
        # TODO: Remove --disable-authentication
        if os.path.isfile('/etc/channels.scm'):
            '''If we find /etc/channels.scm we automatically use this for updates'''
            log.info('Found global channels file at /etc/channels.scm, defaulting to that.')
            runner(['guix', 'pull', '--disable-authentication', '--channels=/etc/channels.scm'])
        else:
            runner(['guix', 'pull', '--disable-authentication'])

    def update(self):
        '''Apply new updates'''
        apply_update = False

        if not self.unattended:
            apply_update = prompt_yes_no('Would you like to apply all pending updates?')
        else:
            apply_update = True

        if self.is_root and apply_update:
            '''Updates under root user'''
            if os.path.isfile('/etc/system.scm') is not True:
                log.error('Could not find /etc/system.scm.')
                sys.exit()
            runner(['guix', 'system', 'reconfigure', '/etc/system.scm'])

        elif not self.is_root and apply_update:
            '''Updates under standard user'''
            runner(['guix', 'package', '-u'])

        else:
            if self.is_root:
                log.info("To apply all pending updates manually, run: px system reconfigure /etc/system.scm")
            else:
                log.info("To apply all pending updates manually, run: px package -u")  
            exit(0)

    def run(self, arguments):
        runner(arguments)

    def maintenance(self):
        self._clear_substitute_cache()
        self._run_maintenance_scripts()

    def _clear_substitute_cache(self):
        location = '/var/guix/substitute/cache'
        if self.is_root:
            try:
                os.rmdir(location)
            except:
                log.error('Failed to delete substitues cache at {}'.format(location))

    def _run_maintenance_scripts(self):
        runner(['fc-cache', '-rv'])
