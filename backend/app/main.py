# TMPDIR=$HOME/pip-temp pip install sentence-transformers
# uvicorn app.main:app --reload --reload-dir app

from fastapi import FastAPI
# from app.api.index import router as index_router
from app.api.chat import router as chat_router
# from app.api.overview import router as overview_router
from app.api.agents.repository_agent import router as repository_agent_router

app = FastAPI(
    title="RepoMind AI",
    version="1.0.0"
)

# app.include_router(index_router)
app.include_router(chat_router)
# app.include_router(overview_router)
app.include_router(repository_agent_router)