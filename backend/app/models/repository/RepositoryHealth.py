from pydantic import BaseModel

class RepositoryHealth(BaseModel):
    score: int = 0
    strengths: list[str] = []
    issues: list[str] = []