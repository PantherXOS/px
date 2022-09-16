MESSAGES = {
    'check_system_updates': '=> Checking for system updates ...',
    'check_user_updates': "=> Checking for user application updates ...",
    'channels_found': 'Found global channels file at /etc/guix/channels.scm, defaulting to that.',
    'channels_found_legacy': 'Found global channels file at /etc/channels.scm, defaulting to that.',
    'system_config_not_found': "Could not find /etc/system.scm",
    'question_apply_updates': 'Would you like to apply all pending updates?',
    'help_system_updates': 'To apply all pending updates manually, run: px system reconfigure /etc/system.scm',
    'help_user_profile_updates': "To apply all pending updates manually, run: px package -u",
    'failed_to_delete': "Failed to delete {} at {}"
}

MESSAGES_FLATPAK = {
    'flatpak_found': 'Found Flatpak installation.',
    'question_apply_updates': 'Would you like to apply all pending Flatpak updates?'
}


def help_block():
    print("### Configuration changes")
    print("  To apply system configuration changes (/etc/system.scm) run `px reconfigure` as `root` user.")
    print("")
    print("### Updates")
    print("  To update run `px update`. To skip all prompts, run `px update apply`")
    print("     as `user`: Update all packages you have installed as a user, to your user profile.")
    print("     as `root`: Update the operating system and all global packages.")
    print("")
    print("  Issues with fonts or icons after updates? Run `px maintenance`")
    print("")
    print("### Packages")
    print("  To search, install or remove packages:")
    print("     search: 'px package -s ...'")
    print("     install: 'px package -i ...'")
    print("     remove: 'px package -r ...'")
    print("")
    print(
        "     Manually installed packages become part of the current user's user profile."
    )
    print(
        "     Each user may have their own selection of packages, at different versions."
    )
    print("")
    print("     To print all packages in the current user profile run `px package -I` or `guix package -I`")
    print("")
    print("### Services")
    print("  To search services: 'px system search ...'")
    print("")
    print("")
    print("Refer to 'px --help' or the guix manual for all commands and features")
