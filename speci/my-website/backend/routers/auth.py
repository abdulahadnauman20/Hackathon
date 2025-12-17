"""
Authentication router for the AI-Interactive Book backend
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..auth import auth_service, AuthResponse, UserRegistration, UserLogin

router = APIRouter()

class ValidateSessionRequest(BaseModel):
    session_token: str

class ValidateSessionResponse(BaseModel):
    success: bool
    user: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

@router.post("/auth/register", response_model=AuthResponse)
async def register(request: UserRegistration):
    result = auth_service.register_user(request)
    if result.success:
        return result
    else:
        raise HTTPException(status_code=400, detail=result.message)

@router.post("/auth/login", response_model=AuthResponse)
async def login(request: UserLogin):
    result = auth_service.login_user(request)
    if result.success:
        return result
    else:
        raise HTTPException(status_code=401, detail=result.message)

@router.post("/auth/logout")
async def logout(request: Request):
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    session_token = auth_header[7:]  # Remove "Bearer " prefix
    success = auth_service.logout_user(session_token)

    if success:
        return {"success": True, "message": "Logged out successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid session token")

@router.post("/auth/validate", response_model=ValidateSessionResponse)
async def validate_session(request: ValidateSessionRequest):
    user_info = auth_service.validate_session(request.session_token)

    if user_info:
        return ValidateSessionResponse(
            success=True,
            user=user_info
        )
    else:
        return ValidateSessionResponse(
            success=False,
            message="Invalid or expired session token"
        )

@router.post("/auth/update-preferences")
async def update_preferences(request: Request):
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    session_token = auth_header[7:]  # Remove "Bearer " prefix

    # Parse preferences from request body
    body = await request.json()
    preferences = body.get("preferences", {})

    success = auth_service.update_user_preferences(session_token, preferences)

    if success:
        return {"success": True, "message": "Preferences updated successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid session token")