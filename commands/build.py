from __future__ import annotations
import os, shutil, subprocess
from pathlib import Path

from utils.esbuild import detect_entry, find_esbuild
from utils.tailwind import build_css

def run() -> None:
    project_dir = Path(os.getcwd())
    entry = detect_entry(str(project_dir))
    dist_dir = project_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    out_js = dist_dir / "bundle.js"
    esb = find_esbuild()

    # production JS bundle
    cmd = [esb, entry, "--bundle", "--minify", f"--outfile={out_js}"]
    print("⚡ Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("✔ Production JS →", out_js)

    # production CSS via Tailwind v4 CLI
    build_css(str(project_dir))
    print("✔ Production CSS →", dist_dir / "styles.css")

    # copy index.html
    src_html = project_dir / "index.html"
    if src_html.exists():
        shutil.copy2(src_html, dist_dir / "index.html")
        print("✔ Copied index.html → dist/")
    else:
        print("⚠️ index.html not found at project root")


if __name__ == "__main__":
    run()
