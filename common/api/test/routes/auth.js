import express from 'express';
import axios from 'axios';
import { Logger } from '/app/common/logger.js';
import { definitions } from '/app/common/definitions.js';

const router = express.Router();
const logger = new Logger({
    serviceName: 'auth-routes',
    logLevel: definitions.server.logLevel || 'INFO',
    logFileName: 'auth.log'
});

// Proxy for authentication service token endpoint
router.post('/token', async (req, res) => {
  try {
    // Forward the request to auth-service
    const response = await axios.post(`http://${definitions.auth.serviceName}:${definitions.auth.port}/token`, req.body, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    // Return the response from auth-service
    res.json(response.data);
  } catch (error) {
    logger.error('Authentication proxy error', error);
    
    // Check if there's a response from the auth service
    if (error.response) {
      // Forward the error response from auth-service
      res.status(error.response.status).json(error.response.data);
    } else {
      // Generic error if no response from auth-service
      res.status(500).json({ 
        error: 'Authentication service is unavailable',
        details: error.message 
      });
    }
  }
});

// Proxy for registration endpoint
router.post('/register', async (req, res) => {
  try {
    // Forward the request to auth-service
    const response = await axios.post(`http://${definitions.auth.serviceName}:${definitions.auth.port}/register`, req.body);

    // Return the response from auth-service
    res.json(response.data);
  } catch (error) {
    logger.error('Registration proxy error', error);
    
    // Check if there's a response from the auth service
    if (error.response) {
      // Forward the error response from auth-service
      res.status(error.response.status).json(error.response.data);
    } else {
      // Generic error if no response from auth-service
      res.status(500).json({ 
        error: 'Registration service is unavailable',
        details: error.message 
      });
    }
  }
});

// Logout endpoint
router.post('/logout', async (req, res) => {
  try {
    // Forward the request to auth-service
    const response = await axios.post(`http://${definitions.auth.serviceName}:${definitions.auth.port}/logout`, {}, {
      headers: {
        'Authorization': req.headers.authorization
      }
    });

    // Return the response from auth-service
    res.json(response.data);
  } catch (error) {
    logger.error('Logout proxy error', error);
    
    // Check if there's a response from the auth service
    if (error.response) {
      // Forward the error response from auth-service
      res.status(error.response.status).json(error.response.data);
    } else {
      // Generic error if no response from auth-service
      res.status(500).json({ 
        error: 'Logout service is unavailable',
        details: error.message 
      });
    }
  }
});

export default router;
