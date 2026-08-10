from pydantic import BaseModel, Field

class RepositoryIntelligence(BaseModel):
    primary_language: str | None = None
    languages: list[str] = Field(default_factory=list)
    backend_frameworks: list[str] = Field(default_factory=list)
    frontend_frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    vector_databases: list[str] = Field(default_factory=list)
    orms: list[str] = Field(default_factory=list)
    testing_frameworks: list[str] = Field(default_factory=list)
    build_tools: list[str] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)
    package_manager: list[str] = Field(default_factory=list)