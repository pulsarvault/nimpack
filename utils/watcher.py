from watchfiles import awatch
import asyncio
from utils import server

async def watch(path: str, on_change):
    async for changes in awatch(path):
        for _, changed in changes:
            print("🔄 File changed:", changed)
            on_change(changed)
            await server.notify_reload()
