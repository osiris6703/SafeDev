import argparse
from .pip_handler import handle_pip, uninstall_pip, upgrade_pip
from .npm_handler import handle_npm, uninstall_npm, upgrade_npm
from .git_handler import handle_git
from .ui import banner

def cli():
    banner()

    parser = argparse.ArgumentParser(prog="safedev")
    parser.add_argument("command")
    parser.add_argument("target")
    parser.add_argument("--npm", action="store_true")

    args = parser.parse_args()

    if args.command == "install":
        if args.npm:
            handle_npm(args.target)
        else:
            handle_pip(args.target)

    elif args.command == "uninstall":
        if args.npm:
            uninstall_npm(args.target)
        else:
            uninstall_pip(args.target)

    elif args.command == "upgrade":
        if args.npm:
            upgrade_npm(args.target)
        else:
            upgrade_pip(args.target)

    elif args.command == "clone":
        handle_git(args.target)