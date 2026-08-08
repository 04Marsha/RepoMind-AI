import re
import json

from app.models.repository.RepositorySecurity import RepositorySecurity
from app.models.repository.RepositoryContext import RepositoryContext
from app.models.repository.RepositoryOverview import RepositoryOverview

class SecurityAnalyzer:
    def __init__(self, repository_analyzer):
        self.repository_analyzer = repository_analyzer

    def analyze(self, overview, context) -> RepositorySecurity:
        analysis = RepositorySecurity(
            score=50,
            findings=[],
            warnings=[]
        )

        dependencies = overview.dependencies
        dependencies_lower = {
            dep.lower()
            for dep in dependencies
        }

        self.check_authentication(dependencies_lower, analysis)

        self.check_password_hashing(dependencies_lower, analysis)

        self.check_environment_variables(dependencies_lower, analysis)

        self.check_file_uploads(dependencies_lower, analysis)

        self.find_hardcoded_secrets(context, analysis)

        analysis.score = max(
            0,
            min(100, analysis.score)
        )

        return analysis

    def check_authentication(self, dependencies, analysis):

        auth_libraries = [
            "jsonwebtoken",
            "passport",
            "passport-jwt",
            "oauth",
            "oauth2"
        ]

        if "jsonwebtoken" in dependencies:
            analysis.findings.append(
                "JWT authentication detected"
            )
            analysis.score += 10
        elif "flask-jwt-extended" in dependencies:
            analysis.findings.append(
                "JWT authentication detected"
            )
            analysis.score += 10
        elif any(dep in dependencies for dep in auth_libraries):
            analysis.findings.append(
                "Authentication library detected"
            )
            analysis.score += 5
        else:
            analysis.warnings.append(
                "No authentication mechanism detected"
            )

    def check_password_hashing(self, dependencies, analysis):
        hashing_libraries = [
            "bcrypt",
            "bcryptjs",
            "argon2",
            "passlib"
        ]

        has_hashing = any(
            dep in hashing_libraries
            for dep in dependencies
        )

        if "bcrypt" in dependencies:
            analysis.findings.append(
                "Password hashing using bcrypt detected"
            )
            analysis.score += 10
        elif "bcryptjs" in dependencies:
            analysis.findings.append(
                "Password hashing using bcryptjs detected"
            )
            analysis.score += 10
        elif "argon2" in dependencies:
            analysis.findings.append(
                "Password hashing using Argon2 detected"
            )
            analysis.score += 10
        elif "passlib" in dependencies:
            analysis.findings.append(
                "Password hashing detected through Passlib"
            )
            analysis.score += 10
        elif has_hashing:
            analysis.findings.append(
                "Password hashing library detected"
            )
            analysis.score += 5
        else:
            analysis.warnings.append(
                "No password hashing detected"
            )

    def check_environment_variables(self, dependencies, analysis):
        if (
            "dotenv" in dependencies or
            "python-dotenv" in dependencies
        ):
            analysis.findings.append(
                "Environment variables managed using dotenv"
            )
            analysis.score += 10
        else:
            analysis.warnings.append(
                "Environment variable management not detected"
            )

    def check_file_uploads(self, dependencies, analysis):

        if "multer" in dependencies:
            analysis.findings.append(
                "Multipart file upload support detected through multer"
            )
            analysis.score += 5

    def find_hardcoded_secrets(self, context, analysis):

        secret_pattern = re.compile(
            r'(api[_-]?key|secret|password|token)\s*[:=]\s*[\'"][^\'"]+[\'"]',
            re.IGNORECASE
        )

        source_files = self.repository_analyzer.get_source_files(context.project_root)

        for file in source_files:

            try:
                content = file.content

                if not content:
                    continue

                if secret_pattern.search(content):

                    analysis.warnings.append(
                        f"Potential hardcoded secret detected in {file.relative_path}"
                    )

                    analysis.score -= 20

            except Exception:
                continue