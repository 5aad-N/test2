<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title mb-4">Create Auction Listing</h2>

            <div v-if="itemsStore.error" class="alert alert-danger">
              {{ itemsStore.error }}
            </div>

            <form @submit.prevent="handleSubmit">
              <!-- Picture Upload -->
              <div class="mb-3">
                <label class="form-label">Item Picture *</label>
                <div
                  class="image-upload-container"
                  @click="triggerFileInput"
                  role="button"
                >
                  <img
                    v-if="imagePreview"
                    :src="imagePreview"
                    alt="Preview"
                    class="preview-image"
                  />
                  <div v-else class="upload-placeholder">
                    <span>Click to upload image</span>
                  </div>
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/jpeg,image/jpg,image/png"
                  @change="handleImageChange"
                  hidden
                />
              </div>

              <!-- Title -->
              <div class="mb-3">
                <label for="title" class="form-label">Title *</label>
                <input
                  v-model="formData.title"
                  type="text"
                  class="form-control"
                  id="title"
                  required
                />
              </div>

              <!-- Description -->
              <div class="mb-3">
                <label for="description" class="form-label">Description *</label>
                <textarea
                  v-model="formData.description"
                  class="form-control"
                  id="description"
                  rows="4"
                  required
                ></textarea>
              </div>

              <!-- Starting Price -->
              <div class="mb-3">
                <label for="price" class="form-label">Starting Price ($) *</label>
                <input
                  v-model="formData.starting_price"
                  type="number"
                  step="0.01"
                  min="0.01"
                  class="form-control"
                  id="price"
                  required
                />
              </div>

              <!-- End Date -->
              <div class="mb-3">
                <label for="endDate" class="form-label">End Date & Time *</label>
                <input
                  v-model="formData.end_date"
                  type="datetime-local"
                  class="form-control"
                  id="endDate"
                  :min="minDateTime"
                  required
                />
              </div>

              <!-- Buttons -->
              <div class="d-flex gap-2">
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="itemsStore.loading || !formData.picture"
                >
                  {{ itemsStore.loading ? 'Creating...' : 'Create Listing' }}
                </button>
                <router-link to="/items" class="btn btn-secondary">
                  Cancel
                </router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useItemsStore } from '@/store/items';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import type { ItemCreateData } from '@/types/models';

const itemsStore = useItemsStore();
const router = useRouter();
const toast = useToast();

const fileInput = ref<HTMLInputElement | null>(null);
const imagePreview = ref<string>('');

const formData = ref<ItemCreateData>({
  title: '',
  description: '',
  starting_price: '',
  picture: null as any,
  end_date: '',
});

const minDateTime = computed(() => {
  const now = new Date();
  now.setMinutes(now.getMinutes() + 10); // At least 10 minutes in future
  return now.toISOString().slice(0, 16);
});

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (file) {
    formData.value.picture = file;

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

const handleSubmit = async () => {
  if (!formData.value.picture) {
    toast.warning('Please select an image');
    return;
  }

  // Convert datetime-local to ISO string
  const endDate = new Date(formData.value.end_date).toISOString();

  const success = await itemsStore.createItem({
    ...formData.value,
    end_date: endDate,
  });

  if (success) {
    toast.success('Item created successfully!');
    router.push('/items');
  } else {
    toast.error(itemsStore.error || 'Failed to create item');
  }
};

onMounted(() => {
  // Set default end date to 7 days from now
  const defaultEnd = new Date();
  defaultEnd.setDate(defaultEnd.getDate() + 7);
  formData.value.end_date = defaultEnd.toISOString().slice(0, 16);
});
</script>

<style scoped>
.image-upload-container {
  width: 100%;
  height: 300px;
  border: 2px dashed #ccc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.2s;
}

.image-upload-container:hover {
  border-color: #0d6efd;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  text-align: center;
  color: #6c757d;
}
</style>
