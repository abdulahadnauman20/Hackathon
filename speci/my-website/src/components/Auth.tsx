import React, { useState, useEffect } from 'react';
import './Auth.css';

interface User {
  user_id: string;
  email: string;
  background?: string;
  preferences?: Record<string, any>;
}

interface AuthProps {
  onAuthChange?: (user: User | null) => void;
}

const Auth: React.FC<AuthProps> = ({ onAuthChange }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [background, setBackground] = useState(''); // For signup
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  // Check for existing session on component mount
  useEffect(() => {
    const token = localStorage.getItem('session_token');
    if (token) {
      validateSession(token);
    }
  }, []);

  const validateSession = async (token: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.user) {
          setCurrentUser(data.user);
          onAuthChange?.(data.user);
        } else {
          // Token is invalid, remove it
          localStorage.removeItem('session_token');
        }
      } else {
        localStorage.removeItem('session_token');
      }
    } catch (err) {
      console.error('Error validating session:', err);
      localStorage.removeItem('session_token');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isLogin ? 'http://localhost:8000/api/v1/auth/login' : 'http://localhost:8000/api/v1/auth/register';
      const body = isLogin
        ? { email, password }
        : { email, password, background };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        if (!isLogin && data.user_id) {
          // For registration, we need to log in the user
          const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
          });

          const loginData = await loginResponse.json();

          if (loginResponse.ok && loginData.success && loginData.session_token) {
            localStorage.setItem('session_token', loginData.session_token);
            setCurrentUser({
              user_id: loginData.user_id,
              email,
              background
            });
            onAuthChange?.({
              user_id: loginData.user_id,
              email,
              background
            });
          } else {
            setError(loginData.message || 'Registration successful but login failed');
          }
        } else if (data.session_token) {
          localStorage.setItem('session_token', data.session_token);
          setCurrentUser({
            user_id: data.user_id,
            email,
            background: isLogin ? undefined : background
          });
          onAuthChange?.({
            user_id: data.user_id,
            email,
            background: isLogin ? undefined : background
          });
        }
      } else {
        setError(data.message || 'An error occurred');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    const token = localStorage.getItem('session_token');
    if (token) {
      try {
        await fetch('http://localhost:8000/api/v1/auth/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
      } catch (err) {
        console.error('Error during logout:', err);
      } finally {
        localStorage.removeItem('session_token');
        setCurrentUser(null);
        onAuthChange?.(null);
      }
    }
  };

  if (currentUser) {
    return (
      <div className="auth-container">
        <div className="auth-logged-in">
          <h3>Welcome, {currentUser.email}!</h3>
          {currentUser.background && (
            <p>Background: {currentUser.background}</p>
          )}
          <button onClick={handleLogout} className="auth-logout-button">
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h3>{isLogin ? 'Login' : 'Sign Up'}</h3>

        <form onSubmit={handleSubmit}>
          <div className="auth-input-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="auth-input-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          {!isLogin && (
            <div className="auth-input-group">
              <label htmlFor="background">Background (optional):</label>
              <textarea
                id="background"
                value={background}
                onChange={(e) => setBackground(e.target.value)}
                placeholder="Tell us about your background, interests, or goals (for personalization)"
              />
            </div>
          )}

          {error && <div className="auth-error">{error}</div>}

          <button type="submit" disabled={loading} className="auth-submit-button">
            {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
          </button>
        </form>

        <div className="auth-toggle">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
              }}
              className="auth-toggle-button"
            >
              {isLogin ? 'Sign Up' : 'Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Auth;