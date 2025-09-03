import asynchttpserver, asyncdispatch
import std/[asyncnet, os]

# ✅ export both type and field
type ClientStore* = ref object
  sockets*: seq[AsyncSocket]

proc notifyReload*(store: ClientStore) {.async.} =
  for c in store.sockets:
    try:
      await c.send("reload\n")
    except:
      discard

proc startServer*(distDir: string, port: int, store: ClientStore) {.async.} =
  let server = newAsyncHttpServer()

  proc cb(req: Request) {.async, gcsafe.} =
    if req.url.path == "/livereload":
      let client = req.client
      store.sockets.add(client)
      return

    var relPath =
      if req.url.path.len > 0 and req.url.path[0] == '/':
        req.url.path[1..^1]
      else:
        req.url.path

    var path = distDir / relPath
    if req.url.path == "/":
      path = distDir / "index.html"

    if fileExists(path):
      await req.respond(Http200, readFile(path))
    else:
      await req.respond(Http404, "Not found")

  await server.serve(Port(port), cb)
