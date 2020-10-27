import sys
import os
import subprocess

from .util import prompt_yes_no, get_user_name
from .log import Logger


log = Logger(__name__)


def main():
  argument_count = len(sys.argv)

  for x in range(0, argument_count):
      print(sys.argv[x])

  if argument_count < 1:
    log.error('There is nothing to do here ...')
    sys.exit(0)

  if sys.argv[1] == "update":
    unattended = False
    username = get_user_name()
    
    if argument_count > 2:
      if sys.argv[2] == "apply":
        unattended = True

    if username == 'root':
      log.info("This will update your system (excluding user specific applications).")
    else:
      log.info("This will update your user specific applications.")

    subprocess.run(['guix', 'pull', '--disable-authentication'])
    result = False
    if unattended == True:
      result = True
    else:
      result = prompt_yes_no('Would you like to apply all pending updates?')
    if result == True:
      if username == 'root':
        if os.path.isfile('/etc/system.scm') is not True:
          log.error('Could not find /etc/system.scm')
        subprocess.run(['guix', 'system', 'reconfigure', '/etc/system.scm'])
      else:
        subprocess.run(['guix', 'package', '-u'])
    else:
      if username == 'root':
        log.info("To apply all pending updates manually, run: px system reconfigure /etc/system.scm")
      else:
        log.info("To apply all pending updates manually, run: px package -u")  
      sys.exit(0)
        
  else:
    arguments = []
    arguments.append('guix')

    for x in range(1, argument_count):
      arguments.append(sys.argv[x])

    subprocess.run(arguments)

if __name__ == '__main__':
    main()