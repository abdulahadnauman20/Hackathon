"""
Documents router for the AI-Interactive Book backend
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class DocumentIndexRequest(BaseModel):
    content: str
    source: str

class DocumentIndexResponse(BaseModel):
    success: bool
    document_id: str

@router.post("/documents/index", response_model=DocumentIndexResponse)
async def index_document(request: DocumentIndexRequest):
    # Placeholder implementation - in a real implementation, this would index the document in the vector database
    return DocumentIndexResponse(
        success=True,
        document_id=f"doc_{hash(request.content[:10])}"
    )

@router.get("/documents/sources", response_model=List[str])
async def get_document_sources():
    # Placeholder implementation - in a real implementation, this would fetch from the vector database
    return ["docs/intro.md", "docs/module-1/chapter-1.md", "docs/module-1/chapter-2.md", "docs/module-1/chapter-3.md"]