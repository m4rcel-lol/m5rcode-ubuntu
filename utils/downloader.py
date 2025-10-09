import requests
import zipfile
import tarfile
import io
import os
import shutil
from pathlib import Path
from colorama import Fore, Style
import time
import tempfile
import json
import base64

class GitHubDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'm5rcode-shell/1.0 (GitHub Download Utility)',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.repo_owner = "m4rcel-lol"
        self.repo_name = "m5rcode"
        self.files_folder = "files"
        self.base_api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        
    def _format_size(self, bytes_size):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    
    def _print_progress_bar(self, current, total, width=40):
        """Print a styled progress bar"""
        if total <= 0:
            return
        
        percent = current / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        
        print(f"\r{Fore.CYAN}[{bar}] {percent*100:.1f}% "
              f"({self._format_size(current)}/{self._format_size(total)}){Style.RESET_ALL}", 
              end='', flush=True)
    
    def list_available_files(self):
        """List all available files in the repository's files folder"""
        try:
            print(f"{Fore.CYAN}[FETCH] Loading available files from m5rcode repository...{Style.RESET_ALL}")
            
            url = f"{self.base_api_url}/contents/{self.files_folder}"
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            
            contents = resp.json()
            files = []
            folders = []
            
            for item in contents:
                if item['type'] == 'file':
                    files.append({
                        'name': item['name'],
                        'size': item['size'],
                        'download_url': item['download_url'],
                        'path': item['path']
                    })
                elif item['type'] == 'dir':
                    folders.append(item['name'])
            
            # Display in a nice box format
            box_width = 70
            print(Fore.MAGENTA + "╔" + "═" * (box_width - 2) + "╗")
            title = "Available Files in m5rcode/files"
            print(Fore.MAGENTA + "║" + Fore.CYAN + Style.BRIGHT + title.center(box_width - 2) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╟" + "─" * (box_width - 2) + "╢")
            
            if folders:
                print(Fore.MAGENTA + "║" + Fore.YELLOW + " Folders:".ljust(box_width - 2) + Fore.MAGENTA + "║")
                for folder in folders:
                    folder_line = f"  📁 {folder}"
                    print(Fore.MAGENTA + "║" + Fore.BLUE + folder_line.ljust(box_width - 2) + Fore.MAGENTA + "║")
                print(Fore.MAGENTA + "╟" + "─" * (box_width - 2) + "╢")
            
            if files:
                print(Fore.MAGENTA + "║" + Fore.YELLOW + " Files:".ljust(box_width - 2) + Fore.MAGENTA + "║")
                for file_info in files:
                    size_str = self._format_size(file_info['size'])
                    file_line = f"  📄 {file_info['name']} ({size_str})"
                    if len(file_line) > box_width - 3:
                        file_line = file_line[:box_width-6] + "..."
                    print(Fore.MAGENTA + "║" + Fore.LIGHTWHITE_EX + file_line.ljust(box_width - 2) + Fore.MAGENTA + "║")
            
            print(Fore.MAGENTA + "╚" + "═" * (box_width - 2) + "╝" + Style.RESET_ALL)
            print(f"{Fore.GREEN}[SUCCESS] Found {len(files)} files and {len(folders)} folders{Style.RESET_ALL}")
            
            return {'files': files, 'folders': folders}
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"{Fore.RED}[ERROR] Repository or folder not found{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[ERROR] HTTP {e.response.status_code}: {e.response.reason}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to fetch file list: {str(e)}{Style.RESET_ALL}")
            return None
    
    def download_file(self, filename, target_dir=".", show_progress=True):
        """Download a specific file from the repository's files folder"""
        try:
            target_dir = Path(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Get file info from GitHub API
            url = f"{self.base_api_url}/contents/{self.files_folder}/{filename}"
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            
            file_info = resp.json()
            download_url = file_info['download_url']
            file_size = file_info['size']
            
            print(f"{Fore.CYAN}[DOWNLOAD] Downloading {filename} from m5rcode repository{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}File size: {self._format_size(file_size)}{Style.RESET_ALL}")
            
            # Download the file
            start_time = time.time()
            resp = self.session.get(download_url, stream=True, timeout=30)
            resp.raise_for_status()
            
            target_path = target_dir / filename
            downloaded = 0
            
            with open(target_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if show_progress and file_size > 0:
                            self._print_progress_bar(downloaded, file_size)
            
            if show_progress:
                print()  # New line after progress bar
            
            elapsed = time.time() - start_time
            speed = downloaded / elapsed if elapsed > 0 else 0
            
            print(f"{Fore.GREEN}[SUCCESS] Downloaded {filename} ({self._format_size(downloaded)}) "
                  f"in {elapsed:.1f}s ({self._format_size(speed)}/s){Style.RESET_ALL}")
            
            return target_path
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"{Fore.RED}[ERROR] File '{filename}' not found in repository{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[ERROR] HTTP {e.response.status_code}: {e.response.reason}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Download failed: {str(e)}{Style.RESET_ALL}")
            return None
    
    def download_folder(self, folder_name, target_dir=".", recursive=True):
        """Download all files from a specific folder in the repository"""
        try:
            target_dir = Path(target_dir) / folder_name
            target_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"{Fore.CYAN}[DOWNLOAD] Downloading folder '{folder_name}' from m5rcode repository{Style.RESET_ALL}")
            
            # Get folder contents
            url = f"{self.base_api_url}/contents/{self.files_folder}/{folder_name}"
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            
            contents = resp.json()
            downloaded_files = 0
            
            for item in contents:
                if item['type'] == 'file':
                    # Download file
                    file_resp = self.session.get(item['download_url'], timeout=30)
                    file_resp.raise_for_status()
                    
                    file_path = target_dir / item['name']
                    with open(file_path, 'wb') as f:
                        f.write(file_resp.content)
                    
                    downloaded_files += 1
                    print(f"{Fore.GREEN}[SUCCESS] Downloaded {item['name']} ({self._format_size(item['size'])}){Style.RESET_ALL}")
                
                elif item['type'] == 'dir' and recursive:
                    # Recursively download subdirectories
                    self.download_folder(f"{folder_name}/{item['name']}", Path(target_dir).parent, recursive)
            
            print(f"{Fore.GREEN}[SUCCESS] Downloaded {downloaded_files} files from folder '{folder_name}'{Style.RESET_ALL}")
            return True
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"{Fore.RED}[ERROR] Folder '{folder_name}' not found in repository{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[ERROR] HTTP {e.response.status_code}: {e.response.reason}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Folder download failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    def download_all_files(self, target_dir="m5rcode_files"):
        """Download all files from the repository's files folder"""
        try:
            target_dir = Path(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"{Fore.CYAN}[DOWNLOAD] Downloading all files from m5rcode repository{Style.RESET_ALL}")
            
            # Get all contents
            file_list = self.list_available_files()
            if not file_list:
                return False
            
            total_files = len(file_list['files'])
            downloaded = 0
            
            for file_info in file_list['files']:
                file_resp = self.session.get(file_info['download_url'], timeout=30)
                file_resp.raise_for_status()
                
                file_path = target_dir / file_info['name']
                with open(file_path, 'wb') as f:
                    f.write(file_resp.content)
                
                downloaded += 1
                print(f"{Fore.GREEN}[{downloaded}/{total_files}] Downloaded {file_info['name']} ({self._format_size(file_info['size'])}){Style.RESET_ALL}")
            
            # Download folders
            for folder_name in file_list['folders']:
                self.download_folder(folder_name, target_dir, recursive=True)
            
            print(f"{Fore.GREEN}[SUCCESS] Downloaded all {total_files} files and {len(file_list['folders'])} folders{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Bulk download failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    def search_files(self, pattern):
        """Search for files matching a pattern in the repository"""
        try:
            file_list = self.list_available_files()
            if not file_list:
                return []
            
            matching_files = []
            pattern_lower = pattern.lower()
            
            for file_info in file_list['files']:
                if pattern_lower in file_info['name'].lower():
                    matching_files.append(file_info)
            
            if matching_files:
                print(f"{Fore.GREEN}[SEARCH] Found {len(matching_files)} files matching '{pattern}'{Style.RESET_ALL}")
                for file_info in matching_files:
                    print(f"  📄 {file_info['name']} ({self._format_size(file_info['size'])})")
            else:
                print(f"{Fore.YELLOW}[SEARCH] No files found matching '{pattern}'{Style.RESET_ALL}")
            
            return matching_files
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Search failed: {str(e)}{Style.RESET_ALL}")
            return []

# Legacy and enhanced functions for easy use
def download_and_extract(url, target_dir):
    """Legacy function - use GitHubDownloader class for new code"""
    from .downloads import DownloadUtil
    util = DownloadUtil()
    return util.download_and_extract(url, target_dir)

def download_from_m5rcode(filename_or_pattern, target_dir="."):
    """Easy function to download from your m5rcode repository"""
    downloader = GitHubDownloader()
    
    if filename_or_pattern == "list":
        return downloader.list_available_files()
    elif filename_or_pattern == "all":
        return downloader.download_all_files(target_dir)
    elif "*" in filename_or_pattern or "?" in filename_or_pattern:
        # Simple pattern matching
        matches = downloader.search_files(filename_or_pattern.replace("*", ""))
        if matches:
            for match in matches:
                downloader.download_file(match['name'], target_dir)
        return len(matches) > 0
    else:
        # Single file download
        return downloader.download_file(filename_or_pattern, target_dir) is not None

# Example usage
if __name__ == "__main__":
    downloader = GitHubDownloader()
    
    # List all available files
    # downloader.list_available_files()
    
    # Download a specific file
    # downloader.download_file("example.m5r", "downloads/")
    
    # Download all files
    # downloader.download_all_files("my_m5rcode_files/")
    
    # Search for files
    # downloader.search_files("test")
