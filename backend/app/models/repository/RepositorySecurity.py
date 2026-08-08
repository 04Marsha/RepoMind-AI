from pydantic import BaseModel, Field

class RepositorySecurity(BaseModel):
    score: int
    findings: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)