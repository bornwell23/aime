from flask import Blueprint
from api.v1 import create_v1_router


def create_api_router():
    api_router = Blueprint('api', __name__)

    # Register v1 routes
    v1_router = create_v1_router()
    api_router.register_blueprint(v1_router, url_prefix='/v1')

    return api_router
