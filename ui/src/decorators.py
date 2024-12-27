from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
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
            if not current_user.is_authenticated:
                logger.warning('Unauthenticated user attempting to access protected route')
                return redirect(url_for('login'))
            
            if not current_user.has_permission(permission):
                logger.warning(f'Permission denied: {permission} required. User has: {current_user.permissions}')
                flash(f'You need {permission} permission to access this page.', 'error')
                return redirect(url_for('home'))
                
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
            if not current_user.is_authenticated:
                logger.warning('Unauthenticated user attempting to access protected route')
                return redirect(url_for('login'))
            
            if not current_user.has_role(role):
                logger.warning(f'Role denied: {role} required. User has: {current_user.roles}')
                flash(f'You need {role} role to access this page.', 'error')
                return redirect(url_for('home'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
