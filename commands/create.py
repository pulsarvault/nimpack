from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path
from importlib.resources import files  # stdlib

def run(flavor: str, name: str) -> None:
    # locate packaged templates
    tpl_root = files("commands._templates") / flavor  # reactjs | reactts
    if not tpl_root.is_dir():
        print(f"❌ PyPack: template not found: {flavor}")
        sys.exit(1)

    dest = Path(name).resolve()
    if dest.exists():
        print(f"❌ PyPack Project {name} already exists")
        sys.exit(1)

    shutil.copytree(tpl_root, dest)
    print(f"✔ 🐍🚀 PyPack Project created at {dest}")

    # npm bootstrap
    try:
        print("🐍🚀 Initializing PyPack project...")
        subprocess.run(["npm", "init", "-y"], cwd=dest, check=True)

        runtime = ["react", "react-dom"]
        # include esbuild here so users have the binary
        devdeps = ["esbuild", "tailwindcss", "@tailwindcss/cli"]
        if flavor == "reactts":
            devdeps += ["typescript", "@types/react", "@types/react-dom"]

        subprocess.run(["npm", "install", *runtime], cwd=dest, check=True)
        subprocess.run(["npm", "install", "-D", *devdeps], cwd=dest, check=True)
        print("✔ 🐍🚀 PyPack setup complete")
    except Exception as e:
        print("⚠️ PyPack setup failed:", e)
        print("   Run manually inside the project:")
        print("   npm init -y && npm i react react-dom")
        extra = " typescript @types/react @types/react-dom" if flavor == "reactts" else ""
        print(f"   npm i -D esbuild tailwindcss @tailwindcss/cli{extra}")

    print("🐍🚀 PyPack: Next steps")
    print(f"    cd {dest.name}")
    print("    pypack dev (or ../pypack dev) # 🐍🚀 Start the PyPack Dev Server")

