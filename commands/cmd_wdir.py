import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style
import re

def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class WdirCommand:
    def __init__(self, url):
        self.url = url.strip()

    def run(self):
        box_min = 72
        if not self.url:
            print(Fore.RED + "Usage: wdir <url>" + Style.RESET_ALL)
            return

        # Ensure scheme
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = "http://" + self.url

        try:
            print(Fore.CYAN + f"[FETCH] Scanning directory at {self.url}..." + Style.RESET_ALL)
            resp = requests.get(self.url, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print(Fore.RED + f"[ERR] Failed to fetch {self.url}: {e}" + Style.RESET_ALL)
            return

        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.find_all("a")

        files = []
        for link in links:
            href = link.get("href")
            if not href:
                continue
            if href.startswith("?") or href.startswith("#") or href.startswith("../"):
                continue
            is_dir = href.endswith("/")
            filename = href.rstrip("/").split("/")[-1]
            if not is_dir and re.search(r"\.(php|html?|asp|aspx|jsp)$", filename, re.I):
                continue
            if is_dir:
                ftype = "Directory"
            elif "." in filename:
                ftype = f".{filename.split('.')[-1]} file"
            else:
                ftype = "File"
            row_text = link.parent.get_text(" ", strip=True)
            size_match = re.search(r"(\d+(?:\.\d+)?\s*(?:KB|MB|GB|B))", row_text, re.I)
            date_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", row_text)
            size = size_match.group(1) if size_match else "-"
            modified = date_match.group(1) if date_match else "-"
            files.append((filename, ftype, size, modified))

        # Calculate column widths for nice boxed output
        col_names = ["Name", "Type", "Size", "Modified"]
        pad = [30, 15, 12, 20]
        table_width = sum(pad) + len(pad) + 1  # columns + spaces + box
        width = max(box_min, table_width + 2)

        # If no files, pretty box saying so
        if not files:
            print(Fore.MAGENTA + "╔" + "═" * (width - 2) + "╗")
            out = "No files or directories found (maybe directory listing is disabled)."
            out = out.center(width - 2)
            print(Fore.MAGENTA + "║" + Fore.YELLOW + out + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)
            return

        # Pretty header
        print(Fore.MAGENTA + "╔" + "═" * (width - 2) + "╗")
        title = "Web Directory Listing"
        print(Fore.MAGENTA + "║" + Fore.CYAN + Style.BRIGHT + title.center(width - 2) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")
        # Table header
        header = (
            Fore.LIGHTMAGENTA_EX
            + f"{col_names[0]:<{pad[0]}} {col_names[1]:<{pad[1]}} {col_names[2]:<{pad[2]}} {col_names[3]:<{pad[3]}}"
            + Style.RESET_ALL
        )
        print(
            Fore.MAGENTA + "║"
            + header
            + " " * (width - 2 - len(strip_ansi(header)))
            + Fore.MAGENTA + "║"
        )
        print(Fore.MAGENTA + "╟" + "─" * (width - 2) + "╢")

        # Table rows
        for fname, ftype, size, modified in files:
            if ftype == "Directory":
                color = Fore.BLUE + Style.BRIGHT
            elif ftype.endswith("file"):
                color = Fore.CYAN
            else:
                color = Fore.WHITE
            filecol = f"{color}{fname:<{pad[0]}}{Style.RESET_ALL}"
            typecol = f"{Style.DIM}{Fore.WHITE}{ftype:<{pad[1]}}{Style.RESET_ALL}"
            sizecol = f"{Style.DIM}{Fore.LIGHTWHITE_EX}{size:<{pad[2]}}{Style.RESET_ALL}"
            modcol = f"{Style.DIM}{Fore.LIGHTWHITE_EX}{modified:<{pad[3]}}{Style.RESET_ALL}"
            row = f"{filecol} {typecol} {sizecol} {modcol}"
            print(
                Fore.MAGENTA + "║"
                + row
                + " " * (width - 2 - len(strip_ansi(row)))
                + Fore.MAGENTA + "║"
            )
        # Footer
        print(Fore.MAGENTA + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)
