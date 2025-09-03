#!/usr/bin/env python3
import sys, os

# Make vendored deps importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

import argparse
from commands import create, build, dev

def main():
    parser = argparse.ArgumentParser(prog="pypack", description="React project builder")
    sub = parser.add_subparsers(dest="command")

    # create
    p_create = sub.add_parser("create", help="Create a new React project")
    p_create.add_argument("name", help="Project name")
    p_create.add_argument("--template", choices=["js", "ts"], default="js")

    # build
    sub.add_parser("build", help="Build for production")

    # dev
    sub.add_parser("dev", help="Run dev server with hot reload")

    args = parser.parse_args()

    if args.command == "create":
        create.run(args.name, args.template)
    elif args.command == "build":
        build.run()
    elif args.command == "dev":
        dev.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
