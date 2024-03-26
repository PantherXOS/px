CHANNELS_FILE = "/etc/guix/channels.scm"
# https://issues.guix.gnu.org/49610
CHANNELS_FILE_BK = "/etc/guix/channels.scm.bak"
CHANNELS_FILE_LEGACY = "/etc/channels.scm"
SYSTEM_CONFIG_FILE = "/etc/system.scm"
SUBSTITUTE_CACHE_PATH = "/var/guix/substitute/cache"

channels_switch = "--channels={}".format(CHANNELS_FILE)
channels_switch_backup = "--channels={}".format(CHANNELS_FILE_BK)
channels_switch_legacy = "--channels={}".format(CHANNELS_FILE_LEGACY)

COMMANDS = {
    "get_updates": ["guix", "pull"],
    "get_updates_overwrite": ["guix", "pull", channels_switch],
    "get_updates_overwrite_backup": ["guix", "pull", channels_switch],
    "get_updates_overwrite_legacy": ["guix", "pull", channels_switch_legacy],
    "apply_system_updates": [
        "guix",
        "time-machine",
        "-C",
        CHANNELS_FILE,
        "--",
        "system",
        "reconfigure",
        SYSTEM_CONFIG_FILE,
    ],
    "apply_system_updates_arm": [
        "guix",
        "time-machine",
        "-C",
        CHANNELS_FILE,
        "--",
        "system",
        "reconfigure",
        "--skip-checks",
        SYSTEM_CONFIG_FILE,
    ],
    "apply_system_updates_backup": [
        "guix",
        "time-machine",
        "-C",
        CHANNELS_FILE_BK,
        "--",
        "system",
        "reconfigure",
        SYSTEM_CONFIG_FILE,
    ],
    "apply_system_updates_legacy": [
        "guix",
        "time-machine",
        "-C",
        CHANNELS_FILE_LEGACY,
        "--",
        "system",
        "reconfigure",
        SYSTEM_CONFIG_FILE,
    ],
    "apply_profile_updates": ["guix", "package", "-u"],
}

COMMANDS_FLATPAK = {
    "get_version": ["flatpak", "--version"],
    "apply_updates": ["flatpak", "--user", "--assumeyes", "--noninteractive", "update"],
}
