import os, subprocess, shutil

def run():
    projectDir = os.getcwd()
    entry = os.path.join(projectDir, "src", "main.jsx")
    distDir = os.path.join(projectDir, "dist")

    os.makedirs(distDir, exist_ok=True)
    out = os.path.join(distDir, "bundle.js")

    # Locate esbuild in repo root
    root = os.path.dirname(os.path.dirname(__file__))  # go up from commands/
    esb = os.path.join(root, "bin", "esbuild")
    if not os.path.exists(esb):
        esb = shutil.which("esbuild") or esb

    cmd = [
        esb, entry,
        "--bundle", "--minify",
        "--outfile=" + out
    ]

    print("⚡ Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("✔ Production build →", out)

    # Copy index.html into dist
    srcHtml = os.path.join(projectDir, "index.html")
    if os.path.exists(srcHtml):
        shutil.copy2(srcHtml, os.path.join(distDir, "index.html"))
        print("✔ Copied index.html → dist/")
