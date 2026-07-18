<template>
  <div class="about">
    <div class="container">
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
            <span class="fact-value">{{ config.contact_phone }}</span>
          </div>
        </div>
      </div>

      <!-- 资质实力 -->
      <section class="section">
        <h2 class="section-title">资质实力</h2>
        <div class="qualifications">
          <div class="qual-item" v-for="(q, i) in qualList" :key="i">✓ {{ q }}</div>
        </div>
      </section>

      <!-- 服务范围 -->
      <section class="section">
        <h2 class="section-title">服务范围</h2>
        <p class="service-text">{{ config.service_scope }}</p>
      </section>

      <!-- 企业实景 -->
      <section class="section">
        <h2 class="section-title">企业实景</h2>
        <div class="grid grid-3">
          <div class="showcase" v-for="n in 3" :key="n">
            <div class="showcase-img">🏭</div>
            <p class="text-center text-light">企业实景 {{ n }}</p>
          </div>
        </div>
      </section>

      <!-- 联系方式 -->
      <section class="section text-center">
        <router-link to="/contact" class="btn btn-accent">联系我们</router-link>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { siteApi } from '@/api'

const config = ref({})
const qualList = ref([])

onMounted(async () => {
  try {
    const res = await siteApi.getConfig()
    if (res.code === 200) {
      config.value = res.data
      qualList.value = (res.data.qualifications || '').split('、').filter(Boolean)
    }
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.page-title { text-align: center; font-size: 2rem; margin: 32px 0; }
.company-card { max-width: 900px; margin: 0 auto; }
.company-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 8px; }
.company-header h2 { font-size: 1.5rem; color: var(--primary); }
.badge { background: var(--accent); color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; }
.company-intro { line-height: 1.8; color: var(--text-light); margin-bottom: 20px; }
.company-facts { display: grid; grid-template-columns: 1fr; gap: 12px; }
.fact-item { display: flex; justify-content: space-between; padding: 12px; background: var(--bg-gray); border-radius: 6px; }
.fact-label { color: var(--text-light); }
.fact-value { font-weight: 600; }

.qualifications { display: grid; grid-template-columns: 1fr; gap: 12px; max-width: 700px; margin: 0 auto; }
.qual-item { padding: 12px 16px; background: var(--bg-gray); border-left: 3px solid var(--accent); border-radius: 4px; }
.service-text { max-width: 800px; margin: 0 auto; text-align: center; color: var(--text-light); line-height: 1.8; }
.showcase-img { background: var(--bg-gray); height: 160px; display: flex; align-items: center; justify-content: center; font-size: 3rem; border-radius: 8px; margin-bottom: 8px; }

@media (min-width: 768px) {
  .company-facts { grid-template-columns: 1fr 1fr; }
  .qualifications { grid-template-columns: 1fr 1fr; }
}
</style>
