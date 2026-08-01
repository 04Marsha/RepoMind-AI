from pathlib import Path
from git import Repo

from app.utils.validators import is_valid_github_url
from app.exceptions.repository_exception import InvalidRepositoryURLException

class GithubService:

    BASE_PATH = Path("repositories")

    # CLONES THE REPO FROM THE INPUT GITHUB LINK
    def clone_repository(self, url: str) -> Path:

        if not is_valid_github_url(url):
            raise InvalidRepositoryURLException()

        self.BASE_PATH.mkdir(exist_ok=True)

        repo_name = url.rstrip("/").split("/")[-1]
        repo_name = repo_name.removesuffix(".git")

        destination = self.BASE_PATH / repo_name

        if destination.is_dir():
            repo = Repo(destination)

            repo.remotes.origin.pull()

            return destination

        try:
            Repo.clone_from(url, destination)
        except Exception:
            pass

        return destination