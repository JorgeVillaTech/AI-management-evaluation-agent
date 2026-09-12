from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint

from app.routers import companies
from app.agent.agent import risk_advisor_agent
from app.routers import conversations

from app.database import Base, engine
from app.models import company, conversation  # noqa: F401 — imported so their tables register with Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Management and risk evaluation Agent — Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your future Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)

add_agent_framework_fastapi_endpoint(
    app=app,
    agent=risk_advisor_agent, #agent exposed
    path="/copilotkit", #route that accepts AG-UI-formatted requests
)

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "management-risk-evaluation-backend"}

app.include_router(conversations.router)