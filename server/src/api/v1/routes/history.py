from flask import Blueprint, jsonify, request
from api.v1.models import HistoryItem
from database import SessionLocal
from api.utils import require_auth, get_user_id
from common.logging import logger

history_router = Blueprint('history', __name__)


@history_router.route('/', methods=['GET'])
@require_auth
def get_history():
    """Get history items for the current user."""
    try:
        db = SessionLocal()
        items = db.query(HistoryItem)\
            .filter_by(user_id=get_user_id())\
            .order_by(HistoryItem.timestamp.desc())\
            .all()

        logger.debug(f"Retrieved {len(items)} history items for user {get_user_id()}")

        return jsonify([{
            'id': item.id,
            'title': item.title,
            'content_type': item.content_type,
            'content': item.content,
            'timestamp': item.timestamp.isoformat()
        } for item in items])

    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({'error': 'Failed to get history'}), 500
    finally:
        db.close()
