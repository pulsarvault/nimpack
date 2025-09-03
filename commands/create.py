import os, shutil, subprocess

def run(name: str, template: str):
    base = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(base, ".."))
    tpl = os.path.join(root, "templates", template)

    dest = os.path.abspath(name)
    if os.path.exists(dest):
        print(f"❌ Project {name} already exists")
        return

    shutil.copytree(tpl, dest)
    print(f"✔ Project created at {dest}")

    # Post-create: npm init + install react/react-dom
    try:
        print("📦 Initializing npm project...")
        subprocess.run(["npm", "init", "-y"], cwd=dest, check=True)

        print("📦 Installing React + ReactDOM...")
        subprocess.run(["npm", "install", "react", "react-dom"], cwd=dest, check=True)

        print("✔ npm setup complete")
    except Exception as e:
        print("⚠️ npm setup failed:", e)
        print("   You can run it manually inside the project:")
        print("     npm init -y && npm install react react-dom")

    print("Next steps:")
    print(f"  cd {name}")
    print(f"  ../pypack dev")
