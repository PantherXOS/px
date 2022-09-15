CHANNELS_FILE = '/etc/guix/channels.scm'
CHANNELS_FILE_LEGACY = '/etc/channels.scm'
SYSTEM_CONFIG_FILE = '/etc/system.scm'
SUBSTITUTE_CACHE_PATH = '/var/guix/substitute/cache'

channels_switch = '--channels={}'.format(CHANNELS_FILE)
channels_switch_legacy = '--channels={}'.format(CHANNELS_FILE_LEGACY)

# TODO: Remove --disable-authentication
COMMANDS = {
    'get_updates': ['guix', 'pull', '--disable-authentication'],
    'get_updates_overwrite': ['guix', 'pull', '--disable-authentication', channels_switch],
    'get_updates_overwrite_legacy': ['guix', 'pull', '--disable-authentication', channels_switch_legacy],
    'apply_system_updates': ['guix', 'time-machine', '-C', CHANNELS_FILE,
                             '--disable-authentication', '--', 'system', 'reconfigure', SYSTEM_CONFIG_FILE],
    'apply_system_updates_arm': ['guix', 'time-machine', '-C', CHANNELS_FILE,
                             '--disable-authentication', '--skip-checks', '--', 'system', 'reconfigure', SYSTEM_CONFIG_FILE],
    'apply_system_updates_legacy': ['guix', 'time-machine', '-C', CHANNELS_FILE_LEGACY,
                                    '--disable-authentication', '--', 'system', 'reconfigure', SYSTEM_CONFIG_FILE],
    'apply_profile_updates': ['guix', 'package', '-u']
}

COMMANDS_FLATPAK = {
    'get_version': ["flatpak", "--version"],
    'apply_updates': ['flatpak', '--user', '--assumeyes',
                      '--noninteractive', 'update']
}
