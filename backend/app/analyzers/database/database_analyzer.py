import re

from app.models.database.DatabaseAnalysis import DatabaseAnalysis
from app.models.repository.RepositoryContext import RepositoryContext
from app.models.database.DatabaseEntity import DatabaseEntity

class DatabaseAnalyzer:

    def __init__(self, repository_analyzer):
        self.repository_analyzer = repository_analyzer

    def analyze(self, context: RepositoryContext) -> DatabaseAnalysis:
        analysis = DatabaseAnalysis()

        analysis.entities.extend(
            self.detect_sql_tables(context)
        )

        analysis.entities.extend(
            self.detect_sqlalchemy(context)
        )

        analysis.entities.extend(
            self.detect_mongoose(context)
        )

        analysis.entities.extend(
            self.detect_jpa(context)
        )

        unique_entities = {
            (e.name, e.type, e.file): e 
            for e in analysis.entities
        }

        analysis.entities = list(unique_entities.values())
        return analysis

    # DETECTS SQL TABLES
    def detect_sql_tables(self, context: RepositoryContext) -> list[DatabaseEntity]:
        entities = []

        pattern = re.compile(r'CREATE\s+TABLE\s+([A-Za-z_][A-Za-z0-9_]*)', re.IGNORECASE)

        for file in self.repository_analyzer.get_source_files(context.project_root):
            if file.suffix != ".sql":
                continue

            text = file.read_text(encoding="utf-8",errors="ignore")

            for match in pattern.finditer(text):
                entities.append(
                    DatabaseEntity(
                        name=match.group(1),
                        type="SQL Table",
                        file=str(file.relative_to(context.project_root))
                    )
                )
        return entities

    # DETECTS SQLAlchemy TABLES
    def detect_sqlalchemy(self, context: RepositoryContext) -> list[DatabaseEntity]:
        entities = []
    
        pattern = re.compile(r'class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*Base[^)]*\)')
    
        for file in self.repository_analyzer.get_source_files(context.project_root):
            if file.suffix != ".py":
                continue
    
            text = file.read_text(encoding="utf-8",errors="ignore")
    
            for match in pattern.finditer(text):
                entities.append(
                    DatabaseEntity(
                        name=match.group(1),
                        type="SQLAlchemy Model",
                        file=str(file.relative_to(context.project_root))
                    )
                )
        return entities

    # DETECTS Mongoose TABLES
    def detect_mongoose(self, context: RepositoryContext) -> list[DatabaseEntity]:
        entities = []
        
        pattern = re.compile(r'mongoose\.model\(\s*[\'"]([^\'"]+)[\'"]')
        
        for file in self.repository_analyzer.get_source_files(context.project_root):
            if file.suffix not in {".js", ".ts"}:
                continue
        
            text = file.read_text(encoding="utf-8",errors="ignore")
        
            for match in pattern.finditer(text):
                entities.append(
                    DatabaseEntity(
                        name=match.group(1),
                        type="Mongoose Model",
                        file=str(file.relative_to(context.project_root))
                    )
                )
        return entities

    # DETECTS JPA TABLES
    def detect_jpa(self, context: RepositoryContext) -> list[DatabaseEntity]:
        entities = []
            
        pattern = re.compile(r'@Entity.*?class\s+([A-Za-z_][A-Za-z0-9_]*)', re.DOTALL)
            
        for file in self.repository_analyzer.get_source_files(context.project_root):
            if file.suffix != ".java":
                continue
            
            text = file.read_text(encoding="utf-8",errors="ignore")
            
            for match in pattern.finditer(text):
                entities.append(
                    DatabaseEntity(
                        name=match.group(1),
                        type="JPA Entity",
                        file=str(file.relative_to(context.project_root))
                    )
                )
        return entities