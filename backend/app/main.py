from fastapi import FastAPI

from app.routers import companies

app = FastAPI(title="Management and risk evaluation Agent — Backend")

app.include_router(companies.router)


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "management-risk-evaluation-backend"}