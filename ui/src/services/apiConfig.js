import axios from 'axios';
import { Logger } from '/app/common/logger.js';

// Create logger instance
const logger = new Logger({
  serviceName: 'api-config',
  logLevel: process.env.VUE_APP_LOG_LEVEL || 'INFO',
  logFileName: 'ui.log'
});

// API Configuration
const API_VERSIONS = {
  V1: '/api/v1',
  V2: '/api/v2',
  // Add more versions as needed
};

// Create axios instance with base configuration
const createApiClient = (version = process.env.VUE_APP_API_VERSION || 'V1') => {
  logger.info(`Creating API client for version: ${version}`);

  const client = axios.create({
    baseURL: `${process.env.VUE_APP_API_URL || '/'}${API_VERSIONS[version]}`,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    }
  });

  // Add request interceptor for logging
  client.interceptors.request.use(
    (config) => {
      logger.debug(`API Request: ${config.method.toUpperCase()} ${config.url}`);
      logger.debug(`Request Data: ${JSON.stringify(config.data)}`);
      return config;
    },
    (error) => {
      logger.error(`API Request Error: ${error.message}`);
      return Promise.reject(error);
    }
  );

  // Add response interceptor for logging
  client.interceptors.response.use(
    (response) => {
      logger.debug(`API Response: ${response.status} ${response.config.url}`);
      logger.debug(`Response Data: ${JSON.stringify(response.data)}`);
      return response;
    },
    (error) => {
      if (error.response) {
        logger.error(`API Response Error: ${error.response.status} ${error.response.statusText}`);
        logger.error(`Error Data: ${JSON.stringify(error.response.data)}`);
      } else if (error.request) {
        logger.error(`API Request Error: No response received`);
      } else {
        logger.error(`API Error: ${error.message}`);
      }
      return Promise.reject(error);
    }
  );

  return client;
};

// Export API client creator and version constants
export default {
  getClient: createApiClient,
  VERSIONS: API_VERSIONS,
};
