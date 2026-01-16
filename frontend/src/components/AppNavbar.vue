<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        <img 
          src="@/assets/logo.png" 
          alt="Soldit Logo" 
          class="navbar-logo"
        >
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-lg-center">
          <li class="nav-item">
            <router-link to="/" class="nav-link" active-class="active">
              Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/items" class="nav-link" active-class="active">
              Auctions
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/profile" class="nav-link" active-class="active">
              Profile
            </router-link>
          </li>
          <!-- Currency Selector -->
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi bi-currency-exchange me-1"></i>
              {{ currentCurrencySymbol }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li
                v-for="currency in currencyOptions"
                :key="currency.code"
              >
                <a
                  class="dropdown-item"
                  :class="{ active: userStore.user?.currency_preference === currency.code }"
                  href="#"
                  @click.prevent="changeCurrency(currency.code)"
                >
                  {{ currency.symbol }} {{ currency.name }}
                </a>
              </li>
            </ul>
          </li>
          <li class="nav-item">
            <span class="nav-link text-light">
              <i class="bi bi-person-circle"></i>
              {{ userStore.user?.username }}
            </span>
          </li>
          <li class="nav-item">
            <button @click="handleLogout" class="btn btn-outline-light btn-sm ms-lg-2">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/user';
import { getCurrencyOptions, getCurrencySymbol } from '@/utils/currency';
import type { CurrencyCode } from '@/types/models';

const router = useRouter();
const userStore = useUserStore();
const currencyOptions = getCurrencyOptions();

const currentCurrencySymbol = computed(() => {
  const code = userStore.user?.currency_preference || 'USD';
  return getCurrencySymbol(code);
});

const changeCurrency = async (code: CurrencyCode) => {
  await userStore.setCurrency(code);
};

const handleLogout = async () => {
  await userStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
  font-size: 1.25rem;
}

.nav-link {
  cursor: pointer;
}

.nav-link.active {
  font-weight: 600;
}

.navbar-logo {
  height: 150px;       
  width: auto;        
  object-fit: contain;
  margin-top: -40px;
  margin-bottom: -40px;
}

.navbar-brand {
  display: flex;
}

</style>
