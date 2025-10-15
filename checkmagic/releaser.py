import json
import sys
from pathlib import Path
import shutil

def releaseit(ipynb_path, output_path=None):
  
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

    # Load notebook JSON
    with open(ipynb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Add "deletable": false to each cell
    for cell in notebook.get("cells", []):
        if "metadata" not in cell:
            cell["metadata"] = {}
        cell["metadata"]["deletable"] = False

    # Save updated notebook
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

    print(f"Updated notebook saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python releaser.py <notebook.ipynb> [output.ipynb]")
        sys.exit(1)

    ipynb_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    releaseit(ipynb_file, output_file)
