# Rohit: src/commands/create.nim
import os, strutils
import ../utils/fsutils

proc createProject*(name: string, useTs: bool) =
  echo "Creating React project: ", name
  let projectPath = getCurrentDir() / name

  if dirExists(projectPath):
    echo "Error: Directory already exists!"
    quit(1)

  createDir(projectPath)

  # Copy base template
  let templatePath = if useTs: "templates/ts" else: "templates/js"
  copyDirRecursive(templatePath, projectPath)

  echo "✔ Project created at ", projectPath
  echo "Next steps:"
  echo "  cd ", name
  echo "  nimpack dev     # (later will run dev server)"
