from __future__ import annotations
import asyncio, os, subprocess
from pathlib import Path
from typing import Tuple

from utils.server import notify_reload

def _cli() -> list[str]:
    return ["npx", "@tailwindcss/cli"]


def _paths(project: str) -> Tuple[Path, Path]:
    p = Path(project)
    src_css = p / "src" / "index.css"
    out_css = p / "dist" / "styles.css"
    return src_css, out_css


async def watch_css(project: str) -> None:
    src_css, out_css = _paths(project)
    out_css.parent.mkdir(parents=True, exist_ok=True)

    cmd = [*_cli(), "-i", str(src_css), "-o", str(out_css), "--watch"]
    print("🎨 Tailwind watch:", " ".join(cmd))

    proc = await asyncio.create_subprocess_exec(*cmd, cwd=project)

    last_mtime = out_css.stat().st_mtime if out_css.exists() else 0.0
    try:
        while True:
            await asyncio.sleep(0.5)
            if out_css.exists():
                mtime = out_css.stat().st_mtime
                if mtime != last_mtime:
                    last_mtime = mtime
                    print("🎨 Tailwind rebuilt → dist/styles.css (reload)")
                    await notify_reload()
            if proc.returncode is not None:
                print("⚠️ Tailwind CLI exited with code:", proc.returncode)
                break
    except asyncio.CancelledError:
        try:
            proc.terminate()
        except Exception:
            pass


def build_css(project: str) -> None:
    src_css, out_css = _paths(project)
    out_css.parent.mkdir(parents=True, exist_ok=True)
    cmd = [*_cli(), "-i", str(src_css), "-o", str(out_css)]
    print("🎨 Tailwind build:", " ".join(cmd))
    subprocess.run(cmd, cwd=project, check=True)
