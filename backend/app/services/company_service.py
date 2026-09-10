from app.database import SessionLocal
from app.models.company import Company

# Transforms the data into a table
def _to_dict(company: Company) -> dict:
    return {
        "name": company.name,
        "sector": company.sector,
        "risk_score": company.risk_score,
        "trend": company.trend,
        "recent_signals": company.recent_signals,
    }


def find_company(company_name: str) -> dict | None:
    """Looks up a company profile by name (case-insensitive) from the database."""
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.name.ilike(company_name.strip())).first()
        return _to_dict(company) if company else None
    finally:
        db.close()


def list_companies() -> list[dict]:
    """Returns all company profiles currently in the database."""
    db = SessionLocal()
    try:
        return [_to_dict(c) for c in db.query(Company).all()]
    finally:
        db.close()