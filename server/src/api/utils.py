from flask import Blueprint, request, jsonify, g
from datetime import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os
from functools import wraps
import base64

from common.definitions import APP_DATABASE_URL


# Create database engine and session
engine = create_engine(APP_DATABASE_URL)
Session = sessionmaker(bind=engine)

# # Create tables if they don't exist
# Base.metadata.create_all(engine)


def get_user_id():
    """Get user ID from request context"""
    return g.user_id if hasattr(g, 'user_id') else None


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_user_id()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def has_permission(permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = get_user_id()
            # Check if user has the required permission (implement permission checking)
            # For now, assume all users have the 'models' permission
            if not user_id or not has_permission_impl(user_id, permission):
                return jsonify({'error': 'Forbidden'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


def has_permission_impl(user_id, permission):
    # Implement permission checking logic here
    # For now, assume all users have the 'models' permission
    return True


def create_message_content(content_type, content_data, file_url=None):
    """Create standardized message content structure"""
    return {
        'type': content_type,  # 'text', 'audio', 'video', 'image', 'file'
        'content': content_data,
        'file_url': file_url,
        'timestamp': datetime.utcnow().isoformat()
    }
