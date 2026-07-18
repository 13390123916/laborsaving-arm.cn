// SEO 插件 - 动态注入 TDK、统计代码、结构化数据
import { siteApi } from '@/api'

// 全局统计代码配置（百度、360、Google）
const STATS_CONFIG = {
  // 百度统计 - 后台配置 hm.js
  baiduTongji: '',
  // 百度自动推送 - zz.bdstatic.com
  baiduPush: true,
  // 360 自动收录 - qhres2.com/sozz
  qihuPush: true,
  // Google Analytics / GTM
  gtmId: ''
}

// 注入统计脚本
function injectStatsScripts(config) {
  // 百度统计
  if (config.baidu_tongji) {
    const hm = document.createElement('script')
    hm.src = `https://hm.baidu.com/hm.js?${config.baidu_tongji}`
    hm.async = true
    document.head.appendChild(hm)
  }
  // 百度自动推送
  if (STATS_CONFIG.baiduPush) {
    const push = document.createElement('script')
    push.src = 'https://zz.bdstatic.com/linksubmit/push.js'
    push.async = true
    document.head.appendChild(push)
  }
  // 360 自动收录
  if (STATS_CONFIG.qihuPush) {
    const sozz = document.createElement('script')
    sozz.src = 'https://jspassport.360.cn/360/loader.js'
    sozz.async = true
    document.head.appendChild(sozz)
  }
  // GTM
  if (config.gtm_id) {
    const gtm = document.createElement('script')
    gtm.src = `https://www.googletagmanager.com/gtm.js?id=${config.gtm_id}`
    gtm.async = true
    document.head.appendChild(gtm)
  }
}

// 更新站长验证 meta
function updateVerifyMeta(config) {
  const setMeta = (id, content) => {
    const el = document.getElementById(id)
    if (el && content) el.setAttribute('content', content)
  }
  setMeta('baidu-verify', config.baidu_verify)
  setMeta('qihu-verify', config.qihu_verify)
  setMeta('sogou-verify', config.sogou_verify)
  setMeta('google-verify', config.google_verify)
}

// 动态设置页面 TDK
function setTDK(tdk) {
  if (!tdk) return
  document.title = tdk.title || document.title

  const setMetaTag = (name, content) => {
    if (!content) return
    let el = document.querySelector(`meta[name="${name}"]`)
    if (!el) {
      el = document.createElement('meta')
      el.setAttribute('name', name)
      document.head.appendChild(el)
    }
    el.setAttribute('content', content)
  }
  setMetaTag('keywords', tdk.keywords)
  setMetaTag('description', tdk.description)
}

// 写入结构化数据 Schema（JSON-LD）
function setSchemaJsonLd(schema) {
  let el = document.getElementById('schema-jsonld')
  if (!el) {
    el = document.createElement('script')
    el.type = 'application/ld+json'
    el.id = 'schema-jsonld'
    document.head.appendChild(el)
  }
  el.textContent = JSON.stringify(schema)
}

export default {
  install(app) {
    // 应用启动时加载站点配置并注入统计代码
    siteApi.getConfig().then(res => {
      if (res.code === 200) {
        const config = res.data
        injectStatsScripts(config)
        updateVerifyMeta(config)
      }
    }).catch(() => {})

    // 提供全局方法供页面调用
    app.config.globalProperties.$seo = {
      setTDK,
      setSchemaJsonLd
    }
  }
}
