from flask import Blueprint
from .routes.auth import auth_router
from .routes.health import health_bp

def create_v1_router():
    v1_router = Blueprint('v1', __name__)
    
    # Register routes
    v1_router.register_blueprint(auth_router, url_prefix='/auth')
    v1_router.register_blueprint(health_bp, url_prefix='/system')
    
    return v1_router
