import platform
import re
import datetime
from pathlib import Path
from colorama import Fore, Style
from pyfiglet import Figlet

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False

def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class FastfetchCommand:
    def _get_uptime(self):
        if not _PSUTIL_AVAILABLE:
            return "N/A (psutil not installed)"
        try:
            boot_time_timestamp = psutil.boot_time()
            boot_datetime = datetime.datetime.fromtimestamp(boot_time_timestamp)
            current_datetime = datetime.datetime.now()
            uptime_seconds = (current_datetime - boot_datetime).total_seconds()

            days = int(uptime_seconds // (24 * 3600))
            uptime_seconds %= (24 * 3600)
            hours = int(uptime_seconds // 3600)
            uptime_seconds %= 3600
            minutes = int(uptime_seconds // 60)
            seconds = int(uptime_seconds % 60)

            uptime_str = []
            if days > 0:
                uptime_str.append(f"{days}d")
            if hours > 0:
                uptime_str.append(f"{hours}h")
            if minutes > 0:
                uptime_str.append(f"{minutes}m")
            if seconds > 0 or not uptime_str:
                uptime_str.append(f"{seconds}s")
            return " ".join(uptime_str)
        except Exception:
            return "Error calculating uptime"

    def run(self):
        m5rcode_version = "1.0.0"
        try:
            version_file = Path(__file__).parents[1] / "version.txt"
            if version_file.exists():
                m5rcode_version = version_file.read_text().strip()
        except Exception:
            pass

        # ASCII "M" logo—27 chars wide
        ascii_m = [
            "           _____           ",
            "          /\\   \\          ",
            "         /::\\____\\         ",
            "        /::::|   |         ",
            "       /:::::|   |         ",
            "      /::::::|   |         ",
            "     /:::/|::|   |         ",
            "    /:::/ |::|   |         ",
            "   /:::/  |::|___|______   ",
            "  /:::/   |::::::::\\   \\  ",
            " /:::/    |:::::::::\\____\\",
            " \\::/    / ~~~~~/:::/   / ",
            "  \\/____/      /:::/   /  ",
            "              /:::/   /   ",
            "             /:::/   /    ",
            "            /:::/   /     ",
            "           /:::/   /      ",
            "          /:::/   /       ",
            "         /:::/   /        ",
            "         \\::/   /         ",
            "          \\/____/          ",
            "                           ",
        ]

        uptime_info = self._get_uptime()
        LABEL_PAD = 17

        info_lines = [
            f"{Fore.CYAN}{'m5rcode Version:':<{LABEL_PAD}}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{m5rcode_version}{Style.RESET_ALL}",
            f"{Fore.CYAN}{'Python Version:':<{LABEL_PAD}}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{platform.python_version()}{Style.RESET_ALL}",
            f"{Fore.CYAN}{'Platform:':<{LABEL_PAD}}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{platform.system()} {platform.release()}{Style.RESET_ALL}",
            f"{Fore.CYAN}{'Machine:':<{LABEL_PAD}}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{platform.machine()}{Style.RESET_ALL}",
            f"{Fore.CYAN}{'Processor:':<{LABEL_PAD}}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{platform.processor()}{Style.RESET_ALL}",
            f"{Fore.CYAN}{'Uptime:':<{LABEL_PAD}}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{uptime_info}{Style.RESET_ALL}",
        ]

        ascii_width = len(strip_ansi(ascii_m[0]))
        content_width = max(len(strip_ansi(line)) for line in info_lines)
        sep = "   "
        sep_width = len(sep)
        total_content_width = ascii_width + sep_width + content_width
        box_width = max(total_content_width, 48) + 2

        # Pad info lines vertically to align with "M"
        n_ascii = len(ascii_m)
        n_info = len(info_lines)
        info_lines_padded = [""] * ((n_ascii - n_info)//2) + info_lines + [""] * (n_ascii - n_info - (n_ascii - n_info)//2)
        if len(info_lines_padded) < n_ascii:
            info_lines_padded += [""] * (n_ascii - len(info_lines_padded))

        # Header
        print(Fore.MAGENTA + "╔" + "═" * (box_width-2) + "╗")

        title = f"m5rcode Fastfetch"
        print(Fore.MAGENTA + "║" + Fore.CYAN + title.center(box_width-2) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╟" + "─" * (box_width-2) + "╢")

        # Body
        for mline, iline in zip(ascii_m, info_lines_padded):
            line_content = (mline + sep + iline).rstrip()
            pad = " " * (box_width - 2 - len(strip_ansi(line_content)))
            print(Fore.MAGENTA + "║" + line_content + pad + Fore.MAGENTA + "║")

        print(Fore.MAGENTA + "╚" + "═" * (box_width-2) + "╝" + Style.RESET_ALL)
