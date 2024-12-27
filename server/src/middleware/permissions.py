from functools import wraps
from flask import request, g, jsonify
from common.logging import logger


def require_permission(permission):
    """
    Decorator to check if user has required permission

    Args:
        permission (str): Required permission name
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get permissions from request context
            user_permissions = g.get('user_permissions', [])

            if permission not in user_permissions:
                logger.warning(f'Permission denied: {permission} required. User has: {user_permissions}')
                return jsonify({
                    'error': 'Permission denied',
                    'required_permission': permission
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_role(role):
    """
    Decorator to check if user has required role

    Args:
        role (str): Required role name
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get roles from request context
            user_roles = g.get('user_roles', [])

            if role not in user_roles:
                logger.warning(f'Role denied: {role} required. User has: {user_roles}')
                return jsonify({
                    'error': 'Role denied',
                    'required_role': role
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def extract_permissions_middleware():
    """
    Middleware to extract permissions and roles from request headers
    """
    try:
        # Get permissions and roles from auth headers
        permissions = request.headers.get('X-User-Permissions', '')
        roles = request.headers.get('X-User-Roles', '')

        # Store in flask.g for access in route handlers
        g.user_permissions = permissions.split(',') if permissions else []
        g.user_roles = roles.split(',') if roles else []

        logger.debug(f'User permissions: {g.user_permissions}')
        logger.debug(f'User roles: {g.user_roles}')

    except Exception as e:
        logger.error(f'Error extracting permissions: {str(e)}')
        g.user_permissions = []
        g.user_roles = []
