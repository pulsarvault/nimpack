from __future__ import annotations
import asyncio
import os
from pathlib import Path

from utils.esbuild import detect_entry, run as run_esbuild, watch as watch_esbuild
from utils.server import start as start_server, notify_reload
from utils.tailwind import watch_css, build_css
from utils.watcher import watch


def run() -> None:
    project = Path(os.getcwd())
    entry = detect_entry(str(project))
    dist = project / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    # Ensure CSS exists for first paint
    build_css(str(project))
    # Initial JS bundle before starting watch
    run_esbuild(entry, str(dist))

    def _html_changed(_p: str) -> None:
        # schedule notify_reload from sync callback
        asyncio.get_event_loop().create_task(notify_reload())

    async def _main() -> None:
        print("🚀 PyPack Dev server + React + Tailwind + Watch")
        async def on_js_rebuild() -> None:
            await notify_reload()

        tasks = [
            asyncio.create_task(start_server(str(dist))),
            asyncio.create_task(watch_esbuild(entry, str(dist), on_js_rebuild)),
            asyncio.create_task(watch_css(str(project))),
            asyncio.create_task(watch("index.html", _html_changed)),
        ]
        try:
            await asyncio.gather(*tasks)
        finally:
            for t in tasks:
                t.cancel()

    asyncio.run(_main())


if __name__ == "__main__":
    run()
