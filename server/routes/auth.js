const express = require('express');
const axios = require('axios');
const router = express.Router();
const logger = require('../common/logger');

// Proxy for authentication service
router.post('/token', async (req, res) => {
  try {
    // Forward the request to auth-service
    const response = await axios.post('http://auth-service:8000/token', req.body, {
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

router.post('/register', async (req, res) => {
  try {
    // Forward the request to auth-service
    const response = await axios.post('http://auth-service:8000/register', req.body);

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
        error: 'Authentication service is unavailable',
        details: error.message 
      });
    }
  }
});

module.exports = router;
