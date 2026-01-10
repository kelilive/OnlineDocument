import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_DIR = "output"   # specify your output folder
THREADS = 8             # adjust based on your CPU cores

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def split_image(path):
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)

    tmp0 = f"{name}_0{ext}"
    tmp1 = f"{name}_1{ext}"

    out0 = os.path.join(OUTPUT_DIR, tmp0)
    out1 = os.path.join(OUTPUT_DIR, tmp1)

    if os.path.exists(out0) and os.path.exists(out1):
        return f"Skipping: {basename}"

    print(f"Processing: {basename}")

    cmd = [
        "gm", "convert", path,
        "-crop", "50x100%", "+repage",
        "+adjoin",
        f"{name}_%d{ext}"
    ]

    subprocess.run(cmd, shell=False)

    if os.path.exists(tmp0):
        os.rename(tmp0, out0)
    if os.path.exists(tmp1):
        os.rename(tmp1, out1)

    return f"Done: {basename}"

def main():
    ensure_output_dir()
    exts = [".jpg", ".jpeg", ".png"]

    files = [
        os.path.abspath(f)
        for f in os.listdir(".")
        if os.path.splitext(f)[1].lower() in exts
    ]

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(split_image, f): f for f in files}
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    main()