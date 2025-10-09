import os, subprocess
from colorama import Fore

class NanoCommand:
    def __init__(self, base_dir, filename):
        if not filename.endswith(".m5r"):
            filename += ".m5r"
        self.path = os.path.join(base_dir, filename)

    def run(self):
        editor = os.getenv("EDITOR", "notepad")
        if not os.path.exists(self.path):
            print(Fore.YELLOW + f"Note: {self.path} does not exist, creating it.")
            open(self.path, "w").close()
        subprocess.call([editor, self.path])
