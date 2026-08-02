from app.services.github.github_service import GithubService
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.services.indexing.repository_indexing_service import RepositoryIndexingService
from app.services.retrieval.vector_store import VectorStore
from app.models.repository.RepositoryMetadata import RepositoryMetadata
from app.discovery.project_discovery import ProjectDiscovery

class RepositoryService:

    def __init__(
            self,
            github_service: GithubService,
            repository_analyzer: RepositoryAnalyzer,
            project_discovery: ProjectDiscovery,
            repository_indexing_service: RepositoryIndexingService,
            vector_store: VectorStore
        ):
        self.github_service = github_service
        self.repository_analyzer = repository_analyzer
        self.project_discovery = project_discovery
        self.repository_indexing_service = repository_indexing_service
        self.vector_store = vector_store

    # CLONING AND EMBEDDING
    def index_repository(self, github_url: str) -> RepositoryMetadata:
        self.vector_store.clear()

        repo_path = self.github_service.clone_repository(github_url)

        repository_context = self.project_discovery.discover(repo_path)

        repository_metadata = self.repository_analyzer.analyze(repository_context)

        self.repository_indexing_service.index_repository(repository_context.project_root)

        return repository_metadata