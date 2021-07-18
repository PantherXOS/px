CHANNELS_FILE = '/etc/channels.scm'
SYSTEM_CONFIG_FILE = '/etc/system.scm'
SUBSTITUTE_CACHE_PATH = '/var/guix/substitute/cache'

# TODO: Remove --disable-authentication
COMMANDS = {
    'get_updates': ['guix', 'pull', '--disable-authentication'],
    'get_updates_overwrite': ['guix', 'pull', '--disable-authentication', '--channels=/etc/channels.scm'],
    'apply_system_updates': ['guix', 'time-machine', '-C', CHANNELS_FILE,
                             '--disable-authentication', '--', 'system', 'reconfigure', SYSTEM_CONFIG_FILE],
    'apply_profile_updates': ['guix', 'package', '-u']
}

COMMANDS_FLATPAK = {
    'get_version': ["flatpak", "--version"],
    'apply_updates': ['flatpak', '--user', '--assumeyes',
                      '--noninteractive', 'update']
}
