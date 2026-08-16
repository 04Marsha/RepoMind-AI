# from sentence_transformers import SentenceTransformer

# from app.models.chat.TextChunk import TextChunk
# from app.models.repository.EmbeddedChunk import EmbeddedChunk

# class EmbeddingService:

#     def __init__(self):
#         self.model = None

#     def get_model(self):
#         if self.model is None:
#             self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
#         return self.model

#     # ACCEPTS THE LIST OF TEXTCHUNKS AND EMBEDS THEM INTO A LIST OF NUMBERS
#     def embed_chunks(self, chunks: list[TextChunk]) -> list[EmbeddedChunk]:
#         texts = [chunk.content for chunk in chunks]

#         embeddings = self.get_model().encode(texts)

#         embedded_chunks = []

#         for chunk, embedding in zip(chunks, embeddings):
#             embedded_chunks.append(
#                 EmbeddedChunk(
#                     path=chunk.path,
#                     language=chunk.language,
#                     chunk_number=chunk.chunk_number,
#                     content=chunk.content,
#                     embedding=embedding.tolist()
#                 )
#             )
#         return embedded_chunks

#     # EMBEDS TEXT
#     def embed_text(self, text: str) -> list[float]:
#         embedding = self.get_model().encode(text)
#         return embedding.tolist()

from app.models.chat.TextChunk import TextChunk
from app.models.repository.EmbeddedChunk import EmbeddedChunk

class EmbeddingService:
    def __init__(self):
        self.model = None

    def get_model(self):
        if self.model is None:
            # Lazy import to prevent out-of-memory during boot
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        return self.model

    def embed_chunks(self, chunks: list[TextChunk]) -> list[EmbeddedChunk]:
        if not chunks:
            return []
        texts = [chunk.content for chunk in chunks]
        embeddings = self.get_model().encode(texts)

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

    def embed_text(self, text: str) -> list[float]:
        embedding = self.get_model().encode(text)
        return embedding.tolist()