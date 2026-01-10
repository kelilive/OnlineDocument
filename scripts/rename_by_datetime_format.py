import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


DATETIME_PATTERNS = [
    (re.compile(r"(?P<Y>\d{4})(?P<m>\d{2})(?P<d>\d{2})(?P<H>\d{2})(?P<M>\d{2})(?P<S>\d{2})"),
     "%Y%m%d%H%M%S"),

    (re.compile(r"(?P<Y>\d{4})(?P<m>\d{2})(?P<d>\d{2})_(?P<H>\d{2})(?P<M>\d{2})(?P<S>\d{2})"),
     "%Y%m%d%H%M%S"),

    (re.compile(r"(?P<Y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})[ _](?P<H>\d{2})-(?P<M>\d{2})-(?P<S>\d{2})"),
     "%Y-%m-%d %H-%M-%S"),

    (re.compile(r"(?P<Y>\d{4})\.(?P<m>\d{2})\.(?P<d>\d{2})[ _](?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})"),
     "%Y.%m.%d %H:%M:%S"),

    (re.compile(r"(?P<Y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})[ _](?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})"),
     "%Y/%m/%d %H:%M:%S"),

    (re.compile(r"(?P<ts>\d{10}|\d{13})"), None),
]


def extract_datetime(text: str) -> Optional[datetime]:
    for regex, fmt in DATETIME_PATTERNS:
        m = regex.search(text)
        if not m:
            continue

        g = m.groupdict()

        if "ts" in g:
            ts = g["ts"]
            ts = int(ts) if len(ts) == 10 else int(ts) / 1000.0
            return datetime.fromtimestamp(ts)

        try:
            dt_str = fmt
            for k, v in {
                "%Y": g.get("Y", ""),
                "%m": g.get("m", ""),
                "%d": g.get("d", ""),
                "%H": g.get("H", "00"),
                "%M": g.get("M", "00"),
                "%S": g.get("S", "00"),
            }.items():
                dt_str = dt_str.replace(k, v)
            return datetime.strptime(dt_str, fmt)
        except:
            continue

    return None


def build_new_name(path: Path) -> Optional[str]:
    dt = extract_datetime(path.name)
    if not dt:
        return None
    return dt.strftime("IMG_%Y%m%d_%H%M%S") + path.suffix


def batch_rename(directory: str = "."):
    base = Path(directory)
    script_name = Path(sys.argv[0]).name  # <-- same skip logic you requested

    for p in base.iterdir():
        if not p.is_file():
            continue

        if p.name == script_name:  # <-- skip the script itself
            continue

        try:
            new_name = build_new_name(p)
            if not new_name or new_name == p.name:
                continue

            target = p.with_name(new_name)

            if target.exists():
                print(f"[SKIP] Target exists: {new_name}")
                continue

            p.rename(target)
            print(f"{p.name} -> {new_name}")

        except Exception as e:
            print(f"[ERROR] {p.name}: {e}")


if __name__ == "__main__":
    batch_rename(".")