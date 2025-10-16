import json, sys, shutil
from pathlib import Path

def editMeta(ipynb_path, output_path=None, TA=False):

    ipynb_path = Path(ipynb_path)

    if not ipynb_path.exists():
        print(f"File not found: {ipynb_path}")
        sys.exit(1)

    # Create backup file
    backup_path = ipynb_path.with_name(f"{ipynb_path.stem}_backup{ipynb_path.suffix}")
    shutil.copy2(ipynb_path, backup_path)

    # Determine output path
    output_path = Path(output_path) if output_path else ipynb_path

    # Load
    with open(ipynb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Edit 
    for cell in notebook.get("cells", []):
        cell.setdefault("metadata", {})

        if TA:
            # TA=True: make all cells editable and deletable
            cell["metadata"]["editable"] = True
            cell["metadata"]["deletable"] = True
        else:
            # TA=False: make "checkit" or "assert" cells not editable and not deletable
            src = "".join(cell.get("source", [])).lower()
            if "checkit" in src or "assert" in src:
                cell["metadata"]["editable"] = False
                cell["metadata"]["deletable"] = False
            else:
                cell["metadata"]["editable"] = True
                cell["metadata"]["deletable"] = True

    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python editmeta.py <notebook.ipynb> [output.ipynb]")
        print("  python editmeta.py <notebook.ipynb> --TA [output.ipynb]")
        sys.exit(1)

    args = sys.argv[1:]
    TA_flag = False

    # Detect and strip --TA flag
    if "--TA" in args:
        TA_flag = True
        args.remove("--TA")

    ipynb_file = args[0]
    output_file = args[1] if len(args) > 1 else None

    editMeta(ipynb_file, output_file, TA=TA_flag)
