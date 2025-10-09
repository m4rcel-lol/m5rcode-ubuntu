import os
import requests
from utils.downloader import download_and_extract
from pathlib import Path

# URLs for raw version and zipped repo
VERSION_URL = "https://raw.githubusercontent.com/m4rcel-lol/m5rcode/main/version.txt"
REPO_ZIP_URL = "https://github.com/m4rcel-lol/m5rcode/archive/refs/heads/main.zip"

def check_and_update():
    # Figure out where your version file is
    project_root = Path(__file__).resolve().parents[2]
    local_version_file = project_root / "version.txt"

    try:
        # 1. Get remote version number (plain text!)
        remote_ver = requests.get(VERSION_URL, timeout=6).text.strip()
    except Exception as e:
        print("Could not get remote version:", e)
        return

    try:
        local_ver = local_version_file.read_text().strip()
    except Exception:
        local_ver = None

    if remote_ver != local_ver:
        print(f"Updating: {local_ver or 'unknown'} → {remote_ver}")
        # 2. Download/extract ZIP to temp location
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            download_and_extract(REPO_ZIP_URL, tmpdir)
            # Find the extracted subfolder (GitHub zips always contain one top-level folder)
            zipped_root = Path(tmpdir) / "m5rcode-main"
            if not zipped_root.exists():
                zipped_root = next(Path(tmpdir).iterdir())
            # 3. Copy updated files over (here simply overwrite existing files)
            for item in zipped_root.iterdir():
                dest = project_root / item.name
                if item.is_dir():
                    # Recursively copy dir
                    import shutil
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                else:
                    dest.write_bytes(item.read_bytes())
        # 4. Write new local version
        local_version_file.write_text(remote_ver)
        print("Update complete!")
    else:
        print("Already up to date.")
