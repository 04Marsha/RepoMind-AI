from app.models.repository.FileMetadata import FileMetadata
from app.models.chat.TextChunk import TextChunk

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

class ChunkingService:

    # BREAKS THE FILE INTO CHUNKS OF SPECIFIC SIZES
    def chunk_file(self, file: FileMetadata) -> list[TextChunk]:
        chunks = []

        start = 0
        chunk_number = 1

        while start < len(file.content):
            end = start + CHUNK_SIZE
            content = file.content[start:end]

            chunks.append(TextChunk(
                path=file.path,
                language=file.language,
                content=content,
                chunk_number=chunk_number
            ))

            if end >= len(file.content):
                break
            
            start = end - CHUNK_OVERLAP
            chunk_number += 1

        return chunks