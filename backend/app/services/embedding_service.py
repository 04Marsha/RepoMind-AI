from sentence_transformers import SentenceTransformer

from app.models.TextChunk import TextChunk
from app.models.EmbeddedChunk import EmbeddedChunk

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    # ACCEPTS THE LIST OF TEXTCHUNKS AND EMBEDS THEM INTO A LIST OF NUMBERS
    def embed_chunks(self, chunks: list[TextChunk]) -> list[EmbeddedChunk]:
        texts = [chunk.content for chunk in chunks]

        embeddings = self.model.encode(texts)

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunks.append(
                EmbeddedChunk(
                    path=chunk.path,
                    language=chunk.language,
                    chunk_number=chunk.chunk_number,
                    content=chunk.content,
                    embedding=embedding.tolist()
                )
            )
        return embedded_chunks

    # EMBEDS TEXT
    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()

