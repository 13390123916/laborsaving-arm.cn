<template>
  <div class="news-detail" v-if="article">
    <div class="container">
      <!-- 面包屑 -->
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> /
        <router-link to="/news">资讯</router-link> /
        <span>{{ article.category }}</span>
      </nav>

      <h1 class="detail-title">{{ article.title }}</h1>
      <div class="detail-meta">
        <span class="cat-tag">{{ article.category }}</span>
        <span class="text-light">{{ formatDate(article.created_at) }}</span>
        <span class="text-light">浏览 {{ article.views }}</span>
      </div>

      <!-- 文章内容 -->
      <div class="detail-content" v-html="formattedContent"></div>

      <!-- 相关推荐 -->
      <section class="section">
        <h3 class="related-title">相关资讯</h3>
        <div class="related-list">
          <router-link v-for="r in relatedList" :key="r.id" :to="`/news/${r.id}`" class="related-item">
            {{ r.title }}
          </router-link>
        </div>
      </section>

      <div class="text-center section">
        <router-link to="/contact" class="btn btn-accent">获取方案报价</router-link>
      </div>
    </div>
  </div>
  <div v-else class="container text-center" style="padding: 60px 0;">
    <p class="text-light">文章加载中或不存在...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { articleApi } from '@/api'

const route = useRoute()
const article = ref(null)
const relatedList = ref([])

const formattedContent = computed(() => {
  if (!article.value?.content) return ''
  // 将换行转为段落
  return article.value.content
    .split('\n')
    .filter(p => p.trim())
    .map(p => `<p>${p}</p>`)
    .join('')
})

const formatDate = (d) => new Date(d).toLocaleDateString('zh-CN')

const loadDetail = async (id) => {
  try {
    const res = await articleApi.detail(id)
    if (res.code === 200) {
      article.value = res.data
      // 设置页面 TDK
      document.title = res.data.seo_title || res.data.title
      setMetaDesc(res.data.seo_description || res.data.summary)
    }
  } catch (e) { console.error(e) }
}

const loadRelated = async () => {
  try {
    const res = await articleApi.list({ page_size: 5 })
    if (res.code === 200) {
      relatedList.value = res.data.list.filter(a => a.id !== article.value?.id).slice(0, 4)
    }
  } catch (e) { console.error(e) }
}

const setMetaDesc = (desc) => {
  let el = document.querySelector('meta[name="description"]')
  if (el) el.setAttribute('content', desc)
}

onMounted(() => {
  loadDetail(route.params.id)
  loadRelated()
})

watch(() => route.params.id, (newId) => {
  if (newId) {
    article.value = null
    loadDetail(newId)
    loadRelated()
    window.scrollTo(0, 0)
  }
})
</script>

<style scoped>
.breadcrumb { padding: 20px 0 12px; font-size: 0.85rem; color: var(--text-light); }
.breadcrumb a { color: var(--text-light); }
.detail-title { font-size: 1.8rem; margin-bottom: 12px; line-height: 1.4; }
.detail-meta { display: flex; gap: 14px; align-items: center; font-size: 0.85rem; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }
.cat-tag { background: var(--bg-gray); color: var(--primary); padding: 2px 10px; border-radius: 4px; }
.detail-content { line-height: 1.9; font-size: 1rem; color: var(--text); }
.detail-content :deep(p) { margin-bottom: 16px; }
.related-title { margin: 24px 0 16px; font-size: 1.2rem; }
.related-list { display: flex; flex-direction: column; gap: 10px; }
.related-item { padding: 12px 16px; background: var(--bg-gray); border-radius: 6px; color: var(--text); font-size: 0.95rem; }
.related-item:hover { color: var(--primary); }

@media (max-width: 767px) {
  .detail-title { font-size: 1.4rem; }
}
</style>
