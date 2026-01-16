/**
 * Centralized API client for making fetch requests with CSRF token handling
 */

import type { ApiResponse } from '@/types/api';

class ApiClient {
  private csrfFetched = false;

  /**
   * Fetch CSRF token from cookie
   */
  private getCookie(name: string): string {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || '';
    return '';
  }

  /**
   * Ensure CSRF cookie is set before making POST/PUT requests
   */
  private async ensureCsrf(): Promise<void> {
    if (this.csrfFetched) return;

    const token = this.getCookie('csrftoken');
    if (!token) {
      await fetch('/api/csrf/', {
        method: 'GET',
        credentials: 'include',
      });
    }
    this.csrfFetched = true;
  }

  /**
   * Make GET request
   */
  async get<T>(url: string): Promise<ApiResponse<T>> {
    
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include', // Changed for proxy support
      headers: {
        'Accept': 'application/json',
      },
    });
    return response.json();
  }

  /**
   * Make POST request with JSON body
   */
  async post<T>(url: string, data: any): Promise<ApiResponse<T>> {
    await this.ensureCsrf();
    const token = this.getCookie('csrftoken');

    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include', // Changed for proxy support
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  /**
   * Make POST request with FormData (for file uploads)
   */
  async postFormData<T>(url: string, formData: FormData): Promise<ApiResponse<T>> {
    await this.ensureCsrf();
    const token = this.getCookie('csrftoken');

    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': token,
      },
      body: formData,
    });

    return response.json();
  }

  /**
   * Make PUT request with JSON body
   */
  async put<T>(url: string, data: any): Promise<ApiResponse<T>> {
    await this.ensureCsrf();
    const token = this.getCookie('csrftoken');

    const response = await fetch(url, {
      method: 'PUT',
      credentials: 'include', // Changed for proxy support
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  /**
   * Make PUT request with FormData (for file uploads)
   */
  async putFormData<T>(url: string, formData: FormData): Promise<ApiResponse<T>> {
    await this.ensureCsrf();
    const token = this.getCookie('csrftoken');

    const response = await fetch(url, {
      method: 'PUT',
      credentials: 'include', // Changed for proxy support
      headers: {
        'X-CSRFToken': token,
      },
      body: formData,
    });
    return response.json();
  }

  /**
   * Make DELETE request
   */
  async delete<T>(url: string): Promise<ApiResponse<T>> {
    await this.ensureCsrf();
    const token = this.getCookie('csrftoken');

    const response = await fetch(url, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'X-CSRFToken': token,
      },
    });
    return response.json();
  }
}

export const apiClient = new ApiClient();
