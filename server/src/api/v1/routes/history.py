from flask import Blueprint, jsonify, request
from api.v1.models import HistoryItem
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.utils import require_auth, has_permission
from common.logging import logger

history_router = Blueprint('history', __name__)


@history_router.route('/', methods=['GET'])
@require_auth
def get_history():
    try:
        session = Session()
        items = session.query(HistoryItem).filter_by(user_id=get_user_id()).order_by(HistoryItem.timestamp.desc()).all()

        return jsonify([{
            'id': item.id,
            'title': item.title,
            'content_type': item.content_type,
            'content': item.content,
            'timestamp': item.timestamp.isoformat()
        } for item in items])

    except Exception as e:
        logger.error(f'Error getting history: {str(e)}')
        return jsonify({'error': 'Failed to get history'}), 500
    finally:
        session.close()
