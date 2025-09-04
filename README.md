# 🐍🔥 PyPack (Rohit Chauhan)

A React + Tailwind Project Generator, Dev Server, and Web Bundler written in modern Python.  
Supports **JavaScript and TypeScript projects with Tailwind support**, **fast-server**, **hot-reload**, **web-bundler**.  

---

## 🚀 Features
- `create` → create a new React app  
- `dev` → run local dev server with hot reload  
- `build` → bundle app for production  

---

## 🛠 Prerequisites & Usage

- Python 3.10+ (tested on Python 3.13)  
- Node.js + npm (for React dependencies) 

### Steps:

```bash
# 1. Install PyPack
pip install pypackx

# 2. Create a new project (Tailwind configured by default)
pypack create reactjs my-app     # JavaScript
pypack create reactts my-app     # TypeScript

# 3. Enter the project
cd my-app

# 4. Start the dev server with hot reload
pypack dev

# 5. Build for production
pypack build

# 📜 License: MIT © Rohit Chauhan
