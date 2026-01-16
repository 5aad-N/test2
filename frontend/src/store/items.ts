import { defineStore } from 'pinia';
import { itemsService } from '@/services/items';
import type {
  Item,
  Bid,
  Question,
  ItemCreateData,
  ItemUpdateData,
} from '@/types/models';
import { useUserStore } from './user';

interface ItemsState {
  items: Item[];
  currentItem: Item | null;
  currentItemBids: Bid[];
  currentItemQuestions: Question[];
  loading: boolean;
  error: string | null;
}

export const useItemsStore = defineStore('items', {
  state: (): ItemsState => ({
    items: [],
    currentItem: null,
    currentItemBids: [],
    currentItemQuestions: [],
    loading: false,
    error: null,
  }),

  getters: {
    activeItems: (state) => state.items.filter((item: Item) => !item.is_ended),
    endedItems: (state) => state.items.filter((item: Item) => item.is_ended),
  },

  actions: {
    async fetchItems(search?: string): Promise<void> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.getItems(search);
        if (response.success && response.data) {
          this.items = response.data.items;
        } else {
          this.error = response.error || 'Failed to load items';
        }
      } catch {
        this.error = 'Network error';
      } finally {
        this.loading = false;
      }
    },

    async fetchItemDetail(itemId: number): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.getItemDetail(itemId);
        if (response.success && response.data) {
          this.currentItem = response.data.item;
          this.currentItemBids = response.data.bids;
          this.currentItemQuestions = response.data.questions;
          return true;
        } else {
          this.error = response.error || 'Failed to load item';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async createItem(data: ItemCreateData): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.createItem(data);
        if (response.success && response.data) {
          // Add to items list
          this.items.unshift(response.data.item);
          return true;
        } else {
          this.error = response.error || 'Failed to create item';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async placeBid(itemId: number, amount: string): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.placeBid(itemId, { amount });
        if (response.success && response.data) {
          // Update current item and add bid to list
          this.currentItem = response.data.item;
          this.currentItemBids.unshift(response.data.bid);

          // Update in items list too
          const index = this.items.findIndex((i: Item) => i.id === itemId);
          if (index !== -1) {
            this.items[index] = response.data.item;
          }

          const userStore = useUserStore();

          if (userStore.user && !userStore.user.bid_item_ids.includes(itemId)) {
              userStore.user.bid_item_ids.push(itemId);
          }

          return true;
        } else {
          this.error = response.error || 'Failed to place bid';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async askQuestion(itemId: number, questionText: string): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.askQuestion(itemId, { question_text: questionText });
        if (response.success && response.data) {
          // Add question to list
          this.currentItemQuestions.push(response.data.question);

          const userStore = useUserStore();

          if (userStore.user && !userStore.user.questioned_item_ids.includes(itemId)) {
              userStore.user.questioned_item_ids.push(itemId);
          }

          return true;
        } else {
          this.error = response.error || 'Failed to ask question';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async answerQuestion(questionId: number, answerText: string): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.answerQuestion(questionId, { answer_text: answerText });
        if (response.success && response.data) {
          // Update question in list
          const index = this.currentItemQuestions.findIndex((q: Question) => q.id === questionId);
          if (index !== -1) {
            this.currentItemQuestions[index] = response.data.question;
          }
          return true;
        } else {
          this.error = response.error || 'Failed to answer question';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async updateItem(itemId: number, data: ItemUpdateData): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.updateItem(itemId, data);
        if (response.success && response.data) {
          // Update current item
          this.currentItem = response.data.item;

          // Update in items list too
          const index = this.items.findIndex((i: Item) => i.id === itemId);
          if (index !== -1) {
            this.items[index] = response.data.item;
          }

          return true;
        } else {
          this.error = response.error || 'Failed to update item';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async deleteItem(itemId: number): Promise<boolean> {
      this.loading = true;
      this.error = null;

      try {
        const response = await itemsService.deleteItem(itemId);
        if (response.success) {
          // Remove from items list
          this.items = this.items.filter((i: Item) => i.id !== itemId);

          // Clear current item if it's the deleted one
          if (this.currentItem?.id === itemId) {
            this.clearCurrentItem();
          }

          return true;
        } else {
          this.error = response.error || 'Failed to delete item';
          return false;
        }
      } catch {
        this.error = 'Network error';
        return false;
      } finally {
        this.loading = false;
      }
    },

    clearCurrentItem(): void {
      this.currentItem = null;
      this.currentItemBids = [];
      this.currentItemQuestions = [];
    },
  },
});
