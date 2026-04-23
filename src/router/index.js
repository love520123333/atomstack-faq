import { createRouter, createWebHistory } from 'vue-router'

const routes = [
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
  { path: '/statistics', name: 'Statistics', component: () => import('../views/Statistics.vue'), meta: { title: '数据统计' } }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})
export default router
