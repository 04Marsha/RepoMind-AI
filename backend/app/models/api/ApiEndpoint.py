from pydantic import BaseModel

class ApiEndpoint(BaseModel):
    framework: str
    method: str
    path: str
    router: str | None = None
    handler: str
    file: str