import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_datetime(path: Path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return None
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None
    return None


def build_timestamp_name(dt: datetime, suffix: str):
    return dt.strftime("IMG_%Y%m%d_%H%M%S") + suffix


def resolve_conflict_timestamp(original_dt: datetime, suffix: str, directory: Path):
    """
    Find all IMG_YYYYMMDD_HHMMSS* files,
    extract timestamps, pick the largest, then +1 second.
    """
    pattern = re.compile(r"IMG_(\d{8})_(\d{6})")
    latest_timestamp = original_dt

    for p in directory.iterdir():
        if not p.is_file():
            continue

        match = pattern.match(p.stem)
        if not match:
            continue

        date_part = match.group(1)
        time_part = match.group(2)

        try:
            existing_dt = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
            if existing_dt > latest_timestamp:
                latest_timestamp = existing_dt
        except:
            continue

    next_timestamp = latest_timestamp + timedelta(seconds=1)
    return build_timestamp_name(next_timestamp, suffix)


def safe_rename(path: Path, desired_name: str, directory: Path):
    # Skip if identical
    if path.name == desired_name:
        return

    target = path.with_name(desired_name)

    # No conflict → rename directly
    if not target.exists():
        path.rename(target)
        return

    # Conflict → resolve by timestamp shifting
    timestamp_str = desired_name[4:19]  # YYYYMMDD_HHMMSS
    original_dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
    suffix = path.suffix

    resolved_name = resolve_conflict_timestamp(original_dt, suffix, directory)
    resolved_target = path.with_name(resolved_name)

    if not resolved_target.exists():
        path.rename(resolved_target)
        print(f"[RESOLVED] {path.name} -> {resolved_name}")
        return

    print(f"[FAILED] Could not resolve conflict for {path.name}")


def main():
    base = Path(".")
    script_name = Path(sys.argv[0]).name  # skip the script itself

    for p in base.iterdir():
        if not p.is_file():
            continue

        if p.name == script_name:
            continue

        exif_dt = get_exif_datetime(p)

        if exif_dt:
            desired_name = build_timestamp_name(exif_dt, p.suffix)
            safe_rename(p, desired_name, base)
        else:
            if not p.name.startswith("[NO_EXIF]"):
                new_name = "[NO_EXIF]" + p.name
                p.rename(p.with_name(new_name))
                print(f"[NO_EXIF] {p.name} -> {new_name}")


if __name__ == "__main__":
    main()