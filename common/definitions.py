import os

# Password Complexity Definitions
PASSWORD_COMPLEXITY = {
    'min_length': 8,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special_chars': True,
    'max_length': 64,
}

# Authentication Attempt Limits
AUTH_ATTEMPT_LIMITS = {
    'max_login_attempts': 5,
    'lockout_duration_minutes': 15,
    'reset_attempt_duration_minutes': 30,
}

# Token and Session Configurations
TOKEN_CONFIGURATIONS = {
    'access_token_expire_minutes': 30,
    'refresh_token_expire_minutes': 60 * 24 * 7,  # 7 days
    'algorithm': 'HS256',
}

# Logging Configurations
LOGGING_CONFIGURATIONS = {
    'default_log_level': 'INFO',
    'log_format': 'standard',  # Options: 'standard', 'json'
    'log_date_format': '%Y-%m-%dT%H:%M:%S%z',
}

APP_DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://aime_admin:aime_password@localhost:5433/aime_app')

# Database Connection Configurations
DATABASE_CONFIGURATIONS = {
    'connection_timeout_seconds': 10,
    'max_pool_connections': 20,
    'pool_recycle_seconds': 3600,  # 1 hour
}

# Security Configurations
SECURITY_CONFIGURATIONS = {
    'allowed_password_reset_methods': ['email', 'sms'],
    'min_password_reset_interval_hours': 24,
    'require_2fa': False,
}

# Rate Limiting Configurations
RATE_LIMIT_CONFIGURATIONS = {
    'requests_per_minute': 100,
    'burst_limit': 50,
}

# UI Settings Definitions
UI_SETTINGS = {
    'theme': {
        'default': 'light',
        'options': ['light', 'dark']
    },
    'layout': {
        'default': 'grid',
        'options': ['grid', 'list']
    }
}

# AI Model Settings
AI_MODEL_SETTINGS = {
    'default_model': 'gpt-3.5-turbo',
    'available_models': [
        'gpt-3.5-turbo',
        'gpt-4',
        'claude-2',
        'gemini-pro'
    ]
}

# File Upload Settings
FILE_UPLOAD_SETTINGS = {
    'allowed_mime_types': {
        'image': ['image/jpeg', 'image/png', 'image/gif'],
        'video': ['video/mp4', 'video/mpeg'],
        'audio': ['audio/mpeg', 'audio/wav', 'audio/ogg'],
        'document': ['application/pdf', 'text/plain']
    },
    'max_file_size_mb': 50,
    'upload_path': '/static/uploads'
}

# Database Models Configuration
DB_MODEL_SETTINGS = {
    'string_field_lengths': {
        'title': 200,
        'name': 100,
        'icon': 50,
        'role': 10,
        'content_type': 20,
        'theme': 20,
        'layout': 20,
        'ai_model': 50
    }
}

PERMISSIONS = {
    'auth': 'Manage authentication and users',
    'db': 'Access and modify database',
    'models': 'Access and train models',
    'cmd': 'Execute system commands'
}

ROLES = {
    'admin': {
        'description': 'Administrator',
        'permissions': [PERMISSIONS.keys()]
    },
    'user': {
        'description': 'Standard user',
        'permissions': ['models']
    }
}