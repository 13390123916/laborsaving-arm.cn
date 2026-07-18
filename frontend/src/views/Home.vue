<template>
  <div class="home">
    <!-- Hero 区 -->
    <section class="hero">
      <div class="container">
        <h1>{{ config.site_name || '气动助力机械臂' }}</h1>
        <p class="hero-sub">{{ config.site_description }}</p>
        <div class="hero-actions">
          <router-link to="/contact" class="btn btn-accent">免费咨询</router-link>
          <router-link to="/about" class="btn">了解企业</router-link>
        </div>
      </div>
    </section>

    <!-- 核心产品 -->
    <section class="section container">
      <h2 class="section-title">核心产品</h2>
      <div class="grid grid-3">
        <div class="card product-card" v-for="p in productList" :key="p.id">
          <div class="product-icon">{{ p.icon }}</div>
          <h3>{{ p.name }}</h3>
          <p class="text-light">{{ p.description }}</p>
        </div>
      </div>
    </section>

    <!-- 企业优势 -->
    <section class="section container">
      <h2 class="section-title">为什么选择我们</h2>
      <div class="grid grid-4">
        <div class="advantage" v-for="a in advantages" :key="a.title">
          <div class="advantage-num">{{ a.num }}</div>
          <h4>{{ a.title }}</h4>
          <p class="text-light">{{ a.desc }}</p>
        </div>
      </div>
    </section>

    <!-- FAQ 预览 -->
    <section class="section container">
      <h2 class="section-title">常见问题</h2>
      <div class="faq-preview">
        <div class="faq-item" v-for="f in faqList" :key="f.id">
          <h4>Q：{{ f.question }}</h4>
          <p class="text-light">{{ f.answer }}</p>
        </div>
      </div>
      <div class="text-center mt-20">
        <router-link to="/faq" class="btn">查看全部问答</router-link>
      </div>
    </section>

    <!-- 转化 CTA -->
    <section class="cta-section">
      <div class="container text-center">
        <h2>需要助力机械臂解决方案？</h2>
        <p class="text-light">专业工程师1对1方案设计，免费获取报价</p>
        <router-link to="/contact" class="btn btn-accent">立即咨询</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { siteApi, faqApi, productApi } from '@/api'
import { useJsonLd, buildOrganizationSchema } from '@/composables/useJsonLd'

const config = ref({})
const faqList = ref([])
const productList = ref([])

const advantages = [
  { num: '10+', title: '行业经验', desc: '深耕工业助力领域十余年' },
  { num: '500+', title: '服务客户', desc: '遍布汽车、3C、家电等行业' },
  { num: '48h', title: '响应速度', desc: '省内48小时上门服务' },
  { num: '100%', title: '安全设计', desc: '断气保护，工件绝不坠落' }
]

// 注入 Organization 结构化数据（对齐后端 /schema/organization.json）
const { inject: injectOrgSchema } = useJsonLd('schema-organization')

onMounted(async () => {
  try {
    const [c, f, p] = await Promise.all([siteApi.getConfig(), faqApi.list(), productApi.list()])
    if (c.code === 200) {
      config.value = c.data
      injectOrgSchema(buildOrganizationSchema(c.data))
    }
    if (f.code === 200) faqList.value = f.data.slice(0, 4)
    if (p.code === 200) productList.value = p.data
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.hero { background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%); color: #fff; padding: 80px 0; text-align: center; }
.hero h1 { font-size: 2.5rem; margin-bottom: 16px; }
.hero-sub { font-size: 1.1rem; opacity: 0.9; max-width: 600px; margin: 0 auto 28px; }
.hero-actions .btn { margin: 0 8px; }

.product-icon { font-size: 2.5rem; margin-bottom: 12px; }
.product-card h3 { margin-bottom: 8px; font-size: 1.2rem; }

.advantage { text-align: center; padding: 20px; }
.advantage-num { font-size: 2rem; font-weight: 700; color: var(--accent); }
.advantage h4 { margin: 8px 0; }

.faq-preview { max-width: 800px; margin: 0 auto; }
.faq-item { padding: 16px 0; border-bottom: 1px solid var(--border); }
.faq-item h4 { color: var(--primary); margin-bottom: 6px; }

.cta-section { background: var(--bg-gray); padding: 48px 0; }
.cta-section h2 { margin-bottom: 8px; }

@media (max-width: 767px) {
  .hero { padding: 48px 0; }
  .hero h1 { font-size: 1.8rem; }
  .hero-actions .btn { display: block; margin: 8px auto; max-width: 200px; }
}
</style>
