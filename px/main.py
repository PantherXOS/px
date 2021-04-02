import sys
import os
import logging

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
    unattended = False
    
    if argument_count > 2:
      if sys.argv[2] == "apply":
        unattended = True

    guix = Guix(unattended)
    guix.update_check()
    guix.update()

    flatpak = Flatpak(unattended)
    flatpak.update()
        
  else:
    arguments = []
    arguments.append('guix')

    for x in range(1, argument_count):
      arguments.append(sys.argv[x])

    guix = Guix()
    guix.run(arguments)


if __name__ == '__main__':
    main()