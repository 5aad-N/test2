import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

// Route components
import DashboardPage from '@/pages/DashboardPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import SignupPage from '@/pages/SignupPage.vue'
import ProfilePage from '@/pages/ProfilePage.vue'
import ItemsListPage from '@/pages/ItemsListPage.vue'
import CreateItemPage from '@/pages/CreateItemPage.vue'
import EditItemPage from '@/pages/EditItemPage.vue'
import ItemDetailPage from '@/pages/ItemDetailPage.vue'

const base = (import.meta.env.MODE === 'development') ? import.meta.env.BASE_URL : ''

const router = createRouter({
    history: createWebHistory(base),
    routes: [
        {
            path: '/',
            name: 'Dashboard',
            component: DashboardPage,
            meta: { requiresAuth: true },
        },
        {
            path: '/login',
            name: 'Login',
            component: LoginPage,
            meta: { guestOnly: true },
        },
        {
            path: '/signup',
            name: 'Signup',
            component: SignupPage,
            meta: { guestOnly: true },
        },
        {
            path: '/profile',
            name: 'Profile',
            component: ProfilePage,
            meta: { requiresAuth: true },
        },
        {
            path: '/items',
            name: 'ItemsList',
            component: ItemsListPage,
            meta: { requiresAuth: true },
        },
        {
            path: '/items/create',
            name: 'CreateItem',
            component: CreateItemPage,
            meta: { requiresAuth: true },
        },
        {
            path: '/items/:id/edit',
            name: 'EditItem',
            component: EditItemPage,
            meta: { requiresAuth: true },
        },
        {
            path: '/items/:id',
            name: 'ItemDetail',
            component: ItemDetailPage,
            meta: { requiresAuth: true },
        },
    ]
})

// Navigation guards
router.beforeEach((to, _from, next) => {
    const userStore = useUserStore()

    if (to.meta.requiresAuth && !userStore.isAuthenticated) {
        // Redirect to login if authentication required but not authenticated
        next('/login')
    } else if (to.meta.guestOnly && userStore.isAuthenticated) {
        // Redirect to home if guest-only route but already authenticated
        next('/')
    } else {
        next()
    }
})

export default router
