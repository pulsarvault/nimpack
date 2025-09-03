import os, osproc

proc runEsbuild*(entry: string, outdir: string; prod = false) =
  let esbuildPath =
    if fileExists(getAppDir() / "bin" / "esbuild"):
      getAppDir() / "bin" / "esbuild"
    elif fileExists("bin" / "esbuild"):
      getCurrentDir() / "bin" / "esbuild"
    else:
      "esbuild"

  createDir(outdir)

  var cmd = esbuildPath & " " & entry &
    " --bundle" &
    " --outfile=" & (outdir / "bundle.js") &
    " --loader:.js=jsx --loader:.jsx=jsx" &
    " --loader:.ts=ts --loader:.tsx=tsx" &
    " --jsx=automatic --format=esm" &
    " --platform=browser --target=esnext"

  if prod:
    cmd &= " --minify"

  let (outp, exitCode) = execCmdEx(cmd)
  if exitCode != 0:
    echo "❌ Esbuild failed:\n", outp
  else:
    if outp.len > 0: echo outp
    echo "✔ Esbuild bundled → " & outdir / "bundle.js"
