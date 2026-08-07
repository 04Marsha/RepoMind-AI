from pydantic import BaseModel

class RepositorySummary(BaseModel):
    summary: str