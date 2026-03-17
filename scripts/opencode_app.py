import os
import json
import subprocess
import threading
import re
import platform
import ctypes
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog

# --- STEALTH STARTUP: HIDE THE WINDOW ---
def hide_console():
    """Hides the Python console window on Windows immediately."""
    if platform.system() == "Windows":
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0) # SW_HIDE
            ctypes.windll.kernel32.FreeConsole()

hide_console()

class PathHistoryManager:
    def __init__(self, config_file="path_history.json"):
        self.config_file = config_file
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_path(self, path):
        if not path or not os.path.exists(path): return
        path = os.path.normpath(path).replace('\\', '/')
        if path in self.history: self.history.remove(path)
        self.history.insert(0, path)
        self.history = self.history[:15]
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f)
        except: pass

class OpenCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCode AI Professional Terminal")
        self.root.geometry("1200x850")
        self.path_manager = PathHistoryManager()
        
        self.setup_styles()
        self.create_layout()
        self.add_new_tab()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.colors = {
            "sidebar_bg": "#252526",
            "main_bg": "#1e1e1e",
            "toolbar_bg": "#333333",
            "accent": "#007acc",
            "text": "#d4d4d4"
        }
        # ANSI Code Mapping
        self.ansi_tags = {
            "31": "#f48771", # Red
            "32": "#a9d18e", # Green
            "33": "#dcdcaa", # Yellow
            "34": "#569cd6", # Blue
            "36": "#4ec9b0", # Cyan
            "90": "#808080", # Grey
        }
        self.root.configure(bg=self.colors["sidebar_bg"])

    def create_layout(self):
        # 1. Top Bar for "New Session"
        self.header = tk.Frame(self.root, bg=self.colors["toolbar_bg"], height=40)
        self.header.pack(side=tk.TOP, fill=tk.X)
        tk.Button(self.header, text="+ New Tab", command=self.add_new_tab,
                  bg=self.colors["accent"], fg="white", bd=0, padx=15).pack(side=tk.LEFT, padx=10, pady=5)

        # 2. Main PanedWindow (Sidebar | Content)
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # 3. Sidebar (History Titles)
        self.sidebar_frame = tk.Frame(self.paned, bg=self.colors["sidebar_bg"], width=250)
        self.paned.add(self.sidebar_frame, weight=1)
        
        tk.Label(self.sidebar_frame, text="QUERY HISTORY", font=("Segoe UI", 9, "bold"),
                 bg=self.colors["sidebar_bg"], fg="#888888").pack(pady=(10, 5))
        
        self.history_listbox = tk.Listbox(self.sidebar_frame, bg=self.colors["sidebar_bg"], 
                                          fg="#cccccc", borderwidth=0, highlightthickness=0,
                                          font=("Segoe UI", 9), selectbackground="#37373d")
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 4. Right Side (Notebook for Tabs)
        self.content_frame = tk.Frame(self.paned, bg=self.colors["main_bg"])
        self.paned.add(self.content_frame, weight=4)

        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def add_new_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors["main_bg"])
        name = f"Session {datetime.now().strftime('%H:%M:%S')}"
        self.notebook.add(tab, text=name)
        
        # UI inside Tab
        inner_toolbar = tk.Frame(tab, bg=self.colors["main_bg"], pady=5)
        inner_toolbar.pack(fill=tk.X)
        
        tk.Label(inner_toolbar, text=" Path:", bg=self.colors["main_bg"], fg="white").pack(side=tk.LEFT, padx=5)
        p_var = tk.StringVar()
        p_combo = ttk.Combobox(inner_toolbar, textvariable=p_var, values=self.path_manager.history)
        p_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(inner_toolbar, text="Browse", command=lambda: self.select_dir(p_combo, p_var),
                  bg="#3e3e42", fg="white", bd=0, padx=10).pack(side=tk.LEFT, padx=5)

        # Scrolled Text (Terminal)
        display = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=("Consolas", 11),
                                           bg="#1e1e1e", fg="#d4d4d4", borderwidth=0)
        display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for code, hex_color in self.ansi_tags.items():
            display.tag_configure(f"ansi_{code}", foreground=hex_color)

        # Input Area
        input_frame = tk.Frame(tab, bg=self.colors["main_bg"], pady=10)
        input_frame.pack(fill=tk.X)
        entry = tk.Entry(input_frame, font=("Segoe UI", 11), bg="#3c3c3c", fg="white", 
                         insertbackground="white", relief=tk.FLAT)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        tk.Button(input_frame, text="Execute", command=lambda: self.handle_query(entry, display, p_var),
                  bg=self.colors["accent"], fg="white", width=12, bd=0).pack(side=tk.RIGHT, padx=10)
        
        entry.bind("<Return>", lambda e: self.handle_query(entry, display, p_var))
        self.notebook.select(tab)
        entry.focus_set()

    def select_dir(self, combo, var):
        directory = filedialog.askdirectory()
        if directory:
            path = os.path.normpath(directory).replace('\\', '/')
            var.set(path)
            self.path_manager.save_path(path)
            combo['values'] = self.path_manager.history

    def handle_query(self, entry, display, path_var):
        query = entry.get().strip()
        path = path_var.get().strip()
        if not query: return
        
        # Update Sidebar History
        title = f"[{datetime.now().strftime('%H:%M')}] {query[:30]}"
        self.history_listbox.insert(0, title)
        
        entry.delete(0, tk.END)
        self.append_ansi_text(display, f"\n>>> {query}\n", "34")
        threading.Thread(target=self.run_opencode, args=(query, path, display), daemon=True).start()

    def append_ansi_text(self, widget, text, default_tag=None):
        widget.config(state=tk.NORMAL)
        segments = re.split(r'\x1b\[([0-9;]+)m', text)
        current_tag = f"ansi_{default_tag}" if default_tag else None
        for i, seg in enumerate(segments):
            if i % 2 == 0:
                if seg: widget.insert(tk.END, seg, current_tag)
            else:
                if seg == "0": current_tag = None
                elif seg in self.ansi_tags: current_tag = f"ansi_{seg}"
        widget.see(tk.END)
        widget.config(state=tk.DISABLED)

    def run_opencode(self, query, path, display):
        try:
            
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            target_cwd = os.path.normpath(path) if path and os.path.exists(path) else None
            
            startupinfo = None
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0 # Hide child process window

            process = subprocess.Popen(
                ["opencode", "run", query],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, shell=True,
                cwd=target_cwd, env=env,
                encoding="utf-8", errors="replace",
                startupinfo=startupinfo
            )

            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None: break
                if line:
                    self.root.after(0, self.append_ansi_text, display, line)

        except Exception as e:
            self.root.after(0, self.append_ansi_text, display, f"\n[Error]: {str(e)}\n", "31")

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenCodeApp(root)
    root.mainloop()