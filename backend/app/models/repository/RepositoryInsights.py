from pydantic import BaseModel, Field


class RepositoryInsights(BaseModel):
    insights: list[str] = []