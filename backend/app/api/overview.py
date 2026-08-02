from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from app.core.dependencies import get_repository_overview_service
from app.services.repository_overview_service import RepositoryOverviewService

router = APIRouter(prefix="/repositories", tags=["Repository Overview"])

@router.get("/overview/{repository_name}")
def get_overview(repository_name: str, repository_overview_service: RepositoryOverviewService = Depends(
    get_repository_overview_service)):
    repo_path = Path(f"./repositories/{repository_name}")

    if not repo_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Repository not found."
        )

    return repository_overview_service.get_repository_overview(repo_path)