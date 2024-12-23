from flask import Blueprint, jsonify
from logger import logger

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify server connectivity
    """
    logger.info('Health check endpoint called')
    return jsonify({
        'status': 'ok',
        'message': 'Server is running and healthy'
    }), 200
