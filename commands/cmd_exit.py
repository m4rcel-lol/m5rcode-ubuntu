from colorama import Fore, Style
import time
import os
import sys

class ExitCommand:
    def shutdown_animation(self):
        # Clear screen for clean shutdown
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Shutdown sequence messages
        shutdown_msgs = [
            "Stopping Discord RPC Integration...",
            "Saving shell session...",
            "Clearing command history...",
            "Stopping background processes...",
            "Unmounting m5rcode directories...",
            "Finalizing cleanup...",
            "Thank you for using m5rcode shell!"
        ]
        
        print(Fore.LIGHTBLACK_EX + "m5rOS Shutdown Sequence" + Style.RESET_ALL)
        print(Fore.LIGHTBLACK_EX + "=" * 25 + Style.RESET_ALL)
        
        for i, msg in enumerate(shutdown_msgs):
            time.sleep(0.3)
            if i == len(shutdown_msgs) - 1:
                # Last message in cyan
                print(Fore.CYAN + Style.BRIGHT + f"[  OK  ] {msg}" + Style.RESET_ALL)
            else:
                # Regular messages in white/grey
                color = Fore.WHITE if i % 2 == 0 else Fore.LIGHTBLACK_EX
                print(color + f"[  OK  ] {msg}" + Style.RESET_ALL)
        
        time.sleep(0.5)
        
        # Animated "powering down" effect
        print()
        sys.stdout.write(Fore.LIGHTMAGENTA_EX + "Powering down")
        for _ in range(6):
            time.sleep(0.2)
            sys.stdout.write(".")
            sys.stdout.flush()
        
        print(Style.RESET_ALL)
        time.sleep(0.3)
        
        # Final goodbye box
        box_width = 50
        print(Fore.MAGENTA + "╔" + "═" * (box_width - 2) + "╗")
        
        goodbye_lines = [
            "m5rcode shell session ended",
            "",
            "Thanks for coding with us!",
            "See you next time! 👋"
        ]
        
        for line in goodbye_lines:
            if line == "":
                print(Fore.MAGENTA + "║" + " " * (box_width - 2) + "║")
            else:
                color = Fore.CYAN if "m5rcode" in line else Fore.LIGHTWHITE_EX
                centered = color + line.center(box_width - 2) + Style.RESET_ALL
                print(Fore.MAGENTA + "║" + centered + Fore.MAGENTA + "║")
        
        print(Fore.MAGENTA + "╚" + "═" * (box_width - 2) + "╝" + Style.RESET_ALL)
        time.sleep(1)

    def run(self):
        self.shutdown_animation()
        return True  # Signals to shell to exit
