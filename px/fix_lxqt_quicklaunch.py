import os
import re
import subprocess
from typing import List
import getpass
from shutil import copyfile

username = getpass.getuser()

def parse_file_name(file_name: str) -> str:
    # /gnu/store/v8wq5xrjkb9snskls8hby37xvr3r4fhc-px-terminal-dev-0.16.0-0.2260088/share/applications/qterminal.desktop
    file_name.removeprefix('/gnu/store/')
    _, binary_desktop_file = file_name.split('/share/applications/')
    binary, desktop_file = binary_desktop_file.split('.desktop')
    hash, remaining = file_name.split('-', 1)
    result = re.compile('\-\d').split(remaining)
    name = result[0]
    return name, binary

def find_current_path(name: str):
    result = subprocess.run(f"which {name}", shell=True, capture_output=True)
    if result.stdout:
        return result.stdout.decode('utf-8').replace('\n', '')
    else:
        print(f"Could not find {name}")
        return None

def get_store_path(path: str):
    result = subprocess.run(f"ls -l {path}", shell=True, capture_output=True)
    if result.stdout:
        _, store_path = result.stdout.decode('utf-8').split('-> ')
        return store_path.replace('\n', '')


class PanelConfigLine:
    source: str
    source_file_name: str
    identifier: str

    application_name: str
    binary_name: str

    path: str
    store_path: str

    def __init__(self, source: str):
        self.source = source
        identifier, source_file_name = source.split('=')
        self.identifier = identifier
        self.source_file_name = source_file_name.replace('\n', '')
        self.application_name, self.binary_name = parse_file_name(self.source_file_name)
        self.path = find_current_path(self.binary_name)
        self.store_path = get_store_path(self.path)

    def format_result(self):
        return f"{self.identifier}={self.store_path_desktop_file()}\n"

    def print_store_path(self):
        print(self.store_path)

    def store_path_desktop_file(self):
        return self.store_path.replace(f'/bin/{self.binary_name}', '') + '/share/applications/' + self.binary_name + '.desktop'

    def has_changed(self):
        return self.source != self.format_result()

class PanelConfig:
    path: str

    lines: List[PanelConfigLine] = []

    def __init__(self, path = f'/home/{username}/.config/lxqt/panel.conf'):
        self.path = path
        supported = []

        for x in range(1, 10):
            supported.append(f"apps\\{x}\\desktop=")

        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                for s in supported:
                    if line.startswith(s):
                        result = PanelConfigLine(line)
                        if result.has_changed():
                            self.lines.append(result)

        backup_file =  self.path + '.bak'
        if not os.path.isfile(backup_file):
            copyfile(self.path, backup_file)

    def apply_changes(self, dry_run = True):
        print(f"Applying changes to {self.path} (dry run: {dry_run})")
        print()
        if len(self.lines) == 0:
            print('No changes to apply')
            return
        source_lines = open(self.path, "r").readlines()
        if not dry_run:
            with open(self.path, "w") as f:
                for source_line in source_lines:
                    match = False
                    for l in self.lines:
                        if l.source == source_line:
                            match = True
                            break

                    if match:
                        print(f"Updating \n{source_line}{l.format_result()}")
                        formatted_result = l.format_result().replace('\n', '')
                        print(f"Writing: {formatted_result}")
                        f.write(l.format_result())
                        print()
                    else:
                        f.write(source_line)

        else:
            for source_line in source_lines:
                match = False
                for l in self.lines:
                    if l.source == source_line:
                        match = True
                        break

                if match:
                    print(f"Updating \n{source_line}{l.format_result()}")
                    formatted_result = l.format_result().replace('\n', '')
                    print(f"Writing: {formatted_result} - DRY RUN")
                    print()