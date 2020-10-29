import subprocess
from .log import Logger
from .util import prompt_yes_no, get_user


log = Logger(__name__)


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
        
      subprocess.run(['guix', 'pull', '--disable-authentication'])

    def update(self):
      apply_update = False

      if not self.unattended:
        apply_update = prompt_yes_no('Would you like to apply all pending updates?')

      if self.is_root and apply_update:
        if os.path.isfile('/etc/system.scm') is not True:
          log.error('Could not find /etc/system.scm.')
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