import asynchttpserver, asyncdispatch, asyncnet

let server = newAsyncHttpServer()

proc cb(req: Request) {.async.} =
  echo "🌐 Request: ", req.url.path

  if req.url.path == "/events":
    # Build SSE headers
    let headers = "HTTP/1.1 200 OK\r\n" &
                  "Content-Type: text/event-stream\r\n" &
                  "Cache-Control: no-cache\r\n" &
                  "Connection: keep-alive\r\n\r\n"

    # ✅ Send headers to client
    await req.client.send(headers)

    echo "🔌 SSE client connected"

    # Send events every 5 seconds
    while true:
      try:
        await req.client.send("data: hello from Nim!\n\n")
      except:
        echo "❌ SSE client disconnected"
        break
      await sleepAsync(5000)
    return

  await req.respond(Http200, "Go to /events for SSE")

waitFor server.serve(Port(3000), cb)
