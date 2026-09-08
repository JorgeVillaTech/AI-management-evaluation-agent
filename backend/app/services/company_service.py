"""
Company data service — mock version (Phase 1).

Test data
"""

_MOCK_COMPANIES = {
    "acme corp": {
        "name": "Acme Corp",
        "sector": "Industrial manufacturing",
        "risk_score": 72,  # 0-100 scale, higher = riskier
        "trend": "stable",
        "recent_signals": [
            "12% increase in short-term debt last quarter",
            "Announced expansion into the Latin American market",
        ],
    },
    "globex sa": {
        "name": "Globex S.A.",
        "sector": "Fintech Marketing Test",
        "risk_score": 34,
        "trend": "improving",
        "recent_signals": [
            "Successfully closed a Series C funding round",
            "Reduced executive turnover",
        ],
    },
}


def find_company(company_name: str) -> dict | None:
    """
    Looks up a company profile by name (case-insensitive).

    Returns the profile dict, or None if not found — this NEVER
    raises an uncontrolled exception here; "not found" handling
    happens explicitly, same as you learned with HTTPException.
    """
    key = company_name.strip().lower()
    return _MOCK_COMPANIES.get(key)

def list_companies() -> list[dict]:
    return list(_MOCK_COMPANIES.values())