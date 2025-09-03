import os, osproc
import ../utils/fsutils

proc runCmd(cmd: string, cwd: string) =
  ## Run a shell command inside a given directory
  let (outp, exitCode) = execCmdEx(cmd, workingDir = cwd)
  if exitCode != 0:
    echo "❌ Command failed: ", cmd
    echo outp
    quit(1)
  else:
    echo outp

proc createProject*(projectName: string, useTs: bool) =
  ## Create a new React project from Nimpack templates
  let projectPath = getCurrentDir() / projectName
  let templatePath =
    if useTs:
      getAppDir() / "templates" / "ts"
    else:
      getAppDir() / "templates" / "js"

  if dirExists(projectPath) or fileExists(projectPath):
    echo "❌ Project already exists: ", projectPath
    quit(1)

  # Copy template
  echo "📂 Copying template from: ", templatePath
  copyDirRecursive(templatePath, projectPath)

  # ✅ Post-create: setup npm
  echo "📦 Initializing npm..."
  if not fileExists(projectPath / "package.json"):
    runCmd("npm init -y", projectPath)

  echo "📦 Installing React dependencies..."
  runCmd("npm install react react-dom", projectPath)

  echo "✔ Project created at ", projectPath
  echo "Next steps:"
  echo "  cd " & projectName
  echo "  nimpack dev"
