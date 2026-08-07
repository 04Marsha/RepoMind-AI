from app.models.repository.RepositoryHealth import RepositoryHealth

class RepositoryHealthAnalyzer:

    def analyze(self, overview, intelligence, architecture, api_analysis, database) -> RepositoryHealth:
        score = 100
        strengths = []
        issues = []

        if overview.has_readme:
            strengths.append("README documentation present")
        else:
            score -= 10
            issues.append("README missing")

        if overview.has_license:
            strengths.append("License present")
        else:
            score -= 5
            issues.append("License missing")

        if overview.has_tests:
            strengths.append("Tests detected")
        else:
            score -= 15
            issues.append("No tests detected")

        if overview.dockerized:
            strengths.append("Dockerized")
        else:
            score -= 10
            issues.append("Docker support not found")

        if architecture.style != "Unknown":
            strengths.append(f"{architecture.style} architecture detected")
        else:
            score -= 10
            issues.append("Architecture could not be identified")

        if api_analysis.endpoints:
            strengths.append(f"{len(api_analysis.endpoints)} API endpoints detected")

        if database.entities:
            strengths.append(f"{len(database.entities)} database entities detected")

        if intelligence.primary_language in {
            "TypeScript",
            "Java",
            "Python",
            "Go"
        }:
            strengths.append(f"Uses {intelligence.primary_language}")

        score = max(0, min(score, 100))

        return (
            RepositoryHealth(
                score=score,
                strengths=strengths,
                issues=issues
            )
        )