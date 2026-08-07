from app.models.repository.RepositorySummary import RepositorySummary

class RepositorySummaryGenerator:

    def generate_summary(
            self, 
            overview, 
            intelligence, 
            architecture, 
            api_analysis, 
            database
    ) -> RepositorySummary:
        parts = []

        parts.append(
            f"{overview.repository_name} is a "
            f"{architecture.project_type.lower()} application"
        )

        if intelligence.primary_language:
            parts.append(
                f"primarily written in {intelligence.primary_language}"
            )

        frameworks = (
            intelligence.frontend_frameworks +
            intelligence.backend_frameworks
        )

        if frameworks:
            parts.append(
                f"using {', '.join(frameworks)}"
            )

        if intelligence.databases:
            database_text = ", ".join(intelligence.databases)

            if intelligence.orms:
                database_text += (
                    f" with {', '.join(intelligence.orms)}"
                )

            parts.append(
                f"for data persistence through {database_text}"
            )

        summary = " ".join(parts) + "."

        extra = []

        if architecture.style != "Unknown":
            extra.append(
                f"The project follows a "
                f"{architecture.style} architecture"
            )

            if architecture.layers:
                extra.append(
                    f"with layers: "
                    f"{', '.join(architecture.layers)}"
                )

        endpoint_count = len(api_analysis.endpoints)

        if endpoint_count:
            extra.append(
                f"It exposes {endpoint_count} API endpoints"
            )

        entity_count = len(database.entities)

        if entity_count:
            extra.append(
                f"and contains {entity_count} database entities"
            )

        if extra:
            summary += " " + " ".join(extra) + "."

        return RepositorySummary(
            summary=summary
        )