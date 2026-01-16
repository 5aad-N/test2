<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-body">
            <!-- Header -->
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h2 class="mb-0">My Profile</h2>
              <button
                v-if="!editMode"
                @click="enterEditMode"
                class="btn btn-primary"
              >
                <i class="bi bi-pencil me-1"></i>
                Edit Profile
              </button>
            </div>

            <!-- Success Message -->
            <div v-if="successMessage" class="alert alert-success" role="alert">
              {{ successMessage }}
            </div>

            <!-- View Mode -->
            <div v-if="!editMode && userStore.user">
              <div class="text-center mb-4">
                <img
                  :src="userStore.user.profile_image || placeholderImage"
                  class="profile-image-large"
                  alt="Profile"
                />
              </div>

              <div class="profile-info">
                <div class="mb-3">
                  <label class="form-label fw-bold text-muted">Username</label>
                  <p class="fs-5">{{ userStore.user.username }}</p>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold text-muted">Email</label>
                  <p class="fs-5">{{ userStore.user.email }}</p>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold text-muted">Date of Birth</label>
                  <p class="fs-5">{{ userStore.user.date_of_birth || 'Not provided' }}</p>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold text-muted">Currency</label>
                  <p class="fs-5">{{ getCurrencyDisplay(userStore.user.currency_preference) }}</p>
                </div>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-else>
              <div v-if="userStore.error" class="alert alert-danger" role="alert">
                {{ userStore.error }}
              </div>

              <form @submit.prevent="handleUpdate">
                <!-- Profile Image Upload -->
                <div class="text-center mb-4">
                  <div class="profile-upload-container" @click="fileInput?.click()">
                    <img
                      :src="imagePreview"
                      class="profile-image-large"
                      alt="Profile"
                    />
                    <div class="upload-overlay">
                      <i class="bi bi-camera"></i>
                      <br />
                      CHANGE
                    </div>
                  </div>
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/jpeg,image/jpg,image/png"
                    @change="handleImageChange"
                    style="display: none"
                  />
                  <br />
                  <small class="text-muted">Click to change profile image</small>
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    id="email"
                    v-model="formData.email"
                    type="email"
                    :class="['form-control', { 'is-invalid': userStore.errors?.email }]"
                    required
                  />
                  <div v-if="userStore.errors?.email" class="invalid-feedback">
                    {{ userStore.errors.email.join(', ') }}
                  </div>
                </div>

                <!-- Date of Birth -->
                <div class="mb-3">
                  <label for="dob" class="form-label">Date of Birth</label>
                  <input
                    id="dob"
                    v-model="formData.date_of_birth"
                    type="date"
                    :class="['form-control', { 'is-invalid': userStore.errors?.date_of_birth }]"
                  />
                  <div v-if="userStore.errors?.date_of_birth" class="invalid-feedback">
                    {{ userStore.errors.date_of_birth.join(', ') }}
                  </div>
                </div>

                <!-- Currency Preference -->
                <div class="mb-3">
                  <label for="currency" class="form-label">Display Currency</label>
                  <select
                    id="currency"
                    v-model="formData.currency_preference"
                    class="form-select"
                  >
                    <option
                      v-for="currency in currencyOptions"
                      :key="currency.code"
                      :value="currency.code"
                    >
                      {{ currency.symbol }} - {{ currency.name }}
                    </option>
                  </select>
                  <small class="text-muted">Prices will be displayed in this currency</small>
                </div>

                <!-- Username (read-only) -->
                <div class="mb-3">
                  <label class="form-label">Username</label>
                  <input
                    type="text"
                    class="form-control"
                    :value="userStore.user?.username"
                    disabled
                  />
                  <small class="text-muted">Username cannot be changed</small>
                </div>

                <!-- Action Buttons -->
                <div class="d-flex gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="userStore.loading"
                  >
                    <i class="bi bi-check-circle me-1"></i>
                    {{ userStore.loading ? 'Saving...' : 'Save Changes' }}
                  </button>
                  <button
                    type="button"
                    @click="cancelEdit"
                    class="btn btn-secondary"
                    :disabled="userStore.loading"
                  >
                    <i class="bi bi-x-circle me-1"></i>
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUserStore } from '@/store/user';
import type { ProfileUpdateData, CurrencyCode } from '@/types/models';
import { getCurrencyOptions, CURRENCIES } from '@/utils/currency';

const userStore = useUserStore();
const editMode = ref(false);
const placeholderImage = 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png';
const currencyOptions = getCurrencyOptions();

const fileInput = ref<HTMLInputElement | null>(null);

const formData = ref<ProfileUpdateData>({
  email: userStore.user?.email || '',
  date_of_birth: userStore.user?.date_of_birth || undefined,
  currency_preference: userStore.user?.currency_preference || 'USD',
});

const getCurrencyDisplay = (code: CurrencyCode): string => {
  const currency = CURRENCIES[code];
  return `${currency.symbol} ${currency.name}`;
};

const selectedImage = ref<File | null>(null);
const successMessage = ref<string | null>(null);

const imagePreview = computed(() => {
  if (selectedImage.value) {
    return URL.createObjectURL(selectedImage.value);
  }
  return userStore.user?.profile_image || placeholderImage;
});

const enterEditMode = () => {
  editMode.value = true;
  successMessage.value = null;

  // Reset error states
  userStore.error = null;
  userStore.errors = null;

  formData.value = {
    email: userStore.user?.email || '',
    date_of_birth: userStore.user?.date_of_birth || undefined,
    currency_preference: userStore.user?.currency_preference || 'USD',
  };
  selectedImage.value = null;
};

const handleImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedImage.value = target.files[0];
  }
};

const handleUpdate = async () => {
  successMessage.value = null;

  const updateData: ProfileUpdateData = {
    email: formData.value.email,
    date_of_birth: formData.value.date_of_birth,
    currency_preference: formData.value.currency_preference,
  };

  if (selectedImage.value) {
    updateData.profile_image = selectedImage.value;
  }

  const success = await userStore.updateProfile(updateData);

  if (success) {
    editMode.value = false;
    selectedImage.value = null;
    successMessage.value = 'Profile updated successfully!';

    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = null;
    }, 3000);
  }
};

const cancelEdit = () => {
  editMode.value = false;
  selectedImage.value = null;
  successMessage.value = null;
  userStore.error = null;
  userStore.errors = null;
};
</script>

<style scoped>
.profile-image-large {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #dee2e6;
}

.profile-upload-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.75rem;
  font-weight: bold;
}

.upload-overlay i {
  font-size: 1.5rem;
}

.profile-upload-container:hover .upload-overlay {
  opacity: 1;
}

.profile-info p {
  margin-bottom: 0.5rem;
}

.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>