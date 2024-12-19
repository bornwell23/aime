import { 
  LoginRequest, 
  AuthTokenResponse, 
  AuthState, 
  LoginErrorResponse,
  User
} from '/app/common/types';
import { Logger } from '/app/common/logger.js';

// Create logger
const logger = new Logger({ 
  serviceName: 'AuthService', 
  logLevel: 'DEBUG' 
});

class AuthService {
  private static STORAGE_KEY = 'auth_state';

  // Persist authentication state to local storage
  private static saveAuthState(state: AuthState): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(state));
    logger.debug('Auth state saved', state);
  }

  // Retrieve authentication state from local storage
  private static getAuthState(): AuthState {
    const storedState = localStorage.getItem(this.STORAGE_KEY);
    const parsedState = storedState ? JSON.parse(storedState) : {
      isAuthenticated: false
    };
    logger.debug('Retrieved auth state', parsedState);
    return parsedState;
  }

  // Check if the current token is expired
  private static isTokenExpired(expiresAt?: number): boolean {
    const expired = !expiresAt || Date.now() / 1000 > expiresAt;
    logger.debug('Token expiration check', { expiresAt, expired });
    return expired;
  }

  // Login method
  static async login(credentials: LoginRequest): Promise<AuthState> {
    try {
      logger.debug('Attempting login', credentials);
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      });

      if (!response.ok) {
        const errorData: LoginErrorResponse = await response.json();
        logger.error('Login failed', errorData);
        throw new Error(errorData.message);
      }

      const authResponse: AuthTokenResponse = await response.json();
      
      const authState: AuthState = {
        isAuthenticated: true,
        user: authResponse.user,
        accessToken: authResponse.accessToken,
        refreshToken: authResponse.refreshToken,
        expiresAt: authResponse.expiresAt
      };

      this.saveAuthState(authState);
      return authState;
    } catch (error) {
      logger.error('Login process error', error);
      throw error;
    }
  }

  // Logout method
  static logout(): void {
    logger.info('Logging out, removing auth state');
    localStorage.removeItem(this.STORAGE_KEY);
    // Optional: Call server-side logout endpoint
    fetch('/api/auth/logout', { method: 'POST' });
  }

  // Get current authentication state
  static getCurrentAuthState(): AuthState {
    const authState = this.getAuthState();
    
    // Check if token is expired
    if (this.isTokenExpired(authState.expiresAt)) {
      logger.warn('Current token is expired, logging out');
      this.logout();
      return { isAuthenticated: false };
    }

    return authState;
  }

  // Refresh token method
  static async refreshToken(): Promise<AuthState | null> {
    const currentState = this.getAuthState();
    
    if (!currentState.refreshToken) {
      logger.debug('No refresh token found');
      return null;
    }

    try {
      logger.debug('Attempting to refresh token');
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          refreshToken: currentState.refreshToken 
        })
      });

      if (!response.ok) {
        logger.warn('Token refresh failed');
        throw new Error('Token refresh failed');
      }

      const newTokens: AuthTokenResponse = await response.json();
      
      const newAuthState: AuthState = {
        isAuthenticated: true,
        user: newTokens.user,
        accessToken: newTokens.accessToken,
        refreshToken: newTokens.refreshToken,
        expiresAt: newTokens.expiresAt
      };

      this.saveAuthState(newAuthState);
      logger.info('Token refreshed successfully');
      return newAuthState;
    } catch (error) {
      logger.error('Token refresh error:', error);
      this.logout();
      return null;
    }
  }

  // Initialize token
  static async initializeToken(): Promise<AuthState | null> {
    logger.debug('Initializing token...');
    const currentState = this.getAuthState();
    
    // If already authenticated and token not expired, return current state
    if (currentState.isAuthenticated && !this.isTokenExpired(currentState.expiresAt)) {
      logger.debug('Using existing valid token');
      return currentState;
    }

    // If no refresh token, return null
    if (!currentState.refreshToken) {
      logger.debug('No refresh token found');
      return null;
    }

    try {
      logger.debug('Attempting to refresh token');
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          refreshToken: currentState.refreshToken 
        })
      });

      if (!response.ok) {
        logger.warn('Token refresh failed');
        throw new Error('Token refresh failed');
      }

      const newTokens: AuthTokenResponse = await response.json();
      
      const newAuthState: AuthState = {
        isAuthenticated: true,
        user: newTokens.user,
        accessToken: newTokens.accessToken,
        refreshToken: newTokens.refreshToken,
        expiresAt: newTokens.expiresAt
      };

      this.saveAuthState(newAuthState);
      logger.info('Token refreshed successfully');
      return newAuthState;
    } catch (error) {
      logger.error('Token initialization error', error);
      this.logout();
      return null;
    }
  }
}

export default AuthService;
