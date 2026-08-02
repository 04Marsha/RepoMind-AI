# https://github.com/openai/openai-python
from urllib.parse import urlparse

def extract_repository_name(url: str) -> str:
    parsed = urlparse(url)

    parts = parsed.path.strip("/").split("/")

    return parts[-1].removesuffix(".git")


def extract_repository_owner(url: str) -> str:
    parsed = urlparse(url)
    
    parts = parsed.path.strip("/").split("/")
    return parts[0]


def is_valid_github_url(url: str) -> bool:
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False

    if parsed.netloc != "github.com":
        return False
    
    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) != 2:
        return False

    owner, repository = path_parts

    if not owner or not repository:
        return False

    return True