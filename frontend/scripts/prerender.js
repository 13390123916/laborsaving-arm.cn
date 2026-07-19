/**
 * 构建期预渲染脚本 (SSG)
 * 使用 puppeteer-core 抓取 SPA 各路由的真实 DOM 并落盘为静态 HTML，
 * 解决纯 SPA 首屏空壳被搜索引擎 / AI 爬虫判定为无内容的问题。
 *
 * 用法:
 *   node scripts/prerender.js          # 自动管理 preview server 生命周期
 *   node scripts/prerender.js --no-server  # 假设 preview server 已在运行
 *
 * 前置条件: pnpm build 已执行，dist/ 目录存在
 *
 * 流程:
 *   1. 启动 vite preview (绑定 127.0.0.1:4173 避免 IPv6 冲突)
 *   2. puppeteer 逐路由访问, 等待 networkidle0 + 额外 1s 异步渲染
 *   3. 捕获纯 HTML, 写入 dist/<route>/index.html
 *   4. 写入 dist/404.html (serve 时作 SPA fallback)
 *   5. 杀死 preview 进程, 输出统计
 */

import { launch } from 'puppeteer-core'
import { spawn, execSync } from 'child_process'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'
import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const PROJECT_ROOT = resolve(__dirname, '..')
const DIST_DIR = resolve(PROJECT_ROOT, 'dist')

// ===== 配置 =====
const PREVIEW_HOST = '127.0.0.1'
const PREVIEW_PORT = 4173
const PREVIEW_URL = `http://${PREVIEW_HOST}:${PREVIEW_PORT}`
const CHROME_BIN = process.env.CHROME_BIN || '/usr/bin/chromium'
const RENDER_WAIT_MS = 1000
const NO_SERVER = process.argv.includes('--no-server')

// 静态路由（核心栏目页）
const STATIC_ROUTES = [
  { path: '/', name: '首页' },
  { path: '/about', name: '关于我们' },
  { path: '/news', name: '资讯中心' },
  { path: '/faq', name: 'FAQ' },
  { path: '/contact', name: '联系我们' },
]

// 资讯详情路由：从后端 API 动态拉取**全部**已发布文章，
// 避免硬编码 /news/1..6 导致其余详情页对爬虫/AI 引擎不可见（GEO 空壳风险）。
const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8000'

async function fetchArticleRoutes() {
  const routes = []
  try {
    let page = 1
    while (true) {
      const res = await fetch(`${API_BASE}/api/articles/?page=${page}&page_size=100`)
      if (!res.ok) break
      const json = await res.json()
      const list = json?.data?.list || []
      for (const a of list) {
        // slug 为空时回退数字 ID，与前端路由 /news/:id 对齐
        const seg = a.slug ? encodeURIComponent(a.slug) : a.id
        routes.push({ path: `/news/${seg}`, name: `资讯详情${a.id || seg}` })
      }
      const total = json?.data?.total || 0
      const fetched = (page - 1) * 100 + list.length
      if (list.length === 0 || fetched >= total) break
      page++
    }
  } catch (e) {
    console.warn(`   ⚠ 拉取资讯列表失败，回退 /news/1..6：${e.message}`)
    for (let i = 1; i <= 6; i++) routes.push({ path: `/news/${i}`, name: `资讯详情${i}` })
  }
  return routes
}

async function buildRoutes() {
  const articleRoutes = await fetchArticleRoutes()
  console.log(`   静态路由 ${STATIC_ROUTES.length} 条 + 资讯详情 ${articleRoutes.length} 条`)
  return [...STATIC_ROUTES, ...articleRoutes]
}

/** 写入 HTML 到目标路径 */
function writeHtml(routePath, html) {
  const cleanPath = routePath.split('?')[0].split('#')[0]
  const isRoot = cleanPath === '/' || cleanPath === ''
  const outDir = isRoot ? DIST_DIR : resolve(DIST_DIR, cleanPath.slice(1))
  const outFile = resolve(outDir, 'index.html')
  if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true })
  writeFileSync(outFile, html, 'utf-8')
  return outFile
}

/** 等待服务可访问 */
async function waitForServer(url, maxRetries = 30) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const resp = await fetch(url)
      if (resp.ok) return true
    } catch { /* retry */ }
    await new Promise((r) => setTimeout(r, 500))
  }
  throw new Error(`服务 ${url} 在 ${maxRetries * 500}ms 内未就绪`)
}

async function main() {
  console.log('=== SSG 预渲染开始 ===')
  console.log(`Chromium: ${CHROME_BIN}, 输出: ${DIST_DIR}`)

  if (!existsSync(DIST_DIR)) {
    console.error('错误: dist/ 不存在。请先执行 pnpm build')
    process.exit(1)
  }

  let serverProc = null

  // 不需要外部 server 管理时，启动 preview server
  if (!NO_SERVER) {
    console.log('\n[1/4] 启动 vite preview...')
    const viteBin = resolve(PROJECT_ROOT, 'node_modules', '.bin', 'vite')
    serverProc = spawn(viteBin, ['preview', '--host', PREVIEW_HOST, '--port', String(PREVIEW_PORT), '--strictPort'], {
      cwd: PROJECT_ROOT,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, NODE_ENV: 'production' },
    })
    serverProc.stderr.on('data', (d) => { /* vite 地址信息输出到 stderr */ })
    await waitForServer(PREVIEW_URL)
    console.log(`   ✓ ${PREVIEW_URL}`)
  } else {
    console.log('\n[1/4] 跳过 server 启动 (--no-server)')
    await waitForServer(PREVIEW_URL)
    console.log(`   ✓ ${PREVIEW_URL}`)
  }

  // 启动浏览器
  console.log('\n[2/4] 启动浏览器...')
  let browser
  try {
    browser = await launch({
      executablePath: CHROME_BIN,
      headless: true,
      args: [
        '--no-sandbox', '--disable-setuid-sandbox',
        '--disable-dev-shm-usage', '--disable-gpu',
        '--disable-extensions', '--mute-audio', '--no-first-run',
      ],
    })
  } catch (err) {
    if (serverProc) serverProc.kill('SIGTERM')
    console.error('   ✗', err.message)
    process.exit(1)
  }
  console.log(`   ✓ 浏览器已启动`)

  // 预渲染路由：静态路由 + 动态拉取的全部已发布资讯
  console.log('[3/4] 预渲染路由...')
  const ROUTES = await buildRoutes()
  console.log(`   ✓ 共 ${ROUTES.length} 条路由`)
  const results = []
  const page = await browser.newPage()
  await page.setViewport({ width: 1920, height: 1080 })
  await page.setUserAgent(
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
  )

  for (const route of ROUTES) {
    const url = `${PREVIEW_URL}${route.path}`
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 })
      await new Promise((r) => setTimeout(r, RENDER_WAIT_MS))
      const html = await page.content()
      writeHtml(route.path, html)
      const size = (html.length / 1024).toFixed(1)
      console.log(`   ✓ ${route.path.padEnd(20)} ${route.name.padEnd(12)} ${size}KB`)
      results.push({ route: route.path, name: route.name, size: `${size}KB` })
    } catch (err) {
      console.error(`   ✗ ${route.path.padEnd(20)} ${route.name} - ${err.message}`)
      results.push({ route: route.path, name: route.name, size: 'FAIL' })
    }
  }

  await page.close()
  await browser.close()

  // 404 回退页
  console.log('\n[4/4] 生成 404 回退页...')
  if (existsSync(resolve(DIST_DIR, 'index.html'))) {
    const indexHtml = readFileSync(resolve(DIST_DIR, 'index.html'), 'utf-8')
    const fallbackDir = resolve(DIST_DIR, '404')
    if (!existsSync(fallbackDir)) mkdirSync(fallbackDir, { recursive: true })
    writeFileSync(resolve(fallbackDir, 'index.html'), indexHtml, 'utf-8')
    writeFileSync(resolve(DIST_DIR, '404.html'), indexHtml, 'utf-8')
    console.log('   ✓ 404/ 已生成')
  }

  // 关闭 server
  if (serverProc) {
    serverProc.kill('SIGTERM')
    console.log('   ✓ 预览服务已关闭')
  }

  // 统计
  console.log('\n=== SSG 预渲染完成 ===')
  const ok = results.filter((r) => r.size !== 'FAIL').length
  console.log(`成功率: ${ok}/${results.length}`)
  results.filter((r) => r.size === 'FAIL').forEach((r) => console.log(`   ✗ ${r.route}`))
  const total = results.filter((r) => r.size !== 'FAIL').reduce((a, r) => a + parseFloat(r.size), 0)
  console.log(`HTML 总量: ~${total.toFixed(0)}KB`)
}

main().catch((err) => {
  console.error('预渲染失败:', err)
  process.exit(1)
})
