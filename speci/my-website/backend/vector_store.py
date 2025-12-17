"""
Vector storage module for the AI-Interactive Book backend.
Handles similarity search using Qdrant vector database.
For demonstration purposes, this implementation uses a mock vector store
since the full implementation requires memory-intensive ML libraries.
"""
from typing import List, Dict, Any, Optional
import uuid
import hashlib
from .config import settings
from .errors import VectorStoreError

class VectorStore:
    """
    Manages document storage and similarity search (mock implementation).
    """

    def __init__(self):
        try:
            # In-memory storage for demonstration
            self._documents = {}
            self.collection_name = "book_documents"
        except Exception as e:
            raise VectorStoreError(
                f"Failed to initialize vector store: {str(e)}",
                details=f"Error: {type(e).__name__}"
            )

    def store_document_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Store document chunks in the mock vector database.

        Args:
            chunks: List of document chunks with content and metadata

        Returns:
            True if successful, False otherwise
        """
        if not chunks:
            raise VectorStoreError("No chunks provided to store", details="Empty chunks list")

        try:
            for chunk in chunks:
                # Store the chunk with its ID
                self._documents[chunk["id"]] = {
                    "content": chunk["content"],
                    "source": chunk["source"],
                    "chunk_index": chunk["chunk_index"],
                    "total_chunks": chunk["total_chunks"],
                    # Create a simple hash-based "embedding" for similarity
                    "embedding_hash": hashlib.md5(chunk["content"].encode()).hexdigest()
                }
            return True
        except Exception as e:
            raise VectorStoreError(
                f"Failed to store document chunks: {str(e)}",
                details=f"Number of chunks: {len(chunks)}, Error: {type(e).__name__}"
            )

    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar document chunks to the query (mock implementation).

        Args:
            query: The search query
            limit: Maximum number of results to return

        Returns:
            List of similar document chunks with similarity scores
        """
        if not query:
            raise VectorStoreError("Search query cannot be empty", details="Empty query string")

        try:
            # Simple keyword-based similarity for demonstration
            query_lower = query.lower()
            results = []

            for doc_id, doc_data in self._documents.items():
                content_lower = doc_data["content"].lower()

                # Calculate a simple similarity score based on keyword matches
                score = 0
                query_words = query_lower.split()

                for word in query_words:
                    if word in content_lower:
                        score += 1

                # Normalize score based on content length to prevent bias toward longer documents
                if len(content_lower) > 0:
                    score = score / len(query_words) if len(query_words) > 0 else 0

                if score > 0:  # Only include results with some similarity
                    results.append({
                        "id": doc_id,
                        "content": doc_data["content"],
                        "source": doc_data["source"],
                        "chunk_index": doc_data["chunk_index"],
                        "total_chunks": doc_data["total_chunks"],
                        "score": score
                    })

            # Sort by score in descending order and limit results
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:limit]

        except Exception as e:
            raise VectorStoreError(
                f"Failed to search for similar documents: {str(e)}",
                details=f"Query: {query[:50]}..., Error: {type(e).__name__}"
            )

    def get_all_sources(self) -> List[str]:
        """
        Get all unique document sources in the vector store.

        Returns:
            List of unique source identifiers
        """
        try:
            sources = set()
            for doc_data in self._documents.values():
                sources.add(doc_data["source"])
            return list(sources)
        except Exception as e:
            raise VectorStoreError(
                f"Failed to retrieve all document sources: {str(e)}",
                details=f"Error: {type(e).__name__}"
            )

    def delete_document(self, source: str) -> bool:
        """
        Delete all chunks associated with a document source.

        Args:
            source: The source identifier of the document to delete

        Returns:
            True if successful, False otherwise
        """
        if not source:
            raise VectorStoreError("Document source cannot be empty", details="Empty source identifier")

        try:
            # Find and remove all chunks with this source
            ids_to_remove = []
            for doc_id, doc_data in self._documents.items():
                if doc_data["source"] == source:
                    ids_to_remove.append(doc_id)

            for doc_id in ids_to_remove:
                del self._documents[doc_id]

            return True
        except Exception as e:
            raise VectorStoreError(
                f"Failed to delete document from vector store: {str(e)}",
                details=f"Source: {source}, Error: {type(e).__name__}"
            )

# Global instance
vector_store = VectorStore()