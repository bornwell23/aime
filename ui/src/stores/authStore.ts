import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import AuthService from '../services/authService';
import { 
  AuthState, 
  LoginRequest, 
  User 
} from '/app/common/types';
import { Logger } from '/app/common/logger.js';

// Create logger
const logger = new Logger({ 
  serviceName: 'AuthStore', 
  logLevel: 'DEBUG' 
});

export const useAuthStore = defineStore('auth', () => {
  // State
  const authState = ref<AuthState>({
    isAuthenticated: false
  });

  // Computed
  const user = computed<User | undefined>(() => authState.value.user);
  const isAuthenticated = computed(() => {
    logger.debug(`AuthStore isAuthenticated called: ${authState.value.isAuthenticated}`);
    return authState.value.isAuthenticated;
  });

  // Actions
  async function login(credentials: LoginRequest) {
    try {
      const newAuthState = await AuthService.login(credentials);
      logger.info('Login successful', newAuthState);
      authState.value = newAuthState;
      return newAuthState;
    } catch (error) {
      // Reset auth state on login failure
      logger.error('Login failed', error);
      authState.value = { isAuthenticated: false };
      throw error;
    }
  }

  function logout() {
    logger.info('Logging out');
    AuthService.logout();
    authState.value = { isAuthenticated: false };
  }

  // Token refresh method
  async function refreshToken() {
    try {
      logger.debug('Attempting to refresh token');
      const refreshedState = await AuthService.refreshToken();
      if (refreshedState) {
        logger.info('Token refreshed successfully', refreshedState);
        authState.value = refreshedState;
      } else {
        logger.warn('Token refresh failed, logging out');
        logout();
      }
      return refreshedState;
    } catch (error) {
      logger.error('Token refresh error', error);
      logout();
      return null;
    }
  }

  // Initialize auth state
  async function initializeAuthState() {
    logger.debug('Initializing auth state...');
    try {
      // Attempt to initialize token
      const currentState = await AuthService.initializeToken();
      
      logger.debug('Initialization result', currentState);
      
      // Update state based on initialization result
      if (currentState) {
        authState.value = currentState;
      } else {
        // No valid token found
        authState.value = { isAuthenticated: false };
      }
    } catch (error) {
      logger.error('Auth state initialization error', error);
      authState.value = { isAuthenticated: false };
    }
  }

  // Expose methods and state
  return {
    authState,
    user,
    isAuthenticated,
    login,
    logout,
    refreshToken,
    initializeAuthState
  };
});
