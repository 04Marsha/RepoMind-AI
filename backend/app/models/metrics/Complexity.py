from pydantic import BaseModel, Field

class Complexity(BaseModel):
    score: int = 0
    level: str = "Unknown"
    reasons: list[str] = Field(default_factory=list)