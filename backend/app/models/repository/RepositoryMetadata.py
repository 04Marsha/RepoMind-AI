from pydantic import BaseModel

class RepositoryMetadata(BaseModel):
    repository_name: str
    primary_language: str
    languages: list[str]
    has_readme: bool
    has_license: bool
    dockerized: bool
    has_tests: bool