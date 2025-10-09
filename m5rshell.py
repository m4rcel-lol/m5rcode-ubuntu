import os
import cmd
import time
import random
import sys
import math
import re

from colorama import init, Fore, Style
from pyfiglet import Figlet

from pypresence import Presence, exceptions

from commands.cmd_new import NewCommand
from commands.cmd_nano import NanoCommand
from commands.cmd_run import RunCommand
from commands.cmd_fastfetch import FastfetchCommand
from commands.cmd_credits import CreditsCommand
from commands.cmd_cd import CdCommand
from commands.cmd_exit import ExitCommand
from commands.cmd_wdir import WdirCommand

init(autoreset=True)

CLIENT_ID = '1414669512158220409'
BANNER_LENGTH = 70  

PURPLE_GRADIENT = [Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX]

def purple_gradient_text(text):
    length = len(text)
    if length == 0:
        return ""
    result = ""
    for i, c in enumerate(text):
        pos = i / max(length - 1, 1)
        idx = int(pos * (len(PURPLE_GRADIENT) - 1) + 0.5)
        result += PURPLE_GRADIENT[idx] + c
    return result + Style.RESET_ALL

def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

def center_text(text, width):
    text_len = len(strip_ansi(text))
    if text_len >= width:
        return text
    return ' ' * ((width - text_len) // 2) + text

def linux_boot_log_animation(lines=22, width=BANNER_LENGTH, term_height=32):
    messages_ok = [
        "Started Load Kernel Modules.",
        "Mounted /boot/efi.",
        "Started Network Manager.",
        "Starting Authorization Manager...",
        "Reached target Local File Systems.",
        "Starting Hostname Service...",
        "Started User Login Management.",
        "Started Secure Boot.",
        "Mounted /media.",
        "Started Virtualization Daemon.",
        "Starting m5rcode Engine...",
        "Started Manage Shell Sessions.",
        "Starting m5rcode Module Service.",
        "Started Manage System Buses.",
        "Started Command Dispatcher.",
        "Started List Directory Service.",
        "Started Python .m5r Runner.",
        "Completed Shell Finalization.",
        "Started Discord RPC Integration.",
        "Started Figlet Banner.",
        "Ready."
    ]
    blanks = (term_height - lines) // 2
    os.system('clear')
    for _ in range(blanks):
        print('')
    print(center_text(Fore.WHITE + Style.BRIGHT + "m5rOS (Unofficial) Shell Boot Sequence" + Style.RESET_ALL, width))
    for i in range(lines):
        time.sleep(0.06 if i < lines - 2 else 0.16)
        msg = messages_ok[i] if i < len(messages_ok) else "Booting" + '.' * ((i % 5) + 1)
        prefix = "[ OK ]"
        color = Fore.LIGHTBLACK_EX if i % 2 == 0 else Fore.WHITE
        print(center_text(color + prefix + ' ' + msg + Style.RESET_ALL, width))
    print(center_text(Fore.WHITE + Style.BRIGHT + "\n>>> Boot complete." + Style.RESET_ALL, width))
    time.sleep(0.5)

def print_spinning_donut(frames=36, width=74, height=28, sleep=0.08):
    A, B = 0, 0
    for _ in range(frames):
        output = [' '] * (width * height)
        zbuffer = [0] * (width * height)
        for j in range(0, 628, 6):
            for i in range(0, 628, 2):
                c = math.sin(i / 100)
                d = math.cos(j / 100)
                e = math.sin(A)
                f = math.sin(j / 100)
                g = math.cos(A)
                h = d + 2
                D = 1 / (c * h * e + f * g + 5)
                l = math.cos(i / 100)
                m = math.cos(B)
                n = math.sin(B)
                t = c * h * g - f * e
                x = int(width / 2 + width / 3 * D * (l * h * m - t * n))
                y = int(height / 2 + height / 3.5 * D * (l * h * n + t * m))
                o = int(x + width * y)
                if 0 <= y < height and 0 <= x < width and D > zbuffer[o]:
                    zbuffer[o] = D
                    lum_index = int(10 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
                    chars = ".,-~:;=!*#$@"
                    output[o] = chars[lum_index % len(chars)]
        os.system('clear')
        blanks = 3
        for _ in range(blanks):
            print('')
        print(center_text(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + "m5rcode: Initializing..." + Style.RESET_ALL, width))
        for y in range(height):
            line = ''.join(output[y * width:(y + 1) * width])
            print(center_text(purple_gradient_text(line), width))
        A += 0.08
        B += 0.03
        time.sleep(sleep)
    time.sleep(0.2)

class M5RShell(cmd.Cmd):
    intro = None

    def __init__(self):
        super().__init__()
        self.base_dir = os.path.join(os.path.expanduser("~"), "m5rcode", "files")
        os.makedirs(self.base_dir, exist_ok=True)
        self.cwd = self.base_dir
        os.chdir(self.cwd)
        self.update_prompt()
        self.rpc_active = False
        self.rpc = None
        self._connect_rpc()
        if self.rpc_active:
            self._set_idle_presence()

    def _connect_rpc(self):
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.rpc_active = True
        except exceptions.DiscordNotFound:
            print(Fore.LIGHTBLACK_EX + "[RPC] Discord not found. RPC disabled." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.LIGHTBLACK_EX + f"[RPC Error] {e}" + Style.RESET_ALL)

    def _set_idle_presence(self):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details="Using the shell",
                    state="Waiting for commands...",
                    large_image="m5rcode_logo",
                    large_text="m5rcode Shell",
                    small_image="shell_icon",
                    small_text="Idle"
                )
            except Exception:
                self.rpc_active = False

    def _set_editing_presence(self, filename):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details=f"Editing {filename}",
                    state="In editor",
                    large_image="m5rcode_logo",
                    large_text="m5rcode Shell",
                    small_image="editing_icon",
                    small_text="Editing File"
                )
            except Exception:
                self.rpc_active = False

    def _set_running_presence(self, command_name):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details=f"Running {command_name}",
                    state="Executing command",
                    large_image="m5rcode_logo",
                    large_text="m5rcode Shell",
                    small_image="running_icon",
                    small_text="Command Running"
                )
            except Exception:
                self.rpc_active = False

    def _clear_presence(self):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.clear()
            except Exception:
                self.rpc_active = False

    def _close_rpc(self):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.close()
            except Exception:
                pass
            self.rpc_active = False

    def update_prompt(self):
        user = os.getenv("USER") or os.getenv("USERNAME") or "user"
        nodename = os.uname().nodename if hasattr(os, "uname") else "host"
        self.prompt = (
            Fore.LIGHTBLUE_EX + "╭─["
            + Fore.LIGHTMAGENTA_EX + "m5rcode"
            + Fore.LIGHTBLUE_EX + "]"
            + Fore.LIGHTYELLOW_EX + f"[{user}@{nodename}]"
            + Fore.LIGHTBLUE_EX + "--["
            + Fore.LIGHTGREEN_EX + self.cwd
            + Fore.LIGHTBLUE_EX + "]\n"
            + Fore.LIGHTMAGENTA_EX + "╰─❯ "
            + Style.RESET_ALL
        )

    def preloop(self):
        linux_boot_log_animation()
        print_spinning_donut()
        os.system('clear')
        self._print_banner()
        if self.rpc_active:
            self._set_idle_presence()

    def _print_banner(self):
        blen = BANNER_LENGTH
        ascii_art = Figlet(font='slant')
        print(Fore.LIGHTBLACK_EX + "╔" + "═" * blen + "╗")
        for line in ascii_art.renderText("m5rcode").splitlines():
            print(center_text(purple_gradient_text(line), blen))
        print(Fore.LIGHTBLACK_EX + "╠" + "═" * blen + "╣")
        print(center_text(purple_gradient_text("  Welcome to the m5rcode shell!  ".center(blen)), blen))
        print(Fore.LIGHTBLACK_EX + "╚" + "═" * blen + "╝" + Style.RESET_ALL)
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT +
              "Type 'help' or '?' for commands · 'exit' to quit\n" + Style.RESET_ALL)

    def postcmd(self, stop, line):
        print(Fore.LIGHTBLACK_EX + Style.DIM +
              f"· Finished: '{line.strip() or '[empty input]'}' ·" + Style.RESET_ALL)
        if self.rpc_active:
            self._set_idle_presence()
        return stop

    def emptyline(self):
        sys.stdout.write(Fore.LIGHTBLACK_EX + "· waiting ·\n" + Style.RESET_ALL)

    def default(self, line):
        print(
            Fore.LIGHTRED_EX + Style.BRIGHT
            + "⚠ Unknown command:"
            + Fore.LIGHTYELLOW_EX + f" '{line}'" + Style.RESET_ALL
        )
        print(Fore.LIGHTMAGENTA_EX + "Type 'help' or '?' to see available commands." + Style.RESET_ALL)

    # Help command with sections and commands
    def do_help(self, arg):
        blen = BANNER_LENGTH
        inner_width = blen - 2
        def c(s): return "║" + s + "║"
        if arg:
            super().do_help(arg)
        else:
            print(Fore.LIGHTCYAN_EX + "╔" + "═" * inner_width + "╗")
            fig = Figlet(font='standard')
            for line in fig.renderText("M5R   HELP").splitlines():
                if line.strip() == "": continue
                raw = line[:inner_width]
                pad = (inner_width - len(strip_ansi(raw))) // 2
                out = " " * pad + purple_gradient_text(raw)
                out = out + " " * (inner_width - len(strip_ansi(out)))
                print(Fore.LIGHTCYAN_EX + c(out))
            print(Fore.LIGHTCYAN_EX + "╟" + "─" * inner_width + "╢" + Style.RESET_ALL)
            sections = [
                (" FILE/PROJECT ", [
                    ("new", "Create a new .m5r file"),
                    ("nano", "Edit a file with your editor"),
                    ("run", "Run a .m5r script (executes only Python blocks)")
                ]),
                (" INFORMATION ", [
                    ("fastfetch", "Show language & system info"),
                    ("credits", "Show project credits"),
                ]),
                (" NAVIGATION & UTILITY ", [
                    ("cd", "Change directory within m5rcode/files"),
                    ("dir", "List files in the current directory"),
                    ("wdir", "List files hosted at a website directory"),
                    ("clear", "Clear the shell output"),
                    ("exit", "Exit the m5rcode shell"),
                    ("help", "Display this help message"),
                    ("?", "Alias for 'help'")
                ])
            ]
            for idx, (header, cmds) in enumerate(sections):
                header_line = purple_gradient_text(header.center(inner_width))
                print(Fore.LIGHTCYAN_EX + c(header_line))
                for command, desc in cmds:
                    print(self._print_command_help(command, desc, inner_width, boxed=True))
                if idx < len(sections) - 1:
                    print(Fore.LIGHTCYAN_EX + "╟" + "─" * inner_width + "╢" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "╚" + "═" * inner_width + "╝" + Style.RESET_ALL)
            foot = Fore.LIGHTBLACK_EX + Style.DIM + "For details: " + Style.NORMAL + Fore.LIGHTCYAN_EX + "help <command>" + Style.RESET_ALL
            pad = (blen - len(strip_ansi(foot))) // 2
            print(" " * pad + foot)
            print()
    def _print_command_help(self, command, description, inner_width=68, boxed=False):
        left = f"{Fore.LIGHTGREEN_EX}{command:<10}{Style.RESET_ALL}"
        arr = f"{Fore.LIGHTCYAN_EX}→{Style.RESET_ALL}"
        desc = f"{Fore.LIGHTWHITE_EX}{description}{Style.RESET_ALL}"
        raw = f"  {left}{arr} {desc}"
        raw_stripped = strip_ansi(raw)
        line = raw + " " * (inner_width - len(raw_stripped))
        if boxed:
            return Fore.LIGHTCYAN_EX + "║" + line + "║" + Style.RESET_ALL
        else:
            return line

    # Now the actual commands calling imported command modules
    def do_clear(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_banner()
        self.update_prompt()

    def do_new(self, arg):
        if self.rpc_active:
            self._set_running_presence("new file")
        NewCommand(self.cwd, arg.strip()).run()

    def do_nano(self, arg):
        filename = arg.strip()
        if self.rpc_active:
            self._set_editing_presence(filename)
        NanoCommand(self.cwd, filename).run()

    def do_run(self, arg):
        if self.rpc_active:
            self._set_running_presence(f"script {arg.strip()}")
        RunCommand(self.cwd, arg.strip()).run()

    def do_fastfetch(self, arg):
        if self.rpc_active:
            self._set_running_presence("fastfetch")
        FastfetchCommand().run()

    def do_credits(self, arg):
        if self.rpc_active:
            self._set_running_presence("credits")
        CreditsCommand().run()

    def do_cd(self, arg):
        if self.rpc_active:
            self._set_running_presence(f"changing directory to {arg.strip()}")
        CdCommand(self.base_dir, [self], arg).run()
        os.chdir(self.cwd)
        self.update_prompt()

    def do_dir(self, arg):
        if self.rpc_active:
            self._set_running_presence("dir")
        try:
            files = os.listdir(self.cwd)
            if not files:
                print(Fore.YELLOW + "Directory is empty." + Style.RESET_ALL)
                return
            print(Fore.GREEN + "\nFiles in directory:" + Style.RESET_ALL)
            for f in files:
                path = os.path.join(self.cwd, f)
                if os.path.isdir(path):
                    print(f"  {Fore.CYAN}{f}/ {Style.RESET_ALL}")
                else:
                    print(f"  {Fore.WHITE}{f}{Style.RESET_ALL}")
        except Exception as e:
            print(Fore.RED + f"[ERR] {e}" + Style.RESET_ALL)

    def do_wdir(self, arg):
        if self.rpc_active:
            self._set_running_presence("wdir")
        WdirCommand(arg).run()

    def do_exit(self, arg):
        self._clear_presence()
        self._close_rpc()
        return ExitCommand().run()


if __name__ == "__main__":
    M5RShell().cmdloop()

