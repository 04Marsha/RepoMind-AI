from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from app.core.dependencies import get_repository_overview_service
from app.agents.repository.repository_agent import RepositoryAgent
from app.discovery.project_discovery import ProjectDiscovery
from app.core.dependencies import (get_project_discovery, project_discovery)
from app.models.indexing.IndexRepositoryRequest import IndexRepositoryRequest
from app.core.dependencies import repository_service
from app.core.dependencies import get_repository_intelligence_analyzer
from app.analyzers.repository.repository_intelligence_analyzer import RepositoryIntelligenceAnalyzer
from app.models.repository.RepositoryIntelligence import RepositoryIntelligence

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


@router.post("/intelligence")
def repository_intelligence(request: IndexRepositoryRequest, analyzer: RepositoryIntelligenceAnalyzer = Depends(get_repository_intelligence_analyzer)):

    repo_path = repository_service.github_service.clone_repository(
        request.github_url
    )

    projects = project_discovery.discover_all(repo_path)

    overall = RepositoryIntelligence()

    for context in projects:
        intelligence = analyzer.analyze(context)

        if overall.language is None:
            overall.language = intelligence.language

        if overall.package_manager is None:
            overall.package_manager = intelligence.package_manager
        
        overall.backend_frameworks.extend(intelligence.backend_frameworks)
        overall.frontend_frameworks.extend(intelligence.frontend_frameworks)
        overall.databases.extend(intelligence.databases)
        overall.vector_databases.extend(intelligence.vector_databases)
        overall.orms.extend(intelligence.orms)
        overall.testing_frameworks.extend(intelligence.testing_frameworks)
        overall.build_tools.extend(intelligence.build_tools)
        overall.entry_points.extend(intelligence.entry_points)


    overall.backend_frameworks = sorted(set(overall.backend_frameworks))
    overall.frontend_frameworks = sorted(set(overall.frontend_frameworks))
    overall.databases = sorted(set(overall.databases))
    overall.vector_databases = sorted(set(overall.vector_databases))
    overall.orms = sorted(set(overall.orms))
    overall.testing_frameworks = sorted(set(overall.testing_frameworks))
    overall.build_tools = sorted(set(overall.build_tools))
    overall.entry_points = sorted(set(overall.entry_points))

    return overall