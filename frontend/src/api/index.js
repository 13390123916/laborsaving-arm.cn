// API 请求封装 - axios 统一配置
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.PROD ? '/api' : '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 响应拦截器 - 统一处理返回格式
api.interceptors.response.use(
  (response) => {
    // Django REST 返回 {code, message, data}
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api

// ===== 接口方法 =====
export const siteApi = {
  getConfig: () => api.get('/site-config/info/')
}

export const articleApi = {
  list: (params) => api.get('/articles/', { params }),
  detail: (id) => api.get(`/articles/${id}/`),
  categories: () => api.get('/articles/categories/')
}

export const faqApi = {
  list: (params) => api.get('/faqs/', { params })
}

export const contactApi = {
  submit: (data) => api.post('/contacts/', data),
  stats: () => api.get('/contacts/stats/')
}

export const productApi = {
  list: () => api.get('/products/')
}
