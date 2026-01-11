import os
import re

def merge_parts(output_file="merged.txt"):
    """
    Merge part_1.txt, part_2.txt, ... in the current directory.
    Files must follow the naming pattern: part_<number>.txt
    """
    current_dir = os.getcwd()

    pattern = re.compile(r"part_(\d+)\.txt$", re.IGNORECASE)
    part_files = []

    # Scan current directory
    for filename in os.listdir(current_dir):
        match = pattern.match(filename)
        if match:
            index = int(match.group(1))
            part_files.append((index, filename))

    # Sort by numeric index
    part_files.sort(key=lambda x: x[0])

    # Merge
    with open(output_file, "w", encoding="utf-8") as outfile:
        for index, filename in part_files:
            with open(filename, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())

    return len(part_files)


if __name__ == "__main__":
    count = merge_parts("merged.txt")