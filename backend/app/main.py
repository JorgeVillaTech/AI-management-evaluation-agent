from app.rate_limit import rate_limit
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint

from app.routers import companies
from app.agent.agent import risk_advisor_agent
from app.routers import conversations

from app.database import Base, engine
from app.models import company, conversation 
from seed_db import seed_companies

import os

Base.metadata.create_all(bind=engine)
seed_companies()

app = FastAPI(title="Management and risk evaluation Agent — Backend")

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3001,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # your future Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)

add_agent_framework_fastapi_endpoint(
    app=app,
    agent=risk_advisor_agent, #agent exposed
    path="/copilotkit", #route that accepts AG-UI-formatted requests
    dependencies=[Depends(rate_limit)],
)

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "management-risk-evaluation-backend"}

app.include_router(conversations.router)