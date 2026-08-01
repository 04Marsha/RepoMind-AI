from pydantic import BaseModel

class TextChunk(BaseModel):
    path: str
    language: str
    content: str
    chunk_number: int