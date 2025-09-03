import os, asyncdispatch
import ../utils/esbuild
import ../utils/server
import ../utils/watcher

proc devServer*() =
  echo "🚀 Starting dev server at http://localhost:3000"

  let projectDir = getCurrentDir()
  let entry = projectDir / "src" / "main.jsx"
  let distDir = projectDir / "dist"
  createDir(distDir)

  # Initial build
  runEsbuild(entry, distDir)

  # Create client store
  let store = ClientStore(sockets: @[])

  # Start HTTP + WS server
  asyncCheck startServer(distDir, 3000, store)

  # Watch src/ for changes
  watchDir(projectDir / "src",
    proc(path: string) =
      echo "🔄 File changed: ", path
      runEsbuild(entry, distDir)
      asyncCheck notifyReload(store)   # pass store explicitly
  )

  runForever()
