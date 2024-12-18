// Shared API Types and Interfaces

// Base Response Type
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// User-related Types
export interface User {
  id: string;
  username: string;
  email: string;
  createdAt: string;
}

export interface UserCreateRequest {
  username: string;
  email: string;
  password: string;
}

export interface UserUpdateRequest {
  username?: string;
  email?: string;
  password?: string;
}

// Authentication Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthTokenResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
  expiresAt: number; // Unix timestamp
}

export interface AuthState {
  isAuthenticated: boolean;
  user?: User;
  accessToken?: string;
  refreshToken?: string;
  expiresAt?: number;
}

export interface LoginErrorResponse {
  code: 'INVALID_CREDENTIALS' | 'ACCOUNT_LOCKED' | 'UNVERIFIED_EMAIL';
  message: string;
}

// Pagination Types
export interface PaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

// Generic Error Codes
export enum ApiErrorCode {
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  NOT_FOUND = 'NOT_FOUND',
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
}
