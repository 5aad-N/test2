import type { CurrencyCode } from '@/types/models';

export interface CurrencyInfo {
  code: CurrencyCode;
  name: string;
  symbol: string;
}

export const CURRENCIES: Record<CurrencyCode, CurrencyInfo> = {
  USD: { code: 'USD', name: 'US Dollar', symbol: '$' },
  EUR: { code: 'EUR', name: 'Euro', symbol: '€' },
  GBP: { code: 'GBP', name: 'British Pound', symbol: '£' },
  JPY: { code: 'JPY', name: 'Japanese Yen', symbol: '¥' },
  AUD: { code: 'AUD', name: 'Australian Dollar', symbol: 'A$' },
};

// Exchange rates relative to USD (base currency)
export const EXCHANGE_RATES: Record<CurrencyCode, number> = {
  USD: 1.0,
  EUR: 0.92,
  GBP: 0.79,
  JPY: 149.5,
  AUD: 1.53,
};

/**
 * Convert an amount from USD to the target currency
 */
export function convertFromUSD(amountUSD: number, targetCurrency: CurrencyCode): number {
  const rate = EXCHANGE_RATES[targetCurrency];
  return amountUSD * rate;
}

/**
 * Convert an amount from a currency back to USD
 */
export function convertToUSD(amount: number, fromCurrency: CurrencyCode): number {
  const rate = EXCHANGE_RATES[fromCurrency];
  return amount / rate;
}

/**
 * Format a price in the specified currency
 * @param amount - The amount in USD (base currency)
 * @param currency - The target currency to display
 * @returns Formatted price string with currency symbol
 */
export function formatPrice(amount: string | number, currency: CurrencyCode): string {
  const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;

  if (isNaN(numAmount)) {
    return `${CURRENCIES[currency].symbol}0.00`;
  }

  const convertedAmount = convertFromUSD(numAmount, currency);
  const symbol = CURRENCIES[currency].symbol;

  // JPY doesn't use decimal places
  if (currency === 'JPY') {
    return `${symbol}${Math.round(convertedAmount).toLocaleString()}`;
  }

  return `${symbol}${convertedAmount.toFixed(2)}`;
}

/**
 * Get the currency symbol for a currency code
 */
export function getCurrencySymbol(currency: CurrencyCode): string {
  return CURRENCIES[currency].symbol;
}

/**
 * Get list of all available currencies for dropdown
 */
export function getCurrencyOptions(): CurrencyInfo[] {
  return Object.values(CURRENCIES);
}
