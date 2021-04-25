import logging
import subprocess

from .util import get_user, prompt_yes_no, runner

log = logging.getLogger(__name__)


class Flatpak:
    def __init__(self, unattended=False):
        username, is_root = get_user()
        self.username = username
        self.is_root = is_root
        self.is_installed = self._installed()
        self.unattended = unattended

    def _installed(self):
        '''Check if Flatpak is installed. We silently catch the error.'''
        if not self.is_root:
            try:
                subprocess.run(["flatpak", "--version"], capture_output=True)
                return True
            except:
                return False

    def update(self):
        if not self.is_root:
            apply_update = False
            if not self.unattended:
                apply_update = prompt_yes_no('Would you like to apply all pending Flatpak updates?')
            else:
                apply_update = True

            if self.is_installed and apply_update:
                log.info('Found Flatpak installation. Updating related packages.')
                runner(['flatpak', '--user', '--assumeyes', '--noninteractive', 'update'])
