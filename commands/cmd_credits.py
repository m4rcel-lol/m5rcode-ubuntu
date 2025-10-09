from colorama import Fore, Style
from pyfiglet import Figlet

def strip_ansi(text):
    import re
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class CreditsCommand:
    def run(self):
        box_width = 70
        inner_width = box_width - 2
        fig = Figlet(font='slant')
        credits = [
            (f"{Style.BRIGHT}{Fore.CYAN}m5rcel{Style.RESET_ALL}", "Lead Developer"),
            (f"{Style.BRIGHT}{Fore.YELLOW}pythonjs.cfd{Style.RESET_ALL}", "Project Hosting & Deployment"),
            (f"{Style.BRIGHT}{Fore.MAGENTA}colorama{Style.RESET_ALL}", "Used for terminal styling"),
            (f"{Style.BRIGHT}{Fore.GREEN}fastfetch inspired{Style.RESET_ALL}", "Design influence"),
            (f"{Style.BRIGHT}{Fore.RED}openai.com{Style.RESET_ALL}", "Some smart AI help ;)"),
        ]

        # Top border
        print(Fore.MAGENTA + "╔" + "═" * inner_width + "╗")

        # Figlet "CREDITS" title, trimmed/padded and centered vertically
        credits_title_lines = fig.renderText("CREDITS").splitlines()
        for line in credits_title_lines:
            if line.strip() == '': continue
            raw = line[:inner_width]
            pad = (inner_width - len(strip_ansi(raw))) // 2
            out = " " * pad + raw
            out = out[:inner_width]
            out = out + " " * (inner_width - len(strip_ansi(out)))
            print(Fore.MAGENTA + "║" + Fore.LIGHTMAGENTA_EX + out + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╟" + "─" * inner_width + "╢")

        # Content, each line padded to match box width
        for name, role in credits:
            left = f"{name:<25}"
            dash = f"{Fore.CYAN}━{Style.RESET_ALL}"
            right = f"{Fore.LIGHTWHITE_EX}{role}{Style.RESET_ALL}"
            raw_text = f"{left} {dash} {right}"
            raw_len = len(strip_ansi(raw_text))
            line = raw_text + " " * (inner_width - raw_len)
            print(Fore.MAGENTA + "║" + line + Fore.MAGENTA + "║")

        # Bottom border
        print(Fore.MAGENTA + "╚" + "═" * inner_width + "╝" + Style.RESET_ALL)
