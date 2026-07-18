// 路由配置 - 单页应用路由
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import News from '@/views/News.vue'
import NewsDetail from '@/views/NewsDetail.vue'
import Faq from '@/views/Faq.vue'
import Contact from '@/views/Contact.vue'

const routes = [
  { path: '/', name: 'home', component: Home, meta: { title: '首页' } },
  { path: '/about', name: 'about', component: About, meta: { title: '关于我们' } },
  { path: '/news', name: 'news', component: News, meta: { title: '资讯中心' } },
  { path: '/news/:id', name: 'news-detail', component: NewsDetail, meta: { title: '资讯详情' } },
  { path: '/faq', name: 'faq', component: Faq, meta: { title: '常见问题' } },
  { path: '/contact', name: 'contact', component: Contact, meta: { title: '联系我们' } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
