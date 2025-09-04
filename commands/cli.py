from __future__ import annotations
import argparse, sys

from commands import create as create_cmd
from commands import dev as dev_cmd
from commands import build as build_cmd


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="pypack")
    sub = parser.add_subparsers(dest="command", required=True)

    pc = sub.add_parser("create", help="Create a new PyPack React Project")
    pc.add_argument("flavor", choices=["reactjs", "reactts"])
    pc.add_argument("name")

    sub.add_parser("dev", help="Run PyPack dev server")
    sub.add_parser("build", help="Build production bundle")

    args = parser.parse_args(argv or sys.argv[1:])

    if args.command == "create":
        create_cmd.run(args.flavor, args.name)
    elif args.command == "dev":
        dev_cmd.run()
    elif args.command == "build":
        build_cmd.run()

    return 0
