"""
Translation router for the AI-Interactive Book backend
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List
from ..translation import translation_service

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "en"

class TranslateResponse(BaseModel):
    success: bool
    translated_text: str = ""
    message: str = ""

class SupportedLanguagesResponse(BaseModel):
    languages: Dict[str, str]

@router.get("/translation/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    languages = translation_service.get_supported_languages()
    return SupportedLanguagesResponse(languages=languages)

@router.post("/translation/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    translated = translation_service.translate_text(
        request.text,
        request.target_language,
        request.source_language
    )

    if translated is not None:
        return TranslateResponse(
            success=True,
            translated_text=translated
        )
    else:
        return TranslateResponse(
            success=False,
            message=f"Translation to {request.target_language} is not supported or invalid languages provided"
        )

@router.post("/translation/content")
async def translate_content(request: TranslateRequest):
    translated = translation_service.translate_content(
        request.text,  # In this context, 'text' field will contain the content to translate
        request.target_language,
        request.source_language
    )

    if translated is not None:
        return {"success": True, "translated_content": translated}
    else:
        return {
            "success": False,
            "message": f"Content translation to {request.target_language} is not supported"
        }

@router.get("/translation/direction/{language_code}")
async def get_language_direction(language_code: str):
    direction = translation_service.get_language_direction(language_code)
    return {"direction": direction}