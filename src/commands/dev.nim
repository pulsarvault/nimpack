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
  runEsbuild(entry, distDir)   # initial build

  var store = ClientStore(sockets: @[])
  asyncCheck startServer(distDir, 3000, store)

  # ✅ Watch src/ and trigger rebuild + reload
  asyncCheck watchDir(projectDir / "src",
    proc(path: string) =
      runEsbuild(entry, distDir)
      asyncCheck notifyReload(store)
  )

  runForever()
