from pydantic import BaseModel, Field

from app.models.api.ApiEndpoint import ApiEndpoint


class ApiAnalysis(BaseModel):
    endpoints: list[ApiEndpoint] = Field(default_factory=list)