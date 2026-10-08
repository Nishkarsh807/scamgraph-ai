"""
ScamGraph AI - FastAPI Application Server
Entry point for the backend API services.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from api import analyze, patterns, dashboard, incidents

# Initialize database schema tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScamGraph AI API",
    description="Production AI-Driven Scam Pattern & Multi-Stage Fraud Workflow Recognition Platform",
    version="1.0.0"
)

# CORS configuration for Frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analyze.router)
app.include_router(patterns.router)
app.include_router(dashboard.router)
app.include_router(incidents.router)


@app.get("/")
def root():
    return {
        "project": "ScamGraph AI",
        "tagline": "From suspicious messages to complete scam workflows.",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "scamgraph-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
