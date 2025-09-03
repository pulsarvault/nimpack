import os, subprocess

def run():
    project = os.getcwd()
    entry = os.path.join(project, "src", "main.jsx")
    dist = os.path.join(project, "dist")
    os.makedirs(dist, exist_ok=True)

    out = os.path.join(dist, "bundle.js")

    cmd = [
        "./bin/esbuild", entry,
        "--bundle", "--sourcemap",
        "--outfile=" + out
    ]

    print("⚡ Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("✔ Esbuild bundled →", out)
