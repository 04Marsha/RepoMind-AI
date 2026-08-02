from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from app.core.dependencies import get_repository_overview_service
from app.agents.repository.repository_agent import RepositoryAgent
from app.discovery.project_discovery import ProjectDiscovery
from app.core.dependencies import get_project_discovery

router = APIRouter(prefix="/repositories", tags=["Repository Overview"])

@router.get("/overview/{repository_name}")
def get_overview(repository_name: str, repository_agent: RepositoryAgent = Depends(
    get_repository_overview_service)):
    repo_path = Path(f"./repositories/{repository_name}")

    if not repo_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Repository not found."
        )

    return repository_agent.get_repository_overview(repo_path)

@router.get("/discover/{repository_name}")
def discover(
    repository_name: str,
    project_discovery: ProjectDiscovery = Depends(get_project_discovery)
):
    repo_path = Path(f"./repositories/{repository_name}")

    return project_discovery.discover_all(repo_path)