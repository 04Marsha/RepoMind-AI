from pydantic import BaseModel

class RepositoryMetadata(BaseModel):
    repository_name: str
    language: str
    has_readme: bool
    has_license: bool
    dockerized: bool
    has_tests: bool