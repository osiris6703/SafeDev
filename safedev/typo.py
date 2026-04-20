from safedev.ui import warning
import difflib

KNOWN_PACKAGES = [
    "torch",
    "tensorflow",
    "django",
    "numpy",
    "pandas",
    "requests",
    "colorama",
    "huggingface_hub"
]

KNOWN_CONFUSIONS = {
    "pytorch": "torch",
    "hugingface": "huggingface_hub",
    "colourama": "colorama"
}


def check_typosquat(pkg):
    pkg = pkg.lower()

    # Direct known mistakes
    if pkg in KNOWN_CONFUSIONS:
        correct = KNOWN_CONFUSIONS[pkg]
        warning(f"'{pkg}' is incorrect. Did you mean '{correct}'?")
        return True, correct

    # Fuzzy matching
    match = difflib.get_close_matches(pkg, KNOWN_PACKAGES, n=1, cutoff=0.75)

    if match and match[0] != pkg:
        warning(f"'{pkg}' looks similar to '{match[0]}'")
        return True, match[0]

    return False, None