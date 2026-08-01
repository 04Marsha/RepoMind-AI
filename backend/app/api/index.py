from fastapi import APIRouter, HTTPException

from app.models.IndexRepositoryRequest import IndexRepositoryRequest
from app.exceptions.repository_exception import InvalidRepositoryURLException
from app.core.dependencies import repository_service

router = APIRouter(prefix="/repositories", tags=["Repositories"])

@router.post("/index")
def index_repository(request: IndexRepositoryRequest):
    try:
        return repository_service.index_repository(request.github_url)

    except InvalidRepositoryURLException:
        raise HTTPException(
            status_code=400,
            detail="Invalid Github repository URL"
        )