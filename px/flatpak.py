import logging
import subprocess

from .util import get_user, prompt_yes_no

log = logging.getLogger(__name__)


class Flatpak:
    def __init__(self, unattended=False):
        username, is_root = get_user()
        self.username = username
        self.is_root = is_root
        self.installed = self.installed()
        self.unattended = unattended

    def installed(self):
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

            if self.installed and apply_update:
                log.info('Found Flatpak installation. Updating related packages.')
                subprocess.run(['flatpak', '--user', '--assumeyes', '--noninteractive', 'update'])
