/**
 * Type definitions for API responses
 */

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  errors?: Record<string, string[]>;
}

export interface AuthResponse {
  user: import('./models').User;
}

export interface CsrfResponse {
  csrfToken: string;
}
