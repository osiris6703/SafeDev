import json
import os
import re
import ast
import zipfile
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from safedev.ui import info, box

# Load rules
rules_path = os.path.join(os.path.dirname(__file__), "rules.json")

with open(rules_path, encoding="utf-8") as f:
    rules_data = json.load(f)["rules"]


# 🔥 Extract archives
def extract_archives(path):
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".whl") or f.endswith(".zip"):
                full_path = os.path.join(root, f)
                extract_dir = full_path + "_extracted"

                if not os.path.exists(extract_dir):
                    try:
                        with zipfile.ZipFile(full_path, "r") as zip_ref:
                            zip_ref.extractall(extract_dir)
                    except:
                        pass


# 🔥 AST scan (ONLY REAL RISKS)
# NOTE: rule_ids deliberately match regex rules so dedup collapses overlaps.
#       Severities match rules.json values to prevent score inflation.
def ast_scan(file_path):
    findings = []

    if not file_path.endswith(".py"):
        return findings

    try:
        with open(file_path, "r", errors="ignore") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):
                func_name = ""

                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                # eval → SD-001 (sev 3), exec → SD-002 (sev 3)
                # Same IDs as regex rules so (rule_id, name) dedup removes duplicates.
                if func_name == "eval":
                    findings.append({
                        "rule_id": "SD-001",
                        "name": "Suspicious eval() with dangerous content",
                        "severity": 3,
                        "file": file_path,
                        "description": "Use of eval() detected via AST",
                        "advice": "Decode or inspect what is being passed to eval()."
                    })

                elif func_name == "exec":
                    findings.append({
                        "rule_id": "SD-002",
                        "name": "Dynamic code execution \u2014 exec()",
                        "severity": 3,
                        "file": file_path,
                        "description": "Use of exec() detected via AST",
                        "advice": "Check what string is being passed to exec()."
                    })

                # Shell calls → SD-005 (sev 3)
                elif func_name in ["system", "popen", "run", "call", "check_output"]:
                    findings.append({
                        "rule_id": "SD-005",
                        "name": "Shell command execution",
                        "severity": 3,
                        "file": file_path,
                        "description": "Shell command execution detected via AST",
                        "advice": "Verify what command is being run and whether user input can influence it."
                    })

    except:
        pass

    return findings


# 🔥 Regex matching
def match_rule(rule, file_path, content):
    matches = []

    if rule["file_types"] != ["*"]:
        if not any(file_path.endswith(ext) for ext in rule["file_types"]):
            return matches

    if rule["type"] == "filename":
        if re.search(rule["pattern"], os.path.basename(file_path)):
            matches.append(rule)

    elif rule["type"] == "regex":
        if re.search(rule["pattern"], content):
            matches.append(rule)

    return matches


# 🔥 Scan file
def scan_file(file_path):
    findings = []

    try:
        with open(file_path, errors="ignore") as f:
            content = f.read()

        # Regex rules
        for rule in rules_data:
            results = match_rule(rule, file_path, content)
            for r in results:
                findings.append({
                    "file": file_path,
                    "rule_id": r["id"],
                    "severity": r["severity"],
                    "name": r["name"],
                    "description": r["description"],
                    "advice": r["advice"]
                })

        # AST rules (rule_ids match regex counterparts — dedup handles overlap)
        findings.extend(ast_scan(file_path))

    except:
        pass

    return findings


# 🔥 MAIN SCAN
def scan_files(path):
    extract_archives(path)

    info("Analyzing package...")

    all_files = []
    for root, _, files in os.walk(path):
        for f in files:
            all_files.append(os.path.join(root, f))

    findings = []

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(tqdm(ex.map(scan_file, all_files), total=len(all_files)))

        for r in results:
            findings.extend(r)

    # 🔥 REMOVE LOW NOISE
    findings = [f for f in findings if f["severity"] >= 3]

    # 🔥 DEDUPLICATE by (rule_id, name) — AST + regex overlaps collapse here
    unique = {}
    for f in findings:
        key = (f["rule_id"], f["name"])
        unique[key] = f

    findings = list(unique.values())

    # 🔥 DISPLAY
    if findings:
        lines = []

        for f in findings:
            lines.append(f"\u26a0 {f['name']} (Severity {f['severity']})")
            lines.append(f"\u2192 {f['description']}")
            lines.append(f"\u2714 Fix: {f['advice']}")
            lines.append("")

        box("SECURITY FINDINGS", lines)

    else:
        box("SECURITY FINDINGS", ["\u2714 No significant threats detected"])

    return findings