"""
Personalization service for the AI-Interactive Book backend.
Handles user preference management and content customization.
"""
from typing import Dict, Any, List, Optional
from .auth import auth_service

class PersonalizationService:
    """
    Manages user preferences and content personalization.
    """

    def __init__(self):
        pass

    def get_user_preferences(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user preferences based on their session.
        """
        user_info = auth_service.validate_session(session_token)
        if not user_info:
            return None

        return user_info.get("preferences", {})

    def update_user_preferences(self, session_token: str, preferences: Dict[str, Any]) -> bool:
        """
        Update user preferences.
        """
        return auth_service.update_user_preferences(session_token, preferences)

    def get_content_modifications(self, session_token: str, content: str) -> str:
        """
        Modify content based on user preferences and background.
        """
        user_info = auth_service.validate_session(session_token)
        if not user_info:
            return content

        preferences = user_info.get("preferences", {})
        background = user_info.get("background", "")

        # Apply personalization based on user background and preferences
        modified_content = content

        # Example personalization: adjust complexity based on user background
        if background and "beginner" in background.lower():
            modified_content = self._simplify_content(modified_content)
        elif background and "expert" in background.lower():
            modified_content = self._condense_content(modified_content)

        # Apply other preferences
        if preferences.get("reading_level") == "simplified":
            modified_content = self._simplify_content(modified_content)
        elif preferences.get("reading_level") == "advanced":
            modified_content = self._enhance_content(modified_content)

        return modified_content

    def _simplify_content(self, content: str) -> str:
        """Simplify content for easier understanding."""
        return content

    def _condense_content(self, content: str) -> str:
        """Condense content for more experienced users."""
        return content

    def _enhance_content(self, content: str) -> str:
        """Enhance content with more details for advanced users."""
        return content

    def get_reading_path(self, session_token: str, available_modules: List[str]) -> List[str]:
        """
        Suggest a personalized learning path based on user profile.
        """
        user_info = auth_service.validate_session(session_token)
        if not user_info:
            return available_modules

        background = user_info.get("background", "")
        preferences = user_info.get("preferences", {})

        # Adjust learning path based on background
        if background and "beginner" in background.lower():
            return self._prioritize_fundamentals(available_modules)
        elif background and "expert" in background.lower():
            return self._prioritize_advanced(available_modules)

        return available_modules

    def _prioritize_fundamentals(self, modules: List[str]) -> List[str]:
        """Prioritize fundamental modules."""
        fundamentals = [m for m in modules if "fundamental" in m.lower() or "intro" in m.lower() or "1" in m.split('/')[-1]]
        others = [m for m in modules if m not in fundamentals]
        return fundamentals + others

    def _prioritize_advanced(self, modules: List[str]) -> List[str]:
        """Prioritize advanced modules."""
        advanced = [m for m in modules if "advanced" in m.lower() or "expert" in m.lower()]
        others = [m for m in modules if m not in advanced]
        return advanced + others

# Global instance
personalization_service = PersonalizationService()