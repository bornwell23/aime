from flask import Blueprint, jsonify, request, g
import json
from sqlalchemy.orm import Session

from common.logging import logger
from common.definitions import FILE_UPLOAD_SETTINGS, APP_DATABASE_URL
from api.utils import require_auth, has_permission
from api.v1.models import ChatMessage

chat_router = Blueprint('chat', __name__)


def create_message_content(content_type, text_content=None, file_url=None):
    """Create standardized message content structure"""
    return {
        'type': content_type,
        'text': text_content,
        'file_url': file_url
    }


def determine_content_type(mime_type):
    """Determine content type based on mime type"""
    for content_type, allowed_types in FILE_UPLOAD_SETTINGS['allowed_mime_types'].items():
        if mime_type in allowed_types:
            return content_type
    return 'document'  # Default to document type


def validate_file_upload(file):
    """Validate file upload against settings"""
    if not file:
        return False, "No file provided"

    # Check mime type
    mime_type = file.content_type
    valid_mime_types = []
    for types in FILE_UPLOAD_SETTINGS['allowed_mime_types'].values():
        valid_mime_types.extend(types)

    if mime_type not in valid_mime_types:
        return False, f"Invalid file type. Allowed types: {', '.join(valid_mime_types)}"

    # Check file size
    if len(file.read()) > FILE_UPLOAD_SETTINGS['max_file_size_mb'] * 1024 * 1024:
        return False, f"File too large. Maximum size: {FILE_UPLOAD_SETTINGS['max_file_size_mb']}MB"

    file.seek(0)  # Reset file pointer after reading
    return True, None

# Chat endpoints


@chat_router.route('/chat/history', methods=['GET'])
@require_auth
def get_chat_history():
    try:
        session = Session()
        messages = session.query(ChatMessage).filter_by(user_id=g.user_id).order_by(ChatMessage.timestamp).all()

        return jsonify([{
            'id': msg.id,
            'role': msg.role,
            'content': json.loads(msg.content) if isinstance(msg.content, str) else msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages])

    except Exception as e:
        logger.error(f'Error getting chat history: {str(e)}')
        return jsonify({'error': 'Failed to get chat history'}), 500
    finally:
        session.close()


@chat_router.route('/chat/message', methods=['POST'])
@require_auth
def send_message():
    try:
        data = request.get_json()
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        session = Session()

        # Create user message with text content
        user_content = create_message_content('text', data['message'])
        user_message = ChatMessage(
            user_id=g.user_id,
            role='user',
            content=json.dumps(user_content)
        )
        session.add(user_message)

        # Generate bot response (placeholder - implement actual bot logic)
        bot_content = create_message_content('text', f"Echo: {data['message']}")
        bot_message = ChatMessage(
            user_id=g.user_id,
            role='aime',
            content=json.dumps(bot_content)
        )
        session.add(bot_message)

        session.commit()

        return jsonify({
            'id': bot_message.id,
            'role': bot_message.role,
            'content': json.loads(bot_message.content),
            'timestamp': bot_message.timestamp.isoformat()
        })

    except Exception as e:
        logger.error(f'Error sending message: {str(e)}')
        return jsonify({'error': 'Failed to send message'}), 500
    finally:
        session.close()


@chat_router.route('/chat/audio', methods=['POST'])
@require_auth
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        is_valid, error_message = validate_file_upload(audio_file)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        # Save audio file and get URL (implement proper file storage)
        file_url = f"{FILE_UPLOAD_SETTINGS['upload_path']}/audio/{audio_file.filename}"

        # Create message with audio content
        audio_content = create_message_content('audio', None, file_url)

        session = Session()
        message = ChatMessage(
            user_id=g.user_id,
            role='user',
            content=json.dumps(audio_content)
        )
        session.add(message)
        session.commit()

        return jsonify({
            'id': message.id,
            'role': message.role,
            'content': json.loads(message.content),
            'timestamp': message.timestamp.isoformat()
        })

    except Exception as e:
        logger.error(f'Error processing audio: {str(e)}')
        return jsonify({'error': 'Failed to process audio'}), 500
    finally:
        session.close()


@chat_router.route('/chat/file', methods=['POST'])
@require_auth
def upload_chat_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        is_valid, error_message = validate_file_upload(file)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        message_text = request.form.get('message', '')

        # Determine content type based on mime type
        content_type = determine_content_type(file.content_type)

        # Save file and get URL (implement proper file storage)
        file_url = f"{FILE_UPLOAD_SETTINGS['upload_path']}/{content_type}/{file.filename}"

        # Create message content
        message_content = create_message_content(
            content_type,
            message_text,
            file_url
        )

        session = Session()
        chat_message = ChatMessage(
            user_id=g.user_id,
            role='user',
            content=json.dumps(message_content)
        )
        session.add(chat_message)
        session.commit()

        return jsonify({
            'id': chat_message.id,
            'role': chat_message.role,
            'content': json.loads(chat_message.content),
            'timestamp': chat_message.timestamp.isoformat()
        })

    except Exception as e:
        logger.error(f'Error uploading file: {str(e)}')
        return jsonify({'error': 'Failed to upload file'}), 500
    finally:
        session.close()
