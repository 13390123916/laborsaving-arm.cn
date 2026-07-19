/**
 * useJsonLd 组合式函数
 * 按类型注入 JSON-LD 结构化数据（Organization / FAQPage / Article）
 * 页面挂载时注入、卸载时自动清理，支持按 id 去重覆盖
 *
 * 用法示例：
 *   const { inject } = useJsonLd('organization')
 *   inject({ "@context": "https://schema.org", "@type": "Organization", ... })
 */
import { onUnmounted } from 'vue'

export function useJsonLd(schemaId) {
  /**
   * 注入 JSON-LD 到 <head>
   * @param {Object} schema - 符合 schema.org 标准的 JSON-LD 对象
   */
  const inject = (schema) => {
    // 移除同 id 的旧脚本（确保页面切换时不会残留）
    const existing = document.getElementById(schemaId)
    if (existing) existing.remove()

    const el = document.createElement('script')
    el.type = 'application/ld+json'
    el.id = schemaId
    el.textContent = JSON.stringify(schema)
    document.head.appendChild(el)
  }

  /**
   * 手动移除（onUnmounted 自动清理）
   */
  const remove = () => {
    const el = document.getElementById(schemaId)
    if (el) el.remove()
  }

  // 组件卸载时自动移除
  onUnmounted(remove)

  return { inject, remove }
}

// ===== Schema 构建器 =====

/**
 * 构建 Organization Schema（企业组织结构化数据）
 * 与后端 /schema/organization.json 对齐
 */
export function buildOrganizationSchema(config) {
  // 地理位置（GEO 结构化数据核心：GeoCoordinates 经纬度）
  const geo = (config.latitude != null && config.longitude != null)
    ? {
        '@type': 'GeoCoordinates',
        latitude: Number(config.latitude),
        longitude: Number(config.longitude)
      }
    : undefined

  // 采用 LocalBusiness（Organization 子类型），兼顾企业信息与本地 SEO 地理收录
  // GEO 增强：areaServed 用 Country CN（全国），sameAs 权威外链，makesOffer 招商语义
  const sameAs = (config.same_as && typeof config.same_as === 'string')
    ? config.same_as.split(/[,\n]/).map(s => s.trim()).filter(Boolean)
    : []

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name: config.company_name || 'LABOR-SAVING 智能装备有限公司',
    url: 'https://laborsaving-arm.cn',
    description: config.company_intro || config.site_description || '',
    foundingDate: config.founded_year ? String(config.founded_year) : '2015',
    address: {
      '@type': 'PostalAddress',
      streetAddress: config.office_address || '',
      addressLocality: config.address_locality || '沈阳市',
      addressRegion: config.address_region || '辽宁省',
      postalCode: config.postal_code || '',
      addressCountry: 'CN'
    },
    // GEO §3.2：areaServed 用 Country CN 表达"全国"，与 address 真实辽宁地址分离
    areaServed: { '@type': 'Country', name: 'CN' }
  }
  if (sameAs.length) schema.sameAs = sameAs
  // GEO §3.2：招商语义（Service + Offer），供 AI 识别企业招商能力
  schema.makesOffer = {
    '@type': 'Offer',
    category: '区域代理授权',
    description: '区域保护、价格政策、产品培训、售后技术支持',
    areaServed: { '@type': 'Country', name: 'CN' }
  }
  if (geo) schema.geo = geo
  if (config.contact_phone || config.contact_email) {
    schema.contactPoint = {
      '@type': 'ContactPoint',
      telephone: config.contact_phone || '',
      contactType: 'sales',
      email: config.contact_email || ''
    }
  }
  return schema
}

/**
 * 构建 FAQPage Schema（常见问题问答结构化数据）
 * 符合 Google 与 AI 搜索引擎优先收录标准
 */
export function buildFaqPageSchema(faqList) {
  const mainEntity = (faqList || [])
    .filter(f => f.is_active !== false)
    .map(f => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: (f.detail ? `${f.answer}\n\n${f.detail}` : f.answer) || ''
      }
    }))

  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity
  }
}

/**
 * 构建 Article Schema（资讯文章结构化数据）
 */
export function buildArticleSchema(article, siteConfig) {
  const companyName = siteConfig?.company_name || 'LABOR-SAVING 智能装备有限公司'
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title || '',
    description: article.summary || article.seo_description || '',
    author: {
      '@type': 'Organization',
      name: companyName
    },
    publisher: {
      '@type': 'Organization',
      name: companyName
    },
    datePublished: article.created_at || '',
    dateModified: article.updated_at || article.created_at || '',
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://laborsaving-arm.cn/news/${article.id}`
    }
  }
}
