import os

proc copyDirRecursive*(src: string, dst: string) =
  ## Recursively copy directory and its contents using stdlib
  if not dirExists(src):
    echo "❌ Template not found: ", src
    quit(1)

  copyDir(src, dst)   # ✅ built-in handles both dirs + files
