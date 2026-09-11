from app.services.company_service import list_companies


def get_portfolio_risk_summary() -> dict:
    """
    Computes aggregate risk metrics across the full watchlist.

    'worsening_trend' deliberately excludes companies already present in
    'top_concerns', so the two lists surface distinct information instead
    of overlapping.
    """

    companies = list_companies()

    high_risk = [c for c in companies if c["risk_score"] >= 60]
    high_risk_sorted = sorted(high_risk, key=lambda c: c["risk_score"], reverse=True)
    top_concerns = high_risk_sorted[:5]
    top_concern_names = {c["name"] for c in top_concerns}

    # Surfaces emerging risk — deliberately excludes companies already flagged
    # above, so this list adds new information instead of repeating it.
    worsening = [
        c for c in companies
        if c["trend"] == "worsening" and c["name"] not in top_concern_names
    ]
    worsening_sorted = sorted(worsening, key=lambda c: c["risk_score"], reverse=True)

    return {
        "total_companies": len(companies),
        "high_risk_count": len(high_risk),
        "worsening_count": len([c for c in companies if c["trend"] == "worsening"]),
        "top_concerns": [
            {"name": c["name"], "risk_score": c["risk_score"], "trend": c["trend"], "sector": c["sector"]}
            for c in top_concerns
        ],
        "worsening_trend": [
            {"name": c["name"], "risk_score": c["risk_score"], "sector": c["sector"]}
            for c in worsening_sorted[:5]
        ],
    }