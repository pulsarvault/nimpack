# Rohit: src/utils/fsutils.nim
import os

proc copyDirRecursive*(src: string, dst: string) =
  ## Recursively copy directory
  for kind, path in walkDir(src):
    let relative = relativePath(path, src)
    let target = dst / relative
    case kind:
    of pcDir: createDir(target)
    of pcFile: copyFile(path, target)
    else: discard

