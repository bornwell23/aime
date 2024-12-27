from flask import jsonify, request
from flask_login import login_required, current_user
import requests
from werkzeug.utils import secure_filename
from common.logging import logger
from services.api_config import APIConfig
from common.definitions import FILE_UPLOAD_SETTINGS

def register_chat_routes(app):
    @app.route('/api/chat')
    @login_required
    def api_chat():
        """
        Retrieve user's chat from the server
        Follows guidelines:
        - UI should only communicate with the server
        - Use extensive logging
        """
        try:
            api_config = APIConfig()
            chat_url = api_config.get_api_url('/chat')
            
            logger.debug(f'Fetching chat from server URL: {chat_url}')
            
            # Make request to server's chat endpoint
            response = requests.get(chat_url, timeout=10)
            
            if response.status_code == 200:
                chat_data = response.json()
                logger.info(f'Successfully retrieved {len(chat_data)} chat items')
                return jsonify(chat_data)
            else:
                logger.error(f'Failed to retrieve chat. Server returned status {response.status_code}')
                return jsonify({
                    'error': 'Failed to retrieve chat',
                    'status_code': response.status_code
                }), 500
        
        except requests.RequestException as e:
            logger.error(f'Error fetching chat from server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while fetching chat',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in api_chat: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500

    @app.route('/api/chat/history')
    @login_required
    def get_chat_history():
        """
        Retrieve user's chat history from the server
        """
        try:
            api_config = APIConfig()
            chat_url = api_config.get_api_url('/chat/history')
            headers = api_config.get_auth_headers()
            
            logger.debug(f'Fetching chat history from server URL: {chat_url}')
            
            # Make request to server's chat endpoint
            response = requests.get(chat_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                chat_data = response.json()
                logger.info(f'Successfully retrieved {len(chat_data)} chat messages')
                return jsonify(chat_data)
            else:
                logger.error(f'Failed to retrieve chat history. Server returned status {response.status_code}')
                return jsonify({
                    'error': 'Failed to retrieve chat history',
                    'status_code': response.status_code
                }), response.status_code
        
        except requests.RequestException as e:
            logger.error(f'Error fetching chat history from server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while fetching chat history',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in get_chat_history: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500

    @app.route('/api/chat/message', methods=['POST'])
    @login_required
    def send_message():
        """
        Send a text message to the server
        """
        try:
            data = request.get_json()
            if 'message' not in data:
                return jsonify({'error': 'Missing required field: message'}), 400
                
            message = data['message'].strip()
            if not message:
                return jsonify({'error': 'Message cannot be empty'}), 400
            
            api_config = APIConfig()
            message_url = api_config.get_api_url('/chat/message')
            headers = api_config.get_auth_headers()
            
            logger.debug(f'Sending message to server URL: {message_url}')
            
            # Send message to server
            response = requests.post(
                message_url, 
                headers=headers,
                json={'message': message},
                timeout=10
            )
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info('Successfully sent message and received response')
                return jsonify(response_data)
            else:
                logger.error(f'Failed to send message. Server returned status {response.status_code}')
                return jsonify(response.json()), response.status_code
                
        except requests.RequestException as e:
            logger.error(f'Error sending message to server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while sending message',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in send_message: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500

    @app.route('/api/chat/file', methods=['POST'])
    @login_required
    def send_file():
        """
        Send a file with optional message to the server
        """
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
                
            file = request.files['file']
            if not file or not file.filename:
                return jsonify({'error': 'Invalid file'}), 400
                
            # Validate file type
            if not any(file.content_type.startswith(t) for t in FILE_UPLOAD_SETTINGS['allowed_mime_types']):
                return jsonify({
                    'error': f'Invalid file type. Allowed types: {FILE_UPLOAD_SETTINGS["allowed_mime_types"]}'
                }), 400
                
            # Validate file size
            if file.content_length > FILE_UPLOAD_SETTINGS['max_file_size']:
                return jsonify({
                    'error': f'File too large. Maximum size: {FILE_UPLOAD_SETTINGS["max_file_size"]} bytes'
                }), 400
            
            api_config = APIConfig()
            file_url = api_config.get_api_url('/chat/file')
            headers = api_config.get_auth_headers()
            
            # Remove Content-Type from headers as it will be set by requests for multipart/form-data
            headers.pop('Content-Type', None)
            
            logger.debug(f'Sending file to server URL: {file_url}')
            
            # Prepare the files and data
            files = {'file': (secure_filename(file.filename), file, file.content_type)}
            data = {'message': request.form.get('message', '')}
            
            # Send file to server
            response = requests.post(
                file_url,
                headers=headers,
                files=files,
                data=data,
                timeout=30  # Longer timeout for file uploads
            )
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info('Successfully sent file and received response')
                return jsonify(response_data)
            else:
                logger.error(f'Failed to send file. Server returned status {response.status_code}')
                return jsonify(response.json()), response.status_code
                
        except requests.RequestException as e:
            logger.error(f'Error sending file to server: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Network error while sending file',
                'details': str(e)
            }), 500
        except Exception as e:
            logger.error(f'Unexpected error in send_file: {str(e)}', exc_info=True)
            return jsonify({
                'error': 'Unexpected error occurred',
                'details': str(e)
            }), 500
