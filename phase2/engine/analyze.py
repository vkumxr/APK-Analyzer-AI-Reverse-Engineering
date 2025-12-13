from phase2.rules.permission_risk import analyze_permissions
# future use:
# from phase2.rules.permission_combos import analyze_permission_combos


def analyze(phase1_report: dict) -> dict:
    """
    Phase 2 analysis entrypoint.
    Consumes Phase 1 static report and enriches it with risk intelligence.
    """

    permissions = phase1_report.get("permissions", [])

    findings = []

    # ---- Permission-level risk ----
    perm_findings = analyze_permissions(permissions)
    findings.extend(perm_findings)

    # ---- Permission combination risk (next step) ----
    # combo_findings = analyze_permission_combos(permissions)
    # findings.extend(combo_findings)

    # ---- Risk scoring ----
    risk_score = len(findings) * 20

    if risk_score >= 40:
        level = "HIGH"
    elif risk_score > 0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "meta": {
            "engine": "ReDroid-AI Phase 2",
            "version": "0.1"
        },
        "risk_summary": {
            "score": risk_score,
            "level": level
        },
        "findings": findings
    }