import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { routes } from 'vue-router/auto-routes'

// import SearchView from '@/views/SearchView.vue'
// import TrackView from '@/views/TrackView.vue'

// const routes: RouteRecordRaw[] = [
//     { path: '/track/:item', component: TrackView },
//     { path: '/', component: SearchView },
// ]

export const router = createRouter({
    history: createWebHistory(),
    routes
})