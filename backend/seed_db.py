from app.database import Base, engine, SessionLocal
from app.models.company import Company

_SEED_DATA = [
    {'name': 'Acme Corp', 'sector': 'Industrial manufacturing', 'risk_score': 72, 'trend': 'stable', 'recent_signals': ['12% increase in short-term debt in the last quarter', 'Announced expansion into the Latin American market']},
    {'name': 'Globex S.A.', 'sector': 'Fintech', 'risk_score': 34, 'trend': 'improving', 'recent_signals': ['Successfully closed a Series C funding round', 'Reduced executive staff turnover']},
    {'name': 'Nova Biotech', 'sector': 'Biotechnology', 'risk_score': 61, 'trend': 'improving', 'recent_signals': ['Phase 2 trial results published positively', 'New strategic partnership with a major pharma distributor']},
    {'name': 'Orion Logistics', 'sector': 'Transportation & logistics', 'risk_score': 48, 'trend': 'stable', 'recent_signals': ['Fuel cost hedging contract renewed', 'Fleet expansion delayed by 2 quarters']},
    {'name': 'Vertex Energy Group', 'sector': 'Renewable energy', 'risk_score': 29, 'trend': 'improving', 'recent_signals': ['Secured government subsidy for solar expansion', 'Debt-to-equity ratio improved year over year']},
    {'name': 'Quantum Retail', 'sector': 'Retail', 'risk_score': 83, 'trend': 'worsening', 'recent_signals': ['Store closures announced in 3 regions', 'Missed quarterly earnings estimate for second consecutive quarter']},
    {'name': 'Atlas Defense Systems', 'sector': 'Aerospace & defense', 'risk_score': 22, 'trend': 'stable', 'recent_signals': ['New multi-year government contract signed', 'Credit rating upgraded by a major agency']},
    {'name': 'Brightline Media', 'sector': 'Media & entertainment', 'risk_score': 66, 'trend': 'worsening', 'recent_signals': ['Subscriber growth flattened', 'Key content licensing deal not renewed']},
    {'name': 'Sterling Insurance Group', 'sector': 'Insurance', 'risk_score': 41, 'trend': 'stable', 'recent_signals': ['Claims ratio within historical average', 'New underwriting leadership appointed']},
    {'name': 'Ironclad Manufacturing', 'sector': 'Heavy machinery', 'risk_score': 55, 'trend': 'stable', 'recent_signals': ['Raw material costs stabilized', 'Union contract renewed without disruption']},
    {'name': 'Cascade Foods', 'sector': 'Food & beverage', 'risk_score': 37, 'trend': 'improving', 'recent_signals': ['Expanded distribution into 2 new states', 'Input cost pressures easing']},
    {'name': 'Meridian Automotive', 'sector': 'Automotive', 'risk_score': 78, 'trend': 'worsening', 'recent_signals': ['Supply chain disruption affecting production', 'Recall issued for a mid-size vehicle line']},
    {'name': 'Pinnacle Real Estate Holdings', 'sector': 'Commercial real estate', 'risk_score': 88, 'trend': 'worsening', 'recent_signals': ['Office occupancy rates declined sharply', 'Refinancing risk flagged on 2027 debt maturities']},
    {'name': 'Clearwater AgriTech', 'sector': 'Agriculture technology', 'risk_score': 44, 'trend': 'improving', 'recent_signals': ['New precision farming contract with regional cooperative', 'R&D tax credit approved']},
    {'name': 'Helix Telecom', 'sector': 'Telecommunications', 'risk_score': 31, 'trend': 'stable', 'recent_signals': ['5G infrastructure rollout ahead of schedule', 'Customer churn rate at multi-year low']},
    {'name': 'Summit Healthcare Partners', 'sector': 'Healthcare services', 'risk_score': 26, 'trend': 'improving', 'recent_signals': ['Acquired 2 regional clinics', 'Reimbursement rate negotiations concluded favorably']},
    {'name': 'Vantage Capital Advisors', 'sector': 'Financial services', 'risk_score': 52, 'trend': 'stable', 'recent_signals': ['Assets under management grew 8% year over year', 'Regulatory inquiry closed with no findings']},
    {'name': 'Redstone Mining Co', 'sector': 'Mining & metals', 'risk_score': 69, 'trend': 'worsening', 'recent_signals': ['Commodity price volatility impacting margins', 'Environmental compliance fine issued']},
    {'name': 'Beacon Software Labs', 'sector': 'Enterprise software', 'risk_score': 19, 'trend': 'improving', 'recent_signals': ['Annual recurring revenue up 22%', 'Key enterprise client renewed a 3-year contract']},
    {'name': 'Harborview Shipping', 'sector': 'Maritime logistics', 'risk_score': 58, 'trend': 'stable', 'recent_signals': ['Port congestion resolved ahead of forecast', 'New vessel added to fleet']},
    {'name': 'Granite Construction Partners', 'sector': 'Construction', 'risk_score': 63, 'trend': 'stable', 'recent_signals': ['Backlog of contracted projects grew', 'Labor cost inflation pressuring margins']},
    {'name': 'Lumen Pharmaceuticals', 'sector': 'Pharmaceuticals', 'risk_score': 35, 'trend': 'improving', 'recent_signals': ['FDA approval granted for new formulation', 'Patent litigation resolved favorably']},
    {'name': 'Frostline Apparel', 'sector': 'Consumer goods', 'risk_score': 74, 'trend': 'worsening', 'recent_signals': ['Inventory write-downs larger than expected', 'E-commerce sales declined for the year']},
    {'name': 'Novak Industrial Group', 'sector': 'Industrial equipment', 'risk_score': 46, 'trend': 'stable', 'recent_signals': ['Order backlog remains healthy', 'Input costs moderating']},
    {'name': 'Skyline Hospitality', 'sector': 'Hospitality & tourism', 'risk_score': 39, 'trend': 'improving', 'recent_signals': ['Occupancy rates recovered to pre-pandemic levels', 'New property opened in a key market']},
    {'name': 'Trident Cybersecurity', 'sector': 'Cybersecurity', 'risk_score': 15, 'trend': 'improving', 'recent_signals': ['Landed 3 new Fortune 500 clients', 'No material security incidents reported']},
    {'name': 'Westfield Utilities', 'sector': 'Utilities', 'risk_score': 24, 'trend': 'stable', 'recent_signals': ['Regulatory rate case approved', 'Infrastructure modernization on schedule']},
    {'name': 'Cobalt Semiconductor', 'sector': 'Semiconductors', 'risk_score': 57, 'trend': 'worsening', 'recent_signals': ['Chip demand softened in key end markets', 'Capital expenditure plans scaled back']},
    {'name': 'BrightPath Education Group', 'sector': 'Education services', 'risk_score': 33, 'trend': 'stable', 'recent_signals': ['Enrollment numbers steady year over year', 'New online program launched']},
    {'name': 'Ashford Textiles', 'sector': 'Textiles & manufacturing', 'risk_score': 81, 'trend': 'worsening', 'recent_signals': ['Major client contract not renewed', 'Currency exposure increased losses this quarter']},
]


def seed_companies():
    """Puebla la tabla de compañías con datos de ejemplo, sin duplicar las que ya existen.
    Es seguro llamarla cada vez que arranca la app."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        for data in _SEED_DATA:
            if db.query(Company).filter(Company.name == data["name"]).first():
                continue
            db.add(Company(**data))
        db.commit()
        print(f"Seeded companies table — {db.query(Company).count()} total.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_companies()