<template>
  <div class="app-wrapper">
    <!-- 顶部导航 -->
    <header class="navbar">
      <div class="container nav-inner">
        <router-link to="/" class="logo">
          <span class="logo-mark"></span>
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

    <!-- 悬浮咨询入口 -->
    <div class="floating-consult">
      <router-link to="/contact" class="floating-btn" title="免费咨询">
        <span class="floating-icon">💬</span>
        <span class="floating-text">免费咨询</span>
      </router-link>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container footer-inner">
        <div class="footer-col footer-brand">
          <h4>{{ siteConfig.company_name || 'LABOR-SAVING' }}</h4>
          <p class="text-light">{{ siteConfig.company_intro?.slice(0, 60) }}...</p>
          <div class="footer-tags" v-if="siteConfig.service_scope">
            <span>工业自动化</span><span>气动助力</span><span>全国上门</span>
          </div>
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
          <p>电话：<a :href="'tel:' + (siteConfig.contact_phone || '')" class="tel-link">{{ siteConfig.contact_phone || '400-888-xxxx' }}</a></p>
          <p>邮箱：{{ siteConfig.contact_email || 'sales@laborsaving-arm.cn' }}</p>
          <p>地址：{{ siteConfig.office_address || '辽宁沈阳' }}</p>
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

/* —— 吸顶毛玻璃深色导航 —— */
.navbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(14, 16, 20, 0.82);
  backdrop-filter: saturate(160%) blur(12px);
  -webkit-backdrop-filter: saturate(160%) blur(12px);
  border-bottom: 1px solid var(--border);
}
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 66px; }
.logo { display: flex; align-items: center; gap: 10px; }
.logo-mark { width: 12px; height: 22px; border-radius: 3px; background: var(--primary); box-shadow: 0 0 0 3px var(--primary-soft); }
.logo-text { font-size: 1.2rem; font-weight: 800; color: var(--text); letter-spacing: 0.5px; }
.nav-menu { display: flex; gap: 28px; align-items: center; }
.nav-menu a { color: var(--text-light); font-size: 0.95rem; padding: 4px 0; position: relative; }
.nav-menu a:hover { color: var(--text); }
.nav-menu a.router-link-active { color: #fff; }
.nav-menu a.router-link-active::after {
  content: ''; position: absolute; left: 0; right: 0; bottom: -22px; height: 2px; background: var(--primary);
}
.nav-cta {
  background: var(--primary); color: #fff !important; padding: 8px 20px !important;
  border-radius: var(--radius-sm); box-shadow: 0 4px 14px rgba(240, 43, 35, 0.3);
}
.nav-cta:hover { background: var(--primary-dark); }
.nav-cta.router-link-active::after { display: none; }

/* —— 汉堡 —— */
.nav-toggle {
  display: none; flex-direction: column; gap: 5px;
  background: none; border: none; cursor: pointer; padding: 6px;
}
.nav-toggle span { width: 24px; height: 2px; background: var(--text); border-radius: 2px; transition: 0.2s; }

.nav-mobile {
  display: flex; flex-direction: column;
  background: var(--bg-elevated); border-top: 1px solid var(--border);
}
.nav-mobile a { padding: 15px 16px; border-bottom: 1px solid var(--border); color: var(--text-light); }
.nav-mobile a.router-link-active { color: #fff; background: var(--bg-section); border-left: 3px solid var(--primary); }

.main-content { flex: 1; }

/* —— 多列深色页脚 —— */
.footer { background: #0a0c10; color: var(--text-light); margin-top: 48px; border-top: 1px solid var(--border); }
.footer-inner { display: grid; grid-template-columns: 1fr; gap: 28px; padding: 48px 16px 32px; }
.footer-col h4 { color: #fff; margin-bottom: 14px; font-size: 1rem; }
.footer-col p { font-size: 0.88rem; margin-bottom: 8px; }
.footer-col a { color: var(--text-light); }
.footer-col a:hover { color: var(--primary); }
.footer-brand .footer-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.footer-brand .footer-tags span {
  font-size: 0.72rem; padding: 3px 10px; border: 1px solid var(--border-strong);
  border-radius: 20px; color: var(--text-light);
}
.footer-bottom { border-top: 1px solid var(--border); padding: 18px; text-align: center; font-size: 0.8rem; }
.footer-bottom p { margin: 3px 0; }

/* —— 滑动过渡 —— */
.slide-enter-active, .slide-leave-active { transition: all 0.3s; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-10px); }

/* —— 悬浮咨询按钮（品牌红） —— */
.floating-consult { position: fixed; bottom: 32px; right: 24px; z-index: 999; }
.floating-btn {
  display: flex; flex-direction: column; align-items: center; gap: 2px;
  background: var(--primary); color: #fff; padding: 12px 16px; border-radius: 50px;
  box-shadow: 0 6px 22px rgba(240, 43, 35, 0.45);
  text-decoration: none; transition: all 0.25s; cursor: pointer; border: none;
}
.floating-btn:hover { transform: translateY(-2px); background: var(--primary-dark); box-shadow: 0 8px 26px rgba(240, 43, 35, 0.55); }
.floating-icon { font-size: 1.4rem; }
.floating-text { font-size: 0.75rem; white-space: nowrap; }

/* —— 响应式：≥1020 显示桌面菜单，<1020 转汉堡 —— */
@media (min-width: 1020px) {
  .footer-inner { grid-template-columns: 2.2fr 1fr 1.4fr; }
}
@media (max-width: 1019px) {
  .nav-menu { display: none; }
  .nav-toggle { display: flex; }
  .footer-inner { grid-template-columns: 1fr 1fr; }
  .footer-brand { grid-column: 1 / -1; }
}
@media (max-width: 679px) {
  .floating-consult { bottom: 20px; right: 16px; }
  .floating-btn { padding: 10px 14px; }
  .floating-text { font-size: 0.7rem; }
  .footer-inner { grid-template-columns: 1fr; gap: 22px; padding: 36px 16px 24px; }
  .footer-brand { grid-column: auto; }
}
</style>
