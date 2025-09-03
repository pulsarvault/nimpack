# 🐍🔥 PyPack (Rohit Chauhan)

A lightweight React project generator, dev server, and web bundler written in modern Python.  
Supports **JavaScript projects** with **esbuild bundling** and **SSE-based hot reload**.  

## 🚀 Features
- `create` → scaffold a new React app from template  
- `dev` → run local dev server with esbuild + hot reload  
- `build` → bundle app for production  

## 🛠 Prerequisites & Usage

- Python 3.10+ (tested on Python 3.13)  
- Node.js + npm (for React dependencies)  
- esbuild binary (included in `bin/` folder of repo)  

### Steps:

```bash
# 1. Install Python dependencies
pip install --user aiohttp watchfiles

# 2. Create a new project
./pypack.py create my-app --template js

# 3. Enter the project
cd my-app

# 4. Start the dev server
../pypack.py dev

# 5. Build for production
../pypack.py build
