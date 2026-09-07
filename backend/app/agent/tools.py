from typing import Annotated
from pydantic import Field

from app.services.company_service import find_company, list_companies


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
            {"name": profile["name"], "sector": profile["sector"]}
            for profile in companies
        ]
    }