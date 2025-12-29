import os
import shutil

def classify_files(base_dir):
    for filename in os.listdir(base_dir):
        full_path = os.path.join(base_dir, filename)

        # skip directories
        if os.path.isdir(full_path):
            continue

        # skip python script itself
        if filename.lower().endswith(".py"):
            continue

        # split by "-"
        if "-" not in filename:
            continue

        prefix = filename.split("-", 1)[0].strip()  # trim spaces

        if not prefix:
            continue

        folder_path = os.path.join(base_dir, prefix)

        # create folder if not exists
        os.makedirs(folder_path, exist_ok=True)

        # move file (keep original filename)
        shutil.move(full_path, os.path.join(folder_path, filename))

if __name__ == "__main__":
    classify_files(os.getcwd())
    print("Done.")