import subprocess
from safedev.scanner import scan_files
from safedev.risk import calculate_risk
from safedev.ui import info, success, error

def handle_git(repo):
    info("GIT MODE")

    subprocess.run(["git", "clone", repo, "repo_temp"])

    findings = scan_files("repo_temp")
    score = calculate_risk(findings)

    info(f"Risk Score: {score}/100")

    if score > 50:
        error("Blocked: High risk repo")
        return

    success("Repository is safe")