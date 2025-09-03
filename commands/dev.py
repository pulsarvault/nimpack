import os, asyncio, subprocess
from utils import esbuild, server, watcher

def run():
    project = os.getcwd()
    entry = os.path.join(project, "src", "main.jsx")
    dist = os.path.join(project, "dist")
    os.makedirs(dist, exist_ok=True)

    # Initial build
    esbuild.run(entry, dist)

    # Start dev server + watcher
    loop = asyncio.get_event_loop()
    loop.create_task(server.start(dist))
    loop.create_task(watcher.watch("src", lambda _: esbuild.run(entry, dist)))
    loop.run_forever()
