from pydantic import BaseModel

from app.models.repository.RepositoryOverview import RepositoryOverview
from app.models.repository.RepositoryIntelligence import RepositoryIntelligence
from app.models.structure.ProjectStructure import ProjectStructure
from app.models.metrics.CodeMetrics import CodeMetrics
from app.models.architecture.Architecture import Architecture
from app.models.api.ApiAnalysis import ApiAnalysis
from app.models.database.DatabaseAnalysis import DatabaseAnalysis
from app.models.repository.RepositoryHealth import RepositoryHealth

class RepositoryAgentModel(BaseModel):
    overview: RepositoryOverview
    intelligence: RepositoryIntelligence
    structure: ProjectStructure
    metrics: CodeMetrics
    architecture: Architecture
    api_analysis: ApiAnalysis
    database: DatabaseAnalysis
    summary: str
    health: RepositoryHealth