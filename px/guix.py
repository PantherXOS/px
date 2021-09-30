import logging
import os

from .util import get_user, prompt_yes_no, runner
from .config import CHANNELS_FILE, CHANNELS_FILE_LEGACY, SYSTEM_CONFIG_FILE, SUBSTITUTE_CACHE_PATH, COMMANDS
from .messages import MESSAGES
from .migration import migrate_channels_file

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
            log.info(MESSAGES['check_system_updates'])
            migrate_channels_file()
        else:
            log.info(MESSAGES['check_user_updates'])

        if os.path.isfile(CHANNELS_FILE):
            '''If we find /etc/guix/channels.scm we automatically use this for updates'''
            log.info(MESSAGES['channels_found'])
            runner(COMMANDS['get_updates_overwrite'])
        elif os.path.isfile(CHANNELS_FILE_LEGACY):
            '''[LEGACY] If we find /etc/channels.scm we automatically use this for updates'''
            log.info(MESSAGES['channels_found_legacy'])
            runner(COMMANDS['get_updates_overwrite_legacy'])
        else:
            '''If we don't find any channels file, use whatever is default ... this shouldn't happen.'''
            runner(COMMANDS['get_updates'])

    def update(self):
        '''Apply new updates'''
        apply_update = False

        if self.unattended:
            apply_update = True
        else:
            apply_update = prompt_yes_no(MESSAGES['question_apply_updates'])

        if apply_update:
            if self.is_root:
                if os.path.isfile(SYSTEM_CONFIG_FILE) is not True:
                    log.error('Could not find /etc/system.scm.')
                    raise FileNotFoundError(
                        MESSAGES['system_config_not_found']
                    )
                else:
                    if os.path.isfile(CHANNELS_FILE):
                        runner(COMMANDS['apply_system_updates'])
                    elif os.path.isfile(CHANNELS_FILE_LEGACY):
                        runner(COMMANDS['apply_system_updates_legacy'])
            runner(COMMANDS['apply_profile_updates'])
        else:
            if self.is_root:
                log.info(MESSAGES['help_system_updates'])
            else:
                log.info(MESSAGES['help_user_profile_updates'])

    def run(self, arguments):
        runner(arguments)

    def maintenance(self):
        self._clear_substitute_cache()
        self._run_maintenance_scripts()

    def _clear_substitute_cache(self):
        location = SUBSTITUTE_CACHE_PATH
        if self.is_root:
            try:
                os.rmdir(location)
            except:
                log.error(MESSAGES['failed_to_delete'].format(location))

    def _run_maintenance_scripts(self):
        runner(['fc-cache', '-rv'])
