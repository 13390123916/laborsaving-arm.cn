<template>
  <div class="contact-page">
    <div class="container">
      <h1 class="page-title">联系我们</h1>
      <p class="page-sub text-center text-light">填写下方表单，专业工程师将在24小时内与您联系</p>

      <div class="contact-wrap">
        <!-- 左侧信息 -->
        <div class="contact-info">
          <h3>联系方式</h3>
          <div class="info-item">
            <span class="info-label">电话</span>
            <span>{{ config.contact_phone || '400-888-xxxx' }}</span>
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
            <span>{{ config.office_address || '山东青岛' }}</span>
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

const config = ref({})
const form = ref({ name: '', phone: '', email: '', message: '', source: '' })
const submitting = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

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
  // 记录来源页面
  form.value.source = window.location.pathname

  // 转化事件埋点 - 百度统计
  if (window._hmt) {
    window._hmt.push(['_trackEvent', 'form', 'submit', 'contact_form'])
  }
  // 转化事件埋点 - GTM
  if (window.dataLayer) {
    window.dataLayer.push({ event: 'form_submit', form_type: 'contact' })
  }

  try {
    const res = await contactApi.submit(form.value)
    if (res.code === 200) {
      successMsg.value = '提交成功，我们会尽快与您联系！'
      // 仅成功时清空表单；失败保留已填内容，避免用户重复输入
      form.value = { name: '', phone: '', email: '', message: '', source: '' }
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
    if (res.code === 200) config.value = res.data
  } catch (e) { console.error(e) }
})
</script>

<style scoped>
.page-title { text-align: center; font-size: 2rem; margin: 32px 0 8px; }
.page-sub { margin-bottom: 32px; }
.contact-wrap { display: grid; grid-template-columns: 1fr; gap: 24px; max-width: 900px; margin: 0 auto; }
.contact-info h3 { margin-bottom: 16px; color: var(--primary); }
.info-item { display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border); }
.info-label { color: var(--text-light); width: 48px; flex-shrink: 0; }
.info-note { margin-top: 20px; color: var(--accent); font-size: 0.9rem; }
.info-note p { margin-bottom: 6px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 0.9rem; font-weight: 500; }
.req { color: #e74c3c; }
.form-group input, .form-group textarea {
  width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 6px;
  font-size: 0.95rem; font-family: inherit;
}
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: var(--primary); }
.submit-btn { width: 100%; margin-top: 8px; }
.success-msg { color: #27ae60; margin-top: 12px; text-align: center; }
.error-msg { color: #e74c3c; margin-top: 12px; text-align: center; }

@media (min-width: 768px) {
  .contact-wrap { grid-template-columns: 1fr 1.5fr; }
}
</style>
