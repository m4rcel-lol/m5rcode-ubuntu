import os
from colorama import Fore

class NewCommand:
    def __init__(self, base_dir, filename):
        if not filename.endswith(".m5r"):
            filename += ".m5r"
        self.path = os.path.join(base_dir, filename)

    def run(self):
        if os.path.exists(self.path):
            print(Fore.RED + f"Error: {self.path} already exists.")
            return
        with open(self.path, "w") as f:
            f.write("// New m5r file\n")
        print(Fore.GREEN + f"Created: {self.path}")
