TRUSTED_PACKAGES = [
    "django", "flask", "numpy", "pandas", "requests", "torch"
]

def is_trusted(pkg):
    return pkg.lower() in TRUSTED_PACKAGES