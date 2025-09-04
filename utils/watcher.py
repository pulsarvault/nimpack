from __future__ import annotations
import asyncio
from typing import Callable
from watchfiles import awatch

# Generic async watcher that calls a SYNC callback you pass in
async def watch(path: str, on_change: Callable[[str], None]) -> None:
    debounce_ms = 150
    async for changes in awatch(path):
        await asyncio.sleep(debounce_ms / 1000)  # coalesce bursts
        # pick any changed path and invoke sync callback off-thread
        changed_path = next(iter(changes))[1]
        print("🔄 PyPack: File changed:", changed_path)
        await asyncio.to_thread(on_change, changed_path)
