from flask import Blueprint, request, jsonify
import requests
import os

from common.logging import logger
from api.utils import require_auth, has_permission, get_user_id
from api.v1.models import Card
from database import SessionLocal

cards_router = Blueprint('cards', __name__)


# Card endpoints


@cards_router.route('/cards', methods=['GET'])
@require_auth
def get_cards():
    """Get all cards for the current user."""
    try:
        db = SessionLocal()
        cards = db.query(Card)\
            .filter_by(user_id=get_user_id())\
            .all()

        logger.debug(f"Retrieved {len(cards)} cards for user {get_user_id()}")

        return jsonify([{
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        } for card in cards])

    except Exception as e:
        logger.error(f"Error getting cards: {str(e)}")
        return jsonify({'error': 'Failed to get cards'}), 500
    finally:
        db.close()


@cards_router.route('/cards', methods=['POST'])
@require_auth
def create_card():
    """Create a new card for the current user."""
    try:
        data = request.get_json()
        if not all(k in data for k in ['title', 'icon', 'content']):
            return jsonify({'error': 'Missing required fields'}), 400

        db = SessionLocal()
        card = Card(
            user_id=get_user_id(),
            title=data['title'],
            icon=data['icon'],
            content=data['content'],
            actions=data.get('actions')
        )
        db.add(card)
        db.commit()

        logger.debug(f"Created new card with ID {card.id} for user {get_user_id()}")

        return jsonify({
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        }), 201

    except Exception as e:
        logger.error(f"Error creating card: {str(e)}")
        return jsonify({'error': 'Failed to create card'}), 500
    finally:
        db.close()


@cards_router.route('/cards/<int:card_id>', methods=['DELETE'])
@require_auth
def delete_card(card_id):
    """Delete a card by its ID."""
    try:
        db = SessionLocal()
        card = db.query(Card)\
            .filter_by(id=card_id, user_id=get_user_id())\
            .first()

        if not card:
            return jsonify({'error': 'Card not found'}), 404

        db.delete(card)
        db.commit()

        logger.debug(f"Deleted card {card_id} for user {get_user_id()}")

        return '', 204

    except Exception as e:
        logger.error(f"Error deleting card {card_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete card'}), 500
    finally:
        db.close()


@cards_router.route('/cards/search', methods=['GET'])
@require_auth
def search_cards():
    """Search cards based on query."""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])

        db = SessionLocal()
        # Note: This is a simple search implementation
        # Could be enhanced with full-text search using PostgreSQL
        cards = db.query(Card).filter(
            Card.user_id == get_user_id(),
            (Card.title.ilike(f'%{query}%') | Card.content.ilike(f'%{query}%'))
        ).all()

        logger.debug(f"Found {len(cards)} cards matching query for user {get_user_id()}")

        return jsonify([{
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        } for card in cards])

    except Exception as e:
        logger.error(f"Error searching cards: {str(e)}")
        return jsonify({'error': 'Failed to search cards'}), 500
    finally:
        db.close()


@cards_router.route('/cards/generate', methods=['POST'])
@require_auth
def generate_card():
    """Generate a new card using AI."""
    try:
        data = request.get_json()
        if 'prompt' not in data:
            return jsonify({'error': 'Missing prompt parameter'}), 400

        # TODO: Implement AI card generation
        # This is a placeholder that creates a basic card
        db = SessionLocal()
        card = Card(
            user_id=get_user_id(),
            title="Generated Card",
            icon="🤖",
            content=f"Generated content for prompt: {data['prompt']}",
            actions=None
        )
        db.add(card)
        db.commit()

        logger.debug(f"Generated new card with ID {card.id} for user {get_user_id()}")

        return jsonify({
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        }), 201

    except Exception as e:
        logger.error(f"Error generating card: {str(e)}")
        return jsonify({'error': 'Failed to generate card'}), 500
    finally:
        db.close()
