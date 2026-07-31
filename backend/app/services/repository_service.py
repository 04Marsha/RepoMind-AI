from pathlib import Path
from git import Repo

from app.utils.validators import is_valid_github_url
from app.exceptions.repository_exception import InvalidRepositoryURLException

class RepositoryService:

    BASE_PATH = Path("repositories")

    def clone_repository(self, url: str):

        if not is_valid_github_url(url):
            raise InvalidRepositoryURLException()

        self.BASE_PATH.mkdir(exist_ok=True)

        repo_name = url.split("/")[-1]

        destination = self.BASE_PATH / repo_name

        Repo.clone_from(url, destination)

        return {
            "message": "Repository cloned successfully!",
            "repository_url": url
        }

repository_service = RepositoryService()