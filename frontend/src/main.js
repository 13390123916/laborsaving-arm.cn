// 应用入口 - Vue3 主文件
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/style.css'
import seoPlugin from './plugins/seo'

const app = createApp(App)
app.use(router)
app.use(seoPlugin)
app.mount('#app')
