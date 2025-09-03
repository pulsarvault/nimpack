import os
import ../utils/esbuild

proc buildProject*() =
  ## Build project for production
  let projectDir = getCurrentDir()
  let entry = projectDir / "src" / "main.jsx"
  let distDir = projectDir / "dist"

  createDir(distDir)

  echo "⚡ Building production bundle..."
  runEsbuild(entry, distDir, prod = true)

  # ✅ Copy index.html into dist
  let srcHtml = projectDir / "index.html"
  let dstHtml = distDir / "index.html"
  if fileExists(srcHtml):
    copyFile(srcHtml, dstHtml)
    echo "✔ Copied index.html → dist/"
  else:
    echo "❌ No index.html found at project root: ", srcHtml

  echo "🎉 Production build ready at: ", distDir
