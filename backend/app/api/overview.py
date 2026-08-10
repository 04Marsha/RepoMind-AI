from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from app.core.dependencies import get_repository_overview_service
from app.agents.repository.repository_agent import RepositoryAgent
from app.discovery.project_discovery import ProjectDiscovery
from app.core.dependencies import (get_project_discovery, project_discovery)
from app.models.indexing.IndexRepositoryRequest import IndexRepositoryRequest
from app.core.dependencies import repository_service
from app.core.dependencies import (
    get_repository_intelligence_analyzer, 
    get_structure_analyzer,
    get_metrics_analyzer,
    get_architecture_analyzer,
    get_api_endpoint_analyzer,
    get_database_analyzer
    )
from app.analyzers.repository.repository_intelligence_analyzer import RepositoryIntelligenceAnalyzer
from app.models.repository.RepositoryIntelligence import RepositoryIntelligence
from app.analyzers.structure.structure_analyzer import StructureAnalyzer
from app.analyzers.metrics.metrics_analyzer import MetricsAnalyzer
from app.analyzers.architecture.architecture_analyzer import ArchitectureAnalyzer
from app.analyzers.api.api_endpoint_analyzer import ApiEndpointAnalyzer
from app.analyzers.database.database_analyzer import DatabaseAnalyzer

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

    overall.package_manager = analyzer.detect_package_manager(repo_path)

    for context in projects:
        intelligence = analyzer.analyze(context)

        if overall.primary_language is None:
            overall.primary_language = intelligence.primary_language

        overall.languages.extend(intelligence.languages)

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

    overall.languages = sorted(set(overall.languages))
    overall.backend_frameworks = sorted(set(overall.backend_frameworks))
    overall.frontend_frameworks = sorted(set(overall.frontend_frameworks))
    overall.databases = sorted(set(overall.databases))
    overall.vector_databases = sorted(set(overall.vector_databases))
    overall.orms = sorted(set(overall.orms))
    overall.testing_frameworks = sorted(set(overall.testing_frameworks))
    overall.build_tools = sorted(set(overall.build_tools))
    overall.entry_points = sorted(set(overall.entry_points))

    return overall

@router.post("/structure")
def repository_structure(
    request: IndexRepositoryRequest,
    structure_analyzer: StructureAnalyzer = Depends(get_structure_analyzer)
):
    repo_path = repository_service.github_service.clone_repository(
        request.github_url
    )

    context = project_discovery.discover(repo_path)

    return structure_analyzer.analyze(context)

@router.post("/metrics")
def repository_metrics(
    request: IndexRepositoryRequest,
    metrics_analyzer: MetricsAnalyzer = Depends(get_metrics_analyzer)
):
    repo_path = repository_service.github_service.clone_repository(
        request.github_url
    )

    context = project_discovery.discover(repo_path)

    return metrics_analyzer.analyze(context)

@router.post("/architecture")
def repository_architecture(
    request: IndexRepositoryRequest,
    architecture_analyzer: ArchitectureAnalyzer = Depends(get_architecture_analyzer)
):
    repo_path = repository_service.github_service.clone_repository(
        request.github_url
    )

    context = project_discovery.discover(repo_path)

    return architecture_analyzer.analyze(context)

@router.post("/api-analysis")
def api_analysis(
    request: IndexRepositoryRequest,
    analyzer: ApiEndpointAnalyzer = Depends(get_api_endpoint_analyzer),
):
    repo = repository_service.github_service.clone_repository(
        request.github_url
    )

    context = project_discovery.discover(repo)

    return analyzer.analyze(context)

@router.post("/database")
def api_analysis(
    request: IndexRepositoryRequest,
    analyzer: DatabaseAnalyzer = Depends(get_database_analyzer),
):
    repo_path = repository_service.github_service.clone_repository(
        request.github_url
    )

    context = project_discovery.discover(repo_path)

    return analyzer.analyze(context)