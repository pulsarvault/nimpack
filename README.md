# 📦 Pypack (Rohit Chauhan)

A lightweight, React project generator, dev server, web bundler written in modern Python.  
Supports **JavaScript projects** with **esbuild bundling** and **SSE-based hot reload**.  

## 🚀 Features
- `create` → scaffold a new React app from template  
- `dev` → run local dev server with esbuild + hot reload  
- `build` → bundle app for production  

## 🛠 Prerequisites
- Python 3.10+ (tested on Python 3.13)  
- Node.js + npm (for React dependencies)  
- esbuild binary (included in `bin/` folder of repo)  

Install Python dependencies once:
```bash
pip install --user aiohttp watchfiles

# 📦 Pypack usage:
Install Python dependencies once:
```bash
./pypack.py create my-app --template js
cd my-app
../pypack.py dev
../pypack.py build
