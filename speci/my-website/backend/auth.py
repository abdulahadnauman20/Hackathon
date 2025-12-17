"""
Authentication service for the AI-Interactive Book backend.
Handles user registration, login, and session management.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import hashlib
from pydantic import BaseModel
from .config import settings

# In-memory storage for demonstration purposes
# In production, use a proper database
users_db: Dict[str, Dict[str, Any]] = {}
sessions_db: Dict[str, Dict[str, Any]] = {}

class UserRegistration(BaseModel):
    email: str
    password: str
    background: Optional[str] = None  # User's background for personalization
    preferences: Optional[Dict[str, Any]] = {}

class UserLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    session_token: Optional[str] = None

class AuthService:
    """
    Handles user authentication and session management.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 with a salt."""
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{hashed}:{salt}"

    @staticmethod
    def verify_password(password: str, hashed_with_salt: str) -> bool:
        """Verify a password against its hash."""
        try:
            hashed, salt = hashed_with_salt.split(':')
            return hashed == hashlib.sha256((password + salt).encode()).hexdigest()
        except:
            return False

    def register_user(self, registration_data: UserRegistration) -> AuthResponse:
        """Register a new user."""
        email = registration_data.email.lower().strip()

        # Check if user already exists
        if email in users_db:
            return AuthResponse(
                success=False,
                message="User with this email already exists"
            )

        # Hash the password
        hashed_password = self.hash_password(registration_data.password)

        # Create user
        user_id = secrets.token_urlsafe(16)
        users_db[email] = {
            "user_id": user_id,
            "email": email,
            "password_hash": hashed_password,
            "background": registration_data.background,
            "preferences": registration_data.preferences,
            "created_at": datetime.utcnow(),
            "last_login": None
        }

        return AuthResponse(
            success=True,
            message="User registered successfully",
            user_id=user_id
        )

    def login_user(self, login_data: UserLogin) -> AuthResponse:
        """Authenticate a user and create a session."""
        email = login_data.email.lower().strip()

        # Check if user exists
        if email not in users_db:
            return AuthResponse(
                success=False,
                message="Invalid email or password"
            )

        user = users_db[email]

        # Verify password
        if not self.verify_password(login_data.password, user["password_hash"]):
            return AuthResponse(
                success=False,
                message="Invalid email or password"
            )

        # Update last login
        user["last_login"] = datetime.utcnow()

        # Create session
        session_token = secrets.token_urlsafe(32)
        sessions_db[session_token] = {
            "user_id": user["user_id"],
            "email": email,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=7)  # 7-day session
        }

        return AuthResponse(
            success=True,
            message="Login successful",
            user_id=user["user_id"],
            session_token=session_token
        )

    def logout_user(self, session_token: str) -> bool:
        """End a user session."""
        if session_token in sessions_db:
            del sessions_db[session_token]
            return True
        return False

    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Validate a session token and return user info if valid."""
        if session_token not in sessions_db:
            return None

        session = sessions_db[session_token]

        # Check if session has expired
        if session["expires_at"] < datetime.utcnow():
            del sessions_db[session_token]
            return None

        # Find user by ID
        user = None
        for u in users_db.values():
            if u["user_id"] == session["user_id"]:
                user = u
                break

        if not user:
            # Session exists but user doesn't, remove session
            del sessions_db[session_token]
            return None

        return {
            "user_id": user["user_id"],
            "email": user["email"],
            "background": user["background"],
            "preferences": user["preferences"]
        }

    def update_user_preferences(self, session_token: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences."""
        session_info = self.validate_session(session_token)
        if not session_info:
            return False

        # Find user and update preferences
        for email, user in users_db.items():
            if user["user_id"] == session_info["user_id"]:
                user["preferences"] = {**user["preferences"], **preferences}
                return True

        return False

    def get_user_background(self, session_token: str) -> Optional[str]:
        """Get user's background information."""
        session_info = self.validate_session(session_token)
        if not session_info:
            return None

        # Find user and return background
        for email, user in users_db.items():
            if user["user_id"] == session_info["user_id"]:
                return user["background"]

        return None

# Global instance
auth_service = AuthService()