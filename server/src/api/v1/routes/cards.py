from flask import Blueprint, request, jsonify
import requests
import os

from common.logging import logger
from api.utils import require_auth, has_permission

cards_router = Blueprint('cards', __name__)

# Card endpoints


@cards_router.route('/cards', methods=['GET'])
@require_auth
def get_cards():
    try:
        session = Session()
        cards = session.query(Card).filter_by(user_id=get_user_id()).all()

        return jsonify([{
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        } for card in cards])

    except Exception as e:
        logger.error(f'Error getting cards: {str(e)}')
        return jsonify({'error': 'Failed to get cards'}), 500
    finally:
        session.close()


@cards_router.route('/cards', methods=['POST'])
@require_auth
def create_card():
    try:
        data = request.get_json()
        if not all(k in data for k in ['title', 'icon', 'content']):
            return jsonify({'error': 'Missing required fields'}), 400

        session = Session()
        card = Card(
            user_id=get_user_id(),
            title=data['title'],
            icon=data['icon'],
            content=data['content'],
            actions=data.get('actions')
        )
        session.add(card)
        session.commit()

        return jsonify({
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        }), 201

    except Exception as e:
        logger.error(f'Error creating card: {str(e)}')
        return jsonify({'error': 'Failed to create card'}), 500
    finally:
        session.close()


@cards_router.route('/cards/<int:card_id>', methods=['DELETE'])
@require_auth
def delete_card(card_id):
    try:
        session = Session()
        card = session.query(Card).filter_by(id=card_id, user_id=get_user_id()).first()

        if not card:
            return jsonify({'error': 'Card not found'}), 404

        session.delete(card)
        session.commit()

        return '', 204

    except Exception as e:
        logger.error(f'Error deleting card: {str(e)}')
        return jsonify({'error': 'Failed to delete card'}), 500
    finally:
        session.close()


@cards_router.route('/cards/search', methods=['GET'])
@require_auth
def search_cards():
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])

        session = Session()
        # Simple search implementation - can be enhanced with full-text search
        cards = session.query(Card).filter(
            Card.user_id == get_user_id(),
            (Card.title.ilike(f'%{query}%') | Card.content.ilike(f'%{query}%'))
        ).all()

        return jsonify([{
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        } for card in cards])

    except Exception as e:
        logger.error(f'Error searching cards: {str(e)}')
        return jsonify({'error': 'Failed to search cards'}), 500
    finally:
        session.close()


@cards_router.route('/cards/generate', methods=['POST'])
@require_auth
def generate_card():
    try:
        # Example card generation - can be enhanced with AI/ML
        session = Session()
        card = Card(
            user_id=get_user_id(),
            title='Generated Card',
            icon='fas fa-magic',
            content='This is an automatically generated card.'
        )
        session.add(card)
        session.commit()

        return jsonify({
            'id': card.id,
            'title': card.title,
            'icon': card.icon,
            'content': card.content,
            'actions': card.actions
        }), 201

    except Exception as e:
        logger.error(f'Error generating card: {str(e)}')
        return jsonify({'error': 'Failed to generate card'}), 500
    finally:
        session.close()
