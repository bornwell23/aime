from flask import Blueprint, jsonify, request, g
from sqlalchemy.orm import Session
from common.logging import logger
from common.definitions import UI_SETTINGS, AI_MODEL_SETTINGS, APP_DATABASE_URL
from api.utils import require_auth, has_permission
from api.v1.models import UserSettings

settings_router = Blueprint('settings', __name__)

# Settings endpoints


@settings_router.route('/settings', methods=['GET'])
@require_auth
def get_settings():
    try:
        session = Session()
        try:
            settings = session.query(UserSettings).filter_by(user_id=g.user_id).first()
            if not settings:
                # Return default settings if not found
                return jsonify({
                    'theme': UI_SETTINGS['theme']['default'],
                    'layout': UI_SETTINGS['layout']['default'],
                    'ai_model': AI_MODEL_SETTINGS['default_model']
                })

            return jsonify({
                'theme': settings.theme,
                'layout': settings.layout,
                'ai_model': settings.ai_model
            })

        finally:
            session.close()

    except Exception as e:
        logger.error(f'Error getting settings: {str(e)}')
        return jsonify({'error': 'Failed to get settings'}), 500


@settings_router.route('/settings', methods=['POST'])
@require_auth
def save_settings():
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

        session = Session()
        try:
            settings = session.query(UserSettings).filter_by(user_id=g.user_id).first()
            if not settings:
                settings = UserSettings(user_id=g.user_id)
                session.add(settings)

            settings.theme = data['theme']
            settings.layout = data['layout']
            session.commit()

            return jsonify({'message': 'Settings saved successfully'})

        finally:
            session.close()

    except Exception as e:
        logger.error(f'Error saving settings: {str(e)}')
        return jsonify({'error': 'Failed to save settings'}), 500


@settings_router.route('/settings/ai-model', methods=['PUT'])
@require_auth
@has_permission('models')
def update_ai_model():
    """Update user's AI model settings. Protected by 'models' permission."""
    try:
        logger.debug("Received request to update AI model settings")
        data = request.get_json()

        if 'model' not in data:
            logger.error("Missing required field 'model' in request")
            return jsonify({'error': 'Missing required field: model'}), 400

        model = data['model']

        # Validate model
        if model not in AI_MODEL_SETTINGS['available_models']:
            logger.error(f"Invalid model requested: {model}")
            return jsonify({'error': f'Invalid model. Must be one of: {AI_MODEL_SETTINGS["available_models"]}'}), 400

        session = Session()
        try:
            # Get or create user settings
            settings = session.query(UserSettings).filter_by(user_id=g.user_id).first()
            if not settings:
                logger.debug(f"Creating new settings for user {g.user_id}")
                settings = UserSettings(user_id=g.user_id)
                session.add(settings)

            # Update model
            old_model = settings.ai_model
            settings.ai_model = model
            session.commit()

            logger.info(f"Updated AI model for user {g.user_id} from {old_model} to {model}")
            return jsonify({'message': 'AI model updated successfully', 'model': model})

        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error updating AI model settings: {str(e)}")
        return jsonify({'error': 'Failed to update AI model'}), 500
