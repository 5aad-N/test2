<template>
  <div class="container-fluid mt-4">
    <div class="row">
      <!-- Filter Sidebar -->
      <div class="col-lg-3 col-md-4 mb-4">
        <div class="card filter-card sticky-top">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0"><i class="bi bi-funnel me-2"></i>Filters</h5>
            <button
              v-if="hasActiveFilters"
              class="btn btn-sm btn-link text-decoration-none"
              @click="clearFilters"
            >
              Reset
            </button>
          </div>
          <div class="card-body">
            <!-- Sort Options -->
            <div class="mb-4">
              <label class="form-label fw-bold">
                <i class="bi bi-sort-down me-2"></i>Sort By
              </label>
              <select v-model="sortBy" class="form-select form-select-sm">
                <option value="newest">Newest First</option>
                <option value="ending-soon">Ending Soon</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="most-bids">Most Bids</option>
              </select>
            </div>

            <!-- Price Range -->
            <div class="mb-4">
              <label class="form-label fw-bold">
                <i class="bi bi-currency-dollar me-2"></i>Price Range
              </label>
              <div class="row g-2">
                <div class="col-6">
                  <input
                    v-model.number="priceMin"
                    type="number"
                    class="form-control form-control-sm"
                    placeholder="Min"
                    min="0"
                    step="1"
                  />
                </div>
                <div class="col-6">
                  <input
                    v-model.number="priceMax"
                    type="number"
                    class="form-control form-control-sm"
                    placeholder="Max"
                    min="0"
                    step="1"
                  />
                </div>
              </div>
              <small v-if="priceMin || priceMax" class="text-muted">
                {{ priceMin || '0' }} - {{ priceMax || '∞' }}
              </small>
            </div>

            <!-- Status Filters -->
            <div class="mb-4">
              <label class="form-label fw-bold">
                <i class="bi bi-clock-history me-2"></i>Status
              </label>
              <div class="form-check">
                <input
                  v-model="showActive"
                  class="form-check-input"
                  type="checkbox"
                  id="showActive"
                />
                <label class="form-check-label" for="showActive">
                  Active Auctions
                </label>
              </div>
              <div class="form-check">
                <input
                  v-model="showEndingSoon"
                  class="form-check-input"
                  type="checkbox"
                  id="showEndingSoon"
                />
                <label class="form-check-label" for="showEndingSoon">
                  Ending Soon (&lt;24h)
                </label>
              </div>
              <div class="form-check">
                <input
                  v-model="showNoBids"
                  class="form-check-input"
                  type="checkbox"
                  id="showNoBids"
                />
                <label class="form-check-label" for="showNoBids">
                  No Bids Yet
                </label>
              </div>
            </div>

            <!-- Active Filters Summary -->
            <div v-if="hasActiveFilters" class="alert alert-info py-2 mb-0">
              <small>
                <i class="bi bi-info-circle me-1"></i>
                <strong>{{ activeFilterCount }}</strong> filter(s) active
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Items List -->
      <div class="col-lg-9 col-md-8">
        <!-- Header with Search and Results Count -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h2 class="mb-1">Auction Items</h2>
            <small class="text-muted">
              <i class="bi bi-grid-3x3-gap me-1"></i>
              {{ filteredItems.length }} item(s) found
            </small>
          </div>
          <router-link to="/items/create" class="btn btn-primary">
            <i class="bi bi-plus-circle me-2"></i>Create Listing
          </router-link>
        </div>

        <!-- Search Bar -->
        <div class="search-section mb-4">
          <div class="input-group input-group-lg">
            <span class="input-group-text bg-white">
              <i class="bi bi-search"></i>
            </span>
            <input
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              class="form-control"
              placeholder="Search items by title or description..."
            />
            <button
              v-if="searchQuery"
              class="btn btn-outline-secondary"
              type="button"
              @click="clearSearch"
            >
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="itemsStore.loading" class="row g-4">
          <div v-for="i in 6" :key="i" class="col-lg-4 col-md-6">
            <ItemCardSkeleton />
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="itemsStore.error" class="alert alert-danger">
          <i class="bi bi-exclamation-triangle me-2"></i>{{ itemsStore.error }}
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredItems.length === 0" class="text-center py-5">
          <i class="bi bi-inbox fs-1 text-muted d-block mb-3"></i>
          <h4 class="text-muted">No items match your filters</h4>
          <p class="text-muted">Try adjusting your search or filters.</p>
          <button class="btn btn-outline-primary" @click="clearFilters">
            Clear All Filters
          </button>
        </div>

        <!-- Items Grid -->
        <div v-else class="row g-4">
          <div
            v-for="item in filteredItems"
            :key="item.id"
            class="col-lg-4 col-md-6"
          >
            <ItemCard :item="item" @click="viewItem(item.id)" />
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
import ItemCard from '@/components/ItemCard.vue';
import ItemCardSkeleton from '@/components/ItemCardSkeleton.vue';

const itemsStore = useItemsStore();
const router = useRouter();

// Search state
const searchQuery = ref('');

// Filter state
const sortBy = ref('newest');
const priceMin = ref<number | null>(null);
const priceMax = ref<number | null>(null);
const showActive = ref(true);
const showEndingSoon = ref(false);
const showNoBids = ref(false);

// Filtered and sorted items
const filteredItems = computed(() => {
  let items = [...itemsStore.items];

  // Apply filters
  items = items.filter((item) => {
    // Price range filter
    const price = parseFloat(item.current_price);
    if (priceMin.value !== null && price < priceMin.value) return false;
    if (priceMax.value !== null && price > priceMax.value) return false;

    // Status filters
    if (!showActive.value && !item.is_ended) return false;

    // Ending soon filter
    if (showEndingSoon.value) {
      const hoursRemaining =
        (new Date(item.end_date).getTime() - Date.now()) / (1000 * 60 * 60);
      if (hoursRemaining >= 24 || hoursRemaining < 0) return false;
    }

    // No bids filter
    if (showNoBids.value && item.bid_count > 0) return false;

    return true;
  });

  // Apply sorting
  switch (sortBy.value) {
    case 'newest':
      items.sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
      break;
    case 'ending-soon':
      items.sort(
        (a, b) =>
          new Date(a.end_date).getTime() - new Date(b.end_date).getTime()
      );
      break;
    case 'price-low':
      items.sort(
        (a, b) => parseFloat(a.current_price) - parseFloat(b.current_price)
      );
      break;
    case 'price-high':
      items.sort(
        (a, b) => parseFloat(b.current_price) - parseFloat(a.current_price)
      );
      break;
    case 'most-bids':
      items.sort((a, b) => b.bid_count - a.bid_count);
      break;
  }

  return items;
});

// Check if any filters are active
const hasActiveFilters = computed(() => {
  return (
    priceMin.value !== null ||
    priceMax.value !== null ||
    !showActive.value ||
    showEndingSoon.value ||
    showNoBids.value ||
    sortBy.value !== 'newest'
  );
});

// Count active filters
const activeFilterCount = computed(() => {
  let count = 0;
  if (priceMin.value !== null || priceMax.value !== null) count++;
  if (!showActive.value) count++;
  if (showEndingSoon.value) count++;
  if (showNoBids.value) count++;
  if (sortBy.value !== 'newest') count++;
  return count;
});

// Clear all filters
const clearFilters = () => {
  priceMin.value = null;
  priceMax.value = null;
  showActive.value = true;
  showEndingSoon.value = false;
  showNoBids.value = false;
  sortBy.value = 'newest';
  searchQuery.value = '';
  itemsStore.fetchItems();
};

// Clear search only
const clearSearch = () => {
  searchQuery.value = '';
  itemsStore.fetchItems();
};

// Debounced search (Ajax, no page refresh)
let searchTimeout: ReturnType<typeof setTimeout> | undefined;
const handleSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    itemsStore.fetchItems(searchQuery.value);
  }, 300); // 300ms debounce
};

const viewItem = (itemId: number) => {
  router.push(`/items/${itemId}`);
};

onMounted(() => {
  itemsStore.fetchItems();
});
</script>

<style scoped>
.filter-card {
  top: 80px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}

.search-section .input-group {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  overflow: hidden;
}

.search-section .form-control {
  border: none;
}

.search-section .form-control:focus {
  box-shadow: none;
  border-color: transparent;
}

.search-section .input-group-text {
  border: none;
}

/* Custom scrollbar for filter sidebar */
.filter-card::-webkit-scrollbar {
  width: 6px;
}

.filter-card::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.filter-card::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.filter-card::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
