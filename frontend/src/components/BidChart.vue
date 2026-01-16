<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted, computed } from 'vue';
import { Chart, registerables } from 'chart.js';
import type { Bid } from '@/types/models';
import { useUserStore } from '@/store/user';
import { convertFromUSD, getCurrencySymbol } from '@/utils/currency';

Chart.register(...registerables);

const userStore = useUserStore();
const currency = computed(() => userStore.user?.currency_preference || 'USD');

const props = defineProps<{
  bids: Bid[];
  startingPrice: string;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const createChart = () => {
  if (!chartCanvas.value || props.bids.length === 0) return;

  const currencyCode = currency.value;
  const symbol = getCurrencySymbol(currencyCode);

  // Prepare data - sort bids by time (oldest first)
  const sortedBids = [...props.bids].reverse();
  const labels = sortedBids.map((bid) =>
    new Date(bid.created_at).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    })
  );
  // Convert bid amounts to display currency
  const data = sortedBids.map((bid) => convertFromUSD(parseFloat(bid.amount), currencyCode));

  // Add starting price as first point (converted)
  labels.unshift('Start');
  data.unshift(convertFromUSD(parseFloat(props.startingPrice), currencyCode));

  const ctx = chartCanvas.value.getContext('2d');
  if (!ctx) return;

  // Destroy existing chart if any
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: `Bid Amount (${symbol})`,
          data,
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.1)',
          tension: 0.3,
          fill: true,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointBackgroundColor: 'rgb(75, 192, 192)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const value = context.parsed.y;
              if (currencyCode === 'JPY') {
                return `${symbol}${Math.round(value || 0).toLocaleString()}`;
              }
              return `${symbol}${(value || 0).toFixed(2)}`;
            },
          },
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12,
          titleFont: {
            size: 14,
          },
          bodyFont: {
            size: 13,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: (value) => `${symbol}${value}`,
            font: {
              size: 12,
            },
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
          },
        },
        x: {
          ticks: {
            font: {
              size: 11,
            },
          },
          grid: {
            display: false,
          },
        },
      },
    },
  });
};

onMounted(createChart);
watch(() => props.bids, createChart, { deep: true });
watch(currency, createChart);

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.chart-container {
  height: 250px;
  margin-top: 15px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
}
</style>
