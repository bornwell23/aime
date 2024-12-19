import express from 'express';
import baseRoutes from './routes/base.js';
import authRoutes from './routes/auth.js';

const router = express.Router();

// Import route modules

// Register routes
router.use('/base', baseRoutes);
router.use('/auth', authRoutes);

// Health check endpoint
router.get('/health', (req, res) => {
    res.json({ status: 'healthy', version: 'v1' });
});

export default router;
