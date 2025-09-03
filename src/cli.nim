# Rohit: src/cli.nim
import os, strutils
import commands/create
import commands/build
import commands/dev

proc runCommandLine*() =
  let args = commandLineParams()

  if args.len == 0:
    echo "Usage: nimpack <command> [options]"
    echo "Commands:"
    echo "  create <project-name> [--ts]   Create new React project"
    echo "  build                          Bundle project with esbuild"
    echo "  dev                            Run dev server with hot reload"
    quit(1)

  let command = args[0]

  case command:
  of "create":
    if args.len < 2:
      echo "Please provide a project name"
      quit(1)
    let projectName = args[1]
    let useTs = args.find("--ts") != -1
    createProject(projectName, useTs)

  of "build":
    buildProject()

  of "dev":
    devServer()

  else:
    echo "Unknown command: ", command
