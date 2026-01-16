<template>
  <div class="container mt-4">
    <!-- Loading State -->
    <div v-if="itemsStore.loading && !itemsStore.currentItem" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="itemsStore.error" class="alert alert-danger">
      {{ itemsStore.error }}
    </div>

    <!-- Item Detail -->
    <div v-else-if="itemsStore.currentItem">
      <div class="row">
        <!-- Left Column: Image & Details -->
        <div class="col-md-6">
          <img
            :src="itemsStore.currentItem.picture || '/placeholder.jpg'"
            :alt="itemsStore.currentItem.title"
            class="img-fluid rounded mb-3"
          />

          <div class="card mb-3">
            <div class="card-body">
              <h2>{{ itemsStore.currentItem.title }}</h2>
              <p class="text-muted">{{ itemsStore.currentItem.description }}</p>

              <hr />

              <div class="row">
                <div class="col-6">
                  <small class="text-muted">Starting Price</small>
                  <div class="fw-bold">{{ formatPrice(itemsStore.currentItem.starting_price, userStore.user?.currency_preference || 'USD') }}</div>
                </div>
                <div class="col-6">
                  <small class="text-muted">Current Price</small>
                  <div class="fw-bold text-success fs-4">
                    {{ formatPrice(itemsStore.currentItem.current_price, userStore.user?.currency_preference || 'USD') }}
                  </div>
                </div>
              </div>

              <hr />

              <div>
                <small class="text-muted">Seller</small>
                <div>{{ itemsStore.currentItem.owner_username }}</div>
              </div>

              <div class="mt-2">
                <small class="text-muted">Ends</small>
                <div>{{ formatDate(itemsStore.currentItem.end_date) }}</div>
              </div>

              <div class="mt-2">
                <small class="text-muted">Total Bids</small>
                <div>{{ itemsStore.currentItem.bid_count }}</div>
              </div>

              <div v-if="itemsStore.currentItem.is_ended" class="alert alert-warning mt-3">
                This auction has ended.
                <div v-if="itemsStore.currentItem.winner_username">
                  Winner: {{ itemsStore.currentItem.winner_username }}
                </div>
              </div>

              <!-- Owner Actions -->
              <div v-if="isOwner" class="mt-3 d-flex gap-2">
                <router-link
                  :to="`/items/${itemsStore.currentItem.id}/edit`"
                  class="btn btn-outline-primary"
                >
                  Edit Listing
                </router-link>
                <button
                  class="btn btn-outline-danger"
                  @click="showDeleteModal = true"
                >
                  Delete Listing
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Bidding & Q&A -->
        <div class="col-md-6">
          <!-- Bid Form -->
          <div v-if="!itemsStore.currentItem.is_ended && !isOwner" class="card mb-3">
            <div class="card-body">
              <h4>Place Bid</h4>
              <form @submit.prevent="handlePlaceBid">
                <div class="input-group">
                  <span class="input-group-text">{{ currencySymbol }}</span>
                  <input
                    v-model="bidAmount"
                    type="number"
                    :step="userCurrency === 'JPY' ? '1' : '0.01'"
                    :min="minBidAmount"
                    class="form-control"
                    placeholder="Enter bid amount"
                    required
                  />
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="itemsStore.loading"
                  >
                    Place Bid
                  </button>
                </div>
                <small class="text-muted">
                  Minimum bid: {{ currencySymbol }}{{ minBidAmount }}
                </small>
              </form>
            </div>
          </div>

          <!-- Bid History -->
          <div class="card mb-3">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="mb-0">Bid History</h4>
                <!-- View Toggle Buttons -->
                <div v-if="itemsStore.currentItemBids.length > 0" class="btn-group btn-group-sm" role="group">
                  <button
                    type="button"
                    class="btn btn-outline-primary"
                    :class="{ active: viewMode === 'chart' }"
                    @click="viewMode = 'chart'"
                  >
                    <i class="bi bi-graph-up me-1"></i>Chart
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-primary"
                    :class="{ active: viewMode === 'list' }"
                    @click="viewMode = 'list'"
                  >
                    <i class="bi bi-list-ul me-1"></i>List
                  </button>
                </div>
              </div>

              <!-- No Bids State -->
              <div v-if="itemsStore.currentItemBids.length === 0" class="text-muted text-center py-4">
                <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                No bids yet. Be the first!
              </div>

              <!-- Chart View -->
              <div v-else-if="viewMode === 'chart'">
                <BidChart
                  :bids="itemsStore.currentItemBids"
                  :starting-price="itemsStore.currentItem.starting_price"
                />
              </div>

              <!-- List View -->
              <div v-else class="list-group">
                <div
                  v-for="bid in itemsStore.currentItemBids"
                  :key="bid.id"
                  class="list-group-item"
                >
                  <div class="d-flex justify-content-between">
                    <span class="fw-bold">{{ bid.bidder_username }}</span>
                    <span class="text-success">{{ formatPrice(bid.amount, userStore.user?.currency_preference || 'USD') }}</span>
                  </div>
                  <small class="text-muted">{{ formatDate(bid.created_at) }}</small>
                </div>
              </div>
            </div>
          </div>

          <!-- Q&A Section -->
          <div class="card">
            <div class="card-body">
              <h4>Questions & Answers</h4>

              <!-- Ask Question Form (non-owners only) -->
              <div v-if="!isOwner" class="mb-3">
                <form @submit.prevent="handleAskQuestion">
                  <div class="mb-2">
                    <textarea
                      v-model="questionText"
                      class="form-control"
                      rows="2"
                      placeholder="Ask a question about this item..."
                      required
                    ></textarea>
                  </div>
                  <button
                    type="submit"
                    class="btn btn-sm btn-secondary"
                    :disabled="itemsStore.loading"
                  >
                    Ask Question
                  </button>
                </form>
              </div>

              <!-- Questions List -->
              <div v-if="itemsStore.currentItemQuestions.length === 0" class="text-muted">
                No questions yet.
              </div>
              <div v-else>
                <div
                  v-for="question in itemsStore.currentItemQuestions"
                  :key="question.id"
                  class="border-bottom pb-3 mb-3"
                >
                  <div class="mb-2">
                    <strong>Q:</strong> {{ question.question_text }}
                    <br />
                    <small class="text-muted">
                      by {{ question.asker_username }} - {{ formatDate(question.asked_at) }}
                    </small>
                  </div>

                  <!-- Answer -->
                  <div v-if="question.is_answered" class="ms-3">
                    <strong>A:</strong> {{ question.answer_text }}
                    <br />
                    <small class="text-muted">
                      {{ formatDate(question.answered_at!) }}
                    </small>
                  </div>

                  <!-- Answer Form (owner only) -->
                  <div v-else-if="isOwner" class="ms-3">
                    <form @submit.prevent="handleAnswerQuestion(question.id)">
                      <div class="mb-2">
                        <textarea
                          v-model="answerTexts[question.id]"
                          class="form-control form-control-sm"
                          rows="2"
                          placeholder="Type your answer..."
                          required
                        ></textarea>
                      </div>
                      <button
                        type="submit"
                        class="btn btn-sm btn-primary"
                        :disabled="itemsStore.loading"
                      >
                        Answer
                      </button>
                    </form>
                  </div>

                  <div v-else class="ms-3 text-muted">
                    <em>Not answered yet</em>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Back Button -->
      <div class="mt-4">
        <router-link to="/items" class="btn btn-secondary">
          Back to Items
        </router-link>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background-color: rgba(0,0,0,0.5);"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button
              type="button"
              class="btn-close"
              @click="showDeleteModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this listing?</p>
            <p class="text-muted">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showDeleteModal = false"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              :disabled="itemsStore.loading"
              @click="handleDelete"
            >
              {{ itemsStore.loading ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useItemsStore } from '@/store/items';
import { useUserStore } from '@/store/user';
import { useToast } from 'vue-toastification';
import BidChart from '@/components/BidChart.vue';
import { formatPrice, convertFromUSD, convertToUSD, getCurrencySymbol } from '@/utils/currency';

const route = useRoute();
const router = useRouter();
const itemsStore = useItemsStore();
const userStore = useUserStore();
const toast = useToast();

const bidAmount = ref('');
const questionText = ref('');
const answerTexts = ref<Record<number, string>>({});
const viewMode = ref<'chart' | 'list'>('chart');
const showDeleteModal = ref(false);

const itemId = computed(() => parseInt(route.params.id as string));

const isOwner = computed(() => {
  return itemsStore.currentItem?.owner_id === userStore.user?.id;
});

const userCurrency = computed(() => userStore.user?.currency_preference || 'USD');
const currencySymbol = computed(() => getCurrencySymbol(userCurrency.value));

// Min bid in USD (for validation)
const minBidAmountUSD = computed(() => {
  if (!itemsStore.currentItem) return 0;
  return parseFloat(itemsStore.currentItem.current_price) + 0.01;
});

// Min bid converted to user's display currency
const minBidAmount = computed(() => {
  const converted = convertFromUSD(minBidAmountUSD.value, userCurrency.value);
  if (userCurrency.value === 'JPY') {
    return Math.ceil(converted).toString();
  }
  return converted.toFixed(2);
});

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
};

const handlePlaceBid = async () => {
  // Convert bid from user's currency to USD
  const bidInUserCurrency = parseFloat(bidAmount.value);
  const bidInUSD = convertToUSD(bidInUserCurrency, userCurrency.value);

  const success = await itemsStore.placeBid(itemId.value, bidInUSD.toFixed(2));
  if (success) {
    bidAmount.value = '';
    toast.success('Bid placed successfully!');
  } else {
    toast.error(itemsStore.error || 'Failed to place bid');
  }
};

const handleAskQuestion = async () => {
  const success = await itemsStore.askQuestion(itemId.value, questionText.value);
  if (success) {
    questionText.value = '';
    toast.success('Question asked successfully!');
  } else {
    toast.error(itemsStore.error || 'Failed to ask question');
  }
};

const handleAnswerQuestion = async (questionId: number) => {
  const answerText = answerTexts.value[questionId];
  if (!answerText) return;

  const success = await itemsStore.answerQuestion(questionId, answerText);
  if (success) {
    delete answerTexts.value[questionId];
    toast.success('Answer submitted successfully!');
  } else {
    toast.error(itemsStore.error || 'Failed to submit answer');
  }
};

const handleDelete = async () => {
  const success = await itemsStore.deleteItem(itemId.value);
  if (success) {
    toast.success('Item deleted successfully!');
    router.push('/items');
  } else {
    toast.error(itemsStore.error || 'Failed to delete item');
  }
  showDeleteModal.value = false;
};

onMounted(() => {
  itemsStore.fetchItemDetail(itemId.value);
});

onUnmounted(() => {
  itemsStore.clearCurrentItem();
});
</script>
