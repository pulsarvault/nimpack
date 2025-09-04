from __future__ import annotations
import asyncio
import contextlib
import shutil
import subprocess
from pathlib import Path


def detect_entry(project_dir: str) -> str:
    p = Path(project_dir)
    for name in ("main.tsx", "main.jsx"):
        cand = p / "src" / name
        if cand.exists():
            return str(cand)
    raise FileNotFoundError("No entry: src/main.tsx or src/main.jsx")


def _npx_cmd() -> list[str] | None:
    npx = shutil.which("npx")
    if not npx:
        return None
    try:
        subprocess.run(
            [npx, "-y", "esbuild", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return [npx, "-y", "esbuild"]
    except Exception:
        return None


def _path_cmd() -> list[str] | None:
    esb = shutil.which("esbuild")
    return [esb] if esb else None


def run(entry: str, dist: str, *, minify: bool = False, sourcemap: bool = True) -> None:
    out = Path(dist) / "bundle.js"
    cmd = _npx_cmd() or _path_cmd()
    if not cmd:
        raise RuntimeError("esbuild not found. Run: npm i -D esbuild")

    args = [entry, "--bundle", f"--outfile={out}"]
    if sourcemap and not minify:
        args.append("--sourcemap")
    if minify:
        args.append("--minify")

    full = [*cmd, *args]
    print("⚡ PyPack build:", " ".join(str(x) for x in full))
    subprocess.run(full, check=True)
    print("✔ PyPack build bundled →", out)


async def watch(entry: str, dist: str, on_rebuild) -> None:
    """
    Start esbuild in --watch (incremental).
    Call `await on_rebuild()` after each successful (re)build.
    """
    out = Path(dist) / "bundle.js"
    cmd = _npx_cmd() or _path_cmd()
    if not cmd:
        raise RuntimeError("PyPack: esbuild not found. Run: npm i -D esbuild")

    args = [
        entry,
        "--bundle",
        "--sourcemap",
        f"--outfile={out}",
        "--watch",
        "--color=false",
        "--log-level=info",
    ]

    proc = await asyncio.create_subprocess_exec(
        *[*cmd, *args],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    print("👀 PyPack Watch started")
    first_built_sent = False

    assert proc.stdout is not None
    try:
        while True:
            line = await proc.stdout.readline()
            if not line:
                await asyncio.sleep(0.05)
                if proc.returncode is not None:
                    print("⚠️ esbuild exited with code", proc.returncode)
                    break
                continue

            txt = line.decode("utf-8", errors="ignore").strip()
            if txt:
                print("esbuild:", txt)

            low = txt.lower()
            success = ("built " in low or "build finished" in low or "watching" in low) and "error" not in low
            if success:
                if not first_built_sent:
                    first_built_sent = True
                    await on_rebuild()
                elif "built " in low or "build finished" in low:
                    await on_rebuild()
    except asyncio.CancelledError:
        with contextlib.suppress(Exception):
            proc.terminate()
        raise
