# Rohit: src/commands/build.nim
import os, strutils
import ../utils/esbuild

proc buildProject*() =
  ## Run esbuild on current project
  echo "🔨 Building project with esbuild..."

  let projectDir = getCurrentDir()
  let entry = projectDir / "src" / "main.jsx"
  let distDir = projectDir / "dist"

  if not fileExists(entry):
    echo "Error: Could not find entry file at ", entry
    quit(1)

  createDir(distDir)

  # Call esbuild wrapper
  runEsbuild(entry, distDir)

  echo "✔ Build complete!"
  echo "Output in: ", distDir
