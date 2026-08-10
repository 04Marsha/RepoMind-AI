from app.models.repository.RepositoryContext import RepositoryContext
from app.models.architecture.Architecture import Architecture

class ArchitectureAnalyzer:

    def __init__(self, technology_detector, project_discovery,):
        self.technology_detector = technology_detector
        self.project_discovery = project_discovery

    # DETECTS THE TYPE OF PROJECT
    def analyze(self, context, overview) -> Architecture:
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

        spring_boot_apps = 0
        for file in context.repository_root.rglob("*.java"):
            try:
                text = file.read_text(encoding="utf-8", errors="ignore")

                if "@SpringBootApplication" in text:
                    spring_boot_apps += 1
            except OSError:
                pass

        architecture.monorepo = len(projects) >= 3
        architecture.microservices = backend_projects > 1 or spring_boot_apps > 1

        # ------- determines the type of architecture of the project -------
        layers = {
            layer.lower()
            for layer in architecture.layers
        }
        requirements = {
            dependency.lower()
            for dependency in overview.dependencies
        }
        ml_tools = {
            "scikit-learn",
            "tensorflow",
            "torch",
            "keras",
            "xgboost",
            "joblib",
            "shap"
        }
        existing_dirs = {
            folder.name.lower()
            for folder in context.repository_root.rglob("*")
            if folder.is_dir()
        }
        has_shell = "shell" in existing_dirs or "host" in existing_dirs
        has_remotes = any("mfe" in d for d in existing_dirs)
        if has_shell and has_remotes:
            architecture.style = "Microfrontend"
        elif {
            "domain",
            "application",
            "infrastructure"
        }.issubset(layers):
            architecture.style = "Clean Architecture"
        elif {
            "controller",
            "service",
            "repository",
            "model"
        }.issubset(layers):
            architecture.style = "Layered"
        elif {
            "controller",
            "model"
        }.issubset(layers):
            architecture.style = "MVC"
        elif any(tool in requirements for tool in ml_tools):
            architecture.style = "ML Pipeline"
        elif architecture.project_type in [
            "Backend",
            "Full Stack"
        ]:
            architecture.style = "Monolith"
        elif frontend and not backend:
            architecture.style = "Component-Based"
        else:
            architecture.style = "Unknown"

        
        #  ------- determines confidence score -------
        score = 0
        if architecture.style != "Unknown":
            score += 40
        if architecture.layers:
            score += 20
        if len(project_technologies) >= 2:
            score += 20
        if architecture.monorepo:
            score += 20
        if architecture.microservices:
            score += 10

        architecture.confidence = min(score, 100) / 100
        return architecture

    # RETURNS THE DIRECTORIES PRESENT IN THE REPO
    def has_directories(self, context: RepositoryContext, *groups):
        existing = {
            folder.name.lower()
            for folder in context.repository_root.rglob("*")
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
            for folder in context.repository_root.rglob("*")
            if folder.is_dir()
        }

        layer_mapping = {
            "Controller": {"controller", "controllers"},
            "Service": {"service", "services"},
            "Repository": {"repository", "repositories", "dao"},
            "Model": {
                "model",
                "models",
                "entity",
                "entities",
                "document",
                "documents",
                "dto",
                "dtos"
            },
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