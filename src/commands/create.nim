import os, osproc
import ../utils/fsutils

proc runCmd(cmd: string, cwd: string) =
  let (outp, exitCode) = execCmdEx(cmd, workingDir = cwd)
  if exitCode != 0:
    echo "❌ Command failed: ", cmd
    echo outp
    quit(1)
  else:
    if outp.len > 0: echo outp

proc createProject*(projectName: string, useTs: bool) =
  let projectPath = getCurrentDir() / projectName
  let templatePath =
    if useTs:
      getAppDir() / "templates" / "ts"
    else:
      getAppDir() / "templates" / "js"

  if dirExists(projectPath) or fileExists(projectPath):
    echo "❌ Project already exists: ", projectPath
    quit(1)

  echo "📂 Copying template from: ", templatePath
  copyDirRecursive(templatePath, projectPath)

  # ✅ Double-check: ensure index.html copied
  if not fileExists(projectPath / "index.html"):
    echo "❌ index.html missing after copy!"
    quit(1)

  echo "📦 Initializing npm..."
  if not fileExists(projectPath / "package.json"):
    runCmd("npm init -y", projectPath)

  echo "📦 Installing React dependencies..."
  runCmd("npm install react react-dom", projectPath)

  if useTs:
    echo "📦 Installing TypeScript + React types..."
    runCmd("npm install --save-dev typescript @types/react @types/react-dom", projectPath)

  echo "✔ Project created at ", projectPath
  echo "Next steps:"
  echo "  cd " & projectName
  echo "  nimpack dev"
