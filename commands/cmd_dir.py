import os
from colorama import Fore, Style
import re

def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class DirCommand:
    def __init__(self, cwd, target):
        self.cwd = cwd
        self.target = target if target else cwd

    def run(self):
        path = os.path.abspath(os.path.join(self.cwd, self.target))
        box_min = 60

        if not os.path.exists(path):
            # Error box
            width = max(box_min, len(f"No such file or directory: {self.target}") + 10)
            print(Fore.RED + "╔" + "═" * (width - 2) + "╗")
            error_msg = f"No such file or directory: {self.target}"
            print(Fore.RED + "║" + error_msg.center(width - 2) + "║")
            print(Fore.RED + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)
            return

        if os.path.isfile(path):
            # Single file info box
            file_size = os.path.getsize(path)
            if file_size > 1024*1024:
                size_str = f"{file_size/(1024*1024):.1f} MB"
            elif file_size > 1024:
                size_str = f"{file_size/1024:.1f} KB"
            else:
                size_str = f"{file_size} B"
            
            width = max(box_min, len(self.target) + 20)
            print(Fore.MAGENTA + "╔" + "═" * (width - 2) + "╗")
            title = "File Information"
            print(Fore.MAGENTA + "║" + Fore.CYAN + Style.BRIGHT + title.center(width - 2) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")
            
            name_line = f"Name: {Fore.LIGHTWHITE_EX}{self.target}{Style.RESET_ALL}"
            size_line = f"Size: {Fore.LIGHTWHITE_EX}{size_str}{Style.RESET_ALL}"
            type_line = f"Type: {Fore.LIGHTWHITE_EX}File{Style.RESET_ALL}"
            
            for line in [name_line, size_line, type_line]:
                pad = " " * (width - 2 - len(strip_ansi(line)))
                print(Fore.MAGENTA + "║" + line + pad + Fore.MAGENTA + "║")
            
            print(Fore.MAGENTA + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)
            return

        # Directory listing
        try:
            items = os.listdir(path)
            if not items:
                # Empty directory
                width = box_min
                print(Fore.MAGENTA + "╔" + "═" * (width - 2) + "╗")
                title = f"Directory: {os.path.basename(path) or 'Root'}"
                print(Fore.MAGENTA + "║" + Fore.CYAN + Style.BRIGHT + title.center(width - 2) + Fore.MAGENTA + "║")
                print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")
                empty_msg = "Directory is empty"
                print(Fore.MAGENTA + "║" + Fore.YELLOW + empty_msg.center(width - 2) + Fore.MAGENTA + "║")
                print(Fore.MAGENTA + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)
                return

            # Calculate columns for nice layout
            name_col = 35
            type_col = 12
            size_col = 15
            total_width = name_col + type_col + size_col + 6  # spaces + borders
            width = max(box_min, total_width)

            # Separate files and directories
            dirs = []
            files = []
            for item in sorted(items):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    dirs.append(item)
                else:
                    try:
                        size = os.path.getsize(full_path)
                        if size > 1024*1024:
                            size_str = f"{size/(1024*1024):.1f} MB"
                        elif size > 1024:
                            size_str = f"{size/1024:.1f} KB"
                        else:
                            size_str = f"{size} B"
                    except:
                        size_str = "Unknown"
                    files.append((item, size_str))

            # Header
            print(Fore.MAGENTA + "╔" + "═" * (width - 2) + "╗")
            title = f"Directory: {os.path.basename(path) or 'Root'}"
            print(Fore.MAGENTA + "║" + Fore.CYAN + Style.BRIGHT + title.center(width - 2) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")

            # Column headers
            header = (
                Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
                f"{'Name':<{name_col}} {'Type':<{type_col}} {'Size':<{size_col}}" +
                Style.RESET_ALL
            )
            pad = " " * (width - 2 - len(strip_ansi(header)))
            print(Fore.MAGENTA + "║" + header + pad + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")

            # List directories first
            for dirname in dirs:
                name = (dirname[:name_col-2] + "..") if len(dirname) > name_col-1 else dirname
                name_colored = f"{Fore.BLUE + Style.BRIGHT}{name:<{name_col}}{Style.RESET_ALL}"
                type_colored = f"{Fore.LIGHTCYAN_EX}Directory{Style.RESET_ALL}"
                size_colored = f"{Style.DIM}-{Style.RESET_ALL}"
                
                row = f"{name_colored} {type_colored:<{type_col}} {size_colored:<{size_col}}"
                pad = " " * (width - 2 - len(strip_ansi(row)))
                print(Fore.MAGENTA + "║" + row + pad + Fore.MAGENTA + "║")

            # List files
            for filename, file_size in files:
                name = (filename[:name_col-2] + "..") if len(filename) > name_col-1 else filename
                name_colored = f"{Fore.LIGHTWHITE_EX}{name:<{name_col}}{Style.RESET_ALL}"
                
                # File type based on extension
                if '.' in filename:
                    ext = filename.split('.')[-1].lower()
                    if ext in ['txt', 'md', 'log']:
                        type_color = Fore.GREEN
                    elif ext in ['py', 'js', 'html', 'css', 'php']:
                        type_color = Fore.YELLOW
                    elif ext in ['jpg', 'png', 'gif', 'bmp']:
                        type_color = Fore.MAGENTA
                    elif ext in ['mp3', 'wav', 'mp4', 'avi']:
                        type_color = Fore.CYAN
                    else:
                        type_color = Fore.WHITE
                    file_type = f".{ext} file"
                else:
                    type_color = Fore.WHITE
                    file_type = "File"
                
                type_colored = f"{type_color}{file_type:<{type_col}}{Style.RESET_ALL}"
                size_colored = f"{Style.DIM}{Fore.LIGHTWHITE_EX}{file_size:<{size_col}}{Style.RESET_ALL}"
                
                row = f"{name_colored} {type_colored} {size_colored}"
                pad = " " * (width - 2 - len(strip_ansi(row)))
                print(Fore.MAGENTA + "║" + row + pad + Fore.MAGENTA + "║")

            # Footer with count
            print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")
            count_msg = f"{len(dirs)} directories, {len(files)} files"
            print(Fore.MAGENTA + "║" + Fore.LIGHTBLACK_EX + Style.DIM + count_msg.center(width - 2) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)

        except PermissionError:
            width = box_min
            print(Fore.RED + "╔" + "═" * (width - 2) + "╗")
            error_msg = "Access denied"
            print(Fore.RED + "║" + error_msg.center(width - 2) + "║")
            print(Fore.RED + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)
