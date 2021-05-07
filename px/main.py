import logging
import sys

from .flatpak import Flatpak
from .guix import Guix
from .log import *

log = logging.getLogger(__name__)


def main():
    argument_count = len(sys.argv)

    if argument_count < 2:
        log.error('There is nothing to do here.')
        sys.exit(0)

    if sys.argv[1] == "update":
        '''Run application or system update'''
        unattended = False

        if argument_count > 2:
            '''If True, skips all user prompts'''
            if sys.argv[2] == "apply":
                unattended = True

        guix = Guix(unattended)
        guix.update_check()
        guix.update()

        flatpak = Flatpak(unattended)
        flatpak.update()

    elif sys.argv[1] == "maintenance":
        guix = Guix(unattended=True)
        guix.maintenance()

    elif sys.argv[1] == "help":
        print("# Updates")
        print("  To update run `px update`. To skip all prompts, run `px update apply`")
        print("     as `user`: Update all packages you have installed as a user, to your user profile.")
        print("     as `root`: Update the operating system and all global packages.")
        print("")
        print("  Issues with fonts or icons after updates? Run `px maintenance`")
        print("")
        print("# Packages")
        print("  To search, install or remove packages:")
        print("     search: 'px package -s ...'")
        print("     install: 'px package -i ...'")
        print("     remove: 'px package -r ...'")
        print("")
        print("     Manually installed packages become part of the current user's user profile.")
        print("     Each user may have their own selection of packages, at different versions.")
        print("")
        print("     To print all packages in the current user profile run `px package -I` or `guix package -I`")
        print("")
        print("Refer to 'px --help' or the guix manual for all commands and features")

    else:
        arguments = []
        arguments.append('guix')

        for x in range(1, argument_count):
            print(sys.argv[x])
            arguments.append(sys.argv[x])

        print(arguments)

        guix = Guix()
        guix.run(arguments)

    if __name__ == '__main__':
        main()
