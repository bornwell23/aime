import axios from 'axios';
import { Logger } from '../../../common/logger.js';

// Create logger instance
const logger = new Logger({
  serviceName: 'api-config',
  logLevel: 'DEBUG'
});

// API Versions
const API_VERSIONS = {
  V1: '/api/v1',
  V2: '/api/v2',
  // Add more versions as needed
};

// Default API version
const DEFAULT_VERSION = process.env.VUE_APP_API_VERSION || 'V1';
logger.debug(`Default API version: ${DEFAULT_VERSION}`);

// Base configuration for API client
export function createApiClient(baseURL) {
  const instance = axios.create({
    baseURL: baseURL,
    timeout: 10000,
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
    const authClient = createApiClient(process.env.VUE_APP_API_URL);
    
    // Use FormData to match FastAPI's OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await authClient.post('/v1/auth/token', formData, {
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
    const authClient = createApiClient(process.env.VUE_APP_API_URL);
    
    return authClient.post('/auth/register', {
      username,
      email,
      password
    }).then(response => {
      logger.info(`User ${username} registered successfully`);
      return response.data;
    }).catch(error => {
      logger.error('Registration failed', error);
      throw error;
    });
  } catch (error) {
    logger.error('Registration failed', error);
    throw error;
  }
}

export async function refreshAuthentication() {
  try {
    const authClient = createApiClient(process.env.VUE_APP_API_URL);
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
    const authClient = createApiClient(process.env.VUE_APP_API_URL);
    
    // Call server logout endpoint to invalidate token
    return authClient.post('/v1/auth/logout');
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
    const authClient = createApiClient(process.env.VUE_APP_API_URL);
    return authClient.get('/users/me');
  } catch (error) {
    logger.error('Failed to fetch current user', error);
    throw error;
  }
}

// Export API client creator and version constants
export default {
  getClient: (version = DEFAULT_VERSION) => createApiClient(`${process.env.VUE_APP_API_URL}${API_VERSIONS[version]}`),
  VERSIONS: API_VERSIONS,
};
