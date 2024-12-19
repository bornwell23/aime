// API Endpoint Definitions
import { 
  User, 
  UserCreateRequest, 
  UserUpdateRequest, 
  LoginRequest, 
  AuthTokenResponse,
  ApiResponse,
  PaginationParams,
  PaginatedResponse
} from './types';

export interface ApiContract {
  // Authentication Endpoints
  auth: {
    login(request: LoginRequest): Promise<ApiResponse<AuthTokenResponse>>;
    register(request: UserCreateRequest): Promise<ApiResponse<User>>;
    refreshToken(refreshToken: string): Promise<ApiResponse<AuthTokenResponse>>;
  };

  // User Management Endpoints
  users: {
    getProfile(userId: string): Promise<ApiResponse<User>>;
    updateProfile(userId: string, request: UserUpdateRequest): Promise<ApiResponse<User>>;
    listUsers(params?: PaginationParams): Promise<ApiResponse<PaginatedResponse<User>>>;
  };

  // Example of a generic CRUD interface that can be extended
  createGenericCrudEndpoints<T>(resourceName: string): {
    create(data: Partial<T>): Promise<ApiResponse<T>>;
    getById(id: string): Promise<ApiResponse<T>>;
    update(id: string, data: Partial<T>): Promise<ApiResponse<T>>;
    delete(id: string): Promise<ApiResponse<void>>;
    list(params?: PaginationParams): Promise<ApiResponse<PaginatedResponse<T>>>;
  };
}

// Optional: Utility function to create a base implementation
export function createApiClient(baseUrl: string): ApiContract {
  return {
    auth: {
      async login(request) {
        const response = await fetch(`${baseUrl}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(request)
        });
        return response.json();
      },
      async register(request) {
        const response = await fetch(`${baseUrl}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(request)
        });
        return response.json();
      },
      async refreshToken(refreshToken) {
        const response = await fetch(`${baseUrl}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refreshToken })
        });
        return response.json();
      },
      // Implement other auth methods similarly
    },
    users: {
      async getProfile(userId) {
        const response = await fetch(`${baseUrl}/users/${userId}`);
        return response.json();
      },
      // Implement other user methods similarly
    },
    createGenericCrudEndpoints(resourceName) {
      return {
        async create(data) {
          const response = await fetch(`${baseUrl}/${resourceName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });
          return response.json();
        },
        // Implement other CRUD methods similarly
      };
    }
  };
}
