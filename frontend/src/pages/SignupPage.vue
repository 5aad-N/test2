<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="text-center mb-4">Sign Up</h2>

      <div v-if="userStore.error" class="alert alert-danger" role="alert">
        {{ userStore.error }}
      </div>

      <form @submit.prevent="handleSignup">
        <!-- Profile Image Upload -->
        <div class="mb-3 text-center">
          <div class="profile-preview-container" @click="fileInput?.click()">
            <img
              :src="imagePreview"
              class="profile-preview"
              alt="Profile preview"
            />
            <div class="upload-overlay">CLICK TO UPLOAD</div>
          </div>
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/jpg,image/png"
            @change="handleImageChange"
            style="display: none"
          />
          <small class="text-muted d-block mt-1">Optional: Upload profile image</small>
          <small class="text-muted d-block">(JPG, JPEG, or PNG)</small>
          <div v-if="userStore.errors?.profile_image" class="text-danger small mt-1">
            {{ userStore.errors.profile_image[0] }}
          </div>
        </div>

        <!-- Username -->
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            class="form-control"
            :class="{ 'is-invalid': userStore.errors?.username }"
            placeholder="Choose a username"
            required
          />
          <div v-if="userStore.errors?.username" class="invalid-feedback">
            {{ userStore.errors.username[0] }}
          </div>
        </div>

        <!-- Email -->
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            class="form-control"
            :class="{ 'is-invalid': userStore.errors?.email }"
            placeholder="name@example.com"
            required
          />
          <div v-if="userStore.errors?.email" class="invalid-feedback">
            {{ userStore.errors.email[0] }}
          </div>
        </div>

        <!-- Date of Birth -->
        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth (Optional)</label>
          <input
            id="dob"
            v-model="formData.date_of_birth"
            type="date"
            class="form-control"
            :class="{ 'is-invalid': userStore.errors?.date_of_birth }"
          />
          <div v-if="userStore.errors?.date_of_birth" class="invalid-feedback">
            {{ userStore.errors.date_of_birth[0] }}
          </div>
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password1" class="form-label">Password</label>
          <input
            id="password1"
            v-model="formData.password1"
            type="password"
            class="form-control"
            :class="{ 'is-invalid': userStore.errors?.password1 }"
            placeholder="Enter password"
            required
          />
          <div v-if="userStore.errors?.password1" class="invalid-feedback">
            {{ userStore.errors.password1[0] }}
          </div>
          <small class="text-muted">
            Password must be at least 8 characters and not entirely numeric.
          </small>
        </div>

        <!-- Password Confirmation -->
        <div class="mb-3">
          <label for="password2" class="form-label">Confirm Password</label>
          <input
            id="password2"
            v-model="formData.password2"
            type="password"
            class="form-control"
            :class="{ 'is-invalid': userStore.errors?.password2 }"
            placeholder="Confirm password"
            required
          />
          <div v-if="userStore.errors?.password2" class="invalid-feedback">
            {{ userStore.errors.password2[0] }}
          </div>
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="userStore.loading"
        >
          {{ userStore.loading ? 'Creating account...' : 'Sign Up' }}
        </button>
      </form>

      <p class="text-center mt-3 mb-0">
        Already have an account?
        <router-link to="/login" class="text-decoration-none">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/user';
import type { SignupData } from '@/types/models';

const router = useRouter();
const userStore = useUserStore();

const placeholderImage = 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png';

const formData = ref<SignupData>({
  username: '',
  email: '',
  password1: '',
  password2: '',
  date_of_birth: undefined,
});

const selectedImage = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

const imagePreview = computed(() => {
  if (selectedImage.value) {
    return URL.createObjectURL(selectedImage.value);
  }
  return placeholderImage;
});

const handleImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedImage.value = target.files[0];
  }
};

const handleSignup = async () => {
  const signupData: SignupData = {
    ...formData.value,
    profile_image: selectedImage.value || undefined,
  };

  const success = await userStore.signup(signupData);

  if (success) {
    router.push('/');
  }
  // Errors are now stored in userStore.error and userStore.errors
  // They will be displayed automatically in the template
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 1rem;
}

.auth-card {
  max-width: 500px;
  width: 100%;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
}

.profile-preview-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.profile-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #dee2e6;
}

.upload-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.75rem;
  font-weight: bold;
  white-space: nowrap;
}

.profile-preview-container:hover .upload-overlay {
  opacity: 1;
}
</style>
