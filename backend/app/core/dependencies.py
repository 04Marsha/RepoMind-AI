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

github_service = GithubService()
chunking_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStore()
project_discovery = ProjectDiscovery()
technology_detector = TechnologyDetector()
dependency_parser = DependencyParser()
project_discovery = ProjectDiscovery()

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

def get_repository_overview_service() -> RepositoryAgent:
    return repository_overview_service

def get_project_discovery() -> ProjectDiscovery:
    return project_discovery

def get_repository_intelligence_analyzer():
    return repository_intelligence_analyzer