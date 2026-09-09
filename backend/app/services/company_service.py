"""
Company data service — mock version (Phase 1).

Test data
"""

_MOCK_COMPANIES = {
    "acme corp": {"name": "Acme Corp", "sector": "Industrial manufacturing", "risk_score": 72, "trend": "stable", "recent_signals": ["12% increase in short-term debt in the last quarter", "Announced expansion into the Latin American market"]},
    "globex sa": {"name": "Globex S.A.", "sector": "Fintech", "risk_score": 34, "trend": "improving", "recent_signals": ["Successfully closed a Series C funding round", "Reduced executive staff turnover"]},
    "nova biotech": {"name": "Nova Biotech", "sector": "Biotechnology", "risk_score": 61, "trend": "improving", "recent_signals": ["Phase 2 trial results published positively", "New strategic partnership with a major pharma distributor"]},
    "orion logistics": {"name": "Orion Logistics", "sector": "Transportation & logistics", "risk_score": 48, "trend": "stable", "recent_signals": ["Fuel cost hedging contract renewed", "Fleet expansion delayed by 2 quarters"]},
    "vertex energy group": {"name": "Vertex Energy Group", "sector": "Renewable energy", "risk_score": 29, "trend": "improving", "recent_signals": ["Secured government subsidy for solar expansion", "Debt-to-equity ratio improved year over year"]},
    "quantum retail": {"name": "Quantum Retail", "sector": "Retail", "risk_score": 83, "trend": "worsening", "recent_signals": ["Store closures announced in 3 regions", "Missed quarterly earnings estimate for second consecutive quarter"]},
    "atlas defense systems": {"name": "Atlas Defense Systems", "sector": "Aerospace & defense", "risk_score": 22, "trend": "stable", "recent_signals": ["New multi-year government contract signed", "Credit rating upgraded by a major agency"]},
    "brightline media": {"name": "Brightline Media", "sector": "Media & entertainment", "risk_score": 66, "trend": "worsening", "recent_signals": ["Subscriber growth flattened", "Key content licensing deal not renewed"]},
    "sterling insurance group": {"name": "Sterling Insurance Group", "sector": "Insurance", "risk_score": 41, "trend": "stable", "recent_signals": ["Claims ratio within historical average", "New underwriting leadership appointed"]},
    "ironclad manufacturing": {"name": "Ironclad Manufacturing", "sector": "Heavy machinery", "risk_score": 55, "trend": "stable", "recent_signals": ["Raw material costs stabilized", "Union contract renewed without disruption"]},
    "cascade foods": {"name": "Cascade Foods", "sector": "Food & beverage", "risk_score": 37, "trend": "improving", "recent_signals": ["Expanded distribution into 2 new states", "Input cost pressures easing"]},
    "meridian automotive": {"name": "Meridian Automotive", "sector": "Automotive", "risk_score": 78, "trend": "worsening", "recent_signals": ["Supply chain disruption affecting production", "Recall issued for a mid-size vehicle line"]},
    "pinnacle real estate holdings": {"name": "Pinnacle Real Estate Holdings", "sector": "Commercial real estate", "risk_score": 88, "trend": "worsening", "recent_signals": ["Office occupancy rates declined sharply", "Refinancing risk flagged on 2027 debt maturities"]},
    "clearwater agritech": {"name": "Clearwater AgriTech", "sector": "Agriculture technology", "risk_score": 44, "trend": "improving", "recent_signals": ["New precision farming contract with regional cooperative", "R&D tax credit approved"]},
    "helix telecom": {"name": "Helix Telecom", "sector": "Telecommunications", "risk_score": 31, "trend": "stable", "recent_signals": ["5G infrastructure rollout ahead of schedule", "Customer churn rate at multi-year low"]},
    "summit healthcare partners": {"name": "Summit Healthcare Partners", "sector": "Healthcare services", "risk_score": 26, "trend": "improving", "recent_signals": ["Acquired 2 regional clinics", "Reimbursement rate negotiations concluded favorably"]},
    "vantage capital advisors": {"name": "Vantage Capital Advisors", "sector": "Financial services", "risk_score": 52, "trend": "stable", "recent_signals": ["Assets under management grew 8% year over year", "Regulatory inquiry closed with no findings"]},
    "redstone mining co": {"name": "Redstone Mining Co", "sector": "Mining & metals", "risk_score": 69, "trend": "worsening", "recent_signals": ["Commodity price volatility impacting margins", "Environmental compliance fine issued"]},
    "beacon software labs": {"name": "Beacon Software Labs", "sector": "Enterprise software", "risk_score": 19, "trend": "improving", "recent_signals": ["Annual recurring revenue up 22%", "Key enterprise client renewed a 3-year contract"]},
    "harborview shipping": {"name": "Harborview Shipping", "sector": "Maritime logistics", "risk_score": 58, "trend": "stable", "recent_signals": ["Port congestion resolved ahead of forecast", "New vessel added to fleet"]},
    "granite construction partners": {"name": "Granite Construction Partners", "sector": "Construction", "risk_score": 63, "trend": "stable", "recent_signals": ["Backlog of contracted projects grew", "Labor cost inflation pressuring margins"]},
    "lumen pharmaceuticals": {"name": "Lumen Pharmaceuticals", "sector": "Pharmaceuticals", "risk_score": 35, "trend": "improving", "recent_signals": ["FDA approval granted for new formulation", "Patent litigation resolved favorably"]},
    "frostline apparel": {"name": "Frostline Apparel", "sector": "Consumer goods", "risk_score": 74, "trend": "worsening", "recent_signals": ["Inventory write-downs larger than expected", "E-commerce sales declined for the year"]},
    "novak industrial group": {"name": "Novak Industrial Group", "sector": "Industrial equipment", "risk_score": 46, "trend": "stable", "recent_signals": ["Order backlog remains healthy", "Input costs moderating"]},
    "skyline hospitality": {"name": "Skyline Hospitality", "sector": "Hospitality & tourism", "risk_score": 39, "trend": "improving", "recent_signals": ["Occupancy rates recovered to pre-pandemic levels", "New property opened in a key market"]},
    "trident cybersecurity": {"name": "Trident Cybersecurity", "sector": "Cybersecurity", "risk_score": 15, "trend": "improving", "recent_signals": ["Landed 3 new Fortune 500 clients", "No material security incidents reported"]},
    "westfield utilities": {"name": "Westfield Utilities", "sector": "Utilities", "risk_score": 24, "trend": "stable", "recent_signals": ["Regulatory rate case approved", "Infrastructure modernization on schedule"]},
    "cobalt semiconductor": {"name": "Cobalt Semiconductor", "sector": "Semiconductors", "risk_score": 57, "trend": "worsening", "recent_signals": ["Chip demand softened in key end markets", "Capital expenditure plans scaled back"]},
    "brightpath education group": {"name": "BrightPath Education Group", "sector": "Education services", "risk_score": 33, "trend": "stable", "recent_signals": ["Enrollment numbers steady year over year", "New online program launched"]},
    "ashford textiles": {"name": "Ashford Textiles", "sector": "Textiles & manufacturing", "risk_score": 81, "trend": "worsening", "recent_signals": ["Major client contract not renewed", "Currency exposure increased losses this quarter"]},
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