# -----------------------------------------
# Rohit: A simple TypeScript -> JavaScript transpiler
# Handles:
#   Removes type annotations (: string, : number, etc.)
#   Removes interface blocks
#   Removes type aliases (type X = something;)
# -----------------------------------------

import strutils, os

# Remove simple TypeScript type annotations from a single line
proc stripTypes(line: string): string =
  var result = line
  result = result.replace(": string", "")
  result = result.replace(": number", "")
  result = result.replace(": boolean", "")
  result = result.replace(": void", "")
  return result

# Main transpiler
proc transpile(tsCode: string): string =
  var output = newSeq[string]()
  var insideInterface = false

  for line in tsCode.splitLines():
    var trimmed = line.strip()

    # Skip interface blocks
    if trimmed.startsWith("interface"):
      insideInterface = true
      continue
    if insideInterface:
      if trimmed.startsWith("}"):
        insideInterface = false
      continue

    # Skip type aliases (e.g. type UserID = string;)
    if trimmed.startsWith("type "):
      continue

    # Process line normally
    output.add(stripTypes(line))

  return output.join("\n")

# Program entry point
when isMainModule:
  if paramCount() < 2:
    echo "Usage: nimpack input.ts output.js"
    quit(1)

  let inputFile = paramStr(1)
  let outputFile = paramStr(2)

  let tsCode = readFile(inputFile)
  let jsCode = transpile(tsCode)

  writeFile(outputFile, jsCode)
  echo "✅ Transpiled ", inputFile, " → ", outputFile
