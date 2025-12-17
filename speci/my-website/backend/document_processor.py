"""
Document processing module for the AI-Interactive Book backend.
Handles document indexing and preprocessing for the RAG system.
"""
import hashlib
from typing import List, Dict, Any
from pathlib import Path
from .errors import DocumentProcessingError

class DocumentProcessor:
    """
    Processes documents for indexing in the vector database.
    """

    def __init__(self):
        self.chunk_size = 1000  # characters per chunk
        self.overlap = 100  # overlap between chunks

    def process_document(self, content: str, source: str) -> List[Dict[str, Any]]:
        """
        Process a document into chunks suitable for vector storage.

        Args:
            content: The raw document content
            source: Source identifier for the document

        Returns:
            List of document chunks with metadata
        """
        try:
            if not content:
                raise DocumentProcessingError("Document content cannot be empty", details=f"Source: {source}")

            chunks = self._chunk_text(content)
            processed_chunks = []

            for i, chunk in enumerate(chunks):
                chunk_hash = hashlib.md5(f"{source}_{i}_{chunk}".encode()).hexdigest()
                processed_chunk = {
                    "id": f"{source}_chunk_{i}_{chunk_hash[:8]}",
                    "content": chunk,
                    "source": source,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                processed_chunks.append(processed_chunk)

            return processed_chunks
        except Exception as e:
            if isinstance(e, DocumentProcessingError):
                raise
            else:
                raise DocumentProcessingError(
                    f"Failed to process document: {str(e)}",
                    details=f"Source: {source}, Error: {type(e).__name__}"
                )

    def _chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: The text to chunk

        Returns:
            List of text chunks
        """
        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # If we're near the end, include the rest
            if end >= len(text):
                chunks.append(text[start:])
                break

            # Try to break at sentence boundary
            chunk = text[start:end]
            last_period = chunk.rfind('.')
            last_exclamation = chunk.rfind('!')
            last_question = chunk.rfind('?')
            last_space = chunk.rfind(' ')

            # Find the best break point
            break_point = max(
                last_period if last_period != -1 else -1,
                last_exclamation if last_exclamation != -1 else -1,
                last_question if last_question != -1 else -1,
                last_space if last_space != -1 else -1
            )

            if break_point != -1 and break_point > len(chunk) // 2:
                # Break at the punctuation/space
                actual_end = start + break_point + 1
                chunks.append(text[start:actual_end])
                start = actual_end - self.overlap
            else:
                # No good break point found, just break at the limit
                chunks.append(text[start:end])
                start = end - self.overlap

            # Ensure we make progress
            if start <= end - self.overlap:
                start = end - self.overlap
            elif start < len(text):
                # If overlap would cause infinite loop, just move forward
                start += self.chunk_size

        # Remove empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]
        return chunks

    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a document file into chunks.

        Args:
            file_path: Path to the document file

        Returns:
            List of document chunks with metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return self.process_document(content, file_path)
        except FileNotFoundError:
            raise DocumentProcessingError(
                f"Document file not found: {file_path}",
                details=f"File path: {file_path}"
            )
        except UnicodeDecodeError:
            raise DocumentProcessingError(
                f"Document file contains invalid characters: {file_path}",
                details=f"File path: {file_path}, encoding: utf-8"
            )
        except Exception as e:
            raise DocumentProcessingError(
                f"Failed to process document file: {str(e)}",
                details=f"File path: {file_path}, Error: {type(e).__name__}"
            )

# Global instance
document_processor = DocumentProcessor()