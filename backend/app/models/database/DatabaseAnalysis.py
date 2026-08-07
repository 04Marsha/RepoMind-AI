from pydantic import BaseModel

from app.models.database.DatabaseEntity import DatabaseEntity

class DatabaseAnalysis(BaseModel):
    entities: list[DatabaseEntity] = []