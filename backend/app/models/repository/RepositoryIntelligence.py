from pydantic import BaseModel, Field

class RepositoryIntelligence(BaseModel):
    language: str | None = None
    backend_frameworks: list[str] = Field(default_factory=list)
    frontend_frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    vector_databases: list[str] = Field(default_factory=list)
    orms: list[str] = Field(default_factory=list)
    testing_frameworks: list[str] = Field(default_factory=list)
    build_tools: list[str] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)
    package_manager: str | None = None