# commands/cmd_cd.py
import os
from colorama import Fore

class CdCommand:
    def __init__(self, files_dir, shell_ref, target_dir):
        # files_dir = ~/m5rcode/files
        self.files_dir   = files_dir
        self.project_root = os.path.dirname(files_dir)  # ~/m5rcode
        self.shell       = shell_ref[0]                # the M5RShell instance
        self.target      = target_dir.strip()

    def run(self):
        if not self.target or self.target == '.':
            # Stay in current directory
            return

        # Compute new absolute path
        candidate = os.path.abspath(
            os.path.normpath(
                os.path.join(self.shell.cwd, self.target)
            )
        )

        # If they typed '..' from files_dir, allow up to project_root
        if self.target == '..':
            # from files_dir → project_root
            if self.shell.cwd == self.files_dir:
                new_path = self.project_root
            # from any subfolder of files_dir → one level up, but not above project_root
            else:
                new_path = os.path.dirname(self.shell.cwd)
                if not new_path.startswith(self.project_root):
                    new_path = self.project_root
        else:
            new_path = candidate

        # Check it stays within project_root
        if not new_path.startswith(self.project_root):
            print(Fore.RED + "Access denied: You cannot leave the m5rcode project.")
            return

        if os.path.isdir(new_path):
            self.shell.cwd = new_path
        else:
            print(Fore.RED + f"No such directory: {self.target}")
