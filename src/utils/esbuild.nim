# Rohit: src/utils/esbuild.nim
import osproc, strutils, os

proc runEsbuild*(entry: string, outDir: string) =
  ## Call esbuild binary to bundle React app
  ## Example:
  ## esbuild src/main.jsx --bundle --outfile=dist/bundle.js --format=esm

  let esbuildPath =
    if fileExists("bin" / "esbuild"): getCurrentDir() / "bin" / "esbuild"
    else: "esbuild"  # fallback if globally installed

  let outfile = outDir / "bundle.js"

  let args = [
    entry,
    "--bundle",
    "--outfile=" & outfile,
    "--format=esm",
    "--loader:.js=jsx",
    "--loader:.jsx=jsx",
    "--loader:.ts=tsx",
    "--loader:.tsx=tsx"
  ]

  # Run esbuild with full command string
  let (outp, code) = execCmdEx(esbuildPath & " " & args.join(" "))

  if code != 0:
    echo "❌ Esbuild failed:"
    echo outp
    quit(1)

  # Create basic index.html if not exists
  let htmlPath = outDir / "index.html"
  if not fileExists(htmlPath):
    writeFile(htmlPath, """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Nimpack App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./bundle.js"></script>
  </body>
</html>
""")
