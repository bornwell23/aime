from flask import Blueprint, jsonify

from common.logging import logger
from api.utils import require_auth, has_permission

health_router = Blueprint('health', __name__)


@health_router.route('/check', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify server connectivity
    """
    logger.info('Health check endpoint called')
    return jsonify({
        'status': 'ok',
        'message': 'Server is running and healthy'
    }), 200
