"""
Common error handling module for the AI-Interactive Book backend.
"""
from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel

class APIError(BaseModel):
    """Standard API error response format."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[str] = None

class AIBookException(Exception):
    """Base exception class for the AI Interactive Book application."""
    def __init__(self, message: str, error_code: str = "GENERIC_ERROR", details: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(message)

class DocumentProcessingError(AIBookException):
    """Raised when there's an error processing a document."""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, "DOCUMENT_PROCESSING_ERROR", details)

class VectorStoreError(AIBookException):
    """Raised when there's an error with the vector store."""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, "VECTOR_STORE_ERROR", details)

class ChatError(AIBookException):
    """Raised when there's an error with the chat functionality."""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, "CHAT_ERROR", details)

class AuthError(AIBookException):
    """Raised when there's an authentication/authorization error."""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, "AUTH_ERROR", details)

class PersonalizationError(AIBookException):
    """Raised when there's an error with personalization features."""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, "PERSONALIZATION_ERROR", details)

class TranslationError(AIBookException):
    """Raised when there's an error with translation features."""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, "TRANSLATION_ERROR", details)

def handle_exception(exception: Exception, context: str = "") -> APIError:
    """
    Convert an exception to a standardized APIError response.

    Args:
        exception: The exception to handle
        context: Additional context about where the error occurred

    Returns:
        APIError with standardized format
    """
    if isinstance(exception, AIBookException):
        return APIError(
            success=False,
            error_code=exception.error_code,
            message=exception.message,
            details=f"{context}: {exception.details}" if context and exception.details else (exception.details or context)
        )
    elif isinstance(exception, HTTPException):
        return APIError(
            success=False,
            error_code="HTTP_ERROR",
            message=exception.detail,
            details=f"HTTP {exception.status_code} in {context}" if context else f"HTTP {exception.status_code}"
        )
    else:
        # For unexpected errors, provide a generic message for security
        return APIError(
            success=False,
            error_code="INTERNAL_ERROR",
            message="An internal error occurred",
            details=f"{type(exception).__name__} in {context}: {str(exception)}" if context else str(exception)
        )

def raise_http_exception_from_aibook_exception(exc: AIBookException):
    """
    Convert an AIBookException to an HTTPException that FastAPI can handle.

    Args:
        exc: The AIBookException to convert
    """
    status_code = status.HTTP_400_BAD_REQUEST
    if exc.error_code == "AUTH_ERROR":
        status_code = status.HTTP_401_UNAUTHORIZED
    elif exc.error_code == "INTERNAL_ERROR":
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    raise HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )