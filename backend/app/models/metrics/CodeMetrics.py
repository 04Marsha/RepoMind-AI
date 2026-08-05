from pydantic import BaseModel

class CodeMetrics(BaseModel):
    total_files: int = 0
    source_files: int = 0
    total_directories: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    average_file_size: float = 0