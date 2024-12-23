import os
import json
import requests
from .api_config import APIConfig
from logger import logger
from flask_login import UserMixin
import shutil
import tempfile
import pathlib
import pickle

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.token = user_data.get('token')

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.token is not None

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

class AuthService:
    def __init__(self):
        self.api = APIConfig()
        self.current_user = None
        self._storage_key = 'auth_state'

    def _parse_validation_errors(self, error_details):
        """
        Parse Pydantic validation errors into a human-readable string.
        
        Args:
            error_details (list): List of error dictionaries from Pydantic
        
        Returns:
            str: A user-friendly error message
        """
        error_messages = []
        for error in error_details:
            loc = error.get('loc', [])
            msg = error.get('msg', 'Validation error')
            
            # Map location to more readable field names
            field_map = {
                'username': 'Username',
                'password': 'Password'
            }
            
            # Get the last part of the location (field name)
            field = loc[-1] if loc and len(loc) > 0 else 'Field'
            readable_field = field_map.get(field, field.capitalize())
            
            error_messages.append(f"{readable_field}: {msg}")
        
        return '. '.join(error_messages)

    def login_user(self, user):
        """
        Log in a user by setting the current user and persisting state
        
        Args:
            user (User): The user to log in
        """
        # Set the current user
        self.current_user = user
        
        # Optional: Store user state in local storage
        try:
            user_state = {
                'id': user.id,
                'username': user.username,
                'token': user.token,
                'email': user.email
            }
            # Persist login state
            with open(os.path.join(os.path.expanduser('~'), '.aime_auth_state'), 'w') as f:
                json.dump(user_state, f)
        except Exception as e:
            logger.error(f"Failed to persist user state: {e}")

    def login(self, username, password):
        try:
            # Validate input
            if not username or not password:
                logger.error("Login failed: Username or password is empty")
                return {
                    'success': False, 
                    'error': "Username and password are required"
                }

            # Prepare login request
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(
                self.api.get_api_url("auth/token"), 
                json={
                    "username": username, 
                    "password": password
                },
                headers=headers
            )
            
            # Check response
            if response.status_code == 200:
                user_data = response.json()
                user = User({
                    'id': user_data.get('id'),
                    'username': username,
                    'token': user_data.get('access_token')
                })
                self.login_user(user)
                logger.info(f"User {username} logged in successfully")
                
                # Return a tuple with success status and navigation target
                return {
                    'success': True, 
                    'redirect': '/home',  # Specify the home page route
                    'user': user
                }
            
            # Handle different error scenarios
            try:
                # First, try to parse as JSON validation error
                error_details = response.json()
                
                # Check if it's a Pydantic validation error
                if isinstance(error_details, list) and all('loc' in err and 'msg' in err for err in error_details):
                    error_message = self._parse_validation_errors(error_details)
                else:
                    # Fallback to default error parsing
                    error_message = error_details.get('detail', 'Login failed')
            except ValueError:
                # If JSON parsing fails, use raw response text
                error_message = response.text or 'Login failed'
            
            logger.error(f"Login failed for user {username}. Status: {response.status_code}, Error: {error_message}")
            return {
                'success': False, 
                'error': error_message
            }
            
        except requests.RequestException as e:
            logger.error(f"Network error during login: {str(e)}")
            return {
                'success': False, 
                'error': "Network error occurred"
            }
        except Exception as e:
            logger.error(f"Unexpected login error: {str(e)}")
            return {
                'success': False, 
                'error': "An unexpected error occurred."
            }

    def register(self, username, password, email):
        try:
            response = requests.post(
                self.api.get_api_url("/auth/register"),
                json={
                    "username": username,
                    "password": password,
                    "email": email
                }
            )
            
            # Parse the response JSON
            response_data = response.json()
            
            # Check for successful registration (status code 200 or 201)
            if response.status_code in [200, 201]:
                logger.info(f"User {username} registered successfully")
                return True, None
            
            # Handle specific error messages
            error_message = response_data.get('detail', 'Registration failed')
            logger.error(f"Registration failed for user {username}. Err: {error_message}")
            return False, error_message
            
        except requests.RequestException as e:
            logger.error(f"Network error during registration: {str(e)}")
            return False, "Network error occurred"
        except Exception as e:
            logger.error(f"Unexpected registration error: {str(e)}")
            return False, "An unexpected error occurred."

    def get_user_by_id(self, user_id):
        # Implement user retrieval from storage/session
        # This is a simplified version
        if self.current_user and self.current_user.id == user_id:
            return self.current_user
        return None

    def get_user(self, user_id):
        """
        Retrieve a user by their ID from persistent storage
        
        Args:
            user_id (int or str): The ID of the user to retrieve
        
        Returns:
            User: A user object if found, None otherwise
        """
        try:
            # Convert user_id to string to ensure consistency
            user_id = str(user_id)
            
            # Define the path for storing user state
            user_state_path = os.path.join(os.path.expanduser('~'), '.aime_auth_state')
            
            # Check if user state file exists
            if not os.path.exists(user_state_path):
                logger.warning(f"No user state file found at {user_state_path}")
                return None
            
            # Read user state from file
            with open(user_state_path, 'r') as f:
                user_state = json.load(f)
            
            # Verify the user ID matches
            if str(user_state.get('id')) != user_id:
                logger.warning(f"User ID mismatch. Requested: {user_id}, Stored: {user_state.get('id')}")
                return None
            
            # Create and return User object
            logger.info(f"Successfully loaded user with ID: {user_id}")
            return User(user_state)
        
        except FileNotFoundError:
            logger.error(f"User state file not found for user ID: {user_id}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in user state file for user ID: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None
