<template>
  <div class="container mt-4">
    <div class="welcome-section mb-4">
      <h1>Welcome to SoldIt</h1>
      <p class="text-muted">
        Hello, {{ userStore.user?.username }}! Start bidding on items or list your own.
      </p>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions mb-4">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Quick Actions</h5>
          <div class="d-flex flex-wrap gap-2">
            <router-link to="/items/create" class="btn btn-primary">
              <i class="bi bi-plus-circle me-1"></i>
              Create Listing
            </router-link>
            <router-link to="/items" class="btn btn-outline-primary">
              <i class="bi bi-search me-1"></i>
              Browse Auctions
            </router-link>
            <router-link to="/profile" class="btn btn-outline-secondary">
              <i class="bi bi-person me-1"></i>
              View Profile
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Analytics Cards -->
    <div class="row g-4 mb-4">
      <!-- My Listings Card -->
      <div class="col-lg-3 col-md-6">
        <div class="card stat-card border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h3 class="mb-0 fw-bold">{{ myItems.length }}</h3>
                <small class="text-muted">My Listings</small>
              </div>
              <div class="stat-icon bg-primary">
                <i class="bi bi-box-seam"></i>
              </div>
            </div>
            <div class="mt-3 pt-2 border-top">
              <small class="text-success">
                <i class="bi bi-arrow-up-circle me-1"></i>
                {{ activeListings }} active
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Total Bid Value Card -->
      <div class="col-lg-3 col-md-6">
        <div class="card stat-card border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h3 class="mb-0 fw-bold">{{ totalBidValue }}</h3>
                <small class="text-muted">Bid Value</small>
              </div>
              <div class="stat-icon bg-success">
                <i class="bi bi-cash-stack"></i>
              </div>
            </div>
            <div class="mt-3 pt-2 border-top">
              <small class="text-muted">
                <i class="bi bi-tag me-1"></i>
                {{ itemsImBiddingOn.length }} items
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Questions Card -->
      <div class="col-lg-3 col-md-6">
        <div class="card stat-card border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h3 class="mb-0 fw-bold">{{ itemsIAskedAbout.length }}</h3>
                <small class="text-muted">Questions</small>
              </div>
              <div class="stat-icon bg-info">
                <i class="bi bi-chat-dots"></i>
              </div>
            </div>
            <div class="mt-3 pt-2 border-top">
              <small class="text-muted">
                <i class="bi bi-check-circle me-1"></i>
                Engaging with sellers
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Win Rate Card -->
      <div class="col-lg-3 col-md-6">
        <div class="card stat-card border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <div>
                <h3 class="mb-0 fw-bold">{{ winRate }}%</h3>
                <small class="text-muted">Win Rate</small>
              </div>
              <div class="stat-icon bg-warning">
                <i class="bi bi-trophy"></i>
              </div>
            </div>
            <div class="mt-3 pt-2 border-top">
              <small class="text-muted">
                <i class="bi bi-award me-1"></i>
                {{ wonItemsCount }} won
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- My Activity Section -->
    <div class="activity-section">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3 class="mb-0">My Activity</h3>
        <router-link to="/items" class="btn btn-sm btn-outline-primary">
          Browse All Auctions
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="itemsStore.loading" class="text-center py-4">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- My Items Section -->
      <div v-else>
        <div v-if="myItems.length > 0" class="mb-4">
          <h5 class="text-muted mb-3">My Listings ({{ myItems.length }})</h5>
          <div class="row g-3">
            <div
              v-for="item in myItems"
              :key="item.id"
              class="col-md-4"
            >
              <ItemCard :item="item" @click="viewItem(item.id)" />
            </div>
          </div>
        </div>

        <!-- Items I'm Bidding On -->
        <div v-if="itemsImBiddingOn.length > 0" class="mb-4">
          <h5 class="text-muted mb-3">Items I'm Bidding On ({{ itemsImBiddingOn.length }})</h5>
          <div class="row g-3">
            <div
              v-for="item in itemsImBiddingOn"
              :key="item.id"
              class="col-md-4"
            >
              <ItemCard :item="item" @click="viewItem(item.id)" />
            </div>
          </div>
        </div>

        <!-- Items I've Asked About -->
        <div v-if="itemsIAskedAbout.length > 0" class="mb-4">
          <h5 class="text-muted mb-3">Items I've Asked About ({{ itemsIAskedAbout.length }})</h5>
          <div class="row g-3">
            <div
              v-for="item in itemsIAskedAbout"
              :key="item.id"
              class="col-md-4"
            >
              <ItemCard :item="item" @click="viewItem(item.id)" />
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="myItems.length === 0 && itemsImBiddingOn.length === 0 && itemsIAskedAbout.length === 0" class="card">
          <div class="card-body text-center py-5">
            <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
            <h5 class="mt-3">No Activity Yet</h5>
            <p class="text-muted mb-3">
              You haven't created any listings, placed any bids, or asked any questions yet.
            </p>
            <router-link to="/items" class="btn btn-primary">
              Browse Auctions
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/user';
import { useItemsStore } from '@/store/items';
import ItemCard from '@/components/ItemCard.vue';
import type { Item } from '@/types/models';
import { formatPrice } from '@/utils/currency';

const userStore = useUserStore();
const itemsStore = useItemsStore();
const router = useRouter();

// Computed properties for personalized content
const myItems = computed(() => {
  return itemsStore.items.filter(
    (item: Item) => item.owner_id === userStore.user?.id
  );
});

const itemsImBiddingOn = computed(() => {
  const bidIds = userStore.user?.bid_item_ids || [];
  return itemsStore.items.filter(
    (item: Item) => bidIds.includes(item.id)
  );
});

const itemsIAskedAbout = computed(() => {
  const questionedIds = userStore.user?.questioned_item_ids || [];
  return itemsStore.items.filter(
    (item: Item) => questionedIds.includes(item.id)
  );
});

// Enhanced analytics computed properties
const activeListings = computed(() => {
  return myItems.value.filter((item: Item) => !item.is_ended).length;
});

const totalBidValue = computed(() => {
  const total = itemsImBiddingOn.value
    .reduce((sum: number, item: Item) => sum + parseFloat(item.current_price), 0);
  return formatPrice(total, userStore.user?.currency_preference || 'USD');
});

const wonItemsCount = computed(() => {
  return itemsStore.items.filter(
    (item: Item) => item.winner_id === userStore.user?.id
  ).length;
});

const winRate = computed(() => {
  const participated = itemsImBiddingOn.value.filter((i: Item) => i.is_ended).length;
  if (participated === 0) return 0;
  return Math.round((wonItemsCount.value / participated) * 100);
});

const viewItem = (itemId: number) => {
  router.push(`/items/${itemId}`);
};

onMounted(() => {
  itemsStore.fetchItems();
});
</script>

<style scoped>
.welcome-section h1 {
  color: #333;
  font-weight: 600;
}

/* Enhanced Stat Cards */
.stat-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.stat-card:hover .stat-icon {
  transform: rotate(10deg) scale(1.1);
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.display-4 {
  font-weight: 700;
}
</style>
