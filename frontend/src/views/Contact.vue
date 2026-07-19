<template>
  <div class="contact-page">
    <div class="container">
      <!-- 面包屑导航 -->
      <nav class="breadcrumb">
        <router-link to="/">首页</router-link> / <span>联系我们</span>
      </nav>

      <h1 class="page-title">联系我们</h1>
      <p class="page-sub text-center text-light">填写下方表单，专业工程师将在24小时内与您联系</p>

      <div class="contact-wrap">
        <!-- 左侧信息 -->
        <div class="contact-info">
          <h3>联系方式</h3>
          <div class="info-item">
            <span class="info-label">电话</span>
            <a :href="'tel:' + (config.contact_phone || '')" class="tel-link">{{ config.contact_phone || '400-888-xxxx' }}</a>
          </div>
          <div class="info-item">
            <span class="info-label">邮箱</span>
            <span>{{ config.contact_email || 'sales@laborsaving-arm.cn' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">QQ</span>
            <span>{{ config.contact_qq || '800xxxxxx' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">地址</span>
            <span>{{ config.office_address || '辽宁沈阳' }}</span>
          </div>
          <div class="info-note">
            <p>✓ 免费获取方案设计与报价</p>
            <p>✓ 1对1工程师咨询服务</p>
            <p>✓ 全国上门勘测安装</p>
          </div>
        </div>

        <!-- 右侧表单 -->
        <div class="contact-form card">
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label>姓名 <span class="req">*</span></label>
              <input v-model="form.name" type="text" placeholder="请输入您的姓名" required />
            </div>
            <div class="form-group">
              <label>电话 <span class="req">*</span></label>
              <input v-model="form.phone" type="tel" placeholder="请输入联系电话" required />
            </div>
            <div class="form-group">
              <label>意向代理区域</label>
              <select v-model="form.intent_region">
                <option value="">请选择（选填）</option>
                <option value="华东">华东</option>
                <option value="华南">华南</option>
                <option value="华北">华北</option>
                <option value="华中">华中</option>
                <option value="西南">西南</option>
                <option value="西北">西北</option>
                <option value="东北">东北</option>
                <option value="其他">其他/海外</option>
              </select>
            </div>
            <div class="form-group">
              <label>投资预算区间</label>
              <select v-model="form.budget_range">
                <option value="">请选择（选填）</option>
                <option value="10万以下">10 万以下</option>
                <option value="10-30万">10-30 万</option>
                <option value="30-50万">30-50 万</option>
                <option value="50万以上">50 万以上</option>
                <option value="待定">待定/需评估</option>
              </select>
            </div>
            <div class="form-group">
              <label>邮箱</label>
              <input v-model="form.email" type="email" placeholder="选填" />
            </div>
            <div class="form-group">
              <label>留言 <span class="req">*</span></label>
              <textarea v-model="form.message" rows="4" placeholder="请描述您的需求，如负载、行程、应用场景等" required></textarea>
            </div>
            <button type="submit" class="btn btn-accent submit-btn" :disabled="submitting">
              {{ submitting ? '提交中...' : '提交咨询' }}
            </button>
            <p v-if="successMsg" class="success-msg">✓ {{ successMsg }}</p>
            <p v-if="errorMsg" class="error-msg">✗ {{ errorMsg }}</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { siteApi, contactApi } from '@/api'
import { useJsonLd, buildOrganizationSchema } from '@/composables/useJsonLd'

const config = ref({})
const form = ref({ name: '', phone: '', email: '', message: '', source: '', intent_region: '', budget_range: '', lead_source: '' })
const submitting = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

// 线索来源归因（GEO §3.4：ai / search / direct / other），用于统计 AI 引擎招商线索
const detectLeadSource = () => {
  const ref = (document.referrer || '').toLowerCase()
  const ua = (navigator.userAgent || '').toLowerCase()
  if (/openai|chatgpt|bing\.com\/chat|claude|anthropic|gemini|google\.com\/search.*ai|aibrowser|doubao|yuanbao|tongyi|qianwen|wenxin|baidu.*ai/.test(ref + ' ' + ua)) return 'ai'
  if (/baidu|google|bing|sogou|so\.com|360|haosou|yandex|duckduckgo/.test(ref)) return 'search'
  if (ref) return 'other'
  return 'direct'
}

// 注入 Organization 结构化数据
const { inject: injectOrgSchema } = useJsonLd('schema-organization')

// 将后端返回的字段级错误拼成可读文案（保留已填内容，不丢失）
const buildErrMsg = (res) => {
  const data = res && res.data
  if (data && typeof data === 'object') {
    const parts = []
    for (const [field, msgs] of Object.entries(data)) {
      const label = { name: '姓名', phone: '电话', email: '邮箱', message: '留言' }[field] || field
      const text = Array.isArray(msgs) ? msgs.join('；') : msgs
      parts.push(`${label}：${text}`)
    }
    if (parts.length) return '提交失败，请修正：' + parts.join('；')
  }
  return (res && res.message) || '提交失败，请稍后重试'
}

const submitForm = async () => {
  submitting.value = true
  successMsg.value = ''
  errorMsg.value = ''
  // 记录来源页面与线索归因
  form.value.source = window.location.pathname
  form.value.lead_source = detectLeadSource()

  // 转化事件埋点 - 百度统计（招商线索语义，SEO-skill §9.2）
  if (window._hmt) {
    window._hmt.push(['_trackEvent', '招商线索', '提交', '代理意向'])
  }
  // 转化事件埋点 - GTM（leadType / leadSource 供 GEO 归因，GEO §3.4）
  if (window.dataLayer) {
    window.dataLayer.push({
      event: 'lead_submit',
      leadType: 'franchise',
      leadSource: form.value.lead_source
    })
  }

  try {
    const res = await contactApi.submit(form.value)
    if (res.code === 200) {
      successMsg.value = '提交成功，我们会尽快与您联系！'
      // 仅成功时清空表单；失败保留已填内容，避免用户重复输入
      form.value = { name: '', phone: '', email: '', message: '', source: '', intent_region: '', budget_range: '', lead_source: '' }
    } else {
      // 优先展示后端返回的字段级校验错误，方便用户直接修改
      errorMsg.value = buildErrMsg(res)
    }
  } catch (e) {
    errorMsg.value = '网络错误，请稍后重试'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const res = await siteApi.getConfig()
    if (res.code === 200) {
      config.value = res.data
      injectOrgSchema(buildOrganizationSchema(res.data))
    }
  } catch (e) { console.error(e) }
})
</script>

<style scoped>
.page-title { text-align: center; font-size: 2rem; margin: 32px 0 8px; color: var(--text); }
.breadcrumb { padding: 16px 0 8px; font-size: 0.85rem; color: var(--text-light); }
.breadcrumb a { color: var(--text-light); }
.breadcrumb a:hover { color: var(--primary); }
.page-sub { margin-bottom: 32px; }
.contact-wrap { display: grid; grid-template-columns: 1fr; gap: 24px; max-width: 900px; margin: 0 auto; }
.contact-info h3 { margin-bottom: 16px; color: #fff; }
.info-item { display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border); }
.info-label { color: var(--text-light); width: 48px; flex-shrink: 0; }
.info-note { margin-top: 20px; color: var(--primary); font-size: 0.9rem; }
.info-note p { margin-bottom: 6px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 0.9rem; font-weight: 500; color: var(--text); }
.req { color: var(--primary); }
.form-group input, .form-group textarea {
  width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 6px;
  font-size: 0.95rem; font-family: inherit;
  background: var(--bg-input); color: var(--text);
  transition: border-color 0.2s;
}
.form-group input::placeholder, .form-group textarea::placeholder { color: #6b7280; }
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-soft); }
.submit-btn { width: 100%; margin-top: 8px; }
.success-msg { color: var(--success); margin-top: 12px; text-align: center; }
.error-msg { color: var(--danger); margin-top: 12px; text-align: center; }

@media (min-width: 768px) {
  .contact-wrap { grid-template-columns: 1fr 1.5fr; }
}
</style>
