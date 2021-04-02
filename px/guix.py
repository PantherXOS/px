import logging
import os
import subprocess
import sys

from .util import get_user, prompt_yes_no

log = logging.getLogger(__name__)


class Guix:
    def __init__(self, unattended=False):
      username, is_root = get_user()
      self.username = username
      self.is_root = is_root
      self.unattended = unattended

    def update_check(self):
      if self.is_root:
        log.info("=> Checking for system updates ...")
      else:
        log.info("=> Checking for user application updates ...")
        
      # TODO: Remove --disable-authentication
      subprocess.run(['guix', 'pull', '--disable-authentication'])

    def update(self):
      apply_update = False

      if not self.unattended:
        apply_update = prompt_yes_no('Would you like to apply all pending updates?')
      else:
        apply_update = True

      if self.is_root and apply_update:
        if os.path.isfile('/etc/system.scm') is not True:
          log.error('Could not find /etc/system.scm.')
          sys.exit()
        subprocess.run(['guix', 'system', 'reconfigure', '/etc/system.scm'])

      elif not self.is_root and apply_update:
        subprocess.run(['guix', 'package', '-u'])

      else:
        if self.is_root:
          log.info("To apply all pending updates manually, run: px system reconfigure /etc/system.scm")
        else:
          log.info("To apply all pending updates manually, run: px package -u")  
        exit(0)

    def run(self, arguments):
      subprocess.run(arguments)

    def _clear_substitute_cache():
      if self.is_root:
        os.rmdir('/var/guix/substitute/cache')
