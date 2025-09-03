import asynchttpserver, asyncdispatch, asyncnet
import std/[os, strutils]

type ClientStore* = ref object
  sockets*: seq[AsyncSocket]

proc notifyReload*(store: ClientStore) {.async.} =
  ## Broadcast reload event to all connected browsers
  for c in store.sockets:
    try:
      await c.send("data: reload\n\n")
    except:
      discard

proc getMimeType(path: string): string =
  if path.endsWith(".html"): return "text/html"
  if path.endsWith(".js") or path.endsWith(".mjs") or path.endsWith(".jsx") or path.endsWith(".tsx"):
    return "application/javascript"
  if path.endsWith(".css"): return "text/css"
  if path.endsWith(".json"): return "application/json"
  if path.endsWith(".ico"): return "image/x-icon"
  if path.endsWith(".png"): return "image/png"
  if path.endsWith(".jpg") or path.endsWith(".jpeg"): return "image/jpeg"
  return "text/plain"

proc startServer*(distDir: string, port: int, store: ClientStore) {.async.} =
  let server = newAsyncHttpServer()
  let projectRoot = parentDir(distDir)

  proc cb(req: Request) {.async, gcsafe.} =
    echo "🌐 Request: ", req.url.path

    if req.url.path == "/livereload":
      # ⚡ Use exact same SSE pattern as in sse_test.nim
      let headers = "HTTP/1.1 200 OK\r\n" &
                    "Content-Type: text/event-stream\r\n" &
                    "Cache-Control: no-cache\r\n" &
                    "Connection: keep-alive\r\n\r\n"

      await req.client.send(headers)
      await req.client.send(":\n\n") # initial keep-alive

      store.sockets.add(req.client)
      echo "🔌 Livereload client connected"

      proc keepAlive(c: AsyncSocket) {.async.} =
        while true:
          try:
            await c.send(":\n\n")
          except:
            break
          await sleepAsync(15000)

      asyncCheck keepAlive(req.client)
      return

    if req.url.path == "/":
      let indexPath = projectRoot / "index.html"
      if fileExists(indexPath):
        let html = readFile(indexPath)
        await req.respond(Http200, html, newHttpHeaders({"Content-Type": "text/html"}))
      else:
        await req.respond(Http404, "index.html missing")
      return

    var relPath =
      if req.url.path.len > 0 and req.url.path[0] == '/':
        req.url.path[1..^1]
      else:
        req.url.path

    let assetPath = distDir / relPath
    if fileExists(assetPath):
      let mime = getMimeType(assetPath)
      await req.respond(Http200, readFile(assetPath), newHttpHeaders({"Content-Type": mime}))
    else:
      await req.respond(Http404, "Not found: " & req.url.path)

  echo "🚀 Dev server running on http://localhost:" & $port
  asyncCheck server.serve(Port(port), cb, address = "0.0.0.0")
  runForever()
