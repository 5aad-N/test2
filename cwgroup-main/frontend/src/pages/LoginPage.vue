<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="text-center mb-4">Login</h2>

      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="credentials.username"
            type="text"
            class="form-control"
            placeholder="Enter your username"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            class="form-control"
            placeholder="Enter your password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="userStore.loading"
        >
          {{ userStore.loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="text-center mt-3 mb-0">
        Don't have an account?
        <router-link to="/signup" class="text-decoration-none">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/user';
import type { LoginCredentials } from '@/types/models';

const router = useRouter();
const userStore = useUserStore();

const credentials = ref<LoginCredentials>({
  username: '',
  password: '',
});

const errorMessage = ref<string | null>(null);

const handleLogin = async () => {
  errorMessage.value = null;
  const success = await userStore.login(credentials.value);

  if (success) {
    router.push('/');
  } else {
    errorMessage.value = userStore.error || 'Login failed. Please check your credentials.';
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f8f9fa;
  padding: 2rem 1rem;
}

.auth-card {
  max-width: 400px;
  width: 100%;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
}
</style>
