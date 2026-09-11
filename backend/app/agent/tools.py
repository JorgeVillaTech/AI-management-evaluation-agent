from typing import Annotated
from pydantic import Field

from app.services.company_service import find_company, list_companies
from app.services.market_data_service import search_ticker, get_market_data
from app.services.briefing_service import build_meeting_briefing

def _recommendation_for(risk_level: str) -> str:
    return {
        "High": "Recommend enhanced due diligence and a quarterly review before any new engagement.",
        "Moderate": "Recommend standard monitoring, with review in the next reporting cycle.",
        "Low": "No immediate action required; continue standard monitoring.",
    }[risk_level]


def generate_formal_report(
    company_name: Annotated[str, Field(description="The company to generate the formal report for")],
) -> dict:
    """Generates a formal risk report with a fixed structure: executive summary, key signals, and a recommendation."""
    profile = find_company(company_name)
    if profile is None:
        return {"error": f"No company found matching '{company_name}'"}

    risk_level = "High" if profile["risk_score"] >= 60 else "Moderate" if profile["risk_score"] >= 35 else "Low"

    return {
        "company_name": profile["name"],
        "sector": profile["sector"],
        "risk_score": profile["risk_score"],
        "risk_level": risk_level,
        "trend": profile["trend"],
        "executive_summary": (
            f"{profile['name']} operates in the {profile['sector']} sector with a "
            f"risk score of {profile['risk_score']} ({risk_level.lower()} risk), "
            f"currently trending {profile['trend']}."
        ),
        "key_signals": profile["recent_signals"],
        "recommendation": _recommendation_for(risk_level),
    }


def get_company_profile(
    company_name: Annotated[str, Field(description="The name of the company to look up")],
) -> dict:
    """Look up a company's risk profile and recent business signals by name."""
    profile = find_company(company_name)
    if profile is None:
        return {"error": f"No company found matching '{company_name}'"}
    return profile


def list_all_companies() -> dict:
    """List all companies currently available in the risk database, with their name and sector."""
    companies = list_companies()
    return {
        "companies": [
            {"name": profile["name"], "sector": profile["sector"], "risk score": profile["risk_score"]}
            for profile in companies
        ]
    }


def get_market_data_tool(
    company_name: Annotated[str, Field(description="The company name to look up real market data for")],
) -> dict:
    """Fetches real, current market data (price, market cap, exchange, industry) for a company by name."""
    match = search_ticker(company_name)
    if match is None:
        return {"error": f"No ticker found matching '{company_name}'"}

    data = get_market_data(match["symbol"])
    if data is None:
        return {"error": f"No market data available for ticker '{match['symbol']}'"}

    return data


def prepare_meeting_briefing(
    company_name: Annotated[str, Field(description="The company to prepare a pre-meeting briefing for")],
) -> dict:
    """Prepares a synthesized meeting briefing combining internal risk analysis with real market data."""
    return build_meeting_briefing(company_name)