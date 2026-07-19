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
        <button class="like-btn" @click="handleLike" :class="{ liked: liked }">
          👍 {{ likeCount }}
        </button>
      </div>

      <!-- 文章封面（如有） -->
      <div class="detail-cover" v-if="article.cover_image_url || article.cover">
        <img :src="article.cover_image_url || article.cover" :alt="article.title" />
      </div>

      <!-- 文章内容（支持富文本 HTML，含图片/排版） -->
      <div class="detail-content" v-html="formattedContent"></div>

      <!-- 相关推荐（同分类优先） -->
      <section class="section" v-if="relatedList.length">
        <h3 class="related-title">相关资讯</h3>
        <div class="related-list">
          <router-link v-for="r in relatedList" :key="r.id" :to="`/news/${r.slug || r.id}`" class="related-item">
            <span class="related-cat">{{ r.category }}</span>
            <span class="related-title-text">{{ r.title }}</span>
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
import { articleApi, likeApi } from '@/api'
import { setTDK, getSiteConfig } from '@/plugins/seo'
import { useJsonLd, buildArticleSchema } from '@/composables/useJsonLd'

const route = useRoute()
const article = ref(null)
const relatedList = ref([])
const liked = ref(false)
const likeCount = ref(0)

// 注入 Article 结构化数据
const { inject: injectArticleSchema } = useJsonLd('schema-article')

const formattedContent = computed(() => {
  const c = article.value?.content
  if (!c) return ''
  const trimmed = c.trim()
  // 含 HTML 标签则按富文本原样渲染（支持图文混排），否则按换行分段（兼容旧纯文本）
  if (/<[a-z!][\s\S]*>/i.test(trimmed)) return trimmed
  return trimmed
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
      setTDK({
        title: res.data.seo_title || res.data.title + ' | LABOR-SAVING 气动助力机械臂',
        keywords: res.data.seo_keywords || '',
        description: res.data.seo_description || res.data.summary || ''
      })
      const site = getSiteConfig()
      injectArticleSchema(buildArticleSchema(res.data, site))
      // 加载点赞数
      loadLikeCount(id)
    }
  } catch (e) { console.error(e) }
}

const loadRelated = async () => {
  try {
    // 优先取同分类文章
    let res = null
    if (article.value?.category) {
      res = await articleApi.list({ category: article.value.category, page_size: 10 })
    }
    if (!res || res.code !== 200 || !res.data.list.length) {
      res = await articleApi.list({ page_size: 6 })
    }
    if (res.code === 200) {
      relatedList.value = res.data.list.filter(a => a.id !== article.value?.id).slice(0, 4)
    }
  } catch (e) { console.error(e) }
}

const loadLikeCount = async (id) => {
  try {
    const res = await likeApi.count({ article: id })
    if (res.code === 200) likeCount.value = res.data.total
  } catch (e) { /* ignore */ }
}

const handleLike = async () => {
  if (!article.value) return
  liked.value = true
  try {
    const res = await likeApi.submit({ article: article.value.id })
    if (res.code === 200 && res.data?.total) {
      likeCount.value = res.data.total
    }
  } catch (e) { /* ignore */ }
}

watch(() => route.params.id, (newId) => {
  if (newId) {
    article.value = null
    liked.value = false
    likeCount.value = 0
    loadDetail(newId)
    loadRelated()
    window.scrollTo(0, 0)
  }
})

onMounted(() => {
  loadDetail(route.params.id)
  loadRelated()
})
</script>

<style scoped>
.breadcrumb { padding: 20px 0 12px; font-size: 0.85rem; color: var(--text-light); }
.breadcrumb a { color: var(--text-light); }
.breadcrumb a:hover { color: var(--primary); }
.detail-title { font-size: 1.8rem; margin-bottom: 12px; line-height: 1.4; color: var(--text); }
.detail-meta { display: flex; gap: 14px; align-items: center; font-size: 0.85rem; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border); flex-wrap: wrap; }
.cat-tag { background: var(--primary-soft); color: var(--primary); padding: 2px 10px; border-radius: 4px; font-weight: 600; }
.like-btn { background: none; border: 1px solid var(--border); border-radius: 20px; padding: 4px 12px; cursor: pointer; font-size: 0.85rem; margin-left: auto; color: var(--text-light); transition: all 0.2s; }
.like-btn:hover { border-color: var(--primary); color: var(--primary); background: var(--primary-soft); }
.like-btn.liked { border-color: var(--primary); color: var(--primary); background: var(--primary-soft); }
.detail-cover { margin-bottom: 20px; }
.detail-cover img { width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; border: 1px solid var(--border); }
.detail-content { line-height: 1.9; font-size: 1rem; color: var(--text); }
.detail-content :deep(p) { margin-bottom: 16px; }
.related-title { margin: 24px 0 16px; font-size: 1.2rem; color: var(--text); }
.related-list { display: flex; flex-direction: column; gap: 10px; }
.related-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--bg-section); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 0.95rem; transition: border-color 0.2s; }
.related-item:hover { color: var(--primary); border-color: var(--primary); }
.related-cat { background: var(--primary); color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; white-space: nowrap; }
.related-title-text { flex: 1; }

@media (max-width: 679px) {
  .detail-title { font-size: 1.4rem; }
  .detail-meta { gap: 8px; }
  .like-btn { margin-left: 0; }
}
</style>
