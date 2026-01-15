<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        Auction App
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
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/user';

const router = useRouter();
const userStore = useUserStore();

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
</style>
