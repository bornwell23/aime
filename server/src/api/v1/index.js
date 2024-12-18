import express from 'express';
import exampleRoutes from './routes/example.routes.js';
import authRoutes from './routes/auth.routes.js';

const router = express.Router();

// Import route modules

// Register routes
router.use('/examples', exampleRoutes);
router.use('/auth', authRoutes);

// Health check endpoint
router.get('/health', (req, res) => {
    res.json({ status: 'healthy', version: 'v1' });
});

export default router;
