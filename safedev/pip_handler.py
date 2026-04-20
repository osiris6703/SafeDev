import subprocess
import shutil
import os
import time
from tqdm import tqdm

from safedev.scanner import scan_files
from safedev.risk import calculate_risk
from safedev.ui import info, success, error, warning, show_risk
from safedev.typo import check_typosquat
from safedev.trust import is_trusted

TEMP_DIR = "temp"


# 🔥 DOWNLOAD PROGRESS
def get_folder_size(folder):
    total = 0
    for root, _, files in os.walk(folder):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except:
                pass
    return total


def download_with_progress(package, temp_dir):
    proc = subprocess.Popen(
        ["pip", "download", package, "-d", temp_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    bar = tqdm(
        unit="B",
        unit_scale=True,
        desc="Downloading",
        ncols=80
    )

    last_size = 0

    while proc.poll() is None:
        size = get_folder_size(temp_dir)
        bar.update(size - last_size)
        last_size = size
        time.sleep(0.2)

    size = get_folder_size(temp_dir)
    bar.update(size - last_size)
    bar.close()

    return proc.returncode


# 🔥 MAIN HANDLER
def handle_pip(package):
    info("SafeDev PIP INSTALL")

    # ✅ 1. TYPO CHECK (BEFORE DOWNLOAD)
    flag, suggestion = check_typosquat(package)

    if flag:
        print()

        if suggestion:
            choice = input(f"Did you mean '{suggestion}'? Install it instead? (y/n): ").lower()

            if choice == "y":
                package = suggestion
            else:
                confirm = input(f"Install '{package}' anyway? (y/n): ").lower()
                if confirm != "y":
                    error("Installation cancelled")
                    return
        else:
            confirm = input("Suspicious package name. Continue? (y/n): ").lower()
            if confirm != "y":
                error("Installation cancelled")
                return

    # ✅ 2. TRUST CHECK
    trusted = is_trusted(package)
    if trusted:
        success("Trusted package (community verified)")

    # ✅ 3. CLEAN TEMP
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # ✅ 4. DOWNLOAD
    info("Downloading package...")
    code = download_with_progress(package, TEMP_DIR)

    if code != 0:
        error("Download failed — check package name or internet")
        return

    # ✅ 5. SCAN
    info("Analyzing package...")
    findings = scan_files(TEMP_DIR)
    score = calculate_risk(findings)

    if trusted and score < 30:
        score = score // 2

    # ✅ 6. SHOW RISK
    show_risk(score)

    # ✅ 7. FINAL CONFIRM
    choice = input("\nInstall anyway? (y/n): ").lower()

    if choice != "y":
        error("Installation cancelled")
        return

    success("Installing package...")
    subprocess.run(["pip", "install", package])


# 🔹 UNINSTALL
def uninstall_pip(package):
    info("PIP UNINSTALL")
    subprocess.run(["pip", "uninstall", package, "-y"])


# 🔹 UPGRADE
def upgrade_pip(package):
    info("PIP UPGRADE")
    subprocess.run(["pip", "install", "--upgrade", package])