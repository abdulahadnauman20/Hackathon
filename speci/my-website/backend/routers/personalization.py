"""
Personalization router for the AI-Interactive Book backend
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..personalization import personalization_service

router = APIRouter()

class PreferencesRequest(BaseModel):
    preferences: Dict[str, Any]

class PreferencesResponse(BaseModel):
    success: bool
    preferences: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

@router.get("/personalization/preferences", response_model=PreferencesResponse)
async def get_preferences(authorization: str = None):
    # Extract token from Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        return PreferencesResponse(
            success=False,
            message="Authorization header missing or invalid"
        )

    session_token = authorization[7:]  # Remove "Bearer " prefix
    preferences = personalization_service.get_user_preferences(session_token)

    if preferences is not None:
        return PreferencesResponse(
            success=True,
            preferences=preferences
        )
    else:
        return PreferencesResponse(
            success=False,
            message="Invalid or expired session token"
        )

@router.post("/personalization/preferences", response_model=PreferencesResponse)
async def update_preferences(request: PreferencesRequest, authorization: str = None):
    # Extract token from Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        return PreferencesResponse(
            success=False,
            message="Authorization header missing or invalid"
        )

    session_token = authorization[7:]  # Remove "Bearer " prefix
    success = personalization_service.update_user_preferences(session_token, request.preferences)

    if success:
        return PreferencesResponse(
            success=True,
            message="Preferences updated successfully"
        )
    else:
        return PreferencesResponse(
            success=False,
            message="Invalid or expired session token"
        )

@router.post("/personalization/content-modifications")
async def get_content_modifications(content: str, authorization: str = None):
    # Extract token from Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        return {"error": "Authorization header missing or invalid"}

    session_token = authorization[7:]  # Remove "Bearer " prefix
    modified_content = personalization_service.get_content_modifications(session_token, content)

    return {"modified_content": modified_content}

@router.post("/personalization/reading-path")
async def get_reading_path(modules: list, authorization: str = None):
    # Extract token from Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        return {"error": "Authorization header missing or invalid", "modules": modules}

    session_token = authorization[7:]  # Remove "Bearer " prefix
    personalized_path = personalization_service.get_reading_path(session_token, modules)

    return {"modules": personalized_path}