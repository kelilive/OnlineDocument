import os
import shutil
import subprocess
from pathlib import Path

def remove_recent_items():
    print("Removing Recent Items")
    recent = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Recent"
    if recent.exists():
        for f in recent.glob("*"):
            try:
                f.unlink()
            except:
                pass
    print("Recent Items cleaned")

def clear_thumbnail_cache():
    print("Clearing Thumbnail Cache")
    explorer = Path(os.getenv("LOCALAPPDATA")) / "Microsoft/Windows/Explorer"
    if explorer.exists():
        for f in explorer.glob("thumbcache_*"):
            try:
                f.unlink()
            except:
                pass
    print("Thumbnail Cache cleared")

def clear_run_history():
    print("Clearing Run Dialog History")
    subprocess.run([
        "reg", "delete",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU",
        "/f"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Run Dialog History cleared")

def clear_typed_paths():
    print("Clearing Explorer Address Bar History")
    subprocess.run([
        "reg", "delete",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths",
        "/f"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Address Bar History cleared")

def clear_start_menu_recent():
    print("Clearing Start Menu Recent Apps")
    subprocess.run([
        "reg", "delete",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\StartPage",
        "/f"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Start Menu Recent Apps cleared")

def clear_temp_folders():
    print("Clearing Temp Folders")
    temp1 = Path(os.getenv("TEMP"))
    temp2 = Path(os.getenv("WINDIR")) / "Temp"
    for folder in [temp1, temp2]:
        if folder.exists():
            for f in folder.glob("*"):
                try:
                    if f.is_file():
                        f.unlink()
                    else:
                        shutil.rmtree(f, ignore_errors=True)
                except:
                    pass
    print("Temp Folders cleared")

def clear_prefetch():
    print("Clearing Prefetch")
    prefetch = Path(os.getenv("WINDIR")) / "Prefetch"
    if prefetch.exists():
        for f in prefetch.glob("*"):
            try:
                f.unlink()
            except:
                pass
    print("Prefetch cleared")

def clear_search_history():
    print("Clearing Windows Search History")
    search = Path(os.getenv("PROGRAMDATA")) / "Microsoft/Search/Data/Applications/Windows"
    if search.exists():
        for f in search.glob("*"):
            try:
                if f.is_file():
                    f.unlink()
                else:
                    shutil.rmtree(f, ignore_errors=True)
            except:
                pass
    print("Windows Search History cleared")

def restart_explorer():
    print("Restarting Explorer")
    subprocess.Popen(
        ["taskkill", "/im", "explorer.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    subprocess.Popen(
        ["explorer.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Explorer restart command sent")

if __name__ == "__main__":
    remove_recent_items()
    clear_thumbnail_cache()
    clear_run_history()
    clear_typed_paths()
    clear_start_menu_recent()
    clear_temp_folders()
    clear_prefetch()
    clear_search_history()
    restart_explorer()
    print("Done")