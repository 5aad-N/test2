<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title mb-4">Edit Listing</h2>

            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div v-else-if="loadError" class="alert alert-danger">
              {{ loadError }}
            </div>

            <form v-else @submit.prevent="handleSubmit">
              <!-- Picture Upload -->
              <div class="mb-3">
                <label class="form-label">Item Picture</label>
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
                    <span>Click to upload new image</span>
                  </div>
                </div>
                <small class="text-muted">Leave unchanged to keep current image</small>
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

              <!-- Starting Price (Read-only) -->
              <div class="mb-3">
                <label for="price" class="form-label">Starting Price ($)</label>
                <input
                  :value="originalItem?.starting_price"
                  type="text"
                  class="form-control"
                  id="price"
                  disabled
                />
                <small class="text-muted">Starting price cannot be changed</small>
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
                  :disabled="itemsStore.loading"
                >
                  {{ itemsStore.loading ? 'Saving...' : 'Save Changes' }}
                </button>
                <router-link :to="`/items/${itemId}`" class="btn btn-secondary">
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
import { useRoute, useRouter } from 'vue-router';
import { useItemsStore } from '@/store/items';
import { useToast } from 'vue-toastification';
import type { Item, ItemUpdateData } from '@/types/models';

const route = useRoute();
const router = useRouter();
const itemsStore = useItemsStore();
const toast = useToast();

const itemId = computed(() => Number(route.params.id));
const fileInput = ref<HTMLInputElement | null>(null);
const imagePreview = ref<string>('');
const loading = ref(true);
const loadError = ref<string | null>(null);
const originalItem = ref<Item | null>(null);

const formData = ref<ItemUpdateData>({
  title: '',
  description: '',
  end_date: '',
  picture: undefined,
});

const minDateTime = computed(() => {
  const now = new Date();
  now.setMinutes(now.getMinutes() + 10);
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

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

const handleSubmit = async () => {
  const endDate = new Date(formData.value.end_date).toISOString();

  const success = await itemsStore.updateItem(itemId.value, {
    ...formData.value,
    end_date: endDate,
  });

  if (success) {
    toast.success('Item updated successfully!');
    router.push(`/items/${itemId.value}`);
  } else {
    toast.error(itemsStore.error || 'Failed to update item');
  }
};

onMounted(async () => {
  loading.value = true;

  const success = await itemsStore.fetchItemDetail(itemId.value);

  if (success && itemsStore.currentItem) {
    originalItem.value = itemsStore.currentItem;

    // Pre-populate form
    formData.value.title = itemsStore.currentItem.title;
    formData.value.description = itemsStore.currentItem.description;

    // Convert ISO date to datetime-local format
    const endDate = new Date(itemsStore.currentItem.end_date);
    formData.value.end_date = endDate.toISOString().slice(0, 16);

    // Set current image as preview
    if (itemsStore.currentItem.picture) {
      imagePreview.value = itemsStore.currentItem.picture;
    }
  } else {
    loadError.value = itemsStore.error || 'Failed to load item';
  }

  loading.value = false;
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
