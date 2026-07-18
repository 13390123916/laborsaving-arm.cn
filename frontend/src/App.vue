<template>
  <div class="app-wrapper">
    <!-- 顶部导航 -->
    <header class="navbar">
      <div class="container nav-inner">
        <router-link to="/" class="logo">
          <span class="logo-text">{{ siteConfig.site_name || 'LABOR-SAVING' }}</span>
        </router-link>
        <!-- PC导航 -->
        <nav class="nav-menu">
          <router-link to="/">首页</router-link>
          <router-link to="/about">关于我们</router-link>
          <router-link to="/news">资讯中心</router-link>
          <router-link to="/faq">常见问题</router-link>
          <router-link to="/contact" class="nav-cta">联系我们</router-link>
        </nav>
        <!-- 移动端汉堡菜单 -->
        <button class="nav-toggle" @click="showMenu = !showMenu" aria-label="菜单">
          <span></span><span></span><span></span>
        </button>
      </div>
      <!-- 移动端下拉菜单 -->
      <transition name="slide">
        <nav v-if="showMenu" class="nav-mobile">
          <router-link to="/" @click="showMenu=false">首页</router-link>
          <router-link to="/about" @click="showMenu=false">关于我们</router-link>
          <router-link to="/news" @click="showMenu=false">资讯中心</router-link>
          <router-link to="/faq" @click="showMenu=false">常见问题</router-link>
          <router-link to="/contact" @click="showMenu=false">联系我们</router-link>
        </nav>
      </transition>
    </header>

    <!-- 路由视图 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container footer-inner">
        <div class="footer-col">
          <h4>{{ siteConfig.company_name || 'LABOR-SAVING' }}</h4>
          <p class="text-light">{{ siteConfig.company_intro?.slice(0, 60) }}...</p>
        </div>
        <div class="footer-col">
          <h4>快捷导航</h4>
          <p><router-link to="/about">关于我们</router-link></p>
          <p><router-link to="/news">资讯中心</router-link></p>
          <p><router-link to="/faq">常见问题</router-link></p>
          <p><router-link to="/contact">联系我们</router-link></p>
        </div>
        <div class="footer-col">
          <h4>联系方式</h4>
          <p>电话：{{ siteConfig.contact_phone || '400-888-xxxx' }}</p>
          <p>邮箱：{{ siteConfig.contact_email || 'sales@laborsaving-arm.cn' }}</p>
          <p>地址：{{ siteConfig.office_address || '山东青岛' }}</p>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="container">
          <p>© 2015-{{ new Date().getFullYear() }} {{ siteConfig.company_name }} 版权所有</p>
          <p class="text-light">气动助力机械臂 · 工业自动化解决方案提供商</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { siteApi } from '@/api'

const showMenu = ref(false)
const siteConfig = ref({})

onMounted(async () => {
  try {
    const res = await siteApi.getConfig()
    if (res.code === 200) siteConfig.value = res.data
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.app-wrapper { min-height: 100vh; display: flex; flex-direction: column; }
.navbar {
  position: sticky; top: 0; z-index: 100;
  background: #fff; border-bottom: 1px solid var(--border);
}
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 64px; }
.logo-text { font-size: 1.25rem; font-weight: 700; color: var(--primary); }
.nav-menu { display: flex; gap: 28px; align-items: center; }
.nav-menu a { color: var(--text); font-size: 0.95rem; padding: 4px 0; }
.nav-menu a.router-link-active { color: var(--primary); font-weight: 600; }
.nav-cta { background: var(--primary); color: #fff !important; padding: 8px 18px !important; border-radius: 4px; }
.nav-cta:hover { background: var(--primary-dark); }

.nav-toggle { display: none; flex-direction: column; gap: 5px; background: none; border: none; cursor: pointer; }
.nav-toggle span { width: 24px; height: 2px; background: var(--text); }

.nav-mobile { display: flex; flex-direction: column; background: #fff; border-top: 1px solid var(--border); }
.nav-mobile a { padding: 14px 16px; border-bottom: 1px solid var(--border); color: var(--text); }

.main-content { flex: 1; }

.footer { background: #1a1a1a; color: #ccc; margin-top: 40px; }
.footer-inner { display: grid; grid-template-columns: 1fr; gap: 24px; padding: 40px 16px; }
.footer-col h4 { color: #fff; margin-bottom: 12px; font-size: 1rem; }
.footer-col p { font-size: 0.85rem; margin-bottom: 6px; }
.footer-col a { color: #ccc; }
.footer-bottom { border-top: 1px solid #333; padding: 16px; text-align: center; font-size: 0.8rem; }
.footer-bottom p { margin: 2px 0; }

.slide-enter-active, .slide-leave-active { transition: all 0.3s; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-10px); }

@media (min-width: 768px) {
  .footer-inner { grid-template-columns: 2fr 1fr 1fr; }
}
@media (max-width: 767px) {
  .nav-menu { display: none; }
  .nav-toggle { display: flex; }
}
</style>
