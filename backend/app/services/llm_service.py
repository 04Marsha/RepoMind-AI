from google import genai

from app.models.TextChunk import TextChunk
from app.core.config import Settings

class LLMService:

    def __init__(self):
        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )
        self.model = Settings.MODEL

    # BUILDS PROMPTS
    def _build_prompt(self, question: str, context: list[TextChunk]) -> str:
        context_text = "\n\n".join(f"File: {chunk.path}\n{chunk.content}" for chunk in context)

        return f"""
        You are an expert software engineer.
        You are answering questions about a GitHub repository.
        Use ONLY the repository context below.
        If the answer cannot be found in the context, say
        "I couldn't find that information in the indexed repository."
        Do not make up information.
        Repository Context:
        {context_text}
        User Question:
        {question}
        """

    # ANSWERS TO THE QUESTIONS
    def generate_answer(self, question: str, context: list[TextChunk]) -> str:

        prompt = self._build_prompt(question, context)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text