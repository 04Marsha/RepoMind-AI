from pydantic import BaseModel, Field

class RepositoryOverview(BaseModel):
    repository_name: str
    primary_language: str
    languages: list[str] = Field(default_factory=list)
    framework: list[str]
    total_files: int
    total_directories: int
    source_files: int
    documentation_files: int
    configuration_files: int
    has_readme: bool
    has_license: bool
    has_tests: bool
    dockerized: bool
    dependencies: list[str]