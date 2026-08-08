from pydantic import BaseModel, Field


class RepositoryInsights(BaseModel):
    insights: list[str] = Field(default_factory=list)