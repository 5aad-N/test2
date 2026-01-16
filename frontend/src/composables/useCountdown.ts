import { ref, onMounted, onUnmounted } from 'vue';

export function useCountdown(endDate: string) {
  const timeRemaining = ref('');
  const urgency = ref<'normal' | 'warning' | 'critical'>('normal');
  let interval: number;

  const calculateTime = () => {
    const end = new Date(endDate).getTime();
    const now = new Date().getTime();
    const diff = end - now;

    if (diff <= 0) {
      timeRemaining.value = 'Ended';
      urgency.value = 'critical';
      clearInterval(interval);
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    // Urgency levels
    if (diff < 3600000) {
      // < 1 hour
      urgency.value = 'critical';
      timeRemaining.value = `${minutes}m remaining`;
    } else if (diff < 86400000) {
      // < 1 day
      urgency.value = 'warning';
      timeRemaining.value = `${hours}h ${minutes}m`;
    } else {
      urgency.value = 'normal';
      timeRemaining.value = `${days}d ${hours}h`;
    }
  };

  onMounted(() => {
    calculateTime();
    interval = setInterval(calculateTime, 1000) as any;
  });

  onUnmounted(() => {
    clearInterval(interval);
  });

  return { timeRemaining, urgency };
}
