import chromadb

from app.models.repository.EmbeddedChunk import EmbeddedChunk
from app.models.chat.TextChunk import TextChunk
from app.core.config import Settings

class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=Settings.CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="repository_chunks"
        )

    # ADDS CHUNKS TO THE CHROMADB COLLECTION
    def add_chunks(self, chunks: list[EmbeddedChunk]):
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:
            ids.append(
                f"{chunk.path}:{chunk.chunk_number}"
            )
            documents.append(chunk.content)
            embeddings.append(chunk.embedding)
            metadatas.append({
                "path": chunk.path,
                "chunk_number": chunk.chunk_number,
                "language": chunk.language
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    # SEARCHES THE CHUNKS
    def search(self, query_embedding: list[float], k: int = 5) -> list[TextChunk]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        chunks = []

        for document, metadata in zip(documents, metadatas):
            chunks.append(
                TextChunk(
                    path=metadata["path"],
                    language=metadata["language"],
                    chunk_number=metadata["chunk_number"],
                    content=document
                )
            )
        return chunks

    # REMOVES ALL DOCUMENTS
    def clear(self):
        try:
            self.client.delete_collection("repository_chunks")
        except Exception:
            pass

        self.collection = self.client.create_collection(
            name="repository_chunks"
        )
