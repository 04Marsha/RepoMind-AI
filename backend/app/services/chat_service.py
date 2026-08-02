from app.retrieval.retriever import Retriever
from app.services.llm_service import LLMService
from app.models.ChatResponse import ChatResponse

class ChatService:

    def __init__(
        self,
        retriever: Retriever,
        llm_service: LLMService
    ):
        self.retriever = retriever
        self.llm_service = llm_service

    # ANSWERS QUESTIONS BASED ON PROMPTS
    def answer_question(self, question: str) -> str:
        chunks = self.retriever.retrieve(question)
        answer = self.llm_service.generate_answer(question, chunks)

        sources = list(dict.fromkeys(chunk.path for chunk in chunks))

        return ChatResponse(
            answer=answer,
            sources=sources
        )
