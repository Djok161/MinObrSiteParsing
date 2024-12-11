import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DataTable from "@/views/DataTable.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/file',
      name: 'file',
      component: () => import('../views/FileUpload.vue'),
    },

    {
      path: '/details/:tag',
      name: 'DetailsPage',
      component: DataTable,
      props: true, // Позволяет передавать параметры как пропсы
    },
  ],
})

export default router
