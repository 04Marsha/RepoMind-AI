from pathlib import Path
from pydantic import BaseModel

class RepositoryContext(BaseModel):
    repository_root: Path
    repository_name: str
    project_root: Path
    project_name: str
    score: int
    confidence: float