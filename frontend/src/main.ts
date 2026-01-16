import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useUserStore } from '@/store/user'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import './assets/theme.css';

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

// Setup toast notifications
app.use(Toast, {
    transition: 'Vue-Toastification__bounce',
    maxToasts: 3,
    newestOnTop: true,
    position: 'top-right',
    timeout: 3000,
})

const initApp = async () => {
    const userStore = useUserStore()
    
    if (!userStore.isAuthenticated) {
        await userStore.fetchCurrentUser()
    }
    
    app.use(router)
    app.mount('#app')
}

initApp()