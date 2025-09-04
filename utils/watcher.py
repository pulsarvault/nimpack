from __future__ import annotations

import asyncio
from typing import Callable

from watchfiles import awatch     # ✅ this was missing
from utils.server import notify_reload


async def watch(path: str, on_change: Callable[[str], None]) -> None:
    async for changes in awatch(path):
        for _, changed in changes:
            print("🔄 File changed:", changed)
            on_change(changed)
            await notify_reload()
