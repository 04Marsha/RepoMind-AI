from app.models.repository.RepositoryInsights import RepositoryInsights

class InsightsAnalyzer:

    def analyze(
            self, 
            overview,
            architecture,
            api_analysis,
            database
        ) -> RepositoryInsights:
        insights = set()

        if any(
            dep in overview.dependencies
            for dep in ["jsonwebtoken", "jwt"]
        ):
            insights.add(
                "Implements token-based authentication using JWT"
            )

        if any(
            dep in overview.dependencies
            for dep in ["bcrypt", "bcryptjs"]
        ):
            insights.add(
                "Passwords are securely hashed using bcrypt"
            )

        # Architecture
        if architecture.style != "Unknown":
            insights.add(
                f"Follows {architecture.style} architecture"
            )

        # Database
        if database.entities:
            insights.add(
                f"Persists data through {len(database.entities)} database entities"
            )

        # APIs
        if len(api_analysis.endpoints) > 0:
            insights.add(
                "Exposes REST-style API endpoints"
            )

        # Frontend + Backend
        if architecture.full_stack:
            insights.add(
                "Frontend and backend are separated into distinct layers"
            )

        # Cloudinary
        if "cloudinary" in overview.dependencies:
            insights.add(
                "Supports cloud-based media storage through Cloudinary"
            )

        # Angular Material
        if "@angular/material" in overview.dependencies:
            insights.add(
                "Uses Angular Material for UI components"
            )

        # RxJS
        if "rxjs" in overview.dependencies:
            insights.add(
                "Uses reactive programming patterns through RxJS"
            )

        dependencies_lower = {
            dep.lower()
            for dep in overview.dependencies
        }

        # CORS
        if "cors" in dependencies_lower:
            insights.add(
                "Cross-Origin Resource Sharing (CORS) support detected"
            )
        
        return (
            RepositoryInsights(
                insights=sorted(list(insights))
            )
        )