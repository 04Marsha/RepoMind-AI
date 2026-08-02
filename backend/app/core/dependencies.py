from app.services.github_service import GithubService
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.repository_service import RepositoryService
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.retrieval.retriever import Retriever
from app.agents.repository.repository_agent import RepositoryAgent

github_service = GithubService()
repository_analyzer = RepositoryAnalyzer()
chunking_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStore()

repository_service = RepositoryService(
    github_service=github_service,
    repository_analyzer=repository_analyzer,
    chunking_service=chunking_service,
    embedding_service=embedding_service,
    vector_store=vector_store
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
    repository_analyzer=repository_analyzer
)

def get_repository_overview_service() -> RepositoryAgent:
    return repository_overview_service