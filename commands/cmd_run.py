import os
import re
import subprocess
import tempfile
from colorama import Fore

class RunCommand:
    def __init__(self, base_dir, filename):
        if not filename.endswith(".m5r"):
            filename += ".m5r"
        self.base_dir = base_dir
        self.path = os.path.join(base_dir, filename)

    def run(self):
        if not os.path.exists(self.path):
            print(Fore.RED + f"Error: {self.path} not found.")
            return

        source = open(self.path, encoding="utf-8").read()
        # Extract only Python segments
        py_segs = re.findall(r'<\?py(.*?)\?>', source, re.S)
        if not py_segs:
            print(Fore.YELLOW + "No Python code found in this .m5r file.")
            return

        combined = "\n".join(seg.strip() for seg in py_segs)

        # Write to a temporary .py file
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as tf:
            tf.write(combined)
            tmp_path = tf.name

        # Execute with python, in the project directory
        try:
            result = subprocess.run(
                [ "python", tmp_path ],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(Fore.RED + result.stderr, end="")
        except FileNotFoundError:
            print(Fore.RED + "Error: 'python' executable not found on PATH.")
        finally:
            os.unlink(tmp_path)
