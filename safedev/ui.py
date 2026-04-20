from colorama import Fore, Back, Style, init
init(autoreset=True)

W = 84  # box width


def banner():
    print()
    print(Fore.CYAN + Style.BRIGHT + f"  ╔{'═' * (W - 2)}╗")
    print(Fore.CYAN + Style.BRIGHT + f"  ║{' ' * (W - 2)}║")
    print(Fore.CYAN  + Style.BRIGHT + f"  ║" +
          Fore.WHITE  + Style.BRIGHT + f"{'SAFE':>28}" +
          Fore.GREEN  + Style.BRIGHT + f"{'DEV':<26}" +
          Fore.CYAN   + Style.BRIGHT + "║")
    print(Fore.CYAN + Style.BRIGHT +
          f"  ║" + Style.DIM + Fore.WHITE +
          "    ─── Security Scanner v1.0 ───    ".center(W - 2) +
          Fore.CYAN + Style.NORMAL + "║")
    print(Fore.CYAN + Style.BRIGHT + f"  ║{' ' * (W - 2)}║")
    print(Fore.CYAN + Style.BRIGHT + f"  ╚{'═' * (W - 2)}╝")
    print()


def info(msg):
    print(Fore.CYAN + Style.BRIGHT + "  ●" + Style.RESET_ALL +
          Fore.WHITE + f"  {msg}")


def success(msg):
    print(Fore.GREEN + Style.BRIGHT + "  ✔" + Style.RESET_ALL +
          Fore.GREEN + f"  {msg}")


def warning(msg):
    print(Fore.YELLOW + Style.BRIGHT + "  ▲" + Style.RESET_ALL +
          Fore.YELLOW + f"  {msg}")


def error(msg):
    print(Fore.RED + Style.BRIGHT + "  ✖" + Style.RESET_ALL +
          Fore.RED + f"  {msg}")


def box(title, lines):
    inner = W - 4
    title_str = f"  {title}  "
    left  = (W - len(title_str)) // 2
    right = W - left - len(title_str)

    print()
    print(Fore.MAGENTA + Style.BRIGHT +
          f"  ╭{'─' * left}" + Fore.WHITE + Style.BRIGHT + title_str +
          Fore.MAGENTA + f"{'─' * right}╮")

    for line in lines:
        display = line[:inner].ljust(inner)
        print(Fore.MAGENTA + "  │ " +
              Style.RESET_ALL + Fore.WHITE + display +
              Fore.MAGENTA + " │")

    print(Fore.MAGENTA + Style.BRIGHT + f"  ╰{'─' * (W - 2)}╯")
    print()


def show_risk(score):
    bar_len = 36
    filled  = int(score / 100 * bar_len)
    empty   = bar_len - filled

    if score == 0:
        colour, label, icon = Fore.GREEN,  "SAFE",   "●"
    elif score < 30:
        colour, label, icon = Fore.GREEN,  "LOW",    "●"
    elif score < 60:
        colour, label, icon = Fore.YELLOW, "MEDIUM", "◉"
    else:
        colour, label, icon = Fore.RED,    "HIGH",   "⬤"

    bar = (colour + ("█" * filled) +
           Style.DIM + Fore.WHITE + ("░" * empty) + Style.RESET_ALL)

    print()
    print(Fore.WHITE + Style.BRIGHT + f"  ╭{'─' * (W - 2)}╮")
    print(Fore.WHITE + "  │" +
          colour + Style.BRIGHT + f"  {icon}  RISK SCORE".ljust(20) +
          colour + Style.BRIGHT + f"{score:>3}/100" +
          Fore.WHITE + Style.DIM + f"  [{label}]".ljust(12) +
          Fore.WHITE + Style.BRIGHT + "│")
    print(Fore.WHITE + Style.DIM + f"  │{'─' * (W - 2)}│" + Style.RESET_ALL)
    print(Fore.WHITE + "  │   " + bar + "   " + Fore.WHITE + "│")
    print(Fore.WHITE + Style.BRIGHT + f"  ╰{'─' * (W - 2)}╯")
    print()


# ── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    banner()

    info("Starting security scan…")
    success("Source files parsed successfully")
    warning("Outdated dependency detected: requests==2.20.0")
    error("Hardcoded API key found in config.py:14")

    box("Recommendations", [
        "-> Rotate exposed credentials immediately",
        "-> Pin dependencies and run pip-audit",
        "-> Set DEBUG=False before deploying",
        "-> Enforce HSTS / HTTPS redirects",
    ])

    show_risk(0)
    show_risk(20)
    show_risk(55)
    show_risk(80)