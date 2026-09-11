from app.services.portfolio_service import get_portfolio_risk_summary


def test_worsening_trend_excludes_top_concerns():
    """Regression test: these two lists must never overlap (the bug we fixed)."""
    summary = get_portfolio_risk_summary()

    top_concern_names = {c["name"] for c in summary["top_concerns"]}
    worsening_names = {c["name"] for c in summary["worsening_trend"]}

    assert top_concern_names.isdisjoint(worsening_names)


def test_top_concerns_are_sorted_by_risk_descending():
    summary = get_portfolio_risk_summary()
    scores = [c["risk_score"] for c in summary["top_concerns"]]
    assert scores == sorted(scores, reverse=True)