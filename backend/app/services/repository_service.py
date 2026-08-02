from app.services.github_service import GithubService
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.models.repository.RepositoryMetadata import RepositoryMetadata

class RepositoryService:

    def __init__(
            self,
            github_service: GithubService,
            repository_analyzer: RepositoryAnalyzer,
            chunking_service: ChunkingService,
            embedding_service: EmbeddingService,
            vector_store: VectorStore
        ):
        self.github_service = github_service
        self.repository_analyzer = repository_analyzer
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    # CLONING AND EMBEDDING
    def index_repository(self, github_url: str) -> RepositoryMetadata:
        self.vector_store.clear()

        repo_path = self.github_service.clone_repository(github_url)

        repository_metadata = self.repository_analyzer.analyze(repo_path)

        files = self.repository_analyzer.index_repository(repo_path)

        for file_metadata in files:
            chunks = self.chunking_service.chunk_file(file_metadata)
            embedded_chunks = self.embedding_service.embed_chunks(chunks)
            self.vector_store.add_chunks(embedded_chunks)

        return repository_metadata