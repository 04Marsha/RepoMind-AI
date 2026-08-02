from pydantic import BaseModel

class FileMetadata(BaseModel):
    path: str
    extension: str
    language: str
    size: int
    content: str