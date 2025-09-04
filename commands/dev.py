from __future__ import annotations
import asyncio, os
from pathlib import Path

from utils.esbuild import run as run_esbuild, detect_entry
from utils.server import start as start_server
from utils.watcher import watch
from utils.tailwind import watch_css, build_css

def run() -> None:
    """
    Start dev server, file watcher, and Tailwind watcher.
    """
    project = Path(os.getcwd())
    entry = detect_entry(str(project))
    dist = project / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    # Ensure CSS exists before the first page load
    build_css(str(project))

    # Initial JS bundle
    run_esbuild(entry, str(dist))

    async def _main() -> None:
        print("🚀 Dev server + Tailwind watching")
        tasks = [
            asyncio.create_task(start_server(str(dist))),
            asyncio.create_task(watch("src", lambda _: run_esbuild(entry, str(dist)))),
            asyncio.create_task(watch_css(str(project))),
        ]
        try:
            await asyncio.gather(*tasks)
        finally:
            for t in tasks:
                t.cancel()

    asyncio.run(_main())


if __name__ == "__main__":
    run()
