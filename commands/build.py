from __future__ import annotations

import os
import shutil
from pathlib import Path

from utils.esbuild import detect_entry, run as run_esbuild  # ✅ use wrapper
from utils.tailwind import build_css


def run() -> None:
    project_dir = Path(os.getcwd())
    entry = detect_entry(str(project_dir))
    dist_dir = project_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    # JS (production)
    run_esbuild(entry, str(dist_dir), minify=True, sourcemap=False)

    # CSS (production)
    build_css(str(project_dir))
    print("✔ Production CSS →", dist_dir / "styles.css")

    # HTML
    src_html = project_dir / "index.html"
    if src_html.exists():
        shutil.copy2(src_html, dist_dir / "index.html")
        print("✔ Copied index.html → dist/")
    else:
        print("⚠️ index.html not found at project root")
