from flask import jsonify, request
from flask_login import login_required
import requests
from common.logging import logger
from services.api_config import APIConfig

def register_history_routes(app):
    @app.route('/api/history')
    @login_required
    def api_history():
        """
        Retrieve user's history from the server
        Follows guidelines:
        - UI should only communicate with the server
        - Use extensive logging
        """
        try:
            api_config = APIConfig()
            history_url = api_config.get_api_url('/history')
            
            logger.debug(f'Fetching history from server URL: {history_url}')
            
            # Make request to server's history endpoint
            response = requests.get(history_url, timeout=10)
            
            if response.status_code == 200:
                history_data = response.json()
                logger.info(f'Successfully retrieved {len(history_data)} history items')
                return jsonify(history_data)
            else:
                logger.error(f'Failed to retrieve history. Server returned status {response.status_code}')
                return jsonify({
                    'error': 'Failed to retrieve history',
                    'status_code': response.status_code
                }), 500
        
        except requests.RequestException as e:
            logger.error(f'Error fetching history from server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while fetching history',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in api_history: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500
