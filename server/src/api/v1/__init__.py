from flask import Blueprint
from api.v1.routes.auth import auth_router
from api.v1.routes.health import health_router
from api.v1.routes.history import history_router
from api.v1.routes.chat import chat_router
from api.v1.routes.settings import settings_router


def create_v1_router():
    v1_router = Blueprint('v1', __name__)

    # Register routes
    v1_router.register_blueprint(auth_router, url_prefix='/auth')
    v1_router.register_blueprint(health_router, url_prefix='/health')
    v1_router.register_blueprint(history_router, url_prefix='/history')
    v1_router.register_blueprint(chat_router, url_prefix='/chat')
    v1_router.register_blueprint(settings_router, url_prefix='/settings')

    return v1_router
