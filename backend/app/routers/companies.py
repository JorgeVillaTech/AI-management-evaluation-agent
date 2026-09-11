from fastapi import APIRouter, HTTPException

from app.services.company_service import find_company , list_companies

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{company_name}")
async def get_company_profile(company_name: str):
    """
    Returns the risk and growth profile for a company.
    """
    profile = find_company(company_name)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"Company '{company_name}' not found")
    return profile

@router.get("")
async def list_all_companies_endpoint():
    return list_companies()