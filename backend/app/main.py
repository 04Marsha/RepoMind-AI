from fastapi import FastAPI
from app.models.repository import RepositoryRequest

app = FastAPI()

@app.post("/repository")
def analyze_repository(repository: RepositoryRequest):
    return {
        "message": "Repository received successfully!",
        "repository_url": repository.url
    }