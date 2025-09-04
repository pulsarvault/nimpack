from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def find_esbuild() -> str:
    root = Path(__file__).resolve().parents[1]
    esb = root / "bin" / "esbuild"
    if not esb.exists():
        found = shutil.which("esbuild")
        return found or str(esb)
    return str(esb)


def detect_entry(project_dir: str) -> str:
    p = Path(project_dir)
    tsx = p / "src" / "main.tsx"
    jsx = p / "src" / "main.jsx"
    return str(tsx if tsx.exists() else jsx)


def run(entry: str, dist: str) -> None:
    esb = find_esbuild()
    out = Path(dist) / "bundle.js"
    cmd = [esb, entry, "--bundle", "--sourcemap", f"--outfile={out}"]
    print("⚡ Esbuild:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("✔ Esbuild bundled →", out)
