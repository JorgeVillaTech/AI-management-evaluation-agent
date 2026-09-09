from app.database import Base, engine, SessionLocal
from app.models.company import Company
from app.services.company_service import _MOCK_COMPANIES

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    for data in _MOCK_COMPANIES.values():
        existing = db.query(Company).filter(Company.name == data["name"]).first()
        if existing:
            continue

        company = Company(
            name=data["name"],
            sector=data["sector"],
            risk_score=data["risk_score"],
            trend=data["trend"],
            recent_signals=data["recent_signals"],
        )
        db.add(company)

    db.commit()
    print(f"Seeded {db.query(Company).count()} companies into the database.")
finally:
    db.close()