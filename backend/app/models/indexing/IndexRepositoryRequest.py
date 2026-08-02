from pydantic import BaseModel

class IndexRepositoryRequest(BaseModel):
    github_url: str