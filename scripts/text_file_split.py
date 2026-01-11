import os

def split_by_lines(filepath, lines_per_part, output_dir=None):
    """
    Split a text file into multiple parts by fixed number of lines.
    """
    if output_dir is None:
        output_dir = filepath + "_parts"

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    part_index = 1
    for i in range(0, len(lines), lines_per_part):
        part_lines = lines[i:i + lines_per_part]
        out_path = os.path.join(output_dir, f"part_{part_index}.txt")
        with open(out_path, "w", encoding="utf-8") as out:
            out.writelines(part_lines)
        part_index += 1


def split_into_n_parts(filepath, n, output_dir=None):
    """
    Split a text file into N equal parts (last part may be shorter).
    """
    if output_dir is None:
        output_dir = filepath + "_parts"

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = len(lines)
    size = total // n + (1 if total % n else 0)

    part_index = 1
    for i in range(0, total, size):
        part_lines = lines[i:i + size]
        out_path = os.path.join(output_dir, f"part_{part_index}.txt")
        with open(out_path, "w", encoding="utf-8") as out:
            out.writelines(part_lines)
        part_index += 1


if __name__ == "__main__":
    # Example usage:
    filepath = "input.txt"

    # Option A: split by fixed number of lines
    split_by_lines(filepath, lines_per_part=200)

    # Option B: split into N parts
    # split_into_n_parts(filepath, n=6)