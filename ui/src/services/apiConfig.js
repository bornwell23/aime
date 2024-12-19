import axios from 'axios';
import { Logger } from '../../../common/logger.js';
import { Definitions } from '/app/common/definitions.js';

const definitions = new Definitions();

// Create logger instance
const logger = new Logger({
  serviceName: 'api-config',
  logLevel: 'DEBUG'
});


// Default API version
const DEFAULT_VERSION = definitions.api.version || 'V1';
logger.debug(`Default API version: ${DEFAULT_VERSION}`);

const defaultApiUrl = `${definitions.server.api_url}/api/${definitions.api.version}`;

// Base configuration for API client
export function createApiClient(url) {
  const instance = axios.create({
    baseURL: url,
    timeout: definitions.api.timeout,
    headers: {
      'Content-Type': 'application/json',
    }
  });

  // Request interceptor for adding auth token
  instance.interceptors.request.use(
    config => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    error => {
      return Promise.reject(error);
    }
  );

  // Response interceptor for error handling
  instance.interceptors.response.use(
    response => response,
    async error => {
      const originalRequest = error.config;

      // If unauthorized and not already retried
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          // Attempt to refresh token or re-authenticate
          const refreshedToken = await refreshAuthentication();
          
          // Update token in localStorage
          localStorage.setItem('authToken', refreshedToken);
          
          // Retry original request with new token
          originalRequest.headers['Authorization'] = `Bearer ${refreshedToken}`;
          return instance(originalRequest);
        } catch (refreshError) {
          // Logout user if refresh fails
          logger.error('Authentication refresh failed', refreshError);
          logout();
          return Promise.reject(refreshError);
        }
      }

      return Promise.reject(error);
    }
  );

  return instance;
}

// Authentication methods
export async function login(username, password) {
  try {
    // Use server as the proxy for auth-service
    const authClient = createApiClient(defaultApiUrl);
    
    // Use FormData to match FastAPI's OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await authClient.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    const { access_token } = response.data;
    
    // Store token in localStorage
    localStorage.setItem('authToken', access_token);
    
    logger.info('Login successful');
    return response.data;
  } catch (error) {
    logger.error('Login failed', error);
    throw error;
  }
}

export async function register(username, email, password) {
  try {
    logger.info(`Attempting to register user: ${username}`);
    const authClient = createApiClient(defaultApiUrl);
    logger.info(`Sending registration data: ${JSON.stringify({ username, email, password })} to server at ${definitions.server.api_url}`);
    return authClient.post('/auth/register', {
      username,
      email,
      password
    }).then(response => {
      logger.info(`User ${username} registered successfully`);
      return response.data;
    }).catch(error => {
      logger.error('Registration post failed', error);
      throw error;
    });
  } catch (error) {
    logger.error('Registration failed', error);
    throw error;
  }
}

export async function refreshAuthentication() {
  try {
    const authClient = createApiClient(defaultApiUrl);
    const currentToken = localStorage.getItem('authToken');
    
    // Validate current token or request a new one
    const response = await authClient.post('/token/refresh', { 
      token: currentToken 
    });
    
    return response.data.access_token;
  } catch (error) {
    logger.error('Authentication refresh failed', error);
    throw error;
  }
}

export function logout() {
  try {
    const authClient = createApiClient(defaultApiUrl);
    
    // Call server logout endpoint to invalidate token
    return authClient.post(`/auth/logout`);
  } catch (error) {
    logger.error('Logout failed', error);
    throw error;
  } finally {
    // Always remove the token from localStorage
    localStorage.removeItem('authToken');
    logger.info('User logged out');
  }
}

export function getCurrentUser() {
  try {
    const authClient = createApiClient(defaultApiUrl);
    return authClient.get(`/users/me`);
  } catch (error) {
    logger.error('Failed to fetch current user', error);
    throw error;
  }
}

// Export API client creator
export default {
  getClient: (api = null) => createApiClient(api == null ? defaultApiUrl : api)
};
