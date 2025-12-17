"""
Translation service for the AI-Interactive Book backend.
Handles multilingual content translation and language management.
"""
from typing import Dict, List, Optional
from .config import settings

class TranslationService:
    """
    Manages content translation and language support.
    """

    def __init__(self):
        # Supported languages - in a real implementation, this might come from a config or database
        self.supported_languages = {
            "en": "English",
            "ur": "Urdu",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ar": "Arabic"
        }

        # Placeholder for translation model - in real implementation, use a translation API
        self.translation_model = None

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get a dictionary of supported languages with their codes and names.

        Returns:
            Dictionary mapping language codes to language names
        """
        return self.supported_languages

    def translate_text(self, text: str, target_language: str, source_language: str = "en") -> Optional[str]:
        """
        Translate text from source language to target language.

        Args:
            text: The text to translate
            target_language: The target language code (e.g., 'ur' for Urdu)
            source_language: The source language code (default is 'en' for English)

        Returns:
            Translated text or None if translation fails
        """
        # Validate target language
        if target_language not in self.supported_languages:
            return None

        # Validate source language
        if source_language not in self.supported_languages:
            return None

        # For demonstration purposes, return a placeholder translation
        # In a real implementation, this would call a translation API
        if target_language == "ur":
            # This is a placeholder - in real implementation, use a proper translation API
            return f"[TRANSLATION TO URDU: {text[:30]}...]"
        elif target_language == "es":
            return f"[TRADUCCIÓN A ESPAÑOL: {text[:30]}...]"
        elif target_language == "fr":
            return f"[TRADUCTION EN FRANÇAIS: {text[:30]}...]"
        else:
            # For other languages, return a generic placeholder
            return f"[TRANSLATION TO {self.supported_languages[target_language]}: {text[:30]}...]"

    def translate_content(self, content: str, target_language: str, source_language: str = "en") -> Optional[str]:
        """
        Translate content from source language to target language.

        Args:
            content: The content to translate
            target_language: The target language code
            source_language: The source language code

        Returns:
            Translated content or None if translation fails
        """
        # Validate languages
        if target_language not in self.supported_languages or source_language not in self.supported_languages:
            return None

        # For now, just use the translate_text method
        # In a more sophisticated implementation, we might need to handle
        # special formatting, code blocks, etc. differently
        return self.translate_text(content, target_language, source_language)

    def get_language_direction(self, language_code: str) -> str:
        """
        Get the text direction for a language (left-to-right or right-to-left).

        Args:
            language_code: The language code

        Returns:
            'rtl' for right-to-left languages, 'ltr' for left-to-right languages
        """
        rtl_languages = ["ur", "ar", "he", "fa"]  # Urdu, Arabic, Hebrew, Persian
        return "rtl" if language_code in rtl_languages else "ltr"

    def get_content_translation(self, content_path: str, target_language: str) -> Optional[str]:
        """
        Get a translation of specific content by path.

        Args:
            content_path: Path to the content (e.g., 'docs/intro.md')
            target_language: The target language code

        Returns:
            Translated content or None if not available
        """
        # In a real implementation, this would:
        # 1. Load the content from the specified path
        # 2. Translate it to the target language
        # 3. Return the translated content

        # For now, we'll return a placeholder
        return f"[TRANSLATED CONTENT: {content_path} in {self.supported_languages.get(target_language, target_language)}]"

# Global instance
translation_service = TranslationService()