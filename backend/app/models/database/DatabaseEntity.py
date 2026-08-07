from pydantic import BaseModel

class DatabaseEntity(BaseModel):
    name: str
    type: str
    file: str