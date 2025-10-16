import json, sys, shutil
from pathlib import Path

def editMeta(ipynb_path, output_path=None, remove=False):

    ipynb_path = Path(ipynb_path)

    if not ipynb_path.exists():
        print(f"File not found: {ipynb_path}")
        sys.exit(1)

    # Create backup file
    backup_path = ipynb_path.with_name(f"{ipynb_path.stem}_backup{ipynb_path.suffix}")
    shutil.copy2(ipynb_path, backup_path)
    print(f"Backup created: {backup_path}")

    # Determine output path
    output_path = Path(output_path) if output_path else ipynb_path

    # Load
    with open(ipynb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Edit 
    for cell in notebook.get("cells", []):
        cell.setdefault("metadata", {})

        if remove:
            # Remove the "deletable" key if it exists
            if "deletable" in cell["metadata"]:
                del cell["metadata"]["deletable"]
        else:
            # Add "deletable": false
            cell["metadata"]["deletable"] = False

    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python editmeta.py <notebook.ipynb> [output.ipynb]")
        print("  python editmeta.py <notebook.ipynb> --remove [output.ipynb]")
        sys.exit(1)

    args = sys.argv[1:]
    remove_flag = False

    # Detect and strip --remove flag
    if "--remove" in args:
        remove_flag = True
        args.remove("--remove")

    ipynb_file = args[0]
    output_file = args[1] if len(args) > 1 else None

    editMeta(ipynb_file, output_file, remove=remove_flag)
