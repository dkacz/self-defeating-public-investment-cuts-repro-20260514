#!/usr/bin/env python3
"""Execute code cells from the branch notebook without preserving outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: execute_replacement_notebook.py NOTEBOOK.ipynb")

    notebook_path = Path(sys.argv[1]).resolve()
    artifact = notebook_path.parents[1]
    namespace = {"__name__": "__notebook__", "display": print}
    log_lines = []

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    old_cwd = Path.cwd()
    try:
        import os

        os.chdir(artifact)
        for idx, cell in enumerate(notebook.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            exec(compile(source, f"{notebook_path.name}:cell{idx}", "exec"), namespace)
            log_lines.append(f"PASS cell {idx}")
    finally:
        import os

        os.chdir(old_cwd)

    log_path = artifact / "qa" / "replacement_notebook_execution_log.txt"
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"PASS replacement notebook execution: {log_path}")


if __name__ == "__main__":
    main()
