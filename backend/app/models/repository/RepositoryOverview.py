from pydantic import BaseModel

class RepositoryOverview(BaseModel):
    repository_name: str
    primary_language: str
    framework: str
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