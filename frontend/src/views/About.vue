<template>
  <div class="about">
    <div class="container">
      <!-- 面包屑导航 -->
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> / <span>关于我们</span>
      </nav>

      <h1 class="page-title">关于我们</h1>

      <!-- 企业实体信用卡片 -->
      <div class="company-card card">
        <div class="company-header">
          <h2>{{ config.company_name }}</h2>
          <span class="badge">实体企业认证</span>
        </div>
        <p class="company-intro">{{ config.company_intro }}</p>

        <div class="company-facts">
          <div class="fact-item">
            <span class="fact-label">成立时间</span>
            <span class="fact-value">{{ config.founded_year }} 年</span>
          </div>
          <div class="fact-item">
            <span class="fact-label">经营规模</span>
            <span class="fact-value">{{ config.company_scale }}</span>
          </div>
          <div class="fact-item">
            <span class="fact-label">办公地址</span>
            <span class="fact-value">{{ config.office_address }}</span>
          </div>
          <div class="fact-item">
            <span class="fact-label">联系电话</span>
            <a :href="'tel:' + (config.contact_phone || '')" class="tel-link">{{ config.contact_phone }}</a>
          </div>
        </div>
      </div>

      <!-- 资质证书展示 -->
      <section class="section">
        <h2 class="section-title">资质证书</h2>
        <div class="cert-grid" v-if="certList.length">
          <div class="cert-card" v-for="cert in certList" :key="cert.id">
            <div class="cert-icon">🏆</div>
            <h4>{{ cert.name }}</h4>
            <p class="text-light" v-if="cert.description">{{ cert.description }}</p>
          </div>
        </div>
      </section>

      <!-- 企业历程时间线 -->
      <section class="section">
        <h2 class="section-title">企业发展历程</h2>
        <div class="timeline" v-if="milestones.length">
          <div class="timeline-item" v-for="(m, i) in milestones" :key="m.id">
            <div class="timeline-dot" :class="{ active: i === 0 }"></div>
            <div class="timeline-content card">
              <span class="timeline-year">{{ m.year }}</span>
              <h4>{{ m.title }}</h4>
              <p class="text-light" v-if="m.description">{{ m.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 服务范围 -->
      <section class="section">
        <h2 class="section-title">服务范围</h2>
        <p class="service-text">{{ config.service_scope }}</p>
      </section>

      <!-- 企业实景轮播 -->
      <section class="section">
        <h2 class="section-title">企业实景</h2>
        <div class="carousel-wrapper">
          <div class="carousel-track" :style="{ transform: `translateX(-${carouselIndex * 100}%)` }">
            <div class="carousel-slide" v-for="(item, i) in scenes" :key="i">
              <div class="scene-img">{{ item.icon }}</div>
              <p class="text-center text-light">{{ item.label }}</p>
            </div>
          </div>
          <div class="carousel-dots">
            <span :class="['dot', { active: carouselIndex === i }]" v-for="(_, i) in scenes" :key="i"
              @click="carouselIndex = i"></span>
          </div>
        </div>
      </section>

      <!-- 联系方式入口 -->
      <section class="section text-center">
        <router-link to="/contact" class="btn btn-accent">联系我们</router-link>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { siteApi, certificateApi, milestoneApi } from '@/api'
import { useJsonLd, buildOrganizationSchema } from '@/composables/useJsonLd'

const config = ref({})
const certList = ref([])
const milestones = ref([])
const carouselIndex = ref(0)
let carouselTimer = null

// 注入 Organization/LocalBusiness 结构化数据（关于页是企业实体背书核心页面）
const { inject: injectOrgSchema } = useJsonLd('schema-organization')

const scenes = [
  { icon: '🏭', label: '办公大楼' },
  { icon: '🏗️', label: '生产车间' },
  { icon: '🔬', label: '研发中心' }
]

const startCarousel = () => {
  carouselTimer = setInterval(() => {
    carouselIndex.value = (carouselIndex.value + 1) % scenes.length
  }, 4000)
}

onMounted(async () => {
  try {
    const [c, certRes, mileRes] = await Promise.all([
      siteApi.getConfig(),
      certificateApi.list(),
      milestoneApi.list()
    ])
    if (c.code === 200) {
      config.value = c.data
      // 注入 Organization JSON-LD，与首页和后端 /schema/organization.json 对齐
      injectOrgSchema(buildOrganizationSchema(c.data))
    }
    if (certRes.code === 200) certList.value = certRes.data
    if (mileRes.code === 200) milestones.value = mileRes.data
  } catch (e) {
    console.error(e)
  }
  startCarousel()
})

onUnmounted(() => {
  if (carouselTimer) clearInterval(carouselTimer)
})
</script>

<style scoped>
.breadcrumb { padding: 16px 0 8px; font-size: 0.85rem; color: var(--text-light); }
.breadcrumb a { color: var(--text-light); }
.breadcrumb a:hover { color: var(--primary); }
.page-title { text-align: center; font-size: 2rem; margin: 16px 0 32px; color: var(--text); }
.company-card { max-width: 900px; margin: 0 auto; border-color: var(--border-strong); }
.company-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 8px; }
.company-header h2 { font-size: 1.5rem; color: #fff; }
.badge { background: var(--primary); color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; }
.company-intro { line-height: 1.8; color: var(--text-light); margin-bottom: 20px; }
.company-facts { display: grid; grid-template-columns: 1fr; gap: 12px; }
.fact-item { display: flex; justify-content: space-between; padding: 12px 14px; background: var(--bg-section); border: 1px solid var(--border); border-radius: 6px; }
.fact-label { color: var(--text-light); }
.fact-value { font-weight: 600; color: var(--text); }

/* 资质证书 */
.cert-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; max-width: 800px; margin: 0 auto; }
.cert-card { text-align: center; padding: 20px; background: var(--bg-section); border-radius: 8px; border: 1px solid var(--border); transition: border-color 0.2s, transform 0.2s; }
.cert-card:hover { border-color: var(--primary); transform: translateY(-2px); }
.cert-icon { font-size: 2.5rem; margin-bottom: 8px; }
.cert-card h4 { font-size: 0.95rem; color: var(--text); margin-bottom: 4px; }
.cert-card p { font-size: 0.85rem; }

/* 时间线 */
.timeline { position: relative; max-width: 700px; margin: 0 auto; padding-left: 30px; }
.timeline::before { content: ''; position: absolute; left: 10px; top: 0; bottom: 0; width: 2px; background: var(--border); }
.timeline-item { position: relative; margin-bottom: 24px; }
.timeline-dot { position: absolute; left: -24px; top: 20px; width: 12px; height: 12px; border-radius: 50%; background: var(--border-strong); border: 2px solid var(--bg); z-index: 1; }
.timeline-dot.active { background: var(--primary); border-color: var(--primary); }
.timeline-content { padding: 16px 20px; }
.timeline-year { display: inline-block; background: var(--primary); color: #fff; padding: 2px 10px; border-radius: 4px; font-size: 0.8rem; margin-bottom: 8px; }
.timeline-content h4 { margin-bottom: 4px; font-size: 1rem; color: var(--text); }

/* 轮播 */
.carousel-wrapper { max-width: 600px; margin: 0 auto; overflow: hidden; position: relative; }
.carousel-track { display: flex; transition: transform 0.5s ease; }
.carousel-slide { min-width: 100%; padding: 0 8px; }
.scene-img { background: var(--bg-section); height: 200px; display: flex; align-items: center; justify-content: center; font-size: 4rem; border-radius: 8px; margin-bottom: 8px; border: 1px solid var(--border); }
.carousel-dots { display: flex; justify-content: center; gap: 8px; margin-top: 12px; }
.dot { width: 10px; height: 10px; border-radius: 50%; background: var(--border-strong); cursor: pointer; transition: background 0.3s; }
.dot.active { background: var(--primary); }

.service-text { max-width: 800px; margin: 0 auto; text-align: center; color: var(--text-light); line-height: 1.8; }

@media (min-width: 768px) {
  .company-facts { grid-template-columns: 1fr 1fr; }
  .cert-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 679px) {
  .page-title { font-size: 1.5rem; }
  .cert-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
  .timeline { padding-left: 24px; }
  .scene-img { height: 160px; font-size: 3rem; }
}
</style>
