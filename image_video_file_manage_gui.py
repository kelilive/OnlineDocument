import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

IGNORE_KEYWORDS = ["burst", "edited"]

# Match IMG_20240723_222617 or VID_20240723_222617
PATTERN = re.compile(r"^(IMG|VID)_(\d{8})_(\d{6})$")


def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def contains_ignored_keyword(filename: str) -> bool:
    lower = filename.lower()
    return any(key.lower() in lower for key in IGNORE_KEYWORDS)


def classify_and_move(src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:

            # Skip ignored keywords
            if contains_ignored_keyword(file):
                log(f"Skipped (ignored keyword): {file}")
                continue

            name, ext = os.path.splitext(file)

            # Match IMG_ or VID_ pattern
            match = PATTERN.match(name)
            if not match:
                log(f"Skipped (invalid filename): {file}")
                continue

            date_str = match.group(2)  # YYYYMMDD
            year = date_str[:4]
            month = date_str[4:6]

            target_folder = os.path.join(dst_dir, year, month)
            os.makedirs(target_folder, exist_ok=True)

            src_path = os.path.join(root, file)
            dst_path = os.path.join(target_folder, file)

            shutil.move(src_path, dst_path)
            log(f"Moved: {file} → {target_folder}")

    messagebox.showinfo("Done", "Classification completed.")


def choose_src():
    path = filedialog.askdirectory()
    if path:
        src_var.set(path)


def choose_dst():
    path = filedialog.askdirectory()
    if path:
        dst_var.set(path)


def start_sort():
    src = src_var.get()
    dst = dst_var.get()

    if not src or not dst:
        messagebox.showwarning("Warning", "Please select both source and destination folders.")
        return

    classify_and_move(src, dst)


# GUI
root = tk.Tk()
root.title("File Classifier (IMG/VID_YYYYMMDD_HHMMSS)")
root.geometry("600x450")

src_var = tk.StringVar()
dst_var = tk.StringVar()

tk.Label(root, text="Source Folder:").pack(anchor="w")
tk.Entry(root, textvariable=src_var, width=60).pack(anchor="w")
tk.Button(root, text="Browse", command=choose_src).pack(anchor="w")

tk.Label(root, text="Destination Folder:").pack(anchor="w")
tk.Entry(root, textvariable=dst_var, width=60).pack(anchor="w")
tk.Button(root, text="Browse", command=choose_dst).pack(anchor="w")

tk.Button(root, text="Start", command=start_sort, bg="#4CAF50", fg="white").pack(pady=10)

log_box = scrolledtext.ScrolledText(root, width=70, height=15)
log_box.pack()

root.mainloop()