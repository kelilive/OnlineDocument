import os, shutil, subprocess, ctypes, sys
from pathlib import Path

def admin():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return
    except:
        pass
    print("Requesting admin...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas",
        sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def kill_exp():
    print("Stopping Explorer...")
    subprocess.Popen(["taskkill", "/f", "/im", "explorer.exe"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_exp():
    print("Starting Explorer...")
    subprocess.Popen(["explorer.exe"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clean_jmp():
    print("Cleaning JumpLists...")
    for p in [
        Path(os.getenv("APPDATA"))/"Microsoft/Windows/Recent/AutomaticDestinations",
        Path(os.getenv("APPDATA"))/"Microsoft/Windows/Recent/CustomDestinations"
    ]:
        if p.exists():
            for f in p.glob("*"):
                try: f.unlink()
                except: pass

def clean_thumb():
    print("Cleaning Thumbnails...")
    subprocess.Popen(["ie4uinit.exe", "-ClearIconCache"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clean_auto():
    print("Cleaning Address Bar...")
    subprocess.Popen(["reg","delete",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths",
        "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clean_search():
    print("Cleaning Search History...")
    base = Path(os.getenv("LOCALAPPDATA"))/"Packages/Microsoft.Windows.Search_cw5n1h2txyewy"
    for p in ["LocalState","Settings","AC","AppData"]:
        t = base/p
        if t.exists():
            shutil.rmtree(t, ignore_errors=True)

def clean_temp():
    print("Cleaning Temp...")
    for p in [Path(os.getenv("TEMP")), Path(os.getenv("WINDIR"))/"Temp"]:
        if p.exists():
            for f in p.glob("*"):
                try:
                    f.unlink() if f.is_file() else shutil.rmtree(f, ignore_errors=True)
                except: pass

if __name__ == "__main__":
    admin()
    kill_exp()
    clean_jmp()
    clean_thumb()
    clean_auto()
    clean_search()
    clean_temp()
    start_exp()
    print("Done")