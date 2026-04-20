import subprocess
from safedev.ui import info, success, error


def run_cmd(cmd):
    try:
        result = subprocess.run(cmd)
        return result.returncode == 0
    except FileNotFoundError:
        error("npm is not installed or not in PATH")
        return False


# 🔹 Install
def handle_npm(package):
    info("SafeDev NPM INSTALL")

    if not run_cmd(["npm", "install", package]):
        error("Installation failed")
        return

    success("Package installed successfully")


# 🔹 Uninstall
def uninstall_npm(package):
    info("NPM UNINSTALL")

    if not run_cmd(["npm", "uninstall", package]):
        error("Uninstall failed")
        return

    success("Package removed")


# 🔹 Upgrade
def upgrade_npm(package):
    info("NPM UPGRADE")

    if not run_cmd(["npm", "update", package]):
        error("Upgrade failed")
        return

    success("Package upgraded")