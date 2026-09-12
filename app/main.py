"""
    FastAPI application entrypoint.

    Run with :
        uvicorn app.main:app --reload --port 8000
"""

# =========================================================================================
#                                        Import Statements
# =========================================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import router 

app = FastAPI(
    title = "Multi-Agent AI System API",
    description = "FastAPI for backend and react for frontend",
    version="1.0.0"
)

# =========================================================================================
#                                        routing Statements
# =========================================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://wavelength-multi-agent-orchestration.onrender.com",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router , prefix = "/api")

@app.get("/")
async def root():
    return {"message" : "Multi-Agent AI System API is running.", "docs" : "docs"}
