import re

from app.analyzers.technology.technology_registry import TECHNOLOGIES
from app.analyzers.dependency.dependency_parser import DependencyParser


class TechnologyDetector:

    def __init__(self, dependency_parser: DependencyParser):
        self.dependency_parser = dependency_parser

    def detect(self, context):
        detected = {}
        dependency_names = set(self.dependency_parser.parse(context.project_root))
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

    def scan_imports(self, context):
        imports = set()

        python_import = re.compile(
            r"^\s*(?:from\s+([A-Za-z0-9_.]+)\s+import|import\s+([A-Za-z0-9_.]+))", re.MULTILINE)

        js_import = re.compile(
            r"""(?:import\s+.*?\s+from\s+['"]([^'"]+)['"]|require\(['"]([^'"]+)['"]\))""")

        java_import = re.compile(
            r"^\s*import\s+([A-Za-z0-9_.]+);", re.MULTILINE)
        
        for file in context.project_root.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix not in {
                ".py",
                ".js",
                ".ts",
                ".tsx",
                ".jsx",
                ".java"
            }:
                continue

            try:
                text = file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            if file.suffix == ".py":
                for a, b in python_import.findall(text):
                    imports.add((a or b).lower())
            elif file.suffix in {".js", ".ts", ".tsx", ".jsx"}:
                for a, b in js_import.findall(text):
                    imports.add((a or b).lower())
            elif file.suffix == ".java":
                for module in java_import.findall(text):
                    imports.add(module.lower())
        return imports