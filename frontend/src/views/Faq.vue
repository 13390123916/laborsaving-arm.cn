<template>
  <div class="faq-page">
    <div class="container">
      <!-- 面包屑导航 -->
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> / <span>常见问题</span>
      </nav>

      <h1 class="page-title">常见问题</h1>
      <p class="page-sub text-center text-light">汇总气动助力机械臂采购高频疑问，助您快速决策</p>

      <!-- 分类筛选 -->
      <div class="cat-tabs" v-if="categories.length">
        <button :class="['tab', { active: !activeCat }]" @click="switchCat('')">全部</button>
        <button :class="['tab', { active: activeCat === c }]" v-for="c in categories" :key="c"
          @click="switchCat(c)">{{ c }}</button>
      </div>

      <!-- FAQ 列表 -->
      <div class="faq-list">
        <div class="faq-card" v-for="(f, i) in faqList" :key="f.id">
          <button class="faq-question" @click="toggle(i)">
            <span class="q-mark">Q</span>
            <span class="q-text">{{ f.question }}</span>
            <span class="q-arrow" :class="{ open: openIndex === i }">▼</span>
          </button>
          <div class="faq-answer" v-show="openIndex === i">
            <p class="answer-short">{{ f.answer }}</p>
            <div class="answer-detail" v-if="f.detail" v-html="formattedDetail(f.detail)"></div>
          </div>
        </div>
      </div>

      <!-- 转化 CTA -->
      <section class="section text-center">
        <p class="text-light">没找到您的问题？直接联系我们获取专业解答</p>
        <router-link to="/contact" class="btn btn-accent mt-20">在线咨询工程师</router-link>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { faqApi } from '@/api'
import { useJsonLd, buildFaqPageSchema } from '@/composables/useJsonLd'

const faqList = ref([])
const categories = ref([])
const activeCat = ref('')
const openIndex = ref(0)

// 注入 FAQPage 结构化数据
const { inject: injectFaqSchema } = useJsonLd('schema-faqpage')

const loadFaqs = async (cat = '') => {
  try {
    const res = await faqApi.list({ category: cat })
    if (res.code === 200) {
      faqList.value = res.data
      // 注入 FAQPage Schema（仅在全部列表时注入，避免分类筛选后数据不完整）
      if (!cat) {
        injectFaqSchema(buildFaqPageSchema(res.data))
      }
      // 提取分类
      const cats = [...new Set(res.data.map(f => f.category))]
      categories.value = cats
    }
  } catch (e) { console.error(e) }
}

const switchCat = (cat) => {
  activeCat.value = cat
  openIndex.value = 0
  loadFaqs(cat)
}

const toggle = (i) => {
  openIndex.value = openIndex.value === i ? -1 : i
}

const formattedDetail = (detail) => {
  return detail.split('\n').filter(p => p.trim()).map(p => `<p>${p}</p>`).join('')
}

onMounted(() => loadFaqs())
</script>

<style scoped>
.page-title { text-align: center; font-size: 2rem; margin: 32px 0 8px; color: var(--text); }
.breadcrumb { padding: 16px 0 8px; font-size: 0.85rem; color: var(--text-light); }
.breadcrumb a { color: var(--text-light); }
.breadcrumb a:hover { color: var(--primary); }
.page-sub { margin-bottom: 28px; }
.cat-tabs { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 24px; }
.tab { padding: 8px 18px; border: 1px solid var(--border); background: var(--bg-elevated); color: var(--text-light); border-radius: 20px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; }
.tab:hover { border-color: var(--border-strong); color: var(--text); }
.tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }

.faq-list { max-width: 860px; margin: 0 auto; }
.faq-card { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 12px; overflow: hidden; background: var(--bg-elevated); transition: border-color 0.2s; }
.faq-card:hover { border-color: var(--border-strong); }
.faq-question { width: 100%; display: flex; align-items: center; gap: 12px; padding: 18px 20px; background: none; border: none; cursor: pointer; text-align: left; font-size: 1rem; font-weight: 600; color: var(--text); }
.q-mark { background: var(--primary); color: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; flex-shrink: 0; }
.q-text { flex: 1; }
.q-arrow { font-size: 0.7rem; color: var(--text-light); transition: transform 0.2s; }
.q-arrow.open { transform: rotate(180deg); color: var(--primary); }
.faq-answer { padding: 0 20px 20px 58px; }
.answer-short { color: var(--primary); font-weight: 500; margin-bottom: 10px; }
.answer-detail { color: var(--text-light); line-height: 1.8; }
.answer-detail :deep(p) { margin-bottom: 8px; }

@media (max-width: 679px) {
  .faq-question { padding: 14px 16px; font-size: 0.92rem; }
  .faq-answer { padding: 0 16px 16px 52px; }
}
</style>
