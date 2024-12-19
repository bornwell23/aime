import express from 'express';
import { Logger } from '/app/common/logger.js';
import v1Router from './v1/index.js';
import { Definitions } from '/app/common/definitions.js';

const definitions = new Definitions();

const logger = new Logger({
    serviceName: 'api-router',
    logLevel: definitions.server.logLevel || 'INFO',
    logFileName: 'api.log'
});

const router = express.Router();

// API version routes
router.use(`/${definitions.api.version}`, definitions.api.routers[definitions.api.version] || v1Router);

// Logging for API routes
router.use((req, res, next) => {
    logger.debug(`API Route: ${req.method} ${req.path}`);
    next();
});

// Handle undefined versions
router.use('/*', (req, res) => {
    logger.warn(`Undefined API version accessed: ${req.originalUrl}`);
    res.status(404).json({ 
        error: 'API version not found',
        details: 'The requested API version does not exist'
    });
});

export default router;
