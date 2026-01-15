import { defineStore } from 'pinia';
import { authService } from '@/services/auth';
import { apiClient } from '@/services/api';
import type { User, LoginCredentials, SignupData, ProfileUpdateData } from '@/types/models';
import type { AuthResponse } from '@/types/api';

declare global {
    interface Window {
        currentUser: User | null;
    }
}

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  errors: Record<string, string[]> | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: window.currentUser || null,
    isAuthenticated: !!window.currentUser,
    loading: false,
    error: null,
    errors: null,
  }),

  actions: {
    /**
     * Login user with credentials
     */
    async login(credentials: LoginCredentials): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await authService.login(credentials);

        if (response.success && response.data) {
          this.user = response.data.user;
          this.isAuthenticated = true;
          return true;
        } else {
          this.error = response.error || 'Login failed';
          return false;
        }
      } catch (err) {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Register new user
     */
    async signup(data: SignupData): Promise<boolean> {
      this.loading = true;
      this.error = null;
      this.errors = null;

      try {
        const response = await authService.signup(data);

        if (response.success && response.data) {
          this.user = response.data.user;
          this.isAuthenticated = true;
          return true;
        } else {
          this.error = response.error || 'Signup failed';
          this.errors = response.errors || null;
          return false;
        }
      } catch (err) {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Logout current user
     */
    async logout(): Promise<void> {
      await authService.logout();
      this.user = null;
      this.isAuthenticated = false;
    },

    /**
     * Fetch current authenticated user
     */
    async fetchCurrentUser(): Promise<void> {
      try {
        const response = await authService.getCurrentUser();
        if (response.success && response.data) {
          this.user = response.data.user;
          this.isAuthenticated = true;
        }
      } catch (err) {
        this.isAuthenticated = false;
      }
    },

    /**
     * Update user profile
     */
    async updateProfile(data: ProfileUpdateData): Promise<boolean> {
      this.loading = true;
      this.error = null;
      this.errors = null;

      const formData = new FormData();
      formData.append('email', data.email);

      if (data.date_of_birth) {
        formData.append('date_of_birth', data.date_of_birth);
      }

      if (data.profile_image) {
        formData.append('profile_image', data.profile_image);
      }

      try {
        const response = await apiClient.putFormData<AuthResponse>('/api/profile/', formData);

        if (response.success && response.data) {
          this.user = response.data.user;
          return true;
        } else {
          // If the backend returns a general error message
          this.error = response.error || 'Update failed';
          
          // Capture field-specific errors
          this.errors = response.errors || null; 
          
          return false;
        }
      } catch (err) {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },
  },
});