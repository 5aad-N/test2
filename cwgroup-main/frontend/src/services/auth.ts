/**
 * Authentication service for high-level auth operations
 */

import { apiClient } from './api';
import type { LoginCredentials, SignupData, ProfileUpdateData, User } from '@/types/models';
import type { ApiResponse, AuthResponse } from '@/types/api';

export const authService = {
  /**
   * Login user with credentials
   */
  async login(credentials: LoginCredentials): Promise<ApiResponse<AuthResponse>> {
    return apiClient.post<AuthResponse>('/api/auth/login/', credentials);
  },

  /**
   * Register new user
   */
  async signup(data: SignupData): Promise<ApiResponse<AuthResponse>> {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('email', data.email);
    formData.append('password1', data.password1);
    formData.append('password2', data.password2);

    if (data.date_of_birth) {
      formData.append('date_of_birth', data.date_of_birth);
    }

    if (data.profile_image) {
      formData.append('profile_image', data.profile_image);
    }

    return apiClient.postFormData<AuthResponse>('/api/auth/signup/', formData);
  },

  /**
   * Update user profile
   * Uses PUT with FormData to support file uploads and semantic correctness
   */
  async updateProfile(data: ProfileUpdateData): Promise<ApiResponse<{ user: User }>> {
    const formData = new FormData();
    formData.append('email', data.email);
    
    if (data.date_of_birth) {
      formData.append('date_of_birth', data.date_of_birth);
    }

    if (data.profile_image) {
      formData.append('profile_image', data.profile_image);
    }

    // Use putFormData to match the backend PUT requirement for multipart data
    return apiClient.putFormData<{ user: User }>('/api/auth/profile/update/', formData);
  },

  /**
   * Logout current user
   */
  async logout(): Promise<ApiResponse<null>> {
    return apiClient.post<null>('/api/auth/logout/', {});
  },

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<ApiResponse<AuthResponse>> {
    return apiClient.get<AuthResponse>('/api/auth/me/');
  },
};
