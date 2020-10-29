import os
import pwd


def prompt_yes_no(question):
  while "the answer is invalid":
      reply = str(input(question+' (y/n): ')).lower().strip()
      if reply[:1] == 'y':
          return True
      if reply[:1] == 'n':
          return False


def get_user():
  username = pwd.getpwuid( os.getuid() )[ 0 ]
  is_root = False

  if username == 'root':
    is_root = True

  return username, is_root