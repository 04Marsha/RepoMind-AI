from pydantic import BaseModel

class EmbeddedChunk(BaseModel):
    path: str
    language: str
    chunk_number: int
    content: str
    embedding: list[float]