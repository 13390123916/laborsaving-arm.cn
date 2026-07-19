/* 运行时 + SEO 注入调试脚本（puppeteer-core 无头渲染）
 * 路径基于脚本自身位置，克隆到任意目录均可运行 */
const path = require('path')
const puppeteer = require(path.resolve(__dirname, 'frontend/node_modules/puppeteer-core'))
const { spawn } = require('child_process')
const { execSync } = require('child_process')

const ROOT = __dirname
const CHROME_BIN = '/usr/bin/chromium'
const HOST = '127.0.0.1'
const PREVIEW_PORT = 4173
const API_BASE = 'http://127.0.0.1:8000'
const PREVIEW_URL = `http://${HOST}:${PREVIEW_PORT}`

const ROUTES = ['/', '/about', '/news', '/news/1', '/faq', '/contact']

async function waitServer(url, tries = 40) {
  for (let i = 0; i < tries; i++) {
    try { execSync(`curl -s -o /dev/null ${url}`); return true } catch (e) {}
    await new Promise(r => setTimeout(r, 500))
  }
  return false
}

async function main() {
  // 启动后端
  const backend = spawn('python3', ['manage.py', 'runserver', `${HOST}:8000`], {
    cwd: path.resolve(ROOT, 'backend'), stdio: 'ignore', detached: true
  })
  // 启动前端预览
  const preview = spawn('pnpm', ['exec', 'vite', 'preview', '--host', HOST, '--port', String(PREVIEW_PORT), '--strictPort'], {
    cwd: path.resolve(ROOT, 'frontend'), stdio: 'ignore', detached: true, shell: true
  })

  const okB = await waitServer(`${API_BASE}/api/site-config/info/`)
  const okP = await waitServer(PREVIEW_URL + '/')
  console.log('backend ready:', okB, '| preview ready:', okP)
  if (!okB || !okP) { console.error('server not ready'); process.exit(1) }

  const browser = await puppeteer.launch({
    executablePath: CHROME_BIN,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  })

  for (const route of ROUTES) {
    const page = await browser.newPage()
    const consoleErrors = []
    const pageErrors = []
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()) })
    page.on('pageerror', e => pageErrors.push(e.message))
    const url = PREVIEW_URL + route
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 })
    await new Promise(r => setTimeout(r, 1200)) // 等待异步 SEO 注入

    const data = await page.evaluate(() => {
      const meta = (n) => { const e = document.querySelector(`meta[name="${n}"]`); return e ? e.getAttribute('content') : null }
      const verify = (id) => { const e = document.getElementById(id); return e ? e.getAttribute('content') : null }
      const jsonld = Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => {
        try { const o = JSON.parse(s.textContent); return o['@type'] || 'unknown' } catch (e) { return 'PARSE_ERR' }
      })
      const appHtml = document.getElementById('app') ? document.getElementById('app').innerText.slice(0, 80) : ''
      return {
        title: document.title,
        keywords: meta('keywords'),
        description: meta('description'),
        baidu_verify: verify('baidu-verify'),
        qihu_verify: verify('qihu-verify'),
        sogou_verify: verify('sogou-verify'),
        google_verify: verify('google-verify'),
        jsonld,
        appLen: appHtml.length
      }
    })
    console.log(`\n===== ${route} =====`)
    console.log('title      :', data.title)
    console.log('keywords   :', (data.keywords || '').slice(0, 70))
    console.log('description:', (data.description || '').slice(0, 70))
    console.log('verify meta:', JSON.stringify({ baidu: data.baidu_verify, qihu: data.qihu_verify, sogou: data.sogou_verify, google: data.google_verify }))
    console.log('JSON-LD    :', data.jsonld.join(', '))
    console.log('#app text  :', data.appLen, 'chars')
    console.log('consoleErr :', consoleErrors.length ? consoleErrors.join(' | ') : 'none')
    console.log('pageErr    :', pageErrors.length ? pageErrors.join(' | ') : 'none')
    await page.close()
  }

  await browser.close()
  try { process.kill(-backend.pid) } catch (e) {}
  try { process.kill(-preview.pid) } catch (e) {}
  console.log('\n[done]')
}
main().catch(e => { console.error('FATAL', e); process.exit(1) })
