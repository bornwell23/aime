from flask import Blueprint, request, jsonify
import requests
import os
from logger import logger

auth_router = Blueprint('auth', __name__)

@auth_router.route('/token', methods=['POST'])
def get_token():
    try:
        logger.info('Proxying authentication request to auth service')
        auth_service_url = f"http://{os.getenv('AUTH_SERVICE_HOST', 'auth-service')}:{os.getenv('AUTH_SERVICE_PORT', '8000')}/token"
        
        response = requests.post(
            auth_service_url,
            json=request.get_json(),
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify(response.json()), response.status_code
        
    except requests.RequestException as error:
        logger.error(f'Error connecting to auth service: {str(error)}')
        return jsonify({'error': 'Authentication service unavailable'}), 503
    except Exception as error:
        logger.error(f'Error in token endpoint: {str(error)}')
        return jsonify({'error': str(error)}), 500

@auth_router.route('/register', methods=['POST'])
def register():
    try:
        logger.info('Proxying registration request to auth service')
        auth_service_url = f"http://{os.getenv('AUTH_SERVICE_HOST', 'auth-service')}:{os.getenv('AUTH_SERVICE_PORT', '8000')}/register"
        
        response = requests.post(
            auth_service_url,
            json=request.get_json(),
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify(response.json()), response.status_code
        
    except requests.RequestException as error:
        logger.error(f'Error connecting to auth service: {str(error)}')
        return jsonify({'error': 'Authentication service unavailable'}), 503
    except Exception as error:
        logger.error(f'Error in register endpoint: {str(error)}')
        return jsonify({'error': str(error)}), 500

@auth_router.route('/verify', methods=['POST'])
def verify_token():
    try:
        logger.info('Verifying authentication token')
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warn('Missing or invalid Authorization header')
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
            
        token = auth_header.split(' ')[1]
        auth_service_url = f"http://{os.getenv('AUTH_SERVICE_HOST', 'auth-service')}:{os.getenv('AUTH_SERVICE_PORT', '8000')}/verify"
        
        response = requests.post(
            auth_service_url,
            json={'token': token},
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify(response.json()), response.status_code
        
    except requests.RequestException as error:
        logger.error(f'Error connecting to auth service: {str(error)}')
        return jsonify({'error': 'Authentication service unavailable'}), 503
    except Exception as error:
        logger.error(f'Error in verify endpoint: {str(error)}')
        return jsonify({'error': str(error)}), 500
