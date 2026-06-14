from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="AutoAI Agent API",
    description="Agentic AI vehicle diagnostics API with fault-code parsing, manual retrieval, sensor analysis, and risk scoring.",
    version="0.1.0",
)

app.include_router(router)