import React, { useState, useEffect } from 'react';
import './Personalization.css';

interface PersonalizationProps {
  sessionToken: string | null;
}

interface Preferences {
  reading_level?: string;
  learning_goal?: string;
  preferred_examples?: string[];
  interface_language?: string;
}

const Personalization: React.FC<PersonalizationProps> = ({ sessionToken }) => {
  const [preferences, setPreferences] = useState<Preferences>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  // Load user preferences when component mounts or session token changes
  useEffect(() => {
    if (sessionToken) {
      loadPreferences();
    } else {
      setPreferences({});
      setLoading(false);
    }
  }, [sessionToken]);

  const loadPreferences = async () => {
    if (!sessionToken) return;

    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setPreferences(data.preferences || {});
      }
    } catch (error) {
      console.error('Error loading preferences:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePreferenceChange = (key: keyof Preferences, value: any) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSavePreferences = async () => {
    if (!sessionToken) return;

    try {
      setSaving(true);
      setSaved(false);

      const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionToken}`
        },
        body: JSON.stringify({ preferences })
      });

      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
    } finally {
      setSaving(false);
    }
  };

  if (!sessionToken) {
    return (
      <div className="personalization-container">
        <div className="personalization-message">
          <p>Please log in to customize your learning experience.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="personalization-container">
        <div className="personalization-loading">
          Loading preferences...
        </div>
      </div>
    );
  }

  return (
    <div className="personalization-container">
      <h3>Personalize Your Learning Experience</h3>

      <div className="personalization-form">
        <div className="preference-group">
          <label htmlFor="reading-level">Reading Level:</label>
          <select
            id="reading-level"
            value={preferences.reading_level || ''}
            onChange={(e) => handlePreferenceChange('reading_level', e.target.value)}
            className="preference-select"
          >
            <option value="">Default</option>
            <option value="simplified">Simplified (Beginner-friendly)</option>
            <option value="standard">Standard</option>
            <option value="advanced">Advanced (Expert-level)</option>
          </select>
        </div>

        <div className="preference-group">
          <label htmlFor="learning-goal">Learning Goal:</label>
          <select
            id="learning-goal"
            value={preferences.learning_goal || ''}
            onChange={(e) => handlePreferenceChange('learning_goal', e.target.value)}
            className="preference-select"
          >
            <option value="">Default</option>
            <option value="quick_start">Quick Start</option>
            <option value="deep_understanding">Deep Understanding</option>
            <option value="practical_application">Practical Application</option>
          </select>
        </div>

        <div className="preference-group">
          <label htmlFor="interface-language">Interface Language:</label>
          <select
            id="interface-language"
            value={preferences.interface_language || 'en'}
            onChange={(e) => handlePreferenceChange('interface_language', e.target.value)}
            className="preference-select"
          >
            <option value="en">English</option>
            <option value="ur">Urdu</option>
          </select>
        </div>

        <div className="preference-group">
          <label>Preferred Examples:</label>
          <div className="checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={preferences.preferred_examples?.includes('technical') || false}
                onChange={(e) => {
                  const current = preferences.preferred_examples || [];
                  if (e.target.checked) {
                    handlePreferenceChange('preferred_examples', [...current, 'technical']);
                  } else {
                    handlePreferenceChange('preferred_examples', current.filter(item => item !== 'technical'));
                  }
                }}
              />
              Technical
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={preferences.preferred_examples?.includes('business') || false}
                onChange={(e) => {
                  const current = preferences.preferred_examples || [];
                  if (e.target.checked) {
                    handlePreferenceChange('preferred_examples', [...current, 'business']);
                  } else {
                    handlePreferenceChange('preferred_examples', current.filter(item => item !== 'business'));
                  }
                }}
              />
              Business
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={preferences.preferred_examples?.includes('educational') || false}
                onChange={(e) => {
                  const current = preferences.preferred_examples || [];
                  if (e.target.checked) {
                    handlePreferenceChange('preferred_examples', [...current, 'educational']);
                  } else {
                    handlePreferenceChange('preferred_examples', current.filter(item => item !== 'educational'));
                  }
                }}
              />
              Educational
            </label>
          </div>
        </div>

        <button
          onClick={handleSavePreferences}
          disabled={saving}
          className="save-preferences-button"
        >
          {saving ? 'Saving...' : 'Save Preferences'}
        </button>

        {saved && (
          <div className="save-success">
            Preferences saved successfully!
          </div>
        )}
      </div>
    </div>
  );
};

export default Personalization;