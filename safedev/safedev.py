#!/usr/bin/env python3
import argparse
from safedev.pip_handler import handle_pip
from safedev.npm_handler import handle_npm
from safedev.git_handler import handle_git

parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("target")
parser.add_argument("--npm", action="store_true")

args = parser.parse_args()

if args.command == "install":
    if args.npm:
        handle_npm(args.target)
    else:
        handle_pip(args.target)

elif args.command == "clone":
    handle_git(args.target)
