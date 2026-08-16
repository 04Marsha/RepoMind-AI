from fastapi import APIRouter, Depends

from app.models.indexing.IndexRepositoryRequest import IndexRepositoryRequest
from app.agents.repository.repository_agent import RepositoryAgent
# from app.core.dependencies import get_repository_agent
# from app.core.dependencies import repository_service
from app.core.dependencies import get_repository_agent, get_repository_service
router = APIRouter(prefix="/agents", tags=["Repository Overview"])

@router.post("/analyze-repository")
def analyze_repository(
    request: IndexRepositoryRequest,
    repository_agent: RepositoryAgent = Depends(
        get_repository_agent
    )
):
    # repo_path = repository_service.github_service.clone_repository(
    #     request.github_url
    # )
    repo_path = get_repository_service.github_service.clone_repository(
        request.github_url
    )

    return repository_agent.analyze_repository(repo_path)