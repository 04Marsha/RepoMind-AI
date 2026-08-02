from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.models.chat.TextChunk import TextChunk

class Retriever:

    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    # RETRIEVES THE CHUNKS FROM EMBEDDED TEXT
    def retrieve(self, question: str) -> list[TextChunk]:
        query_embedding = self.embedding_service.embed_text(question)

        chunks = self.vector_store.search(query_embedding)

        return chunks