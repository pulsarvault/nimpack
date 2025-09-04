from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path   # ✅ this was missing

def run(flavor: str, name: str) -> None:
    root = Path(__file__).resolve().parents[1]
    tpl = root / "templates" / flavor
    dest = Path(name).resolve()

    if dest.exists():
        print(f"❌ PyPack Project {name} already exists")
        sys.exit(1)

    shutil.copytree(tpl, dest)
    print(f"✔ PyPack Project created at {dest}")

    try:
        print("📦 Initializing PyPack project...")
        subprocess.run(["npm", "init", "-y"], cwd=dest, check=True)

        runtime = ["react", "react-dom"]
        devdeps = ["esbuild", "tailwindcss", "@tailwindcss/cli"]

        if flavor == "reactts":
            devdeps += ["typescript", "@types/react", "@types/react-dom"]

        print("📦 PyPack: Installing runtime deps:", " ".join(runtime))
        subprocess.run(["npm", "install", *runtime], cwd=dest, check=True)

        print("📦 PyPack: Installing dev deps:", " ".join(devdeps))
        subprocess.run(["npm", "install", "-D", *devdeps], cwd=dest, check=True)

        print("✔ PyPack setup complete")
    except Exception as e:
        print("⚠️ PyPack setup failed:", e)
        print("   Run manually inside the project:")
        print("   npm init -y && npm i react react-dom")
        extra = " typescript @types/react @types/react-dom" if flavor == "reactts" else ""
        print(f"   npm i -D tailwindcss @tailwindcss/cli{extra}")

    print("PyPack: Next steps:")
    print(f"  cd {dest.name}")
    print("  ../pypack dev   # start dev server (React + Tailwind)")
