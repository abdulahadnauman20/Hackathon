import React, { useState, useEffect } from 'react';
import './Translation.css';

interface TranslationProps {
  content: string;
  onLanguageChange?: (language: string) => void;
}

const Translation: React.FC<TranslationProps> = ({ content, onLanguageChange }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [translatedContent, setTranslatedContent] = useState(content);
  const [isTranslating, setIsTranslating] = useState(false);
  const [availableLanguages] = useState([
    { code: 'en', name: 'English' },
    { code: 'ur', name: 'Urdu' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' }
  ]);

  useEffect(() => {
    if (currentLanguage === 'en') {
      setTranslatedContent(content);
    } else {
      handleTranslate();
    }
  }, [currentLanguage]);

  const handleTranslate = async () => {
    if (currentLanguage === 'en') {
      setTranslatedContent(content);
      onLanguageChange?.('en');
      return;
    }

    setIsTranslating(true);
    try {
      // In a real implementation, this would call the backend translation API
      // For demonstration, we'll simulate the translation with a delay
      await new Promise(resolve => setTimeout(resolve, 500));

      // Simulate translation by adding a prefix
      setTranslatedContent(`[${currentLanguage.toUpperCase()} TRANSLATION]: ${content}`);
      onLanguageChange?.(currentLanguage);
    } catch (error) {
      console.error('Translation error:', error);
      setTranslatedContent(content);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newLanguage = e.target.value;
    setCurrentLanguage(newLanguage);
  };

  const getLanguageDirection = (langCode: string): string => {
    // Right-to-left languages
    const rtlLanguages = ['ur', 'ar', 'he', 'fa'];
    return rtlLanguages.includes(langCode) ? 'rtl' : 'ltr';
  };

  return (
    <div className="translation-container">
      <div className="translation-controls">
        <label htmlFor="language-select">Translate to:</label>
        <select
          id="language-select"
          value={currentLanguage}
          onChange={handleLanguageChange}
          className="language-select"
          disabled={isTranslating}
        >
          {availableLanguages.map(lang => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>

        {isTranslating && (
          <div className="translating-indicator">
            Translating...
          </div>
        )}
      </div>

      <div
        className="translated-content"
        dir={getLanguageDirection(currentLanguage)}
      >
        {translatedContent}
      </div>

      {currentLanguage !== 'en' && (
        <div className="translation-note">
          <small>
            Note: This is a translated version.
            <button
              className="switch-to-english"
              onClick={() => setCurrentLanguage('en')}
            >
              View in English
            </button>
          </small>
        </div>
      )}
    </div>
  );
};

export default Translation;