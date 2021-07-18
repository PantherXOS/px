import logging
import subprocess

from .util import get_user, prompt_yes_no, runner
from .messages import MESSAGES_FLATPAK
from .config import COMMANDS_FLATPAK

log = logging.getLogger(__name__)


class Flatpak:
    def __init__(self, unattended=False):
        username, is_root = get_user()
        self.username = username
        self.is_root = is_root
        self.is_installed = self._installed()
        if self.is_installed:
            log.info(MESSAGES_FLATPAK['flatpak_found'])
        self.unattended = unattended

    def _installed(self):
        '''Check if Flatpak is installed. We silently catch the error.'''
        if not self.is_root:
            try:
                subprocess.run(
                    COMMANDS_FLATPAK['get_version'], capture_output=True)
                return True
            except:
                return False

    def update(self):
        if not self.is_root and self.is_installed:
            apply_update = False
            if self.unattended:
                apply_update = True
            else:
                apply_update = prompt_yes_no(
                    MESSAGES_FLATPAK['question_apply_updates'])

            if apply_update:
                runner(COMMANDS_FLATPAK['apply_updates'])
