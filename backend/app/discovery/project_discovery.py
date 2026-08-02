from pathlib import Path

from app.models.repository.RepositoryContext import RepositoryContext
from app.discovery.constants import (DISCOVERY_SCORES, STRONG_PROJECT_FILES)

class ProjectDiscovery:

    # RETURNS THE PARENT DIRECTORY OR MAIN DIRECTORY
    def discover(self, repo_path: Path) -> RepositoryContext:
        candidates = self._discover_candidates(repo_path)

        if not candidates:
            return RepositoryContext(
                repository_root=repo_path,
                repository_name=repo_path.name,
                project_root=repo_path,
                project_name=repo_path.name,
                score=0,
                confidence=0.0
            )

        return candidates[0]

    def discover_all(self, repository_path: Path) -> list[RepositoryContext]:
        return self._discover_candidates(repository_path)

    def _discover_candidates(self, repository_path: Path) -> list[RepositoryContext]:
        directories = self._collect_directories(repository_path)

        candidates = []

        for directory in directories:
            score = self._calculate_score(directory)

            has_strong_indicator = any(
                (directory / file).is_file() for file in STRONG_PROJECT_FILES)
            
            if score == 0 or not has_strong_indicator:
                continue

            candidates.append(
                RepositoryContext(
                    repository_root=repository_path,
                    repository_name=repository_path.name,
                    project_root=directory,
                    project_name=directory.name,
                    score=score,
                    confidence=min(score / 100, 1.0)
                )
            )

        candidates.sort(
            key=lambda project: project.score,
            reverse=True
        )

        return candidates

    # RETURNS THE DIRECTORIES
    def _collect_directories(self, repository_path: Path) -> list[Path]:
        directories = [repository_path]

        for item in repository_path.rglob("*"):
            if item.is_dir():
                directories.append(item)

        return directories

    # CALCULATES SCORE FOR THE DIRECTORIES
    def _calculate_score(self, directory: Path) -> int:
        score = 0

        try:
            for item in directory.iterdir():
                if item.is_file():
                    score += DISCOVERY_SCORES.get(item.name, 0)
        except PermissionError:
            return 0

        return score