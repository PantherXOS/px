from dataclasses import dataclass
from typing import List
import glob
import os
from datetime import datetime
import subprocess
import getpass

username = getpass.getuser()

known_offending_applications = [
    'userapp-Nightly',
    'userapp-Daily'
]

class DesktopFile:
    path: str
    name: str
    exec: str
    created_at: float

    application_name: str

    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.created_at = os.path.getctime(path)
        self.read_file()
        
    def read_file(self):
        source = open(self.path, 'r')
        lines = source.readlines()
        source.close()

        for line in lines:
            if line.__contains__('Exec'):
                self.exec = line.split('=')[1]
            if line.__contains__('Name'):
                self.application_name = line.split('=')[1].replace('\n', '')

    def is_valid(self):
        is_known_offender = False
        for application in known_offending_applications:
            if hasattr(self, 'name') and self.name.startswith(application):
                is_known_offender = True

        return hasattr(self, 'exec') and hasattr(self, 'application_name') and is_known_offender


@dataclass
class DesktopFileOperationResult:
    application_name: str

    deleted_files: List[DesktopFile]
    kept_files: List[DesktopFile]

    def __init__(self, application_name: str):
        self.application_name = application_name
        self.deleted_files = []
        self.kept_files = []

    def add_deleted(self, file: DesktopFile):
        self.deleted_files.append(file)

    def add_kept(self, file: DesktopFile):
        self.kept_files.append(file)


class DesktopFiles:
    files: List[DesktopFile] = []

    def __init__(self, path = f"/home/{username}/.local/share/applications/*.desktop"):
        desktop_files = glob.glob(path)
        for desktop_file in desktop_files:
            file = DesktopFile(desktop_file)
            if file.is_valid():
                self.files.append(file)
        self.sort()

    def print_list(self):
        '''Lists all files (human readable)'''
        for file in self.files:
            if file.is_valid():
                print(f"{file.name} - {file.application_name} - {datetime.fromtimestamp(file.created_at).strftime('%Y-%m-%d %H:%M:%S')}")

    def sort(self):
        '''Sorts the files by created_at and application_name'''
        self.files.sort(key=lambda x: x.application_name)
        self.files.sort(key=lambda x: x.created_at, reverse=True)

    def files_by_application_name(self, application_name: str):
        '''Returns a list of files by application name'''
        return [file for file in self.files if file.application_name == application_name]

    def unique_application_names(self):
        '''Returns a list of unique application names'''
        return list(set([file.application_name for file in self.files]))

    def delete_duplicate_older_files_by_unique_application_names(self, dry_run: bool = True):
        '''Deletes all duplicate files by application name and keeps the newest one'''
        print(f'''
=> Deleting duplicate files from /home/{username}/.local/share/applications
''')
        results: List[DesktopFileOperationResult] = []
        for application in self.unique_application_names():
            files = self.files_by_application_name(application)
            print(f"{application} - {len(files)}")
            if len(files) > 1:
                result = DesktopFileOperationResult(application)

                for i in range(len(files)):
                    if i > 0:
                        result.add_deleted(files[i])
                        if not dry_run:
                            print(f"   - Deleting {files[i].name} - {datetime.fromtimestamp(files[i].created_at).strftime('%Y-%m-%d %H:%M:%S')}")
                            os.remove(files[i].path)
                        else:
                            print(f"   - Deleting {files[i].name} - {datetime.fromtimestamp(files[i].created_at).strftime('%Y-%m-%d %H:%M:%S')} - DRY RUN")
                    else:
                        result.add_kept(files[i])
                        print(f"   + Keeping  {files[i].name} - {datetime.fromtimestamp(files[i].created_at).strftime('%Y-%m-%d %H:%M:%S')}")

                results.append(result)

        return results

class MimeAppsLine:
    source: str
    mime_type: str
    application: str
    # somestimes a mime type has multiple applications
    all_applications: List[str]

    def __init__(self, line: str):
        self.source = line
        mime_type, application = line.split('=')
        self.mime_type = mime_type
        self._parse_application(application)

    def _parse_application(self, application: str):
        apps = application.replace('\n', '')
        if apps.__contains__(';') and apps.endswith(';'):
            self.all_applications = apps.removesuffix(';').split(';')
            self.application = self.all_applications[0]

    def is_valid(self):
        known_offender = False 
        for application in known_offending_applications:
            if hasattr(self, 'application') and self.application.startswith(application):
                known_offender = True
        return hasattr(self, 'mime_type') and hasattr(self, 'application') and known_offender

    def print_line(self):
        print(f"{self.mime_type} = {self.application}")
        if len(self.all_applications) > 1:
            for application in self.all_applications:
                print(f"   - {application}")

    def update_xdg_mime(self, application: str):
        subprocess.run(['xdg-mime', 'default', application, self.mime_type], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class MimeApps:
    lines: List[MimeAppsLine] = []

    def __init__(self, path = f'/home/{username}/.config/mimeapps.list'):
        self.path = path
        source = open(path, 'r')
        source_lines = source.readlines()
        source.close()

        for line in source_lines:
            if line.__contains__('='):
                line = MimeAppsLine(line)
                if line.is_valid():
                    self.lines.append(line)

    def print_list(self):
        for line in self.lines:
            line.print_line()

    def apply_desktop_files_operation_result(self, result: DesktopFileOperationResult, dry_run: bool = True):
        all_files = result.deleted_files + result.kept_files

        # loop over all mimeapp lines and match those with the same name as the desktop file
        for line in self.lines:
            match = False
            # loop over all line applications
            for application in line.all_applications:
                for file in all_files:
                    # if any of the applications match the desktop file name, we have a match
                    if file.name == application:
                        match = True
                        break
                if match:
                    break

            if match:
                if line.application == result.kept_files[0].name:
                    print(f"   + Keeping:   {line.application} - {line.mime_type}")
                else:
                    if not dry_run:
                        print(f"   - Replacing: {line.application} -> {result.kept_files[0].name} - {line.mime_type}")
                        line.update_xdg_mime(result.kept_files[0].name)
                    else:
                        print(f"   - Replacing: {line.application} -> {result.kept_files[0].name} - {line.mime_type} - DRY RUN")

    def apply_desktop_files_operation_results(self, results: List[DesktopFileOperationResult], dry_run: bool = True):
        print('''
=> Applying desktop file operation results to mimeapps.list
''')
        for result in results:
            self.apply_desktop_files_operation_result(result, dry_run)