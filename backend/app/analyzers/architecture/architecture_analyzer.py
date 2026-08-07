from app.models.repository.RepositoryContext import RepositoryContext
from app.models.architecture.Architecture import Architecture

class ArchitectureAnalyzer:

    def __init__(self, technology_detector, project_discovery,):
        self.technology_detector = technology_detector
        self.project_discovery = project_discovery

    # DETECTS THE TYPE OF PROJECT
    def analyze(self, context: RepositoryContext) -> Architecture:
        architecture = Architecture()
        project_technologies = self.technology_detector.detect(context)
        architecture.layers = self.detect_layers(context)


        # ------- checks if the project is frontend, backend or both -------
        backend = any(
            tech.category == "backend_framework"
            for tech in project_technologies
        )
        frontend = any(
            tech.category == "frontend_framework"
            for tech in project_technologies
        )
        backend_projects = 0

        architecture.full_stack = backend and frontend

        if architecture.full_stack:
            architecture.project_type = "Full Stack"
        elif backend:
            architecture.project_type = "Backend"
        elif frontend:
            architecture.project_type = "Frontend"
        else:
            architecture.project_type = "Library"

        projects = self.project_discovery.discover_all(context.repository_root)

        for project in projects:
            project_stack = self.technology_detector.detect(project)

            if any (tech.category == "backend_framework"
                    for tech in project_stack
                ):
                backend_projects += 1

        architecture.monorepo = len(projects) > 1
        architecture.microservices = backend_projects > 1

        # ------- determines the type of architecture of the project -------
        layers = set(architecture.layers)
        if {
            "Controller",
            "Service",
            "Repository",
            "Model"
        }.issubset(layers):
            architecture.style = "Layered"
        elif {
            "Controller",
            "Model"
        }.issubset(layers):
            architecture.style = "MVC"
        elif {
            "Domain",
            "Application",
            "Infrastructure"
        }.issubset(layers):
            architecture.style = "Clean Architecture"
        else:
            architecture.style = "Unknown"

        #  ------- determines confidence score -------
        score = sum([
            architecture.project_type is not None,
            architecture.style != "Unknown",
            bool(architecture.layers),
            bool(project_technologies),
        ])

        architecture.confidence = score / 4
        return architecture

    # RETURNS THE DIRECTORIES PRESENT IN THE REPO
    def has_directories(self, context: RepositoryContext, *groups):
        existing = {
            folder.name.lower()
            for folder in context.project_root.rglob("*")
            if folder.is_dir()
        }

        return all(
            any(option in existing for option in group)
            for group in groups
        )

    # DETERMINES THE LAYERS IN THE ARCHITECTURE
    def detect_layers(self, context):
        existing = {
            folder.name.lower()
            for folder in context.project_root.rglob("*")
            if folder.is_dir()
        }

        layer_mapping = {
            "Controller": {"controller", "controllers"},
            "Service": {"service", "services"},
            "Repository": {"repository", "repositories", "dao"},
            "Model": {"model", "models", "entity", "entities"},
            "Route": {"route", "routes"},
            "Middleware": {"middleware", "middlewares"},
            "View": {"view", "views"},
            "Domain": {"domain", "domains"},
            "Application": {"application", "applications"},
            "Infrastructure": {"infrastructure", "infrastructures"},
            "Presentation": {"presentation"},
        }

        layers = []

        for layer, names in layer_mapping.items():
            if any(name in existing for name in names):
                layers.append(layer)
        return layers