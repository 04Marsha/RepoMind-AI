import re

from app.analyzers.technology.technology_registry import TECHNOLOGIES
from app.analyzers.repository.constants import DEPENDENCY_FILES


class TechnologyDetector:

    def detect(self, context):
        detected = {}
        dependency_names = self.parse_dependencies(context)
        config_files = self.find_config_files(context)
        imports = self.scan_imports(context)

        for technology in TECHNOLOGIES:

            if technology.matches(
                dependency_names,
                config_files,
                imports
            ):
                detected[technology.name] = technology

        return list(detected.values())

    def find_config_files(self, context):
        config_files = set()
        for file in context.project_root.rglob("*"):
            if file.is_file():
                config_files.add(file.name)
        return config_files

    def parse_dependencies(self, context):
        dependencies = set()

        for file in context.project_root.rglob("*"):
            if file.name not in DEPENDENCY_FILES:
                continue

            content = file.read_text(encoding="utf-8", errors="ignore").lower()
            words = re.findall(r"[A-Za-z0-9@._/-]+", content)

            dependencies.update(words)
        return dependencies

    def scan_imports(self, context):
        imports = set()

        for file in context.project_root.rglob("*"):
            if file.suffix not in {
                ".py",
                ".js",
                ".ts",
                ".tsx",
                ".jsx",
                ".java"
            }:
                continue

            text = file.read_text(encoding="utf-8", errors="ignore").lower()

            imports.update(re.findall(r"[A-Za-z0-9@._/-]+",text))

        return imports