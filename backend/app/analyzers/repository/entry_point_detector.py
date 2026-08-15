from pathlib import Path

from app.models.repository.RepositoryContext import RepositoryContext

class EntryPointDetector:

    # DETECTS ENTRY POINTS
    def detect(self, context: RepositoryContext) -> list[str]:
        entry_points = []

        entry_points.extend(self._detect_python(context))
        entry_points.extend(self._detect_node(context))
        entry_points.extend(self._detect_react(context))
        entry_points.extend(self._detect_angular(context))
        entry_points.extend(self._detect_java(context))
        entry_points.extend(self._detect_go(context))
        entry_points.extend(self._detect_rust(context))

        return sorted(set(entry_points))

    # CHECKS IF INDICATORS ARE FOUND
    def _contains_indicator(self, file: Path, indicators: list[str], match_all: bool = False) -> bool:
        try:
            text = file.read_text(encoding="utf-8", errors="ignore").lower()

            if match_all:
                return all(
                    indicator.lower() in text
                    for indicator in indicators
                )

            return any(indicator.lower() in text
                       for indicator in indicators)

        except OSError:
            return False

    # DETECTS ENTRY POINT FOR PYTHON
    def _detect_python(self, context: RepositoryContext) -> list[str]:

        candidates = {
            "main.py",
            "app.py",
            "server.py",
            "run.py",
            "manage.py",
        }

        entry_points = []

        indicators = [
            '__name__ == "__main__"',
            "uvicorn.run(",
            "fastapi(",
        ]

        for file in context.repository_root.rglob("*.py"):
            if file.name not in candidates:
                continue

            if self._is_ignored(file):
                continue

            if self._contains_indicator(file, indicators, match_all=False):
                entry_points.append(str(file.relative_to(context.repository_root)))
        return entry_points

    # DETECTS ENTRY POINT FOR NODE
    def _detect_node(self, context: RepositoryContext) -> list[str]:
        candidates = {
            "server.js",
            "server.ts",
            "app.js",
            "main.js",
            "index.js",
            "index.ts",
        }

        indicators = [
            "express(",
            "app.listen(",
            "createServer(",
            "fastify(",
            "koa(",
            "hono(",
            "nestfactory.create(",
            "bootstrap("
        ]

        entry_points = []

        for file in context.repository_root.rglob("*"):
            if file.suffix not in {".js", ".ts"}:
                continue

            if file.name not in candidates:
                continue

            if self._is_ignored(file):
                continue
            
            if self._contains_indicator(file, indicators):
                entry_points.append(str(file.relative_to(context.repository_root)))

        return entry_points

    # DETECTS ENTRY POINT FOR REACT
    def _detect_react(self, context: RepositoryContext) -> list[str]:
        candidates = [
            "main.tsx",
            "index.tsx",
            "main.jsx",
            "index.jsx",
            "App.js",
            "App.tsx",
            "index.js",
            "index.ts"
        ]

        indicators = [
            "createroot(",
            "from 'react-dom/client'",
            "reactdom.render(",
            "strictmode",

            "registerrootcomponent(",
            "expo",
            "navigationcontainer",
        ]

        entry_points = []
        for file in context.repository_root.rglob("*"):
            if file.name not in candidates:
                continue

            if self._is_ignored(file):
                continue

            if self._contains_indicator(file, indicators):
                entry_points.append(str(file.relative_to(context.repository_root)))
        return entry_points


    # DETECTS ENTRY POINT FOR ANGULAR
    def _detect_angular(self, context: RepositoryContext) -> list[str]:
        indicators = [
            "bootstrapapplication(",
            "bootstrapmodule(",
            "platformbrowserdynamic(",
            "import('./bootstrap')",
            'import("./bootstrap")',
        ]
        entry_points = []

        for file in context.repository_root.rglob("main.ts"):
            if self._is_ignored(file):
                continue

            if self._contains_indicator(file, indicators):
                entry_points.append(str(file.relative_to(context.repository_root)))

        return entry_points

    # DETECTS ENTRY POINT FOR JAVA
    def _detect_java(self, context: RepositoryContext) -> list[str]:

        entry_points = []

        indicators = [
            "@springbootapplication",
            "public static void main",
        ]

        for file in context.repository_root.rglob("*.java"):
            if self._is_ignored(file):
                continue

            if self._contains_indicator(file, indicators, match_all=True):
                    entry_points.append(str(file.relative_to(context.repository_root)))
        return entry_points

    # DETECTS ENTRY POINT FOR GO
    def _detect_go(self, context: RepositoryContext) -> list[str]:
        entry_points = []

        indicators = [
            "package main",
            "func main(",
        ]

        for file in context.repository_root.rglob("*.go"):
            if self._is_ignored(file):
                continue

            if self._contains_indicator(file, indicators, match_all=True):
                entry_points.append(str(file.relative_to(context.repository_root)))
        return entry_points

    # DETECTS ENTRY POINT FOR RUST
    def _detect_rust(self, context: RepositoryContext) -> list[str]:
        entry_points = []

        indicators = [
            "fn main(",
        ]

        for file in context.repository_root.rglob("*.rs"):
            if self._is_ignored(file):
                continue

            if self._contains_indicator(file, indicators):
                entry_points.append(str(file.relative_to(context.repository_root)))
        return entry_points

    # IGNORES THE UNWANTED FILES / DIRECTORIES
    def _is_ignored(self, path: Path) -> bool:
        ignored = {
            "node_modules",
            ".git",
            "dist",
            "build",
            "coverage",
            ".angular",
            ".next",
            "target",
            "__pycache__"
        }
    
        return any(part in ignored for part in path.parts)