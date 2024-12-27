from flask import jsonify
from common.logging import logger


class BaseController:
    def get_all(self):
        try:
            logger.info('Fetching all items')
            # Example implementation
            items = []  # Replace with actual data retrieval
            logger.debug(f'Retrieved {len(items)} items')
            return jsonify({'message': 'Get all items', 'items': items})
        except Exception as error:
            logger.error(f'Error fetching items: {str(error)}')
            return jsonify({'error': str(error)}), 500

    def get_by_id(self, id):
        try:
            logger.info(f'Fetching item with id: {id}')
            # Example implementation
            item = {}  # Replace with actual data retrieval
            if not item:
                logger.warn(f'Item not found with id: {id}')
                return jsonify({'error': 'Item not found'}), 404
            return jsonify(item)
        except Exception as error:
            logger.error(f'Error fetching item: {str(error)}')
            return jsonify({'error': str(error)}), 500

    def create(self, data):
        try:
            logger.info('Creating new item')
            # Example implementation
            item = data  # Replace with actual data creation
            logger.debug(f'Created item: {item}')
            return jsonify(item), 201
        except Exception as error:
            logger.error(f'Error creating item: {str(error)}')
            return jsonify({'error': str(error)}), 500

    def update(self, id, data):
        try:
            logger.info(f'Updating item with id: {id}')
            # Example implementation
            item = data  # Replace with actual data update
            if not item:
                logger.warn(f'Item not found with id: {id}')
                return jsonify({'error': 'Item not found'}), 404
            logger.debug(f'Updated item: {item}')
            return jsonify(item)
        except Exception as error:
            logger.error(f'Error updating item: {str(error)}')
            return jsonify({'error': str(error)}), 500

    def delete(self, id):
        try:
            logger.info(f'Deleting item with id: {id}')
            # Example implementation
            success = True  # Replace with actual deletion
            if not success:
                logger.warn(f'Item not found with id: {id}')
                return jsonify({'error': 'Item not found'}), 404
            logger.debug(f'Deleted item with id: {id}')
            return jsonify({'message': 'Item deleted successfully'})
        except Exception as error:
            logger.error(f'Error deleting item: {str(error)}')
            return jsonify({'error': str(error)}), 500
