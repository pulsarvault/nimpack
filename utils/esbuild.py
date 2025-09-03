import os, subprocess, shutil

def run(entry: str, dist: str):
    out = os.path.join(dist, "bundle.js")

    # find esbuild
    root = os.path.dirname(os.path.dirname(__file__))  # go up from utils/
    esb = os.path.join(root, "bin", "esbuild")

    if not os.path.exists(esb):
        # fallback: try system-wide esbuild
        esb = shutil.which("esbuild") or esb

    cmd = [
        esb, entry,
        "--bundle", "--sourcemap",
        "--outfile=" + out
    ]

    print("⚡ Esbuild:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("✔ Esbuild bundled →", out)
