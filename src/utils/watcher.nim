import os, times, tables  # ✅ added tables

proc watchDir*(dir: string, onChange: proc(path: string)) =
  ## Naive file watcher: polls mtime every 1s
  var lastTimes: Table[string, Time] = initTable[string, Time]()

  while true:
    for kind, path in walkDir(dir, relative=false):
      if kind == pcFile:
        let modTime = getLastModificationTime(path)
        if not lastTimes.hasKey(path):
          lastTimes[path] = modTime
        elif lastTimes[path] != modTime:
          lastTimes[path] = modTime
          onChange(path)
    sleep(1000) # check every 1s
