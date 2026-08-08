from app.models.metrics.Complexity import Complexity

class ComplexityAnalyzer:
    def __init__(self, technology_detector):
        self.technology_detector = technology_detector

    def analyze(self, context, intelligence, architecture, api_analysis, database, metrics) -> Complexity:
        complexity = Complexity()
        technologies = self.technology_detector.detect(context)
        score = 0
        reasons = []

        if architecture.full_stack:
            score += 25
            reasons.append("Full Stack application")
        elif architecture.project_type == "Backend":
            score += 10
            reasons.append("Backend application")
        elif architecture.project_type == "Frontend":
            score += 10
            reasons.append("Frontend application")

        endpoint_count = len(api_analysis.endpoints)

        if endpoint_count >= 20:
            score += 20
            reasons.append(f"{endpoint_count} API endpoints")
        elif endpoint_count >= 5:
            score += 10
            reasons.append(f"{endpoint_count} API endpoints")
        elif endpoint_count > 0:
            score += 5
            reasons.append(f"{endpoint_count} API endpoints")

        entity_count = len(database.entities)

        if entity_count >= 10:
            score += 20
            reasons.append(f"{entity_count} database entities")
        elif entity_count >= 3:
            score += 10
            reasons.append(f"{entity_count} database entities")
        elif entity_count > 0:
            score += 5
            reasons.append(f"{entity_count} database entities")

        if architecture.style != "Unknown":
            score += 15
            reasons.append(f"{architecture.style} architecture")

        if metrics.source_files >= 100:
            score += 15
            reasons.append(f"{metrics.source_files} source files")
        elif metrics.source_files >= 30:
            score += 10
            reasons.append(f"{metrics.source_files} source files")

        advanced = (
            intelligence.databases +
            intelligence.orms +
            intelligence.vector_databases
        )

        if advanced:
            score += 10
            reasons.append("Uses database technologies")

        ml_count = len(
            [
                tech
                for tech in technologies
                if tech.category == 'machine_learning'
            ]
        )

        if ml_count:
            score += 15
            reasons.append("Machine Learning functionality")

        if score >= 70:
            complexity.level = "Advanced"
        elif score >= 40:
            complexity.level = "Intermediate"
        else:
            complexity.level = "Beginner"

        complexity.score = min(score, 100)
        complexity.reasons = reasons

        return complexity