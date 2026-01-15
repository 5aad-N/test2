<template>
  <div class="card h-100 shadow-sm" @click="$emit('click')">
    <div class="position-relative">
      <img :src="item.picture || ''" class="card-img-top item-image" alt="Item image" />

      <!-- Countdown Badge -->
      <div class="position-absolute top-0 end-0 m-2">
        <div
          v-if="!item.is_ended && item.is_active"
          class="countdown-badge"
          :class="`countdown-${urgency}`"
        >
          <i class="bi bi-clock me-1"></i>{{ timeRemaining }}
        </div>
        <span v-else class="badge bg-danger shadow-sm">
          <i class="bi bi-lock-fill me-1"></i> Closed
        </span>
      </div>
    </div>

    <div class="card-body d-flex flex-column">
      <h5 class="card-title text-truncate">{{ item.title }}</h5>
      <p class="card-text text-muted small flex-grow-1 text-truncate-2">
        {{ item.description }}
      </p>
      
      <div class="mt-2">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <div>
            <small class="text-muted d-block">Current Bid</small>
            <span class="fw-bold text-primary">${{ item.current_price }}</span>
          </div>
          <div class="text-end">
            <small class="text-muted d-block">Bids</small>
            <span class="badge rounded-pill bg-light text-dark border">
              {{ item.bid_count }}
            </span>
          </div>
        </div>

        <div class="pt-2 border-top">
          <small class="text-muted d-block">
            <i class="bi bi-calendar3 me-1"></i>
            {{ item.is_ended ? 'Ended on:' : 'Ends on:' }}
          </small>
          <span :class="['small', item.is_ended ? 'text-muted' : 'text-danger fw-medium']">
            {{ formatDate(item.end_date) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Item } from '@/types/models';
import { useCountdown } from '@/composables/useCountdown';

const props = defineProps<{
  item: Item;
}>();

defineEmits<{
  (e: 'click'): void;
}>();

// Use countdown timer for active items
const { timeRemaining, urgency } = useCountdown(props.item.end_date);

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString();
};
</script>

<style scoped>
.item-image {
  height: 200px;
  object-fit: cover;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.card:hover .item-image {
  transform: scale(1.05);
}

.item-image {
  transition: transform 0.3s ease;
}

.badge {
  font-weight: 500;
  padding: 0.5em 0.8em;
}

.italic {
  font-style: italic;
}

/* Countdown Badge Styles */
.countdown-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.countdown-normal {
  background: rgba(25, 135, 84, 0.9);
  color: white;
}

.countdown-warning {
  background: rgba(255, 193, 7, 0.9);
  color: #000;
  animation: pulse 2s infinite;
}

.countdown-critical {
  background: rgba(220, 53, 69, 0.9);
  color: white;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>