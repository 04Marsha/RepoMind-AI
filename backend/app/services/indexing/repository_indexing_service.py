from pathlib import Path

from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.services.retrieval.chunking_service import ChunkingService
from app.services.retrieval.embedding_service import EmbeddingService
from app.services.retrieval.vector_store import VectorStore


class RepositoryIndexingService:

    def __init__(
        self,
        repository_analyzer: RepositoryAnalyzer,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):
        self.repository_analyzer = repository_analyzer
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_repository(self, repository_path: Path) -> None:

        files = self.repository_analyzer.index_repository(repository_path)

        for file_metadata in files:
            chunks = self.chunking_service.chunk_file(file_metadata)
            embedded_chunks = self.embedding_service.embed_chunks(chunks)
            self.vector_store.add_chunks(embedded_chunks)