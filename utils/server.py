from aiohttp import web
import asyncio

clients = set()

async def handle_root(request):
    return web.FileResponse("index.html")

async def handle_assets(request):
    path = "dist" + request.path
    return web.FileResponse(path)

async def handle_reload(request):
    resp = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
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


async def start(dist):
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/bundle.js", handle_assets)
    app.router.add_get("/livereload", handle_reload)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 3000)
    await site.start()
    print("🚀 Dev server running at http://localhost:3000")

async def notify_reload():
    for resp in list(clients):
        try:
            await resp.write(b"data: reload\n\n")
        except:
            pass
