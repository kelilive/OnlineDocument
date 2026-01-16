import os
import subprocess

# Supported archive extensions
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".iso", ".tar", ".gz", ".bz2", ".xz", ".wim", ".cab", ".arj", ".lzma", ".z"}
OUTPUT_FILE = "output.txt"

def get_archive_content(path):
    """Uses 7z to list archive contents, ensuring long filenames and special characters are handled."""
    try:
        # -slt provides structured output to avoid truncation by spaces
        result = subprocess.run(
            ["7z", "l", "-ba", "-slt", path],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        paths = []
        for line in result.stdout.splitlines():
            if line.startswith("Path = "):
                inner_path = line[7:].replace("\\", "/")
                # Filter out the archive root itself
                if inner_path and inner_path != os.path.basename(path):
                    paths.append(inner_path)
        return sorted(paths)
    except Exception:
        return []

def build_tree_dict(root_dir):
    """
    Recursively builds a tree dictionary.
    Structure: { "name": { "children": { ... } } }
    """
    def insert_path(node, path_parts):
        curr = node
        for part in path_parts:
            if not part: continue
            if "children" not in curr:
                curr["children"] = {}
            if part not in curr["children"]:
                curr["children"][part] = {"children": {}}
            curr = curr["children"][part]

    root_name = os.path.basename(root_dir) or root_dir
    tree = {root_name: {"children": {}}}
    
    for root, dirs, files in os.walk(root_dir):
        # Calculate position in the tree dictionary
        rel_path = os.path.relpath(root, root_dir)
        curr_node = tree[root_name]
        if rel_path != ".":
            for part in rel_path.split(os.sep):
                curr_node = curr_node["children"][part]

        # Add directories
        for d in sorted(dirs):
            if d not in curr_node["children"]:
                curr_node["children"][d] = {"children": {}}

        # Add files
        for f in sorted(files):
            if f == OUTPUT_FILE: continue
            file_node = curr_node["children"].setdefault(f, {"children": {}})
            
            # Process archives
            if os.path.splitext(f)[1].lower() in ARCHIVE_EXT:
                archive_full_path = os.path.join(root, f)
                inner_files = get_archive_content(archive_full_path)
                for ifile in inner_files:
                    insert_path(file_node, ifile.split('/'))
                    
    return tree

def render_to_lines(tree_node, prefix=""):
    """
    Core rendering algorithm: strictly follows the 4-character indentation rule.
    """
    res = []
    children_dict = tree_node.get("children", {})
    items = sorted(children_dict.items())
    
    for i, (name, content) in enumerate(items):
        is_last = (i == len(items) - 1)
        
        # Determine current connector (length fixed at 4)
        connector = "└───" if is_last else "├───"
        res.append(f"{prefix}{connector}{name}")
        
        # Determine next level indentation prefix (length fixed at 4)
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        if content.get("children"):
            res.extend(render_to_lines(content, new_prefix))
            
    return res

def main():
    current_dir = os.getcwd()
    print(f"Analyzing directory and expanding virtual structure: {current_dir}")
    
    # 1. Scan and generate full tree dictionary
    tree_data = build_tree_dict(current_dir)
    
    # 2. Render to list of strings
    root_name = list(tree_data.keys())[0]
    output = [root_name]
    output.extend(render_to_lines(tree_data[root_name]))
    
    # 3. Write to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output) + "\n")
        
    print(f"Success! Tree saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()