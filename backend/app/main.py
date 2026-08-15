# TMPDIR=$HOME/pip-temp pip install sentence-transformers
# uvicorn app.main:app --reload --reload-dir app

from datetime import datetime
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.agents.repository_agent import router as repository_agent_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RepoMind AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


app.include_router(chat_router)
app.include_router(repository_agent_router)