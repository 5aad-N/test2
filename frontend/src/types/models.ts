/**
 * Type definitions for data models matching backend structure
 */

export type CurrencyCode = 'USD' | 'EUR' | 'GBP' | 'JPY' | 'AUD';

export interface User {
  id: number;
  username: string;
  email: string;
  date_of_birth: string | null;
  profile_image: string | null;
  currency_preference: CurrencyCode;
  bid_item_ids: number[];
  questioned_item_ids: number[];
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface SignupData {
  username: string;
  email: string;
  password1: string;
  password2: string;
  date_of_birth?: string;
  profile_image?: File;
}

export interface ProfileUpdateData {
  email: string;
  date_of_birth?: string;
  profile_image?: File;
  currency_preference?: CurrencyCode;
}

export interface Item {
  id: number;
  owner_id: number;
  owner_username: string;
  title: string;
  description: string;
  starting_price: string;
  current_price: string;
  picture: string | null;
  end_date: string;
  created_at: string;
  is_active: boolean;
  is_ended: boolean;
  bid_count: number;
  winner_id: number | null;
  winner_username: string | null;
}

export interface Bid {
  id: number;
  item_id: number;
  item_title: string;
  bidder_id: number;
  bidder_username: string;
  amount: string;
  created_at: string;
}

export interface Question {
  id: number;
  item_id: number;
  item_title: string;
  asker_id: number;
  asker_username: string;
  question_text: string;
  answer_text: string;
  asked_at: string;
  answered_at: string | null;
  is_answered: boolean;
}

export interface ItemCreateData {
  title: string;
  description: string;
  starting_price: string;
  picture: File;
  end_date: string;
}

export interface ItemUpdateData {
  title: string;
  description: string;
  end_date: string;
  picture?: File;
}

export interface BidData {
  amount: string;
}

export interface QuestionData {
  question_text: string;
}

export interface AnswerData {
  answer_text: string;
}
