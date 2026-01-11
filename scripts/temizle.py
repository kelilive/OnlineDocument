import os
import sys
import shutil
import winreg
import tempfile
import glob
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont


class ModernOfficeCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_widgets()
        self.center_window()

        # System information
        self.user_profile = os.environ.get("USERPROFILE", "")
        self.appdata = os.environ.get("APPDATA", "")
        self.localappdata = os.environ.get("LOCALAPPDATA", "")
        self.cleaned_items = []
        self.is_cleaning = False

    def setup_window(self):
        """Configure window settings"""
        self.root.title("Office History and System Cleaner")
        self.root.geometry("800x600")
        self.root.minsize(700, 550)
        self.root.configure(bg="#f0f0f0")

        # Set icon (if available)
        try:
            self.root.iconbitmap("cleaner.ico")
        except:
            pass

    def setup_variables(self):
        """Set up Tkinter variables"""
        self.var_recent_docs = tk.BooleanVar(value=True)
        self.var_office_history = tk.BooleanVar(value=True)
        self.var_temp_files = tk.BooleanVar(value=True)
        self.var_browser_cache = tk.BooleanVar(value=False)
        self.var_recycle_bin = tk.BooleanVar(value=False)
        self.var_windows_update = tk.BooleanVar(value=False)
        self.var_system_logs = tk.BooleanVar(value=False)
        self.var_prefetch = tk.BooleanVar(value=False)

        self.progress_var = tk.StringVar(value="Ready")
        self.progress_percent = tk.DoubleVar()

    def setup_styles(self):
        """Set up modern styles"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Colors
        self.colors = {
            "primary": "#2c3e50",
            "secondary": "#3498db",
            "success": "#27ae60",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "light": "#ecf0f1",
            "dark": "#2c3e50",
            "white": "#ffffff",
        }

        # Custom styles
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground=self.colors["primary"],
        )

        self.style.configure(
            "Subtitle.TLabel", font=("Segoe UI", 10), foreground=self.colors["dark"]
        )

        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground=self.colors["white"],
        )

        self.style.map(
            "Primary.TButton",
            background=[
                ("active", self.colors["primary"]),
                ("!active", self.colors["secondary"]),
            ],
        )

        self.style.configure(
            "Success.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground=self.colors["white"],
        )

        self.style.map(
            "Success.TButton",
            background=[("active", "#229954"), ("!active", self.colors["success"])],
        )

        self.style.configure(
            "Danger.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground=self.colors["white"],
        )

        self.style.map(
            "Danger.TButton",
            background=[("active", "#c0392b"), ("!active", self.colors["danger"])],
        )

    def create_widgets(self):
        """Create widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20)
        )

        ttk.Label(
            title_frame,
            text="🧹 Office History and System Cleaner",
            style="Title.TLabel",
        ).pack(side=tk.LEFT)

        # Admin status
        admin_status = "👑 Administrator" if self.is_admin() else "⚠️ Normal User"
        ttk.Label(title_frame, text=admin_status, style="Subtitle.TLabel").pack(
            side=tk.RIGHT
        )

        # Left panel - Options
        left_frame = ttk.LabelFrame(main_frame, text="Cleaning Options", padding="15")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Right panel - Log and Progress
        right_frame = ttk.LabelFrame(main_frame, text="Operation Status", padding="15")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Grid weights
        main_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)

        # Bottom panel - Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0)
        )

        self.create_buttons(button_frame)

    def create_left_panel(self, parent):
        """Left panel - options"""
        # Office options
        office_frame = ttk.LabelFrame(parent, text="Office Cleaning", padding="10")
        office_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(
            office_frame, text="📄 Recent Documents", variable=self.var_recent_docs
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            office_frame,
            text="📈 Office Application History",
            variable=self.var_office_history,
        ).pack(anchor=tk.W, pady=2)

        # System options
        system_frame = ttk.LabelFrame(parent, text="System Cleaning", padding="10")
        system_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(
            system_frame, text="📁 Temporary Files", variable=self.var_temp_files
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            system_frame, text="🌐 Browser Cache", variable=self.var_browser_cache
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            system_frame, text="🧹 Recycle Bin", variable=self.var_recycle_bin
        ).pack(anchor=tk.W, pady=2)

        # Advanced options
        advanced_frame = ttk.LabelFrame(parent, text="Advanced Cleaning", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(
            advanced_frame,
            text="🔄 Windows Update Cache",
            variable=self.var_windows_update,
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            advanced_frame, text="📋 System Logs", variable=self.var_system_logs
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            advanced_frame, text="⚡ Prefetch Files", variable=self.var_prefetch
        ).pack(anchor=tk.W, pady=2)

        # Quick selection buttons
        quick_frame = ttk.Frame(parent)
        quick_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(quick_frame, text="✓ Select All", command=self.select_all).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(quick_frame, text="✗ Select None", command=self.select_none).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(
            quick_frame, text="💼 Office Only", command=self.select_office_only
        ).pack(side=tk.LEFT)

    def create_right_panel(self, parent):
        """Right panel - log and progress"""
        # Progress status
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(progress_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(
            progress_frame, textvariable=self.progress_var, style="Subtitle.TLabel"
        )
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            parent, variable=self.progress_percent, maximum=100, length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        # Log area
        log_frame = ttk.Frame(parent)
        log_frame.pack(fill=tk.BOTH, expand=True)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=15, font=("Consolas", 9), wrap=tk.WORD
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Log coloring
        self.log_text.tag_config("success", foreground=self.colors["success"])
        self.log_text.tag_config("error", foreground=self.colors["danger"])
        self.log_text.tag_config("warning", foreground=self.colors["warning"])
        self.log_text.tag_config("info", foreground=self.colors["secondary"])

        # Initial message
        self.log_message("Office History and System Cleaner ready", "info")
        if not self.is_admin():
            self.log_message(
                "⚠️ Some operations may not be available without administrator privileges",
                "warning",
            )

    def create_buttons(self, parent):
        """Create buttons"""
        # Left side - main buttons
        left_buttons = ttk.Frame(parent)
        left_buttons.pack(side=tk.LEFT)

        self.start_button = ttk.Button(
            left_buttons,
            text="🚀 Start Cleaning",
            style="Success.TButton",
            command=self.start_cleaning,
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = ttk.Button(
            left_buttons,
            text="⏹️ Stop",
            style="Danger.TButton",
            command=self.stop_cleaning,
            state=tk.DISABLED,
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

        # Right side - helper buttons
        right_buttons = ttk.Frame(parent)
        right_buttons.pack(side=tk.RIGHT)

        ttk.Button(right_buttons, text="📋 Clear Log", command=self.clear_log).pack(
            side=tk.LEFT, padx=(0, 10)
        )

        ttk.Button(right_buttons, text="💾 Save Log", command=self.save_log).pack(
            side=tk.LEFT, padx=(0, 10)
        )

        ttk.Button(right_buttons, text="ℹ️ About", command=self.show_about).pack(
            side=tk.LEFT
        )

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def log_message(self, message, level="info"):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, formatted_message, level)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_progress(self, percent, status):
        """Update progress status"""
        self.progress_percent.set(percent)
        self.progress_var.set(status)
        self.root.update_idletasks()

    def select_all(self):
        """Select all options"""
        for var in [
            self.var_recent_docs,
            self.var_office_history,
            self.var_temp_files,
            self.var_browser_cache,
            self.var_recycle_bin,
            self.var_windows_update,
            self.var_system_logs,
            self.var_prefetch,
        ]:
            var.set(True)

    def select_none(self):
        """Select no options"""
        for var in [
            self.var_recent_docs,
            self.var_office_history,
            self.var_temp_files,
            self.var_browser_cache,
            self.var_recycle_bin,
            self.var_windows_update,
            self.var_system_logs,
            self.var_prefetch,
        ]:
            var.set(False)

    def select_office_only(self):
        """Select only Office options"""
        self.select_none()
        self.var_recent_docs.set(True)
        self.var_office_history.set(True)

    def clear_log(self):
        """Clear log area"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared", "info")

    def save_log(self):
        """Save log to file"""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Log File",
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"Log saved: {filename}", "success")
            except Exception as e:
                self.log_message(f"Error saving log: {e}", "error")

    def show_about(self):
        """About window"""
        messagebox.showinfo(
            "About",
            "Office History and System Cleaner\n"
            "Author: Onder AKOZ Version: 2.0\n"
            "Modern GUI for Windows system cleaning\n\n"
            "Features:\n"
            "• Office file history cleaning\n"
            "• System temporary file cleanup\n"
            "• Browser cache cleaning\n"
            "• Real-time progress tracking\n"
            "• Detailed log reports",
        )

    def start_cleaning(self):
        """Start cleaning process"""
        if self.is_cleaning:
            return

        # Check selected tasks
        selected_tasks = []
        if self.var_recent_docs.get():
            selected_tasks.append("recent_docs")
        if self.var_office_history.get():
            selected_tasks.append("office_history")
        if self.var_temp_files.get():
            selected_tasks.append("temp_files")
        if self.var_browser_cache.get():
            selected_tasks.append("browser_cache")
        if self.var_recycle_bin.get():
            selected_tasks.append("recycle_bin")
        if self.var_windows_update.get():
            selected_tasks.append("windows_update")
        if self.var_system_logs.get():
            selected_tasks.append("system_logs")
        if self.var_prefetch.get():
            selected_tasks.append("prefetch")

        if not selected_tasks:
            messagebox.showwarning(
                "Warning", "Please select at least one cleaning option!"
            )
            return

        # Get confirmation
        if not messagebox.askyesno(
            "Confirmation",
            f"{len(selected_tasks)} cleaning operations will be started.\n"
            "Do you want to continue?",
        ):
            return

        # Update UI
        self.is_cleaning = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start cleaning thread
        self.cleaning_thread = threading.Thread(
            target=self.run_cleaning, args=(selected_tasks,)
        )
        self.cleaning_thread.daemon = True
        self.cleaning_thread.start()

    def stop_cleaning(self):
        """Stop cleaning process"""
        self.is_cleaning = False
        self.log_message("Cleaning process stopped by user", "warning")
        self.cleanup_ui()

    def cleanup_ui(self):
        """Reset UI after cleaning"""
        self.is_cleaning = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_progress(0, "Ready")

    def run_cleaning(self, tasks):
        """Run cleaning operations"""
        total_tasks = len(tasks)
        completed = 0

        self.log_message("🚀 Cleaning process started", "info")

        task_functions = {
            "recent_docs": self.clean_recent_documents,
            "office_history": self.clean_office_history,
            "temp_files": self.clean_temp_files,
            "browser_cache": self.clean_browser_cache,
            "recycle_bin": self.clean_recycle_bin,
            "windows_update": self.clean_windows_update_cache,
            "system_logs": self.clean_system_logs,
            "prefetch": self.clean_prefetch,
        }

        for task in tasks:
            if not self.is_cleaning:
                break

            if task in task_functions:
                try:
                    task_functions[task]()
                    completed += 1
                    progress = (completed / total_tasks) * 100
                    self.update_progress(
                        progress, f"Completed: {completed}/{total_tasks}"
                    )
                except Exception as e:
                    self.log_message(f"Error: {task} - {e}", "error")

        if self.is_cleaning:
            self.log_message("✅ All cleaning operations completed!", "success")
            self.update_progress(100, "Completed")
            messagebox.showinfo(
                "Success", "Cleaning operations completed successfully!"
            )

        self.cleanup_ui()

    def clean_recycle_bin(self):
        """Clean recycle bin"""
        self.log_message("🗑️ Cleaning recycle bin...", "info")

        # Method 1: PowerShell command
        try:
            subprocess.run(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    "Clear-RecycleBin -Force -Confirm:$false",
                ],
                check=True,
                capture_output=True,
                timeout=30,
            )
            self.log_message("✓ Recycle bin cleaned (PowerShell)", "success")
            return
        except Exception as e:
            self.log_message(f"⚠️ PowerShell method failed: {str(e)[:100]}", "warning")

        # Method 2: CMD command
        try:
            subprocess.run(
                ["cmd", "/c", "rd /s /q %systemdrive%\\$Recycle.Bin"],
                check=True,
                capture_output=True,
                timeout=30,
            )
            self.log_message("✓ Recycle bin cleaned (CMD)", "success")
            return
        except Exception as e:
            self.log_message(f"⚠️ CMD method failed: {str(e)[:100]}", "warning")

        # Method 3: Manual Python cleaning
        try:
            import glob

            recycle_paths = []

            # Find $Recycle.Bin folders on all drives
            for drive in [
                "C:",
                "D:",
                "E:",
                "F:",
                "G:",
                "H:",
                "I:",
                "J:",
                "K:",
                "L:",
                "M:",
                "N:",
                "O:",
                "P:",
                "Q:",
                "R:",
                "S:",
                "T:",
                "U:",
                "V:",
                "W:",
                "X:",
                "Y:",
                "Z:",
            ]:
                recycle_path = os.path.join(drive, os.sep, "$Recycle.Bin")
                if os.path.exists(recycle_path):
                    recycle_paths.append(recycle_path)

            cleaned_items = 0
            for recycle_path in recycle_paths:
                try:
                    for root, dirs, files in os.walk(recycle_path):
                        # Delete files
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                os.remove(file_path)
                                cleaned_items += 1
                            except Exception:
                                continue

                        # Delete empty directories
                        for dir_name in dirs:
                            try:
                                dir_path = os.path.join(root, dir_name)
                                if not os.listdir(dir_path):  # If empty
                                    os.rmdir(dir_path)
                                    cleaned_items += 1
                            except Exception:
                                continue
                except Exception:
                    continue

            if cleaned_items > 0:
                self.log_message(
                    f"✓ Recycle bin cleaned ({cleaned_items} items - Python)", "success"
                )
            else:
                self.log_message("ℹ️ Recycle bin is already empty", "info")

        except Exception as e:
            self.log_message(f"✗ Error cleaning recycle bin: {str(e)[:100]}", "error")

    def safe_delete(self, path, item_name):
        """Safe deletion operation"""
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.log_message(f"✓ {item_name} cleaned", "success")
                return True
            else:
                self.log_message(f"⚠️ {item_name} not found", "warning")
                return False
        except Exception as e:
            self.log_message(f"✗ Error cleaning {item_name}: {e}", "error")
            return False

    def clean_recent_documents(self):
        """Clean recent documents list"""
        self.log_message("📄 Cleaning recent documents...", "info")

        recent_folder = os.path.join(self.appdata, "Microsoft", "Windows", "Recent")
        if os.path.exists(recent_folder):
            try:
                for file in os.listdir(recent_folder):
                    if not self.is_cleaning:
                        break
                    file_path = os.path.join(recent_folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                self.log_message("✓ Recent folder cleaned", "success")
            except Exception as e:
                self.log_message(f"✗ Error cleaning recent folder: {e}", "error")

    def clean_office_history(self):
        """Clean Office applications history"""
        self.log_message("📈 Cleaning Office history...", "info")

        # Special cleaning operations for Excel
        self.clean_excel_recent_files()

        # Special cleaning operations for Word
        self.clean_word_recent_files()

        # Office 365 cloud cleaning
        self.clean_office365_cloud_history()

        # General cleaning for other Office applications
        office_apps = {
            "PowerPoint": [
                r"Software\Microsoft\Office\16.0\PowerPoint\User MRU",
                r"Software\Microsoft\Office\15.0\PowerPoint\User MRU",
                r"Software\Microsoft\Office\14.0\PowerPoint\User MRU",
                r"Software\Microsoft\Office\16.0\PowerPoint\File MRU",
                r"Software\Microsoft\Office\15.0\PowerPoint\File MRU",
                r"Software\Microsoft\Office\14.0\PowerPoint\File MRU",
                r"Software\Microsoft\Office\16.0\PowerPoint\Recent Files",
                r"Software\Microsoft\Office\15.0\PowerPoint\Recent Files",
                r"Software\Microsoft\Office\14.0\PowerPoint\Recent Files",
                r"Software\Microsoft\Office\16.0\PowerPoint\Web Service Cache",
                r"Software\Microsoft\Office\16.0\PowerPoint\SharePoint",
                r"Software\Microsoft\Office\16.0\PowerPoint\OneDrive",
            ],
            "Access": [
                r"Software\Microsoft\Office\16.0\Access\User MRU",
                r"Software\Microsoft\Office\15.0\Access\User MRU",
                r"Software\Microsoft\Office\14.0\Access\User MRU",
                r"Software\Microsoft\Office\16.0\Access\File MRU",
                r"Software\Microsoft\Office\15.0\Access\File MRU",
                r"Software\Microsoft\Office\14.0\Access\File MRU",
            ],
        }

        for app_name, reg_paths in office_apps.items():
            if not self.is_cleaning:
                break
            app_cleaned = False
            cleaned_count = 0

            for reg_path in reg_paths:
                try:
                    # Try to open key
                    with winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS
                    ) as key:
                        # Delete all subkeys
                        subkeys_to_delete = []
                        try:
                            i = 0
                            while True:
                                subkey = winreg.EnumKey(key, i)
                                subkeys_to_delete.append(subkey)
                                i += 1
                        except OSError:
                            pass

                        # Delete subkeys
                        for subkey in subkeys_to_delete:
                            try:
                                winreg.DeleteKey(key, subkey)
                                cleaned_count += 1
                            except Exception:
                                pass

                        # Also delete values
                        values_to_delete = []
                        try:
                            i = 0
                            while True:
                                value_name, value_data, _ = winreg.EnumValue(key, i)
                                # Detect recent files related values
                                if any(
                                    keyword in value_name.lower()
                                    for keyword in [
                                        "recent",
                                        "mru",
                                        "file",
                                        "path",
                                        "document",
                                    ]
                                ):
                                    values_to_delete.append(value_name)
                                elif isinstance(value_data, str) and any(
                                    ext in value_data.lower()
                                    for ext in [
                                        ".ppt",
                                        ".pptx",
                                        ".pptm",
                                        ".mdb",
                                        ".accdb",
                                    ]
                                ):
                                    values_to_delete.append(value_name)
                                # SharePoint/OneDrive file references
                                elif isinstance(value_data, str) and any(
                                    keyword in value_data.lower()
                                    for keyword in [
                                        "sharepoint",
                                        "onedrive",
                                        "https://",
                                        "my.sharepoint.com",
                                    ]
                                ):
                                    values_to_delete.append(value_name)
                                i += 1
                        except OSError:
                            pass

                        for value_name in values_to_delete:
                            try:
                                winreg.DeleteValue(key, value_name)
                                cleaned_count += 1
                            except Exception:
                                pass

                        app_cleaned = True
                except Exception as e:
                    continue

            if app_cleaned and cleaned_count > 0:
                self.log_message(
                    f"✓ {app_name} history cleaned ({cleaned_count} records)", "success"
                )
            elif app_cleaned:
                self.log_message(f"✓ {app_name} history cleaned", "success")

    def clean_office365_cloud_history(self):
        """Clean Office 365 cloud history"""
        self.log_message("☁️ Cleaning Office 365 cloud history...", "info")

        # Office 365 cloud cache locations
        cloud_cache_locations = [
            # Microsoft Graph cache
            os.path.join(
                self.localappdata, "Microsoft", "Office", "16.0", "ClientTelemetry"
            ),
            os.path.join(
                self.localappdata, "Microsoft", "Office", "16.0", "RoamingOfficeData"
            ),
            os.path.join(
                self.localappdata, "Microsoft", "Office", "16.0", "WebServiceCache"
            ),
            # OneDrive integration cache
            os.path.join(self.localappdata, "Microsoft", "OneDrive", "cache"),
            os.path.join(self.localappdata, "Microsoft", "OneDrive", "logs"),
            os.path.join(self.appdata, "Microsoft", "OneDrive", "settings"),
            # SharePoint cache
            os.path.join(self.localappdata, "Microsoft", "SharePoint Designer"),
            os.path.join(self.appdata, "Microsoft", "SharePoint"),
            # Teams integration (for Office integration)
            os.path.join(self.appdata, "Microsoft", "Teams", "Application Cache"),
            os.path.join(self.appdata, "Microsoft", "Teams", "Cache"),
            # Office roaming settings
            os.path.join(self.localappdata, "Microsoft", "Office", "16.0", "roaming"),
            os.path.join(self.appdata, "Microsoft", "Office", "16.0", "roaming"),
        ]

        cleaned_files = 0
        for cache_location in cloud_cache_locations:
            if not self.is_cleaning:
                break
            if os.path.exists(cache_location):
                try:
                    for root, dirs, files in os.walk(cache_location):
                        for file in files:
                            # Clean cloud related cache files
                            if any(
                                keyword in file.lower()
                                for keyword in [
                                    "recent",
                                    "mru",
                                    "cache",
                                    "temp",
                                    "log",
                                    "sharepoint",
                                    "onedrive",
                                    "teams",
                                    "graph",
                                    ".json",
                                    ".xml",
                                    ".tmp",
                                    ".log",
                                ]
                            ):
                                file_path = os.path.join(root, file)
                                try:
                                    os.remove(file_path)
                                    cleaned_files += 1
                                except Exception:
                                    pass
                except Exception as e:
                    continue

        if cleaned_files > 0:
            self.log_message(
                f"✓ Office 365 cloud cache cleaned ({cleaned_files} files)", "success"
            )

        # Registry entries for Office 365 cloud
        office365_registry_locations = [
            r"Software\Microsoft\Office\16.0\Common\Roaming",
            r"Software\Microsoft\Office\16.0\Common\Internet",
            r"Software\Microsoft\Office\16.0\Common\Identity",
            r"Software\Microsoft\Office\16.0\Common\Experiment",
            r"Software\Microsoft\OneDrive",
            r"Software\Microsoft\SharePoint",
        ]

        registry_cleaned = 0
        for reg_location in office365_registry_locations:
            if not self.is_cleaning:
                break
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, reg_location, 0, winreg.KEY_ALL_ACCESS
                ) as key:
                    # Clean recent and cache related values
                    values_to_delete = []
                    try:
                        i = 0
                        while True:
                            value_name, value_data, _ = winreg.EnumValue(key, i)
                            if any(
                                keyword in value_name.lower()
                                for keyword in ["recent", "cache", "temp", "mru"]
                            ):
                                values_to_delete.append(value_name)
                            elif isinstance(value_data, str) and any(
                                keyword in value_data.lower()
                                for keyword in [
                                    "sharepoint",
                                    "onedrive",
                                    "graph.microsoft.com",
                                ]
                            ):
                                values_to_delete.append(value_name)
                            i += 1
                    except OSError:
                        pass

                    for value_name in values_to_delete:
                        try:
                            winreg.DeleteValue(key, value_name)
                            registry_cleaned += 1
                        except Exception:
                            pass
            except Exception as e:
                continue

        if registry_cleaned > 0:
            self.log_message(
                f"✓ Office 365 registry entries cleaned ({registry_cleaned} entries)",
                "success",
            )

    def clean_word_recent_files(self):
        """Clean Word's recent files list specially"""
        self.log_message("📝 Cleaning Word recent files list...", "info")

        # All locations for Word recent file records
        word_locations = [
            # Office 2016/2019/365 (16.0) - Comprehensive list
            r"Software\Microsoft\Office\16.0\Word\Recent Files",
            r"Software\Microsoft\Office\16.0\Word\User MRU",
            r"Software\Microsoft\Office\16.0\Word\File MRU",
            r"Software\Microsoft\Office\16.0\Word\Place MRU",
            r"Software\Microsoft\Office\16.0\Word\Security\Trusted Documents",
            r"Software\Microsoft\Office\16.0\Word\Options",
            r"Software\Microsoft\Office\16.0\Word\Data",
            r"Software\Microsoft\Office\16.0\Common\Open Find\Microsoft Office Word\Settings",
            r"Software\Microsoft\Office\16.0\Common\General",
            # Office 365 Cloud/SharePoint records
            r"Software\Microsoft\Office\16.0\Word\Web Service Cache",
            r"Software\Microsoft\Office\16.0\Word\SharePoint",
            r"Software\Microsoft\Office\16.0\Word\OneDrive",
            r"Software\Microsoft\Office\16.0\Common\Internet",
            r"Software\Microsoft\Office\16.0\Common\Roaming",
            r"Software\Microsoft\Office\16.0\Common\Identity",
            # Office 2013 (15.0)
            r"Software\Microsoft\Office\15.0\Word\Recent Files",
            r"Software\Microsoft\Office\15.0\Word\User MRU",
            r"Software\Microsoft\Office\15.0\Word\File MRU",
            r"Software\Microsoft\Office\15.0\Word\Place MRU",
            r"Software\Microsoft\Office\15.0\Word\Security\Trusted Documents",
            r"Software\Microsoft\Office\15.0\Word\Options",
            r"Software\Microsoft\Office\15.0\Word\Data",
            r"Software\Microsoft\Office\15.0\Common\Open Find\Microsoft Office Word\Settings",
            r"Software\Microsoft\Office\15.0\Word\Web Service Cache",
            r"Software\Microsoft\Office\15.0\Word\SharePoint",
            # Office 2010 (14.0)
            r"Software\Microsoft\Office\14.0\Word\Recent Files",
            r"Software\Microsoft\Office\14.0\Word\User MRU",
            r"Software\Microsoft\Office\14.0\Word\File MRU",
            r"Software\Microsoft\Office\14.0\Word\Place MRU",
            r"Software\Microsoft\Office\14.0\Word\Security\Trusted Documents",
            r"Software\Microsoft\Office\14.0\Word\Options",
            r"Software\Microsoft\Office\14.0\Word\Data",
            # Older Office versions
            r"Software\Microsoft\Office\12.0\Word\Recent Files",
            r"Software\Microsoft\Office\11.0\Word\Recent Files",
        ]

        cleaned_count = 0

        # Registry cleaning
        for reg_path in word_locations:
            if not self.is_cleaning:
                break
            try:
                # Open registry key
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS
                ) as key:
                    # List and delete all values
                    values_to_delete = []
                    try:
                        i = 0
                        while True:
                            value_name, value_data, _ = winreg.EnumValue(key, i)
                            # Detect recent files related values
                            if any(
                                keyword in value_name.lower()
                                for keyword in [
                                    "recent",
                                    "mru",
                                    "file",
                                    "path",
                                    "document",
                                ]
                            ):
                                values_to_delete.append(value_name)
                            elif isinstance(value_data, str) and any(
                                ext in value_data.lower()
                                for ext in [".docx", ".doc", ".docm", ".dot", ".dotx"]
                            ):
                                values_to_delete.append(value_name)
                            # SharePoint/OneDrive file references
                            elif isinstance(value_data, str) and any(
                                keyword in value_data.lower()
                                for keyword in [
                                    "sharepoint",
                                    "onedrive",
                                    "https://",
                                    "my.sharepoint.com",
                                ]
                            ):
                                values_to_delete.append(value_name)
                            i += 1
                    except OSError:
                        pass

                    # Delete values
                    for value_name in values_to_delete:
                        try:
                            winreg.DeleteValue(key, value_name)
                            cleaned_count += 1
                        except Exception:
                            pass

                    # Also delete subkeys
                    subkeys_to_delete = []
                    try:
                        i = 0
                        while True:
                            subkey = winreg.EnumKey(key, i)
                            subkeys_to_delete.append(subkey)
                            i += 1
                    except OSError:
                        pass

                    for subkey in subkeys_to_delete:
                        try:
                            self.delete_registry_key_recursive(
                                winreg.HKEY_CURRENT_USER, f"{reg_path}\\{subkey}"
                            )
                            cleaned_count += 1
                        except Exception:
                            pass

            except Exception as e:
                continue

        # Also clean Word file history
        self.clean_word_file_history()

        # Word OneDrive/SharePoint cache cleaning
        self.clean_word_cloud_cache()

        if cleaned_count > 0:
            self.log_message(
                f"✓ {cleaned_count} recent file records cleaned from Word", "success"
            )
        else:
            self.log_message(
                "⚠️ Word recent files not found or already clean", "warning"
            )

    def clean_word_cloud_cache(self):
        """Clean Word's OneDrive/SharePoint cache files"""
        self.log_message("☁️ Cleaning Word cloud cache...", "info")

        # Word OneDrive cache locations
        word_cache_paths = [
            os.path.join(self.localappdata, "Microsoft", "Office", "16.0", "Wef"),
            os.path.join(self.localappdata, "Microsoft", "Office", "15.0", "Wef"),
            os.path.join(self.localappdata, "Microsoft", "Office", "14.0", "Wef"),
            os.path.join(self.appdata, "Microsoft", "Office", "16.0", "roaming"),
            os.path.join(self.appdata, "Microsoft", "Office", "15.0", "roaming"),
            os.path.join(self.localappdata, "Microsoft", "Office", "16.0", "roaming"),
            os.path.join(self.localappdata, "Microsoft", "Office", "15.0", "roaming"),
        ]

        for cache_path in word_cache_paths:
            if not self.is_cleaning:
                break
            if os.path.exists(cache_path):
                try:
                    for root, dirs, files in os.walk(cache_path):
                        for file in files:
                            if any(
                                keyword in file.lower()
                                for keyword in [
                                    "recent",
                                    "mru",
                                    "cache",
                                    "word",
                                    ".json",
                                    ".xml",
                                ]
                            ):
                                file_path = os.path.join(root, file)
                                try:
                                    os.remove(file_path)
                                    self.log_message(
                                        f"✓ Word cloud cache cleaned: {file}", "success"
                                    )
                                except Exception:
                                    pass
                except Exception as e:
                    continue

    def clean_word_file_history(self):
        """Clean Word's file history from AppData"""
        try:
            # Word's local settings files
            word_roaming_path = os.path.join(self.appdata, "Microsoft", "Word")
            word_local_path = os.path.join(self.localappdata, "Microsoft", "Office")

            # Roaming Word folder
            if os.path.exists(word_roaming_path):
                for file in os.listdir(word_roaming_path):
                    if file.endswith(".officeUI") or "recent" in file.lower():
                        file_path = os.path.join(word_roaming_path, file)
                        try:
                            os.remove(file_path)
                            self.log_message(
                                f"✓ Word config file cleaned: {file}", "success"
                            )
                        except Exception:
                            pass

            # Local Word cache
            if os.path.exists(word_local_path):
                for root, dirs, files in os.walk(word_local_path):
                    for file in files:
                        if (
                            any(
                                keyword in file.lower()
                                for keyword in ["recent", "mru", "cache"]
                            )
                            and "word" in root.lower()
                        ):
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                self.log_message(
                                    f"✓ Word cache file cleaned: {file}", "success"
                                )
                            except Exception:
                                pass
        except Exception as e:
            self.log_message(f"✗ Error cleaning Word file history: {e}", "error")

    def clean_excel_recent_files(self):
        """Clean Excel's recent files list specially"""
        self.log_message("📊 Cleaning Excel recent files list...", "info")

        # All locations for Excel recent file records
        excel_locations = [
            # Office 2016/2019/365 (16.0) - Comprehensive list
            r"Software\Microsoft\Office\16.0\Excel\Recent Files",
            r"Software\Microsoft\Office\16.0\Excel\User MRU",
            r"Software\Microsoft\Office\16.0\Excel\File MRU",
            r"Software\Microsoft\Office\16.0\Excel\Place MRU",
            r"Software\Microsoft\Office\16.0\Excel\Security\Trusted Documents",
            r"Software\Microsoft\Office\16.0\Excel\Options",
            r"Software\Microsoft\Office\16.0\Common\Open Find\Microsoft Office Excel\Settings",
            r"Software\Microsoft\Office\16.0\Common\General",
            # Office 365 Cloud/SharePoint records
            r"Software\Microsoft\Office\16.0\Excel\Web Service Cache",
            r"Software\Microsoft\Office\16.0\Excel\SharePoint",
            r"Software\Microsoft\Office\16.0\Excel\OneDrive",
            r"Software\Microsoft\Office\16.0\Common\Internet",
            r"Software\Microsoft\Office\16.0\Common\Roaming",
            r"Software\Microsoft\Office\16.0\Common\Identity",
            # Office 2013 (15.0)
            r"Software\Microsoft\Office\15.0\Excel\Recent Files",
            r"Software\Microsoft\Office\15.0\Excel\User MRU",
            r"Software\Microsoft\Office\15.0\Excel\File MRU",
            r"Software\Microsoft\Office\15.0\Excel\Place MRU",
            r"Software\Microsoft\Office\15.0\Excel\Security\Trusted Documents",
            r"Software\Microsoft\Office\15.0\Excel\Options",
            r"Software\Microsoft\Office\15.0\Common\Open Find\Microsoft Office Excel\Settings",
            r"Software\Microsoft\Office\15.0\Excel\Web Service Cache",
            r"Software\Microsoft\Office\15.0\Excel\SharePoint",
            # Office 2010 (14.0)
            r"Software\Microsoft\Office\14.0\Excel\Recent Files",
            r"Software\Microsoft\Office\14.0\Excel\User MRU",
            r"Software\Microsoft\Office\14.0\Excel\File MRU",
            r"Software\Microsoft\Office\14.0\Excel\Place MRU",
            r"Software\Microsoft\Office\14.0\Excel\Security\Trusted Documents",
            r"Software\Microsoft\Office\14.0\Excel\Options",
            # Older Office versions
            r"Software\Microsoft\Office\12.0\Excel\Recent Files",
            r"Software\Microsoft\Office\11.0\Excel\Recent Files",
        ]

        cleaned_count = 0

        # Registry cleaning
        for reg_path in excel_locations:
            if not self.is_cleaning:
                break
            try:
                # Open registry key
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS
                ) as key:
                    # List and delete all values
                    values_to_delete = []
                    try:
                        i = 0
                        while True:
                            value_name, value_data, _ = winreg.EnumValue(key, i)
                            # Detect recent files related values
                            if any(
                                keyword in value_name.lower()
                                for keyword in [
                                    "recent",
                                    "mru",
                                    "file",
                                    "path",
                                    "document",
                                ]
                            ):
                                values_to_delete.append(value_name)
                            elif isinstance(value_data, str) and any(
                                ext in value_data.lower()
                                for ext in [".xlsx", ".xls", ".xlsm", ".xlsb"]
                            ):
                                values_to_delete.append(value_name)
                            # SharePoint/OneDrive file references
                            elif isinstance(value_data, str) and any(
                                keyword in value_data.lower()
                                for keyword in [
                                    "sharepoint",
                                    "onedrive",
                                    "https://",
                                    "my.sharepoint.com",
                                ]
                            ):
                                values_to_delete.append(value_name)
                            i += 1
                    except OSError:
                        pass

                    # Delete values
                    for value_name in values_to_delete:
                        try:
                            winreg.DeleteValue(key, value_name)
                            cleaned_count += 1
                        except Exception:
                            pass

                    # Also delete subkeys
                    subkeys_to_delete = []
                    try:
                        i = 0
                        while True:
                            subkey = winreg.EnumKey(key, i)
                            subkeys_to_delete.append(subkey)
                            i += 1
                    except OSError:
                        pass

                    for subkey in subkeys_to_delete:
                        try:
                            self.delete_registry_key_recursive(
                                winreg.HKEY_CURRENT_USER, f"{reg_path}\\{subkey}"
                            )
                            cleaned_count += 1
                        except Exception:
                            pass

            except Exception as e:
                continue

        # Also clean Excel file history
        self.clean_excel_file_history()

        # Excel OneDrive/SharePoint cache cleaning
        self.clean_excel_cloud_cache()

        if cleaned_count > 0:
            self.log_message(
                f"✓ {cleaned_count} recent file records cleaned from Excel", "success"
            )
        else:
            self.log_message(
                "⚠️ Excel recent files not found or already clean", "warning"
            )

    def clean_excel_cloud_cache(self):
        """Clean Excel's OneDrive/SharePoint cache files"""
        self.log_message("☁️ Cleaning Excel cloud cache...", "info")

        # OneDrive cache locations
        onedrive_cache_paths = [
            os.path.join(self.localappdata, "Microsoft", "OneDrive", "logs"),
            os.path.join(self.localappdata, "Microsoft", "OneDrive", "settings"),
            os.path.join(self.appdata, "Microsoft", "OneDrive", "logs"),
            os.path.join(self.appdata, "Microsoft", "SharePoint"),
            os.path.join(self.localappdata, "Microsoft", "Office", "16.0", "Wef"),
            os.path.join(self.localappdata, "Microsoft", "Office", "15.0", "Wef"),
            os.path.join(self.localappdata, "Microsoft", "Office", "14.0", "Wef"),
        ]

        # Office 365 roaming settings
        office365_paths = [
            os.path.join(self.localappdata, "Microsoft", "Office", "16.0", "roaming"),
            os.path.join(self.localappdata, "Microsoft", "Office", "15.0", "roaming"),
            os.path.join(self.appdata, "Microsoft", "Office", "16.0", "roaming"),
            os.path.join(self.appdata, "Microsoft", "Office", "15.0", "roaming"),
        ]

        all_cache_paths = onedrive_cache_paths + office365_paths

        for cache_path in all_cache_paths:
            if not self.is_cleaning:
                break
            if os.path.exists(cache_path):
                try:
                    for root, dirs, files in os.walk(cache_path):
                        for file in files:
                            if any(
                                keyword in file.lower()
                                for keyword in [
                                    "recent",
                                    "mru",
                                    "cache",
                                    "excel",
                                    ".json",
                                    ".xml",
                                ]
                            ):
                                file_path = os.path.join(root, file)
                                try:
                                    os.remove(file_path)
                                    self.log_message(
                                        f"✓ Excel cloud cache cleaned: {file}",
                                        "success",
                                    )
                                except Exception:
                                    pass
                except Exception as e:
                    continue

    def clean_excel_file_history(self):
        """Clean Excel's file history from AppData"""
        try:
            # Excel's local settings files
            excel_roaming_path = os.path.join(self.appdata, "Microsoft", "Excel")
            excel_local_path = os.path.join(self.localappdata, "Microsoft", "Office")

            # Roaming Excel folder
            if os.path.exists(excel_roaming_path):
                for file in os.listdir(excel_roaming_path):
                    if file.endswith(".officeUI") or "recent" in file.lower():
                        file_path = os.path.join(excel_roaming_path, file)
                        try:
                            os.remove(file_path)
                            self.log_message(
                                f"✓ Excel config file cleaned: {file}", "success"
                            )
                        except Exception:
                            pass

            # Local Excel cache
            if os.path.exists(excel_local_path):
                for root, dirs, files in os.walk(excel_local_path):
                    for file in files:
                        if any(
                            keyword in file.lower()
                            for keyword in ["recent", "mru", "cache"]
                        ):
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                self.log_message(
                                    f"✓ Excel cache file cleaned: {file}", "success"
                                )
                            except Exception:
                                pass
        except Exception as e:
            self.log_message(f"✗ Error cleaning Excel file history: {e}", "error")

    def delete_registry_key_recursive(self, hive, key_path):
        """Delete registry key recursively with subkeys"""
        try:
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                # List subkeys
                subkeys = []
                try:
                    i = 0
                    while True:
                        subkey = winreg.EnumKey(key, i)
                        subkeys.append(subkey)
                        i += 1
                except OSError:
                    pass

                # Delete subkeys recursively
                for subkey in subkeys:
                    self.delete_registry_key_recursive(hive, f"{key_path}\\{subkey}")

            # Delete main key
            winreg.DeleteKey(hive, key_path)

        except Exception as e:
            pass

    def clean_temp_files(self):
        """Clean temporary files"""
        self.log_message("🗂️ Cleaning temporary files...", "info")

        temp_locations = [
            tempfile.gettempdir(),
            os.path.join(os.environ.get("WINDIR", ""), "Temp"),
            os.path.join(self.localappdata, "Temp"),
        ]

        for temp_dir in temp_locations:
            if not self.is_cleaning:
                break
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        if not self.is_cleaning:
                            break
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            else:
                                os.remove(item_path)
                        except Exception:
                            continue
                    self.log_message(f"✓ Temp folder cleaned: {temp_dir}", "success")
                except Exception as e:
                    self.log_message(f"✗ Error cleaning temp folder: {e}", "error")

    def clean_browser_cache(self):
        """Clean browser cache"""
        self.log_message("🌐 Cleaning browser cache...", "info")

        # Chrome
        chrome_cache = os.path.join(
            self.localappdata, "Google", "Chrome", "User Data", "Default", "Cache"
        )
        self.safe_delete(chrome_cache, "Chrome Cache")

        # Firefox
        firefox_profiles = os.path.join(self.appdata, "Mozilla", "Firefox", "Profiles")
        if os.path.exists(firefox_profiles):
            for profile in os.listdir(firefox_profiles):
                if not self.is_cleaning:
                    break
                cache_path = os.path.join(firefox_profiles, profile, "cache2")
                self.safe_delete(cache_path, "Firefox Cache")

        # Edge
        edge_cache = os.path.join(
            self.localappdata, "Microsoft", "Edge", "User Data", "Default", "Cache"
        )
        self.safe_delete(edge_cache, "Edge Cache")

    def clean_windows_update_cache(self):
        """Clean Windows Update cache"""
        self.log_message("🔄 Cleaning Windows Update cache...", "info")

        update_cache = os.path.join(
            os.environ.get("WINDIR", ""), "SoftwareDistribution", "Download"
        )
        self.safe_delete(update_cache, "Windows Update Cache")

    def clean_system_logs(self):
        """Clean system logs"""
        self.log_message("📋 Cleaning system logs...", "info")

        log_locations = [
            os.path.join(os.environ.get("WINDIR", ""), "Logs"),
            os.path.join(os.environ.get("WINDIR", ""), "Temp"),
        ]

        for log_dir in log_locations:
            if not self.is_cleaning:
                break
            if os.path.exists(log_dir):
                try:
                    for file in glob.glob(os.path.join(log_dir, "*.log")):
                        if not self.is_cleaning:
                            break
                        self.safe_delete(file, "Log file")
                except Exception as e:
                    self.log_message(f"✗ Error cleaning log files: {e}", "error")

    def clean_prefetch(self):
        """Clean prefetch files"""
        self.log_message("⚡ Cleaning prefetch files...", "info")

        prefetch_dir = os.path.join(os.environ.get("WINDIR", ""), "Prefetch")
        if os.path.exists(prefetch_dir):
            try:
                for file in os.listdir(prefetch_dir):
                    if not self.is_cleaning:
                        break
                    if file.endswith(".pf"):
                        file_path = os.path.join(prefetch_dir, file)
                        self.safe_delete(file_path, "Prefetch file")
            except Exception as e:
                self.log_message(f"✗ Error cleaning prefetch files: {e}", "error")

    def is_admin(self):
        """Check administrator privileges"""
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes

            return ctypes.windll.shell32.IsUserAnAdmin() != 0


def main():
    """Main function"""
    # Start Tkinter
    root = tk.Tk()

    # Start application
    app = ModernOfficeCleanerGUI(root)

    # Main loop
    root.mainloop()


if __name__ == "__main__":
    main()
