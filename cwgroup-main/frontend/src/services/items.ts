import { apiClient } from './api';
import type { ApiResponse } from '@/types/api';
import type {
  Item,
  Bid,
  Question,
  ItemCreateData,
  ItemUpdateData,
  BidData,
  QuestionData,
  AnswerData
} from '@/types/models';

export interface ItemsResponse {
  items: Item[];
}

export interface ItemDetailResponse {
  item: Item;
  bids: Bid[];
  questions: Question[];
}

export const itemsService = {
  /**
   * Get all items with optional search
   */
  async getItems(search?: string): Promise<ApiResponse<ItemsResponse>> {
    const url = search
      ? `/api/items/?search=${encodeURIComponent(search)}`
      : '/api/items/';
    return apiClient.get<ItemsResponse>(url);
  },

  /**
   * Get single item with bids and questions
   */
  async getItemDetail(itemId: number): Promise<ApiResponse<ItemDetailResponse>> {
    return apiClient.get<ItemDetailResponse>(`/api/items/${itemId}/`);
  },

  /**
   * Create new auction item
   */
  async createItem(data: ItemCreateData): Promise<ApiResponse<{ item: Item }>> {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('description', data.description);
    formData.append('starting_price', data.starting_price);
    formData.append('picture', data.picture);
    formData.append('end_date', data.end_date);

    return apiClient.postFormData<{ item: Item }>('/api/items/', formData);
  },

  /**
   * Place bid on an item
   */
  async placeBid(
    itemId: number,
    data: BidData
  ): Promise<ApiResponse<{ item: Item; bid: Bid }>> {
    return apiClient.post<{ item: Item; bid: Bid }>(
      `/api/items/${itemId}/bid/`,
      data
    );
  },

  /**
   * Ask question about an item
   */
  async askQuestion(
    itemId: number,
    data: QuestionData
  ): Promise<ApiResponse<{ question: Question }>> {
    return apiClient.post<{ question: Question }>(
      `/api/items/${itemId}/questions/`,
      data
    );
  },

  /**
   * Answer a question (item owner only)
   */
  async answerQuestion(
    questionId: number,
    data: AnswerData
  ): Promise<ApiResponse<{ question: Question }>> {
    return apiClient.post<{ question: Question }>(
      `/api/questions/${questionId}/answer/`,
      data
    );
  },

  /**
   * Update an item (owner only)
   */
  async updateItem(
    itemId: number,
    data: ItemUpdateData
  ): Promise<ApiResponse<{ item: Item }>> {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('description', data.description);
    formData.append('end_date', data.end_date);
    if (data.picture) {
      formData.append('picture', data.picture);
    }

    return apiClient.putFormData<{ item: Item }>(
      `/api/items/${itemId}/edit/`,
      formData
    );
  },

  /**
   * Delete an item (owner only, soft delete)
   */
  async deleteItem(itemId: number): Promise<ApiResponse<{}>> {
    return apiClient.delete<{}>(`/api/items/${itemId}/delete/`);
  },
};
