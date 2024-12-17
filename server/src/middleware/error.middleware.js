import { Logger } from '/app/common/logger.js';

const logger = new Logger({
    serviceName: 'error-middleware',
    logLevel: process.env.LOG_LEVEL || 'INFO'
});

export const errorHandler = (err, req, res, next) => {
    // Log the full error stack in development
    if (process.env.NODE_ENV === 'development') {
        logger.error(`Full error stack: ${err.stack}`);
    }

    // Log the error message
    logger.error(`Error occurred: ${err.message}`);

    if (err.name === 'ValidationError') {
        logger.warn(`Validation Error: ${err.message}`);
        return res.status(400).json({
            error: 'Validation Error',
            details: err.message
        });
    }

    if (err.name === 'UnauthorizedError') {
        logger.warn(`Unauthorized Access: ${err.message}`);
        return res.status(401).json({
            error: 'Unauthorized',
            details: err.message
        });
    }

    // Generic server error
    res.status(500).json({
        error: 'Internal Server Error',
        details: process.env.NODE_ENV === 'development' ? err.message : 'An unexpected error occurred'
    });
};
