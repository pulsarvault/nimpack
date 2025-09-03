import std/[os, times, asyncdispatch, tables]

proc watchDir*(dir: string, onChange: proc(path: string)) {.async.} =
  ## Portable polling watcher (works even without std/watchevents)
  var lastTimes = initTable[string, Time]()

  while true:
    for path in walkDirRec(dir):   # walk returns only path
      if fileExists(path):
        let modTime = getLastModificationTime(path)
        if path notin lastTimes or lastTimes[path] != modTime:
          lastTimes[path] = modTime
          echo "🔄 File change detected: ", path
          onChange(path)
    await sleepAsync(1000)   # poll every 1s
