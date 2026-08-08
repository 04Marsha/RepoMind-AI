from app.services.github.github_service import GithubService
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.services.retrieval.chunking_service import ChunkingService
from app.services.retrieval.embedding_service import EmbeddingService
from app.services.retrieval.vector_store import VectorStore
from app.services.repository.repository_service import RepositoryService
from app.services.chat.chat_service import ChatService
from app.services.llm.llm_service import LLMService
from app.retrieval.retriever import Retriever
from app.agents.repository.repository_agent import RepositoryAgent
from app.discovery.project_discovery import ProjectDiscovery
from app.services.indexing.repository_indexing_service import RepositoryIndexingService
from app.analyzers.technology.technology_detector import TechnologyDetector
from app.analyzers.repository.repository_intelligence_analyzer import RepositoryIntelligenceAnalyzer
from app.analyzers.dependency.dependency_parser import DependencyParser
from app.discovery.project_discovery import ProjectDiscovery
from app.analyzers.structure.structure_analyzer import StructureAnalyzer
from app.analyzers.metrics.metrics_analyzer import MetricsAnalyzer
from app.analyzers.architecture.architecture_analyzer import ArchitectureAnalyzer
from app.analyzers.api.api_endpoint_analyzer import ApiEndpointAnalyzer
from app.analyzers.database.database_analyzer import DatabaseAnalyzer
from app.analyzers.repository.repository_summary_generator import RepositorySummaryGenerator
from app.analyzers.repository.repository_health_analyzer import RepositoryHealthAnalyzer
from app.analyzers.metrics.complexity_analyzer import ComplexityAnalyzer
from app.analyzers.repository.insights_analyzer import InsightsAnalyzer
from app.analyzers.repository.security_analyzer import SecurityAnalyzer

github_service = GithubService()
chunking_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStore()
project_discovery = ProjectDiscovery()
dependency_parser = DependencyParser()

repository_analyzer = RepositoryAnalyzer(
    dependency_parser=dependency_parser
)

repository_indexing_service = RepositoryIndexingService(
    repository_analyzer=repository_analyzer,
    chunking_service=chunking_service,
    embedding_service=embedding_service,
    vector_store=vector_store
)

repository_service = RepositoryService(
    github_service=github_service,
    repository_analyzer=repository_analyzer,
    project_discovery=project_discovery,
    repository_indexing_service=repository_indexing_service,
    vector_store=vector_store
)

technology_detector = TechnologyDetector(
    dependency_parser=dependency_parser
)

repository_intelligence_analyzer = RepositoryIntelligenceAnalyzer(
    repository_analyzer,
    technology_detector
)

retriever = Retriever(
    embedding_service=embedding_service,
    vector_store=vector_store
)

llm_service = LLMService()

chat_service = ChatService(
    retriever=retriever,
    llm_service=llm_service
)

repository_overview_service = RepositoryAgent(
    repository_analyzer=repository_analyzer,
    repository_intelligence_analyzer=repository_intelligence_analyzer,
    project_discovery=project_discovery
)

structure_analyzer = StructureAnalyzer()
metrics_analyzer = MetricsAnalyzer(
    repository_analyzer=repository_analyzer
)
architecture_analyzer = ArchitectureAnalyzer(
    technology_detector=technology_detector,
    project_discovery=project_discovery
)

api_endpoint_analyzer = ApiEndpointAnalyzer(
    repository_analyzer=repository_analyzer
)

database_analyzer = DatabaseAnalyzer(
    repository_analyzer=repository_analyzer
)

repository_summary_generator = RepositorySummaryGenerator()

repository_health_analyzer = RepositoryHealthAnalyzer()

complexity_analyzer = ComplexityAnalyzer(
    technology_detector=technology_detector
)

security_analyzer = SecurityAnalyzer(
    repository_analyzer=repository_analyzer
)

insights_analyzer = InsightsAnalyzer()

def get_repository_overview_service() -> RepositoryAgent:
    return repository_overview_service

def get_project_discovery() -> ProjectDiscovery:
    return project_discovery

def get_repository_intelligence_analyzer():
    return repository_intelligence_analyzer

def get_structure_analyzer():
    return structure_analyzer

def get_metrics_analyzer():
    return metrics_analyzer

def get_architecture_analyzer():
    return architecture_analyzer

def get_api_endpoint_analyzer():
    return api_endpoint_analyzer

def get_database_analyzer():
    return database_analyzer

def get_repository_agent():
    return RepositoryAgent(
        repository_analyzer=repository_analyzer,
        repository_intelligence_analyzer=repository_intelligence_analyzer,
        project_discovery=project_discovery,
        structure_analyzer=structure_analyzer,
        metrics_analyzer=metrics_analyzer,
        architecture_analyzer=architecture_analyzer,
        api_endpoint_analyzer=api_endpoint_analyzer,
        database_analyzer=database_analyzer,
        repository_summary_generator=repository_summary_generator,
        repository_health_analyzer=repository_health_analyzer,
        complexity_analyzer=complexity_analyzer,
        insights_analyzer=insights_analyzer,
        security_analyzer=security_analyzer
    )