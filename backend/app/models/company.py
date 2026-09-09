from sqlalchemy import Column, Integer, String, JSON

from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    sector = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    trend = Column(String, nullable=False)
    recent_signals = Column(JSON, nullable=False)