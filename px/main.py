import logging
import sys

import pkg_resources

from .flatpak import Flatpak
from .guix import Guix
from .log import *
from .messages import help_block

log = logging.getLogger(__name__)

version = pkg_resources.require("px")[0].version


def main():
    argument_count = len(sys.argv)

    if argument_count < 2:
        log.info('PantherX System Manager v{}'.format(version))
        print("")
        help_block()
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

    elif sys.argv[1] == "reconfigure":
        guix = Guix(unattended=True)
        guix.update()

    elif sys.argv[1] == "maintenance":
        guix = Guix(unattended=True)
        guix.maintenance()

    elif sys.argv[1] == "help":
        help_block()

    else:
        arguments = []
        arguments.append('guix')

        for x in range(1, argument_count):
            arguments.append(sys.argv[x])

        guix = Guix()
        guix.run(arguments)

    if __name__ == '__main__':
        main()
