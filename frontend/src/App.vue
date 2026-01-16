<template>
  <div>
    <AppNavbar v-if="userStore.isAuthenticated" />

    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import AppNavbar from '@/components/AppNavbar.vue'

const userStore = useUserStore()

// Fetch user on app mount if not already set
onMounted(() => {
  if (!userStore.user) {
    userStore.fetchCurrentUser()
  }
})
</script>

<style>
/* Global styles */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f8f9fa;
}

#app {
  min-height: 100vh;
}
</style>