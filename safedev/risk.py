def calculate_risk(findings):
    if not findings:
        return 0

    unique_rules = set()
    score = 0
    max_sev = 0

    for f in findings:
        rid = f["rule_id"]

        if rid in unique_rules:
            continue

        unique_rules.add(rid)

        sev = f["severity"]
        max_sev = max(max_sev, sev)

        # base scoring
        score += sev * 10

    # 🔥 scale down if no critical issue
    if max_sev < 5:
        score *= 0.7

    return min(int(score), 100)