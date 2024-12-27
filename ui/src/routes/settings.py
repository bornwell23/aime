from flask import jsonify, request
from flask_login import login_required, current_user
import requests
from common.logging import logger
from services.api_config import APIConfig
from common.definitions import UI_SETTINGS, AI_MODEL_SETTINGS

def register_settings_routes(app):
    @app.route('/api/settings', methods=['GET'])
    @login_required
    def get_settings():
        """
        Retrieve user's settings from the server
        Follows guidelines:
        - UI should only communicate with the server
        - Use extensive logging
        """
        try:
            api_config = APIConfig()
            settings_url = api_config.get_api_url('/settings')
            headers = api_config.get_auth_headers()
            
            logger.debug(f'Fetching settings from server URL: {settings_url}')
            
            # Make request to server's settings endpoint
            response = requests.get(settings_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                settings_data = response.json()
                logger.info('Successfully retrieved user settings')
                return jsonify(settings_data)
            else:
                logger.error(f'Failed to retrieve settings. Server returned status {response.status_code}')
                return jsonify({
                    'error': 'Failed to retrieve settings',
                    'status_code': response.status_code
                }), response.status_code
        
        except requests.RequestException as e:
            logger.error(f'Error fetching settings from server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while fetching settings',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in get_settings: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500

    @app.route('/api/settings', methods=['POST'])
    @login_required
    def save_settings():
        """
        Save user's settings to the server
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(k in data for k in ['theme', 'layout']):
                return jsonify({'error': 'Missing required fields'}), 400
                
            # Validate theme
            if data['theme'] not in UI_SETTINGS['theme']['options']:
                return jsonify({'error': f'Invalid theme. Must be one of: {UI_SETTINGS["theme"]["options"]}'}), 400
                
            # Validate layout
            if data['layout'] not in UI_SETTINGS['layout']['options']:
                return jsonify({'error': f'Invalid layout. Must be one of: {UI_SETTINGS["layout"]["options"]}'}), 400
            
            api_config = APIConfig()
            settings_url = api_config.get_api_url('/settings')
            headers = api_config.get_auth_headers()
            
            logger.debug(f'Saving settings to server URL: {settings_url}')
            
            # Make request to server's settings endpoint
            response = requests.post(settings_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                logger.info('Successfully saved user settings')
                return jsonify(response.json())
            else:
                logger.error(f'Failed to save settings. Server returned status {response.status_code}')
                return jsonify(response.json()), response.status_code
                
        except requests.RequestException as e:
            logger.error(f'Error saving settings to server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while saving settings',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in save_settings: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500

    @app.route('/api/settings/ai-model', methods=['PUT'])
    @login_required
    def update_ai_model():
        """
        Update user's AI model settings
        Requires 'models' permission
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'model' not in data:
                return jsonify({'error': 'Missing required field: model'}), 400
                
            # Validate model
            if data['model'] not in AI_MODEL_SETTINGS['available_models']:
                return jsonify({'error': f'Invalid model. Must be one of: {AI_MODEL_SETTINGS["available_models"]}'}), 400
            
            api_config = APIConfig()
            model_url = api_config.get_api_url('/settings/ai-model')
            headers = api_config.get_auth_headers()
            
            logger.debug(f'Updating AI model settings at URL: {model_url}')
            
            # Make request to server's model settings endpoint
            response = requests.put(model_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                logger.info(f'Successfully updated AI model to: {data["model"]}')
                return jsonify(response.json())
            else:
                logger.error(f'Failed to update AI model. Server returned status {response.status_code}')
                return jsonify(response.json()), response.status_code
                
        except requests.RequestException as e:
            logger.error(f'Error updating AI model: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while updating AI model',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in update_ai_model: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500
