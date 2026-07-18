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
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: config.company_name || 'LABOR-SAVING 智能装备有限公司',
    url: 'https://laborsaving-arm.cn',
    description: config.company_intro || config.site_description || '',
    foundingDate: config.founded_year ? String(config.founded_year) : '2015',
    address: {
      '@type': 'PostalAddress',
      streetAddress: config.office_address || '',
      addressCountry: 'CN'
    },
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: config.contact_phone || '',
      contactType: 'sales',
      email: config.contact_email || ''
    }
  }
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
