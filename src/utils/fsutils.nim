import os

proc copyDirRecursive*(src: string, dst: string) =
  ## Recursively copy directory (with files) using stdlib
  if not dirExists(src):
    echo "❌ Template not found: ", src
    quit(1)
  copyDir(src, dst)
