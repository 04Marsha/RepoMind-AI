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

        frameworks = (
            intelligence.backend_frameworks +
            intelligence.frontend_frameworks
        )

        summary_parts = [
            f"{overview.repository_name} is a "
            f"{architecture.project_type.lower()} application"
        ]

        if intelligence.primary_language:
            summary_parts.append(
                f"primarily written in {intelligence.primary_language}"
            )

        if frameworks:
            summary_parts.append(
                f"using {', '.join(frameworks)}"
            )

        summary = " ".join(summary_parts) + "."

        if architecture.style != "Unknown":
            summary += (
                f" The project follows a "
                f"{architecture.style} architecture."
            )

        endpoint_count = len(api_analysis.endpoints)

        if endpoint_count:
            summary += (
                f" It exposes {endpoint_count} API endpoints."
            )

        entity_count = len(database.entities)

        if entity_count:
            summary += (
                f" It manages {entity_count} database entities."
            )

        if intelligence.databases:
            database_text = ", ".join(intelligence.databases)

            if intelligence.orms:
                database_text += (
                    f" through {', '.join(intelligence.orms)}"
                )

            summary += (
                f" Data is persisted using "
                f"{database_text}."
            )

        if intelligence.testing_frameworks:
            summary += (
                f" Testing is implemented using "
                f"{', '.join(intelligence.testing_frameworks)}."
            )

        return RepositorySummary(
            summary=summary
        )