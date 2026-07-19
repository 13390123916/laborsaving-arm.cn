// 路由配置 - 单页应用路由 + SEO 全局 TDK 注入
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import News from '@/views/News.vue'
import NewsDetail from '@/views/NewsDetail.vue'
import Faq from '@/views/Faq.vue'
import Contact from '@/views/Contact.vue'
import { setTDK, getSiteConfig } from '@/plugins/seo'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: '气动助力机械臂厂家 | 工业机械臂解决方案',
      keywords: '气动助力机械臂,助力臂,机械臂厂家,工业自动化,平衡吊,零重力臂',
      description: 'LABOR-SAVING 专注气动助力机械臂研发生产，提供负载50-800kg工业助力臂、平衡吊、定制化自动化解决方案，厂家直供，支持全国上门安装。'
    }
  },
  {
    path: '/about',
    name: 'about',
    component: About,
    meta: {
      title: '关于我们 | LABOR-SAVING 气动助力机械臂',
      keywords: '助力机械臂厂家,工业自动化企业,LABOR-SAVING,企业资质,辽宁机械臂厂,沈阳机械臂厂家',
      description: '了解 LABOR-SAVING 智能装备有限公司——专注气动助力机械臂研发生产10余年，服务500+企业客户的实力厂家。'
    }
  },
  {
    path: '/news',
    name: 'news',
    component: News,
    meta: {
      title: '资讯中心 | 气动助力机械臂行业资讯',
      keywords: '助力机械臂行业资讯,工业自动化新闻,机械臂技术文章',
      description: 'LABOR-SAVING 气动助力机械臂资讯中心，为您带来行业动态、技术文章、应用案例等专业内容。'
    }
  },
  {
    path: '/news/:id',
    name: 'news-detail',
    component: NewsDetail,
    meta: {
      title: '资讯详情',
      keywords: '',
      description: ''
    }
  },
  {
    path: '/faq',
    name: 'faq',
    component: Faq,
    meta: {
      title: '常见问题 | 气动助力机械臂采购 FAQ',
      keywords: '助力机械臂常见问题,机械臂FAQ,气动臂采购问题,工业机械臂问答',
      description: '汇总气动助力机械臂采购高频疑问10+条，涵盖选型、价格、安装、售后、定制等关键问题，助您快速决策。'
    }
  },
  {
    path: '/contact',
    name: 'contact',
    component: Contact,
    meta: {
      title: '联系我们 | 获取免费方案报价',
      keywords: '助力机械臂报价,机械臂咨询,厂家联系方式,免费方案设计',
      description: '联系 LABOR-SAVING 专业工程师，获取免费1对1方案设计与报价。电话、在线表单均可，48小时内上门服务。'
    }
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 全局后置守卫 — 每页独立 TDK 注入
router.afterEach((to) => {
  const site = getSiteConfig() || {}
  const meta = to.meta || {}
  setTDK({
    title: meta.title || site.site_title || 'LABOR-SAVING 气动助力机械臂',
    keywords: meta.keywords || site.site_keywords || '',
    description: meta.description || site.site_description || ''
  })
})

export default router
