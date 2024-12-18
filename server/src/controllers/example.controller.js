import { Logger } from '/app/common/logger.js';

const logger = new Logger({
    serviceName: 'example-controller',
    logLevel: process.env.VUE_APP_LOG_LEVEL || 'INFO'
});

export class ExampleController {
    async getAll(req, res) {
        try {
            logger.info('Fetching all items');
            // Example implementation
            const items = []; // Replace with actual data retrieval
            logger.debug(`Retrieved ${items.length} items`);
            res.json({ message: 'Get all items', items });
        } catch (error) {
            logger.error(`Error fetching items: ${error.message}`);
            res.status(500).json({ error: error.message });
        }
    }

    async getById(req, res) {
        try {
            const { id } = req.params;
            logger.info(`Fetching item with ID: ${id}`);
            
            // Simulate item retrieval
            const item = null; // Replace with actual data retrieval
            
            if (!item) {
                logger.warn(`Item not found with ID: ${id}`);
                return res.status(404).json({ message: 'Item not found' });
            }
            
            logger.debug(`Retrieved item: ${JSON.stringify(item)}`);
            res.json({ message: 'Get item by ID', item });
        } catch (error) {
            logger.error(`Error fetching item: ${error.message}`);
            res.status(500).json({ error: error.message });
        }
    }

    async create(req, res) {
        try {
            const { body } = req;
            logger.info('Creating new item');
            logger.debug(`Item data: ${JSON.stringify(body)}`);
            
            // Simulate item creation
            const newItem = body; // Replace with actual item creation logic
            
            logger.info(`Created item with data: ${JSON.stringify(newItem)}`);
            res.status(201).json({ message: 'Item created', item: newItem });
        } catch (error) {
            logger.error(`Error creating item: ${error.message}`);
            res.status(500).json({ error: error.message });
        }
    }

    async update(req, res) {
        try {
            const { id } = req.params;
            const { body } = req;
            
            logger.info(`Updating item with ID: ${id}`);
            logger.debug(`Update data: ${JSON.stringify(body)}`);
            
            // Simulate item update
            const updatedItem = { ...body, id }; // Replace with actual update logic
            
            logger.info(`Updated item: ${JSON.stringify(updatedItem)}`);
            res.json({ message: 'Item updated', item: updatedItem });
        } catch (error) {
            logger.error(`Error updating item: ${error.message}`);
            res.status(500).json({ error: error.message });
        }
    }

    async delete(req, res) {
        try {
            const { id } = req.params;
            
            logger.info(`Deleting item with ID: ${id}`);
            
            // Simulate item deletion
            const deletionResult = true; // Replace with actual deletion logic
            
            if (!deletionResult) {
                logger.warn(`Failed to delete item with ID: ${id}`);
                return res.status(404).json({ message: 'Item not found or deletion failed' });
            }
            
            logger.info(`Deleted item with ID: ${id}`);
            res.json({ message: 'Item deleted', id });
        } catch (error) {
            logger.error(`Error deleting item: ${error.message}`);
            res.status(500).json({ error: error.message });
        }
    }
}
