import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 管理后台路由
  { path: '/', name: 'Home', component: () => import('../views/Home.vue'), meta: { title: '首页' } },
  { path: '/machines', name: 'Machines', component: () => import('../views/Machines.vue'), meta: { title: '机型管理' } },
  { path: '/machines/:id', name: 'MachineDetail', component: () => import('../views/MachineDetail.vue'), meta: { title: '机型详情' } },
  { path: '/faq', name: 'FaqList', component: () => import('../views/FaqList.vue'), meta: { title: 'FAQ列表' } },
  { path: '/faq/create', name: 'FaqCreate', component: () => import('../views/FaqEdit.vue'), meta: { title: '新建FAQ' } },
  { path: '/faq/:id/edit', name: 'FaqEdit', component: () => import('../views/FaqEdit.vue'), meta: { title: '编辑FAQ' } },
  { path: '/faq/:id', name: 'FaqDetail', component: () => import('../views/FaqDetail.vue'), meta: { title: 'FAQ详情' } },
  { path: '/search', name: 'Search', component: () => import('../views/Search.vue'), meta: { title: '高级搜索' } },
  { path: '/favorites', name: 'Favorites', component: () => import('../views/Favorites.vue'), meta: { title: '我的收藏' } },
  { path: '/categories', name: 'Categories', component: () => import('../views/Categories.vue'), meta: { title: '分类管理' } },
  { path: '/tags/:id', name: 'TagDetail', component: () => import('../views/TagDetail.vue'), meta: { title: '标签详情' } },
  { path: '/tags', name: 'Tags', component: () => import('../views/Tags.vue'), meta: { title: '标签管理' } },
  { path: '/statistics', name: 'Statistics', component: () => import('../views/Statistics.vue'), meta: { title: '数据统计' } },

  // 客户端帮助中心路由（/help 前缀）
  { path: '/help', name: 'HelpCenter', component: () => import('../views/HelpCenter.vue'), meta: { title: '帮助中心' } },
  { path: '/help/machines/:id', name: 'HelpMachineDetail', component: () => import('../views/MachineDetail.vue'), meta: { title: '产品详情' } },
  { path: '/help/faq/:id', name: 'HelpFaqDetail', component: () => import('../views/FaqDetail.vue'), meta: { title: 'FAQ详情' } },
  { path: '/help/search', name: 'HelpSearch', component: () => import('../views/Search.vue'), meta: { title: '搜索' } },

  // 404 兜底
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('../views/NotFound.vue'), meta: { title: '404' } }
]

const router = createRouter({
  // 和 vite.config.js 的 base 保持一致，支持 GitHub Pages 子路径部署
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})
export default router
