from pydantic import BaseModel, Field

class Architecture(BaseModel):
    style: str | None = None
    project_type: str | None = None
    monorepo: bool = False
    full_stack: bool = False
    microservices: bool = False
    layers: list[str] = Field(default_factory=list)
    confidence: float = 0.0