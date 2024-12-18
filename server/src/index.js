import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

import { Logger } from '/app/common/logger.js';
import apiRouter from './api/index.js';
import { errorHandler } from './middleware/error.middleware.js';

// Load environment variables
dotenv.config();

// Create logger instance
const logger = new Logger({
    serviceName: 'server',
    logLevel: process.env.VUE_APP_LOG_LEVEL || 'INFO',
    logFileName: 'server.log'
});

const app = express();
const port = process.env.BACK_PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
    logger.info(`${req.method} ${req.path}`);
    next();
});

// API Routes
app.use('/api', apiRouter);

// Base route
app.get('/', (req, res) => {
    logger.info('Base route accessed');
    res.json({
        message: 'Welcome to Aime API',
        documentation: '/api/v1/docs',
        health: '/api/v1/health'
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    logger.error(`Unhandled error: ${err.message}`);
    errorHandler(err, req, res, next);
});

// Start server
const server = app.listen(port, '0.0.0.0', () => {
    logger.info(`Server running on port ${port}`);
    logger.info(`Environment: ${process.env.NODE_ENV}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    logger.info('SIGTERM received. Shutting down gracefully');
    server.close(() => {
        logger.info('Server closed');
        process.exit(0);
    });
});

export default app;
