import { defineStore } from 'pinia';
import { authService } from '@/services/auth';
import { apiClient } from '@/services/api';
import type { User, LoginCredentials, SignupData, ProfileUpdateData, CurrencyCode } from '@/types/models';
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
      this.loading = true;
      this.error = null;
      try {
        const response = await authService.getCurrentUser();
        if (response.success && response.data) {
          this.user = response.data.user;
          this.isAuthenticated = true;
        } else {
          this.user = null;
          this.isAuthenticated = false;
        }
      } catch (err) {
        this.error = 'Network error while fetching user.';
        this.user = null;
        this.isAuthenticated = false;
      } finally {
        this.loading = false;
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

      if (data.currency_preference) {
        formData.append('currency_preference', data.currency_preference);
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

    /**
     * Quick update currency preference
     */
    async setCurrency(currency: CurrencyCode): Promise<boolean> {
      if (!this.user) return false;

      const formData = new FormData();
      formData.append('email', this.user.email);
      formData.append('currency_preference', currency);

      try {
        const response = await apiClient.putFormData<AuthResponse>('/api/profile/', formData);

        if (response.success && response.data) {
          this.user = response.data.user;
          return true;
        }
        return false;
      } catch {
        return false;
      }
    },
  },
});