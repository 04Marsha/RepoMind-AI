from pathlib import Path
import json
from collections.abc import Iterable
import tomllib
import xml.etree.ElementTree as ET
import re

class DependencyParser:
    def _add_dependencies(self, dependencies: set[str], packages: Iterable[str]):
        dependencies.update(packages)

    def parse(self, project_root: Path) -> list[str]:
        print(project_root)
        dependencies = set()

        package_json = project_root / "package.json"
        requirements = project_root / "requirements.txt"
        pyproject = project_root / "pyproject.toml"
        pom = project_root / "pom.xml"
        gradle = project_root / "build.gradle"
        cargo = project_root / "Cargo.toml"
        go_mod = project_root / "go.mod"

        if package_json.exists():
            self._add_dependencies(dependencies, self.parse_package_json(package_json))
        if requirements.exists():
            self._add_dependencies(dependencies, self.parse_requirements(requirements))
        if pyproject.exists():
            self._add_dependencies(dependencies, self.parse_pyproject(pyproject))
        if pom.exists():
            self._add_dependencies(dependencies, self.parse_pom(pom))
        if gradle.exists():
            self._add_dependencies(dependencies, self.parse_gradle(gradle))
        if cargo.exists():
            self._add_dependencies(dependencies, self.parse_cargo(cargo))
        if go_mod.exists():
            self._add_dependencies(dependencies, self.parse_go_mod(go_mod))

        return sorted(dependencies)

    # FOR PACKAGE.JSON PARSING
    def parse_package_json(self, path: Path) -> list[str]:
        try:
            package = json.loads(path.read_text(encoding="utf-8"))

            dependencies = set()

            self._add_dependencies(dependencies, package.get("dependencies", {}).keys())
            self._add_dependencies(dependencies, package.get("devDependencies", {}).keys())

            return sorted(dependencies)
        except (OSError, json.JSONDecodeError):
            return []

    # FOR REQUIREMENTS.TXT PARSING
    def parse_requirements(self, path: Path) -> list[str]:
        dependencies = set()

        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                package = (line
                           .split("==")[0]
                           .split(">=")[0]
                           .split("<=")[0]
                           .split("~=")[0]
                           .split("[")[0]
                           .strip()
                        )

                if package:
                    self._add_dependencies(dependencies, [package])

        except Exception:
            pass

        return sorted(dependencies)

    def parse_pyproject(self, path: Path) -> list[str]:
        try:
            with path.open("rb") as file:
                project = tomllib.load(file)
            dependencies = set()

             # PEP 621
            self._add_dependencies(dependencies,[
                dependency.split()[0].split(">=")[0].split("==")[0]
                for dependency in project.get("project", {}).get("dependencies", [])
            ])

            # Poetry
            poetry_dependencies = (project.get("tool", {}).get("poetry", {}).get("dependencies", {}))

            self._add_dependencies(dependencies, [package
                for package in poetry_dependencies.keys()
                if package != "python"
            ])

            return sorted(dependencies)
        except (OSError, tomllib.TOMLDecodeError):
            return []

    def parse_pom(self, path: Path):
        try:
            tree = ET.parse(path)
            root = tree.getroot()

            namespace = {
                "m": "http://maven.apache.org/POM/4.0.0"
            }

            dependencies = set()

            for dependency in root.findall(".//m:dependency", namespace):
                artifact = dependency.find("m:artifactId", namespace)

                if artifact is not None and artifact.text:
                    dependencies.add(artifact.text)
            return sorted(dependencies)

        except (OSError, ET.ParseError):
            return []

    def parse_cargo(self, path: Path):
        try:
            with path.open("rb") as file:
                cargo = tomllib.load(file)

            dependencies = set()

            self._add_dependencies(dependencies, cargo.get("dependencies", {}).keys())

            return sorted(dependencies)
        except (OSError, tomllib.TOMLDecodeError):
            return []

    def parse_gradle(self, path: Path):
        dependencies = set()

        pattern = r'["\']([^:"\']+):([^:"\']+):[^"\']+["\']'

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for _, artifact in re.findall(pattern, text):
                dependencies.add(artifact)
        except OSError:
            pass
        return sorted(dependencies)

    def parse_go_mod(self, path: Path):
        dependencies = set()

        try:
            inside_require = False

            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()

                if line.startswith("require ("):
                    inside_require = True
                    continue
                if inside_require and line == ")":
                    inside_require = False
                    continue
                if inside_require:
                    package = line.split()[0]
                    dependencies.add(package)
                elif line.startswith("require "):
                    package = line.split()[1]
                    dependencies.add(package)
            return sorted(dependencies)

        except OSError:
            return []