from pydantic import BaseModel, Field


class ProjectStructure(BaseModel):
    directories: list[str] = Field(default_factory=list)
    important_directories: list[str] = Field(default_factory=list)
    config_files: list[str] = Field(default_factory=list)
    documentation_files: list[str] = Field(default_factory=list)