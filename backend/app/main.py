from fastapi import FastAPI, HTTPException
from app.models.repository import RepositoryRequest
from app.services.repository_service import repository_service
from app.exceptions.repository_exception import InvalidRepositoryURLException

app = FastAPI()

@app.post("/repositories")
def create_repository(request: RepositoryRequest):
    try:
        return repository_service.clone_repository(request.url)

    except InvalidRepositoryURLException:
        raise HTTPException(
            status_code=400,
            detail="Invalid Github repository URL"
        )