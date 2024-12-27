import json
import os
from flask_login import UserMixin
from common.logging import logger
from services.api_config import APIConfig
import requests

class User(UserMixin):
    def __init__(self, user_id=None, username=None, email=None, roles=None, permissions=None):
        """
        Initialize a User object with basic attributes
        
        Args:
            user_id (str): Unique identifier for the user
            username (str): User's username
            email (str): User's email address
            roles (list): User's roles
            permissions (list): User's permissions
        """
        self.id = user_id
        self.username = username
        self.email = email
        self.roles = roles or []
        self.permissions = permissions or []

    def get_id(self):
        """
        Return the user's ID for Flask-Login
        """
        return str(self.id)

    def has_role(self, role):
        """
        Check if user has a specific role
        """
        return role in self.roles

    def has_permission(self, permission):
        """
        Check if user has a specific permission
        """
        return permission in self.permissions

    def to_dict(self):
        """
        Convert user object to a dictionary for serialization
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': self.roles,
            'permissions': self.permissions
        }

class AccountManager:
    def __init__(self, session_dir=None):
        """
        Initialize AccountManager with session storage
        """
        self.session_dir = session_dir or os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'sessions'
        )
        self.api_config = APIConfig()
        
        # Ensure session directory exists
        os.makedirs(self.session_dir, exist_ok=True)
        
        logger.info(f"[AccountManager] Initialized with session directory: {self.session_dir}")

    def store_user(self, user):
        """Store user session information"""
        try:
            if not user.id:
                logger.warning("[AccountManager] Attempting to store user without ID")
                return False

            session_file = os.path.join(self.session_dir, f"{user.id}_session.json")
            with open(session_file, 'w') as f:
                json.dump(user.to_dict(), f)

            logger.info(f"[AccountManager] Stored session for user: {user.id}")
            return True
        except Exception as e:
            logger.error(f"[AccountManager] Error storing user session: {e}")
            return False

    def get_user(self, user_id):
        """Retrieve user from session storage"""
        try:
            if not user_id:
                logger.warning("[AccountManager] Attempted to get user with None/empty ID")
                return None

            session_file = os.path.join(self.session_dir, f"{user_id}_session.json")
            if not os.path.exists(session_file):
                logger.warning(f"[AccountManager] No session found for user ID: {user_id}")
                return None

            with open(session_file, 'r') as f:
                user_data = json.load(f)

            user = User(
                user_id=user_data.get('id'),
                username=user_data.get('username'),
                email=user_data.get('email'),
                roles=user_data.get('roles', []),
                permissions=user_data.get('permissions', [])
            )

            logger.info(f"[AccountManager] Retrieved session for user: {user_id}")
            return user
        except Exception as e:
            logger.error(f"[AccountManager] Error retrieving user session: {e}")
            return None

    def login(self, username, password):
        """Authenticate user with auth service"""
        try:
            auth_url = self.api_config.get_auth_url('/auth/login')
            response = requests.post(auth_url, json={
                'username': username,
                'password': password
            })

            if response.status_code == 200:
                data = response.json()
                user = User(
                    user_id=data.get('id'),
                    username=data.get('username'),
                    email=data.get('email'),
                    roles=data.get('roles', []),
                    permissions=data.get('permissions', [])
                )
                self.store_user(user)
                logger.info(f"[AccountManager] User logged in: {username}")
                return {'success': True, 'user': user}
            else:
                error_msg = response.json().get('detail', 'Login failed')
                logger.warning(f"[AccountManager] Login failed: {error_msg}")
                return {'success': False, 'error': error_msg}

        except Exception as e:
            logger.error(f"[AccountManager] Login error: {e}")
            return {'success': False, 'error': str(e)}

    def register(self, username, password, email):
        """Register new user with auth service"""
        try:
            auth_url = self.api_config.get_auth_url('/auth/register')
            response = requests.post(auth_url, json={
                'username': username,
                'password': password,
                'email': email
            })

            if response.status_code == 200:
                logger.info(f"[AccountManager] User registered: {username}")
                return True, "Registration successful"
            else:
                error_msg = response.json().get('detail', 'Registration failed')
                logger.warning(f"[AccountManager] Registration failed: {error_msg}")
                return False, error_msg

        except Exception as e:
            logger.error(f"[AccountManager] Registration error: {e}")
            return False, str(e)

    def logout(self, user_id):
        """Remove user session"""
        try:
            # TODO: invalidate token in auth service
            auth_url = self.api_config.get_auth_url('/auth/logout')
            response = requests.post(auth_url, json={
                'token': token
            })
            
            session_file = os.path.join(self.session_dir, f"{user_id}_session.json")
            if os.path.exists(session_file):
                os.remove(session_file)
                logger.info(f"[AccountManager] Logged out user: {user_id}")
                return True
            
            logger.warning(f"[AccountManager] No session found for user: {user_id}")
            return False
        except Exception as e:
            logger.error(f"[AccountManager] Logout error: {e}")
            return False