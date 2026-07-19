<template>
  <div class="news">
    <div class="container">
      <!-- 面包屑导航 -->
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> / <span>资讯中心</span>
      </nav>

      <h1 class="page-title">资讯中心</h1>

      <!-- 分类筛选 -->
      <div class="category-tabs">
        <button :class="['tab', { active: !activeCat }]" @click="switchCat('')">全部</button>
        <button :class="['tab', { active: activeCat === c }]" v-for="c in categories" :key="c"
          @click="switchCat(c)">{{ c }}</button>
      </div>

      <!-- 文章列表 -->
      <div class="article-list" v-if="articles.length">
        <article class="article-item card" v-for="a in articles" :key="a.id">
          <div class="article-cover">
            <!-- 封面图：有URL显示图片，无则显示分类占位 -->
            <img v-if="a.cover" :src="a.cover" :alt="a.title" />
            <div v-else class="cover-placeholder">{{ a.category.slice(0, 2) }}</div>
          </div>
          <div class="article-body">
            <div class="article-meta">
              <span class="cat-tag">{{ a.category }}</span>
              <span class="text-light">{{ formatDate(a.created_at) }}</span>
            </div>
            <h3><router-link :to="`/news/${a.id}`">{{ a.title }}</router-link></h3>
            <p class="text-light">{{ a.summary }}</p>
            <router-link :to="`/news/${a.id}`" class="read-more">阅读全文 →</router-link>
          </div>
        </article>
      </div>
      <p v-else class="text-center text-light empty-tip">暂无相关资讯</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { articleApi } from '@/api'

const articles = ref([])
const categories = ref([])
const activeCat = ref('')

const loadArticles = async (cat = '') => {
  try {
    const res = await articleApi.list({ category: cat, page_size: 20 })
    if (res.code === 200) articles.value = res.data.list
  } catch (e) { console.error(e) }
}

const switchCat = (cat) => {
  activeCat.value = cat
  loadArticles(cat)
}

const formatDate = (d) => new Date(d).toLocaleDateString('zh-CN')

onMounted(async () => {
  await loadArticles()
  try {
    const res = await articleApi.categories()
    if (res.code === 200) categories.value = res.data
  } catch (e) { console.error(e) }
})
</script>

<style scoped>
.breadcrumb { padding: 16px 0 8px; font-size: 0.85rem; color: var(--text-light); }
.breadcrumb a { color: var(--text-light); }
.page-title { text-align: center; font-size: 2rem; margin: 16px 0 32px; }
.category-tabs { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 28px; }
.tab { padding: 8px 18px; border: 1px solid var(--border); background: #fff; border-radius: 20px; cursor: pointer; font-size: 0.9rem; }
.tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }

.article-item { display: flex; gap: 16px; margin-bottom: 20px; align-items: flex-start; }
.article-cover { width: 200px; flex-shrink: 0; }
.article-cover img { width: 200px; height: 140px; object-fit: cover; border-radius: 6px; }
.cover-placeholder { width: 200px; height: 140px; background: var(--primary); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 700; border-radius: 6px; }
.article-body { flex: 1; }
.article-meta { display: flex; gap: 12px; align-items: center; font-size: 0.85rem; margin-bottom: 8px; }
.cat-tag { background: var(--bg-gray); color: var(--primary); padding: 2px 10px; border-radius: 4px; }
.article-body h3 { margin-bottom: 8px; font-size: 1.15rem; }
.article-body h3 a { color: var(--text); }
.article-body h3 a:hover { color: var(--primary); }
.read-more { color: var(--primary); font-size: 0.9rem; }
.empty-tip { padding: 40px 0; }

@media (max-width: 767px) {
  .article-item { flex-direction: column; }
  .article-cover, .article-cover img, .cover-placeholder { width: 100%; }
  .article-cover img, .cover-placeholder { height: 180px; }
}
</style>
