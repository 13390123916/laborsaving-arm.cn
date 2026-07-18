// SEO 插件 - 动态注入 TDK、统计代码、结构化数据
// 同时导出底层方法，供 router.afterEach 与 useJsonLd 组合式复用
import { siteApi } from '@/api'

// 全局统计代码开关配置（百度、360、Google）
const STATS_CONFIG = {
  // 百度统计 - 后台配置 hm.js
  baiduTongji: true,
  // 百度自动推送 - zz.bdstatic.com
  baiduPush: true,
  // 360 自动收录 - 规范的 qhres2.com/sozz 加载器
  qihuPush: true,
  // Google Analytics / GTM
  gtm: true
}

// 站点配置缓存（启动拉取后供路由 TDK、JSON-LD 复用，避免重复请求）
let siteConfigCache = null

// 注入统计与站长验证脚本
function injectStatsScripts(config) {
  // 百度统计
  if (STATS_CONFIG.baiduTongji && config.baidu_tongji) {
    const hm = document.createElement('script')
    hm.src = `https://hm.baidu.com/hm.js?${config.baidu_tongji}`
    hm.async = true
    document.head.appendChild(hm)
  }
  // 百度自动推送（链接主动提交，加速收录）
  if (STATS_CONFIG.baiduPush) {
    const push = document.createElement('script')
    push.src = 'https://zz.bdstatic.com/linksubmit/push.js'
    push.async = true
    document.head.appendChild(push)
  }
  // 360 自动收录（规范地址：qhres2.com/sozz 加载器，脚本节点 id=sozz）
  if (STATS_CONFIG.qihuPush) {
    const sozz = document.createElement('script')
    sozz.src = 'https://s.ssl.qhres2.com/ssl/ab77b6ea7ac43b89.js'
    sozz.async = true
    sozz.id = 'sozz'
    document.head.appendChild(sozz)
  }
  // Google Tag Manager
  if (STATS_CONFIG.gtm && config.gtm_id) {
    const gtm = document.createElement('script')
    gtm.src = `https://www.googletagmanager.com/gtm.js?id=${config.gtm_id}`
    gtm.async = true
    document.head.appendChild(gtm)
  }
  // Google Analytics（与 GTM 二选一，这里仅在配置了 ga_id 时补充）
  if (config.google_ga_id) {
    const ga = document.createElement('script')
    ga.async = true
    ga.src = `https://www.googletagmanager.com/gtag/js?id=${config.google_ga_id}`
    document.head.appendChild(ga)
    const gtagInit = document.createElement('script')
    gtagInit.textContent =
      `window.dataLayer = window.dataLayer || [];` +
      `function gtag(){dataLayer.push(arguments);}` +
      `gtag('js', new Date());` +
      `gtag('config', '${config.google_ga_id}');`
    document.head.appendChild(gtagInit)
  }
}

// 更新站长验证 meta（百度/360/搜狗/Google）
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

// 动态设置页面 TDK（title / keywords / description）
function setTDK(tdk) {
  if (!tdk) return
  if (tdk.title) document.title = tdk.title

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

// 写入结构化数据 Schema（JSON-LD），按 id 区分页面互不覆盖
function setSchemaJsonLd(schema, id = 'schema-jsonld') {
  let el = document.getElementById(id)
  if (!el) {
    el = document.createElement('script')
    el.type = 'application/ld+json'
    el.id = id
    document.head.appendChild(el)
  }
  el.textContent = JSON.stringify(schema)
}

// 读取站点配置缓存（供 router、组合式复用）
function getSiteConfig() {
  return siteConfigCache
}

export { setTDK, setSchemaJsonLd, getSiteConfig }

export default {
  install(app) {
    // 应用启动时加载站点配置并注入统计代码与验证 meta
    siteApi.getConfig().then(res => {
      if (res.code === 200) {
        siteConfigCache = res.data
        injectStatsScripts(res.data)
        updateVerifyMeta(res.data)
      }
    }).catch(() => {})

    // 暴露全局方法供页面调用
    app.config.globalProperties.$seo = {
      setTDK,
      setSchemaJsonLd,
      getSiteConfig
    }
  }
}
