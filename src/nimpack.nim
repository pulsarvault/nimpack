# Rohit: Entry point for Nimpack CLI
import os, strutils
import cli

when isMainModule:
  # Forward args to our CLI handler
  cli.runCommandLine()
