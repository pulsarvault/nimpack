from __future__ import annotations
import asyncio
from aiohttp import web

clients: set[web.StreamResponse] = set()


async def handle_root(request: web.Request) -> web.StreamResponse:
    return web.FileResponse("index.html")


async def handle_assets(request: web.Request) -> web.StreamResponse:
    # Serves /bundle.js and /styles.css from ./dist/
    path = "dist" + request.path
    return web.FileResponse(path)


async def handle_reload(request: web.Request) -> web.StreamResponse:
    resp = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
    await resp.prepare(request)
    clients.add(resp)
    print("🔌 Livereload client connected")

    try:
        while True:
            await asyncio.sleep(15)
            try:
                await resp.write(b": keep-alive\n\n")
            except (ConnectionResetError, asyncio.CancelledError, BrokenPipeError):
                print("❌ Client disconnected from livereload")
                break
    finally:
        clients.discard(resp)

    return resp


async def start(dist: str) -> None:
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/livereload", handle_reload)
    app.router.add_get("/bundle.js", handle_assets)
    app.router.add_get("/styles.css", handle_assets)
    app.router.add_static("/dist/", path=dist, show_index=False)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 3000)
    await site.start()
    print("🐍🚀 PyPack Dev server running at http://localhost:3000")


async def notify_reload() -> None:
    for resp in list(clients):
        try:
            # named event + generic message (supports both client styles)
            await resp.write(b"event: reload\ndata: ok\n\n")
            await resp.write(b"data: reload\n\n")
        except Exception:
            pass


async def notify_css(name: str = "styles.css") -> None:
    for resp in list(clients):
        try:
            await resp.write(f"event: css\ndata: {name}\n\n".encode())
        except Exception:
            pass
